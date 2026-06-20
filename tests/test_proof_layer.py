# SPDX-License-Identifier: GPL-3.0-only
"""
Tests for the v0.1.1 mechanical continuity proof layer.

velvet_continuity.proof_records
velvet_continuity.proof_hashing
velvet_continuity.proof_verify
velvet_continuity.proof_surface

Coverage targets (per spec):
  - valid genesis verifies
  - valid two-record successor chain verifies
  - valid chain returns tail authority
  - failed chain returns authority 0
  - blank genesis_proof / model_fp / surface_fp rejected
  - context hash values must be non-empty strings
  - intentional empty context list is allowed
  - negative authority rejected
  - authority_level == 0 allowed
  - wrong key fails / downgrades authority
  - tampered integrity tag fails
  - broken previous_hash fails
  - lineage_root mutation fails
  - instance id mutation fails
  - valid LineageEvent verifies
  - tampered LineageEvent fails
  - identity hash ignores integrity_tag
  - lineage event hash ignores integrity_tag
"""

import unittest
from dataclasses import replace

from velvet_continuity.proof_hashing import (
    lineage_event_hash,
    proof_identity_hash,
)
from velvet_continuity.proof_surface import generate_surface_fingerprint
from velvet_continuity.proof_verify import (
    create_genesis_identity,
    create_lineage_event,
    create_successor_identity,
    verify_lineage_chain,
    verify_lineage_event,
)
from velvet_continuity.validation import ValidationError

KEY = b"test-local-key"
PROOF = "genesis-proof-placeholder"
MODEL = "model:v1"


def _genesis(
    key: bytes = KEY,
    proof: str = PROOF,
    model: str = MODEL,
    surface: str = "surface:test",
    authority_level: int = 1,
) -> object:
    return create_genesis_identity(proof, model, surface, key, authority_level=authority_level)


# ---------------------------------------------------------------------------
# Genesis creation and verification
# ---------------------------------------------------------------------------

class TestGenesisCreation(unittest.TestCase):

    def test_valid_genesis_id_format(self):
        g = _genesis()
        self.assertTrue(g.id.startswith("velvet:instance:"))

    def test_valid_genesis_lineage_root_matches_id_suffix(self):
        g = _genesis()
        self.assertEqual(g.id, f"velvet:instance:{g.lineage_root}")

    def test_valid_genesis_previous_hash_is_none(self):
        g = _genesis()
        self.assertIsNone(g.previous_hash)

    def test_valid_genesis_integrity_tag_set(self):
        g = _genesis()
        self.assertTrue(g.integrity_tag)

    def test_valid_genesis_verifies(self):
        g = _genesis()
        valid, errors, authority = verify_lineage_chain([g], KEY)
        self.assertTrue(valid)
        self.assertEqual(errors, [])
        self.assertEqual(authority, 1)

    def test_genesis_ts_is_positive_int(self):
        g = _genesis()
        self.assertIsInstance(g.genesis_ts, int)
        self.assertGreater(g.genesis_ts, 0)

    def test_genesis_active_context_hashes_stored_as_tuple(self):
        g = _genesis()
        self.assertIsInstance(g.active_context_hashes, tuple)


# ---------------------------------------------------------------------------
# Input validation — genesis factory
# ---------------------------------------------------------------------------

