#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
import sys
import logging
import pymysql
import os
import configparser


# read config
cur_path=os.path.dirname(os.path.realpath(__file__))
config_path=os.path.join(cur_path,'../conf/config.ini')
conf = configparser.ConfigParser()
conf.read(config_path,encoding='utf-8-sig')
DB_IP = conf.get("MYSQL", "DB_IP")
DB_PORT = conf.get("MYSQL", "DB_PORT")
DB_USER = conf.get("MYSQL", "DB_USER")
DB_PASSWORD = conf.get("MYSQL", "DB_PASSWORD")
DB_SCHEMA = conf.get("MYSQL", "DB_SCHEMA")
DB_CHARSET = conf.get("MYSQL", "DB_CHARSET")


# 特定参数
SOURCE_FILE = conf.get("SOURCE_FILE", "AGENT_INFO")
LOG_FILE = conf.get("BASE_CONF", "LOG_PATH") + "/itm_agent_info.log"
TABLE_NAME = "itm_agent_info"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
counter = 0
global host_dict
host_dict = {}

# 设置log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    logger.info("开始处理agentinfo.txt文件！")
    # 清空数据库
    clean_db()

    # 循环agentinfo.txt文件，逐个处理agent
    process_agent()

    # 补漏，完善ip信息
    post_process()

    logger.info("处理完成！")
    print("处理完成，共%s条记录！" % counter)


# 清空数据库
def clean_db():
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    sql = "delete from " + TABLE_NAME
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print("Table %s has been cleaned!" % TABLE_NAME)
    logger.info('表%s已被清空！', TABLE_NAME)


def import_data(cursor,AGENT_NAME,AGENT_CODE,AGENT_VERSION,HOSTNAME,IP_ADDRESS,INSTANCE,AGENT_HOST,AGENT_TYPE):
    global counter
    sqlStr = "insert into " + TABLE_NAME + " (write_time,AGENT_NAME,AGENT_CODE,AGENT_VERSION,HOSTNAME,IP_ADDRESS,INSTANCE,AGENT_HOST,AGENT_TYPE)" \
             "values (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    try:
        cursor.execute(sqlStr,(write_time,AGENT_NAME,AGENT_CODE,AGENT_VERSION,HOSTNAME,IP_ADDRESS,INSTANCE,AGENT_HOST,AGENT_TYPE))
    except:
        print("有问题的记录:%s" % AGENT_NAME)
        logger.error('有问题的记录:%s', AGENT_NAME)
    counter += 1


def isIP(str): # 判断字符串是否IP地址格式
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def get_host_dict():
    global host_dict
    host_dict = {}
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    cursor.execute("select HOSTNAME,IP_ADDRESS from {0} where HOSTNAME != '' and IP_ADDRESS != ''".format(TABLE_NAME));
    rows = cursor.fetchall()
    for row in rows:
        host_dict[row[0]] = row[1]
    conn.close()

