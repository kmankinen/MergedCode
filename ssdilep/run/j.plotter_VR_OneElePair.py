#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
j.postprocessor.py
"""

## std modules
import os,re

## ROOT
import ROOT
ROOT.gROOT.SetBatch(True)

## my modules
import pyframe

## local modules
import ssdilep

GeV = 1000.0


#_____________________________________________________________________________
def analyze(config):
  
    ##-------------------------------------------------------------------------
    ## setup
    ##-------------------------------------------------------------------------
    config['tree']       = 'physics/nominal'
    config['do_var_log'] = True
    main_path = os.getenv('MAIN')
    
    ## build chain
    chain = ROOT.TChain(config['tree'])
    for fn in config['input']: chain.Add(fn)

    ##-------------------------------------------------------------------------
    ## systematics 
    ##-------------------------------------------------------------------------
    """
    pass systematics on the command line like this:
    python j.plotter.py --config="sys:SYS_UP"
    """
    config.setdefault('sys',None)
    systematic = config['sys']

    sys_ff    = None

    if   systematic == None: pass
    elif systematic == 'FF_UP':      sys_ff    = 'up'
    elif systematic == 'FF_DN':      sys_ff    = 'dn'
    else: 
        assert False, "Invalid systematic %s!"%(systematic)


    ##-------------------------------------------------------------------------
    ## event loop
    ##-------------------------------------------------------------------------
    loop = pyframe.core.EventLoop(name='ssdilep',
                                  sampletype=config['sampletype'],
                                  samplename=config['samplename'],
                                  outfile=config['samplename']+".root",
                                  quiet=False,
                                  )
    
    ## configure the list of triggers 
    ## with eventual prescales and puts a
    ## trig list to the store for later cutflow
    ## ---------------------------------------

    loop += ssdilep.algs.vars.BuildTrigConfig(
        #required_triggers = ["HLT_mu26_imedium","HLT_mu50"], # @todo
        key               = 'electrons',
        )

    ## build and pt-sort objects
    ## ---------------------------------------
    loop += pyframe.algs.ListBuilder(
        prefixes = ['muon_','el_','jet_'],
        keys = ['muons','electrons','jets'],
        )
    loop += pyframe.algs.AttachTLVs(
        keys = ['muons','electrons','jets'],
        )
    # just a decoration of particles ...
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='muons',
        )

    loop += ssdilep.algs.vars.ParticlesBuilder(
       key='electrons',
       )

    ## build MET
    ## ---------------------------------------
    loop += ssdilep.algs.met.METCLUS(
        prefix='metFinalClus',
        key = 'met_clus',
        )
    loop += ssdilep.algs.met.METTRK(
        prefix='metFinalTrk',
        key = 'met_trk',
        )

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.LPXKfactor(cutflow='presel',key='weight_kfactor')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    
    # electron cuts for SSVR:

    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='PassHLT2e17lhloose')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ExactlyTwoLooseEleLooseLLHSS')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='Mass130GeV200LooseLLH')

    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OddSSElectrons')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllElePairsM20')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleLHLoose') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleEta247')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleZ0SinTheta05')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleIsoBound15')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllJetPt25')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHFilter')

    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='EleMass130GeV200')

    
    ## initialize and/or decorate objects
    ## ---------------------------------------
    loop += ssdilep.algs.vars.DiEleVars(key_electrons='electrons')   
    
    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.EvWeights.TrigPresc(
    #        use_avg   = True,
    #        SKIP      = True,
    #        key       = "DataUnPrescAvg",
    #        )

    """

    """

    ## objects
    ## +++++++++++++++++++++++++++++++++++++++


    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.Main_hists.hist_list
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## VR1
    ## ---------------------------------------

    """

    """ 
    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
    ## run the job
    ##-------------------------------------------------------------------------
    loop.run(chain, 0, config['events'],
            branches_on_file = config.get('branches_on_file'),
            do_var_log = config.get('do_var_log'),
            )
#______________________________________________________________________________
if __name__ == '__main__':
    pyframe.config.main(analyze)



