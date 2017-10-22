import pandas as pd
import pdb
import sys

#file_path = './test.txt'
file_path = sys.argv[1]
#just for testing purpose
TAIL_LIMIT = 2
HEAD_LIMIT = 5
MAX_RANK_ALLOWED = 5

def separator(file_path):
    log = pd.read_table(file_path)
    print log.columns
    ind=0
    missing_clicks=pd.DataFrame(data=None, columns=log.columns)
    head_tail_df = pd.DataFrame(data=None,columns=['Query','count','URL','ItemRank'] )
    head_list = pd.DataFrame(data=None,columns=['Query','count','URL','ItemRank'] )
    tail_list = pd.DataFrame(data=None,columns=['Query','count','URL','ItemRank'] )

    for row in log.itertuples(index=False):

        if pd.isnull(getattr(row,"ClickURL")) or getattr(row,"ItemRank")>MAX_RANK_ALLOWED: # Checkiing for the availabilty of url
            missing_clicks=missing_clicks.append([row],ignore_index=True)
            log.drop(log.index[ind])
            continue

        pos=head_tail_df.index[head_tail_df['Query'] == row[1]].tolist() #index for the query

        if len(pos): #for increamenting the count of the query
            head_tail_df.at[pos[0],head_tail_df.columns[1]]+=1
            head_tail_df.at[pos[0],head_tail_df.columns[2]].append(getattr(row,"ClickURL")) #storing all urls visited at the given query
            head_tail_df.at[pos[0],head_tail_df.columns[3]].append(getattr(row,"ItemRank"))
        else: #adding new query
            ins=[row[1],row[4],1]
            head_tail_df=head_tail_df.append({'Query':row[1],'count':1,'URL':[getattr(row,"ClickURL")],'ItemRank':[getattr(row,"ItemRank")]},ignore_index=True)
        ind+=1

    for row in head_tail_df.itertuples(index=False):

        # pdb.set_trace()
        if row[1] < TAIL_LIMIT:
            tail_list = tail_list.append({'Query':row[0],'count':row[1],'URL':row[2],'ItemRank':row[3]},ignore_index=True)
        elif row[1] > HEAD_LIMIT:
            head_list = head_list.append({'Query':row[0],'count':row[1],'URL':row[2],'ItemRank':row[3]},ignore_index=True)

    return head_tail_df,missing_clicks,head_list,tail_list

def main():
    global file_path
    head_tail_df,missing_clicks,head_list,tail_list = separator(file_path)
    print head_list
    print "taillist now"
    print tail_list
    print len(head_list),len(tail_list),len(head_tail_df),len(missing_clicks)


if __name__ == "__main__":
    main()
