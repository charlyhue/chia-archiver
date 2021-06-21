from pyftpdlib.handlers import FTPHandler
from redis import Redis
import os


class CustomFtpHandler(FTPHandler):

    def delete_from_db(self, file):
        db = Redis(host=self.config['redis']['host'], port=self.config['redis']['port'])
        db.delete("directory_" + os.path.split(file)[0] + "/")

    def on_file_received(self, file):
        # do something when a file has been received
        os.rename(file, file.replace('.tmp', ''))
        self.delete_from_db(file)


    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)
        self.delete_from_db(file)
