#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.etree import ElementTree as et;
import re
import datetime
import os
from sub_common import *

# 设置log
logger = get_logger("import.log")

# 特定参数
conf = get_conf()
FILE_PATH = conf.get("SOURCE_FILE", "SIT_PATH")
TABLE_NAME = "ITM_SIT_INFO"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
global counter_err

def main():
    logger.info("Begin to import xml files in SITUATION directory.");
    #清空数据库
    delsql = "delete from {0} ".format(TABLE_NAME)
    clean_db(delsql)

    #创建数据库连接
    conn = get_conn()
    cursor = conn.cursor();

    #根据列出的目录，调用导入函数
    agent_list = ['01','02','GB','HT','LZ','MQ','NT','OQ','RZ','T3','T5','UD','UL','UM','UX','VM','YJ','Others']
    logger.info("Processing directory: %s",agent_list)
    for agent in agent_list:
       path = os.path.join(FILE_PATH,agent)
       word = "CEB_"
       import_agent(cursor,path,word,agent);

    conn.commit()
    conn.close()

    logger.info("Successfully import situations:%s. Warning records:%s.",counter,counter_err);


# 按照agent导入
def import_agent(cursor,path, word, agent):
    global counter
    counter = 0
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and word in filename:
            proc_sit(cursor,fp, agent)
            counter += 1


#解析xml文件，并执行导入
def proc_sit(cursor,xmlfile,agent):
    global counter_err
    counter_err =0
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
                print("Format is error:%s." % sit_name )
                logger.warn("Format is error:%s.",sit_name)
                counter_err += 1

        #级别、次数等字段抽取。SITINFO 字段举例 ：  COUNT=3;ATOM=K01SERVER.SERVERNAME;TFWD=Y;SEV=Minor;TDST=0;~;
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

            sitforward = re.findall(r"TFWD=([YN]);",tmpInfo)
            # if not sitforward:
            #     sitforward = 'N'

            samplecount = re.findall(r"COUNT=([0-9]{1,2})",tmpInfo)
            if not samplecount:
                samplecount = ('0',)

            atom = re.findall(r"ATOM=([0-9A-Z.]*);",tmpInfo)
            if not atom:
                atom = ('',)

    #sql = sql_tmp + "'" + threshold + "','" + period + "','" + isstd_sit + "','" + severity +  "');"
    sql = sql_tmp + "'{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(threshold,period,isstd_sit,severity,sitforward[0],samplecount[0],atom[0])
    cursor.execute(sql)

if __name__ == '__main__':
    main()
