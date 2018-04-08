1. 导入mysql镜像
2. 启动mysql容器，创建库、用户和表
3. 导入python3env 镜像
4. 拷贝文件
	#/opt/itump/easyump/itmapp
	拷贝项目文件到该目录 : bin/  logs/   conf/   src/
5. 启动python3env 容器



1.导入mysql镜像
	

2.启动mysql容器，创建库、用户和表
   docker run --name easyump-mysql -v /opt/mysql_data:/var/lib/mysql -p 3333:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

3.导入python3env 镜像
  #docker load -i python3env.tar

4.拷贝文件
	#/opt/itump/easyump/itmapp
	拷贝项目文件到该目录 : bin/  logs/   conf/   src/
  
5.启动python3env 容器
	#docker run --name itmapp -v /opt/itump/easyump/itmapp:/opt/itump/easyump/itmapp -v /usr/share/zoneinfo/Asia/Beijing:/etc/localtime easyump/python3env python3 /opt/itump/easyump/itmapp/bin/run_all.py 

6.检查结果，logs/process.log的末尾，出现类似的日志
	2018-04-06 10:22:26,975 - sub_common - INFO - Begin to insert to table:ITM_POLICY.
	2018-04-06 10:27:06,188 - sub_common - INFO - Success insert records:117333.
	2018-04-06 10:27:11,266 - sub_common - INFO - Begin to insert to table:UMP_DOC
	2018-04-06 10:27:11,270 - sub_common - INFO - Table UMP_DOC has been cleaned!
	2018-04-06 10:28:19,402 - sub_common - INFO - Success insert records:108584.

	

pip知识：
列出已安装的包： pip list
导出pip包信息：  pip freeze > requestments.txt
只下载不安装（需手工创建pgk目录）：   pip install -d pgk/ -r requestments.txt
本地安装包：     pip install 文件名

yum知识：
下载缓存配置： /etc/yum.conf ,  keepcache=1
缓存目录：     /var/cache/yum/


 