# -*- coding: utf-8 -*-
import os

activemq_jms_ip = '127.0.0.1'
activemq_jms_port = 61613
activemq_jms_user = os.getenv("ACTIVEMQ_USER") or "admin"
activemq_jms_password = os.getenv("ACTIVEMQ_PASSWORD") or "password"

# activemq管理界面：http://localhost:8161/admin/index.jsp  admin/admin