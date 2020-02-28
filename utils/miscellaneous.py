import os
import sys
from functools import wraps


def ensure_only_one_instance_running(name):
    """Decorator that creates pid file /tmp/{name}.pid when wrapped function starts
    and removes pid file when function finishes or exception is risen.
    While pid file exists, wrapped function can not be called (sys.exit() is called instead.)
    This decorator is usefull if you do not want two instances of application executing simultaneously."""
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            pid = str(os.getpid())
            pidfile = "/tmp/{}.pid".format(name)
            if os.path.isfile(pidfile):
                print("%s already exists, exiting" % pidfile)
                sys.exit()
            with open(pidfile, 'w') as f:
                f.write(pid)
            try:
                function(*args, **kwargs)
            finally:
                os.unlink(pidfile)
        return wrapper
    return inner_function
