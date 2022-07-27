from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import networkx as nx
db_connection_str = 'mysql://root:mysqlpw@localhost:49153/gnn_db'
db_connection = create_engine(db_connection_str)



def get_user_data(ids):
    str_query="SELECT post_id, user_id FROM user_post WHERE "
    i=0
    for post_id in ids:
        if (i==0):
            str_query+=" post_id="+str(post_id)
        else:
            str_query+=" or post_id="+str(post_id)
        i+=1
    str_query+=" ORDER BY user_id ASC"

    df_user_post=pd.read_sql(str_query, con=db_connection)



    df_user_id= df_user_post["user_id"]

    str_query="SELECT * FROM user_user WHERE"
    i=0
    for user_id in df_user_id:
        if (i==0):
            str_query+=" (user_id_1="+str(user_id)+" or (user_id_2="+str(user_id)+" and relationship=\"friend\"))"
        else:
            str_query+=" or (user_id_1="+str(user_id)+" or (user_id_2="+str(user_id)+" and relationship=\"friend\"))"
        i+=1
    
    df_rel_user=pd.read_sql(str_query, con=db_connection)
    
    df_rel_user.replace("friend", 1, inplace=True)
    df_rel_user.replace("follow", 0.5, inplace=True)
    add_friend_list={"user_id_1":[], "user_id_2":[], "relationship":[]}
    for _, row in df_rel_user.iterrows():
        if row["relationship"]==1:
            print(type(row['user_id_1']))
            add_friend_list['user_id_1'].append((row["user_id_2"]))
            add_friend_list['user_id_2'].append((row["user_id_1"]))
            add_friend_list['relationship']=1

    print(add_friend_list)
    new_df=pd.DataFrame(add_friend_list)
    df_rel_user=pd.concat([df_rel_user ,new_df]).drop("id", axis=1)
    str_query="SELECT * FROM user_info WHERE"
    i=0
    for _,user_id in df_rel_user.iterrows():
        if (i==0):
            str_query+=" id="+str(user_id["user_id_1"])+" or id="+str(user_id["user_id_2"])
        else:
            str_query+=" or id="+str(user_id["user_id_1"])+" or id="+str(user_id["user_id_2"])
        i+=1
    str_query+=" ORDER BY id ASC"

    df_user_info=pd.read_sql(str_query, con=db_connection)
    df_user_ids=np.array(df_user_info["id"].values)


    post_list=np.array(ids)
    print(post_list)
    # print(len(df_user_ids))

    user_post_matrix=np.zeros((len(df_user_ids), len(post_list)))
    print(user_post_matrix.shape)
    # print(df_user_ids)
    for user_id, post_id in df_user_post[['user_id', 'post_id']].values:
        print(user_id, post_id)
        idx_user=np.where(df_user_ids==user_id)
        idx_post=np.where(post_list==post_id)
        print(idx_user[0][0])
        print(idx_post[0][0])
        print(user_post_matrix[0][1])
        user_post_matrix[idx_user[0][0]][idx_post[0][0]]=1

    print(user_post_matrix)

    print(df_user_ids)
    df_encode_user=encode_user_data(df_user_info)
    print(df_encode_user)
    print(df_rel_user)
    graph_user_user=nx.DiGraph()
    graph_user_user.add_nodes_from(df_user_ids)
    graph_user_user.add_weighted_edges_from(df_rel_user[["user_id_1", "user_id_2", "relationship"]].values)
    
    nx.draw_networkx(graph_user_user, with_labels = True)
    user_user_matrix = nx.adjacency_matrix(
            graph_user_user,
            # nodelist=df_rel_user['user_id_1'].values
        )
    print(user_user_matrix.A[0])
    return(df_rel_user)

def encode_user_data(user_df):
    kept_features = [
            'statuses_count',
            'followers_count',
            'friends_count',
            'favourites_count',
            'listed_count',
            'default_profile',
            'default_profile_image',
            'protected',
            'verified',
            'updated',
            'created_at',
            'name',
            'screen_name',
            'description'
        ]
    user_df = user_df[kept_features].copy()
    if 'updated' in user_df.columns:
        age = (
            pd.to_datetime(user_df.loc[:, 'updated']) - 
            pd.to_datetime(user_df.loc[:, 'created_at']).dt.tz_localize(None)
        ) / np.timedelta64(1, 'Y')
    else:
        age = (
            pd.to_datetime(pd.to_datetime('today')) - 
            pd.to_datetime(user_df.loc[:, 'created_at']).dt.tz_localize(None)
        ) / np.timedelta64(1, 'Y')
    user_df['tweet_freq'] = user_df['statuses_count'] / age
    user_df['followers_growth_rate'] = user_df['followers_count'] / age
    user_df['friends_growth_rate'] = user_df['friends_count'] / age
    user_df['favourites_growth_rate'] = user_df['favourites_count'] / age
    user_df['listed_growth_rate'] = user_df['listed_count'] / age
    user_df['followers_friends_ratio'] = user_df['followers_count'] / np.maximum(user_df['friends_count'], 1)
    user_df['screen_name_length'] = user_df['screen_name'].str.len()
    user_df['num_digits_in_screen_name'] = user_df['screen_name'].str.count('\d')
    user_df['name_length'] = user_df['name'].str.len()
    user_df['num_digits_in_name'] = user_df['name'].str.count('\d')
    user_df['description_length'] = user_df['description'].str.len()
    return user_df.select_dtypes('number').fillna(0.0)



df_user=get_user_data([2,4])
