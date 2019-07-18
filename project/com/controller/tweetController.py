from flask import *
from project import app
from project.com.dao import conn_db
from project.com.vo.tweetVO import tweetVO
from project.com.dao.tweetDAO import tweetDAO
# from project.com.dao.loginDAO import loginDAO

import datetime
import copy

conn = conn_db()


def read_json(file):
    json_file = open(file)
    data = json_file.read()
    json_file.close()
    data_json = json.loads(data)
    return data_json


@app.route('/annot', methods=['POST', 'GET'])
def annot():
    if session.get('user'):
        tweetvo = tweetVO()
        tweetdao = tweetDAO()
        cursor = conn.cursor()
        data_json = read_json('data/annoted_tweets.json')
        annoted_tweet_ids = data_json[session['user']]['annoted_tweets']
        if request.method == 'POST':
            # annot=request.form.get('annot')
            tweet = request.form.get('tweet')
            tweet = tweet.replace('"', "'")
            # tweet='"hello"'
            id_str = request.form.get('id_str')
            task_1 = request.form.get('task_1')
            task_2 = request.form.get('task_2')
            # task_b=request.form.get('task_b')
            task_3 = request.form.get('task_3')
            lang = request.form.get('lang')
            row_no = request.form.get('row_no')
            if task_3 == None:
                task_3 = 'NULL'
            # print('task3',task_3)
            # print(task_1)
            # print(request.form)
            resp = '{}\t{}\t{}'.format(task_1, task_2, task_3)
            # print(resp)
            tweetvo.resp = resp
            tweetvo.tweet_id = id_str
            tweetvo.tweet = tweet
            tweetvo.lang = lang
            tweetvo.username = session['user']
            rows, db_status = tweetdao.check_exists(tweetvo)
            if rows == 0:
                # print('inside if')
                db_status = tweetdao.insert_annot(tweetvo)
            elif rows == 1:
                # print('inside elif')
                db_status = tweetdao.update_records(tweetvo)

            if db_status == True:
                annoted_tweet_ids.append(id_str)
                data_json[session['user']]['annoted_count']=len(annoted_tweet_ids)
                # print(rows)
                utc_now = datetime.datetime.utcnow()
                date_list = str(utc_now.date()).split('-')
                date = '-'.join(date_list[-1::-1])
                time = str(utc_now.time()).split('.')[0]
                # print(date, time)
                data_json[session['user']]['annoted_tweets'] = annoted_tweet_ids
                data_json[session['user']]['last_updated'] = {
                    "date": date,
                    "time": time
                }
                new_data = json.dumps(data_json, indent=4)
                json_file = open('data/annoted_tweets.json', 'w')
                json_file.write(new_data)
                json_file.close()
                # cursor.execute(query)
                conn.commit()
                resp = {'status': 'OK'}
                return json.dumps(resp)
            else:
                return 'database Failure'

        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/annotated_tweets')
def annotated_tweets():
    if session.get('user') == 'admin':
        return redirect(url_for('annotated_tweets_admin'))
    if session.get('user'):
        tweetvo = tweetVO()
        tweetdao = tweetDAO()
        user = session.get('user')
        tweetvo.username = user
        resp, rows_tup = tweetdao.get_annots(tweetvo)
        rows = []
        for i in range(len(rows_tup)):
            row = list(rows_tup[i])
            row[-1] = tuple(row[-1].split('\t'))
            rows.append(tuple(row))
        # print(rows)
        if resp == True:
            return render_template('view_annotated_tweets.html', rows=rows, error=None)
        else:
            return render_template('view_annotated_tweets.html', error=resp)
    else:
        return redirect(url_for('login'))


