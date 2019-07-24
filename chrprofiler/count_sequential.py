import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle, islice
import chrprofiler.constant as ct
import chrprofiler.dateutil as dtutil


def run():
    # database
    historiy_url = pd.read_csv(f'{ct.CSV_DIR}/history_devpc_urls.csv')
    
    # get access date (without time)
    historiy_url = historiy_url['last_visit_time']
    # aggregate based on date
    historiy_url = historiy_url.map(dtutil.toNumToDateStr).value_counts().sort_index(ascending=True).reset_index()
    
    # set range 
    start_date = dtutil.strToDate(historiy_url.loc[0, 'index'])
    end_data = dtutil.strToDate(historiy_url.iloc[-1, historiy_url.columns.get_loc('index')])
    target_duration = [dtutil.dateToStr(i) for i in dtutil.daterange(start_date, end_data)]
    target_duration = pd.DataFrame(target_duration, columns=['index'])
    
    historiy_url = pd.merge(historiy_url, target_duration, on='index', how='outer').sort_values(by=['index'])
    historiy_url_week = historiy_url['index'].apply(dtutil.getWeekFromDateSre).rename('week')
    historiy_url = pd.concat([historiy_url,historiy_url_week],axis=1).fillna(0).rename(columns={'index':'date'})
    
    for k, v in ct.WEEK_MAP.items():
        temp = historiy_url['last_visit_time'].where(historiy_url['week'] == v).rename(f'visit_{v.lower()}')
        historiy_url = pd.concat([historiy_url, temp], axis=1)
    
    historiy_url = historiy_url.fillna(0)
    week_summary = historiy_url.drop(['date', 'last_visit_time', 'week'], axis=1)
    week_colors=['#F5F5F5', '#F5F5F5', '#F5F5F5', '#F5F5F5', '#F5F5F5', '#87cefa', '#cd5c5c']
    
    ticks=4
    x = list(historiy_url['date'])
    y = list(historiy_url['last_visit_time'])
    
    # each weekday
    for i in range(0, 5):
        fig = plt.subplot()
        # all days
        fig.plot(x, y, label='all day', marker='*', linestyle='--')
        # each days
        week_colors[i] = '#2756b3'
        week_summary.plot(kind='bar', ax=fig, width=0.3, align='center', stacked=True, color=week_colors)
    
        plt.xticks(range(0, len(x), ticks), x[::ticks], rotation=70)
        plt.xlabel('Date')
        plt.ylabel('Count of Searcing by Chrome')
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize=10)
        plt.savefig(f'{ct.FIG_DIR}/keywords_search_sequential_{ct.WEEK_MAP[i].lower()}.png', bbox_inches="tight")
        plt.savefig(f'{ct.PDF_DIR}/keywords_search_sequential_{ct.WEEK_MAP[i].lower()}.pdf', bbox_inches="tight")
        plt.clf()
        # reset color
        week_colors[i] = '#F5F5F5'
    
    # plotting
    historiy_sum_weekday = historiy_url.loc[:, 'visit_mon':].sum().drop(['visit_sat','visit_sun']).rename('sum')
    historiy_cnt_weekday = historiy_url.groupby('week').count().loc[:,'date'].rename('week_count').drop(['Sat', 'Sun'])
    historiy_cnt_weekday = historiy_cnt_weekday.rename(index={k:f'visit_{k.lower()}' for k in historiy_cnt_weekday.index})
    
    historiy_sum_weekday = pd.concat([historiy_sum_weekday, historiy_cnt_weekday], axis=1)
    historiy_sum_weekday = pd.concat([historiy_sum_weekday, (historiy_sum_weekday['sum'] / historiy_sum_weekday['week_count']).rename('avg')], axis=1)
    historiy_sum_weekday_plt = historiy_sum_weekday.loc[['visit_mon', 'visit_tue', 'visit_wed', 'visit_thu', 'visit_fri'], :]
    
    historiy_sum_weekday_plt.loc[:, 'sum'].plot(kind='bar', rot=45, color='#575757')
    plt.xlabel('Week Day')
    plt.ylabel('Count of Searcing by Chrome')
    plt.savefig(f'{ct.FIG_DIR}/keywords_search_weekday_sum.png', bbox_inches="tight")
    plt.savefig(f'{ct.PDF_DIR}/keywords_search_weekday_sum.pdf', bbox_inches="tight")
    plt.clf()
    
    historiy_sum_weekday_plt.loc[:, 'avg'].plot(kind='bar', rot=45, color='#575757')
    plt.xlabel('Week Day')
    plt.ylabel('Count of Searcing by Chrome')
    plt.savefig(f'{ct.FIG_DIR}/keywords_search_weekday_avg.png', bbox_inches="tight")
    plt.savefig(f'{ct.PDF_DIR}/keywords_search_weekday_avg.pdf', bbox_inches="tight")
    plt.clf()
