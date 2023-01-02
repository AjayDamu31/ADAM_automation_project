import requests
import json
from .config_reader import Config
from .exception_utils import ExceptionUtils
from .url_constants import URLConstant


class CoreAPIUtils(object):
    __log = None
    exception_util = None
    config = None

    def __init__(self, log):
        self.__log = log
        self.exception_util = ExceptionUtils(log)
        self.config = Config()
        self.api_util = URLConstant()

    def get_api_token(self):
        """
        Method to return api token for authentication.
        :param api_key: Api key required for token generation.
        :return: return the api token if the api status is 200.
        """
        self.__log.debug("CoreAPIUtils.get_api_token(self, api_key):")
        try:
            username = self.config.get_key_value('login')['email']
            password = self.config.get_key_value('login')['password']

            json_post_data = json.dumps({
                "email": username,
                "password": password
            })
            url = self.api_util.get_url(self.api_util.AUTH_LOGIN)
            response = self.post_api_request(url, json_post_data)
            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))['token']
            return response.status_code
        except Exception as exc:
            self.exception_util.generic_exception("Error occurred while waiting for token", exc)
            raise

    def post_api_request(self, url, api_data):
        """
        Method for POST api request.
        :param url: URL for POST request.
        :param api_data: API data that is required to POST
        :return: Returns the response from the POST request.
        """
        self.__log.debug(
            "CoreAPIUtils.post_api_request(self, url, api_data):" + "url:" + url + "api_data : " + api_data)
        try:
            head = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            response = requests.post(url=url, data=api_data, headers=head)
            return response
        except Exception as exc:
            self.exception_util.generic_exception("Error occurred during api post ", exc)
            raise

    def post_api_request_with_token(self, url, api_data, token):
        """
        Method to perform POST request with token authentication.
        :param url: URL for POST request.
        :param api_data: API data that is required to POST.
        :param token: Token for authentication.
        :return: Returns the response from the POST request.
        """
        self.__log.debug(
            "CoreAPIUtils.post_api_request_with_token(self, url, api_data,token):" + "url:" + url + "api_data : " + api_data + "token" + token)
        try:
            head = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(token)}
            response = requests.post(url=url, data=api_data, headers=head)
            return response
        except Exception as exc:
            self.exception_util.generic_exception("Error occurred during api post ", exc)
            raise

    def get_api_request(self, url, token, param=None):
        """
        Method to perform GET request.
        :param url: URL for GET request.
        :param token: Token for authentication.
        :return:  Returns the response of GET request.
        """
        self.__log.debug(
            "CoreAPIUtils.get_api_request(self, url, token):" + "url:" + url + "token : " + token)
        try:
            head = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(token)}
            if param is None:
                response = requests.get(url, headers=head)
                return response
            elif param is not None:
                response = requests.get(url, headers=head, params=param)
                return response
        except Exception as exc:
            self.exception_util.generic_exception("Error occurred during api get", exc)
            raise

    def put_api_request(self, url, api_data, token):
        """
        Method to perform PUT request.
        :param url: URL for PUT request.
        :param api_data: API data that is required to PUT request.
        :param token: Token for authentication.
        :return: Returns the response from the PUT request.
        """
        self.__log.debug(
            "CoreAPIUtils.put_api_request(self, url, api_data):" + "url:" + url + "api_data : " + api_data)
        try:
            head = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(token)}
            response = requests.put(url=url, data=api_data, headers=head)
            return response
        except Exception as exc:
            self.exception_util.generic_exception("Error occurred during api put ", exc)
            raise

    def delete_api_request(self, url, api_data, token):
        """
        Method to perform DELETE request.
        :param url: URL for DELETE request.
        :param api_data: API data that is required to DELETE request.
        :param token: Token for authentication.
        :return: Returns the response from the DELETE request.
        """
        self.__log.debug(
            "CoreAPIUtils.delete_api_request(self, url, api_data):" + "url:" + url)
        try:
            head = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + str(token)}
            response = requests.delete(url=url, headers=head, data=api_data)
            return response
        except Exception as exc:
            self.exception_util.generic_exception("Error occurred during api put ", exc)
            raise


if __name__ == '__main__':
    obj = CoreAPIUtils(None)
    import logging

    token = (obj.get_api_token(logging))
    print(token)
#     # url1 = "https://api.shieldsquare.com/v1/sites/7747/bad-bot/geo-bot-distribution/?starttime=1553601600445&endtime=1554202800451&sids=7747"
#     # print(obj.get_api_request(url1, token).content.decode('utf-8'))