@app.route('/annotated_tweets_admin')
def annotated_tweets_admin():
    if session.get('user') == 'admin':
        # print('inside admin===============')
        tweetvo = tweetVO()
        tweetdao = tweetDAO()
        user = session.get('user')
        tweetvo.username = user
        data_json = read_json('data/annoted_tweets.json')
        active_users = tweetdao.get_active_users()
        # print(data_json)
        for user in data_json:
            if user in active_users:
                data_json[user]['active']=True
            else:
                data_json[user]['active']=False
        resp, annotated_tweets = tweetdao.get_annots_admin()
        if resp == True:
            # print('inside if true')
            for user in annotated_tweets:
                annots = annotated_tweets[user]
                labels = [annot[2] for annot in annots]
                task_1, task_2, task_3 = [label.split('\t')[0] for label in labels], [label.split('\t')[1] for label in
                                                                                      labels], [label.split('\t')[2] for
                                                                                                label in labels]
                # print('task 1',task_1)
                # print('task 2',task_2)
                # print('task 3',task_3)
                annotated_tweets[user].append({'HOF_COUNT': task_1.count('HOF'), 'NOT_COUNT': task_1.count('NOT'),
                                               'HATE_COUNT': task_2.count('HATE'), 'OFFN_COUNT': task_2.count('OFFN'),
                                               'PRFN_COUNT': task_2.count('PRFN'), 'UNT_COUNT': task_3.count('UNT'),
                                               'TIN_COUNT': task_3.count('TIN'), 'NULL_COUNT': task_3.count('NULL')})
            # print(annotated_tweets['german_1'][-1])
            return render_template('view_annotated_tweets_admin_graph.html', annotated_tweets_users=annotated_tweets,
                                   error=None, data_json=data_json)
        else:
            return render_template('view_annotated_tweets_admin_graph.html', error=resp)
    else:
        return redirect(url_for('login'))


@app.route('/annotated_tweets_admin/<user>')
def get_individual_annotator_log(user):
    if session.get('user') == 'admin':
        # print('inside admin indi')
        tweetvo = tweetVO()
        tweetdao = tweetDAO()
        # user = session.get('user')
        tweetvo.username = user
        resp, annotated_tweets = tweetdao.get_annots_admin()
        rows_tup = annotated_tweets[user]
        rows = []
        for i in range(len(rows_tup)):
            row = list(rows_tup[i])
            row[-1] = tuple(row[-1].split('\t'))
            rows.append(tuple(row))
        # print('--------- {} --------'.format(rows))
        if resp == True:
            # print('inside if true')
            # print(annotated_tweets[user])
            return render_template('view_annotated_tweets_admin_tables.html',
                                   rows=rows, error=None, user=user)
        else:
            return render_template('view_annotated_tweets_admin_tables.html', error=resp)
    else:
        return redirect(url_for('login'))


@app.route('/report_incomplete', methods=['POST', 'GET'])
def report_incomplete():
    if session.get('user'):
        if request.method == 'POST':
            id_str = request.form.get('id_str')
            tweet = request.form.get('tweet')
            # print(tweet)
            tweetvo = tweetVO()
            tweetdao = tweetDAO()
            # user = session.get('user')
            tweetvo.username = session['user']
            tweetvo.tweet_id = id_str
            tweetvo.tweet = tweet
            resp = tweetdao.report_incomplete_tweet(tweetvo)
            user_data = read_json('data/annoted_tweets.json')
            user_data[session['user']]['reported_tweets'].append(id_str)
            new_data = json.dumps(user_data, indent=4)
            json_file = open('data/annoted_tweets.json', 'w')
            json_file.write(new_data)
            json_file.close()

            if resp:
                resp = {'status': 'INC_OK'}
                return json.dumps(resp)
            else:
                return '<h1>Oooppss!! Internal Database Error</h1>'
        else:
            return '<h1>INVALID REQUEST</h1>'
    else:
        return redirect(url_for('login'))


@app.route('/report_not_english', methods=['POST', 'GET'])
def report_not_english():
    if session.get('user'):
        if request.method == 'POST':
            id_str = request.form.get('id_str')
            tweet = request.form.get('tweet')
            # print(tweet)
            tweetvo = tweetVO()
            tweetdao = tweetDAO()
            # user = session.get('user')
            tweetvo.username = session['user']
            tweetvo.tweet_id = id_str
            tweetvo.tweet = tweet
            resp = tweetdao.report_not_english(tweetvo)
            user_data = read_json('data/annoted_tweets.json')
            user_data[session['user']]['reported_tweets'].append(id_str)
            new_data = json.dumps(user_data, indent=4)
            json_file = open('data/annoted_tweets.json', 'w')
            json_file.write(new_data)
            json_file.close()

            if resp:
                resp = {'status': 'NOT_ENGLISH_OK'}
                return json.dumps(resp)
            else:
                return '<h1>Oooppss!! Internal Database Error</h1>'
        else:
            return '<h1>INVALID REQUEST</h1>'
    else:
        return redirect(url_for('login'))


