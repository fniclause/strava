from math import radians, cos, sin, asin, sqrt
from numpy import nan
from datetime import datetime, timezone
import calendar

#create log
def log(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now=datetime.now()
    timestamp = now.strftime(timestamp_format)
    print(timestamp+' , '+message+';')
    

def start_date(date_):
    return datetime.fromisoformat(date_[:-1])
def get_weekday(date_):
    #date_=datetime.fromisoformat(date_[:-1] + '+00:00').astimezone(timezone.utc)
    return calendar.day_name[date_.weekday()]
def get_day(date_):
    return date_.day
def get_month(date_):
    return date_.month
def get_year(date_):
    return date_.year
def get_week(date_):
    return date_.week

def localize_time(time_):
    return time_.tz_localize('Europe/Paris')
