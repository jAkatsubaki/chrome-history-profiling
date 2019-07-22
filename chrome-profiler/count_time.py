import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import cycle, islice

weekMap = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}

def toNumToTimeStr(num):
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

def getWeekFromDateStr(s):
    from datetime import datetime as dt
    return str(dt.strptime(s, '%Y-%m-%d').weekday()) + weekMap[dt.strptime(s, '%Y-%m-%d').weekday()]

# system parameter
fig_dir = './fig'
csv_dir = './csv'
pdf_dir = './pdf'

# database
dbname = 'History'
historiy_url = pd.read_csv(f'{csv_dir}/history_devpc_urls.csv')

# get access date (without time)
historiy_url = historiy_url['last_visit_time']
# aggregate based on date
historiy_time = historiy_url.map(toNumToTimeStr).rename('time')
historiy_week = historiy_url.map(toNumToDateStr).map(getWeekFromDateStr).rename('week')

historiy_url = pd.concat([historiy_time, historiy_week], axis=1)


heatmap_table = pd.DataFrame({'count' : historiy_url.groupby(['time', 'week']).size()}).reset_index()
heatmap_data = pd.pivot_table(heatmap_table, values='count', 
                     index=['time'], 
                     columns='week')
sns.heatmap(heatmap_data, cmap="YlGnBu")
plt.savefig(f'{fig_dir}/keywords_search_heatmap_time_and_weekday.png', bbox_inches="tight")
plt.savefig(f'{pdf_dir}/keywords_search_heatmap_time_and_weekday.pdf', bbox_inches="tight")
