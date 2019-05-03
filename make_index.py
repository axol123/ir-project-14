from elasticsearch import Elasticsearch
import re
import time
import os
import glob


# Make dictionary from file id to git location
meta_file = "crawler/path_index.txt"
meta_dict = {}
with open(meta_file) as f:
	for line in f:
		(key, val) = line.split()
		meta_dict[key] = val


# Files for testing
# File with single line comments crawler/sources/48823c52-6be1-11e9-9546-a8667f0ad154-TestRSeedTestSuccess2.java
# Interface 46dc67ec-6be1-11e9-9546-a8667f0ad154-Doc.java
# file_id="crawler/sources/48823c52-6be1-11e9-9546-a8667f0ad154-TestRSeedTestSuccess2.java"
# file_id = "crawler/sources/46dc67ec-6be1-11e9-9546-a8667f0ad154-Doc.java"
# text = open(file_id).read()


es = Elasticsearch()
path = "crawler/sources/"
# For each file in the sources directory
for file in glob.glob(os.path.join(path, '*.java')):
	# Initialize help variables for file parsing
	file_id = re.sub(path, '', file)
	text = open(file).read()
	in_multi_comment=False
	in_single_comment=False
	doc_string=''
	parsing = ''
	parse_interface = False
	nr_brackets=0
	skip_until=-1
	# For each line in the file
	for line_nr, line in enumerate(text.splitlines()):
		# For each word(separated by space) in the line
		for word in line.split():
			# For each token with respect to the characters of interest
			for token in re.split('([{}();@]|\/\/|\/\*|\*\/)', word):
				# Make sure contents of multi line comments are ignored
				if(token=='/*'):
					in_multi_comment=True
				if(token=='*/'):
					in_multi_comment=False
				if(in_multi_comment):
					continue
				# Make sure contents of single line comments are ignored
				if(token=='//'):
					in_single_comment=True
					break
				# Keep track of brackets
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
					# Add class or interface to elasticsearch index
					if(parsing=='class' or parsing=='interface'):
						doc = {
						    'declaration': doc_string[1:],
						    'line_nr': line_nr+1,
						    'file_id': file_id,
						    'file_location': meta_dict[file_id],
						}
						res = es.index(index=parsing, body=doc)
						parsing=''
					else:
						# If there is a bracket and we are not in a class or an interface, start skipping
						skip_until=nr_brackets
					nr_brackets=nr_brackets+1

				if(nr_brackets>0):
					if (token=='('):
						parsing='method'
					# Add method to elasticsearch index
					elif (token==')' and parsing=='method'):
						doc = {
						    'declaration': doc_string[1:]+' )',
						    'line_nr': line_nr+1,
						    'file_id': file_id,
						    'file_location': meta_dict[file_id],
						}
						res = es.index(index=parsing, body=doc)
						parsing=''
					# Add field to elasticsearch index
					elif (token==';'):
						parsing='field'
						doc = {
						    'declaration': doc_string[1:],
						    'line_nr': line_nr+1,
						    'file_id': file_id,
						    'file_location': meta_dict[file_id],
						}
						res = es.index(index=parsing, body=doc)
						parsing=''
				if(token!='{' and token != '*/'):
					# add token to docstring
					doc_string = doc_string+' '+token

				if(token=='}' or token==';' or token=='{'):
					# make sure doc_string is reset before new entry
					doc_string =''
			# Ignore the rest of the line if in a single line comment
			if(in_single_comment):
				in_single_comment=False
				break
			


time.sleep(1)

# # Test queries
# res = es.search(index="class", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(declaration)s %(line_nr)s: %(file_id)s" % hit["_source"])

# res = es.search(index="method", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(declaration)s %(line_nr)s: %(file_id)s" % hit["_source"])

# res = es.search(index="interface", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(declaration)s %(line_nr)s: %(file_id)s" % hit["_source"])

# res = es.search(index="field", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(declaration)s %(line_nr)s: %(file_id)s" % hit["_source"])
