class ConnectionInit:

    __connection_keyword = 'database'

    def __init__(self, config: dict):
        self.url = ConnectionInit.get_url(config, by=self.__connection_keyword)

    @staticmethod
    def get_url(config, by, db='postgresql'):

        config_by=config.get(by, {})

        print(config_by)

        user = config_by.get('user')

        host = config_by.get('host')
        print(config_by)
        port = config_by.get('port')
        password = config_by.get('password')
        db_name = config_by.get('db_name')

        url_string = "{db}://{user}:{password}@{host}:{port}/{db_name}".format(
            db=db,
            user=user,
            host=host,
            port=port,
            password=password,
            db_name=db_name
        )
        print(url_string)
        return url_string
