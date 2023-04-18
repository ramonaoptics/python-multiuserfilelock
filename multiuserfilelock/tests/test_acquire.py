from multiuserfilelock import MultiUserFileLock, Timeout
import pytest


def test_acquire_lock(tmp_path):
    lock_filename = tmp_path / 'test.lock'

    lock1 = MultiUserFileLock(lock_filename)
    lock1.acquire()
    assert lock_filename.exists()
    lock1.release()

    lock2 = MultiUserFileLock(lock_filename)
    lock2.acquire()


def test_double_acquire(tmp_path):
    lock_filename = tmp_path / 'test.lock'

    lock1 = MultiUserFileLock(lock_filename)
    lock1.acquire()

    lock2 = MultiUserFileLock(lock_filename, timeout=0.001)
    with pytest.raises(Timeout):
        lock2.acquire()

    lock1.release()
    lock2.acquire()

from threading import Thread
from queue import Queue

def test_release_lock_from_different_thread(tmp_path):
    # 1. Users start the MCAM in the background
    #     acquire!
    # 2. Users closes the MCAM in a different background thread.
    #     release!
    # 3. Users tries to open the MCAM in a new thread.
    #     acquire!
    #    unfortunately, the acquisition fails.

    lock_filename = tmp_path / 'test.lock'
    lock1 = MultiUserFileLock(lock_filename)
    result = lock1.acquire()
    print(result)
    lock_thread = Thread(target=result)
    lock_thread.start()
    lock_thread.join()
    assert lock_filename.exists()

    lock_thread2 = Thread(target=lock1.release())
    lock_thread2.start()

    lock_thread3 = Thread(target=lock1.acquire())
    lock_thread3.start()
