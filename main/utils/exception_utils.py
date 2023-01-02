class ExceptionUtils(object):
    def __init__(self, log):
        self.log = log
        # def no_such_element_exception(self, log, element, ):

    #     log.exception("")
    #
    # def no_such_element_exception(self, log, element, message):
    #     log.exception("")
    def generic_exception(self, message, exception):
        """
        Method to log an unknown exception
        :param
        message: Message that is required to appear in log
        :param
        exception: Exception that has been captured
        """
        error_message = message + ". Exception raised : " + type(exception).__name__
        self.log.error(error_message)
        self.log.error("Exception raised due to : " + exception.__doc__)
        self.log.exception("Exception raised")

    def no_such_element_exception(self, message, exception):
        """
        Method to handle no such element exception thrown by selenium exception.

        :param
        message: Message that is required to appear in log
        :param
        exception: Exception that has been captured
        """
        error_message = message + ". Exception raised : "
        self.log.error(error_message)
        self.log.error("NoSuchElementException raised due to : " + exception.__doc__)
        self.log.exception("Exception raised")

    def time_out_while_waiting(self, message, exception):
        """
        Method to handle time out exception.
        :param
        message: Message that is required to appear in log
        :param
        exception: Exception that has been captured
        """
        error_message = "Timed out while waiting for " + message + " Exception raised : "
        self.log.error(error_message)
        self.log.error("Time out Exception: " + exception.__doc__)
        self.log.exception("Exception raised")

    def mismatch_exception(self, locator, exception, actual_text, expected_text):
        """
        Method to handle mismatch exception.
        :param locator: Locator from the user.
        :param exception: Exception that has been captured.
        :param actual_text: Text from the UI.
        :param expected_text: Text from the user.
        :return:
        """
        error_message = "Mismatch exception: Text mismatch at locator : " + locator + "/n" + \
                        ". Expected text : " + expected_text + ". Actual text : " + actual_text + "."

        self.log.error(error_message)
        self.log.error("Exception raised due to : " + exception.__doc__)
        self.log.exception("Exception raised")

    def index_error(self, locator, exception, index):
        """
        Method to handle index error.
        :param locator: Locator from the user.
        :param exception: Exception that has been captured.
        :param index: Index from the UI.
        """
        error_message = "Index error occurred. Attempted to access element : " + locator + "/n" + \
                        "from the index : " + index

        self.log.error(error_message)
        self.log.error("Exception raised due to : " + exception.__doc__)
        self.log.exception("Exception raised")
