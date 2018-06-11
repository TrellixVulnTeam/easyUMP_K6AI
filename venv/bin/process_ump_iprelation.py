#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
from sub_common import *

# 设置log
logger = get_logger("process.log")

# 特定参数
TABLE_NAME = "CMDB_IP_RELATION"

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
    sql = '''SELECT 
                FLOATIP,MAPPINGIP,PHYSICIP, SYSCODE, APPFULLNAME, AGENTID
            FROM 
                ump.CMDB_OS_RAW
            WHERE 
                USETYPE='生产机' and COLLECTSTATUS !='已下线' and (FLOATIP != 'None' or MAPPINGIP !='None')
        '''
    cursor.execute(sql);
    rows = cursor.fetchall()
    if len(rows) > 0:
        i = 0
        for i in range(len(rows)):
            floatip = str(rows[i][0])
            mappingip = str(rows[i][1])
            phy_ip = str(rows[i][2])
            app_code = str(rows[i][3])
            app_name = str(rows[i][4])
            agentid = str(rows[i][5])

            if  phy_ip != "None":
                ip_type = "PHYSICIP"
                phy_iplist = phy_ip.split(" ")
                if len(phy_iplist) > 1:
                    for phy_ip_instance in phy_iplist:
                        if re.match(r"10\.",phy_ip_instance):
                            phy_ip = phy_ip_instance
                            break
                        elif re.match(r"192\.",phy_ip_instance):
                            phy_ip = phy_ip_instance
            sql = '''insert into {0} (  WRITE_TIME,VIP,MAPPINGIP,PHYSICIP,APP_CODE,APP_NAME,AGENTID)
                        values( %s,%s,%s,%s,%s,%s,%s)
                    '''.format(TABLE_NAME)
            cursor.execute(sql,(write_time,floatip,mappingip,phy_ip,app_code,app_name,agentid))
            counter += 1


    conn.commit()
    conn.close()

if __name__ == '__main__':
        main()