def process_agent():
    global counter
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    with open(SOURCE_FILE, 'r',encoding='UTF-8') as file_to_read:
        for line in file_to_read.readlines():
            # print(lines,end='')
            line_tmp = line.split()
            instance = ''
            agent_host = ''
            agent_type = ''
            if len(line_tmp) == 6:  # [93]  ip.pipe:#10.1.8.178[22399]<NM>P74017P1</NM>  iftsdb:P74017P1:RZ  RZ  06.31.02  AIX~6.1
                col2 = line_tmp[1]
                agent_name = line_tmp[2]
                agent_code = line_tmp[3]
                agent_version = line_tmp[4]
                ip_address = re.findall(r"^ip.pipe:#(.*)\[",col2)[0]
                hostname = re.findall(r"<NM>(.*)</NM>",col2)[0]

                if agent_code == '01' or agent_code == '02':  # [7048]  ip.pipe:#10.1.71.107[25141]<NM>UMP-JMX3</NM>  10.1.48.52_RWA:UMP-JMX3:01  01  06.23.00  Linux~
                    instance = agent_name.split(":")[0]
                    ip_address = instance.split("_")[0]

                # print("agent_name:%s  agent_code:%s  agent_version:%s ip_address:%s  hostname:%s" % (agent_name,agent_code,agent_version,ip_address,hostname))
                import_data(cursor,agent_name,agent_code,agent_version,hostname,ip_address,instance,agent_host,agent_type)

            elif len(line_tmp) == 5: # [11448]  ip:#10.1.3.7[10000]<NM>ZPMPROXY01</NM>  ZPMProxy01ASFSdp:UAGENT00  UA  06.00.00
                col2 = line_tmp[1]
                agent_name = line_tmp[2]
                agent_code = line_tmp[3]
                agent_version = line_tmp[4]
                ip_address = ''
                hostname = ''

                if agent_code == 'EM':
                    ip_address = re.findall(r"<IP.PIPE>#(.*)\[",col2)[0]
                    hostname = agent_name
                elif isIP(col2):
                    ip_address = col2
                    hostname = agent_name.split(":")[0]
                else:
                    ip_address = re.findall(r"^ip:#(.*)\[", col2)[0]
                    hostname = re.findall(r"<NM>(.*)</NM>", col2)[0]

                import_data(cursor, agent_name, agent_code, agent_version, hostname, ip_address, instance, agent_host,agent_type)
                # print("agent_name:%s  agent_code:%s  agent_version:%s ip_address:%s  hostname:%s" % (agent_name, agent_code, agent_version, ip_address, hostname))

            elif len(line_tmp) == 4:
                agent_name = line_tmp[1]
                agent_code = line_tmp[2]
                agent_version = line_tmp[3]
                ip_address = ''
                hostname = ''
                if agent_code == 'RZ':  # RZ:OIBS1-OIBS1-BL660216:RDB
                    agent_host = agent_name.split(":")[1]
                    hostname = agent_host.split('-', 2)[2]  # 存在多个- 的情况，保留第二个-后面的值
                    instance = agent_host.split('-', 2)[1]  #实例名称

                if agent_code == 'HT' or agent_code == 'YJ' or agent_code == 'VM' or agent_code == 'T3':  # BOP:bl685-469:KHTP
                    hostname = agent_name.split(":")[1]
                    instance = agent_name.split(":")[0]
                    agent_type = agent_name.split(":")[2]


                #print("agent_name:%s  agent_code:%s  agent_version:%s ip_address:%s  hostname:%s" % (agent_name, agent_code, agent_version, ip_address, hostname))
                import_data(cursor, agent_name, agent_code, agent_version, hostname, ip_address, instance, agent_host,agent_type)
            else:
                print("line:" % line)
    conn.commit()
    conn.close()

def post_process():
    get_host_dict()
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();

    # 根据主机名称丰富IP信息
    sqlStr = "select distinct(HOSTNAME) from " + TABLE_NAME + " where IP_ADDRESS=''"
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    for row in rows:
        hostname = row[0]
        try:
            ip_address = host_dict[hostname]
            sql = "update {0} set IP_ADDRESS = %s where HOSTNAME = %s and IP_ADDRESS = ''".format(TABLE_NAME)
            cursor.execute(sql,(ip_address,hostname))
            conn.commit()
        except:
            pass

    # 处理windows RDB Agent，根据主机名称模糊查询
    sqlStr = "select HOSTNAME from " + TABLE_NAME + " where IP_ADDRESS='' and HOSTNAME like 'WIN%'"
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    for row in rows:
        hostname = row[0]
        sqlStr = "select IP_ADDRESS,AGENT_NAME from " + TABLE_NAME + " where AGENT_CODE='NT' and HOSTNAME like '" + hostname + "%'"
        cursor.execute(sqlStr)
        rows_ip = cursor.fetchall()
        if len(rows_ip) > 0:
            ip_address = rows_ip[0][0]
            agent_name = rows_ip[0][1]
            sqlStr = "update " + TABLE_NAME + " set IP_ADDRESS = %s where HOSTNAME = %s"
            cursor.execute(sqlStr, (ip_address, hostname))
            conn.commit()


    conn.close()


if __name__ == '__main__':
    main()