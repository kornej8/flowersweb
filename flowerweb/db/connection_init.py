class ConnectionInit:

    __connection_keyword = 'database'

    def __init__(self, config: dict):
        self.url = ConnectionInit.get_url(config, by=self.__connection_keyword)

    @staticmethod
    def build_addr(host, port):
        if port:
            return f"{host}:{port}"
        return host

    @staticmethod
    def get_url(config, by, db='postgresql'):

        config_by=config.get(by, {})
        user = config_by.get('user')
        host = config_by.get('host')
        port = config_by.get('port')
        password = config_by.get('password')
        db_name = config_by.get('db_name')


        addr = ConnectionInit.build_addr(host, port)

        url_string = "{db}://{user}:{password}@{addr}/{db_name}".format(
            db=db,
            user=user,
            addr=addr,
            password=password,
            db_name=db_name
        )

        print(url_string)

        return url_string
