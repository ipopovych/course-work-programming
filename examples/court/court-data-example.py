# This is an example of court api usage
# This module gets data from court API and stores it
# as a dictionary and a list of judgment decisions


# To use this you need to have OpenDataBot API key: http://docs.opendatabot.com/#/v2

import json
from urllib.request import urlopen

keyword = 'OLX'  # search for court decisions that contain this word
sort_param = 'doc_id'
api_key = 'YOUR_API_KEY'  # OpenDataBot Court API Key

docs = json.load(urlopen('http://court.opendatabot.com/api/v1/court?text={}&sort={}&apiKey={}'.format(keyword, sort_param, api_key)))


doc_ids = [doc['doc_id'] for doc in docs['items']]

judgments = {}
for id in doc_ids:
    f = json.load(urlopen('http://court.opendatabot.com/api/v1/court/{}&apiKey={}'.format(id, api_key)))
    judgments[id] = f

decision_texts = [judgments[id]['text'] for id in judgments.keys()]  # a list of court decisions


#print(len(decision_texts))
#print(decision_texts[1])