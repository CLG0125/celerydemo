from django.shortcuts import render

# Create your views here.


# 在相应需要记录日志的函数模块中引入log,并写入函数中
import logging

logger = logging.getLogger(__name__)


def name_test():
    try:
        2 / 0
    except Exception as e:
        logger.info(e)


name_test()
