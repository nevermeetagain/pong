# -*- coding: utf-8 -*-
import threading
import multiprocessing
from temp import collisions_eth_by_mnemonic


def simple_test():
    rpc = {
        "eth_rpc": ["https://api.zan.top/node/v1/eth/mainnet/36e2af2368f24c71b74241773c604f21"],
        "bsc_rpc": ["https://api.zan.top/node/v1/bsc/mainnet/36e2af2368f24c71b74241773c604f21"],
        "tron_rpc": ["https://api.zan.top/node/v1/tron/mainnet/36e2af2368f24c71b74241773c604f21/jsonrpc"],
    }
    while True:
        private_key, public_key, address = collisions_eth_by_mnemonic.get_account()
        print(private_key, public_key, address)
        collisions_eth_by_mnemonic.check_eth_balance_byprivate(private_key=private_key, eth_rpc=rpc["eth_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, chain_rpc=rpc["bsc_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, chain_rpc=rpc["tron_rpc"][0])


if __name__ == '__main__':
    # thread_num = int(input("请输入进程数:"))
    # list_thread = []
    # for i in range(thread_num):
    #     list_thread.append(threading.Thread(target=simple_test))
    # for j in list_thread:
    #     j.start()
    #     j.join()

    cores = int(input("请输入执行进程数:"))
    for i in range(cores):
        p = multiprocessing.Process(target=simple_test)
        p.start()
