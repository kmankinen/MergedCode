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

#indir    = 'HistNewVREB'
#outdir   = 'PlotsNewVREB'

#indir    = 'HistFinalFF'
#outdir   = 'NewPlotsFinalFF'

indir    = 'HistNewTESTV1'
outdir   = 'PlotsNewTESTV1'

USER    = os.getenv('USER')
MAIN    = os.getenv('MAIN')

inpath  = os.path.join("/coepp/cephfs/mel",USER,ana)
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
JOBDIR    = "/coepp/cephfs/mel/%s/jobdir" % USER

#---------------------
# Batch jobs variables
#---------------------
INTARBALL = os.path.join(JOBDIR,'plotstarball_%s.tar.gz' % (time.strftime("d%d_m%m_y%Y_H%H_M%M_S%S")) )
SCRIPT    = os.path.join("./",ana,"scripts",'merge.py')

job_vars={}
job_vars['INTARBALL'] = INTARBALL
job_vars['OUTDIR']    = OUTDIR
job_vars['INDIR']     = INDIR
job_vars['SCRIPT']    = SCRIPT

#fake_estimate = "FullRegions"
#fake_estimate = "ReducedRegions"
fake_estimate = "Subtraction"

regions = {}
# use it as such:
#regions["FOLDERNAME"]     = [icut, "plot label"]


#regions["Z_OS"]   = [6,  "OS", "incl"]
#regions["Z_SS"]   = [6,  "SS", "incl"]

#regions["FAKESVR1_MAINREG"] = [5, "VR",   "V1"]
#regions["FAKESVR1_TT"]      = [5, "TT",   "V1"]
regions["FAKESVR1_LL"]      = [5, "LL",   "V1"]
regions["FAKESVR1_TL"]      = [5, "TL",   "V1"]
regions["FAKESVR1_LT"]      = [5, "LT",   "V1"]
#regions["FAKESVR1_TTL"]     = [5, "TTL",  "V1"]
#regions["FAKESVR1_TLT"]     = [5, "TLT",  "V1"]
#regions["FAKESVR1_LTT"]     = [5, "LTT",  "V1"]
#regions["FAKESVR1_TTTL"]    = [5, "TTTL", "V1"]
#regions["FAKESVR1_TTLT"]    = [5, "TTLT", "V1"]
#regions["FAKESVR1_TLTT"]    = [5, "TLTT", "V1"]
#regions["FAKESVR1_LTTT"]    = [5, "LTTT", "V1"]


#regions["FAKES_NUM_F0"]   = [2,  "numerator", "acc"]
#regions["FAKES_DEN_F0"]   = [2,  "denominator", "acc"]

#regions["FAKES_NUM_F1"]   = [6,  "numerator", "acc"]
#regions["FAKES_DEN_F1"]   = [6,  "denominator", "acc"]


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


for REG,OPT in regions.iteritems():
  vars_list = plots.vars_mumu.vars_list
  #vars_list = plots.vars_fakes.vars_list

  for var in vars_list:

    job_vars['VAR']      = var.name
    job_vars['REG']      = REG
    job_vars['ICUT']     = OPT[0]
    job_vars['LAB']      = OPT[1]
    job_vars['TAG']      = OPT[2]
    job_vars['MAKEPLOT'] = True
    job_vars['FAKEST']   = fake_estimate
    
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

