# -*- coding: utf-8 -*-
import threading
import random
import multiprocessing
from temp import collisions_eth_by_mnemonic


def simple_test():
    rpc = {
        "eth_rpc": ["https://eth.public-rpc.com", "https://ethereum-mainnet.core.chainstack.com/05865e71f7003c5aee9c1a00d896e4f6"],
    }
    while True:
        rint = int(random.randint(0, 1))
        private_key, public_key, address = collisions_eth_by_mnemonic.get_account()
        print(private_key, public_key, address)
        collisions_eth_by_mnemonic.check_eth_balance_byprivate(wallet_address=address, private_key=private_key, chain_rpc=rpc["eth_rpc"][rint])


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
