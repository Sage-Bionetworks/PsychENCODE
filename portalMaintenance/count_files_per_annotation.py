#! /usr/bin/env python
# KKD for Sage Bionetworks
# Jan. 25, 2016

# sys.argv[1] = yaml file of annotation dictionary
# sys.argv[2] = project ID to check

import sys, yaml
import synapseclient

syn = synapseclient.login()

annotations = yaml.load(file(sys.argv[1]))


def countQueryResults(sql):
	'''Counts number of entities returned by a query.'''

	results = syn.chunkedQuery(sql)
	count = 0
	for i in results:
		count += 1
	return count



for key in annotations:
	print '%s' % key
	if isinstance(annotations[key], list):
		for val in annotations[key]:
			sql = 'select id from file where projectId=="%s" and file.%s=="%s"' % (sys.argv[2], key, val)
#			print '%s' % sql
			print '%s: %s\t%d' % (key, val, countQueryResults(sql))
	else:
		sql = 'select id from file where projectId=="%s" and file.%s=="%s"' % (sys.argv[2], key, annotations[key])
#		print '%s' % sql
		print '%s: %s\t%d' % (key, annotations[key], countQueryResults(sql))
	