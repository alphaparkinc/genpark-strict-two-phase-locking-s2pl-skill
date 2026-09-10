import sys
from client import Strict2PLLockManager

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

def run():
    print(">>> Demonstrating Strict 2PL Lock Manager...")
    lm = Strict2PLLockManager()

    # T1 acquires shared lock on item_A
    assert lm.acquire_shared("T1", "item_A") is True
    # T2 acquires shared lock on item_A concurrently
    assert lm.acquire_shared("T2", "item_A") is True
    print("Concurrent shared locks granted to T1 and T2.")

    # T3 requests exclusive lock on item_A -> must be blocked
    assert lm.acquire_exclusive("T3", "item_A") is False
    print("Exclusive lock on item_A blocked for T3.")

    # T1 finishes and releases locks
    lm.release_all_locks("T1")
    # T3 still blocked because T2 still holds shared lock
    assert lm.acquire_exclusive("T3", "item_A") is False

    # T2 finishes and releases locks
    lm.release_all_locks("T2")
    # Now T3 can acquire exclusive lock
    assert lm.acquire_exclusive("T3", "item_A") is True
    print("Exclusive lock granted to T3 after strict lock release.")
    print("[PASS] Strict Two-Phase Locking verified.")

if __name__ == "__main__":
    run()
