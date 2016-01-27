#! /usr/bin/env python
# KKD for Sage Bionetworks
# Jan. 25, 2016

# sys.argv[1] = synapse ID of (yaml) annotation dictionary
# sys.argv[2] = project ID to check
# sys.argv[3] = annotation key by which to stratify the results

import sys, yaml
import synapseclient

syn = synapseclient.login()
yamlEnt = syn.get(sys.argv[1])

annotations = yaml.load(file(yamlEnt.path))


def countQueryResults(sql):
	'''Counts number of entities returned by a query.'''

	results = syn.chunkedQuery(sql)
	count = 0
	for i in results:
		count += 1
	return count

if sys.argv[3] is not None: # This block counts annotation terms stratified by one term as specified in command-line argument #3

	for element in annotations[sys.argv[3]]:
		print '%s' % element
		for key in annotations:
			print '%s' % key
			if isinstance(annotations[key], list):
				for val in annotations[key]:
					sql = 'select id from file where projectId=="%s" and file.%s=="%s" and file.%s=="%s"' % (sys.argv[2], key, val, sys.argv[3], element)
		#			print '%s' % sql
					print '%s: %s\t%d' % (key, val, countQueryResults(sql))
			else:
				sql = 'select id from file where projectId=="%s" and file.%s=="%s" and file.%s=="%s"' % (sys.argv[2], key, annotations[key], sys.argv[3], element)
		#		print '%s' % sql
				print '%s: %s\t%d' % (key, annotations[key], countQueryResults(sql))

else: # This block counts annotation terms across the whole project

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



