import psutil

def get_disk_free_space(disk):
    return psutil.disk_usage(disk).free
