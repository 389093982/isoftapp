# -*- coding: utf-8 -*-
import json

from isoft.common.activemqtool import ActiveMQManager, ActiveMQListener

import timer
from threadlocal import local_intg_data
from timerlog import log_quartz_message_received


class TimerActiveMQListener(ActiveMQListener):
    def __init__(self):
        super(TimerActiveMQListener, self).__init__()

    def on_error(self, headers, message):
        print(headers)
        print('received an error %s' % message)

    def on_message(self, headers, message):
        # 队列信息
        destination = headers['destination']
        if destination == '/queue/quartz/scheduler':
            message = json.loads(message)
            job_id = message['job_id']
            # 任务类型和任务名称
            task_type = message['task_type']
            task_name = message['task_name']
            # 绑定到当前线程实例中
            local_intg_data.job_id = job_id
            local_intg_data.task_type = task_type
            local_intg_data.task_name = task_name
            local_intg_data.destination = destination

            # 记录 quartz 收到的日志信息
            log_quartz_message_received()
            # timer 开始执行任务
            timer.start_with_execute_task()



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
