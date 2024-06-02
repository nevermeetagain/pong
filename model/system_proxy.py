# -*- coding: utf-8 -*-


import requests
from model.system_file import system_file as sys_file


class system_proxy():

    @staticmethod
    def get_proxy(protocol="http", ip="", port="", username="", password=""):
        if protocol.lower() == "http":
            if not username and not password:
                proxy = "http://%(ip)s:%(port)s" % {
                    "ip": ip,
                    "port": port,
                }
            else:
                proxy = "http://%(username)s:%(password)s@%(ip)s:%(port)s" % {
                    "username": username,
                    "password": password,
                    "ip": ip,
                    "port": port,
                }
            proxies = {
                "http": proxy,
                "https": proxy,
            }
        elif protocol.upper() == "socks5":
            if not username and not password:
                proxy = "http://%(ip)s:%(port)s" % {
                    "ip": ip,
                    "port": port,
                }
            else:
                proxy = "socks5://%(username)s:%(password)s@%(ip)s:%(port)s" % {
                    "username": username,
                    "password": password,
                    "ip": ip,
                    "port": port,
                }
            proxies = {
                "http": proxy,
                "https": proxy,
            }
        else:
            proxies = {}
        return proxies

    @staticmethod
    def demo_proxy(url, protocol, ip, port, username, password):
        proxies = system_proxy.get_proxy(protocol, ip, port, username, password)
        rep = requests.get(url, proxies=proxies)
        # rep.encoding = 'utf-8'
        # print(rep.status_code)  # 返回状态值
        # print(rep.text)  # 返回html
        # return rep.json()
        return rep

    @staticmethod
    def get_default_proxy():
        proxies = system_proxy.get_proxy(
            sys_file.get_config("DEFAULT", "default_proxy_protocol"),
            sys_file.get_config("DEFAULT", "default_proxy_host"),
            sys_file.get_config("DEFAULT", "default_proxy_port"),
            sys_file.get_config("DEFAULT", "default_proxy_username"),
            sys_file.get_config("DEFAULT", "default_proxy_password")
        )
        return proxies
