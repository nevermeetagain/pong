# -*- coding: utf-8 -*-
# 私钥碰撞器
import random, time
import json
import traceback
from web3 import Web3
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import threading


def send_email(msg: str, recever="164093410@qq.com"):
    message = MIMEText(msg, _subtype='plain', _charset='utf-8')
    message['From'] = "buchang_123@163.com"
    message['To'] = f"<591547726@qq.com>"
    message['Subject'] = Header(f'验证消息-XeggeX', 'utf-8')
    smtper = smtplib.SMTP_SSL("smtp.163.com", 465)
    smtper.login("buchang_123@163.com", "PMFHEFUVASHUISBQ")
    smtper.sendmail("buchang_123@163.com", recever, message.as_string())


def retry_wrapper(func, params={}, act_name='', sleep_seconds=3, retry_times=5):
    for _ in range(retry_times):
        try:
            if 'timestamp' in list(params.keys()):
                params['timestamp'] = int(time.time()) * 1000
            result = func(params=params)
            return result
        except Exception as e:
            time.sleep(sleep_seconds)
    else:
        send_email(msg="连续重试失败")
        raise ValueError(act_name, '重试失败')


def check_eth_balance_byprivate(private_key):
    try:
        web3 = Web3(Web3.HTTPProvider('https://eth.public-rpc.com'))
        wallet_account = web3.eth.account.from_key(private_key)
        wallet_address = Web3.to_checksum_address(wallet_account.address)
        eth_balance = web3.from_wei(
            web3.eth.get_balance(Web3.to_checksum_address(wallet_address)), "ether"
        )
        eth_usdt_contract = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        contract_source_code = '''    [{
            "type":"function",
            "name":"balanceOf",
            "constant":true,
            "payable":false,
            "inputs":[{"name":"","type":"address"}],
            "outputs":[{"name":"","type":"uint256","value":"0"}]
            }]
        '''
        abi = json.loads(contract_source_code)
        source_code = web3.eth.get_code(eth_usdt_contract)
        contract = web3.eth.contract(abi=abi, address=eth_usdt_contract, bytecode=source_code)
        usdt_balance = contract.functions.balanceOf(wallet_address).call()
        print(private_key, "\t", eth_balance, "\t",usdt_balance)
        if eth_balance > 0 or usdt_balance > 0:
            msg = "\n私钥:" + str(private_key) + "\n地址:" + str(wallet_address) + "\nETH余额:" + str(eth_balance) + "\nUSDT余额:" + str(usdt_balance)
            send_email(msg)
        return True
    except Exception as e:
        return False


def check_btc_balance_byprivate(private_key):
    pass


def simple_test():
    while True:
        private_key = hex(random.getrandbits(256))[2:].zfill(64)
        check_eth_balance_byprivate(private_key)
        # check_btc_balance_byprivate(private_key)
        time.sleep(1)



thread_num = 10
list_thread = []
for i in range(thread_num):
    list_thread.append(threading.Thread(target=simple_test))
for j in list_thread:
    j.start()
    j.join()






