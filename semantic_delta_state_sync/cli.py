"""CLI for semantic-delta-state-sync."""
import sys
import argparse
from .sync import SemanticDeltaStateSync


def main():
    parser = argparse.ArgumentParser(description="Semantic Delta State Sync CLI")
    parser.add_argument("--demo", action="store_true", help="Run semantic delta state synchronization demo")
    args = parser.parse_args()

    if args.demo:
        syncer = SemanticDeltaStateSync({"status": "idle", "active_tool": None})
        target = {"status": "running", "active_tool": "bash", "step": 3}
        ops = syncer.sync_to(target)
        print(f"[+] Computed {len(ops)} delta operations:")
        for op in ops:
            print(f"    {op.op_type} -> {op.path} = {op.value}")
        print(f"[+] State successfully converged: {syncer.state}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
