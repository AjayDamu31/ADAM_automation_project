import pytest
from main import Config
from main import CoreAPIUtils, URLConstant, AllureReport, MySqlDB
import logging


@pytest.fixture(scope="class")
def api_setup(request):
    print("setup")
    request.cls.config = Config
    request.cls.logger = logging.getLogger()
    request.cls.url_util = URLConstant()
    request.cls.api_utils = CoreAPIUtils(request.cls.logger)
    request.cls.allure_url = AllureReport(None)
    request.cls.mysql_obj = MySqlDB()
    yield
    print("test close")
