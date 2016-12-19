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

indir    = 'HistNewVR'
outdir   = 'PlotsNewVR'

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
fake_estimate = "ReducedRegions"
#fake_estimate = "Subtraction"

regions = {}
# use it as such:
#regions["FOLDERNAME"]     = [icut, "plot label"]


#regions["Z_OS"]   = [6,  "OS", "incl"]
#regions["Z_SS"]   = [6,  "SS", "incl"]

regions["FAKESVR6_MAINREG"] = [4, "VR",   "red"]
#regions["FAKESVR6_TT"]      = [4, "TT",   "full"]
#regions["FAKESVR6_LL"]      = [4, "LL",   "full"]
#regions["FAKESVR6_TL"]      = [4, "TL",   "full"]
#regions["FAKESVR6_LT"]      = [4, "LT",   "full"]
#regions["FAKESVR6_TTL"]     = [4, "TTL",  "full"]
#regions["FAKESVR6_TLT"]     = [4, "TLT",  "full"]
#regions["FAKESVR6_LTT"]     = [4, "LTT",  "full"]
#regions["FAKESVR6_TTTL"]    = [4, "TTTL", "full"]
#regions["FAKESVR6_TTLT"]    = [4, "TTLT", "full"]
#regions["FAKESVR6_TLTT"]    = [4, "TLTT", "full"]
#regions["FAKESVR6_LTTT"]    = [4, "LTTT", "full"]


"""
regions["FAKES_NUM_F0"]   = [2,  "numerator", "acc"]
regions["FAKES_DEN_F0"]   = [2,  "denominator", "acc"]

regions["FAKES_NUM_F1"]   = [6,  "numerator", "acc"]
regions["FAKES_DEN_F1"]   = [6,  "denominator", "acc"]
"""


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