class TestGenesisInputValidation(unittest.TestCase):

    def test_blank_genesis_proof_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity("", MODEL, "surface", KEY)

    def test_whitespace_genesis_proof_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity("   ", MODEL, "surface", KEY)

    def test_blank_model_fp_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(PROOF, "", "surface", KEY)

    def test_blank_surface_fp_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(PROOF, MODEL, "", KEY)

    def test_empty_local_key_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(PROOF, MODEL, "surface", b"")

    def test_non_bytes_local_key_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(PROOF, MODEL, "surface", "not-bytes")  # type: ignore

    def test_negative_authority_level_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(PROOF, MODEL, "surface", KEY, authority_level=-1)

    def test_authority_level_zero_allowed(self):
        g = create_genesis_identity(PROOF, MODEL, "surface", KEY, authority_level=0)
        self.assertEqual(g.authority_level, 0)

    def test_bool_authority_level_rejected(self):
        # bool is a subclass of int in Python — we explicitly reject it
        with self.assertRaises(ValidationError):
            create_genesis_identity(PROOF, MODEL, "surface", KEY, authority_level=True)  # type: ignore

    def test_float_authority_level_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(PROOF, MODEL, "surface", KEY, authority_level=1.5)  # type: ignore


# ---------------------------------------------------------------------------
# Context hash validation
# ---------------------------------------------------------------------------

class TestContextHashValidation(unittest.TestCase):

    def test_empty_context_list_allowed(self):
        g = create_genesis_identity(PROOF, MODEL, "surface", KEY, active_context_hashes=[])
        self.assertEqual(g.active_context_hashes, ())

    def test_valid_context_hashes_stored(self):
        hashes = ["sha256:aaa", "sha256:bbb"]
        g = create_genesis_identity(PROOF, MODEL, "surface", KEY, active_context_hashes=hashes)
        self.assertEqual(g.active_context_hashes, tuple(hashes))

    def test_non_string_in_context_hashes_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(
                PROOF, MODEL, "surface", KEY, active_context_hashes=[1, 2, 3]  # type: ignore
            )

    def test_empty_string_in_context_hashes_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(
                PROOF, MODEL, "surface", KEY, active_context_hashes=["sha256:aaa", ""]
            )

    def test_bare_string_as_context_hashes_rejected(self):
        with self.assertRaises(ValidationError):
            create_genesis_identity(
                PROOF, MODEL, "surface", KEY, active_context_hashes="sha256:aaa"  # type: ignore
            )

    def test_successor_empty_context_list_allowed(self):
        g = _genesis()
        s = create_successor_identity(g, KEY, active_context_hashes=[])
        self.assertEqual(s.active_context_hashes, ())

    def test_successor_non_string_context_rejected(self):
        g = _genesis()
        with self.assertRaises(ValidationError):
            create_successor_identity(g, KEY, active_context_hashes=[123])  # type: ignore


# ---------------------------------------------------------------------------
# Successor identity and chain verification
# ---------------------------------------------------------------------------

class TestSuccessorChain(unittest.TestCase):

    def test_successor_inherits_id_and_lineage_root(self):
        g = _genesis()
        s = create_successor_identity(g, KEY, model_fp="model:v2")
        self.assertEqual(s.id, g.id)
        self.assertEqual(s.lineage_root, g.lineage_root)

    def test_successor_previous_hash_matches_genesis_hash(self):
        g = _genesis()
        s = create_successor_identity(g, KEY)
        self.assertEqual(s.previous_hash, proof_identity_hash(g))

    def test_valid_two_record_chain_verifies(self):
        g = _genesis()
        s = create_successor_identity(g, KEY, model_fp="model:v2")
        valid, errors, authority = verify_lineage_chain([g, s], KEY)
        self.assertTrue(valid)
        self.assertEqual(errors, [])

    def test_valid_chain_returns_tail_authority(self):
        g = _genesis(authority_level=1)
        s = create_successor_identity(g, KEY, authority_level=3)
        valid, errors, authority = verify_lineage_chain([g, s], KEY)
        self.assertTrue(valid)
        self.assertEqual(authority, 3)  # tail, not genesis

    def test_valid_chain_tail_authority_zero_returned(self):
        g = _genesis(authority_level=1)
        s = create_successor_identity(g, KEY, authority_level=0)
        valid, errors, authority = verify_lineage_chain([g, s], KEY)
        self.assertTrue(valid)
        self.assertEqual(authority, 0)

    def test_failed_chain_returns_authority_zero(self):
        g = _genesis()
        tampered = replace(g, integrity_tag="tampered")
        valid, errors, authority = verify_lineage_chain([tampered], KEY)
        self.assertFalse(valid)
        self.assertEqual(authority, 0)

    def test_three_record_chain_verifies(self):
        g = _genesis()
        s1 = create_successor_identity(g, KEY, model_fp="model:v2")
        s2 = create_successor_identity(s1, KEY, model_fp="model:v3")
        valid, errors, authority = verify_lineage_chain([g, s1, s2], KEY)
        self.assertTrue(valid)
        self.assertEqual(authority, s2.authority_level)

    def test_successor_wrong_type_raises(self):
        with self.assertRaises(TypeError):
            create_successor_identity("not-a-record", KEY)  # type: ignore

    def test_successor_negative_authority_rejected(self):
        g = _genesis()
        with self.assertRaises(ValidationError):
            create_successor_identity(g, KEY, authority_level=-1)

    def test_empty_chain_fails(self):
        valid, errors, authority = verify_lineage_chain([], KEY)
        self.assertFalse(valid)
        self.assertEqual(authority, 0)
        self.assertTrue(any("empty" in e for e in errors))


