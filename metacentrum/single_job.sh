#!/bin/bash
# ===== PBS job settings =====
# name of the PBS job
#PBS -N EACirc
# number of nodes with specification (1 node, 1 processor per node), :gpu=1
#PBS -l select=1:ncpus=1:mem=200mb:scratch_local=1gb
# # queue for gpu runs: -q gpu or -q gpu_long
# caps(pbs) -q gpu
# email notification at the Beginning, Abortion and End
#PBS -m a

# ===== MetaCentrum intro ===== 
# cleaning scratch disk in case of failure and termination
trap 'clean_scratch' TERM EXIT
# directory of qsub call accessible in $PBS_O_WORKDIR
# scratch directory accessible in $SCRATCHDIR
# swithicng to working directory 
cd $SCRATCHDIR
 
# ===== EACirc job specification  =====
# if defined, keep the environment value, otherwise use the value provided
EACIRC_BINARY=${EACIRC_BINARY:-"eacirc-v4"}
# configuration filename (file must be present in input/ouput directory)
EACIRC_CONFIG=${EACIRC_CONFIG:-"config.xml"}
# number of repetitions/runs
EACIRC_RUNS=${EACIRC_RUNS:-1}
# starting ID number for multiple runs
EACIRC_RUNS_BEGIN=${EACIRC_RUNS_BEGIN:-1}

# ===== EACirc constants and locations =====
# files to copy at the end along with IDs stored in associative array
declare -A EACIRC_OUTFILES
EACIRC_OUTFILES=( [config.json]=00 [eacirc.log]=01 [pvals.txt]=02 ) # [scores.txt]=03 # add this if you want to inspect p-vals during epoch
# root EACirc NFS location
EACIRC_ROOT=/storage/brno2/home/mukrop/eacirc
# network directory with binaries
EACIRC_BINDIR=$EACIRC_ROOT/bin
# network directory for inputs/outputs
EACIRC_DATADIR=$PBS_O_WORKDIR
## uncomment to validate experiments with qrng
## network directory with QRNG data
#EACIRC_QRNGDIR=$EACIRC_ROOT/qrng
## scratch directory with QRNG data
#SCRATCH_QRNGDIR=$SCRATCHDIR/qrng
# scratch working directory for all computations
SCRATCH_RUNDIR=$SCRATCHDIR/run
# scratch results directory
SCRATCH_RESULTSDIR=$SCRATCHDIR/results

# ===== EACirc job intro =====
## uncomment to validate experiments with qrng
## prepare qrng (copy to scratch storage)
#mkdir -p $SCRATCH_QRNGDIR
#cp $EACIRC_QRNGDIR/*.bin $SCRATCH_QRNGDIR/
# prepare the binary
if [ ! -x $EACIRC_BINDIR/$EACIRC_BINARY ]
then
    echo "error: binary file does not exist or is not executable ("$EACIRC_RUNDIR/$EACIRC_BINARY")"
    exit -1
fi
mkdir -p $SCRATCH_RUNDIR
cp $EACIRC_BINDIR/$EACIRC_BINARY $SCRATCH/
# prepare results directory
mkdir -p $SCRATCH_RESULTSDIR
# prepare the configuration file
if [ ! -f $EACIRC_DATADIR/$EACIRC_CONFIG ]
then
    echo "error: configuration file does not exist ("$EACIRC_DATADIR/$EACIRC_CONFIG")"
    exit -1
fi
cp $EACIRC_DATADIR/$EACIRC_CONFIG $SCRATCH/

# ===== actual computation =====
cd $SCRATCH_RUNDIR
#                   05 = max 10^5 runs per experiment
for RUN in `seq -f %05g $EACIRC_RUNS_BEGIN $(($EACIRC_RUNS_BEGIN + EACIRC_RUNS - 1))`
do
    # prepare binary and config
    cp ../$EACIRC_BINARY .
    cp ../$EACIRC_CONFIG .
    # run computation (suppress output log to releave MetaCentrum outfile handling)
    ./$EACIRC_BINARY --config=$EACIRC_CONFIG --no-pvals &>eacirc.log # --no-pvals do not produce p-vals.txt
    cat eacirc.log
    # copy results
    mkdir -p $SCRATCH_RESULTSDIR/$RUN
    # iterate through all output files
    for FILE in ${!EACIRC_OUTFILES[@]}
    do
        cp $FILE $SCRATCH_RESULTSDIR/$RUN/${EACIRC_OUTFILES[$FILE]}_$FILE 2>/dev/null
    done
    rm -f *
done

# ===== EACirc job outro =====
# copying out results (in case of failure, data are left on scratch and the user is informed)
# copy results folder back to NFS system
cp -r $SCRATCH_RESULTSDIR/* $EACIRC_DATADIR || export CLEAN_SCRATCH=false


