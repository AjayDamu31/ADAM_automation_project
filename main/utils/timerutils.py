from time import strptime, mktime
from dateutil.relativedelta import relativedelta
from datetime import datetime
import calendar
import time


class TimerUtil(object):

    @staticmethod
    def epoch_converter(date_data):
        """
        Method to generate the epoch for the date time data in the GMT format.
        :param date_data: Return the epoch
        :return:
        """
        return int(calendar.timegm(strptime(str(date_data), "%Y-%m-%d %H:%M:%S"))) * 1000

    @staticmethod
    def date_time_generator(input_date):
        """
        Method to generate the date time based user input.
        :param input_date: Input date time range to generate. Format 'y=year_difference,m=month_difference,d=day_difference,H=hour,M=minutes'
        :return: Return the date time date.
        """
        arg1 = {i[0]: int(i[2:]) for i in input_date.split(",")}
        return datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=+arg1['d'], months=+arg1['m'],
                                                                             years=+arg1['y'], hour=arg1['H'],
                                                                             minute=arg1['M'], second=0)

    def get_date_difference(self, diff, start_date=None, end_date=None):
        print(datetime.utcnow())
        if diff == "lhr":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=-1, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=0, minute=0,
                                                                                  second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict
        elif diff == "l2hr":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=-2, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=0, minute=0,
                                                                                  second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict
        elif diff == "l4hr":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=-4, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=0, minute=0,
                                                                                  second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict
        elif diff == "l2d":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=-3, hour=0, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=-1, hour=0, minute=0,
                                                                                  second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict
        elif diff == "chr":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=0, hours=0, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=0, hours=0, minutes=0,
                                                                                  second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict
        elif diff == "cus":
            date_dict = {'start_date': self.date_time_generator(start_date).strftime("%Y-%m-%d %H:%M:%S"),
                         'end_date': self.date_time_generator(end_date).strftime("%Y-%m-%d %H:%M:%S")}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict
        elif diff == "l7d":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=-7, hours=0, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=0, hours=0,
                                                                                  second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict
        elif diff == "l1d":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=-1, hours=0, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(days=0, hours=0,
                                                                                  second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict
        elif diff == "l1m":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(day=1, hours=0, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=0, second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            print(date_dict, "data")
            return date_dict
        elif diff == "l1hr":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=-1, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=0, second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            print(date_dict, "data")
            return date_dict
        elif diff == "l30d":
            date_dict = {'start_date': str(
                datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(day=1, hours=0, minute=0, second=0)),
                'end_date': str(
                    datetime.fromtimestamp(mktime(time.gmtime())) + relativedelta(hours=0, second=0))}
            date_dict['start_date_epoch'] = self.epoch_converter(date_dict['start_date'])
            date_dict['end_date_epoch'] = self.epoch_converter(date_dict['end_date'])
            return date_dict


if __name__ == '__main__':
    obj = TimerUtil()
    # #     #     # o = obj.date_time_generator("y=0,m=0,d=7,H=0,M=0")
    # #     #     # print(type(o.strftime("%Y-%m-%d %H:%M:%S")))
    # #     #     # print(obj.epoch_converter(o))
    s = obj.get_date_difference("l1hr")
    print(s)
# s = obj.get_date_difference("Previous hour")
# print(s)
