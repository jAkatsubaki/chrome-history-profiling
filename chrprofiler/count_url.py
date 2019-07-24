import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import re
import chrprofiler.constant as ct
import chrprofiler.dateutil as dtutl
import chrprofiler.textutil as txtutl


def run():
    # database
    historiy_url = pd.read_csv(f'{ct.CSV_DIR}/history_devpc_urls.csv')
    historiy_url = historiy_url.loc[:, ['url', 'title', 'visit_count', 'last_visit_time']]
    historiy_url['url'] = historiy_url['url'].map(txtutl.getUrlDomain)
    historiy_url = historiy_url[historiy_url['url'].map(txtutl.deleteSpecifiedWord) == True]
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
    plt.savefig(f'{ct.FIG_DIR}/keywords_visited_url.png', bbox_inches="tight")
    plt.savefig(f'{ct.PDF_DIR}/keywords_visited_url.pdf', bbox_inches="tight")
    plt.close()
