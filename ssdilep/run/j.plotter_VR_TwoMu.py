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
    
    ## configure the list of triggers 
    ## with eventual prescales and puts a
    ## trig list to the store for later cutflow
    ## ---------------------------------------
    loop += ssdilep.algs.vars.BuildTrigConfig(
        required_triggers = ["HLT_mu26_imedium", "HLT_mu50"],
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
    loop += ssdilep.algs.EvWeights.LPXKfactor(cutflow='presel',key='weight_kfactor')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastTwoSSMuons') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllPairsM20') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='EleVeto') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuLoose') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt22') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='PassDiMuChain') 

    
    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list     = ["HLT_mu26_imedium_OR_HLT_mu50"],
            mu_reco       = "Loose",
            key           = "MuTrigSFRecoLoose",
            scale         = None,
            )
    
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Tight",
            mu_sublead_type = "Loose",
            key             = "EffCorrTL",
            scale           = None,
            )
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Loose",
            mu_sublead_type = "Tight",
            key             = "EffCorrLT",
            scale           = None,
            )
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Loose",
            mu_sublead_type = "Loose",
            key             = "EffCorrLL",
            scale           = None,
            )
    
    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu0RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu0AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 1,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu1RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 1,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu1AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 2,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu2RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 2,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu2AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 3,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu3RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 3,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu3AllSF",
            scale         = None,
            )
    
    
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_ff.root'),
            mu_index=0,
            key='Mu0FF',
            scale=sys_ff,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_ff.root'),
            mu_index=1,
            key='Mu1FF',
            scale=sys_ff,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_ff.root'),
            mu_index=2,
            key='Mu2FF',
            scale=sys_ff,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_ff.root'),
            mu_index=3,
            key='Mu3FF',
            scale=sys_ff,
            )
    
    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.Main_hists.hist_list
    
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## VR6
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['TwoMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTT',['Mu0AllSF','Mu1AllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_LT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['TwoMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuLT',['Mu0RecoSF','Mu1AllSF','Mu0FF','EffCorrLT']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['TwoMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTL',['Mu0AllSF','Mu1RecoSF','Mu1FF','EffCorrTL']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_LL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['TwoMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuLL',['Mu0RecoSF','Mu1RecoSF','Mu0FF','Mu1FF','EffCorrLL']],
              ],
            )
    
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['ThreeMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['ThreeMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTTL',['Mu0AllSF','Mu1AllSF','Mu2RecoSF','Mu2FF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['ThreeMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTLT',['Mu0AllSF','Mu2AllSF','Mu1RecoSF','Mu1FF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_LTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['ThreeMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuLTT',['Mu1AllSF','Mu2AllSF','Mu0RecoSF','Mu0FF']],
              ],
            )



    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['FourMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Mu3AllSF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['FourMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTTTL',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Mu3RecoSF','Mu3FF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['FourMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTTLT',['Mu0AllSF','Mu1AllSF','Mu3AllSF','Mu2RecoSF','Mu2FF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_TLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['FourMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuTLTT',['Mu0AllSF','Mu2AllSF','Mu3AllSF','Mu1RecoSF','Mu1FF']],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'FAKESVR6_LTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
              ['FourMuons',None],
              ['Mlow200',None],
              ['PassAndMatch',['MuTrigSFRecoLoose']],
              ['LeadMuPt30',None],
              ['MuLTTT',['Mu1AllSF','Mu2AllSF','Mu3AllSF','Mu0RecoSF','Mu0FF']],
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



