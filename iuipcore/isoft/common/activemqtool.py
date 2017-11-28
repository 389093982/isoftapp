# -*- coding: utf-8 -*-

import stomp
from isoft.common.singleton import singleton
from isoft.config.mqconfig import activemq_jms_ip, activemq_jms_port, activemq_jms_user, activemq_jms_password


class ActiveMQListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % message)


@singleton
class ActiveMQManager(object):
    def __init__(self, listener=ActiveMQListener()):
        self.conn = stomp.Connection10([(activemq_jms_ip, activemq_jms_port)])
        self.conn.set_listener('', listener)
        self.conn.start()
        self.conn.connect(login=activemq_jms_user, password=activemq_jms_password)

    # 发送消息到队列/主题
    def send(self, body, destination):
        self.conn.send(body=body, destination=destination)

    # 从队列接受消息/主题
    def subscribe(self, destination):
        self.conn.subscribe(destination=destination)

    def disconnect(self):
        self.conn.disconnect()