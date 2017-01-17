#PBS -l walltime=20:00:00
#PBS -l pmem=1gb

#!/bin/bash
STARTTIME=`date +%s`
date

#-------------------------------- ENV VARS -------------------------------
echo 
echo "Environment variables..."
echo " User name:   $USER"
echo " User home:   $HOME"
echo " Queue name:  $PBS_O_QUEUE"
echo " Job name:    $PBS_JOBNAME"
echo " Job-id:      $PBS_JOBID"
echo " Task-id:     $PBS_ARRAYID"
echo " Work dir:    $PBS_O_WORKDIR"
echo " Submit host: $PBS_O_HOST"
echo " Worker node: $HOSTNAME"
echo " Temp dir:    $TMPDIR"
echo " parameters passed: $*"
echo 

echo " SCRIPT:      $SCRIPT"
echo " OUTFILE:     $OUTFILE"
echo " OUTPATH:     $OUTPATH"
echo " CONFIG:      $CONFIG"
echo " INTARBALL:   $INTARBALL"
echo " NCORES:      $NCORES"

echo
export 

MYDIR=Hist_${RANDOM}${RANDOM}

#-------------------------------- NODE CONFIG ------------------------------
echo "going to tmp node dir: $TMPDIR"
cd $TMPDIR

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "mkdir ${MYDIR}"
mkdir ${MYDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "cd ${MYDIR}"
cd ${MYDIR}

setupATLAS
lsetup root

## copy over working area
##echo "ls /data/fscutti"
##ls /data/fscutti

## copy over working area
echo "copying input tarball ${INTARBALL}..."
cp $INTARBALL .
date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"
echo "extracting input tarball..."
tar xzf *.tar.gz
date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"
echo "done setting working area"
ls -alh 

echo 
echo "setting up workarea..."
source setup.sh

echo 
echo "reading in config file '${CONFIG}', line ${PBS_ARRAYID}"
## READ IN CONFIG
line=`sed -n -e ${PBS_ARRAYID}p ${CONFIG}`
echo ${line}
arrIN=(${line//;/ });
SAMPLE=${arrIN[0]}
INPUT=${arrIN[1]}
SAMPLETYPE=${arrIN[2]}
CFG=${arrIN[3]}
echo "SAMPLE:     ${SAMPLE}"
echo "SAMPLETYPE: ${SAMPLETYPE}"
echo "INPUT:      ${INPUT}"
echo "CFG:        ${CFG}"


echo
echo "copying input locally..."
TMPINPUT="`mktemp ntuple.XXXXXXX`.root"
echo cp ${INPUT} ${TMPINPUT}
cp ${INPUT} ${TMPINPUT}

echo ""
echo "executing job..."
echo ${SCRIPT} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}"

# -----------------------------
# avoid to fuck the cluster up:
# -----------------------------

cgcreate -a ${USER} -t ${USER} -g cpuset,cpu,memory:${USER}/${PBS_JOBID}
cp /cgroup/cpuset/${USER}/cpuset.mems /cgroup/cpuset/${USER}/cpuset.cpus /cgroup/cpuset/${USER}/${PBS_JOBID}
MEMLIMIT="$((4 * ${NCORES}))"
echo "${MEMLIMIT}000000000" > /cgroup/cpuset/${USER}/${PBS_JOBID}/memory.limit_in_bytes
echo $$ > /cgroup/cpuset/${USER}/${PBS_JOBID}/tasks


${SCRIPT} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}"


echo "finished execution"

echo 
echo "preparing output dir..."
if [ ! -d ${OUTPATH} ]; then mkdir ${OUTPATH}; fi

echo "copying output"
echo cp ${OUTFILE} ${OUTPATH}/${SAMPLE}.root 
cp ${OUTFILE} ${OUTPATH}/${SAMPLE}.root
chmod a+r ${OUTPATH}/${SAMPLE}.root

echo "cd ${TMPDIR}"
cd ${TMPDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "rm -rf ${MYDIR}"
rm -rf ${MYDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "finished job"

date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"


