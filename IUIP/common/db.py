# -*- coding: utf-8 -*-
import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import ResultProxy
from sqlalchemy.engine.result import ResultMetaData
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("django")


def getConnection(url, username, password, dbType='mysql'):
    dbType = dbType.lower()
    logging.info('execute getConnection method,params is[dbType=%s,url=%s,username=%s,password=%s]' \
                 % (dbType, url, username, password))
    # 获取真实的 url 串
    connection_url = getRealUrl(dbType, url, username, password)

    engine = create_engine(connection_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    sql = {
        'mysql': 'select 1 from dual',
        'oracle': 'select 1 from dual',
    }.get(dbType, 'select 1 from dual')
    session.execute(sql)
    session.close()


def getRealUrl(dbType, url, username, password):
    '''获取真实的 url'''
    dbType = dbType.lower()
    connection_url = {
        'mysql': ''.join(['mysql+pymysql://', username, ':', password, '@', url]),
        'oracle': ''.join(['oracle+cx_oracle://', username, ':', password, '@', url]),
    }.get(dbType, ''.join(['mysql+pymysql://', username, ':', password, '@', url]))
    return connection_url


def validateSql(dbType, url, username, password, sql):
    connection_url = getRealUrl(dbType, url, username, password)
    engine = create_engine(connection_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    rs = session.execute(sql)
    # 连接对象的描述信息 rs.cursor.description
    session.close()


def getMetaData(dbType, url, username, password, sql):
    try:
        connection_url = getRealUrl(dbType, url, username, password)
        engine = create_engine(connection_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        rs = session.execute(sql)
        return {'status': 'SUCCESS', 'result': rs.cursor.description}
    except Exception as e:
        return {'status': 'ERROR', 'result': str(e)}
    finally:
        session.close()


if __name__ == '__main__':
    validateSql('mysql', 'localhost:3306/iuip', 'root', '123456', 'select * from resources_resource t where 1=0')