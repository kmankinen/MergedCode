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
                                  outfile='ntuple.root',
                                  quiet=False,
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
   
    ## initialize and/or decorate objects
    ## ---------------------------------------
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets')   

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OneMuon')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt22')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OneJet')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastTwoMuons') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoOSMuons')  
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt22') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TagAndProbeExist') 
    
    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_single_mu  = True,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Loose",
            mu_trig_chain = "HLT_mu26_imedium_OR_HLT_mu50",
            key           = "TrigSFTightIsoWP",
            scale         = None,
            )
    
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_single_mu  = True,
            mu_iso        = "NotGradient",
            mu_reco       = "Loose",
            mu_trig_chain = "HLT_mu26_imedium_OR_HLT_mu50",
            key           = "TrigSFLooseIsoWP",
            scale         = None,
            )
    
    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "MuSFTightIsoWP",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "NotGradient",
            mu_reco       = "Loose",
            key           = "MuSFLooseIsoWP",
            scale         = None,
            )


    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## Define 2 regions for trigger efficiency
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'PROBE_LOOSE',
            plot_all  = False,
            #obj_keys  = ["mu_pairs"],
            cut_flow  = [
              #['OneJet',None],
              ['LeadMuTruthFilter',None],
              #['LeadMuIsoTight',['MuLeadAllSF']],
              ['LeadMuIsoNotTight',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'PROBE_LOOSE_TRIGMATCHED',
            plot_all  = False,
            #obj_keys  = ["mu_pairs"],
            cut_flow  = [
              #['OneJet',None],
              ['MatchSingleMuIsoChain',None],
              ['PassSingleMuIsoChain',None],
              ['LeadMuTruthFilter',None],
              #['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['LeadMuIsoNotTight',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    
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



