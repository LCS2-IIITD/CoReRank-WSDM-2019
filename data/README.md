# Data files 

## Description

- ```anonymized_graph.gpickle``` : Bipartite graph of users and tweets. For details of construction please refer to our paper.
- ```annotated_tweets_anonymized.csv``` : Manually annotated tweets with TweetIDs replaced for anonymity.
	- ```0``` : means that the tweet was mined from a Blackmarket service
	- ```1``` : means that the tweet was not mined from a Blackmarket service
- ```annotated_users_anonymized.csv``` : Manually annotated users with UserIDs replaced for anonymity.
	- ```0``` : means that the user had submitted a tweet to a Blackmarket service or have been examined by manual annotators and marked as __'collusive'__
	- ```1``` : means that the user was a followee of a verified user in our dataset or have been examined by manual annotators and marked as __'genuine'__
- ```birdnest_tweets_data_anonymized.csv``` : ```Birdnest``` scores for the tweets in the graph
- ```birdnest_users_data_anonymized.csv``` : ```Birdnest``` scores for users in the graph
- ```sim_df_anonymized.csv``` : Topical similarity scores for users in the graph

