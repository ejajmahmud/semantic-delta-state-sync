"""Core Semantic Delta State Sync implementation."""
import copy
from typing import Dict, List, Any, Optional


class DeltaOp:
    def __init__(self, op_type: str, path: str, value: Any = None):
        self.op_type = op_type  # SET, DELETE, APPEND
        self.path = path
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {"op": self.op_type, "path": self.path, "value": self.value}


class SemanticDeltaStateSync:
    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self.state: Dict[str, Any] = copy.deepcopy(initial_state) if initial_state else {}
        self.version = 0

    def compute_delta(self, target_state: Dict[str, Any]) -> List[DeltaOp]:
        ops: List[DeltaOp] = []
        # Check added or modified keys
        for k, v in target_state.items():
            if k not in self.state:
                ops.append(DeltaOp("SET", k, copy.deepcopy(v)))
            elif self.state[k] != v:
                ops.append(DeltaOp("SET", k, copy.deepcopy(v)))
        # Check deleted keys
        for k in self.state:
            if k not in target_state:
                ops.append(DeltaOp("DELETE", k))
        return ops

    def apply_delta(self, ops: List[DeltaOp], new_version: Optional[int] = None):
        for op in ops:
            if op.op_type == "SET":
                self.state[op.path] = copy.deepcopy(op.value)
            elif op.op_type == "DELETE":
                self.state.pop(op.path, None)
            elif op.op_type == "APPEND":
                if op.path not in self.state or not isinstance(self.state[op.path], list):
                    self.state[op.path] = []
                self.state[op.path].append(copy.deepcopy(op.value))
        self.version = new_version if new_version is not None else self.version + 1

    def sync_to(self, new_state: Dict[str, Any]) -> List[DeltaOp]:
        ops = self.compute_delta(new_state)
        self.apply_delta(ops)
        return ops
