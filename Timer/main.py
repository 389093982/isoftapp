# -*- coding: utf-8 -*-
from isoft.common.activemqtool import ActiveMQManager, ActiveMQListener


class TimerActiveMQListener(ActiveMQListener):
    def __init__(self):
        super(TimerActiveMQListener, self).__init__()

    def on_error(self, headers, message):
        print(headers)
        print('received an error %s' % message)

    def on_message(self, headers, message):
        destination = headers.destination
        if destination == '/queue/quartz/scheduler':
            job_id = message.job_id
            task_type = message.task_type
            task_name = message.task_name

        print(headers)
        print('received a message %s' % message)


if __name__ == '__main__':
    try:
        activeMQManager = ActiveMQManager(listener=TimerActiveMQListener())
        destination = '/queue/quartz/scheduler'
        activeMQManager.subscribe(destination=destination)
    except Exception as e:
        print(str(e))

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        activeMQManager.disconnect()
