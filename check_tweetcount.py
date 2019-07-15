import json

file=open("data/annoted_tweets.json","r")
data_json=json.load(file)
file.close()

for user in data_json:
    data_json[user]['annoted_count']=len(data_json[user]['annoted_tweets'])
    data_json[user]['reported_count']=len(data_json[user]['reported_tweets'])
    data_json[user]['total_assigned']=data_json[user]['start_end'][1]-data_json[user]['start_end'][0]
with open("data/annoted_tweets.json", 'w') as json_file:
    json.dump(data_json, json_file, indent=4)