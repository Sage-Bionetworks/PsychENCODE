# Code used for the dry run to update the annotations for syn5843155
# This was used to get the cellType and individual ID
# Cell.Type refers to the cell type in the metadata file
# cellType refers to the re-mapping to match Synapse terms

import synapseclient
from synapseclient.entity import is_container
syn = synapseclient.login()

import pandas as pd
import synapseutils as synu
import synAnnotationUtils as synAnnot
from synAnnotationUtils import update

# Folders to annotate
# BAM - syn6200411
# CpG_Proportions - syn6200436
# Reads - syn6200302
WGBS_Folders = ["syn6200411", "syn6200436", "syn6200302"]

## Metadata File - syn8017780

# Get metadata file
metaData = syn.get("syn8017780")
metaData = pd.read_table(metaData.path, sep = ",")

# collect necessary columns and rename 
# Each folder has its own column of fileNames in the metadata file
df = metaData[["BAM","Cell.Type", "Individual"]]
df.columns = ["fileName","Cell.Type", "Individual"]

df2 = metaData[["CpG_Proportion","Cell.Type", "Individual"]]
df2.columns = ["fileName","Cell.Type", "Individual"]

df3 = metaData[["FASTQ_R1","Cell.Type", "Individual"]]
df3.columns = ["fileName","Cell.Type", "Individual"]

df4 = metaData[["FASTQ_R2","Cell.Type", "Individual"]]
df4.columns = ["fileName","Cell.Type", "Individual"]

df5 = pd.concat([df,df2,df3,df4])

pd.options.mode.chained_assignment = None  # default='warn'; allows temporary renaming of column contents

### Convert cellType in metadata to match cellType terms in Synapse
df5['cellType'] = df5['Cell.Type'].map({'Neuron': 'NeuN+', 'Glia':'NeuN-'})


# Update by metadata
for f in WGBS_Folders:
	synAnnot.update.updateAnnoByMetadata(syn,f,df,"fileName",["Cell.Type", "cellType", "Individual"],[""])

