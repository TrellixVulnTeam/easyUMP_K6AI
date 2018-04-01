#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
from sub_common import *

# 设置log
logger = get_logger("import.log")

# 特定参数
conf = get_conf()
SOURCE_FILE = conf.get("SOURCE_FILE", "SIT_ENRICH_FILE")
TABLE_NAME = "ITM_SIT_ENRICH"

#设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
global counter_err

def main():
    logger.info("Begin to import %s file.",SOURCE_FILE)

    delsql = "delete from {0} ".format(TABLE_NAME)
    clean_db(delsql)

    process_sit_enrich()

    logger.info("Successfully import %s records!", counter)

def process_sit_enrich():
    global  counter_err
    counter_err = 0
    global  counter
    counter = 0

    conn = get_conn()
    cursor = conn.cursor();
    with open(SOURCE_FILE, 'r',encoding='UTF-8') as file_to_read:
        for lines in file_to_read.readlines():
            lines_tmp =  lines.split('\t')

            SITNAME = lines_tmp[0]
            SIT_DESC = lines_tmp[1]
            THRESHOLD_FLAG = lines_tmp[2]
            CUR_VALUE_FLAG = lines_tmp[3]
            DISPLAY_FLAG = lines_tmp[4]
            N_ComponentType = lines_tmp[5]
            N_ComponentTypeId = lines_tmp[6]
            N_Component = lines_tmp[7]
            N_ComponentId = lines_tmp[8]
            N_SubComponent = lines_tmp[9]
            N_SubComponentId = lines_tmp[10]
            sqlStr = "insert into {0} (WRITE_TIME,SITNAME,SIT_DESC,THRESHOLD_FLAG,CUR_VALUE_FLAG,DISPLAY_FLAG,N_ComponentType,N_ComponentTypeId,N_Component,N_ComponentId,N_SubComponent,N_SubComponentId) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(TABLE_NAME)
            try:
                cursor.execute(sqlStr,(write_time,SITNAME,SIT_DESC,THRESHOLD_FLAG,CUR_VALUE_FLAG,DISPLAY_FLAG,N_ComponentType,N_ComponentTypeId,N_Component,N_ComponentId,N_SubComponent,N_SubComponentId));
                counter += 1
            except:
                    logger.error("Duplicated situation: %s", SITNAME )
                    counter_err += 1
    conn.commit()
    conn.close()

if __name__ == '__main__':
        main()

