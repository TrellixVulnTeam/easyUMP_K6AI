#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
from sub_common import *

# 设置log
logger = get_logger("import.log")

# 特定参数
conf = get_conf()
SOURCE_FILE = conf.get("SOURCE_FILE", "AGENT_INFO")
TABLE_NAME = "ITM_AGENT_INFO"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
global host_dict

def main():
    logger.info("Begin to import %s file.",SOURCE_FILE)
    # 清空数据库
    delsql = "delete from {0} ".format(TABLE_NAME)
    clean_db(delsql);

    # 循环agentinfo.txt文件，逐个处理agent
    process_agent()

    # 补漏，完善ip信息
    post_process()

    logger.info("Import done:%s.", counter)
    print("Import done:%s." % counter)


def import_data(cursor,AGENT_NAME,AGENT_CODE,AGENT_VERSION,HOSTNAME,IP_ADDRESS,INSTANCE,AGENT_HOST,AGENT_TYPE):
    global counter
    sqlStr = "insert into " + TABLE_NAME + " (write_time,AGENT_NAME,AGENT_CODE,AGENT_VERSION,HOSTNAME,IP_ADDRESS,INSTANCE,AGENT_HOST,AGENT_TYPE)" \
             "values (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    try:
        cursor.execute(sqlStr,(write_time,AGENT_NAME,AGENT_CODE,AGENT_VERSION,HOSTNAME,IP_ADDRESS,INSTANCE,AGENT_HOST,AGENT_TYPE))
    except:
        print("Duplicated record:%s" % AGENT_NAME)
        logger.error("Duplicated record:%s", AGENT_NAME)
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

    conn = get_conn()
    cursor = conn.cursor();
    cursor.execute("select HOSTNAME,IP_ADDRESS from {0} where HOSTNAME != '' and IP_ADDRESS != ''".format(TABLE_NAME));
    rows = cursor.fetchall()
    for row in rows:
        host_dict[row[0]] = row[1]
    conn.close()

def process_agent():
    global counter
    counter = 0

    conn = get_conn()
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

                if len(agent_name.split(":")) == 2:
                    instance = agent_name.split(":")[0]
                    agent_type = agent_name.split(":")[1]
                if len(agent_name.split(":")) == 3:
                    instance = agent_name.split(":")[0]
                    agent_host = agent_name.split(":")[1]
                    agent_type = agent_name.split(":")[2]

                if agent_code == '01' or agent_code == '02':  # [7048]  ip.pipe:#10.1.71.107[25141]<NM>UMP-JMX3</NM>  10.1.48.52_RWA:UMP-JMX3:01  01  06.23.00  Linux~
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

                if len(agent_name.split(":")) == 2:
                    instance = agent_name.split(":")[0]
                    agent_type = agent_name.split(":")[1]
                if len(agent_name.split(":")) == 3:
                    instance = agent_name.split(":")[0]
                    agent_host = agent_name.split(":")[1]
                    agent_type = agent_name.split(":")[1]

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

                if len(agent_name.split(":")) == 2:
                    instance = agent_name.split(":")[0]
                    agent_type = agent_name.split(":")[1]
                if len(agent_name.split(":")) == 3:
                    instance = agent_name.split(":")[0]
                    agent_host = agent_name.split(":")[1]
                    agent_type = agent_name.split(":")[2]

                if agent_code == 'RZ':  # RZ:OIBS1-OIBS1-BL660216:RDB
                    hostname = agent_host.split('-', 2)[2]  # 存在多个- 的情况，保留第二个-后面的值
                    instance = agent_host.split('-', 2)[1]  #实例名称

                if agent_code == 'HT' or agent_code == 'YJ' or agent_code == 'VM' or agent_code == 'T3':  # BOP:bl685-469:KHTP
                    hostname = agent_name.split(":")[1]


                #print("agent_name:%s  agent_code:%s  agent_version:%s ip_address:%s  hostname:%s" % (agent_name, agent_code, agent_version, ip_address, hostname))
                import_data(cursor, agent_name, agent_code, agent_version, hostname, ip_address, instance, agent_host,agent_type)
            else:
                print("line:" % line)
    conn.commit()
    conn.close()

def post_process():
    get_host_dict()
    conn = get_conn()
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