# Code used for the dry run to update the annotations for syn5843155
# Annotate all the files with the same annotations as defined in the commonDict

import synapseclient
from synapseclient.entity import is_container
syn = synapseclient.login()

import pandas as pd
import synapseutils as synu
import synAnnotationUtils as synAnnot
from synAnnotationUtils import update


# Audit and update by common annotations 
commonDict = {"consortium":"PEC",
"group":"LIBD",
"grant":"R21MH102791",
"PI":"Andrew Jaffe",
"species":"Homo sapiens",
"organ":"brain",
"tissueType":"Dorsolateral Prefrontal Cortex",
"disease":"Control",
"assay":"WGBS",
"platform":"HiSeq X Ten"
}


# Annotate files
# bam syn6200411
# cpg  syn6200436
# reads syn6200302
WGBS_Folders = ["syn6200411", "syn6200436", "syn6200302"]

for f in WGBS_Folders:
	synAnnot.update.updateAnnoByDict(syn,f,commonDict)
