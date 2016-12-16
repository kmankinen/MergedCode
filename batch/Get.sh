#!/bin/bash
#PBS -S /bin/bash
#PBS -l walltime=24:00:00
#PBS -l pmem=1gb


STARTTIME=`date +%s`
date

echo 
echo "Environment variables..."
echo " User name:     $USER"
echo " User home:     $HOME"
echo " Queue name:    $PBS_O_QUEUE"
echo " Job name:      $PBS_JOBNAME"
echo " Job-id:        $PBS_JOBID"
echo " Work dir:      $PBS_O_WORKDIR"
echo " Submit host:   $PBS_O_HOST"
echo " Worker node:   $HOSTNAME"
echo " Temp dir:      $TMPDIR"
echo " parameters passed: $*"
echo 

echo " SCRIPT:        $SCRIPT"
echo " TREEFILE:      $TREEFILE"
echo " METAFILE:      $METAFILE"
echo " CUTFLOWFILE:   $CUTFLOWFILE"
echo " MERGEDTREE:    $MERGEDTREE"
echo " MERGEDMETA:    $MERGEDMETA"
echo " MERGEDCUTFLOW: $MERGEDCUTFLOW"
echo " OUTTREE:       $OUTTREE"
echo " OUTMETA:       $OUTMETA"
echo " OUTCUTFLOW:    $OUTCUTFLOW"
echo " MERGED:        $MERGED"
echo " OUTMERGED:     $OUTMERGED"
echo " NCORES:        $NCORES"

echo
export 

MYDIR=Get_${RANDOM}${RANDOM}

# ----------------
# This is the job!
# ----------------

export X509_USER_PROXY=/coepp/cephfs/mel/fscutti/jobdir/x509up_u1132
setupATLAS
lsetup rucio
lsetup root

# -----------------------------
# avoid to fuck the cluster up:
# -----------------------------

cgcreate -a ${USER} -t ${USER} -g cpuset,cpu,memory:${USER}/${PBS_JOBID}
cp /cgroup/cpuset/${USER}/cpuset.mems /cgroup/cpuset/${USER}/cpuset.cpus /cgroup/cpuset/${USER}/${PBS_JOBID}
MEMLIMIT="$((4 * ${NCORES}))"
echo "${MEMLIMIT}000000000" > /cgroup/cpuset/${USER}/${PBS_JOBID}/memory.limit_in_bytes
echo $$ > /cgroup/cpuset/${USER}/${PBS_JOBID}/tasks
echo ""


echo "executing job..."

echo "-----> ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "-----> rm -rf ${MYDIR}"
rm -rf ${MYDIR}

#echo "-----> rm -rf *.root"
#rm -rf *.root

echo "-----> ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "-----> mkdir ${TMPDIR}/${MYDIR} "
mkdir ${TMPDIR}/${MYDIR} 

echo "-----> ls ${TMPDIR} -la"
ls ${TMPDIR} -la


# ----------------------------
# download and merge tree file
# ----------------------------
echo "-----> rucio download --dir=${TMPDIR}/${MYDIR} ${TREEFILE}"
rucio download --dir=${TMPDIR}/${MYDIR} ${TREEFILE}

echo "-----> ls ${TMPDIR}/${MYDIR}/${TREEFILE} -la"
ls ${TMPDIR}/${MYDIR}/${TREEFILE} -la

echo "-----> cp -rf ${TMPDIR}/${MYDIR}/${TREEFILE} ${OUTTREE}"
cp -rf ${TMPDIR}/${MYDIR}/${TREEFILE} ${OUTTREE}

echo "-----> cd ${TMPDIR}/${MYDIR}/${TREEFILE}"
cd ${TMPDIR}/${MYDIR}/${TREEFILE}

echo "-----> hadd ${MERGEDTREE} *.root*"
hadd ${MERGEDTREE} *.root*

echo "-----> cp ${MERGEDTREE} ${TMPDIR}/${MYDIR}"
cp ${MERGEDTREE} ${TMPDIR}/${MYDIR}

echo "-----> cd ${TMPDIR}/${MYDIR}"
cd ${TMPDIR}/${MYDIR}

echo "-----> rm -rf ${TMPDIR}/${MYDIR}/${TREEFILE}"
rm -rf ${TMPDIR}/${MYDIR}/${TREEFILE}

