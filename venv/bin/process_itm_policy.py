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
LOG_FILE = conf.get("BASE_CONF", "LOG_PATH") + "/process_itm_policy.log"
TABLE_NAME = "itm_policy"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
counter = 0
global agent_to_ip_dict
agent_to_ip_dict = {}
global agent_to_host_dict
agent_to_host_dict = {}
global group_to_agent_dict
group_to_agent_dict = {}


# 设置log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    logger.info('开始处理ITM档案信息分析和入库！')
    clean_db()
    query_sit()
    logger.info("处理完成！共导入%s条档案信息",counter)

def isIP(str): #判断字符串是否IP地址格式
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def clean_db():
    conn = get_conn()
    cursor = conn.cursor();
    sql = "delete from " + TABLE_NAME
    cursor.execute(sql);
    conn.commit();
    print("Table %s has been cleaned!" % TABLE_NAME);
    logger.info('表%s已被清空！',TABLE_NAME)

def query_sit():
    agent_to_ip_dict()
    agent_to_host_dict()

    f = open("rs.txt", 'w', encoding="utf8");
    f.write("开始写文件\n")
    f.close()
    conn = get_conn()
    cursor = conn.cursor();
    sqlStr = "select SITNAME,DISTRIBUTION from itm_sit_info";
    cursor.execute(sqlStr); #循环所有situation
    rows_sit = cursor.fetchall()
    f = open("rs.txt", 'a', encoding="utf8");
    if len(rows_sit) > 0:
        for i in range(len(rows_sit)):

            #根据situation名字进行丰富
            sitname = str(rows_sit[i][0])
            sqlStr = "select SIT_DESC,N_ComponentType,N_Component,N_SubComponent from itm_sit_enrich where SITNAME = \'{0}\'".format(
                sitname)
            cursor.execute(sqlStr)
            rows_enrich = cursor.fetchall()
            if len(rows_enrich) == 0:
                sit_desc = ''
                n_componenttype = ''
                n_component = ''
                n_subcomponent = ''
            elif len(rows_enrich) > 0:
                sit_desc = rows_enrich[0][0]
                n_componenttype = rows_enrich[0][1]
                n_component = rows_enrich[0][2]
                n_subcomponent = rows_enrich[0][3]

            #根据situation名字查找sit原始信息
            sitname = str(rows_sit[i][0])
            sqlStr = "select ISSTD,PDT,THRESHOLD,SEVERITY from itm_sit_info " \
                     "where SITNAME = \'{0}\'".format(sitname)
            cursor.execute(sqlStr)
            rows_enrich = cursor.fetchall()
            if len(rows_enrich) == 0:
                isstd = ''
                pdt = ''
                threshold = ''
                severity = ''
            elif len(rows_enrich) > 0:
                isstd = rows_enrich[0][0]
                pdt = rows_enrich[0][1]
                threshold = rows_enrich[0][2]
                severity = rows_enrich[0][3]

            #根据下发的组或者agent列表进行处理
            dist = str(rows_sit[i][1]).split(',')
            group_flag = str(rows_sit[i][1]).find(':')  #根据冒号判断是发到组还是Agent。 如果未找到，则值为-1
            if  group_flag != -1 : #situation直接下发到Agent的情况
                for agent in dist:
                    try:
                        ip_address = agent_to_ip_dict[agent]
                    except:
                        ip_address = ''

                    try:
                        host = agent_to_host_dict[agent]
                    except:
                        host = ''

                    appname = iptoapp(ip_address)
                    content = str(sitname) + ":" + host + ":" + ip_address + ":" + appname[0] + ":" + sit_desc + ":" + n_componenttype + ":" + n_component + ":" + n_subcomponent +  ":" + severity + "\n"
                    f.write(content)
                    import_data(cursor,sitname,host,ip_address,agent,appname[0],sit_desc,n_componenttype,n_component,n_subcomponent,severity)

                pass

            elif group_flag == -1 : #situation下发到组的情况

                for group in dist:
                    try:
                        agent_list = group_to_agent(group)
                        pass
                    except:
                        print(sitname,group)
                        continue
                    for agent in agent_list :
                        try:
                            host = agent_to_host_dict[agent]  # 找到主机名
                        except:
                            host = ''
                        try:
                            ip_address = agent_to_ip_dict[agent]  # 找到IP
                        except:
                            ip_address = ''
                        appname = iptoapp(ip_address)  # 根据IP地址，查找应用系统信息

                        #print(str(sitname) + ":"+ agent[0] + ":" + ip_address[0] + ":" + sit_desc + ":" + n_componenttype + ":" + n_component + ":" + n_subcomponent)
                        content = str(sitname) + ":"+ host + ":" + ip_address + ":" + appname[0] + ":" + sit_desc + ":" + n_componenttype + ":" + n_component + ":" + n_subcomponent +  ":" + severity +  "\n"
                        f.write(content)
                        import_data(cursor,sitname, host, ip_address, agent, appname[0], sit_desc, n_componenttype, n_component,n_subcomponent,severity)
                        pass
    conn.commit()
    conn.close()
    f.close()

def import_data(cursor,sitname,host,ip_address,agent,appname,sit_desc,n_componenttype,n_component,n_subcomponent,severity):
    global counter
    sqlStr = "insert into itm_policy  (WRITE_TIME,APP_NAME,IP_ADDRESS,AGENT_NAME,HOSTNAME,SIT_NAME,SIT_DESC,COMPONENT_TYPE,COMPONENT,SUB_COMPONENT,SEVERITY)" \
             "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
    cursor.execute(sqlStr,(write_time,appname,ip_address,agent,host,sitname,sit_desc,n_componenttype,n_component,n_subcomponent,severity))
    counter += 1

def iptoapp(ip_address):
    appname = ()
    conn = get_conn()
    cursor = conn.cursor();
    sqlStr = "select APP_NAME from itm_iptoapp where IP_ADDRESS = '" + ip_address + "'"
    cursor.execute(sqlStr);
    rows_app = cursor.fetchall()
    if len(rows_app) > 0 : #如果找到了APP，则赋值
        appname = rows_app[0]
    elif len(rows_app) == 0: #如果没找到，则赋默认值
        appname = ('',)
    conn.close()
    return(appname)


def agent_to_ip_dict():
    global agent_to_ip_dict
    conn = get_conn()
    cursor = conn.cursor();
    cursor.execute("select AGENT_NAME,IP_ADDRESS from itm_agent_info where IP_ADDRESS != ''");
    rows = cursor.fetchall()
    agent_to_ip_dict = {}
    for row in rows:
        agent_to_ip_dict[row[0]] = row[1]
    conn.close()

def agent_to_host_dict():
    global agent_to_host_dict
    #conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("select AGENT_NAME,HOSTNAME from itm_agent_info where HOSTNAME != ''");
    rows = cursor.fetchall()
    agent_to_host_dict = {}
    for row in rows:
        agent_to_host_dict[row[0]] = row[1]
    conn.close()

def group_to_agent(group_name):
    conn = get_conn()
    cursor = conn.cursor();
    cursor.execute("select AGENT_NAME from itm_group_info where GROUP_NAME = %s",group_name);
    rows = cursor.fetchall()
    agent_list = []
    for row in rows:
        agent_list.append(row[0])
    conn.close()
    return (agent_list)


def get_conn():
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    return(conn)


if __name__ == '__main__':
        main()