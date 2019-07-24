import chrprofiler.constant as ct


def toNumToHourStr(num):
    from datetime import datetime, timedelta
    #Google Chromeのタイムスタンプは、通常のUNIXタイムではなく、1601年1月1日0:00からの”マイクロ秒”となっている点に注意
    num = ((num / 1000000) - 11644473600 + (9*60*60)) / 86400 + 25569
    ret = datetime(1899, 12, 30) + timedelta(days=num)
    return ret.strftime('%H oclock')

def toNumToDateStr(num):
    from datetime import datetime, timedelta
    #Google Chromeのタイムスタンプは、通常のUNIXタイムではなく、1601年1月1日0:00からの”マイクロ秒”となっている点に注意
    num = ((num / 1000000) - 11644473600 + (9*60*60)) / 86400 + 25569
    ret = datetime(1899, 12, 30) + timedelta(days=num)
    return ret.strftime('%Y-%m-%d')

def toNumToTimeStr(num):
    from datetime import datetime, timedelta
    #Google Chromeのタイムスタンプは、通常のUNIXタイムではなく、1601年1月1日0:00からの”マイクロ秒”となっている点に注意
    num = ((num / 1000000) - 11644473600 + (9*60*60)) / 86400 + 25569
    ret = datetime(1899, 12, 30) + timedelta(days=num)
    return ret.strftime('%H:%m:%s')

def dateToStr(d):
    from datetime import datetime as dt
    return dt.strftime(d, '%Y-%m-%d')

def strToDate(s):
    from datetime import datetime as dt
    return dt.strptime(s, '%Y-%m-%d')

def daterange(_start, _end):
  from datetime import datetime, timedelta
  for n in range((_end - _start).days):
    yield _start + timedelta(n)

def getWeekFromDateSre(s):
    from datetime import datetime as dt
    return ct.WEEK_MAP[dt.strptime(s, '%Y-%m-%d').weekday()]