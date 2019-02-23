[![HitCount](http://hits.dwyl.io/LCS2-IIITD/CoReRank-WSDM-2019.svg)](http://hits.dwyl.io/LCS2-IIITD/CoReRank-WSDM-2019)
# CoReRank: Ranking to Detect Users Involved in Blackmarket-based Collusive Retweeting Activities

This is the code and the dataset for the paper titled 

>[CoReRank: Ranking to Detect Users Involved in Blackmarket-based Collusive Retweeting Activities. *Aditya Chetan\*, Brihi Joshi\*, Hridoy Sankar Dutta\*, Tanmoy Chakraborty*](https://dl.acm.org/citation.cfm?id=3291010)

accepted at [The Twelfth ACM International Conference on Web Search and Data Mining (WSDM’19), February 11--15, 2019, Melbourne, VIC, Australia](http://www.wsdm-conference.org/2019/).

If you end up using this code or the data, please cite our paper: 

```
@inproceedings{Chetan:2019:CRD:3289600.3291010,
 author = {Chetan, Aditya and Joshi, Brihi and Dutta, Hridoy Sankar and Chakraborty, Tanmoy},
 title = {CoReRank: Ranking to Detect Users Involved in Blackmarket-Based Collusive Retweeting Activities},
 booktitle = {Proceedings of the Twelfth ACM International Conference on Web Search and Data Mining},
 series = {WSDM '19},
 year = {2019},
 isbn = {978-1-4503-5940-5},
 location = {Melbourne VIC, Australia},
 pages = {330--338},
 numpages = {9},
 url = {http://doi.acm.org/10.1145/3289600.3291010},
 doi = {10.1145/3289600.3291010},
 acmid = {3291010},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {blackmarket, collusion, online social networks, retweets, twitter},
}
```

# Quick Start

## Requirements

- Python 3.5.x
To install the dependencies used in the code, you can use the __requirements.txt__ file as follows -

```
pip install -r requirements.txt
```

## Running the code

First ```cd code``` and then run the ```corerank.py``` as follows - 

```
python corerank.py
```
This will generate rankings for the tweets and users present in the Graph as present in the paper.
Provide appropriate paths for data files and parameters in ```constants.py```.

# Contact

If you face any problem in running this code, you can contact us at aditya16217\[at\]iiitd\[dot\]ac\[dot\]in or brihi16142\[at\]iiitd\[dot\]ac\[dot\]in or hridoyd\[at\]iiitd\[dot\]ac\[dot\]in

# License 

Copyright (c) 2019 Aditya Chetan, Brihi Joshi, Hridoy Sankar Dutta, Tanmoy Chakraborty

For license information, see [LICENSE](LICENSE) or http://mit-license.org
