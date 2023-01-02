from .config_reader import Config
from dbutils.pooled_db import PooledDB
import pymysql


class Singleton(object):
    __connection_handler = None
    __cyrene_connection_handler = None

    @classmethod
    def get_mysql_connection(cls):
        try:
            if cls.__connection_handler is None:
                db_name = "adam"
                obj_config = Config()
                connection = "mysql_connection"
                env = "Staging"
                mysql_details = obj_config.get_key_value(connection)[env]
                host = mysql_details['host']
                port = mysql_details['port']
                user = mysql_details['user']
                password = mysql_details['password']
                print(mysql_details)
                # connection_object = pymysql.connect(host=host, port=port, user=user, password=password,
                #                                     cursorclass=pymysql.cursors.DictCursor,
                #                                     db=db_name, autocommit=True)
                connection_object = PooledDB(creator=pymysql, host=host, port=port, user=user, password=password,
                                             cursorclass=pymysql.cursors.DictCursor,
                                             db=db_name, autocommit=True)
                cls.__connection_handler = connection_object.connection()
            return cls.__connection_handler
        except Exception:
            raise

    @classmethod
    def terminate_connection(cls):
        # if cls.__connection_handler is not None:
        #     cls.__connection_handler.close()
        cls.__connection_handler = None


class MySqlDB(object):

    @staticmethod
    def get_connection():
        connection = Singleton.get_mysql_connection()
        return connection

    @staticmethod
    def terminate_connection():
        Singleton.terminate_connection()

    def sql_query_string(self, sql_command):
        try:
            connection_obj = self.get_connection()
            cursor_obj = connection_obj.cursor()
            cursor_obj.execute(sql_command)
            result = cursor_obj.fetchall()
            cursor_obj.close()
            connection_obj.close()
            return result
        except Exception:
            raise
