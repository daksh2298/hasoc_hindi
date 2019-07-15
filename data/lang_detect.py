from google.cloud import translate
import six
import json

translate_client = translate.Client()

def custom_detect_language(text):
	result = translate_client.detect_language(text)
	return result['language']


file_ptr=open('temp.json')
all_data=json.load(file_ptr)

allowed_langs=['hi','en']
for data in all_data:
	lang=custom_detect_language(data['text'])
	if lang in allowed_langs:
		data['lang']=lang
	else:
		all_data.remove(data)
		print('{}\t{}'.format(data['id_str'],lang))
		# print(data)
		# print(lang)


print(len(all_data))
dumped=json.dumps(all_data,indent=4)
file_ptr.close()
file_ptr=open('temp_lang_detected.json','w')
file_ptr.write(dumped)
file_ptr.close()

# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
# text='@RepublicTVLive Arnab BJP ko itna support mat karo!!jo Party tumhare channel ko Banned karne ki baat kiya tha!!Sambit Patra when 183 children died in Bihar then what were you doing?!#GandiNaaliAbuse'
# result = translate_client.detect_language(text)

# print('Text: {}'.format(text))
# print('Confidence: {}'.format(result['confidence']))
# print('Language: {}'.format(result['language']))




