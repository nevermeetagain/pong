# -*- coding: utf-8 -*-
import configparser


class system_file():

    # 读取配置文件
    @staticmethod
    def get_config(sections, options, configpath="./config.ini"):
        try:
            config = configparser.ConfigParser()
            config.read(configpath, encoding='utf-8')
            return config.get(sections, options)
        except Exception as e:
            return False

    # 修改配置文件
    @staticmethod
    def post_config(sections, options, value, configpath="./config.ini"):
        config = configparser.ConfigParser()
        config.read(configpath, encoding='utf-8')
        config.set(sections, options, value)
        config.write(open(configpath, "w+", encoding="utf-8"))
        return value