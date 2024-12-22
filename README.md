# 航味
## 环境配置
mysql安装参考 https://blog.csdn.net/weixin_42868605/article/details/119821028  
navicat安装参考 https://www.bilibili.com/read/cv34556397/

## 初始化项目
新建mysql数据库的连接。将 `/myweb/settings.py` 中 `DATABASES` 的 `NAME` `USER` `PASSWORD` 等字段改为新建连接时的对应内容

执行 `python manage.py import_cuisines static\cuisine` 以初始化菜品  
执行 `python manage.py import_categories static` 以初始化帖子的标签

每当有 `models.py` 发生改变时，均需执行以下两条命令，重新配置数据库
`python manage.py makemigrations` `python manage.py migrate`

## 运行
**以管理员身份运行**命令提示符，输入 `net start mysql` 启动mysql  
在 `manage.py` 同级的文件夹中执行 `python manage.py runserver` ，即可成功运行项目

使用 `Ctrl + C` 或关闭终端以结束运行  
**以管理员身份运行**命令提示符，输入 `net stop mysql` 停止mysql
