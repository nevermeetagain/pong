# -*- coding: utf-8 -*-
import threading
from temp import collisions_eth_by_mnemonic


def simple_test():
    rpc = {
        "eth_rpc": ["https://eth.public-rpc.com"],
        "bsc_rpc": ["https://bscrpc.com"],
        "arb_rpc": ["https://arbitrum.public-rpc.com"],
        "op_rpc": ["https://optimism-mainnet.core.chainstack.com/b5f834546042e096d5941131a72726fe"],
        "poly_rpc": ["https://polygon-rpc.com"],
        "avax_rpc": ["https://avalanche.public-rpc.com"],
        "scroll_rpc": ["https://arbitrum.public-rpc.com"],
    }
    while True:
        private_key, public_key, address = collisions_eth_by_mnemonic.get_account()
        print(private_key, public_key, address)
        collisions_eth_by_mnemonic.check_eth_balance_byprivate(private_key=private_key)
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, chain_rpc=rpc["bsc_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, chain_rpc=rpc["arb_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, chain_rpc=rpc["op_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, chain_rpc=rpc["poly_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, chain_rpc=rpc["avax_rpc"][0])
        collisions_eth_by_mnemonic.check_other_balance_byaddress(wallet_address=address, chain_rpc=rpc["scroll_rpc"][0])


if __name__ == '__main__':
    thread_num = int(input("请输入线程数:"))
    list_thread = []
    for i in range(thread_num):
        list_thread.append(threading.Thread(target=simple_test))
    for j in list_thread:
        j.start()
        j.join()
