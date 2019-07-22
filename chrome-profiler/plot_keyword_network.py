import networkx as nx
import matplotlib.pyplot as plt
import search_classifier_utils as utils
import pandas as pd


# system parameter
fig_dir = './fig'
csv_dir = './csv'
pdf_dir = './pdf'

def __create_keywords_data():
    keywords = []

    # CSVからキーワードを取得
    df = pd.read_csv('./csv/history_devpc_keywords.csv')
    
    for index, row in df.iterrows():
        keywords.append(row['lower_term'])
    
    return keywords


def __get_co_occurrence_matrix_from(keywords):
    # Reference https://www.monotalk.xyz/blog/google-search-console-%E3%81%AE-%E3%82%AD%E3%83%BC%E3%83%AF%E3%83%BC%E3%83%89%E3%81%AE%E5%85%B1%E8%B5%B7%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E5%9B%B3%E3%82%92-python-%E3%81%A7%E6%8F%8F%E7%94%BB%E3%81%99%E3%82%8B/
    # TfidfVectorizer で共起単語行列を作る
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(
        1, 1), stop_words=utils.stop_words, max_df=0.5, min_df=1, max_features=3000, norm='l2')
    X = tfidf_vectorizer.fit_transform(keywords)
    # normalized co-occurence matrix
    import scipy.sparse as sp
    Xc = (X.T * X)
    g = sp.diags(2. / Xc.diagonal())
    Xc_norm = g * Xc

    import collections
    splited_keywords = []
    for keyword in keywords:
        splited_keywords.extend(utils.split_keyword(keyword))
    counter = collections.Counter(splited_keywords)
    return Xc_norm, tfidf_vectorizer.vocabulary_, counter


def main(debug=False):
    # 1. キーワード文字列を取得
    keywords = __create_keywords_data()

    # 2. 共起単語行列を作成する
    Xc_norm, vocabulary, counter = __get_co_occurrence_matrix_from(keywords)

    # 3. networkx で、ネットワーク図を描画
    # 3-1.初期ノードの追加
    G = nx.from_scipy_sparse_matrix(
        Xc_norm, parallel_edges=True, create_using=nx.DiGraph(), edge_attribute='weight')

    # 3-2.nodeに、count にcount属性を設定
    value_key_dict = {}
    for key, value in vocabulary.items():
        count = counter.get(key, 0)
        nx.set_node_attributes(G, {value: count}, "count")
        value_key_dict.update({value: key})

    # 3-3.エッジと、ノードの削除
    # 出現回数の少ないエッジを削除
    removed_edges = []
    for (u, v, d) in G.edges(data=True):
        if d["weight"] <= 0.10:
            removed_edges.append((u, v))
    for e in removed_edges:
        G.remove_edge(e[0], e[1])

    # 出現回数の少ないノードを除去
    removed_edges.clear()
    for n, a in G.nodes(data=True):
        if a["count"] <= 10:
            removed_edges.append(n)
    for n in removed_edges:
        G.remove_node(n)

    # 3-4 ラベルの張り替え、from_scipy_sparse_matrix 設定時はラベルとして1,2,3 等の数値が設定されている
    G = nx.relabel_nodes(G, value_key_dict)

    # グラフ整形のためかけ離れたもの削除
    # G.remove_node('')

    # 3-5 描画のために調整  
    # figsize で 図の大きさを指定
    plt.figure(figsize=(10, 10))
    # 反発力と吸引力の調整
    pos = nx.spring_layout(G, k=0.1)
    # ノードサイズの調整
    node_size = [d['count'] * 30 for (n, d) in G.nodes(data=True)]
    nx.draw_networkx_nodes(G, pos, node_color='lightgray',
                           alpha=0.3, node_size=node_size)
    # フォントサイズ、使用するフォントの設定
    nx.draw_networkx_labels(G, pos, fontsize=6,
                            font_family="IPAexGothic", font_weight="bold")
    # エッジの線の調整
    edge_width = [d['weight'] * 2 for (u, v, d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='c', width=edge_width)
    # 枠線の表示/非表示 on:表示 off:非表示
    plt.axis("off")
    plt.savefig(f'{fig_dir}/keywords_co-occurrence_network.png', bbox_inches="tight")
    plt.savefig(f'{pdf_dir}/keywords_co-occurrence_network.pdf', bbox_inches="tight")


if __name__ == '__main__':
    main(False)