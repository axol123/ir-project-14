from datetime import datetime
from elasticsearch import Elasticsearch
import re
import time

es = Elasticsearch()

# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }

# doc = {
#     'declaration': 'public static class poop',
#     'line_nr': 'Elasticsearch: cool. bonsai cool.',
#     'file_id': datetime.now(),
# }

# res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
# print(res['result'])

# res = es.get(index="test-index", doc_type='tweet', id=1)
# print(res['_source'])

# es.indices.refresh(index="test-index")

# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

# File with single line comments crawler/sources/48823c52-6be1-11e9-9546-a8667f0ad154-TestRSeedTestSuccess2.java
# Interface 46dc67ec-6be1-11e9-9546-a8667f0ad154-Doc.java
# file_id="crawler/sources/48823c52-6be1-11e9-9546-a8667f0ad154-TestRSeedTestSuccess2.java"
file_id = "crawler/sources/46dc67ec-6be1-11e9-9546-a8667f0ad154-Doc.java"
text = open(file_id).read()

# file with multi line comments crawler/sources/46bdfe10-6be1-11e9-9546-a8667f0ad154-Choice.java
# text = open("crawler/sources/46bdfe10-6be1-11e9-9546-a8667f0ad154-Choice.java").read()
#print(text)

# # Remove single line comments
# text = re.sub('\/\/.*', '', text)

# # Remove multiline comments
# text = re.sub('\/\*[\s\S]*\*/','', text)


# Process the files and separate class names, method names, modifiers (for example
# public, private, static, final etc.), variable names

#print(text)
in_multi_comment=False
in_single_comment=False
doc_string=''
delimiters=['{', ]
parsing = ''
parse_interface = False
nr_brackets=0
skip_until=-1
# keywords = ["public", "private", "static", "final"]
# Note that line_nr is (actual line number)-1
delimiters = [';', '{', '}', '(', ')']
for line_nr, line in enumerate(text.splitlines()):
	for word in line.split():
		for token in re.split('([{}();@]|\/\/|\/\*|\*\/)', word):
			if(token=='/*'):
				in_multi_comment=True
			if(token=='*/'):
				in_multi_comment=False
			if(in_multi_comment):
				continue
			if(token=='//'):
				in_single_comment=True
				break
			if(token=='}'):
				nr_brackets=nr_brackets-1
				if(skip_until==nr_brackets):
					skip_until=-1
			if(skip_until>=0):
				if(token=='{'):
					nr_brackets=nr_brackets+1
				continue

			if(token=='class' or token=='interface'):
				parsing=token
			if(token=='{'):
				if(parsing=='class' or parsing=='interface'):
					doc = {
					    'declaration': doc_string[1:],
					    'line_nr': line_nr+1,
					    'file_id': file_id,
					}
					res = es.index(index=parsing, body=doc)
					parsing=''
				else:
					skip_until=nr_brackets
				nr_brackets=nr_brackets+1

			if(nr_brackets>0):
				if (token=='('):
					parsing='method'
				elif (token==')' and parsing=='method'):
					doc = {
					    'declaration': doc_string[1:]+' )',
					    'line_nr': line_nr+1,
					    'file_id': file_id,
					}
					res = es.index(index=parsing, body=doc)
					parsing=''
				elif (token==';'):
					parsing='field'
					doc = {
					    'declaration': doc_string[1:],
					    'line_nr': line_nr+1,
					    'file_id': file_id,
					}
					res = es.index(index=parsing, body=doc)
					parsing=''

			if(token!='{' and token != '*/'):
				doc_string = doc_string+' '+token

			if(token=='}' or token==';' or token=='{'):

				doc_string =''
			


		if(in_single_comment):
			in_single_comment=False
			break
		

time.sleep(1)

# res = es.search(index="class", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(declaration)s %(line_nr)s: %(file_id)s" % hit["_source"])

# res = es.search(index="method", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(declaration)s %(line_nr)s: %(file_id)s" % hit["_source"])

res = es.search(index="interface", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(declaration)s %(line_nr)s: %(file_id)s" % hit["_source"])

res = es.search(index="field", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(declaration)s %(line_nr)s: %(file_id)s" % hit["_source"])



# for token in text.split():
#  	print(token)