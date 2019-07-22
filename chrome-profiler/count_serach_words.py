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

# plotting
fig, ax = plt.subplots()
historiy_kw_count = historiy_kw_only.count()
bar = ax.bar(x=historiy_kw_count.index.tolist(),
             height=historiy_kw_count.values,
             tick_label=historiy_kw_count.index.tolist(),
             alpha=0.7
             )
ax.set_ylabel('Count of Searched Keywords')

ax2 = ax.twinx()
historiy_kw_count_stacked = historiy_kw_count.cumsum() / historiy_kw_count.sum() * 100
line = ax2.plot(historiy_kw_count_stacked.index.tolist(),
                historiy_kw_count_stacked.values,
                ls='-',
                marker='o',
                color='#808080'
                )
threshold = ax2.plot(historiy_kw_count_stacked.index.tolist(),
                    [90] * len(historiy_kw_count_stacked.index.tolist()),
                    ls="--",
                    color="#800000")

ax2.text(historiy_kw_count.index.tolist()[-3], 87, '90% threshold', fontsize=10)
ax2.set_ylabel('Cumulative Sum')
ax2.grid(visible=False)

plt.savefig(f'{fig_dir}/keywords_search_pairs_count.png', bbox_inches="tight")
plt.savefig(f'{pdf_dir}/keywords_search_pairs_count.pdf', bbox_inches="tight")
plt.clf()
