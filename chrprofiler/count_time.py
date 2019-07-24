import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import cycle, islice
import chrprofiler.constant as ct
import chrprofiler.dateutil as dtutl


def run():
    # database
    historiy_url = pd.read_csv(f'{ct.CSV_DIR}/history_devpc_urls.csv')
    
    # get access date (without time)
    historiy_url = historiy_url['last_visit_time']
    # aggregate based on date
    historiy_time = historiy_url.map(dtutl.toNumToHourStr).rename('time')
    historiy_week = historiy_url.map(dtutl.toNumToDateStr).map(dtutl.getWeekFromDateStr).rename('week')
    
    historiy_url = pd.concat([historiy_time, historiy_week], axis=1)
    
    
    heatmap_table = pd.DataFrame({'count' : historiy_url.groupby(['time', 'week']).size()}).reset_index()
    heatmap_data = pd.pivot_table(heatmap_table, values='count', 
                         index=['time'], 
                         columns='week')
    sns.heatmap(heatmap_data, cmap="YlGnBu")
    plt.savefig(f'{ct.FIG_DIR}/keywords_search_heatmap_time_and_weekday.png', bbox_inches="tight")
    plt.savefig(f'{ct.PDF_DIR}/keywords_search_heatmap_time_and_weekday.pdf', bbox_inches="tight")
