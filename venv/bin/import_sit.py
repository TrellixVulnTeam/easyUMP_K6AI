#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.etree import ElementTree as et;
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
FILE_PATH = conf.get("SOURCE_FILE", "SIT_PATH")
LOG_FILE = conf.get("BASE_CONF", "LOG_PATH") + "/import_sit.log"
TABLE_NAME = "itm_sit_info"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
global counter_err
counter = 0
counter_err = 0


# 设置log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    logger.info("开始处理situation xml文件！");
    #清空数据库
    clean_db();

    #创建数据库连接
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();

    #根据列出的目录，调用导入函数
    agent_list = ['01','02','GB','HT','LZ','MQ','NT','OQ','RZ','T3','T5','UD','UL','UM','UX','VM','YJ','Others']
    for agent in agent_list:
       path = os.path.join(FILE_PATH,agent)
       word = "CEB_"
       import_agent(cursor,path,word,agent);

    conn.commit()
    conn.close()

    logger.info("共处理situation%s个，其中%s个描述字段不符合规范需整改！",counter,counter_err);


#清空数据库
def clean_db():
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    sql = "delete from " + TABLE_NAME
    cursor.execute(sql);
    conn.commit();
    print("Table %s has been cleaned!" % TABLE_NAME);
    logger.info('表%s已被清空！',TABLE_NAME)


# 按照agent导入
def import_agent(cursor,path, word, agent):
    global counter
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            proc_sit(cursor,fp, agent)
            counter += 1


#解析xml文件，并执行导入
def proc_sit(cursor,xmlfile,agent):
    global counter_err
    threshold = 'null'
    period = 'null'
    isstd_sit = 'null'
    severity = 'null'

    #解析xml文件，获取第一个ROW标签下的值
    tree = et.parse(xmlfile);
    root = tree.getroot()
    row = root.getchildren()[0]
    tempDict = row.attrib
    sql_tmp = "insert into " + TABLE_NAME + " values('" +write_time + "','" + agent + "',";
    for childNode in row.getchildren():
        slotName = childNode.tag;
        slotValue = childNode.text;
        slotValue = str(slotValue);
        slotValue = slotValue.replace('\'', '"')
        sql_tmp = sql_tmp + "'" + slotValue + "',";
        tempDict[slotName] = slotValue;

        #SITNAME
        if str(slotName) == "SITNAME":
            sit_name = str(slotValue)

        #TEXT字段举例： [Status!='DEPLOYED';7*24;1]
        if str(slotName) == "TEXT":
            tmpDesc = str(slotValue).split(';');
            if len(tmpDesc) == 3:
                threshold = tmpDesc[0]
                period = tmpDesc[1]
                isstd_sit = tmpDesc[2]
            else:
                print("Situation描述字段不符合规范：%s" % sit_name )
                logger.warn("Situation描述字段不符合规范：%s",sit_name)
                counter_err += 1

        #级别处理。SITINFO 字段举例 ：  COUNT=3;ATOM=K01SERVER.SERVERNAME;TFWD=Y;SEV=Minor;TDST=0;~;
        if str(slotName) == "SITINFO":
            tmpInfo = str(slotValue)
            tmpSeverity = re.findall(r"SEV=(.*);TDST",tmpInfo)
            if len(tmpSeverity) == 0:
                severity = 'NA'
            elif tmpSeverity[0] == 'Critical':
                severity = '1'
            elif tmpSeverity[0] == 'Minor':
                severity = '2'
            elif tmpSeverity[0] == 'Warning':
                severity = '3'
            else:
                severity = '4'

    sql = sql_tmp + "'" + threshold + "','" + period + "','" + isstd_sit + "','" + severity +  "');"
    #import_data(cursor,sql);
    print(sql)
    cursor.execute(sql)
    return sql;

if __name__ == '__main__':
    main()

