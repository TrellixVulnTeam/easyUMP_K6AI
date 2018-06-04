#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.etree import ElementTree as et;
import datetime
from sub_common import *

# 设置log
logger = get_logger("import_cmdb.log")

# 特定参数
conf = get_conf()
SOURCE_FILE_OS = conf.get("SOURCE_FILE", "CMDB_OS_FILE")
SOURCE_FILE_ORACLESID = conf.get("SOURCE_FILE", "CMDB_ORACLESID_FILE")
SOURCE_FILE_WEBLOGIC = conf.get("SOURCE_FILE", "CMDB_WEBLOGIC_FILE")
SOURCE_FILE_WEBLOGIC_DOMAIN = conf.get("SOURCE_FILE", "CMDB_WEBLOGIC_DOMAIN_FILE")
SOURCE_FILE_TUXEDO = conf.get("SOURCE_FILE", "CMDB_TUXEDO_FILE")
TABLE_NAME_OS = "CMDB_OS_RAW"
TABLE_NAME_ORACLESID = "CMDB_ORACLESID_RAW"
TABLE_NAME_WEBLOGIC = "CMDB_WEBLOGIC_RAW"
TABLE_NAME_WEBLOGIC_DOMAIN = "CMDB_WEBLOGIC_DOMAIN_RAW"
TABLE_NAME_TUXEDO = "CMDB_TUXEDO_RAW"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter

def main():

    # 处理OperationServer数据
    logger.info("Begin to import %s file !", SOURCE_FILE_OS)
    delsql = "delete from {0} ".format(TABLE_NAME_OS)
    clean_db(delsql);
    v_date_para = re.findall(r"\[(.*)\]", SOURCE_FILE_OS)[0]
    new_date = datetime.datetime.now().strftime(v_date_para)
    SOURCE_FILE_OS_FULL = re.sub("\[.*\]", new_date, SOURCE_FILE_OS)
    process(SOURCE_FILE_OS_FULL,TABLE_NAME_OS);
    logger.info("Total import %s records.",counter)

    # 处理ORACLE数据
    logger.info("Begin to import %s file !", SOURCE_FILE_ORACLESID)
    delsql = "delete from {0} ".format(TABLE_NAME_ORACLESID)
    clean_db(delsql);
    v_date_para = re.findall(r"\[(.*)\]", SOURCE_FILE_ORACLESID)[0]
    new_date = datetime.datetime.now().strftime(v_date_para)
    SOURCE_FILE_ORACLESID_FULL = re.sub("\[.*\]", new_date, SOURCE_FILE_ORACLESID)
    process(SOURCE_FILE_ORACLESID_FULL,TABLE_NAME_ORACLESID);
    logger.info("Total import %s records.",counter)

    # 处理Webligc Domain数据
    logger.info("Begin to import %s file !", SOURCE_FILE_WEBLOGIC_DOMAIN)
    delsql = "delete from {0} ".format(TABLE_NAME_WEBLOGIC_DOMAIN)
    clean_db(delsql);
    v_date_para = re.findall(r"\[(.*)\]", SOURCE_FILE_WEBLOGIC_DOMAIN)[0]
    new_date = datetime.datetime.now().strftime(v_date_para)
    SOURCE_FILE_WEBLOGIC_DOMAIN_FULL = re.sub("\[.*\]", new_date, SOURCE_FILE_WEBLOGIC_DOMAIN)
    process(SOURCE_FILE_WEBLOGIC_DOMAIN_FULL,TABLE_NAME_WEBLOGIC_DOMAIN);
    logger.info("Total import %s records.",counter)

    # 处理Webligc Server数据
    logger.info("Begin to import %s file !", SOURCE_FILE_WEBLOGIC)
    delsql = "delete from {0} ".format(TABLE_NAME_WEBLOGIC)
    clean_db(delsql);
    v_date_para = re.findall(r"\[(.*)\]", SOURCE_FILE_WEBLOGIC)[0]
    new_date = datetime.datetime.now().strftime(v_date_para)
    SOURCE_FILE_WEBLOGIC_FULL = re.sub("\[.*\]", new_date, SOURCE_FILE_WEBLOGIC)
    process(SOURCE_FILE_WEBLOGIC_FULL,TABLE_NAME_WEBLOGIC);
    logger.info("Total import %s records.",counter)

    # 处理Webligc Server数据
    logger.info("Begin to import %s file !", SOURCE_FILE_TUXEDO)
    delsql = "delete from {0} ".format(TABLE_NAME_TUXEDO)
    clean_db(delsql);
    v_date_para = re.findall(r"\[(.*)\]", SOURCE_FILE_TUXEDO)[0]
    new_date = datetime.datetime.now().strftime(v_date_para)
    SOURCE_FILE_TUXEDO_FULL = re.sub("\[.*\]", new_date, SOURCE_FILE_TUXEDO)
    process(SOURCE_FILE_TUXEDO_FULL,TABLE_NAME_TUXEDO);
    logger.info("Total import %s records.",counter)


#处理XML文件
def process(SOURCE_FILE,TABLE_NAME):
    global counter
    counter = 0
    conn = get_conn()
    cursor = conn.cursor();
    cursor.execute("set names utf8")
    root = et.parse(SOURCE_FILE);
    for recordInfo in root.iter("recordInfo"):
        tempDict = recordInfo.attrib
        sql_tmp = "insert into {0} values('{1}',".format(TABLE_NAME,write_time);
        for fieldInfo in recordInfo.findall("fieldInfo"):
            slotName = fieldInfo.find('fieldChName').text;
            slotValue = fieldInfo.find("fieldContent").text;
            sql_tmp = sql_tmp + "'" + str(slotValue) + "',";
            tempDict[slotName] = slotValue;
        sql = sql_tmp[:-1];
        sql = sql + ");"
        cursor.execute(sql)
        counter += 1
    conn.commit();
    conn.close()

if __name__ == '__main__':
    main()
