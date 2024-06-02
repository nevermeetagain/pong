# -*- coding: utf-8 -*-


import pandas as pd
from web3 import Web3
from datetime import datetime
from model.system_file import system_file as sys_file


class chain_evm():

    @staticmethod
    def create_wallet():
        w3 = Web3()
        account = w3.eth.account.create()
        address = account._address
        private = str(account._private_key.hex())[2:]
        return {"address": address, "private": private}

    @staticmethod
    def create_wallet_tocsv(create_amount=100, create_label="", task_name=sys_file.get_config("TASK", "task_name")):
        pass


