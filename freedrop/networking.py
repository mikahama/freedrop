import os
import re
from paramiko import ServerInterface, SFTPServerInterface, SFTPServer, SFTPAttributes, \
    SFTPHandle, SFTP_OK, AUTH_SUCCESSFUL, OPEN_SUCCEEDED


class StubServer (ServerInterface):
    def check_auth_password(self, username, password):
        # all are allowed
        return False
        
    def check_auth_publickey(self, username, key):
        # all are allowed
        return AUTH_SUCCESSFUL
        
    def check_channel_request(self, kind, chanid):
        return OPEN_SUCCEEDED

    def get_allowed_auths(self, username):
        """List availble auth mechanisms."""
        return "publickey"


class StubSFTPHandle (SFTPHandle):
    def stat(self):
        try:
            return SFTPAttributes.from_stat(os.fstat(self.readfile.fileno()))
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)

    def chattr(self, attr):
        # python doesn't have equivalents to fchown or fchmod, so we have to
        # use the stored filename
        try:
            SFTPServer.set_file_attr(self.filename, attr)
            return SFTP_OK
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)


class StubSFTPServer (SFTPServerInterface):
    # assume current folder is a fine root
    # (the tests always create and eventualy delete a subfolder, so there shouldn't be any mess)
    ROOT = os.getcwd()


    def list_folder(self, path):
        print("OMG")
        return []

    def stat(self, path):
        return ""

    def lstat(self, path):
        return ""

    def _realpath(self, path):
        path = path.replace("\\","/")
        path = path.split("/")[-1]
        path = re.sub(r'^(~|-|\.)*', '', path)
        if len(path) == 0:
            path = "noname"
        return path
        
    def open(self, path, flags, attr):
        path = self._realpath(path)
        if flags & os.O_WRONLY:
            if flags & os.O_APPEND:
                fstr = 'ab'
            else:
                fstr = 'wb'
        elif flags & os.O_RDWR:
            return None
        else:
            # O_RDONLY (== 0)
            return None
        try:
            f = open(path, fstr)
        except OSError as e:
            return SFTPServer.convert_errno(e.errno)
        fobj = StubSFTPHandle(flags)
        fobj.filename = path
        #fobj.readfile = f
        fobj.writefile = f
        return fobj

    def remove(self, path):
        return SFTP_OK

    def rename(self, oldpath, newpath):
        return SFTP_OK

    def mkdir(self, path, attr):
        return SFTP_OK

    def rmdir(self, path):
        return SFTP_OK

    def chattr(self, path, attr):
        return SFTP_OK

    def symlink(self, target_path, path):
        return SFTP_OK

    def readlink(self, path):
        return ""