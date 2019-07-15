import json

# files = ['user_tweets_@Birdie51411736.json',
#          'user_tweets_@Der__Patriot.json',
#          'user_tweets_@Kuddelmuddel9.json',
#          'user_tweets_@MuellerBrigitt1.json',
#          'user_tweets_@SapereAudeDE.json']
#
replies_files = ['replies_user_tweets_@Birdie51411736.json.json',
                 'replies_user_tweets_@Der__Patriot.json.json',
                 'replies_user_tweets_@Kuddelmuddel9.json.json',
                 'replies_user_tweets_@MuellerBrigitt1.json.json',
                 'replies_user_tweets_@SapereAudeDE.json.json']
files=['#chaiwala OR chutiya.json','#modi.json','#pappu.json','mamta AND randi.json','#modi AND chutiya.json']
def merge_tweets():
    all_full_tweets=[]
    for file in files:
        file_ptr_tweets=open('data/'+file)
        tweets=json.load(file_ptr_tweets)
        if file =='#modi.json':
            all_full_tweets+=tweets[0:200]
        if file == '#chaiwala OR chutiya.json':
            all_full_tweets += tweets[0:70]
        else:
            all_full_tweets += tweets[0:40]
        print(file,len(all_full_tweets))

    all_tweets=[]
    try:
        for tweet in all_full_tweets:
            tweet_clean={}
            if tweet.get('full_text').startswith('RT'):
                full_text=tweet.get('retweeted_status').get('full_text')
                id_str=tweet.get('retweeted_status').get('id_str')
                tweet_clean['text']=full_text
                tweet_clean['id_str']=id_str
                tweet_clean['len']=len(full_text)
                all_tweets.append(tweet_clean)
            else:
                full_text = tweet.get('full_text')
                id_str = tweet.get('id_str')
                tweet_clean['text'] = full_text
                tweet_clean['id_str'] = id_str
                tweet_clean['len'] = len(full_text)
                all_tweets.append(tweet_clean)
    except Exception as e:
        print(e)
    finally:
        file_ptr_merge=open('merge_hindi_200.json','w')
        all_tweets_str=json.dumps(all_tweets,indent=4)
        file_ptr_merge.write(all_tweets_str)
        file_ptr_merge.close()
        file_ptr_tweets.close()

def fetch_id_updated(file):
    id_list=[]
    directory='./'
    fname=open(directory+file,'r')
    tweets=json.load(fname)
    for tweet in tweets:
        id_list.append(tweet.get('id_str'))
    fname.close()
    return id_list

def merge_replies():
    all_full_tweets=[]
    for file in replies_files:
        file_ptr_tweets=open(file)
        tweets=json.load(file_ptr_tweets)
        for tweet_id in tweets:
            all_full_tweets+=tweets[tweet_id]
        print(file,len(all_full_tweets))

    all_tweets=[]
    try:
        for tweet in all_full_tweets:
            tweet_clean={}
            if tweet.get('full_text').startswith('RT'):
                full_text=tweet.get('retweeted_status').get('full_text')
                id_str=tweet.get('retweeted_status').get('id_str')
                tweet_clean['text']=full_text
                tweet_clean['id_str']=id_str
                tweet_clean['len']=len(full_text)
                all_tweets.append(tweet_clean)
            else:
                full_text = tweet.get('full_text')
                id_str = tweet.get('id_str')
                tweet_clean['text'] = full_text
                tweet_clean['id_str'] = id_str
                tweet_clean['len'] = len(full_text)
                all_tweets.append(tweet_clean)
    except Exception as e:
        print(e)
    finally:
        file_ptr_merge=open('merge_replies.json','w')
        all_tweets_str=json.dumps(all_tweets,indent=4)
        file_ptr_merge.write(all_tweets_str)
        file_ptr_merge.close()
        file_ptr_tweets.close()

def merge_replies_tweets():
    file_ptr_replies=open('merge_replies.json')
    file_ptr_tweets=open('merge_new.json')

    tweets=json.load(file_ptr_tweets)
    replies=json.load(file_ptr_replies)

    file_ptr_merged=open('merge_final.json','w')
    data=tweets+replies
    dump_data=json.dumps(data,indent=4)
    file_ptr_merged.write(dump_data)
    file_ptr_merged.close()
    file_ptr_replies.close()
    file_ptr_tweets.close()


def fetch_id_list():
    file_ptr = open('merge_hindi_200.json')
    tweets=json.load(file_ptr)
    ids=[]
    for tweet in tweets:
        ids.append(tweet['id_str'])
    print(len(ids),len(set(ids)))
    file_ptr.close()
    set_ids=list(set(ids))
    unique_tweets=[]
    count=0
    for tweet in tweets:
        if tweet.get('id_str') in set_ids:
            unique_tweets.append(tweet)
            set_ids.remove(tweet.get('id_str'))
            count+=1
        else:
            pass
    print(count)
    print(len(unique_tweets))
    file_ptr=open('merge_hindi_200_final.json','w')
    file_ptr.write(json.dumps(unique_tweets,indent=4))
    file_ptr.close()


if __name__=='__main__':
    merge_tweets()
    fetch_id_list()