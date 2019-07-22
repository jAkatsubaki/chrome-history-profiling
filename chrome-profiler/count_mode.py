import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# system parameter
fig_dir = './fig'
csv_dir = './csv'
pdf_dir = './pdf'

# database
dbname = 'History'
historiy_kw = pd.read_csv(f'{csv_dir}/history_devpc_keywords.csv')
origin_col_num = len(historiy_kw.columns)

historiy_kw = pd.concat([historiy_kw, historiy_kw['lower_term'].str.split(' ', expand=True)], axis=1)
split_col_num = len(historiy_kw.columns) - origin_col_num
for i in range(0, split_col_num):
    historiy_kw = historiy_kw.rename(columns={i:f'kw_{i}'})

historiy_kw[historiy_kw.isnull()] = np.nan
# keyword extraction
historiy_kw_only = historiy_kw.loc[:,'kw_0':]

historiy_kw_count = historiy_kw_only.apply(pd.value_counts)
historiy_kw_count = historiy_kw_count.fillna(0.)

# top 20 words
historiy_kw_count_top20 = historiy_kw_count.sum(axis=1).sort_values(ascending=False).iloc[:20]

fig, ax = plt.subplots()
ax.barh(y=historiy_kw_count_top20.index.tolist()[::-1], 
        width=historiy_kw_count_top20.values.tolist()[::-1],
        alpha=0.7)

plt.savefig(f'{fig_dir}/keywords_search_count_top20.png', bbox_inches="tight")
plt.savefig(f'{pdf_dir}/keywords_search_count_top20.pdf', bbox_inches="tight")
plt.clf()

