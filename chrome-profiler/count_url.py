import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import re


def toNumToTimeStr(num):
    from datetime import datetime, timedelta
    #Google Chromeのタイムスタンプは、通常のUNIXタイムではなく、1601年1月1日0:00からの”マイクロ秒”となっている点に注意
    num = ((num / 1000000) - 11644473600 + (9*60*60)) / 86400 + 25569
    ret = datetime(1899, 12, 30) + timedelta(days=num)
    return ret.strftime('%H:%m:%s')

def getUrlDomain(url: str):
    url = url.split('://')
    url[1] = url[1].split('/')[0]
    url[1] = url[1].split(':')[0]
    return url[1]

def deleteSpecifiedWord(s):
    if 'login' in s:
        return False
    elif re.match(r'[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}', s):
        # get rid of local IP
        return False
    elif s == '':
        return False

    return True
    

# system parameter
fig_dir = './fig'
csv_dir = './csv'
pdf_dir = './pdf'

# database
dbname = 'History'
historiy_url = pd.read_csv(f'{csv_dir}/history_devpc_urls.csv')
historiy_url = historiy_url.loc[:, ['url', 'title', 'visit_count', 'last_visit_time']]
historiy_url['url'] = historiy_url['url'].map(getUrlDomain)
historiy_url = historiy_url[historiy_url['url'].map(deleteSpecifiedWord) == True]
historiy_url = historiy_url[~historiy_url['url'].str.contains("google.com")]

# print(historiy_url)
historiy_url_visit = historiy_url.loc[:, ['url', 'visit_count']].groupby('url').sum().reset_index()
historiy_url_visit = historiy_url_visit.sort_values(by='visit_count', ascending=False)
historiy_url_visit = historiy_url_visit[historiy_url_visit['visit_count'] >= 15].reset_index().drop('index', axis=1)

historiy_title = historiy_url.loc[:, ['title', 'url']]#.groupby('url').apply(list)

plt.rcParams.update({'font.size': 7})
fig, ax = plt.subplots()
ax.barh(y=historiy_url_visit['url'].tolist()[::-1], 
        width=historiy_url_visit['visit_count'].tolist()[::-1],
        alpha=0.7)
plt.savefig(f'{fig_dir}/keywords_visited_url.png', bbox_inches="tight")
plt.savefig(f'{pdf_dir}/keywords_visited_url.pdf', bbox_inches="tight")
# plt.tick_params(axis='y', which='major', labelsize=3)
plt.close()
