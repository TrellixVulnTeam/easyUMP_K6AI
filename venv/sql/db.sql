docker run --name easyump-mysql -v /opt/mysql_data:/var/lib/mysql -p 3333:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

创建模式
CREATE SCHEMA `ump` DEFAULT CHARACTER SET utf8 ;

drop table if exists UMP_DOC;
CREATE TABLE ump.`UMP_DOC` (
  `WRITE_TIME` datetime NOT NULL,
  `KEYWORD` varchar(128) NOT NULL,
  `APP_NAME` varchar(64) DEFAULT NULL,
  `MO_TYPE` varchar(64) NOT NULL,
  `IP_ADDRESS` varchar(64) DEFAULT NULL,
  `POLICY_NAME` varchar(128) NOT NULL,
  `POLICY_DESC` varchar(256) DEFAULT NULL,
  `POLICY_GROUP` varchar(256) DEFAULT NULL,
  `COMPONENT_TYPE` varchar(64) DEFAULT NULL,
  `COMPONENT` varchar(64) DEFAULT NULL,
  `SUB_COMPONENT` varchar(64) DEFAULT NULL,
  `MONITOR` varchar(64) DEFAULT NULL,
  `MON_INSTANCE` varchar(64) DEFAULT NULL,
  `KPI_ID` varchar(32) DEFAULT NULL,
  `SAMPLE_CYCLE` varchar(64) DEFAULT NULL,
  `TIME_OUT` varchar(64) DEFAULT NULL,
  `MON_PERIOD` varchar(64) DEFAULT NULL,
  `REPEAT_COUNT` varchar(64) DEFAULT NULL,
  `SEV1_CONDITION` text,
  `SEV2_CONDITION` text,
  `SEV3_CONDITION` text,
  `SEV4_CONDITION` text,
  `SEV5_CONDITION` text,
  `DROP_IN_PERIOD` varchar(32) DEFAULT NULL,
  `DROP_OUT_PERIOD` varchar(32) DEFAULT NULL,
  `ORIGINAL_POLICY` varchar(128) DEFAULT NULL,
  `ORG_TYPE` varchar(64) DEFAULT NULL,
  `ORGNIZATION` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists ITM_SIT_INFO;
CREATE TABLE `ITM_SIT_INFO` (
  `WRITE_TIME` datetime NOT NULL,
  `AGENT` varchar(64) NOT NULL,
  `SITNAME` varchar(64) NOT NULL,
  `FULLNAME` varchar(64) DEFAULT NULL,
  `ADVISE` varchar(64) DEFAULT NULL,
  `AFFINITIES` varchar(64) DEFAULT NULL,
  `ALERTLIST` varchar(64) DEFAULT NULL,
  `AUTOSOPT` varchar(64) DEFAULT NULL,
  `AUTOSTART` varchar(64) DEFAULT NULL,
  `CMD` text,
  `DESTNODE` varchar(64) DEFAULT NULL,
  `HUB` varchar(64) DEFAULT NULL,
  `LOCFLAG` varchar(64) DEFAULT NULL,
  `LSTCCSID` varchar(64) DEFAULT NULL,
  `LSTDATE` varchar(64) DEFAULT NULL,
  `LSTRELEASE` varchar(64) DEFAULT NULL,
  `LSTUSRPRF` varchar(64) DEFAULT NULL,
  `NOTIFYARGS` varchar(64) DEFAULT NULL,
  `NOTIFYOPTS` varchar(64) DEFAULT NULL,
  `OBJECTLOCK` varchar(64) DEFAULT NULL,
  `PDT` text,
  `PRNAMES` varchar(64) DEFAULT NULL,
  `QIBSCOPE` varchar(64) DEFAULT NULL,
  `REEV_DAYS` varchar(64) DEFAULT NULL,
  `REEV_TIME` varchar(64) DEFAULT NULL,
  `REFLEXOK` varchar(64) DEFAULT NULL,
  `SENDMSGQ` varchar(64) DEFAULT NULL,
  `SITINFO` varchar(64) DEFAULT NULL,
  `SOURCE` varchar(64) DEFAULT NULL,
  `TEXT` varchar(64) DEFAULT NULL,
  `DISTRIBUTION` text,
  `THRESHOLD` varchar(64) DEFAULT NULL,
  `MON_PERIOD` varchar(64) DEFAULT NULL,
  `ISSTD` varchar(64) DEFAULT NULL,
  `SEVERITY` varchar(32) DEFAULT NULL,
  `FORWARD` varchar(16) DEFAULT NULL,
  `REPEAT_COUNT` varchar(16) DEFAULT NULL,
  `ATOM` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`WRITE_TIME`,`SITNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists APP_INFO;
CREATE TABLE `APP_INFO` (
  `WRITE_TIME` datetime NOT NULL,
  `c1` varchar(64) NOT NULL,
  `systemcode` varchar(64) DEFAULT NULL,
  `systemname` varchar(64) DEFAULT NULL,
  `eapssystemname` varchar(64) DEFAULT NULL,
  `englishcode` varchar(64) DEFAULT NULL,
  `affectsystem` varchar(64) DEFAULT NULL,
  `branch` varchar(64) DEFAULT NULL,
  `key_sys` varchar(64) DEFAULT NULL,
  `status` varchar(64) DEFAULT NULL,
  `securitylevel` varchar(64) DEFAULT NULL,
  `scope` varchar(64) DEFAULT NULL,
  `systempro` varchar(64) DEFAULT NULL,
  `onlinedate` int(11) DEFAULT NULL,
  `outlinedate` int(11) DEFAULT NULL,
  `serverlevel` varchar(64) DEFAULT NULL,
  `systemlevel` varchar(64) DEFAULT NULL,
  `isimportant` varchar(64) DEFAULT NULL,
  `iskey` varchar(64) DEFAULT NULL,
  `iscoresyetem` varchar(64) DEFAULT NULL,
  `cbrcimportantsystem` varchar(64) DEFAULT NULL,
  `applicateoperate` varchar(64) DEFAULT NULL,
  `outsourcingmark` varchar(64) DEFAULT NULL,
  `networkdomain` varchar(64) DEFAULT NULL,
  `team` varchar(64) DEFAULT NULL,
  `teamid` varchar(64) DEFAULT NULL,
  `operatemanager` varchar(64) DEFAULT NULL,
  `operatemanagerid` varchar(64) DEFAULT NULL,
  `applicatemanagerA` varchar(64) DEFAULT NULL,
  `applicatemanageraid` varchar(64) DEFAULT NULL,
  `applicatemanagerB` varchar(64) DEFAULT NULL,
  `applicatemanagerbid` varchar(64) DEFAULT NULL,
  `systemmanagerA` varchar(64) DEFAULT NULL,
  `systemmanageraid` varchar(64) DEFAULT NULL,
  `systemmanagerB` varchar(64) DEFAULT NULL,
  `systemmanagerbid` varchar(64) DEFAULT NULL,
  `DBA` varchar(64) DEFAULT NULL,
  `dbaid` varchar(64) DEFAULT NULL,
  `dbab` varchar(64) DEFAULT NULL,
  `dbabid` varchar(64) DEFAULT NULL,
  `middlewaremanager` varchar(64) DEFAULT NULL,
  `middlewaremanagerid` varchar(64) DEFAULT NULL,
  `middlewaremanagerb` varchar(64) DEFAULT NULL,
  `middlewaremanagerbid` varchar(64) DEFAULT NULL,
  `storemanager` varchar(64) DEFAULT NULL,
  `storemanagerid` varchar(64) DEFAULT NULL,
  `PM` varchar(64) DEFAULT NULL,
  `pmid` varchar(64) DEFAULT NULL,
  `businessdepartment` varchar(64) DEFAULT NULL,
  `businessdepartmentid` varchar(64) DEFAULT NULL,
  `businessmanager` varchar(64) DEFAULT NULL,
  `businessmanagerid` varchar(64) DEFAULT NULL,
  `servicesupporter` varchar(64) DEFAULT NULL,
  `servicesupporterid` varchar(64) DEFAULT NULL,
  `istestcenter` varchar(64) DEFAULT NULL,
  `allottestmanager` varchar(64) DEFAULT NULL,
  `allottestmanagerid` varchar(64) DEFAULT NULL,
  `deliverytestmanager` varchar(64) DEFAULT NULL,
  `deliverytestmanagerid` varchar(64) DEFAULT NULL,
  `qualitymanager` varchar(64) DEFAULT NULL,
  `qualitymanagerid` varchar(64) DEFAULT NULL,
  `performancetestmanag` varchar(64) DEFAULT NULL,
  `performancetestmanagid` varchar(64) DEFAULT NULL,
  `transfercoefficient` varchar(64) DEFAULT NULL,
  `stage` varchar(64) DEFAULT NULL,
  `businessintroduction` varchar(512) DEFAULT NULL,
  `systemmanagerid` varchar(64) DEFAULT NULL,
  `systemmanager` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`c1`,`WRITE_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists ITM_AGENT_ENRICH;
CREATE TABLE `ITM_AGENT_ENRICH` (
  `WRITE_TIME` datetime NOT NULL,
  `AGENT_TYPE` varchar(128) NOT NULL,
  `MO_TYPE` varchar(64) DEFAULT NULL,
  `KEYWORD` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists ITM_AGENT_INFO;
CREATE TABLE `ITM_AGENT_INFO` (
  `WRITE_TIME` datetime NOT NULL,
  `AGENT_NAME` varchar(64) NOT NULL,
  `AGENT_CODE` varchar(32) DEFAULT NULL,
  `AGENT_VERSION` varchar(64) DEFAULT NULL,
  `HOSTNAME` varchar(64) DEFAULT NULL,
  `IP_ADDRESS` varchar(64) DEFAULT NULL,
  `INSTANCE` varchar(64) DEFAULT NULL,
  `AGENT_HOST` varchar(64) DEFAULT NULL,
  `AGENT_TYPE` varchar(64) DEFAULT NULL,
  `KEYWORD` varchar(128) DEFAULT NULL,
  `MO_TYPE` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`AGENT_NAME`,`WRITE_TIME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists ITM_GROUP_INFO;
CREATE TABLE `ITM_GROUP_INFO` (
  `WRITE_TIME` datetime NOT NULL,
  `GROUP_NAME` varchar(64) NOT NULL,
  `AGENT_NAME` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists ITM_IPTOAPP;
CREATE TABLE `ITM_IPTOAPP` (
  `WRITE_TIME` datetime NOT NULL,
  `IP_ADDRESS` varchar(64) NOT NULL,
  `APP_NAME` varchar(64) NOT NULL,
  `APP_CODE` varchar(64) NOT NULL,
  PRIMARY KEY (`WRITE_TIME`,`IP_ADDRESS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists ITM_POLICY;
CREATE TABLE `ITM_POLICY` (
  `WRITE_TIME` datetime NOT NULL,
  `APP_NAME` varchar(64) DEFAULT NULL,
  `IP_ADDRESS` varchar(64) DEFAULT NULL,
  `AGENT_NAME` varchar(64) DEFAULT NULL,
  `HOSTNAME` varchar(64) DEFAULT NULL,
  `SIT_NAME` varchar(64) NOT NULL,
  `SIT_DESC` varchar(128) DEFAULT NULL,
  `COMPONENT_TYPE` varchar(64) DEFAULT NULL,
  `COMPONENT` varchar(64) DEFAULT NULL,
  `SUB_COMPONENT` varchar(64) DEFAULT NULL,
  `SEVERITY` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists ITM_SIT_ENRICH;
CREATE TABLE `ITM_SIT_ENRICH` (
	`WRITE_TIME` datetime NOT NULL,
    `SITNAME`        varchar(64) NOT NULL,
    `SIT_DESC`        varchar(128) NOT NULL,
    `THRESHOLD_FLAG`    varchar(64) NOT NULL,
    `CUR_VALUE_FLAG`    varchar(64) NOT NULL,
    `DISPLAY_FLAG`      varchar(64) NOT NULL,
    `N_ComponentType`   varchar(64) NOT NULL,
    `N_ComponentTypeId` varchar(64) NOT NULL,
    `N_Component`       varchar(64) NOT NULL,
    `N_ComponentId`     varchar(64) NOT NULL,
    `N_SubComponent`    varchar(64) NOT NULL,
    `N_SubComponentId`  varchar(64) NOT NULL,
    PRIMARY KEY (`WRITE_TIME`,`SITNAME`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CMDB_OS_RAW` (
  `WRITE_TIME` datetime NOT NULL,
  `MAPPINGIP` varchar(64) DEFAULT NULL,
  `LOGICALCODE` varchar(64) DEFAULT NULL,
  `APPSYSTEMNAME` varchar(64) DEFAULT NULL,
  `PARTYPE` varchar(64) DEFAULT NULL,
  `EQUIPTYPE` varchar(64) DEFAULT NULL,
  `USETYPE` varchar(64) DEFAULT NULL,
  `LOGICALUSEFULL` varchar(64) DEFAULT NULL,
  `FLOATIP` varchar(64) DEFAULT NULL,
  `VMTYPE` varchar(64) DEFAULT NULL,
  `SYSTEM_VERSION` varchar(64) DEFAULT NULL,
  `HBACARDNUMBER` varchar(64) DEFAULT NULL,
  `COLLECTSN` varchar(64) DEFAULT NULL,
  `VMIP` varchar(64) DEFAULT NULL,
  `HOSTNAME` varchar(64) DEFAULT NULL,
  `NETCARDNUMBER` varchar(512) DEFAULT NULL,
  `COLLECTSTATUS` varchar(64) DEFAULT NULL,
  `SYSTEMADMIN` varchar(64) DEFAULT NULL,
  `VMWARE` varchar(64) DEFAULT NULL,
  `PHYSICIP` varchar(64) DEFAULT NULL,
  `APPROLEGROUP` varchar(64) DEFAULT NULL,
  `AGENTID` varchar(64) DEFAULT NULL,
  `PARNUMBER` varchar(64) DEFAULT NULL,
  `SERIALNUMBER` varchar(64) DEFAULT NULL,
  `SYSTEM_DIGIT` varchar(64) DEFAULT NULL,
  `CPU_NUMBER` varchar(64) DEFAULT NULL,
  `PARNAME` varchar(64) DEFAULT NULL,
  `APPLICATIONTYPE` varchar(128) DEFAULT NULL,
  `SYSCODE` varchar(64) DEFAULT NULL,
  `PHYSICALSEARCHCODE` varchar(64) DEFAULT NULL,
  `VPARNUMBER` varchar(64) DEFAULT NULL,
  `VMHOST` varchar(64) DEFAULT NULL,
  `IP` varchar(256) DEFAULT NULL,
  `MASTERORBACKUP` varchar(64) DEFAULT NULL,
  `DISASTERTYPE` varchar(128) DEFAULT NULL,
  `SYSTEMVERSION` varchar(128) DEFAULT NULL,
  `APPFULLNAME` varchar(64) DEFAULT NULL,
  `MEMORY` varchar(64) DEFAULT NULL,
  `PARSTATUS` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CMDB_ORACLESID_RAW` (
  `WRITE_TIME` datetime NOT NULL,
  `HOSTNAME` varchar(64) DEFAULT NULL,
  `AGENTID` varchar(64) DEFAULT NULL,
  `USETYPE` varchar(64) DEFAULT NULL,
  `VERSION` varchar(64) DEFAULT NULL,
  `SID` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CMDB_TUXEDO_RAW` (
  `WRITE_TIME` datetime NOT NULL,
  `HOSTNAME` varchar(64) DEFAULT NULL,
  `AGENTID` varchar(128) DEFAULT NULL,
  `USETYPE` varchar(64) DEFAULT NULL,
  `VERSION` varchar(128) DEFAULT NULL,
  `SYSNAME` varchar(64) DEFAULT NULL,
  `SYSCODE` varchar(64) DEFAULT NULL,
  `TUXEDOUSER` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CMDB_WEBLOGIC_DOMAIN_RAW` (
  `WRITE_TIME` datetime NOT NULL,
  `ADMINSERVERIP` varchar(64) DEFAULT NULL,
  `HOSTNAME` varchar(64) DEFAULT NULL,
  `AGENTID` varchar(64) DEFAULT NULL,
  `USETYPE` varchar(64) DEFAULT NULL,
  `PRODUCTIONMODE` varchar(64) DEFAULT NULL,
  `WEBLOGIC_VERSION` varchar(128) DEFAULT NULL,
  `DOMAIN_NAME` varchar(64) DEFAULT NULL,
  `DOMAIN_PATH` varchar(256) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CMDB_WEBLOGIC_RAW` (
  `WRITE_TIME` datetime NOT NULL,
  `ADMINSERVERIP` varchar(64) DEFAULT NULL,
  `HOST` varchar(64) DEFAULT NULL,
  `AGENTID` varchar(128) DEFAULT NULL,
  `USETYPE` varchar(64) DEFAULT NULL,
  `VERSION` varchar(128) DEFAULT NULL,
  `LISTENADDRESS` varchar(128) DEFAULT NULL,
  `CN_NAME` varchar(64) DEFAULT NULL,
  `SHORT_NAME` varchar(64) DEFAULT NULL,
  `SNAME` varchar(64) DEFAULT NULL,
  `DNAME` varchar(64) DEFAULT NULL,
  `LISTENPORT` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CMDB_IPTOAPP` (
  `WRITE_TIME` datetime NOT NULL,
  `IP_ADDRESS` varchar(64) DEFAULT NULL,
  `IP_TYPE` varchar(64) DEFAULT NULL,
  `IP_SOURCE` varchar(64) DEFAULT NULL,
  `APP_CODE` varchar(64) DEFAULT NULL,
  `APP_NAME` varchar(64) DEFAULT NULL,
  `USETYPE` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `UMP_MO_OS` (
  `WRITE_TIME` datetime NOT NULL,
  `KEYWORD` varchar(128) DEFAULT NULL,
  `IP_ADDRESS` varchar(64) DEFAULT NULL,
  `AGENTID` varchar(128) DEFAULT NULL,
  `APP_CODE` varchar(64) DEFAULT NULL,
  `APP_NAME` varchar(64) DEFAULT NULL,
  `USETYPE` varchar(64) DEFAULT NULL,
  `HOSTNAME` varchar(64) DEFAULT NULL,
  `OS_TYPE` varchar(64) DEFAULT NULL,
  `VERSION` varchar(128) DEFAULT NULL,
  `IP_ALL` varchar(256) DEFAULT NULL,
  `VIP` varchar(256) DEFAULT NULL,
  `MAPPINGIP` varchar(64) DEFAULT NULL,
  `VOLUME_TYPE` varchar(32) DEFAULT NULL,
  `APPLICATIONTYPE` varchar(128) DEFAULT NULL,
  `DISASTERTYPE` varchar(128) DEFAULT NULL,
  `IS_ORACLE` tinyint(1) DEFAULT NULL,
  `IS_WEBLOGIC` tinyint(1) DEFAULT NULL,
  `IS_ASM` tinyint(1) DEFAULT NULL,
  `IS_TUXEDO` tinyint(1) DEFAULT NULL,
  `IS_VCS` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CMDB_IP_RELATION` (
  `WRITE_TIME` datetime NOT NULL,
  `VIP` varchar(64) DEFAULT NULL,
  `MAPPINGIP` varchar(64) DEFAULT NULL,
  `PHYSICIP` varchar(64) DEFAULT NULL,
  `APP_CODE` varchar(64) DEFAULT NULL,
  `APP_NAME` varchar(64) DEFAULT NULL,
  `AGENTID` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





