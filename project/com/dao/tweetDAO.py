from project.com.dao import conn_db
import sqlite3

conn = conn_db()
cursor = conn.cursor()


class tweetDAO:
    def check_exists(self, tweet):
        query = 'SELECT * FROM annoted_tweets WHERE tweet_id="{}"'.format(tweet.tweet_id)
        try:
            # print('inside try')
            cursor.execute(query)
            rows = cursor.fetchall()
            # print(rows)
            len_rows = len(rows)
            return len_rows, True
        except sqlite3.Error as er:
            # print('\n\n\nCheck_exists', er)
            return er, False

    def insert_annot(self, tweet):
        query = 'INSERT INTO annoted_tweets (tweet_id,tweet,{},lang) VALUES ("{}","{}","{}","{}")'.format(tweet.username,
                                                                                                tweet.tweet_id,
                                                                                                tweet.tweet, tweet.resp,tweet.lang)
        print(query)
        try:
            # print('inside try')
            cursor.execute(query)
            conn.commit()
            return True
        except sqlite3.Error as er:
            # print('\n\n\n insert_annot', er)
            return er

    def update_records(self, tweet):
        query = 'UPDATE annoted_tweets SET {}="{}" WHERE tweet_id="{}"'.format(tweet.username, tweet.resp,
                                                                               tweet.tweet_id)
        try:
            print(query)
            # print('inside try')
            cursor.execute(query)
            conn.commit()
            return True
        except sqlite3.Error as er:
            # print('\n\n\n update_records', er)
            return er

    def get_annots(self, tweet):
        query = 'SELECT tweet_id,tweet,{} From annoted_tweets where {} not null'.format(tweet.username, tweet.username)
        try:
            # print('inside try (get annots)')
            cursor.execute(query)
            rows = cursor.fetchall()
            # print(rows)
            return True, rows
        except sqlite3.Error as er:
            # print('\n\n\n update_records', er)
            return er

    def get_annots_admin(self):
        cursor.execute('SELECT username from users;')
        users=[user[0] for user in cursor.fetchall()]
        # users = ['admin',
        #          'daksh_hasoc',
        #          'aditya_hasoc',
        #          'sahil_hasoc',
        #          'spandan_hasoc',
        #          'krishna_hasoc',
        #          'parth_hasoc',
        #          'mohana_hasoc',
        #          'devarshi_hasoc',
		#  'daksh2_hasoc'
        #          ]
        print(users)
        annotated_tweets = {}

        try:
            # print('inside try (get annots admin)')
            for user in users:
                query = 'SELECT tweet_id,tweet,{} From annoted_tweets where {} not null'.format(user, user)
                cursor.execute(query)
                annotated_tweets[user] = cursor.fetchall()
            return True, annotated_tweets
        except sqlite3.Error as er:
            # print('\n\n\n update_records', er)
            return er

    def report_incomplete_tweet(self, tweet):
        query = 'INSERT INTO incomplete_tweets (tweet_id,tweet,reported_by) VALUES ("{}","{}","{}")'.format(
            tweet.tweet_id, tweet.tweet, tweet.username)
        # print(query)
        try:
            # print('Report Tweet inside try')
            cursor.execute(query)
            conn.commit()
            return True
        except sqlite3.Error as er:
            # print('\n\n\n Report tweet', er)
            return er

    def report_not_english(self, tweet):
        query = 'INSERT INTO not_english (tweet_id,tweet,reported_by) VALUES ("{}","{}","{}")'.format(
            tweet.tweet_id, tweet.tweet, tweet.username)
        # print(query)
        try:
            # print('Report Tweet inside try')
            cursor.execute(query)
            conn.commit()
            return True
        except sqlite3.Error as er:
            # print('\n\n\n Report tweet', er)
            return er

    def get_all_tweets(self):
        query="SELECT * FROM annoted_tweets"
        cursor.execute(query)
        return list(cursor.fetchall())

    def get_active_users(self):
        cursor = conn.cursor()
        query = 'SELECT username from users WHERE active=1'
        cursor.execute(query)
        users = cursor.fetchall()
        users = [user[0] for user in users]
        return users