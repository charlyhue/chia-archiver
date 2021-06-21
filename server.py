import argparse
import confuse
from archiver.server import ApiServer, FtpServer
import threading
import sentry_sdk


parser = argparse.ArgumentParser(description='Chia archiver server.')
parser.add_argument('-c', '--config', default='server-config.yaml', help='Configuration file')
args = parser.parse_args()

config = confuse.YamlSource(args.config)

if config['sentry']['enabled']:
    sentry_sdk.init(
        config['sentry']['link'],
        traces_sample_rate=config['sentry']['rate']
    )

ftp_server = FtpServer(config)
threading.Thread(name="ftp_server", target=ftp_server.run).start()
print("FTP server started")

api_server = ApiServer(config)
api_server.start()