def clean_data(data):
    data_clean = []
    # print(li)
    for row in data:
        row_li = list(row)
        for column in row_li:
            if column == None:
                row_li.remove(column)
            else:
                pass
        data_clean.append(row_li)

    final_data = []
    count_double = 0
    for data in data_clean:
        updated = [d for d in data if d]
        if 'None' in updated:
            print(updated[3:])
        if len(updated[3:]) > 2:
            # print(updated[1], updated[3:-1])
            count_double += 1
        final_data.append(updated[:-1])
    # print('double count', count_double)
    return final_data, count_double


def get_same_annots(data):
    same_annots = []
    count_double = 0
    for row in data:
        row_unique = []
        if 'en' in row:
            row.remove('en')
        if len(row) > 4:
            count_double += 1
            row_unique += row[0:3]
            set_judgement = set(row[3:])
            if len(set_judgement) == 1:
                set_judgement = list(set_judgement)
                row_unique.append(set_judgement[0])
                same_annots.append(row_unique)

    return same_annots, count_double


def get_agg(data):
    all_tasks = {
        'task_1': [],
        'task_2': [],
        'task_3': [],
        'task_1_un': [],
        'task_2_un': [],
        'task_3_un': []
    }
    # print(data)
    results, ignore = clean_data(data)
    if len(data):
        print('inside if')
        for result in results:
            count = 1
            temp_1, temp_2, temp_3 = [], [], []
            for annot in result[3:]:
                if annot != 'en' and annot != 'hi':
                    annot = annot.split('\t')
                    if len(annot)<3:
                        print(result)
                        continue
                    temp_1.append(annot[0])
                    temp_2.append(annot[1])
                    temp_3.append(annot[2])
            if len(temp_1):
                all_tasks['task_1'].append(tuple(set(temp_1)))
            if len(temp_2):
                all_tasks['task_2'].append(tuple(set(temp_2)))
            if len(temp_3):
                all_tasks['task_3'].append(tuple(set(temp_3)))
        for task in ['task_1', 'task_2', 'task_3']:
            temp = [result for result in all_tasks[task] if len(result) == 1]
            # print('--------', temp)
            all_tasks[task + '_un'] = temp
        agg = []
        print(all_tasks )
        for task in ['task_1', 'task_2', 'task_3']:
            # if len(all_tasks[task]):
                # try:
            un_len=len(all_tasks[task + '_un'])
            all_len=len(all_tasks[task])
            if all_len==0:
                all_len=1
            temp=(un_len / all_len) * 100
            agg.append('%.2f' % temp)

    else:
        agg=['0.00']*3
    print('here',agg)
    return agg


def get_single_annots(data=None):
    tweetdao = tweetDAO()
    all_tweets = tweetdao.get_all_tweets()
    new_data = []
    data = []
    for row in all_tweets:
        temp = list(row)
        data.append(temp)
    for li in data:
        l = [item for item in li if item is not None]
        if len(l) == 5:
            new_data.append(l)
    # print(len(new_data))
    return new_data


