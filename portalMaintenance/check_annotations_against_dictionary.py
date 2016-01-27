#! /usr/bin/env python
# KKD for Sage Bionetworks
# Jan. 25, 2016

# sys.argv[1] = synapse ID of (yaml) annotation dictionary
# sys.argv[2] = project ID to check

import sys, yaml
import synapseclient

syn = synapseclient.login()
yamlEnt = syn.get(sys.argv[1])

annotations = yaml.load(file(yamlEnt.path))

allKeysInProject = set()
allValsInProject = set()

systemKeysToExclude = ['creationDate', 'etag', 'id', 'uri', 'accessControl']

#results = syn.chunkedQuery('select id from file where projectId=="%s" and file.assay=="ChIP-seq"' % sys.argv[2])
results = syn.chunkedQuery('select id from file where projectId=="%s"' % sys.argv[2])
for result in results:
	temp = syn.getAnnotations(result['file.id'])
	for key in temp:
		if key in systemKeysToExclude: continue
		if not key in allKeysInProject:
			allKeysInProject.add(key)
		if isinstance(temp[key], list):
			for val in temp[key]:
				if val in allValsInProject: continue
				allValsInProject.add(val)
		else:
			if temp[key] in allValsInProject: continue
			allValsInProject.add(temp[key])

print 'Number of key terms in project: %d' % len(allKeysInProject)
print 'Number of value terms in project: %d' % len(allValsInProject)


allKeysInVocab = set(annotations.keys())
if not allKeysInProject <= allKeysInVocab:
	print 'Keys in use that are not found in dictionary: '
	for item in allKeysInProject.difference(allKeysInVocab):
		print '%s' % item


allValsInVocab = list()
for key in annotations:
	temp = annotations[key]
	if isinstance(temp, list):
		for element in temp:
			allValsInVocab.append(element)
	else:	
		allValsInVocab.append(temp)
allUniqueValsInVocab = set(allValsInVocab)
if not allValsInProject <= allValsInVocab:
	print 'Values in use that are not found in dictionary: '
	for item in allValsInProject.difference(allValsInVocab):
		print '%s' % item
