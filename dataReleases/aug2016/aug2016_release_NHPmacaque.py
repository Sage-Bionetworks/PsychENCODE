import synapseclient
from synapseclient.entity import is_container
syn = synapseclient.login()

import pandas as pd
import re
import synapseutils as synu
import pythonSynapseUtils as synAnnot
from pythonSynapseUtils import auditAndUpdateByCommonDict
from pythonSynapseUtils import auditAndUpdateFormatTypeByFileName
from pythonSynapseUtils import auditAndUpdateByMetadata
from pythonSynapseUtils import delAnnoByKey
from pythonSynapseUtils import annotationsYaml

# NHP-Macaque
#syn7065089

# synAnnot.delAnnoByKey.delAnnoByKey(syn,"syn7065089",["tissueType","readLength"])
# synAnnot.delAnnoByKey.delAnnoByKey(syn,"syn7065089",["platform", "tissueType"])

# 
# # Audit and update by common annotations
# commonDict = {"consortium":"PEC",
#               "grant":"U01MH103339",
#               "group":"Yale, UCSF",
#               "assay":"RNA-seq",
#               "libraryPrep":"polyA selection",
#               "runType":"single-end",
#               "study":"NHP	",
#               "disease":"Control",
#               "fileType":"bam",
#               "PI":"Nenad Sestan, Matt State",
#               "organism":"Rhesus macaque",
#               "tissueType":"",
#               "platform":"GAIIx",
#               "readLength":""
#              }
# 
# synAnnot.auditAndUpdateByCommonDict.updateAnnoByDict(syn,"syn7065089",commonDict)
# 
# 
# entityMissAllAnno, incorrectAnnoated, missingAnno = synAnnot.auditAndUpdateByCommonDict.auditCommonDict(syn,"syn7065089",commonDict)
# 
# 
# result = synAnnot.auditAndUpdateFormatTypeByFileName.auditFormatTypeByFileName(syn,"syn7065089","fileType",{".bam":"bam"})
# for key in result:
# 	print '%s: %d' % (key, len(result[key]))


# Update by metadata
rnaSeqData = syn.get("syn7105855")
rnaSeqData = pd.read_table(rnaSeqData.path, sep = ",")

df = rnaSeqData[["File_Name","BrainRegion Description","ReadLength", "SequencingPlatform"]]
df.columns = ["fileName","tissueType","readLength","platform"]

# entityMissMetadata,incorrectAnnotated, missingAnno = synAnnot.auditAndUpdateByMetadata.auditAgainstMetadata(syn,"syn7065089",df,"fileName",["tissueType","readLength"],[""])
# 
# print 'entityMissMetadata: %d' % len(entityMissMetadata)
# print 'incorrectAnnotated: %d' % len(incorrectAnnotated)
# print 'missingAnno: %d' % len(missingAnno)
# 
# if len(entityMissMetadata) > 0:
# 	for key in entityMissMetadata:
# 		print key
#  
# synAnnot.auditAndUpdateByMetadata.updateAnnoByMetadata(syn,"syn7065089",df,"fileName",["tissueType","readLength"],[""])

synAnnot.auditAndUpdateByMetadata.updateAnnoByMetadata(syn,"syn7065089",df,"fileName",["platform", "tissueType"],[""])


(wrongKeys, wrongValues) = synAnnot.annotationsYaml.checkAgainstDict(syn=syn, synId="syn7065089",annotDictId="syn5605845")


