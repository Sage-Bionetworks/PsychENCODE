#!/bin/bash

synID=syn4227883     #Set the folder where to store results
star_execute=STAR    #path to STAR executable

############################################
#Fetch an unaligned fastq file and the human reference for chr19 from Synapse  
##########################################
synapse get syn2468557  #Get human reference
synapse get syn2468554  #Get fastq

############################################
# Execute STAR
##########################################
##Build the genome index from the human reference
mkdir analysis
mkdir analysis/ref_genome
$star_execute --runMode genomeGenerate --genomeDir analysis/ref_genome --genomeFastaFiles hg19_chr19_subregion.fasta

##Align downloaded sample "brain.fastq"
$star_execute --runThreadN 2 --genomeDir analysis/ref_genome --outFileNamePrefix analysis/brain_ --outSAMunmapped Within --readFilesIn brain.fastq

###############################################
#Add this file and the aligned sample to Synapse
################################################
synapse add Synapse_Commandline_RNA-Seq_alignment.sh --parentid $synID
synapse add analysis/brain_Aligned.out.sam  --parentid  $synID \
        --used hg19_chr19_subregion.fasta brain.fastq \
        --executed Synapse_Commandline_RNA-Seq_alignment.sh \
        --annotations '{"fileType":"sam", "dataType":"mRNA"}'
