celery主要的配置点:

1.在项目(project)目录下创建celery.py并在该模块中实例化一个celery的对象,至于celery的配置问题,可以在django的settings中配置,注意需要一个
命名空间,详细请看settings

2.settings模块中,按照实例化配置文件的namespace进行命名,配置的变量需要全部大写,之间用下划线_隔开

3.在项目(project)目录下需要将__init__.py文件进行更改初始化,一开始加载文件就需要将celery的实例化对象告诉解释器
这样就可以直接指定包名不用指定模块名了
celery -A 包名  worker -l info -P eventlet:这句话的意思是 celery的实例化对象在一个包中(__init__.py)会告诉他具体的位置,然后启动celery

4.tasks.py可以放在自己创建的应用(app)中,通过导入的方式进行目标函数的操作,从而实现异步和定时两个功能

5.增加的不同任务使用不同的队列功能,代码在celery.py模块

6.增加异步任务定义需要设置其他参数的设置方式,代码在celery.py模块中





关于日志打印的的问题
1.日志配置的相关代码在settings.py中

2.日志存放的位置在djlog中

3.需要打印日志的位置目前将其定义在view.py,模块中,以后可以随着需要挪动

4.在setting.py中定义的logger中的infosyn.youzanapp(logger)这个意思就是,如果我在引入logger的时候直接(__name__),django会自动去找相应处理的logger,如果找不到会自动去上一级去寻找
infosyn.youzanapp的意思就是在这个包范围内的所有处理函数,都可以自动寻找到该logger进行处理.

5.logger = logging.getLogger(__name__)这个实例化的logger 在启动时会去寻找符合当前模块的层级关系的logger也就是在settings.py中定义的infosyn.youzanapp,所有符合这个层级关系的处理函数都可以使用该模块
