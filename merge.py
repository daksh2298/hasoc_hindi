import json
import os
import ast
import copy

def merge(has_replies=False):
    dir='data/'
    # files=os.listdir(dir)
    files=['#chaiwala OR chutiya.json','#modi.json','#pappu.json','mamta AND randi.json','#modi AND chutiya.json']
    # reply_id='reply_'
    merge=[]
    count=1
    count_replies=1
    count_files=1
    for file in files:
        # if file.startswith('#') or file.startswith('@'):
        file_ptr=open('{}{}'.format(dir,file))
        if file.startswith('@'):
            for line in file_ptr.readlines():
                tweet_dic={
                    'text':None,
                    'id_str':None
                }
                data=ast.literal_eval(line)
                tweet_dic['text']=data['tweet']
                tweet_dic['id_str']=data['tweet_id']
                merge.append(copy.deepcopy(tweet_dic))
                count+=1
                if len(data['replies']) and has_replies==True:
                    for reply in data['replies']:
                        tweet_dic['text'] = reply
                        tweet_dic['id_str']='reply_{}'.format(count_replies)
                        count_replies+=1
                        merge.append(copy.deepcopy(tweet_dic))
                else:
                    pass
        else:
            for line in file_ptr.readlines():
                tweet_dic={
                    'text':None,
                    'id_str':None
                }
                data=ast.literal_eval(line)
                tweet_dic['text']=data['tweet']
                tweet_dic['id_str']=data['tweet_id']
                merge.append(copy.deepcopy(tweet_dic))
                count+=1

        count_files+=1
        file_ptr.close()

    merge_file_ptr=open('merge_hindi.json','w')
    merge_file_ptr.write(json.dumps(merge,indent=4))
    merge_file_ptr.close()

    print('{} Merge File Length:- {} {}'.format('-*25',len(merge),'-'*25))
    print('{} Total Files:- {} {}'.format('-*25',count_files,'-'*25))
    print('{} Total tweets:- {} {}'.format('-*25',count,'-'*25))
    print('{} Total replies:- {} {}'.format('-*25',count_replies,'-'*25))
    print('{} Total individual tweets:- {} {}'.format('-*25',count+count_replies,'-'*25))


def load_json():
    file_ptr=open('merge.json')
    datas=json.loads(file_ptr.read())
    text=[data['id_str'] for data in datas]
    # print(len(set(text)))
    for t,d in zip(text,datas):
        if len(d['text'])==140:
            print(d['text'])
        if text.count(t) > 1:
            print(t)
            print(d['text'])
    print(len(text))

# load_json()
# merge(has_replies=False)
file_ptr=open('Data/merge_hindi.json')
data=json.load(file_ptr)
count=0
for row in data:
    row['lang']='hi'
file_ptr.close()
file_ptr=open('Data/merge_hindi.json','w')
file_ptr.write(json.dumps(data,indent=2))
file_ptr.close()
