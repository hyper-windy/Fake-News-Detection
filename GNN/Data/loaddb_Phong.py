from sqlalchemy import create_engine
import pandas as pd
import networkx as nx
from collections import deque
import numpy as np

db_connection_str = 'mysql+pymysql://root:Thucuatoi123@localhost/gnn_db'
db_connection = create_engine(db_connection_str)

# Get post list data
try:
    df_post = pd.read_sql(sql="SELECT * FROM post", con=db_connection)
    # print(df_post)
except:
    pass


def feature_tweet(self, tweet_df):
    """
    Use TF-IDF encode
    """
    vect = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=5000)
    v = vect.fit_transform(tweet_df)
    # with open('vect/vectorizer.pk', 'wb') as fin:
    #     pickle.dump(vect, fin)
    return v


res = feature_tweet.A

for idx, row in df_post.iterrows():
    print(row.id)
    postList = [row]
    graph = nx.DiGraph()
    doubleQueue = deque([row.id])
    graph.add_node(row.id)

    while len(doubleQueue) > 0:
        node = doubleQueue.popleft()

        try:
            df = pd.read_sql(sql="SELECT post_id_1, action FROM post_post WHERE post_id_2 = {}".format(node),
                             con=db_connection)
            for _, r in df.iterrows():
                doubleQueue.append(r.post_id_1)
                graph.add_node(r.post_id_1)
                graph.add_edge(r.post_id_1, node, weight=1 if r.action == "cmt" else 2)
        except:
            pass

    print(graph.nodes)
    A = nx.adjacency_matrix(graph)
    print(A.todense())










