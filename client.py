import argparse
import confuse
from archiver.client import Client
import logging
import sentry_sdk


logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Chia archiver client.')
parser.add_argument('-c', '--config', default='client-config.yaml', help='Configuration file')
args = parser.parse_args()

config = confuse.YamlSource(args.config)

if config['sentry']['enabled']:
    sentry_sdk.init(
        config['sentry']['link'],
        traces_sample_rate=config['sentry']['rate']
    )

client = Client(config)

while True:
    client.archive()
