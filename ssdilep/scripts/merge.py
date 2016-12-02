## modules
import ROOT

import histmgr
import funcs
import os

from ssdilep.samples import samples
from ssdilep.plots   import vars_mumu
from systematics     import *

from optparse import OptionParser


#-----------------
# input
#-----------------
parser = OptionParser()
parser.add_option('-v', '--var', dest='vname',
                  help='varable name',metavar='VAR',default=None)
parser.add_option('-r', '--reg', dest='region',
                  help='region name',metavar='REG',default=None)
parser.add_option('-l', '--lab', dest='label',
                  help='region label',metavar='LAB',default=None)
parser.add_option('-c', '--icut', dest='icut',
                  help='number of cuts',metavar='ICUT',default=None)
parser.add_option('-p', '--makeplot', dest='makeplot',
                  help='make plot',metavar='MAKEPLOT',default=None)
parser.add_option('-i', '--input', dest='indir',
                  help='input directory',metavar='INDIR',default=None)
parser.add_option('-o', '--output', dest='outdir',
                  help='output directory',metavar='OUTDIR',default=None)
parser.add_option('-f', '--fakest', dest='fakest',
                  help='choose fake estimate',metavar='FAKEST',default=None)
parser.add_option('-t', '--tag', dest='tag',
                  help='outfile tag',metavar='TAG',default=None)


(options, args) = parser.parse_args()

#-----------------
# Configuration
#-----------------
#lumi =  18232.8
lumi =  33257.2 + 3212.96

# Control regions
plotsfile = []
if options.makeplot == "False":
  plotsfile.append("hists")
plotsfile.append(options.vname)
plotsfile.append(options.region)
plotsfile.append(options.tag)

for s in plotsfile:
  if not s: plotsfile.remove(s)

plotsfile = "_".join(plotsfile)+".root"
plotsfile = os.path.join(options.outdir,plotsfile)

ROOT.gROOT.SetBatch(True)
hm = histmgr.HistMgr(basedir=options.indir,target_lumi=lumi)

#-----------------
# Samples        
#-----------------

## data
data = samples.data
## backgrounds 

"""
mc_backgrounds = [
    #samples.diboson_sherpa,
    #samples.diboson_incl_sherpa,
    ##samples.diboson_powheg,
    samples.WenuSherpa22,
    samples.WmunuSherpa22,
    samples.WtaunuSherpa22,
    samples.ZeeSherpa22,
    samples.ZmumuSherpa22,
    samples.ZtautauSherpa22,
    #samples.ttX,
    samples.singletop,
    samples.ttbar,
   ]
"""
mc_backgrounds = [
    ##samples.diboson_sherpa,
    #samples.diboson_incl_sherpa,
    samples.WenuSherpa22,
    samples.WmunuSherpa22,
    samples.WtaunuSherpa22,
    samples.ZeeSherpa22,
    samples.ZmumuSherpa22,
    samples.ZtautauSherpa22,
    #samples.ttX,
    samples.singletop,
    samples.ttbar,
   ]
"""
mc_backgrounds = [
    ##samples.diboson_sherpa,
    ##samples.diboson_powheg,
    samples.WenuPowheg,
    samples.WmunuPowheg,
    samples.WtaunuPowheg,
    samples.ZeePowheg,
    samples.ZmumuPowheg,
    samples.ZtautauPowheg,
    ##samples.ttX,
    samples.singletop,
    ##samples.ttbar,
    #fakes_mumu,
    ]
"""

fakes_mumu = samples.fakes.copy()

## signals
mumu_signals = []
#mumu_signals.append(samples.all_DCH)
#mumu_signals.append(samples.DCH800)



#--------------
# Estimators
#--------------
for s in mc_backgrounds + mumu_signals + [data]: 
    histmgr.load_base_estimator(hm,s)
"""
if "_SIG" in options.region:
  prefix = options.region.split("_")[:1][0]
  for s in mc_backgrounds + mumu_signals + [data]: 
    s.estimator = histmgr.AddEstimator(
      sample=s,
      hm=hm,
      #regions = [prefix+"_TT",prefix+"_TTT",prefix+"_TTTT"],
      regions = [prefix+"_TT"],
      )
"""
if options.fakest == "FakeFactor":
  fakes_mumu.estimator = histmgr.FakeEstimator(
      hm=hm, 
      sample=fakes_mumu,
      data_sample = data,
      mc_samples = mc_backgrounds )

elif options.fakest == "Subtraction":
  fakes_mumu.estimator = histmgr.DataBkgSubEstimator(
     hm=hm,
     sample=fakes_mumu,
     data_sample=data,
     background_samples=mc_backgrounds,
     )

else:
  print "WARNING: no estimator for fake bkg!!!"


#-----------------
# Systematics       
#-----------------
# just an example ...
mc_sys = [
    SYS1, 
    SYS2,
    ]

## set mc systematics
#for s in mc_backgrounds + mumu_signals:
#    s.estimator.add_systematics(mc_sys)

fakes_mumu.estimator.add_systematics(FF)

mumu_vdict  = vars_mumu.vars_dict

#-----------------
# Plotting 
#-----------------

## order backgrounds for plots
"""
mumu_backgrounds = [
    ##samples.diboson_sherpa,
    #samples.diboson_incl_sherpa,
    ##samples.diboson_powheg,
    samples.WenuSherpa22,
    samples.WmunuSherpa22,
    samples.WtaunuSherpa22,
    samples.ZeeSherpa22,
    samples.ZmumuSherpa22,
    samples.ZtautauSherpa22,
    #samples.ttX,
    samples.singletop,
    samples.ttbar,
    fakes_mumu,
    ]
"""
mumu_backgrounds = [
    #samples.diboson_sherpa,
    #samples.diboson_incl_sherpa,
    samples.WenuSherpa22,
    samples.WmunuSherpa22,
    samples.WtaunuSherpa22,
    samples.ZeeSherpa22,
    samples.ZmumuSherpa22,
    samples.ZtautauSherpa22,
    #samples.ttX,
    samples.singletop,
    samples.ttbar,
    #fakes_mumu,
    ]
"""
mumu_backgrounds = [
    ##samples.diboson_sherpa,
    ##samples.diboson_powheg,
    samples.WenuPowheg,
    samples.WmunuPowheg,
    samples.WtaunuPowheg,
    samples.ZeePowheg,
    samples.ZmumuPowheg,
    samples.ZtautauPowheg,
    ##samples.ttX,
    samples.singletop,
    ##samples.ttbar,
    #fakes_mumu,
    ]
"""

if options.makeplot == "True":
 funcs.plot_hist(
    backgrounds   = mumu_backgrounds,
    signal        = mumu_signals, 
    data          = data,
    region        = options.region,
    label         = options.label,
    histname      = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
    xmin          = mumu_vdict[options.vname]['xmin'],
    xmax          = mumu_vdict[options.vname]['xmax'],
    rebin         = mumu_vdict[options.vname]['rebin'],
    log           = mumu_vdict[options.vname]['log'],
    icut          = int(options.icut),
    #sys_dict      = sys_dict,
    sys_dict      = None,
    do_ratio_plot = False,
    save_eps      = True,
    plotsfile     = plotsfile,
    )

else:
 funcs.write_hist(
         backgrounds = mumu_backgrounds,
         signal      = mumu_signals, # This can be a list
         data        = data,
         region      = options.region,
         icut        = int(options.icut),
         histname    = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
         #rebin       = mumu_vdict[options.vname]['rebin'],
         rebin       = 1,
         sys_dict    = None,
         outname     = plotsfile
         )
 ## EOF



