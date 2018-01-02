#!/usr/bin/env python
import os
import sys
import threading

from quartz.core.timer_scheduler import JobManager

def quartz_initial():
    a = JobManager()
    # 初始化所有job
    a.init_jobs()

def init_daemon():
    quartz_initial_thread = threading.Thread(target=quartz_initial, args=())
    quartz_initial_thread.setDaemon(True)
    quartz_initial_thread.start()



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IUIP.settings")

    # 开启守护线程
    init_daemon()

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
