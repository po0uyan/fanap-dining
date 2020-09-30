import datetime

import jdatetime
week_day_convert = {0: "شنبه", 1: "یکشنبه", 2: "دوشنبه", 3 : "سه‌شنبه", 4 : "چهارشنبه", 5 : "پنجشنبه", 6 : "جمعه"}
month_convert = {
    1:"فروردین",
    2:"اردیبهشت",
    3:"خرداد",
    4:"تیر",
    5:"مرداد",
    6:"شهریور",
    7:"مهر",
    8:"آبان",
    9:"آذر",
    10:"دی",
    11:"بهمن",
    12:"اسفند"
}


def convert_to_date(date):
    return jdatetime.datetime.strptime(date, '%Y-%m-%d')


def get_day_name(date):
    res = convert_to_date(date)
    return week_day_convert[res.weekday()]


def get_day(date):
    res = convert_to_date(date)
    return str(res.day)


def get_month_name(date):
    res = convert_to_date(date)
    return month_convert[res.month]


def next_day(date):
    date = convert_to_date(date)
    date += datetime.timedelta(days=1)
    return str(date.date())


def previous_day(date):
    date = convert_to_date(date)
    date -= datetime.timedelta(days=1)
    return str(date.date())


def get_today():
    return str(jdatetime.datetime.now().date())


def get_proper_jalali_time(date):
    return "📅 "+get_day_name(date)+" "+get_day(date)+" ام "+ get_month_name(date) + " ماه "