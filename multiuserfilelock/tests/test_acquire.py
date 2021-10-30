from multiuserfilelock import MultiUserFileLock, Timeout
import pytest


def test_acquire_lock(tmp_path):
    lock_filename = tmp_path / 'test.lock'

    lock1 = MultiUserFileLock(lock_filename)
    lock1.acquire()
    lock1.release()
    assert lock_filename.exists()

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
