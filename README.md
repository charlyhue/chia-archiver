# Chia-archiver
This tool is used to transfer plots from plotter(s) to harvester(s)

# Installation
```bash
git clone https://github.com/charlyhue/chia-archiver.git
cd chia-archiver
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
On server host yoou also need a redis instance.

# Configuration
## Server
See [example-client-config.yaml](https://github.com/charlyhue/chia-archiver/blob/main/example-client-config.yaml).
## Client
See [example-server-config.yaml](https://github.com/charlyhue/chia-archiver/blob/main/example-server-config.yaml).

# Usage
## Server
### Command
```bash
python server.py -c server-config.yaml
```
### Systemd
```
[Unit]
Description=Chia archiver server

[Service]
ExecStart=/path/to/chia-archiver/.venv/bin/python /path/to/chia-archiver/server.py -c /path/to/chia-archiver/server-config.yaml
User=chia
Group=chia

[Install]
WantedBy=multi-user.target
```

## Client
### Command
```bash
python client.py -c client-config.yaml
```
### Systemd
```
[Unit]
Description=Chia archiver client

[Service]
ExecStart=/path/to/chia-archiver/.venv/bin/python /path/to/chia-archiver/client.py -c /path/to/chia-archiver/client-config.yaml
User=chia
Group=chia

[Install]
WantedBy=multi-user.target
```
