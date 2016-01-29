#! /usr/bin/env python
# KKD for Sage Bionetworks
# Jan. 26, 2016

# sys.argv[1] = input file containing paired old-new terms
# sys.argv[2] = project ID to check

import sys, os
import synapseclient

syn = synapseclient.login()

def updateKey(oldKey,newKey,inAnnot):
	if oldKey in inAnnot:
		inAnnot[newKey] = inAnnot[oldKey]
		del inAnnot[oldKey]
	return(inAnnot)

# 
# # Update keys
# with open(sys.argv[1]) as toChange:
# 	for line in toChange:
# 		(old, new) = line.split()
# 		sql = 'select id,%s from file where projectId=="%s"' % (old,sys.argv[2])
# 		print sql
# 		results = syn.chunkedQuery(sql)
# 		for result in results:
# 			temp = syn.getAnnotations(result['file.id'])
# 			if old not in temp: continue
# 			correctedAnnotations = updateKey(oldKey=old,newKey=new,inAnnot=temp)
# 			savedAnnotations = syn.setAnnotations(result['file.id'],correctedAnnotations)

# Update keys and values
with open(sys.argv[1]) as toChange:
	for line in toChange:
		items = line.strip().split('\t')
		if len(items) == 2: # update keys
			old = items[0]
			new = items[1]
			sql = 'select id,%s from file where projectId=="%s"' % (old,sys.argv[2])
			print sql
			results = syn.chunkedQuery(sql)
			for result in results:
				temp = syn.getAnnotations(result['file.id'])
				if old not in temp: continue
				correctedAnnotations = updateKey(oldKey=old,newKey=new,inAnnot=temp)
	#			print correctedAnnotations
				savedAnnotations = syn.setAnnotations(result['file.id'],correctedAnnotations)
		elif len(items) > 2: # update values
			kKey = items.pop(0)
			old = items.pop(0)
			sql = 'select id,%s from file where projectId=="%s" and file.%s=="%s"' % (kKey,sys.argv[2],kKey,old)
			print sql
			results = syn.chunkedQuery(sql)
			for result in results:
				temp = syn.getAnnotations(result['file.id'])
				if kKey not in temp: continue
				temp[kKey] = items
#				print temp
				savedAnnotations = syn.setAnnotations(result['file.id'],temp)
