import pandas as pd
import pdb
import sys
from collections import defaultdict
import random

from gensim.models import word2vec

#file_path = './test.txt'
file_path = sys.argv[1]
#just for testing purpose
TAIL_LIMIT = 5
HEAD_LIMIT = 100
MAX_RANK_ALLOWED = 5


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
        return -1


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
            while coNeg < 3*coPos:
                randomUrl = random.choice(head_keys)
                if randomUrl == urlKey:
                    continue
                headKey = random.choice(list(url_head_Dict[randomUrl].keys()))
                final_map.append([tailKey,headKey,0])
                coNeg += 1
    return final_map




# def separator(file_path):
#     log = pd.read_table(file_path)
#     print log.columns
#     ind=0
#     missing_clicks=pd.DataFrame(data=None, columns=log.columns)
#     head_tail_df = pd.DataFrame(data=None,columns=['Query','count','URL','ItemRank'] )
#     head_list = pd.DataFrame(data=None,columns=['Query','count','URL','ItemRank'] )
#     tail_list = pd.DataFrame(data=None,columns=['Query','count','URL','ItemRank'] )
#
#     for row in log.itertuples(index=False):
#
#         if pd.isnull(getattr(row,"ClickURL")) or getattr(row,"ItemRank")>MAX_RANK_ALLOWED: # Checkiing for the availabilty of url
#             missing_clicks=missing_clicks.append([row],ignore_index=True)
#             log.drop(log.index[ind])
#             continue
#
#         pos=head_tail_df.index[head_tail_df['Query'] == row[1]].tolist() #index for the query
#
#         if len(pos): #for increamenting the count of the query
#             head_tail_df.at[pos[0],head_tail_df.columns[1]]+=1
#             head_tail_df.at[pos[0],head_tail_df.columns[2]].append(getattr(row,"ClickURL")) #storing all urls visited at the given query
#             head_tail_df.at[pos[0],head_tail_df.columns[3]].append(getattr(row,"ItemRank"))
#         else: #adding new query
#             ins=[row[1],row[4],1]
#             head_tail_df=head_tail_df.append({'Query':row[1],'count':1,'URL':[getattr(row,"ClickURL")],'ItemRank':[getattr(row,"ItemRank")]},ignore_index=True)
#         ind+=1
#
#     for row in head_tail_df.itertuples(index=False):
#
#         # pdb.set_trace()
#         if row[1] < TAIL_LIMIT:
#             tail_list = tail_list.append({'Query':row[0],'count':row[1],'URL':row[2],'ItemRank':row[3]},ignore_index=True)
#         elif row[1] > HEAD_LIMIT:
#             head_list = head_list.append({'Query':row[0],'count':row[1],'URL':row[2],'ItemRank':row[3]},ignore_index=True)
#
#     return head_tail_df,missing_clicks,head_list,tail_list

# def getUrlList(head_list,tail_list):
#     url_list = defaultdict()
#     for row in head_list:
#
# def mapping(head_list,tail_list):


def main():
    global file_path

    

    # creating dexter client connection
    

    head_list,tail_list,url_head_Dict,url_tail_Dict = tryNew(file_path)
    maps = mapping(head_list,tail_list,url_head_Dict,url_tail_Dict)
    for row in maps:
        print row[0],',',row[1],',',row[2]

    #cosine_similarity(headQuery,tailQuery,model)
    # head_tail_df,missing_clicks,head_list,tail_list = separator(file_path)
    # print head_list
    # print "taillist now"
    # print tail_list
    # print len(head_list),len(tail_list),len(head_tail_df),len(missing_clicks)


if __name__ == "__main__":
    main()
