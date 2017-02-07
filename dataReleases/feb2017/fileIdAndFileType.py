# Code used for the dry run to update the annotations for syn5843155
# This was used to get the fileId and fileType

import synapseclient
from synapseclient.entity import is_container
syn = synapseclient.login()

import pandas as pd
import synapseutils as synu
import synAnnotationUtils as synAnnot
from synAnnotationUtils import update

# Folders to annotate
bamFolder = "syn6200411"
cpgFolder = "syn6200436"
readsFolder = "syn6200302"

############## BAM
# Query for the files of interest
fileQuery = syn.chunkedQuery("select name from file where parentId=='%s'" %bamFolder)

# get the file.name for all files
fileNames = [f for f in fileQuery if f['file.name']]

# convert to dataframe
df = pd.DataFrame(fileNames)

# split out the FileID file.name by the first period; have the rest of the file.name as "fileBits" column
# file.names have the format: "FileID.concatenated.sorted.duplicatesRemoved.fileType"
df2 = pd.DataFrame(df['file.name'].str.split('.',1).tolist(), columns = ['FileID','fileBits'])

# split out the last field by period to get the fileType
df2['fileType'] = df2['fileBits'].str.split('.').str[-1]  

# join the original dataframe with the new one (need the fileName from the first df to match to the files in Synapse)
df2 = df.join(df2)

# Update by metadata
### Update bamFolder using values from df2, match by file.name, add annotations "FileID" and "fileType", no file extensions needed since the file.name in the metadata file have the extension as part of the file name
synAnnot.auditAndUpdateByMetadata.updateAnnoByMetadata(syn,bamFolder,df2,"file.name",["FileID", "fileType"],[""])

############ CpG_Proportions
# Query for the files of interest
fileQuery = syn.chunkedQuery("select name from file where parentId=='%s'" %cpgFolder)

# get the file.name for all files
fileNames = [f for f in fileQuery if f['file.name']]

# convert to dataframe
df = pd.DataFrame(fileNames) 

# split out the FileID file.name by the first period; have the rest of the file.name as "fileBits" column
# file.names have the format: "FileID.concatenated.sorted.duplicatesRemoved.CpG_report.fileType.gz"
df2 = pd.DataFrame(df['file.name'].str.split('.',1).tolist(), columns = ['FileID','fileBits'])

# split out the second to last field by period to get the fileType
df2['fileType'] = df2['fileBits'].str.split('.').str[-2]  

# join the original dataframe with the new one (need the fileName from the first df to match to the files in Synapse)
df2 = df.join(df2)

# Update by metadata
### Update cpgFolder using values from df2, match by file.name, add annotations "FileID" and "fileType", no file extensions needed since the file.name in the metadata file have the extension as part of the file name
synAnnot.auditAndUpdateByMetadata.updateAnnoByMetadata(syn,cpgFolder,df2,"file.name",["FileID", "fileType"],[""])


########### Reads
# Query for the files of interest
fileQuery = syn.chunkedQuery("select name from file where parentId=='%s'" %readsFolder)

# get the file.name for all files
fileNames = [f for f in fileQuery if f['file.name']]  

# convert to dataframe
df = pd.DataFrame(fileNames)   

# split out the FileID file.name by everything before the pattern "_combined"; set the rest of the file.name as "fileBits" column
# file.names have the format: "FileID_combined_readEnd.fileType.gz"
df2 = pd.DataFrame(df['file.name'].str.split('_combined',1).tolist(), columns = ['FileID','fileBits'])

# split out the second to last field by period to get the fileType
df2['fileType'] = df2['fileBits'].str.split('.').str[-2]

# get the two characters (either R1 or R2) between an underscore and period to get readEnd
df2['readEnd'] = df2['fileBits'].str.extract('_(\w\d)\.', expand=True)

# join the original dataframe with the new one (need the fileName from the first df to match to the files in Synapse)
df2 = df.join(df2)

# Update by metadata
# Update readsFolder using values from df2, match by file.name, add annotations "FileID", "fileType" and "readEnd", no file extensions needed since the file.name in the metadata file have the extension as part of the file name
synAnnot.auditAndUpdateByMetadata.updateAnnoByMetadata(syn,"syn6200302",df2,"file.name",["FileID", "fileType", "readEnd"],[""])
