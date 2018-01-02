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
    def send(self, body, destination, selector=None):
        if selector is not None:
            # egg : stomp.put(json.dumps(Dict_Message), destination="/queue/test",conf={'Test':'Test123'})
            self.conn.send(body=body, destination=destination, conf={selector['name'] : selector['value']})
        else:
            self.conn.send(body=body, destination=destination)

    # 从队列接受消息/主题
    def subscribe(self, destination, selector=None):
        if selector is not None:
            # egg : stomp.subscribe("/queue/test",conf={'selector' : "Test = 'Test123'"})
            self.conn.subscribe(destination=destination, conf={'selector' : "{name} = '{value}'".format(name=selector['name'], value=selector['value'])})
        else:
            self.conn.subscribe(destination=destination)

    def disconnect(self):
        self.conn.disconnect()
