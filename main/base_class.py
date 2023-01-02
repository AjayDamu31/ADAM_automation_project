import pytest


@pytest.mark.usefixtures('api_setup')
class BaseClass(object):
    api_utils = None
    config = None
    logger = None
    url_util = None
    allure_url = None
    mysql_obj = None

    tok = None

    def get_token(self):
        tok = self.api_utils.get_api_token()
        print(tok)
        self.allure_url.allure_attach_with_text("Token Received", str(tok))
        return tok
