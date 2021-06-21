from bottle import Request
from archiver.utils.plots import get_plots
import threading
import os
import time
import requests
from ftplib import FTP
import socket
import logging
from datetime import datetime


class Client:
    def __init__(self, config):
        self.config = config
    
    def archive_plot(self, plot):
        for host in self.config['archive_hosts']:
            payload = {"plot": os.path.basename(plot), "size": os.path.getsize(plot)}
            r = requests.get("http://{0}:{1}/get_destination".format(host['host'], host['api_port']), params=payload)
            if r.json()['code'] == 0:
                with FTP() as ftp:
                    ftp.connect(host['host'], host['ftp_port'])
                    ftp.login(host['ftp_user'], host['ftp_password'])
                    start = datetime.now()
                    ftp.storbinary('STOR '+r.json()['dest'], open(plot, 'rb'))
                    ftp.quit()
                    os.remove(plot)
                    logging.info("Plot {0} archived on {1} in {2}.".format(os.path.basename(plot), host['host'], datetime.now()-start))
                break
    
    def archive(self):
        plots = get_plots(self.config['plots_directories'])
        archive_threads = []

        while len(plots) > 0:
            if len(archive_threads) < self.config['max_concurrent_archive']:
                f = plots.pop()
                logging.info("Archive plot {0}".format(f))
                nt = threading.Thread( name="archive-" + os.path.splitext(os.path.basename(f))[0], target=Client.archive_plot, args=(self, f, ) )
                nt.start()
                archive_threads.append(nt)
            else:
                # wait for at least one thread to finish
                while len(archive_threads) == self.config['max_concurrent_archive']:
                    for t in archive_threads:
                        if not t.is_alive():
                            archive_threads.remove(t)
                    time.sleep(0.5)
            # whait for finish
            if len(plots) == 0:
                while len(archive_threads) > 0:
                    for t in archive_threads:
                        if not t.is_alive():
                            archive_threads.remove(t)
                    time.sleep(0.5)
