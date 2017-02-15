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
        required_triggers = ["HLT_2e17lhloose"],
        key = 'electrons',
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
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OddOSElectrons') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllElePt30') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleLHLoose') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleEta247AndNotCrackRegion') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleZ0SinTheta05') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleTrkd0Sig5') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllJetPt25') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoElectrons') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHFilter') 

    loop += ssdilep.algs.EvWeights.OneOrTwoBjetsSF(
            key='OneOrTwoBjetsSF',
            )    

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
    loop +=  ssdilep.algs.EvWeights.EleTrigSF(
            trig_list =  ["HLT_2e17_lhloose"],
            key       = "EleTrigSF",
            scale     = None,
            )

    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 0,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele0RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 0,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele0AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 1,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele1RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 1,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele1AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 2,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele2RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 2,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele2AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 3,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele3RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 3,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele3AllSF",
            scale         = None,
            )
    #implementation of electron fake factors
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            ele_index=0,
            key='Ele0FF',
            sys=None,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            ele_index=1,
            key='Ele1FF',
            sys=None,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            ele_index=2,
            key='Ele2FF',
            sys=None,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            ele_index=3,
            key='Ele3FF',
            sys=None,
            )

    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.EleMain_hists.hist_list
    #hist_list += ssdilep.hists.PtOnly_hists.hist_list
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------

    ## VR1
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CRttbar_TT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['TwoElectrons',None],
                           ['EleTT',['Ele0AllSF','Ele1AllSF']],
                           ['Mass130GeV',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CRttbar_TL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['TwoElectrons',None],
                           ['EleTL',['Ele0AllSF','Ele1RecoSF','Ele1FF']],
                           ['Mass130GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CRttbar_LT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['TwoElectrons',None],
                           ['EleLT',['Ele0RecoSF','Ele1AllSF','Ele0FF']],
                           ['Mass130GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CRttbar_LL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['TwoElectrons',None],
                           ['EleLL',['Ele0RecoSF','Ele1RecoSF','Ele0FF','Ele1FF']],
                           ['Mass130GeV',None],
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



