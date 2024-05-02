from pytonconnect import TonConnect
from config_reader import config
from db.tc_connect import TcStorage


def get_connector(chat_id: int):
    return TonConnect('tonconnect-manifest.json', storage=TcStorage(chat_id))
