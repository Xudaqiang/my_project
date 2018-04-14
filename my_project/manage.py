
#要利用ORM 就必须引入SQLAlchemy创建的db对象，这个db对象在程序中创建，我们如何在Python命令行中使用呢？答案就是使用Python script。
#Python script 中的Manager模块可以让我们以命令行的形式运行程序，然后得到程序中SQLAlchemy创建的db对象。
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#因为Manager初始化需要用到我们的app，所以导入app
from my_project import app

#做个初始化
manager = Manager(app)


from exts import db
#使用Migrate绑定app和db
migrate = Migrate(app, db)

#添加迁移脚本的命令道manager中
manager.add_command('db', MigrateCommand)


#把设计好的用户模型映射到数据库的表当中，所以把需要映射到的模型导入进来
from models import User,Question
#这样MigrateCommand就回去读取当前你导入进来的这个模型，这样我们来到终端进入当前项目，记住是从虚拟环境cd进入当前项目。
#然后python manage.py db init 来初始化当前项目的一个迁移环境，可以看到项目下多了一个migrations文件。
#接下来就是把这个模型映射到数据库中，在之前，还要做一个迁移文件python manage.py db migrate(这里我忘了在虚拟环境pip了个啥，自行百度吧。)
#执行上一步后再migrations的versions下面多了个一连串数字的文件。接下来就需要执行这个文件，使真正的映射到数据库当中。python manage.py db upgrade

# import MySQLdb
import pymysql
pymysql.install_as_MySQLdb()





if __name__ == "__main__":
    manager.run()