class Strict2PLLockManager:
    """
    Strict Two-Phase Locking (S2PL) Lock Manager.
    All acquired locks (Shared or Exclusive) are held until transaction commits or aborts.
    """
    def __init__(self):
        self.shared_locks = {}    # item -> set of txn_ids
        self.exclusive_locks = {} # item -> txn_id
        self.txn_locks = {}       # txn_id -> set of (item, mode)

    def acquire_shared(self, txn_id, item):
        # Can acquire if no exclusive lock held, or held by self
        x_holder = self.exclusive_locks.get(item)
        if x_holder is not None and x_holder != txn_id:
            return False # Blocked
        if item not in self.shared_locks:
            self.shared_locks[item] = set()
        self.shared_locks[item].add(txn_id)
        if txn_id not in self.txn_locks:
            self.txn_locks[txn_id] = set()
        self.txn_locks[txn_id].add((item, "S"))
        return True

    def acquire_exclusive(self, txn_id, item):
        # Can acquire if no one else holds exclusive lock, and no one else holds shared lock
        x_holder = self.exclusive_locks.get(item)
        if x_holder is not None and x_holder != txn_id:
            return False
        s_holders = self.shared_locks.get(item, set())
        if any(holder != txn_id for holder in s_holders):
            return False
        
        self.exclusive_locks[item] = txn_id
        if txn_id not in self.txn_locks:
            self.txn_locks[txn_id] = set()
        self.txn_locks[txn_id].add((item, "X"))
        return True

    def release_all_locks(self, txn_id):
        """Atomic release of all locks held by transaction at commit/abort time."""
        locks = self.txn_locks.pop(txn_id, set())
        for item, mode in locks:
            if mode == "S" and item in self.shared_locks:
                self.shared_locks[item].discard(txn_id)
                if not self.shared_locks[item]:
                    del self.shared_locks[item]
            elif mode == "X" and self.exclusive_locks.get(item) == txn_id:
                del self.exclusive_locks[item]
        return len(locks)