echo "-----> ls ${TMPDIR}/${MYDIR} -la"
ls ${TMPDIR}/${MYDIR} -la


# ----------------------------
# download and merge meta file
# ----------------------------
echo "-----> rucio download --dir=${TMPDIR}/${MYDIR} ${METAFILE}"
rucio download --dir=${TMPDIR}/${MYDIR} ${METAFILE}

echo "-----> ls ${TMPDIR}/${MYDIR}/${METAFILE} -la"
ls ${TMPDIR}/${MYDIR}/${METAFILE} -la

echo "-----> cp -rf ${TMPDIR}/${MYDIR}/${METAFILE} ${OUTMETA}"
cp -rf ${TMPDIR}/${MYDIR}/${METAFILE} ${OUTMETA}

echo "-----> cd ${TMPDIR}/${MYDIR}/${METAFILE}"
cd ${TMPDIR}/${MYDIR}/${METAFILE}

echo "-----> hadd ${MERGEDMETA} *.root*"
hadd ${MERGEDMETA} *.root*

echo "-----> cp ${MERGEDMETA} ${TMPDIR}/${MYDIR}"
cp ${MERGEDMETA} ${TMPDIR}/${MYDIR}

echo "-----> cd ${TMPDIR}/${MYDIR}"
cd ${TMPDIR}/${MYDIR}

echo "-----> rm -rf ${TMPDIR}/${MYDIR}/${METAFILE}"
rm -rf ${TMPDIR}/${MYDIR}/${METAFILE}

echo "-----> ls ${TMPDIR}/${MYDIR} -la"
ls ${TMPDIR}/${MYDIR} -la


# -------------------------------
# download and merge cutflow file
# -------------------------------
echo "-----> rucio -v get --dir=${TMPDIR}/${MYDIR} ${CUTFLOWFILE}"
rucio -v get --dir=${TMPDIR}/${MYDIR} ${CUTFLOWFILE}

echo "-----> ls ${TMPDIR}/${MYDIR}/${CUTFLOWFILE} -la"
ls ${TMPDIR}/${MYDIR}/${CUTFLOWFILE} -la

echo "-----> cp -rf ${TMPDIR}/${MYDIR}/${CUTFLOWFILE} ${OUTCUTFLOW}"
cp -rf ${TMPDIR}/${MYDIR}/${CUTFLOWFILE} ${OUTCUTFLOW}

echo "-----> cd ${TMPDIR}/${MYDIR}/${CUTFLOWFILE}"
cd ${TMPDIR}/${MYDIR}/${CUTFLOWFILE}

echo "-----> hadd ${MERGEDCUTFLOW} *.root*"
hadd ${MERGEDCUTFLOW} *.root*

echo "-----> cp ${MERGEDCUTFLOW} ${TMPDIR}/${MYDIR}"
cp ${MERGEDCUTFLOW} ${TMPDIR}/${MYDIR}

echo "-----> cd ${TMPDIR}/${MYDIR}"
cd ${TMPDIR}/${MYDIR}

echo "-----> rm -rf ${TMPDIR}/${MYDIR}/${CUTFLOWFILE}"
rm -rf ${TMPDIR}/${MYDIR}/${CUTFLOWFILE}

echo "-----> ls ${TMPDIR}/${MYDIR} -la"
ls ${TMPDIR}/${MYDIR} -la

# ----------------------
# merge cutflow and tree
# ----------------------
echo "-----> hadd ${MERGED} ${MERGEDTREE} ${MERGEDMETA} ${MERGEDCUTFLOW}"
hadd ${MERGED} ${MERGEDTREE} ${MERGEDMETA} ${MERGEDCUTFLOW}

echo "-----> ls ${TMPDIR}/${MYDIR} -la"
ls ${TMPDIR}/${MYDIR} -la

echo "-----> cp ${MERGED} ${OUTMERGED}"
cp ${MERGED} ${OUTMERGED}

echo "-----> cd ${TMPDIR}"
cd ${TMPDIR}

echo "-----> rm -rf ${MYDIR}"
rm -rf ${MYDIR}

echo "-----> ls ${TMPDIR} -la"
ls ${TMPDIR} -la

# EOF

