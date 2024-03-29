import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import cycle, islice
import chrprofiler.constant as ct
import chrprofiler.dateutil as dtutl


def run():
    # database
    historiy_url = pd.read_csv(f'{ct.CSV_DIR}/history_devpc_urls.csv')
    
    # get access date (without time)
    historiy_url = historiy_url['last_visit_time']
    # aggregate based on date
    historiy_url = historiy_url.map(dtutl.toNumToDateStr).value_counts().sort_index(ascending=True).reset_index()
    
    # set range 
    start_date = dtutl.strToDate(historiy_url.loc[0, 'index'])
    end_data = dtutl.strToDate(historiy_url.iloc[-1, historiy_url.columns.get_loc('index')])
    target_duration = [dtutl.dateToStr(i) for i in dtutl.daterange(start_date, end_data)]
    target_duration = pd.DataFrame(target_duration, columns=['index'])
    
    historiy_url = pd.merge(historiy_url, target_duration, on='index', how='outer').sort_values(by=['index'])
    historiy_url_week = historiy_url['index'].apply(dtutl.getWeekFromDateSre).rename('week')
    
    # avg_visit = historiy_url['last_visit_time'].mean()
    historiy_url = pd.concat([historiy_url,historiy_url_week],axis=1).fillna(0).rename(columns={'index':'date'})
    
    temperature = pd.read_csv(f'{ct.CSV_DIR}/temperature.csv')
    temperature = temperature.loc[:, ['date', 'temp_avg', 'temp_max']]
    historiy_url = historiy_url.merge(temperature, how='inner', on='date')
    del temperature
    
    events = pd.read_csv(f'{ct.CSV_DIR}/event.csv')
    events = events.groupby('date').count().reset_index()
    # events = events.drop('index')
    historiy_url = historiy_url.merge(events, how='inner', on='date')
    
    sns.pairplot(historiy_url)
    
    plt.savefig(f'{ct.FIG_DIR}/keywords_correlations.png', bbox_inches="tight")
    plt.savefig(f'{ct.PDF_DIR}/keywords_correlations.pdf', bbox_inches="tight")
    plt.clf()
