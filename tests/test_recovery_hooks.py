# SPDX-License-Identifier: GPL-3.0-only
"""Tests for RecoveryHooks."""

import unittest
from velvet_continuity import DriftEvent
from velvet_continuity.recovery_hooks import RecoveryHooks


def make_event():
    return DriftEvent(
        drift_type="surface",
        severity="medium",
        expected="nav",
        observed="audio",
        action="review",
    )


class TestRecoveryHooks(unittest.TestCase):

    def setUp(self):
        self.hooks = RecoveryHooks()

    def test_register_and_run(self):
        received = []
        self.hooks.register(lambda e: received.append(e))
        event = make_event()
        self.hooks.run(event)
        self.assertEqual(len(received), 1)
        self.assertIs(received[0], event)

    def test_multiple_callbacks_called_in_order(self):
        order = []
        self.hooks.register(lambda e: order.append(1))
        self.hooks.register(lambda e: order.append(2))
        self.hooks.run(make_event())
        self.assertEqual(order, [1, 2])

    def test_register_non_callable_raises(self):
        with self.assertRaises(TypeError):
            self.hooks.register("not-callable")

    def test_run_wrong_type_raises(self):
        self.hooks.register(lambda e: None)
        with self.assertRaises(TypeError):
            self.hooks.run("not-a-drift-event")

    def test_clear_removes_all_callbacks(self):
        self.hooks.register(lambda e: None)
        self.hooks.register(lambda e: None)
        self.hooks.clear()
        self.assertEqual(len(self.hooks), 0)

    def test_len(self):
        self.assertEqual(len(self.hooks), 0)
        self.hooks.register(lambda e: None)
        self.assertEqual(len(self.hooks), 1)

    def test_run_with_no_callbacks_does_not_raise(self):
        self.hooks.run(make_event())  # should not raise


if __name__ == "__main__":
    unittest.main()
