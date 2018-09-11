celery主要的配置点:
1.在项目(project)目录下创建celery.py并在该模块中实例化一个celery的对象,至于celery的配置问题,可以在django的settings中配置,注意需要一个
命名空间,详细请看settings
2.settings模块中,按照实例化配置文件的namespace进行命名,配置的变量需要全部大写,之间用下划线_隔开
3.在项目(project)目录下需要将__init__.py文件进行更改初始化,一开始加载文件就需要将celery的实例化对象告诉解释器
这样就可以直接指定包名不用指定模块名了
celery -A 包名  worker -l info -P eventlet:这句话的意思是 celery的实例化对象在一个包中(__init__.py)会告诉他具体的位置,然后启动celery
4.tasks.py可以放在自己创建的应用(app)中,通过导入的方式进行目标函数的操作,从而实现异步和定时两个功能