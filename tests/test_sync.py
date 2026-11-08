"""Unit tests for semantic-delta-state-sync."""
import unittest
from semantic_delta_state_sync.sync import SemanticDeltaStateSync, DeltaOp


class TestSemanticDeltaStateSync(unittest.TestCase):
    def test_compute_and_apply_delta(self):
        syncer = SemanticDeltaStateSync({"a": 1, "b": 2})
        target = {"a": 1, "b": 99, "c": 3}
        ops = syncer.compute_delta(target)
        self.assertEqual(len(ops), 2)  # b modified, c added
        syncer.apply_delta(ops)
        self.assertEqual(syncer.state, target)

    def test_delete_operation(self):
        syncer = SemanticDeltaStateSync({"x": 10, "y": 20})
        ops = syncer.compute_delta({"x": 10})
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0].op_type, "DELETE")
        syncer.apply_delta(ops)
        self.assertNotIn("y", syncer.state)

    def test_append_operation(self):
        syncer = SemanticDeltaStateSync({"logs": ["init"]})
        op = DeltaOp("APPEND", "logs", "step_1_done")
        syncer.apply_delta([op])
        self.assertEqual(syncer.state["logs"], ["init", "step_1_done"])
