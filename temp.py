# -*- coding: utf-8 -*-
import threading
import multiprocessing
from temp import collisions_eth_by_mnemonic


def simple_test():
    rpc = {
        "eth_rpc": ["https://eth.public-rpc.com"],
        "bsc_rpc": ["https://bscrpc.com"],
        "arb_rpc": ["https://arbitrum.public-rpc.com"],
        "op_rpc": ["https://optimism-mainnet.core.chainstack.com/8d22e50db5b108fa87cfdff6d0a65dc8"],
        "poly_rpc": ["https://polygon-rpc.com"],
        "avax_rpc": ["https://avalanche.public-rpc.com"],
    }
    while True:
        private_key, public_key, address = collisions_eth_by_mnemonic.get_account()
        print(private_key, public_key, address)
        collisions_eth_by_mnemonic.check_eth_balance_byprivate(wallet_address=address, private_key=private_key, chain_rpc=rpc["eth_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, private_key=private_key, chain_rpc=rpc["bsc_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, private_key=private_key, chain_rpc=rpc["arb_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, private_key=private_key, chain_rpc=rpc["op_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, private_key=private_key, chain_rpc=rpc["poly_rpc"][0])


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
