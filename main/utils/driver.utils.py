from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .exception_utils import ExceptionUtils
from .config_reader import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class DriverCore(object):
    """
    Utils class for all driver related process.
    """
    __driver = None
    __allure_report = None
    log = None
    exception_util = None

    def __init__(self, driver, logger):
        """
        :param driver: Driver instance
        :param logger: Logger instance
        """
        self.__driver = driver
        self.log = logger
        self.__timeout = (Config().get_timeout())
        self.exception_util = ExceptionUtils(logger)

    @classmethod
    def get_allure_instance(cls):
        return cls.__allure_report

    @classmethod
    def set_allure_obj(cls, obj):
        cls.__allure_report = obj

    def get_driver(self):
        return self.__driver

    def go_to_url(self, url):
        """
        This method will go to  the provided url.

        :param
        url: browser will navigate to the provided url
        """
        self.log.debug("DriverCore.go_to_url(self, url): " + url)
        try:

            self.__driver.get(url)
            self.__driver.maximize_window()
        except Exception as exc:
            self.exception_util.generic_exception("Unable to navigate to url: " + url, exc)
            raise

    def orientation_to_landscape(self):
        self.log.debug("DriverCore.orientation_to_landscape(self), Device rotated to landscape")
        try:
            self.__driver.orientation = "LANDSCAPE"
        except Exception as exc:
            self.exception_util.generic_exception("Unable to change the orientation to LANDSCAPE", exc)
            raise

    def orientation_to_portrait(self):
        self.log.debug("DriverCore.orientation_to_portrait(self), Device rotated to portrait")
        try:
            self.__driver.orientation = "PORTRAIT"
        except Exception as exc:
            self.exception_util.generic_exception("Unable to change the orientation to PORTRAIT", exc)
            raise

    def wait_until_angular(self, seconds: int = 10) -> None:
        from datetime import datetime, timedelta
        import time
        from selenium.common.exceptions import WebDriverException
        java_script_to_load_angular = "var injector = window.angular.element('body').injector(); " \
                                      "var $http = injector.get('$http');" \
                                      "return ($http.pendingRequests.length === 0);"
        end_time = datetime.utcnow() + timedelta(seconds=seconds)
        print("wait for Angular Elements....")
        while datetime.utcnow() < end_time:
            try:
                if self.__driver.execute_script(java_script_to_load_angular):
                    return
            except WebDriverException:
                continue
            time.sleep(1)
        raise TimeoutError("waiting for angular elements for too long")

    def wait_for_web_element_to_be_appear(self, locator):
        self.log.debug("DriverCore.wait_for_web_element_to_appear(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.presence_of_element_located((By.XPATH, locator)))
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while waiting for element to appear", exc)
            raise

    def wait_for_web_element_to_be_visible(self, locator):
        self.log.debug("DriverCore.wait_for_web_element_to_visible(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.visibility_of_element_located((By.XPATH, locator)))
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while waiting for element to be visible", exc)
            raise

    def wait_for_web_element_to_be_invisible(self, locator):
        self.log.debug("DriverCore.wait_for_web_element_to_invisible(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.invisibility_of_element_located((By.XPATH, locator)))
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while waiting for element to be invisible", exc)
            raise

    def wait_for_web_element_to_be_clickable(self, locator):
        self.log.debug("DriverCore.wait_for_web_element_to_clickable(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.element_to_be_clickable((By.XPATH, locator)))
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while waiting for element to be clickable", exc)
            raise

    def wait_for_web_element_to_be_selected(self, locator):
        self.log.debug("DriverCore.wait_for_web_element_to_selected(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.element_located_to_be_selected((By.XPATH, locator)))
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while waiting for element to be selected", exc)
            raise

    def wait_for_text_to_be_present_in__element_value(self, locator, text):
        self.log.debug("DriverCore.wait_for_web_element_to_selected(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.text_to_be_present_in_element_value((By.XPATH, locator), text_=text))
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.mismatch_exception(locator + "to appear.", exc,
                                                   self.get_element_text(locator), text)
            raise

    def wait_for_text_to_be_present_in__element(self, locator, text):
        self.log.debug("DriverCore.wait_for_text_to_be_present_in__element(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.text_to_be_present_in_element((By.XPATH, locator), text_=text))
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while waiting for text to be present in the element", exc)
            raise

    def select_drop_down_by_value(self, locator, value):
        self.log.debug("DriverCore.select_drop_down_by_value(self, locator):" + "locator : " +
                       locator + " value : " + value)
        try:
            self.wait_for_web_element_to_be_appear(locator).click()
            select = Select(self.__driver.find_element_by_xpath(locator))
            select.select_by_value(value)
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to select dropdown by value: " + value, exc)
            raise

    def select_drop_down_by_text(self, locator, text):
        self.log.debug("DriverCore.select_drop_down_by_text(self, locator):" + "locator : " +
                       locator + " text : " + text)
        try:
            self.wait_for_web_element_to_be_appear(locator).click()
            select = Select(self.__driver.find_element_by_xpath(locator))
            select.select_by_visible_text(text)
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to select dropdown by text: " + text, exc)
            raise

    def select_drop_down_by_index(self, locator, index):
        self.log.debug("DriverCore.select_drop_down_by_index(self, locator):" + "locator : " +
                       locator + " Index : " + index)
        try:
            self.wait_for_web_element_to_be_appear(locator).click()
            select = Select(self.__driver.find_element_by_xpath(locator))
            select.select_by_index(index)
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except IndexError as exc:
            self.exception_util.index_error(locator, exc, index)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unexpected Error while attempting "
                                                  "to select dropdown " + locator + "at index " + index, exc)
            raise

    def get_selected_drop_down_value(self, locator):
        self.log.debug("DriverCore.get_selected_drop_down_value(self, locator):" + "locator : " +
                       locator)
        try:
            self.wait_for_web_element_to_be_appear(locator)
            select = Select(self.__driver.find_element_by_xpath(locator))
            return select.first_selected_option.text
        except Exception as exc:
            self.exception_util.generic_exception("Unable to get the currently"
                                                  " selected dropdown value from the element" + locator, exc)
            raise

    def get_all_drop_down_values(self, locator):
        self.log.debug("DriverCore.get_selected_drop_down_value(self, locator):" + "locator : " +
                       locator)
        try:
            self.wait_for_web_element_to_be_appear(locator)
            select = Select(self.__driver.find_element_by_xpath(locator))
            return select.all_selected_options()
        except Exception as exc:
            self.exception_util.generic_exception("Unable to get list of all"
                                                  " dropdown value from the locator" + locator, exc)
            raise

    def go_back(self):
        self.log.debug("DriverCore.go_back()")
        try:
            self.__driver.back()
        except Exception as exc:
            self.exception_util.generic_exception("Unable to navigate back in browser", exc)
            raise

    def refresh_page(self):
        self.log.debug("DriverCore.refresh_page()")
        try:
            self.__driver.back()
        except Exception as exc:
            self.exception_util.generic_exception("Unable to refresh page in browser", exc)
            raise

    def get_current_url(self):
        self.log.debug("DriverCore.get_current_url()")
        try:
            return str(self.__driver.current_url)
        except Exception as exc:
            self.exception_util.generic_exception("Unable to refresh page in browser", exc)
            raise

    def wait_for_url_to_be(self, expected_url):
        self.log.debug("DriverCore.wait_for_url_to_be(self, expected_url): expected url : " + expected_url)
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.url_to_be(expected_url))
        except TimeoutException as exc:
            self.exception_util.generic_exception("Timed out waiting for url to be : " + expected_url, exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while waiting for url to be : " + expected_url, exc)
            raise

    def element_is_displayed(self, locator):
        self.log.debug("DriverCore.element_is_displayed(self, locator): locator : " + locator)
        try:
            # self.wait_for_web_element_to_be_appear(locator)
            # self.wait_for_web_element_to_be_visible(locator)
            if self.__driver.find_element_by_xpath(locator).is_displayed():
                return True
        except NoSuchElementException:
            return False
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to locate the element" + locator, exc)
            raise

    def pause(self, time_in_seconds):
        self.log.debug("DriverCore.pause(self, time_in_seconds): time_in_seconds" + str(time_in_seconds))
        try:
            time.sleep(time_in_seconds)
        except InterruptedError as exc:
            self.exception_util.generic_exception("Unable to pause test for : " + str(time_in_seconds), exc)
            raise

    def get_element_text(self, locator):
        self.log.debug("DriverCore.get_element_text(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            self.wait_for_web_element_to_be_appear(locator)
            self.wait_for_web_element_to_be_visible(locator)
            return str(self.__driver.find_element_by_xpath(locator).text)
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to retrieve "
                                                  "text from element:" + locator, exc)
            raise

    def find_element_with_id(self, locator):
        self.log.debug("DriverCore.find_element_with_id(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            ele = self.__driver.find_element_by_id(locator)
            return ele
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to retrieve "
                                                  "text from element:" + locator, exc)
            raise

    def find_elements_with_id(self, locator):
        self.log.debug("DriverCore.find_elements_with_id(self, locator):" + "locator : " +
                       locator + "timeout : " + str(self.__timeout))
        try:
            ele = self.__driver.find_elements_by_id(locator)
            return ele
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to retrieve "
                                                  "text from element:" + locator, exc)
            raise

    def wait_implicit(self, implicit_time):
        self.log.debug("DriverCore.implicit_wait(self, implicit_time):" + "implicit_time : " +
                       str(implicit_time))
        try:
            str(self.__driver.implicitly_wait(implicit_time))
        except Exception as exc:
            self.exception_util.generic_exception("Error during implicit wait time", exc)
            raise

    def clear(self, locator):
        self.log.debug("DriverCore.clear(self, locator): locator :" + locator)
        try:
            self.__driver.find_element_by_xpath(locator).clear()
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to clear contents of element : " + locator, exc)
            raise

    def send_keys(self, locator, key):
        self.log.debug("DriverCore.send_keys(self, locator, key): locator :" + locator + "keys : " + key)
        try:
            self.clear(locator)
            self.wait_for_web_element_to_be_appear(locator)
            self.__driver.find_element_by_xpath(locator).send_keys(key)
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to able to enter " + key + " in the locator " + locator,
                                                  exc)
            raise

    def count_number_of_elements(self, locator):
        self.log.debug("DriverCore.count_number_of_elements(self, locator): locator :" + locator)
        try:
            self.wait_for_web_element_to_be_appear(locator)
            list_element = self.__driver.find_elements_by_xpath(locator)
            return len(list_element)
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to count the number of child elements in locator tree", exc)
            raise

    def get_web_element(self, locator):
        self.log.debug("DriverCore.get_web_element(self, locator): locator :" + locator)
        try:
            self.wait_for_web_element_to_be_appear(locator)
            web_element = self.__driver.find_element_by_xpath(locator)
            return web_element
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to get the web element at the locator", exc)
            raise

    def get_web_elements(self, locator):
        self.log.debug("DriverCore.get_web_elements(self, locator): locator :" + locator)
        try:
            self.wait_for_web_element_to_be_appear(locator)
            web_element = self.__driver.find_elements_by_xpath(locator)
            return web_element
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to get the web elements at the locator", exc)
            raise

    def verify_if_element_present(self, locator):
        self.log.debug("DriverCore.verify_if_element_present(self, locator): locator :" + locator)
        try:
            self.get_web_element(locator)
            return True
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to verify that element is present:", exc)
            raise

    def verify_if_element_visible(self, locator):
        self.log.debug("DriverCore.verify_if_element_visible(self, locator): locator :" + locator)
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            element.until(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to verify that element is visible:", exc)
            raise

    def verify_if_element_not_visible(self, locator):
        self.log.debug("DriverCore.verify_if_element_not_visible(self, locator): locator :" + locator)
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            element.until(EC.invisibility_of_element_located((By.XPATH, locator)))
            return True
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to verify that element is not visible:", exc)
            raise

    def get_element_attribute(self, locator, attribute_name):
        self.log.debug("DriverCore.get_element_attribute(self, locator): locator :" + locator)
        try:
            return self.get_web_element(locator).get_attribute(attribute_name)
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to get the element\'s attribute for", exc)
            raise

    def click_with_wait(self, locator):
        self.log.debug("DriverCore.click_with_wait(self, locator): locator :" + locator)
        try:
            self.wait_for_web_element_to_be_clickable(locator)
            self.__driver.find_element_by_xpath(locator).click()
        except NoSuchElementException as exc:
            self.exception_util.no_such_element_exception(locator + "Element does not exist.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to verify that element is clickable: " + locator,
                                                  exc)
            raise

    def take_screenshot(self):
        self.log.debug("DriverCore.take_screenshot(self)")
        try:
            return self.__driver.get_screenshot_as_png()
        except Exception as exc:
            self.exception_util.generic_exception("Unable to take a screenshot", exc)
            raise

    def get_browser_name(self):
        self.log.debug("DriverCore.get_browser_name(self)")
        try:
            return self.__driver.name
        except Exception as exc:
            self.exception_util.generic_exception("Unable to get browser where test case is running", exc)
            raise

    def press_enter_keys(self):
        self.log.debug("DriverCore.press_enter_keys(self):")
        try:
            import pyautogui as KEYS
            KEYS.press('enter')
        except Exception as exc:
            self.exception_util.generic_exception("Unable to press the enter key using pyautogui API in active window",
                                                  exc)
            raise

    def press_keyboard_keys(self, key):
        """
        Method to simulate mouse events.
        :param key:
        Keys should be sent in the format as ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
        ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
        'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
        'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
        'browserback', 'browserfavorites', 'browserforward', 'browserhome',
        'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
        'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
        'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
        'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
        'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
        'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
        'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
        'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
        'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
        'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
        'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
        'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
        'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
        'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
        'command', 'option', 'optionleft', 'optionright']
        """
        self.log.debug("DriverCore.press_keyboard_keys(self, key): key : " + key)
        try:
            import pyautogui as KEYS
            KEYS.press(key)
        except Exception as exc:
            self.exception_util.generic_exception(
                "Unable to press the" + key + "key using pyautogui API in active window",
                exc)
            raise

    def is_check_box_selected(self, locator):
        self.log.debug("DriverCore.is_check_box_selected(self, locator): locator : " + locator)
        try:
            self.wait_for_web_element_to_be_appear(locator)
            return self.__driver.find_element_by_xpath(locator).is_selected()
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while checking if checkbox " + locator + " is selected",
                                                  exc)
            raise

    def select_check_box(self, locator):
        self.log.debug("DriverCore.select_check_box(self, locator): locator : " + locator)
        try:
            self.wait_for_web_element_to_be_appear(locator)
            if not self.is_check_box_selected(locator):
                self.__driver.find_element_by_xpath(locator).click()
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to select checkbox: " + locator,
                                                  exc)
            raise

    def deselect_check_box(self, locator):
        self.log.debug("DriverCore.select_check_box(self, locator): locator : " + locator)
        try:
            self.wait_for_web_element_to_be_appear(locator)
            if self.is_check_box_selected(locator):
                self.__driver.find_element_by_xpath(locator).click()
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to deselect checkbox: " + locator,
                                                  exc)
            raise

    def execute_java_script(self, java_script):
        self.log.debug("DriverCore.execute_java_script(self, java_script): java_script : " + java_script)
        try:
            self.__driver.execute_script(java_script)
        except Exception as exc:
            self.exception_util.generic_exception("Unable to execute javascript: " + java_script,
                                                  exc)
            raise

    def java_script_click(self, locator):
        self.log.debug("DriverCore.java_script_click(self, locator): locator : " + locator)
        try:
            element = self.__driver.find_element_by_xpath(locator)
            self.__driver.execute_script("arguments[0].click();", element)
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to click element using javascript: " + locator,
                                                  exc)
            raise

    def java_script_get_hidden_text(self, locator):
        self.log.debug("DriverCore.java_script_get_hidden_text(self, locator): locator : " + locator)
        try:
            element = self.__driver.find_element_by_xpath(locator)
            return str(self.__driver.execute_script("return arguments[0].innerText", element))
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting(locator + "to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to get hidden text from element with javascript: "
                                                  "" + locator, exc)
            raise

    def verify_title(self, title):
        self.log.debug("DriverCore.verify_title(self, title): title : " + title)
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            element.until(EC.title_is(title))
            return True
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to verify title of page is: " + title, exc)
            raise

    def verify_title_contains(self, title):
        self.log.debug("DriverCore.verify_title_contains(self, title): title : " + title)
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            element.until(EC.title_contains(title))
            return True
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to verify title of page contains: " + title, exc)
            raise

    def verify_url(self, expected_url):
        self.log.debug("DriverCore.verify_url(self, expected_url): expected_url : " + expected_url)
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            element.until(EC.url_to_be(expected_url))
            return True
        except Exception as exc:
            self.exception_util.generic_exception("Error while trying to verify current the url is:" + expected_url,
                                                  exc)
            raise

    def verify_url_contains(self, expected_url):
        self.log.debug("DriverCore.verify_url_contains(self, expected_url): expected_url : " + expected_url)
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            element.until(EC.url_contains(expected_url))
            return True
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error while trying to verify current the url contains : " + expected_url, exc)
            raise

    def get_alert_text(self):
        self.log.debug("DriverCore.get_alert_text(self)")
        try:
            self.wait_for_alert()
            alert_obj = self.__driver.switch_to_alert()
            return alert_obj.text
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting("alert to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Unable to get the alert text", exc)
            raise

    def verify_alert_text(self, expected_text):
        self.log.debug("DriverCore.verify_alert_text(self,expected_text) expected_text: " + expected_text)
        try:
            self.wait_for_alert()
            alert_obj = self.__driver.switch_to_alert()
            if expected_text == alert_obj.text:
                return True
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting("alert to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while verifying alert contains the text: " + expected_text,
                                                  exc)
            raise

    def accept_alert(self):
        self.log.debug("DriverCore.accept_alert(self)")
        try:
            self.wait_for_alert()
            obj_alert = self.__driver.switch_to_alert()
            obj_alert.accept()
        except Exception as exc:
            self.exception_util.generic_exception("Unable to accept the alert", exc)
            raise

    def accept_dismiss(self):
        self.log.debug("DriverCore.accept_dismiss(self)")
        try:
            self.wait_for_alert()
            obj_alert = self.__driver.switch_to_alert()
            obj_alert.dismiss()
        except Exception as exc:
            self.exception_util.generic_exception("Unable to dismiss the alert", exc)
            raise

    def wait_for_alert(self):
        self.log.debug("DriverCore.wait_for_alert(self)" + str(self.__timeout))
        try:
            element = WebDriverWait(self.__driver, self.__timeout)
            return element.until(EC.alert_is_present())
        except TimeoutException as exc:
            self.exception_util.time_out_while_waiting("alert to appear.", exc)
            raise
        except Exception as exc:
            self.exception_util.generic_exception("Error while waiting for alert to be present", exc)
            raise

    def get_link_response_code(self, link):
        self.log.debug("DriverCore.get_link_response_code(self,link) : " + link)
        try:
            req = requests.head(link)
            return (req.status_code)
        except Exception as exc:
            self.exception_util.generic_exception("Error occurred wile waiting for link response code : " + link, exc)

    def get_element_by_tag_name(self, element, tag_name):
        self.log.debug("DriverCore.get_element_by_tag_name(self,element) : " + str(element) + "tag name : " + tag_name)
        try:
            element_out = element.find_element_by_tag_name(tag_name)
            return element_out
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred wile trying for  tag names: " + tag_name + " from element :" + element, exc)

    def get_elements_by_tag_name(self, element, tag_name):
        self.log.debug("DriverCore.get_elements_by_tag_name(self,element) : " + str(element))
        try:
            element_out = element.find_elements_by_tag_name(tag_name)
            return element_out
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred wile trying for  tag names: " + tag_name + " from element :" + element, exc)

    def validate_if_element_present(self, locator):
        self.log.debug("DriverCore.validate_if_element_present(self,locator) : " + str(locator))
        try:
            self.wait_for_web_element_to_be_appear(locator)
            return True
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred while validating the locator" + locator, exc)

    def check_if_enabled(self, locator):
        self.log.debug("DriverCore.check_if_enabled(self,locator) : " + str(locator))
        try:
            self.wait_for_web_element_to_be_appear(locator)
            return self.__driver.find_element_by_xpath(locator).is_enabled()
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred while checking if the locator enabled or not" + locator, exc)
            raise

    def terminate_browser(self):
        self.log.debug("terminate_browser(self):")
        try:
            if self.__driver is not None:
                self.__driver.close()
            elif self.__driver is None:
                self.log.debug("Browser instance is none, Cannot be closed")
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred while closing browser instance", exc)
            raise

    def quit_session(self):
        self.log.debug("quit_session(self):")
        try:
            if self.__driver is not None:
                self.__driver.quit()
            elif self.__driver is None:
                self.log.debug("Browser instance is none, Cannot be closed")
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred while closing browser instance", exc)
            raise

    def scroll_with_element(self, locator):
        self.log.debug("scroll_with_element(self,locator):")
        try:
            self.wait_for_web_element_to_be_appear(locator)
            web_element = self.__driver.find_element_by_xpath(locator)
            web_element.location_once_scrolled_into_view
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred while scrolling down", exc)
            raise

    def send_keys_with_element(self, locator, left=False, right=False):
        self.log.debug("send_keys_with_element(self,locator,left={0},right={1})".format(str(left), str(right)))
        try:
            action = ActionChains(self.__driver)
            web_element = self.__driver.find_element_by_xpath(locator)
            if left:
                action.send_keys_to_element(web_element, Keys.ARROW_LEFT).release().perform()
            if right:
                action.send_keys_to_element(web_element, Keys.ARROW_RIGHT).release().perform()
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred while sending keys", exc)
            raise

    def get_browser_cookies(self):
        self.log.debug("get_browser_cookies():")
        try:
            return self.__driver.get_cookies()
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred while sending keys", exc)
            raise

    def get_browser_cookie_value(self, key_name):
        self.log.debug("get_browser_cookie_value(self, key_name):" + str(key_name))
        try:
            return self.__driver.get_cookie(key_name)
        except Exception as exc:
            self.exception_util.generic_exception(
                "Error occurred while sending keys", exc)
            raise
