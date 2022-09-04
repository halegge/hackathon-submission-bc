from flask import Flask, render_template, jsonify, request
from spacy.tokens import Doc
from networkx.classes.ordered import MultiGraph
# Just going to make imports etc here for now, will combine later :-)
import json
import os
import requests
import spacy
import networkx as nx
#import pydot
from collections import Counter
import pandas as pd
from datetime import datetime
from requests.exceptions import RequestException
from urllib.parse import quote_plus

_BING_KEY = ""
_BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

SEARCH_KEY = ""
SEARCH_ID = ""
COUNTRY = "uk"    #this could be changed or redone with other countries
SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&num=10&gl=" + COUNTRY
RESULT_COUNT = 20   #this will mean that we technically only get 50 searches

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def search_api(query, pages=int(RESULT_COUNT/10)):
    '''queries custom search API end point and returns search results'''
    results = []
    
    for i in range(0, pages):
        start = i*10+1  #rank fist record on page returned (1,11...)
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            query=quote_plus(query),    #ensures query is properly (URL) formatted
            start=start
        )
        response = requests.get(url)
        data = response.json()
        results += data["items"]    #returns list of dicts

    res_df = pd.DataFrame.from_dict(results)
    res_df["rank"] = list(range(1, res_df.shape[0] + 1))
    res_df = res_df[["link", "rank", "snippet", "title"]]
    return res_df
    
def read_local_google_query():
    return pd.read_csv("test_data/gResults.csv")

def request_constructor(query: str, mkt: str = "en-gb") -> dict: # builds the request for the send_request function
    return {'q': query, 'mkt': mkt}, {'Ocp-Apim-Subscription-Key': _BING_KEY}

def send_request(params: dict, headers: dict) -> dict: # sends request and returns the JSON response
    response = requests.get(_BING_ENDPOINT, headers=headers, params=params)
    return response.json()

def is_valid_noun(stringToken: Doc) -> bool: # checks if a token object is a proper noun/noun +3 chars in length
    if (stringToken.pos_ == "PROPN" or stringToken.pos_ == "NOUN") and len(stringToken.text) > 3:
        return True
    else:
        return False

def return_keyword_sets(jsonInput: dict) -> dict: # takes json and returns dict of lists containing keywords for every search result (10 results)
    resultsKeywords = {}
    for page in jsonInput['webPages']['value']:
        keywords = [x.lemma_.lower() for x in list(filter(is_valid_noun, nlp(page['snippet'])))]
        resultsKeywords[page['url']] = keywords
    return resultsKeywords

def results_formatter(strippedQuery: str, keywordSets: dict, source: str) -> dict: # adds counts for keyword hits and formats the dicts for the graph later
    source_lookup = {"google": "G-", "bing": "B-"}
    for count, url in enumerate(keywordSets):
        score = 0
        counts = dict(Counter(keywordSets[url]))
        keywords = keywordSets[url]
        for token in strippedQuery:
            if token in counts:
                score += counts[token]
        keywordSets[url] = (source_lookup[source] + str(count), "keyword hits against query", score, keywords)
    return keywordSets

def construct_graph(graphData: dict) -> MultiGraph: 
    ''' 
        So the deal here is that graph G = (V,E) where V is the set of vertices/nodes and E is the set of edges
        Now since V is implied by E I just produce E which is why you don't see explicit node instantiation :)

        Nodes are the results, edges are shared keywords. Produced by: for each result, go through every other
          result and do a set intersection on their keywords, for each item in the resulting intersection
          produce an edge between the two results

        Love a good graph sometimes, now I just need to label the edges and colour code the nodes
    '''
    G = nx.MultiGraph()
    for search_result in graphData:
        for other_result in graphData:
            if search_result == other_result:
                pass
            else:
                currentSet = set(graphData[search_result][3])
                otherSet = set(graphData[other_result][3])
                sharedKeywords = currentSet.intersection(otherSet)
                for edge in sharedKeywords:
                    G.add_edge(graphData[search_result][0], graphData[other_result][0], word = edge)
    return G

def return_keyword_sets_google(dfInput):
    googleSearchDict = {}
    for index, row in dfInput.iterrows():
        rowKeywords = [x.lemma_.lower() for x in list(filter(is_valid_noun, nlp(row['snippet'])))]
        googleSearchDict[row['link']] = rowKeywords
    return googleSearchDict

@app.route("/")
def hello_world():
	return render_template("index.html")
    
@app.route("/local_test_query")
def local_test_query():
    query = request.args.get("query")
    strippedQuery = [word.text for word in nlp(query) if word.text not in nlp.Defaults.stop_words]
    apiResponse = send_request(*request_constructor(query))
    results = return_keyword_sets(apiResponse)
    formattedResults = results_formatter(strippedQuery, results, "bing")
    
    google_results = return_keyword_sets_google(read_local_google_query())
    googleFormattedResults = results_formatter(strippedQuery, google_results, "google")
    
    return jsonify({**googleFormattedResults, **formattedResults})
    