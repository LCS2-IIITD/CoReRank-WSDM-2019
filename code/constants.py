import numpy as np

# Algorithm Version

# 1 -> Does not include cold start treatment
# 2 -> Includes cold start treatment with Version 1
# 3 -> Semi- supervised

VERSION = 2

# Main Algorithm Parameters

GRAPH = "<ENTER PATH TO GRAPH>"


GAMMA_SEED_T = 0.6
GAMMA_USER_T = 0.6
CS_SCORE_T = 0.3

GAMMA_SEED_U = 0.6
GAMMA_TWEET_U = 0.6
GAMMA_BIN_U = 3
CS_SCORE_U = 0.3

EPSILON = 0.000001

# Semi-supervised parameters

GENUINE_VAL_U = 100
COLLUSIVE_VAL_U = -100
GENUINE_VAL_T = 100
COLLUSIVE_VAL_T = -100
UNLABELLED_VAL_U = 0
UNLABELLED_VAL_T = 0



# BIRDNEST Parameters

BN_USER_DF = "<ENTER PATH TO BIRDNEST DATA OF USERS>"
BN_TWEETS_DF = "<ENTER PATH TO BIRDNEST DATA OF TWEETS>"
TIME_LOG_BASE = 10
K = 2

# Topic Modelling Parameters

TOPICS = "<ENTER PATH TO SIMILARITY SCORES OF USERS>"

# Annotation Files

ANNO_USERS = "<ENTER PATH TO USER ANNOTATION>"
ANNO_TWEETS = "<ENTER PATH TO TWEET ANNOTATION>"


# FOR EXPERIMENTATION

gamma_seed__T = np.arange(0, 3, 1).tolist()
gamma_user__T = np.arange(0, 3, 1).tolist()
gamma_cs__T = np.arange(0, 3, 1).tolist()

gamma_seed__U = np.arange(0, 3, 1).tolist()
gamma_tweet__U = np.arange(0, 3, 1).tolist()
gamma_cs__U = np.arange(0, 3, 1).tolist()
gamma_bin__U = np.arange(0, 3, 1).tolist()



ANALYSIS_K = 10

# FOR ANALYSIS

ANALYSIS = False
LABEL_KNOWN_FRAC = 1
