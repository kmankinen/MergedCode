#!/usr/bin/python

import os
import subprocess
import time
from ssdilep import plots

def make_tag(cat,var):
  return '_'.join([cat,var])

#---------------------
# Set environment
#---------------------
# Environment variables defined in batchsetup.sh

ana      = 'ssdilep'

#indir    = 'HistSystem'
#outdir   = 'PlotsSystem'

#indir    = 'HistVR'
#outdir   = 'PlotsVR'

#indir    = 'HistNewFF'
#outdir   = 'PlotsNewFF'

indir    = 'HistFinFF'
outdir   = 'PlotsFinFF'

inpath = os.path.join("/data/fscutti",ana)

USER    = os.getenv('USER')
MAIN    = os.getenv('MAIN')
INDIR   = os.path.join(inpath,indir)  
OUTDIR  = os.path.join(inpath,outdir)

if not os.path.isdir(OUTDIR): os.makedirs(OUTDIR)
if not os.path.isdir(OUTDIR+"/"+"log"): os.makedirs(OUTDIR+"/"+"log")

#---------------------
# Batch jobs options
#---------------------
AUTOBUILD = True
QUEUE     = 'short'
BEXEC     = 'Plots.sh'
JOBDIR    = "/data/fscutti/jobdir" 

#---------------------
# Batch jobs variables
#---------------------
INTARBALL = os.path.join(JOBDIR,'plotstarball_%s.tar.gz' % (time.strftime("d%d_m%m_y%Y_H%H_M%M_S%S")) )
SCRIPT    = os.path.join("./",ana,"scripts",'batch_merge.py')

job_vars={}
job_vars['INTARBALL'] = INTARBALL
job_vars['OUTDIR']    = OUTDIR
job_vars['INDIR']     = INDIR
job_vars['SCRIPT']    = SCRIPT

regions = []
#regions.append("NN_NOM")
#regions.append("ND_NOM")
#regions.append("DN_NOM")
#regions.append("DD_NOM")
#regions.append("NN_FAKES")
#regions.append("ND_FAKES")
#regions.append("DN_FAKES")
#regions.append("DD_FAKES")
#regions.append("ZCR")

#regions.append("FAKESVR_MERGED")

#regions.append("SIG_NUM")
#regions.append("SIG_DEN_TL")
#regions.append("SIG_DEN_LT")
#regions.append("SIG_DEN_LL")

regions.append("FAKESFR1_NUM")
regions.append("FAKESFR1_DEN")
regions.append("FAKESFR2_NUM")
regions.append("FAKESFR2_DEN")
regions.append("FAKESFR3_NUM")
regions.append("FAKESFR3_DEN")
regions.append("FAKESFR4_NUM")
regions.append("FAKESFR4_DEN")
regions.append("FAKESFR5_NUM")
regions.append("FAKESFR5_DEN")
regions.append("FAKESFR6_NUM")
regions.append("FAKESFR6_DEN")
regions.append("FAKESFR7_NUM")
regions.append("FAKESFR7_DEN")
regions.append("FAKESFR8_NUM")
regions.append("FAKESFR8_DEN")
#regions.append("FAKESFR9_NUM")
#regions.append("FAKESFR9_DEN")
#regions.append("FAKESFR10_NUM")
#regions.append("FAKESFR10_DEN")
#regions.append("FAKESFR11_NUM")
#regions.append("FAKESFR11_DEN")
#regions.append("FAKESFR12_NUM")
#regions.append("FAKESFR12_DEN")
#regions.append("FAKESFR13_NUM")
#regions.append("FAKESFR13_DEN")
#regions.append("FAKESFR14_NUM")
#regions.append("FAKESFR14_DEN")
#regions.append("FAKESFR15_NUM")
#regions.append("FAKESFR15_DEN")

#regions.append("FAKESVR1_NUM")
#regions.append("FAKESVR1_DEN")

#---------------------
# Make input tarball
#---------------------
if os.path.exists(os.path.join(INTARBALL)):
  print 'removing existing tarball %s...'% (INTARBALL)
  cmd = 'rm %s' % (INTARBALL)
  m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
  m.communicate()[0]

print 'building input tarball %s...'% (INTARBALL)
cmd = 'cd %s; make -f Makefile.plots TARBALL=%s' % (MAIN,INTARBALL)
m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
m.communicate()[0]


for REG in regions:
  vars_list = plots.vars_mumu.vars_list
  #vars_list = plots.vars_fakes.vars_list

  for var in vars_list:

    job_vars['VAR'] = var.name
    job_vars['REG'] = REG
    
    VARS = []
    
    for vname in job_vars.keys(): VARS += ['%s=%s' % (vname,job_vars[vname])]
    
    cmd = 'qsub'
    cmd += " -q %s" % QUEUE
    cmd += ' -v "%s"' % (','.join(VARS))
    cmd += ' -N j.plots.%s' % (make_tag(REG,job_vars['VAR']))
    cmd += ' -o %s/log' % (OUTDIR)
    cmd += ' -e %s/log' % (OUTDIR)
    cmd += ' %s' % BEXEC
    print cmd
    m = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    print m.communicate()[0]
 
 
## EOF

