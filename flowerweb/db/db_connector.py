from sqlalchemy import create_engine
from flowerweb.db.connection_init import ConnectionInit
from flowerweb.config.init_config import Config


class InitDBConnect:
    @classmethod
    def init(cls):
        cfg = Config().get()
        return create_engine(ConnectionInit(cfg).url)

class DBConnect(InitDBConnect):
    def __new__(cls):
        return super().init()

