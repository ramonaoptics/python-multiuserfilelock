from . import _version
__version__ = _version.get_versions()['version']

from filelock import FileLock, Timeout
import os
import shutil
import tempfile
from pathlib import Path

# Creating the locks directly in the /tmp dir on linux causes
# many problems since the `/tmp` dir has the sticky bit enabled.
# The sticky bit stops an other user from deleting your file.
# It seems that this stops some other user from opening a file for
#
# We tried to use `SoftFileLock` and while it worked,
# SoftFileLocks did not automatically get deleted upon the crash
# or force quit of a python console.
# This made them really problematic when closing python quickly.
#
# Therefore, we store all our locks in a subdirectory
# On linux we set the group of this MultiUserFileLock to
# the desired group so that multiple people
if os.name == 'nt':
    # Windows has a pretty bad per use /tmp directory
    # We therefore use the public directory, and create a tempdir in there
    tmpdir = Path(os.environ.get('public', r'C:\Users\Public')) / 'tmp'
else:
    tmpdir = Path(tempfile.gettempdir())


class MultiUserFileLock(FileLock):
    def __init__(self, *args, user=None, group=None, chmod=0o666, **kwargs):
        if os.name == 'nt':
            self._user = None
            self._group = None
        else:
            self._user = user
            self._group = group
        self._chmod = chmod
        # Will create a ._lock_file object
        # but will not create the files on the file system
        super().__init__(*args, **kwargs)
        self._lock_file_path = Path(self._lock_file)
        parent = self._lock_file_path.parent
        # Even though the "other write" permissions are enabled
        # it seems that the operating systems disables that for the /tmp dir
        parent.mkdir(mode=0o777, parents=True, exist_ok=True)

        if self._group is not None and parent.group() != self._group:
            shutil.chown(parent, group=self._group)

        # Changing the owner in the tmp directory is hard..
        if self._user is not None and parent.owner() != self._user:
            shutil.chown(parent, user=self._user)

    def acquire(self, *args, **kwargs):
        super().acquire(*args, **kwargs)
        # once the lock has been acquired, we are more guaranteed that the
        # _lock_file exists
        if self._chmod:
            desired_permissions = self._chmod
            current_permissions = self._lock_file_path.stat().st_mode

            missing_permissions = (
                current_permissions & desired_permissions
            ) ^ desired_permissions

            # changing permissions can be tricky, so only change them
            # if we need to
            if missing_permissions != 0:
                # Make sure the parent directory can be written to by others
                self._lock_file_path.chmod(desired_permissions)
        if self._group is not None:
            if self._lock_file_path.group() != self._group:
                shutil.chown(self._lock_file_path, group=self._group)
        if self._user is not None:
            if self._lock_file_path.owner() != self._user:
                shutil.chown(self._lock_file_path, user=self._user)


__all__ = [
    'MultiUserFileLock',
    'Timeout',
]
