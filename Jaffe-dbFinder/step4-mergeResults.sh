#!/bin/sh

## Usage
# sh step4-mergeResults.sh shula run3-v1.0.10

# Define variables
EXPERIMENT=$1
SHORT="derM-${EXPERIMENT}"
PREFIX=$2

# Directories
ROOTDIR=/yourPath/PyschENCODE/Jaffe-dbFinder
MAINDIR=${ROOTDIR}/${EXPERIMENT}
WDIR=${MAINDIR}/derAnalysis

# Construct shell files
outdir="${PREFIX}"
sname="${SHORT}.${PREFIX}"
echo "Creating script ${sname}"
cat > ${ROOTDIR}/.${sname}.sh <<EOF
#!/bin/bash
#$ -cwd
#$ -m e
#$ -l mem_free=10G,h_vmem=50G,h_fsize=10G
#$ -N ${sname}
#$ -hold_jid derA-${EXPERIMENT}.${PREFIX}.chr*

echo "**** Job starts ****"
date

mkdir -p ${WDIR}/${outdir}/logs

# merge results
cd ${WDIR}
module load R/3.1.x
Rscript -e "library(derfinder); load('/dcs01/ajaffe/Brain/derRuns/derfinderExample/derGenomicState/GenomicState.Hsapiens.UCSC.hg19.knownGene.Rdata'); load('${WDIR}/${PREFIX}/chr22/optionsStats.Rdata'); chrs <- paste0('chr', c(1:22, 'X', 'Y', 'M')); mergeResults(chrs = chrs, prefix = '${PREFIX}', genomicState = GenomicState.Hsapiens.UCSC.hg19.knownGene[['fullGenome']], optionsStats = optionsStats); prefix <- '${PREFIX}'; source('/yourPath/PyschENCODE/Jaffe-dbFinder/fix-colnames.R'); Sys.time(); proc.time(); options(width = 120); devtools::session_info()"

# Move log files into the logs directory
mv ${ROOTDIR}/${sname}.* ${WDIR}/${outdir}/logs/

echo "**** Job ends ****"
date
EOF
call="qsub .${sname}.sh"
echo $call
$call
