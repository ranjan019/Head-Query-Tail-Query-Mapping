import pandas as pd
import pdb
import sys
from collections import defaultdict
import random

from gensim.models import word2vec
import pydexter

#file_path = './test.txt'
file_path = sys.argv[1]
#just for testing purpose
TAIL_LIMIT = 5
HEAD_LIMIT = 150
MAX_RANK_ALLOWED = 3

def calcJaccard(list1,list2):
    s1=set(list1)
    s2=set(list2)
    inters=s1.intersection(s2)
    uni=s1.union(s2)
    return float(len(inters))/len(uni)


def tryNew(file_path):
    log = pd.read_table(file_path)
    query_Dict = defaultdict(int)
    url_Dict = defaultdict(lambda : defaultdict(int))
    url_head_Dict = defaultdict(lambda : defaultdict(int))
    url_tail_Dict = defaultdict(lambda : defaultdict(int))
    head_list = set()
    tail_list = set()
    for row in log.itertuples(index=False):
        if pd.isnull(getattr(row,"ClickURL")): # Checkiing for the availabilty of url
            continue
        query = getattr(row,"Query").lower()
        url = getattr(row,"ClickURL")
        rank = getattr(row,"ItemRank")
        query_Dict[query] += 1
        url_Dict[url][query] = rank

    for key in query_Dict.keys():
        if query_Dict[key] > HEAD_LIMIT :
            head_list.add(key)
        elif query_Dict[key] < TAIL_LIMIT :
            tail_list.add(key)
    for key in url_Dict.keys():
        for queryKey in url_Dict[key].keys():
            if queryKey in head_list :# and queryKey not in tail_list :
                url_head_Dict[key][queryKey] = url_Dict[key][queryKey]
            elif queryKey in tail_list:
                url_tail_Dict[key][queryKey] = url_Dict[key][queryKey]
    return head_list,tail_list,url_head_Dict,url_tail_Dict

#complete this function
def findScore(rankTail,rankHead):
    if rankTail<=5 and rankHead<=5:
        return 1
    else:
        return 0


def mapping(head_list,tail_list,url_head_Dict,url_tail_Dict):
    final_map = []
    head_keys = list(url_head_Dict.keys())
    tail_keys = list(url_tail_Dict.keys())
    for urlKey in url_tail_Dict.keys():
        coNeg = 0
        coPos = 0
        for tailKey in url_tail_Dict[urlKey].keys():
            for headKey in url_head_Dict[urlKey].keys():
                score = findScore(url_tail_Dict[urlKey][tailKey],url_head_Dict[urlKey][headKey])
                final_map.append([tailKey,headKey,score])
                if score==1:
                    coPos += 1
                else:
                    coNeg += 1
            while coNeg < coPos:
                randomUrl = random.choice(head_keys)
                if randomUrl == urlKey:
                    continue
                headKey = random.choice(list(url_head_Dict[randomUrl].keys()))
                final_map.append([tailKey,headKey,0])
                coNeg += 1
    return final_map

def main():
    global file_path
    head_list,tail_list,url_head_Dict,url_tail_Dict = tryNew(file_path)
    f = open('head.txt','w')
    for key in head_list:
        f.write(key)
    f.close()
    f = open('tail.txt','w')
    for key in tail_list:
        f.write(key)
    f.close()
    maps = mapping(head_list,tail_list,url_head_Dict,url_tail_Dict)
    f = open('mapping.txt','w')
    for row in maps:
        r = row[0],',,',row[1],',,',row[2]
        f.write(r)
    f.close()


if __name__ == "__main__":
    main()