# ---------------------------------------------------------------------------
# Tamper detection
# ---------------------------------------------------------------------------

class TestTamperDetection(unittest.TestCase):

    def test_wrong_key_fails_and_downgrades(self):
        g = _genesis()
        valid, errors, authority = verify_lineage_chain([g], b"wrong-key")
        self.assertFalse(valid)
        self.assertEqual(authority, 0)
        self.assertTrue(any("integrity_tag" in e for e in errors))

    def test_tampered_integrity_tag_fails(self):
        g = _genesis()
        tampered = replace(g, integrity_tag="tampered")
        valid, errors, authority = verify_lineage_chain([tampered], KEY)
        self.assertFalse(valid)
        self.assertEqual(authority, 0)

    def test_broken_previous_hash_fails(self):
        g = _genesis()
        s = create_successor_identity(g, KEY, model_fp="model:v2")
        broken = replace(s, previous_hash="not-the-right-hash", integrity_tag="")
        # Recompute tag with the broken field so HMAC passes but chain link fails
        from velvet_continuity.proof_hashing import make_integrity_tag
        broken = replace(broken, integrity_tag=make_integrity_tag(broken, KEY))
        valid, errors, authority = verify_lineage_chain([g, broken], KEY)
        self.assertFalse(valid)
        self.assertEqual(authority, 0)
        self.assertTrue(any("broken chain link" in e for e in errors))

    def test_lineage_root_mutation_fails(self):
        g = _genesis()
        s = create_successor_identity(g, KEY)
        # Mutate lineage_root on successor; recompute tag so HMAC passes
        from velvet_continuity.proof_hashing import make_integrity_tag
        mutated = replace(s, lineage_root="fake-root", integrity_tag="")
        mutated = replace(mutated, integrity_tag=make_integrity_tag(mutated, KEY))
        valid, errors, authority = verify_lineage_chain([g, mutated], KEY)
        self.assertFalse(valid)
        self.assertEqual(authority, 0)
        self.assertTrue(any("lineage_root" in e for e in errors))

    def test_instance_id_mutation_fails(self):
        g = _genesis()
        s = create_successor_identity(g, KEY)
        from velvet_continuity.proof_hashing import make_integrity_tag
        mutated = replace(s, id="velvet:instance:fake", integrity_tag="")
        mutated = replace(mutated, integrity_tag=make_integrity_tag(mutated, KEY))
        valid, errors, authority = verify_lineage_chain([g, mutated], KEY)
        self.assertFalse(valid)
        self.assertEqual(authority, 0)
        self.assertTrue(any("instance id changed" in e for e in errors))

    def test_non_genesis_as_chain_start_fails(self):
        g = _genesis()
        s = create_successor_identity(g, KEY)
        valid, errors, authority = verify_lineage_chain([s], KEY)
        self.assertFalse(valid)
        self.assertEqual(authority, 0)
        self.assertTrue(any("genesis" in e for e in errors))

    def test_multiple_errors_all_reported(self):
        g = _genesis()
        s = create_successor_identity(g, KEY)
        from velvet_continuity.proof_hashing import make_integrity_tag
        # Mutate both lineage_root and id — two structural errors
        mutated = replace(s, lineage_root="fake-root", id="velvet:instance:fake", integrity_tag="")
        mutated = replace(mutated, integrity_tag=make_integrity_tag(mutated, KEY))
        valid, errors, authority = verify_lineage_chain([g, mutated], KEY)
        self.assertFalse(valid)
        self.assertGreaterEqual(len(errors), 2)


