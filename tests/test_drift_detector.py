# SPDX-License-Identifier: GPL-3.0-only
"""Tests for DriftEvent, DriftSeverity, and DriftDetector."""

import unittest
from velvet_continuity import (
    DriftDetector, DriftEvent, DriftSeverity, IdentityRecord, ValidationError,
)

VALID_IDENTITY = dict(
    instance_id="node-001",
    name="Node Alpha",
    role="navigator",
    runtime_class="embedded-node",
    surface="nav",
    memory_scope="local-bounded",
    authority_scope="court-gated",
    receipt_chain_anchor="sha256:genesis",
)


class TestDriftSeverityEnum(unittest.TestCase):

    def test_all_values_present(self):
        values = {s.value for s in DriftSeverity}
        self.assertIn("info", values)
        self.assertIn("low", values)
        self.assertIn("medium", values)
        self.assertIn("high", values)
        self.assertIn("critical", values)

    def test_string_comparison(self):
        self.assertEqual(DriftSeverity.CRITICAL, "critical")


class TestDriftEventConstruction(unittest.TestCase):

    def test_valid_construction(self):
        e = DriftEvent(
            drift_type="surface",
            severity="medium",
            expected="nav",
            observed="audio",
            action="review",
        )
        self.assertEqual(e.drift_type, "surface")
        self.assertEqual(e.severity, "medium")

    def test_invalid_severity_fails_closed(self):
        with self.assertRaises(ValueError):
            DriftEvent(
                drift_type="surface",
                severity="extreme",
                expected="nav",
                observed="audio",
                action="review",
            )

    def test_blank_drift_type_fails_closed(self):
        with self.assertRaises(ValidationError):
            DriftEvent(drift_type="", severity="low", expected="a", observed="b", action="review")

    def test_blank_action_fails_closed(self):
        with self.assertRaises(ValidationError):
            DriftEvent(drift_type="surface", severity="low", expected="a", observed="b", action="")

    def test_notes_defaults_to_empty_string(self):
        e = DriftEvent(drift_type="surface", severity="low", expected="a", observed="b", action="review")
        self.assertEqual(e.notes, "")

    def test_notes_non_string_raises(self):
        with self.assertRaises(TypeError):
            DriftEvent(drift_type="s", severity="low", expected="a", observed="b", action="r", notes=123)

    def test_is_critical_true(self):
        e = DriftEvent(drift_type="authority_scope", severity="critical", expected="a", observed="b", action="quarantine_and_review")
        self.assertTrue(e.is_critical())

    def test_is_critical_false(self):
        e = DriftEvent(drift_type="surface", severity="medium", expected="a", observed="b", action="review")
        self.assertFalse(e.is_critical())

    def test_is_actionable_medium_and_above(self):
        for sev in ("medium", "high", "critical"):
            e = DriftEvent(drift_type="x", severity=sev, expected="a", observed="b", action="review")
            self.assertTrue(e.is_actionable(), f"{sev} should be actionable")

    def test_is_not_actionable_below_medium(self):
        for sev in ("info", "low"):
            e = DriftEvent(drift_type="x", severity=sev, expected="a", observed="b", action="review")
            self.assertFalse(e.is_actionable(), f"{sev} should not be actionable")

    def test_to_dict_keys(self):
        e = DriftEvent(drift_type="surface", severity="medium", expected="nav", observed="audio", action="review")
        d = e.to_dict()
        for key in ("event_id", "drift_type", "severity", "expected", "observed", "action", "notes", "created_at"):
            self.assertIn(key, d)

    def test_frozen(self):
        e = DriftEvent(drift_type="surface", severity="low", expected="a", observed="b", action="review")
        with self.assertRaises((AttributeError, TypeError)):
            e.severity = "high"


class TestDriftDetectorCompareIdentity(unittest.TestCase):

    def setUp(self):
        self.detector = DriftDetector()

    def test_identical_records_produce_no_events(self):
        r = IdentityRecord(**VALID_IDENTITY)
        events = self.detector.compare_identity(r, r)
        self.assertEqual(events, [])

    def test_surface_mismatch_produces_medium_event(self):
        expected = IdentityRecord(**VALID_IDENTITY)
        observed = IdentityRecord(**{**VALID_IDENTITY, "surface": "audio"})
        events = self.detector.compare_identity(expected, observed)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].drift_type, "surface")
        self.assertEqual(events[0].severity, "medium")

    def test_authority_scope_mismatch_is_critical(self):
        expected = IdentityRecord(**VALID_IDENTITY)
        observed = IdentityRecord(**{**VALID_IDENTITY, "authority_scope": "unrestricted"})
        events = self.detector.compare_identity(expected, observed)
        critical = [e for e in events if e.drift_type == "authority_scope"]
        self.assertEqual(len(critical), 1)
        self.assertEqual(critical[0].severity, "critical")

    def test_multiple_drifts_detected(self):
        expected = IdentityRecord(**VALID_IDENTITY)
        observed = IdentityRecord(**{**VALID_IDENTITY, "surface": "audio", "role": "coordinator"})
        events = self.detector.compare_identity(expected, observed)
        drift_types = {e.drift_type for e in events}
        self.assertIn("surface", drift_types)
        self.assertIn("role", drift_types)

    def test_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.detector.compare_identity("not-a-record", IdentityRecord(**VALID_IDENTITY))


class TestDriftDetectorRequireReceiptAnchor(unittest.TestCase):

    def setUp(self):
        self.detector = DriftDetector()

    def test_missing_anchor_produces_critical_event(self):
        r = IdentityRecord(**{**VALID_IDENTITY, "receipt_chain_anchor": None})
        events = self.detector.require_receipt_anchor(r)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].severity, "critical")

    def test_present_anchor_produces_no_events(self):
        r = IdentityRecord(**VALID_IDENTITY)
        events = self.detector.require_receipt_anchor(r)
        self.assertEqual(events, [])

    def test_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            self.detector.require_receipt_anchor("not-a-record")


class TestDriftDetectorHelpers(unittest.TestCase):

    def setUp(self):
        self.detector = DriftDetector()

    def _event(self, severity):
        return DriftEvent(drift_type="x", severity=severity, expected="a", observed="b", action="review")

    def test_has_critical_drift_true(self):
        events = [self._event("medium"), self._event("critical")]
        self.assertTrue(self.detector.has_critical_drift(events))

    def test_has_critical_drift_false(self):
        events = [self._event("medium"), self._event("high")]
        self.assertFalse(self.detector.has_critical_drift(events))

    def test_highest_severity_empty_returns_none(self):
        self.assertIsNone(self.detector.highest_severity([]))

    def test_highest_severity_returns_max(self):
        events = [self._event("low"), self._event("high"), self._event("medium")]
        self.assertEqual(self.detector.highest_severity(events), "high")


if __name__ == "__main__":
    unittest.main()
