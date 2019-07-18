from project.com.dao import conn_db
import json
import copy
from project.com.controller.tweetController import read_json

conn = conn_db()
cursor=conn.cursor()
def conn_commit(conn):
    conn.commit()
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
    # print(data)
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
    # print(data)
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


def get_tweet_ids(data,annotated=None):
    ids = []
    for tweet in data:
        ids.append((tweet['id_str'], 0))
    ids=dict(ids)
    count_all=0
    count_1=0
    count_2=0
    if type(annotated)==list and len(annotated):
        # temp=[]
        all_user_data = read_json('data/annoted_tweets.json')
        assigned_list=[]
        for user in all_user_data:
            assigned_list+=all_user_data[user]['to_be_annotated']
        for tweet_id in assigned_list:
            count_all+=1
            ids[tweet_id]+=1
            if ids[tweet_id]==1:
                count_1+=1
            elif ids[tweet_id]==2:
                count_2+=1
            else:
                pass
        # for row in annotated:
        #     count_all+=1
        #     temp=[col for col in row if col]
        #     if len(temp)==5:
        #         ids[temp[1]]=1
        #         count_1+=1
        #     elif len(temp)==6:
        #         ids[temp[1]] = 2
        #         count_2+=1
        #     else:
        #         pass
        print('count_1:- {}\tcount_2:- {}\tcount_all:- {}'.format(count_1,count_2,count_all))

    return ids


def write_json(data, filename):
    write_data = json.dumps(data, indent=2)
    file_ptr = open(filename, 'w')
    file_ptr.write(write_data)
    file_ptr.close()
    return 'success'


def split_data(new_reg=None,user=None):
    if new_reg:
        all_tweets = read_json('data/merge.json')[:7000]
        static_assigned=user.assigned
        to_be_assigned=int(user.assigned)
        all_user_data = read_json('data/annoted_tweets.json')
        single_annots = get_single_annots()
        ids = get_tweet_ids(all_tweets,single_annots)
        assign_dict=ids
        user_data = all_user_data[user.username]
        user_data['to_be_annotated'] = []
        for tweet in all_tweets:
            id_str = tweet['id_str']
            assigned_count = assign_dict[id_str]
            # print(assign_dict)
            if to_be_assigned > 0 and assigned_count < 2:
                user_data['to_be_annotated'].append(id_str)
                assign_dict[id_str] += 1
                to_be_assigned -= 1
        user_data['total_assigned'] = len(user_data['to_be_annotated'])
        print('Assigned {} to {}.'.format(user_data['total_assigned'], user.username))
        if user_data['total_assigned']==static_assigned:
            print('Successfully assigned new tweets to the user')
        write_json(all_user_data, 'data/annoted_tweets.json')
        return 'success'
    else:
        single_annots = get_single_annots()
        active_users = get_active_users()

        # print(active_users)
        if not single_annots:
            all_tweets = read_json('merge.json')[:7000]
            all_user_data = read_json('annoted_tweets.json')
            split_users = get_split_dict(active_users, len(all_tweets))
            ids = get_tweet_ids(all_tweets)
            assign_dict = ids
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

            write_json(all_user_data, 'data/annoted_tweets.json')



class loginDAO:
    def login_user(self, user):
        # cursor = conn.cursor()
        query="SELECT * FROM users WHERE username='{}'".format(user.username)
        cursor.execute(query)
        data = cursor.fetchall()
        # print(data)
        conn.commit()
        # cursor.close()
        # conn.close()
        return data

    def get_active_users(self):
        # cursor = conn.cursor()
        query = 'SELECT username from users WHERE active=1'
        cursor.execute(query)
        users = cursor.fetchall()
        users = [user[0] for user in users]
        return users

    def reactivate_user(self,user):
        # cursor = conn.cursor()
        query = 'UPDATE users SET active=1 WHERE username="{}"'.format(user.username)
        cursor.execute(query)
        conn.commit()
        return 'success'

    def deactivate_user(self,user):
        # cursor = conn.cursor()
        query = 'UPDATE users SET active=0 WHERE username="{}"'.format(user.username)
        print(query)
        cursor.execute(query)
        conn.commit()
        return 'success'

class registerDAO:
    def do_necessary_changes(self, user):
        # cursor=conn.cursor()
        file_ptr = open('data/annoted_tweets.json')
        users = json.load(file_ptr)
        file_ptr.close()
        temp = copy.deepcopy(users['admin'])
        temp['annoted_count'] = 0
        temp['annoted_tweets'] = []
        temp['last_updated'] = None
        temp['reported_count'] = 0
        temp['reported_tweets'] = []
        temp['start_end'] = [0,0]
        temp['to_be_annotated'] = []
        temp['total_assigned'] = 0
        users[user.username] = temp
        file_ptr = open('data/annoted_tweets.json','w')
        data_dumped=json.dumps(users,indent=4)
        file_ptr.write(data_dumped)
        file_ptr.close()
        print('Json file updated')
        query="alter TABLE annoted_tweets add {} TEXT;".format(user.username)
        cursor.execute(query)
        # conn.commit()
        # cursor.close()
        print('database Updated')
        split_data(user=user,new_reg=True)
        conn_commit(conn)



    def register_user(self, user):
        # cursor = conn.cursor()
        query="INSERT INTO users (name,username,password) VALUES ('{}','{}','{}') ".format(user.name,user.username,user.password)
        cursor.execute(query)
        # data = cursor.fetchall()
        # print(data)
        # conn.commit()
        # cursor.close()
        # conn.close()
        return True

    def check_exists(self,user):
        # cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username='{}'".format(user.username))
        data = cursor.fetchall()
        conn.commit()
        # cursor.close()

        return data

