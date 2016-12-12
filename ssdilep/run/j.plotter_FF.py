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
   
    ## configure the list of triggers 
    ## with eventual prescales and puts a
    ## trig list to the store for later cutflow
    ## ---------------------------------------
    loop += ssdilep.algs.vars.BuildTrigConfig(
        #required_triggers = ["HLT_mu20_L1MU15", "HLT_mu24", "HLT_mu50"],
        required_triggers = ["HLT_mu24", "HLT_mu50"],
        key               = 'muons',
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
    loop += ssdilep.algs.vars.VarsAlg(key_muons='muons',key_jets='jets')   

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
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='LeadMuIsLoose') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='LeadMuZ0SinTheta05') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt22') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247') 
    
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OneJet') 

    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.TrigPresc(
            use_avg   = True,
            key       = "DataUnPrescAvg",
            )
    
    #loop += ssdilep.algs.EvWeights.TrigPresc(
    #        use_avg   = False,
    #        key       = "DataUnPrescNoAvg",
    #        )
    
    # WARNING: no trigger correction available for HLT_mu20_L1MU15 
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list = ["HLT_mu24", "HLT_mu50"],
            mu_reco   = "Loose",
            mu_iso    = "FixedCutTightTrackOnly",
            key       = "MuTrigSFNUM1",
            scale     = None,
            )
    
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list = ["HLT_mu24", "HLT_mu50"],
            mu_reco   = "Loose",
            mu_iso    = "NotFixedCutTightTrackOnly",
            key       = "MuTrigSFDEN1",
            scale     = None,
            )
    
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list = ["HLT_mu24", "HLT_mu50"],
            mu_reco   = "Loose",
            mu_iso    = "Gradient",
            key       = "MuTrigSFNUM2",
            scale     = None,
            )
    
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list = ["HLT_mu24", "HLT_mu50"],
            mu_reco   = "Loose",
            mu_iso    = "Gradient",
            key       = "MuTrigSFDEN2",
            scale     = None,
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
    
    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.FF_hists.hist_list
    #hist_list += ssdilep.hists.PtOnly_hists.hist_list
    hist_list += ssdilep.hists.H2D_hists.hist_list
    
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## before any selection
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F0',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ],
            )
    
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F0',
            plot_all     = False,
            hist_list    = hist_list,
            do_var_check = True,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ],
            )
    ## F1
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F1',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F1',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    ## F2
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F2',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow50',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F2',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow50',None],
              ],
            )
    
    ## F3
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F3',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow30',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F3',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow30',None],
              ],
            )
    
    ## F4
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F4',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi28',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F4',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi28',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    ## F5
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F5',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi26',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F5',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi26',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    ## F6
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F6',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig2',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F6',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    ## F7
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F7',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig4',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F7',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    
    ## F8
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_NUM_F8',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoFixedCutTightTrackOnly',['MuSFFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt40',None],
              ['LeadMuD0Sig3',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKES_DEN_F8',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN1']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotFixedCutTightTrackOnly',['MuSFNotFixedCutTightTrackOnlyLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt40',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    
    
    """ 
    ## before any selection
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G0',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G0',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ],
            )
    
    ## G1
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G1',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G1',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    ## G2
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G2',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow50',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G2',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow50',None],
              ],
            )
    
    ## G3
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G3',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow30',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G3',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow30',None],
              ],
            )
    
    ## G4
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G4',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ['MuJetDphi28',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G4',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ['MuJetDphi28',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    ## G5
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G5',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ['MuJetDphi26',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G5',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ['MuJetDphi26',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    ## G6
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G6',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig2',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G6',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    ## G7
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G7',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig4',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G7',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
    
    
    ## G8
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_NUM_G8',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFNUM2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoGradient',['MuSFGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt40',None],
              ['LeadMuD0Sig3',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKES_DEN_G8',
            plot_all  = False,
            cut_flow  = [
              ['PassAndMatchPresc',['DataUnPrescAvg','MuTrigSFDEN2']],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotGradient',['MuSFNotGradientLoose']],
              ['MuJetDphi27',None],
              ['AllJetPt40',None],
              ['LeadMuD0Sig10',None],
              ['METlow40',None],
              ],
            )
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



