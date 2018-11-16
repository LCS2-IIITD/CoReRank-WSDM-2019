import sys
import networkx as nx
import pandas as pd
import numpy as np
from constants import *
from networkx.algorithms import bipartite
from birdnest_detect import *
import logging
import datetime
import time
from imp import reload
from sklearn.model_selection import train_test_split







# Logging Settings

# reload(logging) # only for ipython

curr_time = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%H-%M-%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(filename='logs/' + curr_time + '.log',level=logging.DEBUG, filemode="a+", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',                    datefmt='%m/%d/%Y %I:%M:%S %p')





# Logging the constants of the algorithm first

logging.info('-----------RECURSION CONSTANTS-----------')
logging.info('VERSION:\t\t%s', VERSION)
logging.info('GRAPH FILE:\t%s', GRAPH)
logging.info('GAMMA_SEED_T:\t%f', GAMMA_SEED_T)
logging.info('GAMMA_USER_T:\t%f', GAMMA_USER_T)
logging.info('GAMMA_SEED_U:\t%f', GAMMA_SEED_U)
logging.info('GAMMA_TWEET_U:\t%f', GAMMA_TWEET_U)
logging.info('GAMMA_BIN_U:\t%f', GAMMA_BIN_U)
logging.info('EPSILON:\t\t%f', EPSILON)

# Logging the constants of the BIRDNEST

logging.info('-----------BIRDNEST CONSTANTS-----------')
logging.info('IAT DATA FOR USERS:\t%s', DATA_USERS)
logging.info('IAT DATA FOR TWEETS:\t%s', DATA_TWEETS)
logging.info('LOG BASE FOR IAT:\t%f', TIME_LOG_BASE)
logging.info('BIRNEST NO. OF CLUSTERS:\t%f', K)

# Logging Topic modelling parameters

logging.info('--------TOPIC MODELLING CONSTANTS--------')
logging.info('TOPIC MODELLING FILE:\t%s', TOPICS)
logging.info('TOTAL TOPICAL BINS:\t%s', T_B)





# Read the graph file

logging.info('Loading GRAPH')
FILE = GRAPH
G = nx.read_gpickle(FILE)

logging.info('GRAPH loaded')





# Accumulate all Tweets and Users by their Tweet/User IDs
T, U = bipartite.sets(G)

T = list(T)
U = list(U)





# print(len(T),len(U))




tweet_neighbours = pd.DataFrame({'tweetID' : T})
user_neighbours = pd.DataFrame({'userID' : U})





# Dataframes for tweets and users
tweets = pd.DataFrame({'tweetID' : T})
users = pd.DataFrame({'userID' : U})






# Dataframe to store edge connectivity
# Rationale: Pandas is easier and faster to query
edges = nx.to_pandas_edgelist(G, source='tweetID', target='userID')

# edges.head(20) 





# BIRDNEST Called
logging.info('EXTRACTING BIRDNEST DATA')
# u_df, t_df = birdnest_detect(DATA_USERS, DATA_TWEETS, TIME_LOG_BASE)
u_df = pd.read_csv(BN_USER_DF)
t_df = pd.read_csv(BN_TWEETS_DF)
logging.info('BIRDNEST DATA EXTRACTED')



# Handling topic modelling factors here

topic_df = pd.read_csv(TOPICS, index_col=0)
topic_df['simScore'] = (topic_df['simScore'] - topic_df['simScore'].min()) / (topic_df['simScore'].max()                                                                               - topic_df['simScore'].min())



# Append it to the dataframes
tweets = pd.merge(tweets, t_df, on='tweetID')
# tweets.head()





tweets["score_T"] = pd.Series(tweets['pi_T'].values, index=tweets.index)





users = pd.merge(users, u_df, on='userID')
users["score_U"] = pd.Series(users['pi_U'].values, index=users.index)
users = pd.merge(users, topic_df, on='userID', how = 'left')



users = users.fillna(value=1)





# Add number of user edges connected to a tweet
num_user_edges = pd.value_counts(edges['tweetID'].values).reset_index()
num_user_edges.columns = ['tweetID', 'num_user_edges']
tweets = pd.merge(tweets, num_user_edges, how='left', on='tweetID')


# Add number of tweet edges connected to a user
num_tweet_edges = pd.value_counts(edges['userID'].values).reset_index()
num_tweet_edges.columns = ['userID', 'num_tweet_edges']
users = pd.merge(users, num_tweet_edges, how='left', on='userID')
# users.head()





# nans = lambda df: df[df.isnull().any(axis=1)]
# nans(users).shape
logging.info('ALL DATAS LOADED')
logging.info('NUMBER OF USERS:\t%d', users.shape[0])
logging.info('NUMBER OF TWEETS:\t%d', tweets.shape[0])

cs_score_U = users['score_U'].mean()
cs_score_T = tweets['score_T'].mean()





# Dataframes to keep track of the score differences between iterations

diff_U = pd.Series(float(sys.maxsize), index=users.index, name='diff_U')
diff_T = pd.Series(float(sys.maxsize), index=tweets.index, name='diff_T')





# Read annotation file and attach it to the users dataframe

labels_u = pd.read_csv(ANNO_USERS, index_col=0)
# users = pd.merge(users, labels_u[["userID", "label"]], on="userID", how="left")
labels_t = pd.read_csv(ANNO_TWEETS, index_col=0)




train = None
test = None
if ANALYSIS == True:
    
    train, test = train_test_split(labels_u, train_size=LABEL_KNOWN_FRAC, stratify=labels_u['label'], shuffle=True)
    users = pd.merge(users, train[["userID", "label"]], on="userID", how="left")
    users['label'] = users['label'].fillna(-1)

else:
    
    users = pd.merge(users, labels_u[["userID", "label"]], on="userID", how="left")

tweets = pd.merge(tweets, labels_t[['tweetID', 'label']], on='tweetID', how='left')





epoch = 1

while max(diff_U.max(), diff_T.max()) > EPSILON:
    
    logging.info('-----------EPOCH %d STARTING-----------', epoch)
    
    # Handle the tweet score updates
    t_score_prev = tweets["score_T"]
    
    edges = pd.merge(edges, users[['userID','score_U']], on='userID', how='left')

    edges['user_factor'] = edges['score_U'] * edges['weight'].astype('float64').map({0.5: 0.75, 0.75: 0.75})

    t_user_weights = edges.groupby(['tweetID']).sum().reset_index()

    # Clean the edgelist

    edges = edges.drop(columns=['user_factor', 'score_U'])

    # Reorder the user factors by ```tweetID```

    t_user_weights = t_user_weights.set_index('tweetID')

    t_user_weights = t_user_weights.reindex(index=tweets['tweetID'])

    t_user_weights = t_user_weights.reset_index()['user_factor']
    
    logging.info('EPOCH %d: CALCULATING CURRENT SCORE FOR TWEETS', epoch)
    
    t_score_cur = None
        
    if VERSION == 1:
        t_score_cur = ((GAMMA_SEED_T * tweets['pi_T']) + (GAMMA_USER_T * t_user_weights))/(GAMMA_SEED_T + GAMMA_USER_T + tweets['num_user_edges'])
        
    elif VERSION == 2:
        t_score_cur = ((GAMMA_SEED_T * tweets['pi_T']) + (GAMMA_USER_T * t_user_weights) + (CS_SCORE_T * cs_score_T))/        (GAMMA_SEED_T + GAMMA_USER_T + tweets['num_user_edges'] + CS_SCORE_T)
        
    elif VERSION == 3:
        t_score_cur = ((GAMMA_SEED_T * tweets['pi_T']) + (GAMMA_USER_T * t_user_weights) + (CS_SCORE_T * cs_score_T) + ( tweets['label'].map({0: COLLUSIVE_VAL_T, 1: GENUINE_VAL_T, -1: UNLABELLED_VAL_T})))/        (GAMMA_SEED_T + GAMMA_USER_T + tweets['num_user_edges'] + CS_SCORE_T )
        

    
    logging.info('EPOCH %d: CURRENT SCORE FOR TWEETS CALCULATED', epoch)
    
    # Updating the diff series for Tweets
    
    logging.info('EPOCH %d: UPDATING SCORE DIFF. FOR TWEETS', epoch)
    
    diff_T = t_score_cur - t_score_prev
    
    logging.info('EPOCH %d: SCORE DIFF. FOR TWEETS CALCULATED', epoch)
    
    # Updating the tweets dataframe
    
    t_temp_df = pd.DataFrame({'score_T' : t_score_cur})
    
    tweets.update(t_temp_df)
    
    logging.info('EPOCH %d: TWEETS DATAFRAME UPDATED WITH NEW SCORE', epoch)
    
    # Handle the user score updates
    
    u_score_prev = users["score_U"]
    
    edges = pd.merge(edges, tweets[['tweetID','score_T']], on='tweetID', how='left')

    edges['tweet_factor'] = edges['score_T'] * edges['weight'].astype('float64').map({0.5: 0.75, 0.75: 0.75})

    u_tweet_weights = edges.groupby(['userID']).sum().reset_index()

    # Clean the edgelist

    edges = edges.drop(columns=['tweet_factor', 'score_T'])

    # Reorder the user factors by ```tweetID```

    u_tweet_weights = u_tweet_weights.set_index('userID')

    u_tweet_weights = u_tweet_weights.reindex(index=users['userID'])

    u_tweet_weights = u_tweet_weights.reset_index()['tweet_factor']
    
#     u_tweet_weights = users['userID'].apply(lambda x: user_neighbour_score(x, edges, tweets))
    
    logging.info('EPOCH %d: CALCULATING CURRENT SCORE FOR USERS', epoch)
    
    u_score_cur = None
        
    if VERSION == 1:
        u_score_cur = ((GAMMA_SEED_U * users['pi_U']) + (GAMMA_BIN_U * users['simScore']) + (GAMMA_TWEET_U * u_tweet_weights)) / (GAMMA_BIN_U + GAMMA_SEED_U + GAMMA_TWEET_U + users['num_tweet_edges'])
    elif VERSION == 2:
        u_score_cur = ((GAMMA_SEED_U * users['pi_U']) + (GAMMA_BIN_U * users['simScore']) + (GAMMA_TWEET_U * u_tweet_weights) + (CS_SCORE_U * cs_score_U)) / (GAMMA_BIN_U + GAMMA_SEED_U + GAMMA_TWEET_U + users['num_tweet_edges'] + CS_SCORE_U)
    elif VERSION == 3:
        u_score_cur = ((GAMMA_SEED_U * users['pi_U']) + (GAMMA_BIN_U * users['simScore']) + (GAMMA_TWEET_U * u_tweet_weights) + (CS_SCORE_U * cs_score_U) +    (  users['label'].map({0: COLLUSIVE_VAL_U, 1: GENUINE_VAL_U, -1:UNLABELLED_VAL_U}))) / (GAMMA_BIN_U + GAMMA_SEED_U + GAMMA_TWEET_U + users['num_tweet_edges'] + CS_SCORE_U )

    logging.info('EPOCH %d: CURRENT SCORE FOR USERS CALCULATED', epoch)
    
    # Updating the diff series for users
    
    logging.info('EPOCH %d: UPDATING SCORE DIFF. FOR USERS', epoch)
    
    diff_U = u_score_cur - u_score_prev
    
    logging.info('EPOCH %d: SCORE DIFF. FOR USERS CALCULATED', epoch)
    
    # Updating the users dataframe
    
    u_temp_df = pd.DataFrame({'score_U' : u_score_cur})
    
    users.update(u_temp_df)
    
    logging.info('EPOCH %d: USERS DATAFRAME UPDATED WITH NEW SCORE', epoch)
    
    logging.info('EPOCH %d: MAX SCORE DIFF. OF USERS\t:\t%f ', epoch , diff_U.max())
    logging.info('EPOCH %d: MAX SCORE DIFF. OF TWEETS\t:\t%f ', epoch , diff_T.max())
    logging.info('EPOCH %d: EPSILON\t\t:\t\t%f ', epoch , EPSILON)
    
    logging.info('EPOCH %d: MAX DIFF. TO BE COMPARED:\t%f', epoch, max(diff_U.max(), diff_T.max()))
                 
    if max(diff_U.max(), diff_T.max()) < EPSILON:
                 
        logging.info('CONVERGENCE REACHED. ALGORITHM TERMINATING.')
    
                 
    logging.info('-----------EPOCH %d ENDED-----------', epoch)
    
    epoch+=1





tweets.sort_values('score_T').to_csv("results/scores_unsup_tweets_"+ curr_time+".csv", mode="a+")
users.sort_values('score_U').to_csv("results/scores_unsup_users_"+ curr_time+".csv", mode="a+")

logging.info('-----------FILES WRITTEN-----------')


