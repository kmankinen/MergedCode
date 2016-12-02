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

#indir    = 'HistSysVR'
#outdir   = 'PlotsSysVR'

indir    = 'HistNewAcceptZ'
outdir   = 'PlotsNewAcceptZ'

#indir    = 'HistRejectZ'
#outdir   = 'PlotsRejectZ'

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

fake_estimate = "FakeFactor"
#fake_estimate = "Subtraction"

regions = {}
# use it as such:
#regions["FOLDERNAME"]     = [icut, "plot label"]


#regions["Z_OS"]   = [6,  "OS", "incl"]
#regions["Z_SS"]   = [6,  "SS", "incl"]

"""
regions["FAKESVR1_NUM"]     = [4,  "VR", "incl"]
regions["FAKESVR1_LLDEN"]   = [4,  "VR", "incl"]
regions["FAKESVR1_TLDEN"]   = [4,  "VR", "incl"]
regions["FAKESVR1_LTDEN"]   = [4,  "VR", "incl"]

regions["FAKESVR2_NUM"]     = [4,  "VR", "incl"]
regions["FAKESVR2_LLDEN"]   = [4,  "VR", "incl"]
regions["FAKESVR2_TLDEN"]   = [4,  "VR", "incl"]
regions["FAKESVR2_LTDEN"]   = [4,  "VR", "incl"]

regions["FAKESVR3_NUM"]     = [4,  "VR", "incl"]
regions["FAKESVR3_LLDEN"]   = [4,  "VR", "incl"]
regions["FAKESVR3_TLDEN"]   = [4,  "VR", "incl"]
regions["FAKESVR3_LTDEN"]   = [4,  "VR", "incl"]

regions["FAKESVR4_NUM"]     = [4,  "VR", "incl"]
regions["FAKESVR4_LLDEN"]   = [4,  "VR", "incl"]
regions["FAKESVR4_TLDEN"]   = [4,  "VR", "incl"]
regions["FAKESVR4_LTDEN"]   = [4,  "VR", "incl"]

regions["FAKESVR5_NUM"]     = [5,  "VR", "incl"]
regions["FAKESVR5_LLDEN"]   = [5,  "VR", "incl"]
regions["FAKESVR5_TLDEN"]   = [5,  "VR", "incl"]
regions["FAKESVR5_LTDEN"]   = [5,  "VR", "incl"]

regions["FAKESVR6_NUM"]     = [5,  "VR", "incl"]
regions["FAKESVR6_LLDEN"]   = [5,  "VR", "incl"]
regions["FAKESVR6_TLDEN"]   = [5,  "VR", "incl"]
regions["FAKESVR6_LTDEN"]   = [5,  "VR", "incl"]

regions["FAKESVR7_NUM"]     = [5,  "VR", "incl"]
regions["FAKESVR7_LLDEN"]   = [5,  "VR", "incl"]
regions["FAKESVR7_TLDEN"]   = [5,  "VR", "incl"]
regions["FAKESVR7_LTDEN"]   = [5,  "VR", "incl"]

"""


regions["FAKES_NUM_F0"]   = [2,  "numerator", "acc"]
regions["FAKES_DEN_F0"]   = [2,  "denominator", "acc"]

regions["FAKES_NUM_F1"]   = [6,  "numerator", "acc"]
regions["FAKES_DEN_F1"]   = [6,  "denominator", "acc"]

"""
regions["FAKES_NUM_F2"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_F2"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_F3"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_F3"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_F4"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_F4"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_F5"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_F5"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_F6"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_F6"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_F7"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_F7"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_F8"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_F8"]   = [7,  "di-jet numerator", "acc"]


regions["FAKES_NUM_G0"]   = [3,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G0"]   = [3,  "di-jet numerator", "acc"]

regions["FAKES_NUM_G1"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G1"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_G2"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G2"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_G3"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G3"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_G4"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G4"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_G5"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G5"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_G6"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G6"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_G7"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G7"]   = [7,  "di-jet numerator", "acc"]

regions["FAKES_NUM_G8"]   = [7,  "di-jet numerator", "acc"]
regions["FAKES_DEN_G8"]   = [7,  "di-jet numerator", "acc"]
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

