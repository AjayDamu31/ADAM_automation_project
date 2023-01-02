import json
import os


class Config(object):
    __path = "properties/config.json"
    json_file = None

    @classmethod
    def get_key_value(cls, key):
        """
        Used to access the config.json file with Key name.
        :param key: Key name that which is required.
        :return: Value of the key from the config.json
        """
        with open(cls.__path) as f:
            my_json = json.load(f)
            return my_json.get(key)


if __name__ == '__main__':
    obj = Config()
    url = obj.get_key_value("login")
    print(url)
#     # if url is not "":
#     #     print("ssss")
#     print(obj.get_env())
