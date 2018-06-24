#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
from sub_common import *

# 设置log
logger = get_logger("report.log")

# 特定参数
STD_CONF_TABLE = "UMP_STD_CONF"
RESULT_TABLE = "UMP_EVAL_RESULT"


# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
global std_all

def main():
    logger.info("Begin to insert to table:%s",RESULT_TABLE)
    compare("LINUX OS ITM监控标准(平稳型)")
    compare("LINUX OS ITM监控标准(震荡型)")
    compare("AIX OS ITM监控标准(平稳型)")
    compare("AIX OS ITM监控标准(震荡型)")
    compare("WINDOWS OS ITM监控标准(平稳型)")
    compare("WINDOWS OS ITM监控标准(震荡型)")
    compare("AIX/LINUX 系统日志监控标准")

def compare(std_name):
    global std_all
    std_all = []
    conn = get_conn()
    cursor = conn.cursor()

    # 先删除结果集
    delsql = "delete from {0} where STD_NAME ='{1}'".format(RESULT_TABLE,std_name)
    cursor.execute(delsql)
    conn.commit()

    # 查询评价规则表
    sql = "select FILTER,POLICY_NAME from {0} where STD_NAME='{1}' ".format(STD_CONF_TABLE,std_name)
    cursor.execute(sql)
    rows = cursor.fetchall()
    if len(rows) > 0:

        # 计算标准策略总数
        for row in rows:
            std_all.append(row[1])
        count_all = len(std_all)

        # 获取MO过滤条件，查找到所有MO全集
        filter = rows[0][0]
        sql_all_mo = str(filter).split(";")[0]
        mo_type = str(filter).split(";")[1].split("=")[1]
        cursor.execute(sql_all_mo)
        mo_data = cursor.fetchall()

        # 针对每个MO，循环查找相关的策略，并写入结果
        for mo in mo_data:
            # 赋初值
            std_pct = 0
            count_real = 0
            count_ext = 0
            policy_real = []
            policy_custom = []
            policy_delta = []

            # 标准规则语句返回3个值
            mo_all_keyword = mo[0]
            ip_address = mo[1]
            app_name = mo[2]

            # 查找单个MO关联的策略
            sql_ump_mo = "select POLICY_NAME from UMP_DOC where KEYWORD='{0}' and MO_TYPE='{1}'"\
                .format(mo_all_keyword,mo_type)
            cursor.execute(sql_ump_mo)
            results = cursor.fetchall()

            if len(results) > 0:

                # 判断是否标准策略，并记数
                for result in results:
                    policy_name = result[0]
                    if policy_name in std_all:
                        count_real += 1
                        policy_real.append(policy_name)
                    else:
                        count_ext += 1
                        policy_custom.append(policy_name)
                #policy_delta = list(set(std_all) - set(policy_real))
                policy_delta = list(set(std_all).difference(set(policy_real)))
                std_pct = 100 * count_real / count_all
            else:
                policy_delta = std_all

            sql_insert = '''insert into {0} (WRITE_TIME,STD_NAME,APP_NAME,MO_TYPE,KEYWORD,IP_ADDRESS,STD_POLICY_COUNT,
                         REAL_STD_POLICY_COUNT,CUSTOM_POLICY_COUNT,STD_POLICY_PCT,STD_DELTA_LIST,CUSTOM_POLICY_LIST) values
                         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''.format(RESULT_TABLE)
            cursor.execute(sql_insert,(write_time,std_name,app_name,mo_type,mo_all_keyword,ip_address,count_all,count_real,count_ext,std_pct,str(policy_delta),str(policy_custom)))
    conn.commit()
    conn.close()

    logger.info("Success insert records.")

if __name__ == '__main__':
        main()