# -*- coding: utf-8 -*-

import requests
from model.system_proxy import system_proxy as sys_proxy

def cex_zeta():
    url = "https://dex-funding-rate-mainnet.zeta.markets/avgfunding"
    proxy = sys_proxy.get_default_proxy()
    rep = requests.get(url, proxies=proxy)
    print(rep.text)

