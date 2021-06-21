from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.filesystems import UnixFilesystem
from archiver.server.custom_ftp_handler import CustomFtpHandler


class FtpServer:
    def __init__(self, config):
        self.config = config
        authorizer = DummyAuthorizer()
        authorizer.add_user(config['ftp']['user'], config['ftp']['password'], '/', perm='elw')
        handler = CustomFtpHandler
        handler.config = self.config
        handler.authorizer = authorizer
        handler.abstracted_fs = UnixFilesystem
        self.server = ThreadedFTPServer((config['ftp']['host'], config['ftp']['port']), handler)


    def run(self):
        self.server.serve_forever()
