import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import cycle, islice

weekMap = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}

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

def getWeekFromDateSre(s):
    from datetime import datetime as dt
    return weekMap[dt.strptime(s, '%Y-%m-%d').weekday()]

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
historiy_url = historiy_url.map(toNumToDateStr).value_counts().sort_index(ascending=True).reset_index()

# set range 
start_date = strToDate(historiy_url.loc[0, 'index'])
end_data = strToDate(historiy_url.iloc[-1, historiy_url.columns.get_loc('index')])
target_duration = [dateToStr(i) for i in daterange(start_date, end_data)]
target_duration = pd.DataFrame(target_duration, columns=['index'])

historiy_url = pd.merge(historiy_url, target_duration, on='index', how='outer').sort_values(by=['index'])
historiy_url_week = historiy_url['index'].apply(getWeekFromDateSre).rename('week')

# avg_visit = historiy_url['last_visit_time'].mean()
historiy_url = pd.concat([historiy_url,historiy_url_week],axis=1).fillna(0).rename(columns={'index':'date'})

temperature = pd.read_csv(f'{csv_dir}/temperature.csv')
temperature = temperature.loc[:, ['date', 'temp_avg', 'temp_max']]
historiy_url = historiy_url.merge(temperature, how='inner', on='date')
del temperature

events = pd.read_csv(f'{csv_dir}/event.csv')
events = events.groupby('date').count().reset_index()
# events = events.drop('index')
historiy_url = historiy_url.merge(events, how='inner', on='date')

sns.pairplot(historiy_url)

# ticks=4
# x = list(historiy_url['date'])

# fig, ax = plt.subplots()
# ax.bar(x, historiy_url['last_visit_time'], color='#E5E5E5')
# ax2 = ax.twinx()
# ax2.plot(x, historiy_url['temp_avg'])
# ax2.plot(x, historiy_url['event_name'])
# plt.xticks(range(0, len(x), ticks), x[::ticks], rotation=70)

plt.savefig(f'{fig_dir}/keywords_correlations.png', bbox_inches="tight")
plt.savefig(f'{pdf_dir}/keywords_correlations.pdf', bbox_inches="tight")
plt.clf()