# def split_data(split=None):
#     if split:
#         pass
#     else:
#         single = get_single_annots()
#         annotated_data = read_json('annoted_tweets.json')
#         split_dict = {'aditya_hasoc': 240, 'admin': 240, 'bhargav_hasoc': 0, 'daksh2_hasoc': 1000, 'daksh_hasoc': 240,
#                       'devarshi_hasoc': 0, 'dhruv_hasoc': 0, 'meet_hasoc': 240, 'mohana_hasoc': 0, 'parth_hasoc': 240,
#                       'spandan_hasoc': 240, 'suru_hasoc': 0}
#         for user in annotated_data:
#             split_dict[user] = int(input('Enter amount of tweet to be allocated for {}:- '.format(user)))
#         # print(split_dict)
#         for user in annotated_data:
#             annotated_reported_list = annotated_data[user]['annoted_tweets'] + annotated_data[user]['reported_tweets']
#             annotated_data[user]['to_be_annotated'] = []
#             for tweet in single:
#                 if tweet[1] not in annotated_reported_list and split_dict[user] != 0:
#                     annotated_data[user]['to_be_annotated'].append(tweet[1])
#                     split_dict[user] -= 1
#             annotated_data[user]['total_assigned'] = len(annotated_data[user]['to_be_annotated'])
#
#         dump_data = json.dumps(annotated_data, indent=4)
#         file_ptr = open('annoted_tweets.json', 'w')
#         file_ptr.write(dump_data)
#         file_ptr.close()

def get_tasks(data):
    all_tasks = {
        'task_1': [],
        'task_2': [],
        'task_3': [],
        'task_1_un': [],
        'task_2_un': [],
        'task_3_un': []
    }
    results, ignore = clean_data(data)
    for result in results:
        count = 1
        temp_1, temp_2, temp_3 = [], [], []
        for annot in result[3:]:
            if annot != 'en' and annot != 'hi':
                annot = annot.split('\t')
                if len(annot)<3:
                    print(result)
                    continue
                temp_1.append(annot[0])
                temp_2.append(annot[1])
                temp_3.append(annot[2])
        all_tasks['task_1'].append(tuple(set(temp_1)))
        all_tasks['task_2'].append(tuple(set(temp_2)))
        all_tasks['task_3'].append(tuple(set(temp_3)))
    for task in ['task_1', 'task_2', 'task_3']:
        temp = [result for result in all_tasks[task] if len(result) == 1]
        # print('--------', temp)
        all_tasks[task + '_un'] = temp
    agg = []
    for task in ['task_1', 'task_2', 'task_3']:
        agg.append('%.2f' % (len(all_tasks[task + '_un']) / len(all_tasks[task]) * 100))
#     print(agg)
    return all_tasks





def get_analysis(all_tasks):
    analysis = {
        1: {
            'count_task_1': {
                'NOT': 0,
                'HOF': 0,
            },
            'count_task_2': {
                'HATE': 0,
                'OFFN': 0,
                'PRFN': 0,
                'None': 0,
            },
            'count_task_3': {
                'UNT': 0,
                'TIN': 0,
                'NULL': 0
            }
        },
        2: {
            'count_task_1': {
                'NOT': 0,
                'HOF': 0,
            },
            'count_task_2': {
                'HATE': 0,
                'OFFN': 0,
                'PRFN': 0,
                'None': 0,
            },
            'count_task_3': {
                'UNT': 0,
                'TIN': 0,
                'NULL': 0
            }
        }
    }

    for user in analysis:
        for task in ['task_1', 'task_2', 'task_3']:
            for result in all_tasks[task]:
                if len(result) < 1:
                    continue
                elif len(result) == 1 or user == 1:
                    analysis[user]['count_{}'.format(task)][result[0]] += 1
                #                 count_task1[result[0]]+=1
                else:
                    analysis[user]['count_{}'.format(task)][result[1]] += 1
    print(analysis)


@app.route('/stats')
def stats():
    if session.get('user') == 'admin':
        tweetvo = tweetVO()
        # logindao = loginDAO()
        tweetdao=tweetDAO()
        active_users=tweetdao.get_active_users()
        all_tweets = tweetdao.get_all_tweets()
        # tweet_ids = [row[1] for row in all_tweets]
        all_data, double_count = clean_data(all_tweets)
        same_annots, count_double = get_same_annots(all_data)
        data = read_json('data/annoted_tweets.json')
        len_same = len(same_annots)
        len_all = len(all_data)
        aggs = get_agg(all_tweets)

        for user in data:
            if user in active_users:
                data[user]['active']=True
            else:
                data[user]['active']=False

        statistics = {
            'same_annots': len_same,
            'total_annots': len_all,
            'double_annots': double_count
        }
        return render_template('view_statistics_admin.html', data=data, len=len, statistics=statistics, aggs=aggs)
    else:
        return redirect(url_for('home'))