# ---------------------------------------------------------------------------
# LineageEvent
# ---------------------------------------------------------------------------

class TestLineageEvent(unittest.TestCase):

    def _make_chain(self):
        g = _genesis()
        s = create_successor_identity(g, KEY, model_fp="model:v2")
        return g, s

    def test_valid_lineage_event_verifies(self):
        g, s = self._make_chain()
        event = create_lineage_event(g, s, "MODEL_UPGRADE", "Upgraded model.", KEY)
        valid, errors = verify_lineage_event(event, g, s, KEY)
        self.assertTrue(valid)
        self.assertEqual(errors, [])

    def test_tampered_from_hash_fails(self):
        g, s = self._make_chain()
        event = create_lineage_event(g, s, "MODEL_UPGRADE", "Upgraded model.", KEY)
        tampered = replace(event, from_identity_hash="fake")
        valid, errors = verify_lineage_event(tampered, g, s, KEY)
        self.assertFalse(valid)
        self.assertTrue(any("from_identity_hash" in e for e in errors))

    def test_tampered_to_hash_fails(self):
        g, s = self._make_chain()
        event = create_lineage_event(g, s, "MODEL_UPGRADE", "Upgraded model.", KEY)
        tampered = replace(event, to_identity_hash="fake")
        valid, errors = verify_lineage_event(tampered, g, s, KEY)
        self.assertFalse(valid)
        self.assertTrue(any("to_identity_hash" in e for e in errors))

    def test_tampered_integrity_tag_fails(self):
        g, s = self._make_chain()
        event = create_lineage_event(g, s, "MODEL_UPGRADE", "Upgraded model.", KEY)
        tampered = replace(event, integrity_tag="tampered")
        valid, errors = verify_lineage_event(tampered, g, s, KEY)
        self.assertFalse(valid)
        self.assertTrue(any("integrity_tag" in e for e in errors))

    def test_wrong_key_fails(self):
        g, s = self._make_chain()
        event = create_lineage_event(g, s, "MODEL_UPGRADE", "Upgraded model.", KEY)
        valid, errors = verify_lineage_event(event, g, s, b"wrong-key")
        self.assertFalse(valid)

    def test_blank_event_type_rejected(self):
        g, s = self._make_chain()
        with self.assertRaises(ValidationError):
            create_lineage_event(g, s, "", "Description.", KEY)

    def test_blank_description_rejected(self):
        g, s = self._make_chain()
        with self.assertRaises(ValidationError):
            create_lineage_event(g, s, "MODEL_UPGRADE", "", KEY)

    def test_wrong_record_type_rejected(self):
        g, s = self._make_chain()
        with self.assertRaises(TypeError):
            create_lineage_event("not-a-record", s, "TYPE", "desc", KEY)  # type: ignore

    def test_receipt_anchor_optional(self):
        g, s = self._make_chain()
        event = create_lineage_event(g, s, "MODEL_UPGRADE", "desc", KEY, receipt_anchor="sha256:anchor")
        self.assertEqual(event.receipt_anchor, "sha256:anchor")

    def test_receipt_anchor_none_by_default(self):
        g, s = self._make_chain()
        event = create_lineage_event(g, s, "MODEL_UPGRADE", "desc", KEY)
        self.assertIsNone(event.receipt_anchor)


