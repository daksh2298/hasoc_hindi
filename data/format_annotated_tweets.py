import json
import sqlite3
import copy
import json


def conn_db():
    return sqlite3.connect('../hasoc.db', check_same_thread=False)


conn = conn_db()
cursor = conn.cursor()


def get_single_annots(data=None):
    query = 'SELECT * FROM annoted_tweets'
    cursor.execute(query)
    rows = cursor.fetchall()
    # print(len(rows))
    new_data = []
    data = []
    for row in rows:
        temp = list(row)
        data.append(temp)
    for li in data:
        l = [item for item in li if item is not None]
        if len(l) == 5:
            new_data.append(l)
    # print(len(new_data))
    return new_data


def reset_json(file):
    file_ptr = open(file)
    data = json.loads(file_ptr.read())
    print(data)
    file_ptr.close()
    print(len(data))
    for user in data:
        data[user]['annoted_count'] = 0
        data[user]['annoted_tweets'] = []
        data[user]['last_updated'] = None
        data[user]['reported_count'] = 0
        data[user]['reported_tweets'] = []
        data[user]['start_end'] = [0, 0]
        data[user]['to_be_annotated'] = []
        data[user]['total_assigned'] = 0
    file_ptr = open(file, 'w')
    data = json.dumps(data, indent=4)
    print(data)
    file_ptr.write(data)
    file_ptr.close()


# file_ptr=open('merge.json')
# data=json.load(file_ptr)
# print(len(data))
def get_active_users():
    query = 'SELECT username from users WHERE active=1'
    cursor.execute(query)
    users = cursor.fetchall()
    users = [user[0] for user in users]
    return users


def read_json(filename):
    file_ptr = open(filename)
    return json.load(file_ptr)


def get_split_dict(users, total_split):
    user_count = len(users)
    ind_split = round(total_split / user_count)
    split_dic = {}
    for user in users:
        split_dic[user] = ind_split
    # print(split_dic)
    return split_dic


def get_tweet_ids(data):
    ids = []
    for tweet in data:
        ids.append((tweet['id_str'], 0))
    return ids


def write_json(data, filename):
    write_data = json.dumps(data, indent=2)
    file_ptr = open(filename, 'w')
    file_ptr.write(write_data)
    file_ptr.close()
    return 'success'


def split_data():
    single_annots = get_single_annots()
    active_users = get_active_users()

    # print(active_users)
    if not single_annots:
        all_tweets = read_json('merge.json')[:7000]
        all_user_data = read_json('annoted_tweets.json')
        split_users = get_split_dict(active_users, len(all_tweets))
        ids = get_tweet_ids(all_tweets)
        assign_dict = dict(ids)
        print(len(assign_dict))
        for user in active_users:
            user_data = all_user_data[user]
            user_data['to_be_annotated'] = []
            for tweet in all_tweets:
                id_str = tweet['id_str']
                assigned_count = assign_dict[id_str]
                if split_users[user] > 0 and assigned_count < 1:
                    user_data['to_be_annotated'].append(id_str)
                    assign_dict[id_str] += 1
                    split_users[user] -= 1
            user_data['total_assigned'] = len(user_data['to_be_annotated'])
            print('Assigned {} to {}.'.format(user_data['total_assigned'], user))
        # all_assigned_check=[all_user_data[user]['to_be_annotated'] for user in all_user_data]
        all_assigned_check = []
        for user in all_user_data:
            all_assigned_check += all_user_data[user]['to_be_annotated']
        print(len(all_assigned_check))
        print(len(set(all_assigned_check)))
        if len(assign_dict) == len(set(all_assigned_check)):
            print('All tweets distributed successfully')

        write_json(all_user_data, 'annoted_tweets.json')


reset_json('annoted_tweets.json')
split_data()
