import json
import sys
from client import Strict2PLLockManager

lm = Strict2PLLockManager()

def handle_rpc(line):
    try:
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        rid = req.get("id")
        
        if method == "tools/list":
            tools = [
                {"name": "acquire_lock", "description": "Acquire shared or exclusive lock"},
                {"name": "release_locks", "description": "Release all locks held by transaction"}
            ]
            return json.dumps({"jsonrpc": "2.0", "id": rid, "result": {"tools": tools}})
        elif method == "tools/call":
            tname = params.get("name")
            args = params.get("arguments", {})
            if tname == "acquire_lock":
                mode = args.get("mode", "S")
                if mode == "X":
                    ok = lm.acquire_exclusive(args["txn_id"], args["item"])
                else:
                    ok = lm.acquire_shared(args["txn_id"], args["item"])
                return json.dumps({"jsonrpc": "2.0", "id": rid, "result": {"granted": ok}})
            elif tname == "release_locks":
                count = lm.release_all_locks(args["txn_id"])
                return json.dumps({"jsonrpc": "2.0", "id": rid, "result": {"released_count": count}})
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}})

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(handle_rpc(line.strip()), flush=True)
