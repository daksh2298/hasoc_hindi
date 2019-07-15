import sqlite3
import copy
import json
def conn_db():
    return sqlite3.connect('hasoc.db', check_same_thread=False)
conn = conn_db()
cursor = conn.cursor()
query = 'SELECT * FROM annoted_tweets'
cursor.execute(query)
rows = cursor.fetchall()
new_data=[]
data=[]
for row in rows:
    temp=list(row)
    data.append(temp)
for li in data:
    l=[item for item in li if item is not None]
    if len(l)==5:
        new_data.append(l)
print(len(new_data))
# for i in range (0,2670)
#     dic['tweet_'+str(i)]=[dict()]
# fieldnames=['tweet_id','tweet', 'annotation','language']
# for lists in new_data:
#     dic=dict( zip( fieldnames, lists))
# print(dic)
# final=[]
# dic={}
# for lists in new_data:
#     dic["tweet_id"]=lists[1]
#     dic["tweet"]=lists[2]
#     dic["annotation"]=lists[3]
#     dic["lang"]=lists[4]
#     final.append(copy.deepcopy(dic))
# print(final)
# f=open("single_annotated_tweets.json", "w")
# json.dump(final, f, indent=4)
# f.close()