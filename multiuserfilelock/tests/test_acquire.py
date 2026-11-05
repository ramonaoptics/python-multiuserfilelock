import os
import grp
from multiuserfilelock import MultiUserFileLock, Timeout
from threading import Thread
from queue import Queue
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


def test_release_lock_from_different_thread(tmp_path):
    results = Queue()

    def thread_lock_acquire(filename):
        lock = MultiUserFileLock(filename)
        lock.acquire()
        assert lock.is_locked
        results.put(lock)

    def thread_lock_release(lock):
        lock.release()

    lock_filename = tmp_path / 'test.lock'
    lock_thread = Thread(target=thread_lock_acquire, args=(lock_filename,))

    lock_thread.start()
    lock_thread.join(timeout=1)
    assert not lock_thread.is_alive()
    lock = results.get(timeout=1)
    assert lock.is_locked

    lock_thread = Thread(target=thread_lock_release, args=(lock,))
    lock_thread.start()
    lock_thread.join(timeout=1)
    assert not lock_thread.is_alive()
    assert not lock.is_locked

    lock_thread2 = Thread(target=thread_lock_acquire, args=(lock_filename,))
    lock_thread2.start()
    lock_thread2.join(timeout=1)
    assert not lock_thread2.is_alive()
    lock2 = results.get(timeout=1)
    assert lock2.is_locked


@pytest.mark.skipif(os.name == 'nt', reason='no unix groups')
def test_nested_directories_get_group_and_mode(tmp_path):
    groups = [g for g in os.getgroups() if g != tmp_path.stat().st_gid]
    if not groups:
        pytest.skip('needs membership in a second group')
    group = grp.getgrgid(groups[0]).gr_name
    lock_filename = tmp_path / 'a' / 'b' / 'test.lock'
    old_umask = os.umask(0o022)
    try:
        lock = MultiUserFileLock(lock_filename, group=group)
    finally:
        os.umask(old_umask)
    lock.acquire()
    lock.release()
    for directory in [tmp_path / 'a', tmp_path / 'a' / 'b']:
        assert directory.group() == group
        assert directory.stat().st_mode & 0o777 == 0o777
