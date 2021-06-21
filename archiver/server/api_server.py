from bottle import Bottle, request
import json
from redis import Redis
from archiver.utils.disks import get_disk_free_space


class ApiServer(object):
    def __init__(self, config):
        self.config = config
        self._app = Bottle()
        self._app.route('/get_destination', method="GET", callback=self.get_destination)
        self._app.route('/delete', method="GET", callback=self.clean)
        self.db = Redis(host=self.config['redis']['host'], port=self.config['redis']['port'])
    
    def start(self):
        self._app.run(host=self.config['api']['host'], port=self.config['api']['port'])

    def to_int(self, var):
        print(var)
        if var is None:
            return 0
        else:
            return int(var)
    
    def get_first_available_disk(self, plot, size):
        for d in self.config['plots_directories']:
            key = "directory_" + d
            print(key)
            if self.to_int(self.db.get(key)) < self.config['max_concurrent_by_disk'] and get_disk_free_space(d) >= self.config['max_concurrent_by_disk'] * size:
                self.db.incr(key)
                return {"code": 0, "dest": d + plot + ".tmp"}
        return {"code": 1}

    def get_destination(self):
        plot = request.query['plot']
        size = int(request.query['size'])

        return json.dumps(self.get_first_available_disk(plot, size))

    def clean(self):
        for d in self.config['plots_directories']:
            self.db.delete("directory_" + d)



