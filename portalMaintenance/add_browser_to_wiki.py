#! /usr/bin/env python
# KKD for Sage Bionetworks
# Jan. 25, 2016

# sys.argv[1] = folder ID containing bigwigs to which to add genome browser in wiki

import sys
import synapseclient
from synapseclient import Wiki

syn = synapseclient.login()

results = syn.chunkedQuery('select id,fileType,organism,versionNumber from file where parentId=="%s"' % sys.argv[1])
for result in results:
#	print '%s' % result
	if result['file.fileType'][0] == "bigwig":
		temp = syn.get(result['file.id'], downloadFile = False)
		if result['file.organism'][0] == "Homo sapiens":
			browser = ''.join([' """${biodalliance13?chr=1&species=HUMAN&viewStart=3025001&viewEnd=3525001&source0=%7B"name"%3A""%2C "entityId"%3A"', result['file.id'], '"%2C "entityVersion"%3A"', str(result['file.versionNumber']), '"%2C "styleType"%3A"default"%2C "styleGlyphType"%3A"HISTOGRAM"%2C "color"%3A"%23808080"%2C "type"%3A"BIGWIG"%2C "height"%3A"120"%7D}""" ' ])
#			print '%s' % browser
		elif result['file.organism'][0] is "Mus musculus":
			browser = ''.join([' """${biodalliance13?chr=1&species=MOUSE&viewStart=3025001&viewEnd=3525001&source0=%7B"name"%3A""%2C "entityId"%3A"', result['file.id'], '"%2C "entityVersion"%3A"', str(result['file.versionNumber']), '"%2C "styleType"%3A"default"%2C "styleGlyphType"%3A"HISTOGRAM"%2C "color"%3A"%23808080"%2C "type"%3A"BIGWIG"%2C "height"%3A"120"%7D}""" ' ])		
		wiki = Wiki(owner=temp, markdown=browser)
		wiki = syn.store(wiki)