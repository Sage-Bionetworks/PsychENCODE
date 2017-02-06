library(data.table)
library(plyr)
library(dplyr)
library(tidyr)

library(synapseClient)
synapseLogin()

# Get data from Table View
d <- synTableQuery('select * from syn8211362')

# Convert to wide format, one synapse ID per file type
d.wide <- d@values %>% 
  select(id, FileID, fileType, readEnd) %>% 
  tidyr::unite(myCol, fileType, readEnd, sep="_") %>%
  tidyr::spread(myCol, id) %>% 
  dplyr::rename(bam=`bam_NA`, txt=`txt_NA`)

# Function to add fastq to bam provenance
alignAct <- function(x) {
  tmp <- synGet(x$bam, downloadFile=FALSE)
  act <- Activity(name='align',
                  used=list(as.character(x$fastq_R1), 
                            as.character(x$fastq_R2)))
  generatedBy(tmp) <- act
  synStore(tmp, forceVersion=FALSE)
}

# Function to add bam to cpg provenance
cpgAct <- function(x) {
  tmp <- synGet(x$txt, downloadFile=FALSE) 
  act <- Activity(name='CpG',
                  used=list(as.character(x$bam)))
  generatedBy(tmp) <- act
  synStore(tmp, forceVersion=FALSE)
}

foo <- dlply(d.wide, .(FileID), alignAct, .progress='text')
foo <- dlply(d.wide, .(FileID), cpgAct, .progress='text')