# ---------------------------------------------------------------------------
# Hash stability — integrity tag is excluded
# ---------------------------------------------------------------------------

class TestHashStability(unittest.TestCase):

    def test_identity_hash_ignores_integrity_tag(self):
        g = _genesis()
        g_retagged = replace(g, integrity_tag="different-tag")
        self.assertEqual(
            proof_identity_hash(g),
            proof_identity_hash(g_retagged),
        )

    def test_lineage_event_hash_ignores_integrity_tag(self):
        g = _genesis()
        s = create_successor_identity(g, KEY)
        event = create_lineage_event(g, s, "UPGRADE", "desc", KEY)
        event_retagged = replace(event, integrity_tag="different-tag")
        self.assertEqual(
            lineage_event_hash(event),
            lineage_event_hash(event_retagged),
        )

    def test_different_proofs_produce_different_hashes(self):
        g1 = create_genesis_identity("proof-A", MODEL, "surface", KEY)
        g2 = create_genesis_identity("proof-B", MODEL, "surface", KEY)
        self.assertNotEqual(proof_identity_hash(g1), proof_identity_hash(g2))

    def test_different_models_produce_different_hashes(self):
        g = _genesis()
        s1 = create_successor_identity(g, KEY, model_fp="model:v2")
        s2 = create_successor_identity(g, KEY, model_fp="model:v3")
        self.assertNotEqual(proof_identity_hash(s1), proof_identity_hash(s2))

    def test_context_hashes_affect_record_hash(self):
        g = _genesis()
        s1 = create_successor_identity(g, KEY, active_context_hashes=["sha256:aaa"])
        s2 = create_successor_identity(g, KEY, active_context_hashes=["sha256:bbb"])
        self.assertNotEqual(proof_identity_hash(s1), proof_identity_hash(s2))


# ---------------------------------------------------------------------------
# Surface fingerprint
# ---------------------------------------------------------------------------

class TestSurfaceFingerprint(unittest.TestCase):

    def test_fingerprint_is_non_empty_string(self):
        fp = generate_surface_fingerprint()
        self.assertIsInstance(fp, str)
        self.assertTrue(fp)

    def test_fingerprint_is_deterministic(self):
        fp1 = generate_surface_fingerprint("test-label")
        fp2 = generate_surface_fingerprint("test-label")
        self.assertEqual(fp1, fp2)

    def test_different_labels_produce_different_fingerprints(self):
        fp1 = generate_surface_fingerprint("slot-A")
        fp2 = generate_surface_fingerprint("slot-B")
        self.assertNotEqual(fp1, fp2)

    def test_fingerprint_usable_in_genesis(self):
        fp = generate_surface_fingerprint("integration-test")
        g = create_genesis_identity(PROOF, MODEL, fp, KEY)
        valid, errors, authority = verify_lineage_chain([g], KEY)
        self.assertTrue(valid)


# ---------------------------------------------------------------------------
# Chain without HMAC verification (structural only)
# ---------------------------------------------------------------------------

class TestChainStructuralOnly(unittest.TestCase):

    def test_valid_chain_no_key(self):
        g = _genesis()
        s = create_successor_identity(g, KEY)
        valid, errors, authority = verify_lineage_chain([g, s])
        self.assertTrue(valid)
        self.assertEqual(authority, s.authority_level)

    def test_broken_previous_hash_caught_without_key(self):
        g = _genesis()
        broken = replace(g, previous_hash="unexpected", integrity_tag="ignored")
        # previous_hash on genesis should be None — this triggers genesis check
        valid, errors, authority = verify_lineage_chain([broken])
        self.assertFalse(valid)
        self.assertEqual(authority, 0)


if __name__ == "__main__":
    unittest.main()
