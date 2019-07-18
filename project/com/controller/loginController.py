from flask import *
from project import app
from project.com.vo.loginVO import loginVO
from project.com.vo.loginVO import registerVO
from project.com.dao.loginDAO import loginDAO
from project.com.dao.loginDAO import registerDAO
from project.com.dao import conn_db
from project.com.controller.tweetController import read_json
import csv
import json

conn = conn_db()


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    loginDao = loginDAO()
    user_temp_not_allowed = loginDao.get_active_users()
    if not session.get('user'):
        user = loginVO()
        error = None
        if request.method == "POST":

            user.username = request.form.get('username')
            user.password = request.form.get('password')
            data = loginDao.login_user(user)
            # print(user.username)
            # print(data)
            if len(data) == 0:
                script = '''<script>
                                alert("Username Invalid!!!");
                                window.location.href="/home";
                            </script>'''
                return script
            elif user.username not in user_temp_not_allowed:
                script = '''<script>
                            alert("You are currently not allowed to annotate! Please contact admin");
                            window.location.href="/home";
                        </script>'''
                return script
            elif user.password != data[0][3]:
                script = '''<script>
                                alert("Incorrect Password!!!");
                                window.location.href="/home";
                            </script>
                        '''
                return script
            else:
                session['user'] = user.username
                session['name'] = data[0][1]
                return redirect(url_for('home'))

        else:
            return render_template('index.html')
    else:
        return redirect(url_for('home'))


def get_user_logs(username):
    file_ptr = open('data/annoted_tweets.json')
    data = json.loads(file_ptr.read())
    annoted_ids_list = [str(x) for x in data[username]['annoted_tweets']] + [str(x) for x in
                                                                             data[username]['reported_tweets']]
    start_end = data[username]['start_end']
    return annoted_ids_list, start_end


def get_user_logs_assigned(username):
    file_ptr = open('data/annoted_tweets.json')
    data = json.loads(file_ptr.read())
    assigned_list = data[username]['to_be_annotated']
    total_assigned = data[username]['total_assigned']
    # print(assigned_list)
    return assigned_list, total_assigned


def fetch_data_json():
    file_ptr = open('data/merge.json')
    # datas=file.readlines()
    datas = json.loads(file_ptr.read())
    count = 0
    rows = []
    annoted_ids_list, start_end = get_user_logs(session['user'])
    for data in datas[start_end[0]:start_end[1]]:
        # data=json.loads(data)
        if data['id_str'] in annoted_ids_list:
            continue
        data['num'] = count
        row = [int(data.get('num')), data.get('text'), data.get('id_str'), data.get('lang')]
        rows.append(row)
        count += 1
    # print(rows)
    return rows


def fetch_data_json_assigned():
    file_ptr = open('data/merge.json')
    # datas=file.readlines()
    datas = json.loads(file_ptr.read())
    count = 0
    rows = []
    assigned_list, total_assigned = get_user_logs_assigned(session['user'])
    annoted_ids_list, start_end = get_user_logs(session['user'])
    # print(set(annoted_ids_list+['1139819120197640192']).intersection(set(assigned_list)))
    for data in datas:
        # data=json.loads(data)
        if data['id_str'] in assigned_list and data['id_str'] not in annoted_ids_list:
            data['num'] = count
            row = [int(data.get('num')), data.get('text'), data.get('id_str'), data.get('lang')]
            rows.append(row)
            count += 1
        else:
            # print('else')
            pass
    return rows, total_assigned


@app.route('/home')
def home():
    if session.get('user'):
        rows,total_assigned = fetch_data_json_assigned()
        # print(rows,total_assigned)
        if total_assigned==0:
            total_assigned=1
        records = {
            'total': total_assigned,
            'remaining': len(rows)
        }
        return render_template('home.html', rows=rows[0:100], name=session['name'], len=len, records=records, str=str)
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = registerVO()
        registerDao = registerDAO()
        user.name = request.form.get('name')
        user.username = request.form.get('uname')
        user.assigned = str(request.form.get('assigned'))
        user.password = request.form.get('pwd')
        user.c_password = request.form.get('cpwd')
        resp = registerDao.check_exists(user)
        if len(resp) > 0:
            return 'Username already taken'
        else:
            resp = registerDao.register_user(user)
            if resp == True:
                registerDao.do_necessary_changes(user)
                return redirect(url_for('home'))
            else:
                return 'Internal DB error'

    else:
        file_ptr = open('data/annoted_tweets.json')
        data = json.load(file_ptr)
        return render_template('register.html', data=data, len=len)

def create_nested_list(data,col=2):
    count=0
    nested=[]
    temp={}
    for d in data:
        if count%(col) !=0 or count==0:
            temp[d]=data[d]
        else:
            nested.append(copy.deepcopy(temp))
            temp={}
            temp[d]=data[d]
        count+=1
    # temp_file=open('temp.json','w')
    # temp_file.write(json.dumps(nested,indent=2))
    # temp_file.close()
    return nested
    # print(json.dumps(nested,indent=2))



@app.route('/manage_users',methods=['POST','GET'])
def manage_users():
    resp=None
    logindao = loginDAO()
    loginvo = loginVO()
    active_users = logindao.get_active_users()
    print(active_users)
    all_user_data = read_json('data/annoted_tweets.json')
    for user in all_user_data:
        if user in active_users:
            all_user_data[user]['active'] = True
        else:
            all_user_data[user]['active'] = False
    if request.method=='POST':
        if session.get('user') == 'admin':
            user=request.form.get('user')
            check=request.form.get('check')
            if check=='add':
                print(request.form.get('add_no_tweets'))
                resp = 'success'
            elif check=='rem':
                print(request.form.get('rem_no_tweets'))
                resp='success'

            elif check=='reac':
                loginvo.username=request.form.get('user')
                resp=logindao.reactivate_user(loginvo)
                print(request.form)
            else:
                print(request.form)
                loginvo.username = request.form.get('user')
                resp = logindao.deactivate_user(loginvo)
            return resp
        else:
            return redirect(url_for('home'))

    else:
        return render_template('manage_users_admin.html', user_data=all_user_data)















@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    fetch_data_json()
