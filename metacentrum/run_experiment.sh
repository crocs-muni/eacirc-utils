#!/bin/bash

# Into how many equal parts should the computation of a single experiment be devided?
PARTS=10
# How many hours would computing the complete experiment sequentially take?
FULLTIME=240
# How many runs to compute?
EACIRC_RUNS=1000

# check number of arguments, display help
if [ $# -eq 0 ]
then
    echo "usage: "$0" <config-file> [<config-file> ...]"
    echo "IMPORTANT: Avoid spaces in paths and names."
    echo "IMPORTANT: Avoid configs with the same names submitted from the same directory."
    echo "  Given config files will be run as experiments"
    echo "  each running "$EACIRC_RUNS" times, divided into "$PARTS" parts"
    echo "  with a time limit of "$(($FULLTIME / $PARTS))" hours per part."
    echo "  Results will be saved here in subfolders ("$PWD")"
    exit 1
fi

# for all configuration file present
for CONFIG_FULL in $@
do
    # strip path
    CONFIG=${CONFIG_FULL##*/}
    # create folder for resutls
    mkdir $CONFIG.d
    if [ ! -f $CONFIG_FULL ]
    then
        echo "error: Config file does not exist! ("$CONFIG_FULL")"
        continue
    fi
    cp $CONFIG_FULL $CONFIG.d/
    cd $CONFIG.d
    EACIRC_RUNS_BEGIN=1
    # submit all parts
    for RUN in `seq 1 $PARTS`
    do
        # for settings of custom variables, see eacirc.sh job script
        qsub -N $CONFIG-$RUN \
                     -l walltime="$(($FULLTIME / $PARTS)):00:00" \
                     -v EACIRC_RUNS=$(($EACIRC_RUNS / $PARTS)),EACIRC_RUNS_BEGIN=$EACIRC_RUNS_BEGIN,EACIRC_CONFIG=$CONFIG \
                     ~/eacirc-utils/metacentrum/single_job.sh
        EACIRC_RUNS_BEGIN="$(($EACIRC_RUNS_BEGIN + $EACIRC_RUNS / $PARTS))"
    done
    cd ..
    echo "Successfully created jobs for "$CONFIG"."
done

