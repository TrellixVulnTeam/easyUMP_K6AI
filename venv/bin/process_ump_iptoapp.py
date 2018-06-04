#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
from sub_common import *

# 设置log
logger = get_logger("process.log")

# 特定参数
TABLE_NAME = "CMDB_IPTOAPP"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter


def main():
    logger.info("Begin to insert to table:%s",TABLE_NAME)
    delsql = "delete from {0} ".format(TABLE_NAME)
    clean_db(delsql)
    logger.info("Table %s has been cleaned!",TABLE_NAME)
    process_import()
    logger.info("Success insert records:%s.",counter)

def process_import():
    global counter
    counter = 0
    conn = get_conn()
    cursor = conn.cursor();
    sql = '''select 
                PHYSICIP,AGENTID,SYSCODE,APPFULLNAME,USETYPE,IP,FLOATIP,MAPPINGIP 
            from 
                CMDB_OS_RAW
            where 
                USETYPE='生产机' 
        '''
    cursor.execute(sql);
    rows = cursor.fetchall()
    if len(rows) > 0:
        i = 0
        for i in range(len(rows)):
            phy_ip = str(rows[i][0])
            agentid = str(rows[i][1])
            app_code = str(rows[i][2])
            app_name = str(rows[i][3])
            usetype = str(rows[i][4])
            ip = str(rows[i][5])
            floatip = str(rows[i][6])
            mappingip = str(rows[i][7])

            ip_source = "CMDB_OS"

            if  phy_ip != "None":
                ip_type = "PHYSICIP"
                ip_address = phy_ip
                sql = '''insert into {0} (  WRITE_TIME,IP_ADDRESS,IP_TYPE,IP_SOURCE,APP_CODE,APP_NAME,USETYPE)
                        values( %s,%s,%s,%s,%s,%s,%s)
                    '''.format(TABLE_NAME)
                cursor.execute(sql,(write_time,ip_address,ip_type,ip_source,app_code,app_name,usetype))
                counter += 1

            if mappingip != "None":
                ip_type = "MAPPINGIP"
                ip_address = mappingip
                sql = '''insert into {0} (  WRITE_TIME,IP_ADDRESS,IP_TYPE,IP_SOURCE,APP_CODE,APP_NAME,USETYPE)
                        values( %s,%s,%s,%s,%s,%s,%s)
                    '''.format(TABLE_NAME)
                cursor.execute(sql,(write_time,ip_address,ip_type,ip_source,app_code,app_name,usetype))
                counter += 1

            if floatip != "None":
                ip_type = "VIP"
                ip_address = floatip
                sql = '''insert into {0} (  WRITE_TIME,IP_ADDRESS,IP_TYPE,IP_SOURCE,APP_CODE,APP_NAME,USETYPE)
                        values( %s,%s,%s,%s,%s,%s,%s)
                    '''.format(TABLE_NAME)
                cursor.execute(sql,(write_time,ip_address,ip_type,ip_source,app_code,app_name,usetype))
                counter += 1

            if ip != "None":
                iplist = ip.split(" ")
                for ip_instance in iplist:
                    if not re.match(r"172",ip_instance) and not re.match(r"169",ip_instance) and \
                            ip_instance != floatip and ip_instance != mappingip and ip_instance != phy_ip \
                            and ip_instance != '':
                        ip_type = "OTHERS"
                        ip_address = ip_instance
                        sql = '''insert into {0} (  WRITE_TIME,IP_ADDRESS,IP_TYPE,IP_SOURCE,APP_CODE,APP_NAME,USETYPE)
                                values( %s,%s,%s,%s,%s,%s,%s)
                            '''.format(TABLE_NAME)
                        cursor.execute(sql, (write_time, ip_address, ip_type, ip_source, app_code, app_name, usetype))
                        counter += 1
    conn.commit()
    conn.close()

if __name__ == '__main__':
        main()