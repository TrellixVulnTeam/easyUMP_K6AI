#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
from sub_common import *

# 设置log
logger = get_logger("process.log")

# 特定参数
TABLE_NAME = "UMP_DOC"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter


def main():
    logger.info("Begin to insert to table:%s",TABLE_NAME)

    delsql = "delete from {0} where MONITOR = 'ITM' ".format(TABLE_NAME)
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
                po.APP_NAME ,po.IP_ADDRESS,po.SIT_NAME, po.SIT_DESC,po.COMPONENT_TYPE,po.COMPONENT,po.SUB_COMPONENT,
                sit.REEV_TIME,sit.MON_PERIOD,sit.THRESHOLD,sit.PDT,sit.SEVERITY,sit.REPEAT_COUNT,
                agt.AGENT_TYPE,agt.MO_TYPE,agt.KEYWORD
            FROM
                ITM_POLICY po,
                ITM_SIT_INFO sit,
                ITM_AGENT_INFO agt
            where
                sit.FORWARD='Y' 
                and po.SIT_NAME = sit.SITNAME
                and po.AGENT_NAME = agt.AGENT_NAME 
        '''
    cursor.execute(sql);
    rows = cursor.fetchall()
    if len(rows) > 0:
        i = 0
        for i in range(len(rows)):
            app_name = str(rows[i][0])
            ip_address = str(rows[i][1])
            sit_name = str(rows[i][2])
            sit_desc = str(rows[i][3])
            component_type = str(rows[i][4])
            component = str(rows[i][5])
            sub_component = str(rows[i][6])
            reev_time = str(rows[i][7])
            mon_period = str(rows[i][8])
            threshold = str(rows[i][9])
            pdt = str(rows[i][10])
            severity = str(rows[i][11])
            repeat_count = str(rows[i][12])
            agent_type = str(rows[i][13])
            mo_type = str(rows[i][14])
            keyword = str(rows[i][15])

            policy_group = ""
            kpi_id = ""
            time_out =""
            drop_in_period = ""
            drop_out_period = ""
            sev1_condition = ""
            sev2_condition = ""
            sev3_condition = ""
            sev4_condition = ""
            sev5_condition = ""
            monitor = "ITM"
            tool_instance = "ITM"
            original_policy = sit_name
            org_type = "总行"
            orgnization = "总行"

            if  threshold:
                alert_condition = threshold + "( {0} )".format(pdt)
            else:
                alert_condition = pdt
            if severity == "1":
                sev1_condition = alert_condition
            elif severity == "2":
                sev2_condition = alert_condition
            elif severity == "3":
                sev3_condition = alert_condition
            elif severity == "4":
                sev4_condition = alert_condition
            else:
                sev5_condition = alert_condition

            tmp_sample_cycle = re.findall(r"^([0-9]{2})([0-9]{2})([0-9]{2})",reev_time)
            sample_cycle = int(tmp_sample_cycle[0][0])*3600 + int(tmp_sample_cycle[0][1])*60 + int(tmp_sample_cycle[0][2])
            values = "%s," * 27 + "%s"
            sql = '''insert into {0} (  WRITE_TIME,KEYWORD,APP_NAME,MO_TYPE,IP_ADDRESS,POLICY_NAME,POLICY_DESC,POLICY_GROUP,COMPONENT_TYPE,COMPONENT,SUB_COMPONENT,
  MONITOR,MON_INSTANCE,KPI_ID,SAMPLE_CYCLE,TIME_OUT,MON_PERIOD,REPEAT_COUNT,SEV1_CONDITION,SEV2_CONDITION,
  SEV3_CONDITION,SEV4_CONDITION,SEV5_CONDITION,DROP_IN_PERIOD,DROP_OUT_PERIOD,ORIGINAL_POLICY,
  ORG_TYPE,ORGNIZATION) values( {1} )'''.format("UMP_DOC",values)
            cursor.execute(sql,(write_time,keyword,app_name,mo_type,ip_address,sit_name,sit_desc,policy_group,component_type,component,sub_component,
                                monitor,tool_instance,kpi_id,str(sample_cycle),time_out,mon_period,repeat_count,sev1_condition,sev2_condition,
                                sev3_condition,sev4_condition,sev5_condition,drop_in_period,drop_out_period,original_policy,org_type,orgnization))
            counter += 1
    conn.commit()
    conn.close()

if __name__ == '__main__':
        main()