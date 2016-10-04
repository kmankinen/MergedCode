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
    config['tree']       = 'physics'
    config['do_var_log'] = True

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
    loop += ssdilep.algs.vars.PairsBuilder(
        obj_keys=['muons'],
        pair_key='mu_pairs',
        met_key='met_clus', 
        )
   

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt12') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuPt22') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoMuons') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AtLeastOneMuon') 

    ## weights configuration
    ## ---------------------------------------
    """
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            mu_trig_level="Loose_Loose",
            mu_trig_chain="HLT_2mu10",
            key='MuTrigSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="Loose",
            sublead_mu_level="Loose",
            key='MuPairsAllLooseSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="Medium",
            sublead_mu_level="Medium",
            key='MuPairsAllMediumSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="Tight",
            sublead_mu_level="Tight",
            key='MuPairsAllTightSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="Tight",
            sublead_mu_level="NotTight",
            key='MuPairsLeadTightSubLeadNotTightAllSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="NotTight",
            sublead_mu_level="Tight",
            key='MuPairsLeadNotTightSubLeadTightAllSF',
            scale=None,
            )
    loop += ssdilep.algs.PairWeights.MuPairsAllSF(
            lead_mu_level="NotTight",
            sublead_mu_level="NotTight",
            key='MuPairsLeadNotTightSubLeadNotTightAllSF',
            scale=None,
            )
    """
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## mumu signal region
    ## ---------------------------------------
    """
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'TEST',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['PASS', None],
              #['TwoMuons', None],
              #['LeadMusTrigMatched',['MuTrigSF']],
              #['LeadMusTrigMatched',None],
              #['MuPairsDeltaRJet04', None],
              ],
            )
    """ 
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'NN_NOM',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['MuPairsDeltaRJet04', None],
              ['MuPairsMVis15',None],
              ['MuPairsMZwindow',None],
              ['MuPairsAreSS',None],
              ['MuPairsLeadPt25SubLeadPt20',None],
              ['MuPairsTight',None],
              #['MuPairsTight',['MuPairsAllTightSF']],
              #['AllMuD0SigLess3', None],
              ],
            )
    
    ## mumu ND nominal
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'ND_NOM',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['MuPairsDeltaRJet04', None],
              ['MuPairsMVis15',None],
              ['MuPairsMZwindow',None],
              ['MuPairsAreSS',None],
              ['MuPairsLeadPt25SubLeadPt20',None],
              ['MuPairsLeadTightSubLeadNotTight',None],
              #['MuPairsLeadTightSubLeadNotTight',['MuPairsLeadTightSubLeadNotTightAllSF']],
              #['AllMuD0SigLess3', None],
              ],
            )
    
    ## mumu DN nominal
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'DN_NOM',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['MuPairsDeltaRJet04', None],
              ['MuPairsMVis15',None],
              ['MuPairsMZwindow',None],
              ['MuPairsAreSS',None],
              ['MuPairsLeadPt25SubLeadPt20',None],
              #['MuPairsLeadNotTightSubLeadTight',['MuPairsLeadNotTightSubLeadTightAllSF']],
              ['MuPairsLeadNotTightSubLeadTight',None],
              #['AllMuD0SigLess3', None],
              ],
            )
    
    ## mumu DD nominal
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'DD_NOM',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['MuPairsDeltaRJet04', None],
              ['MuPairsMVis15',None],
              ['MuPairsMZwindow',None],
              ['MuPairsAreSS',None],
              ['MuPairsLeadPt25SubLeadPt20',None],
              #['MuPairsLeadNotTightSubLeadNotTight',['MuPairsLeadNotTightSubLeadNotTightAllSF']],
              ['MuPairsLeadNotTightSubLeadNotTight',None],
              #['AllMuD0SigLess3', None],
              ],
            )
    
    ## mumu control region fakes NN
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'NN_FAKES',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['OneMuon',None],
              ['OneJet',None],
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['LeadMuTight',None],
              ['METlow40',None],
              ],
            )
    
    ## mumu control region fakes ND
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'ND_FAKES',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['OneMuon',None],
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['MuPairsDeltaRJet04', None],
              ['MuPairsMVis15',None],
              ['MuPairsMZwindow',None],
              ['MuPairsAreOS',None],
              ['MuPairsLeadPt25SubLeadPt20',None],
              #['MuPairsLeadTightSubLeadNotTight',['MuPairsLeadTightSubLeadNotTightAllSF']],
              ['MuPairsLeadTightSubLeadNotTight',None],
              #['AllMuD0SigHigher3', None],
              ],
            )
    
    ## mumu control region fakes DN
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'DN_FAKES',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['OneMuon',None],
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['MuPairsDeltaRJet04', None],
              ['MuPairsMVis15',None],
              ['MuPairsMZwindow',None],
              ['MuPairsAreOS',None],
              ['MuPairsLeadPt25SubLeadPt20',None],
              #['MuPairsLeadNotTightSubLeadTight',['MuPairsLeadNotTightSubLeadTightAllSF']],
              ['MuPairsLeadNotTightSubLeadTight',None],
              #['AllMuD0SigHigher3', None],
              ],
            )
    
    ## mumu control region fakes DD
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'DD_FAKES',
            obj_keys  = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all  = False,
            cut_flow  = [
              ['OneMuon',None],
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['MuPairsDeltaRJet04', None],
              ['MuPairsMVis15',None],
              ['MuPairsMZwindow',None],
              ['MuPairsAreOS',None],
              ['MuPairsLeadPt25SubLeadPt20',None],
              #['MuPairsLeadNotTightSubLeadNotTight',['MuPairsLeadNotTightSubLeadNotTightAllSF']],
              ['MuPairsLeadNotTightSubLeadNotTight',None],
              #['AllMuD0SigHigher3', None],
              ],
            )
    """ 
    ## mumu Zmumu CR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'ZCR',
            obj_keys = ['mu_pairs'], # make obj cutflow for just these objects
            plot_all = False,
            cut_flow = [
              ['TwoMuons',None],
              ['SingleMuTrigMatch',None],
              ['SingleMuTrigPass',None],
              ['MuPairsAreOS',None],
              #['MuPairsLeadPt25SubLeadPt20',None],
              ['MuPairsLeadPt40SubLeadPt35',None],
              ['MuPairsTight',None],
              ['AllMuD0SigLess3', None],
              ['AllMuZ0SinThetaLess05', None],
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



