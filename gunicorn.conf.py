import os
from dotenv import load_dotenv

bind = "127.0.0.1:8000"
workers = 2

env_file = ".env"
env = os.path.join(os.getcwd(), env_file)
if os.path.exists(env):
    load_dotenv(env)

errorlog = 'error.log'
loglevel = 'info'
accesslog = 'access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'