docker run --name easyump-mysql -v /mysql_data:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci


创建模式
CREATE SCHEMA `ump` DEFAULT CHARACTER SET utf8 ;




