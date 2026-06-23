import ipaddress
import json
import os
from multiprocessing import cpu_count

from dotenv import load_dotenv

load_dotenv()

# https://docs.gunicorn.org/en/stable/settings.html
# gunicorn -c webapp/gunicorn.conf.py webapp:app
# gunicorn -c gunicorn.conf.py wsgi:app


def is_localhost(host) -> bool:
    """Returns True if a host string represents a localhost address otherwise False."""
    try:
        ip_address = ipaddress.ip_address(host)
        return ip_address.is_loopback
    except ValueError:
        # Handle cases where the host is not a valid IP address
        return host.lower() in ("localhost", "127.0.0.1", "::1")


default_pool_size = int(os.getenv('DEFAULT_POOL_SIZE', 1))
rds_pool_size = int(os.getenv('RDS_POOL_SIZE', 1))
rds_pool_size += default_pool_size
# validate the pool size
if (rds_pool_size - default_pool_size) < 1:
    raise Exception('PoolSize should be higher that 0!')

# The socket to bind.
host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', '8080')
bind = "{}:{}".format(host, port)

# The number of worker processes for handling requests.
workers = (cpu_count() * 2) + 1 if not is_localhost(host) else 1

# The type of workers to use.
worker_class = 'gthread'

# The number of worker threads for handling requests.
threads = rds_pool_size - default_pool_size

# A base to use with setproctitle for process naming.
proc_name = "gunicorn"
# default_proc_name = "gunicorn"

# Workers silent for more than this many seconds are killed and restarted.
timeout = 60

# The Access log file to write to.
accesslog_var = os.getenv("ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
accesslog = use_accesslog

# The Error log file to write to.
errorlog_var = os.getenv("ERROR_LOG", "-")
use_errorlog = errorlog_var or None
errorlog = use_errorlog

# The granularity of log outputs.
loglevel = 'debug'

# Redirect stdout/stderr to specified file in errorlog.
capture_output = True

# data to log as json
log_data = {
    "loglevel": loglevel,
    "bind": bind,
    "workers": workers,
    "threads": threads,
    "timeout": timeout,
    "errorlog": errorlog,
    "accesslog": accesslog,
    # Additional, non-gunicorn variables
}
print(json.dumps(log_data))
