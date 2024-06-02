# -*- coding: utf-8 -*-


import os
import time
import traceback
from loguru import logger
from datetime import datetime

from model.system_file import system_file as sysfile


class system_log():

    @staticmethod
    def demo_log():
        log_name = datetime.now().strftime("%Y-%m-%d")
        sink = os.path.join(sysfile.get_config("SYSTEM", "path_logs"), "{}.log".format(log_name))
        level = "DEBUG"
        encoding = "utf-8"
        enqueue = True
        rotation = "500MB"
        retention = "1 week"
        logger.add(
            sink=sink, level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <white>{message}</white>",
            encoding=encoding, enqueue=enqueue,
            rotation=rotation, retention=retention,
        )
        # logger.bind(label="").info()
        return logger

    @staticmethod
    def wrapper_log(func):
        log = system_log.demo_log()
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                # log.critical(traceback.format_exc())
                log.exception(e)
            finally:
                pass
        return wrapper

    @staticmethod
    def retry_wrapper(func, params={}, act_name='', sleep_seconds=3, retry_times=5):
        for _ in range(retry_times):
            try:
                if 'timestamp' in list(params.keys()):
                    params['timestamp'] = int(time.time()) * 1000
                result = func(params=params)
                return result
            except Exception as e:
                print(act_name, '错误:', str(e), '\n等待再次重试')
                print(traceback.format_exc())
                time.sleep(sleep_seconds)
        else:
            raise ValueError(act_name, '重试失败')

