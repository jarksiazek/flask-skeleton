import os

from gunicorn import glogging

bind = f"0.0.0.0:{os.getenv('SERVICE_PORT', 8000)}"
max_requests = os.getenv("GUNICORN_MAX_REQUESTS", 0)

workers = 1
worker_class = "gevent"
worker_connections = os.getenv("GEVENT_GREENLETS", 128)

wsgi_app = "app:wsgi_app"

timeout = os.getenv("WORKER_STARTUP_TIMEOUT", 180)

loglevel = "info"
accesslog = "-"
errorlog = "-"

access_log_format = (
    '"message": "%(r)s", "http_host": "%({http_host}i)s", "method": "%(m)s", "uri":'
    ' "%(U)s", "query_string": "%(q)s", "status": %(s)s, "user_agent": "%(a)s",'
    ' "remote_addr": "%(h)s", "rq_size": %(b)s, "rs_time_ms": %(M)s, "protocol":'
    ' "%(H)s"'
)

logconfig = None
glogging.Logger.datefmt = "%Y-%m-%dT%H:%M:%S%z"
glogging.Logger.error_fmt = (
    '{"@timestamp": "%(asctime)s", "logger_name": "gunico'
    'rn", "pid": "%(process)d", "pname": "%(processName)s'
    '", "level": "%(levelname)s", "message": "%(message)s"}'
)
glogging.Logger.access_fmt = (
    '{"@timestamp": "%(asctime)s", "logger_name": "gunic'
    'orn", "pid": "%(process)d", "pname": "%(processName)'
    's", "level": "%(levelname)s", %(message)s}'
)
glogging.Logger.syslog_fmt = (
    '{"@timestamp": "%(asctime)s", "logger_name": "gunico'
    'rn", "pid": "%(process)d", "pname": "%(processName)s'
    '", "level": "%(levelname)s", "message": "%(message)s}"'
)
