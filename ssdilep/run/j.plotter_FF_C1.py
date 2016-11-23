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

    sys_somesys    = None

    if   systematic == None: pass
    elif systematic == 'SOMESYS_UP':      sys_somesys    = 'up'
    elif systematic == 'SOMESYS_DN':      sys_somesys    = 'dn'
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

    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.TrigPresc(
            trig_chain = ["HLT_mu20_L1MU15", "HLT_mu24", "HLT_mu50"],
            key        = "DataUnPresc",
            )
    
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_single_mu  = True,
            mu_reco       = "Loose",
            mu_trig_chain = {"HLT_mu20_L1MU15":0, "HLT_mu24":1, "HLT_mu50":3},
            match_to_trig = "HLT_mu50",
            key           = "MuTrigSFRecoLoose",
            scale         = None,
            )
    
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_single_mu  = True,
            mu_reco       = "Medium",
            mu_trig_chain = {"HLT_mu20_L1MU15":0, "HLT_mu24":1, "HLT_mu50":3},
            match_to_trig = "HLT_mu50",
            key           = "MuTrigSFRecoMedium",
            scale         = None,
            )
    
    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "MuSFNotFixedCutTightTrackOnlyLoose",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "NotGradient",
            mu_reco       = "Loose",
            key           = "MuSFNotGradientLoose",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "MuSFFixedCutTightTrackOnlyLoose",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "Gradient",
            mu_reco       = "Loose",
            key           = "MuSFGradientLoose",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "MuSFFixedCutTightTrackOnlyMedium",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "Gradient",
            mu_reco       = "Medium",
            key           = "MuSFGradientMedium",
            scale         = None,
            )
    
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## FR1
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR1_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR1_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig15',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    ## FR2
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR2_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow30',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR2_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig15',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow30',None],
              ],
            )
    
    ## FR3
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR3_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow50',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR3_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig15',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow50',None],
              ],
            )
    
    ## FR4
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR4_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt40',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR4_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt40',None],
              ['LeadMuD0Sig15',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    ## FR5
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR5_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig2',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR5_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig15',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    ## FR6
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR6_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig4',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR6_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig15',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    
    ## FR7
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR7_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi28',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR7_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi28',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig15',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    ## FR8
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR8_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi26',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR8_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChain',['DataUnPresc']],
              ['PassSingleMuPrescChain',['MuTrigSFRecoLoose']],
              ['LeadMuIsLoose',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['LeadMuTruthFilter',None],
              ['MuJetDphi26',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig15',None],
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



