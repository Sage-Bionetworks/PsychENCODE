#!/bin/sh

## Usage
# sh run-all.sh shula run3-v1.0.10 TRUE

# Define variables
EXPERIMENT=$1
PREFIX=$2
SKIP1=${3-"FALSE"}
SKIP6=${4-"FALSE"}
SKIP8=${5-"FALSE"}

mkdir -p ${EXPERIMENT}/CoverageInfo
mkdir -p ${EXPERIMENT}/derAnalysis

if [[ $SKIP1 == "FALSE" ]]
then  
    echo "Use shula/CoverageInfo/run-import.sh instead"
    #sh step1-fullCoverage.sh ${EXPERIMENT}
fi
sh step2-makeModels.sh ${EXPERIMENT} ${PREFIX}
sh step3-analyzeChr.sh ${EXPERIMENT} ${PREFIX}
sh step4-mergeResults.sh ${EXPERIMENT} ${PREFIX}
sh step5-derfinderReport.sh ${EXPERIMENT} ${PREFIX}
