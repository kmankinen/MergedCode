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
    loop += ssdilep.algs.vars.PairsBuilder(
        obj_keys=['muons'],
        pair_key='mu_pairs',
        met_key='met_clus', 
        )
    
    loop += ssdilep.algs.algs.VarsAlg(key_muons='muons',key_jets='jets')   

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
    #loop += ssdilep.algs.EvWeights.TrigPresc(cutflow='presel',key='trigger_prescale') # Does not work any longer!
    loop += ssdilep.algs.EvWeights.DataUnPresc(cutflow='presel',key='data_unprescale') 
   
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
    """
    No trigger scale factors!!!
    loop += ssdilep.algs.EvWeights.MuTrigSF(
            is_single_mu = True,
            mu_trig_level="Loose_Loose",
            mu_trig_chain="HLT_mu20_L1MU15",
            key='SingleMuonTrigSF',
            scale=None,
            )
    """ 
    
    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            #mu_level="Tight",
            mu_index=0,
            key='MuLeadAllSF',
            scale=None,
            )
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## FR1 (nominal, only with 2015 trigger)
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR1_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR1_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    
    ## FR2 (no muon weights)
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR2_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR2_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',None],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    
    ## FR3 (tighter z0sintheta in num)
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR3_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta05',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR3_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    
    ## FR4 (consider both prescaled triggers)
    ## meaningful results are only expected with getDataWeight
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR4_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR4_DEN',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoNotTight',['MuLeadAllSF']],
              ['MuJetDphi27',None],
              ['AllJetPt35',None],
              ['LeadMuD0Sig10',None],
              ['LeadMuZ0SinTheta1',None],
              ['METlow40',None],
              ],
            )
    
    ## FR5 (W+jets CR)
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR5_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              #['MuJetDphi27',None],
              #['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METhigher40',None],
              ],
            )
    
    ## FR6 (W+jets CR with higher MET)
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR6_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              #['MuJetDphi27',None],
              #['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METhigher50',None],
              ],
            )
    
    ## FR7 (W+jets CR with no mu weights)
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR7_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainLow',None],
              ['PassSingleMuPrescChainLow',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',None],
              #['MuJetDphi27',None],
              #['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METhigher40',None],
              ],
            )
    
    ## FR8 (W+jets CR will all triggers)
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region    = 'FAKESFR8_NUM',
            plot_all  = False,
            cut_flow  = [
              ['MatchSingleMuPrescChainAll',None],
              ['PassSingleMuPrescChainAll',None],
              ['LeadMuTruthFilter',None],
              ['LeadMuIsoTight',['MuLeadAllSF']],
              #['MuJetDphi27',None],
              #['AllJetPt35',None],
              ['LeadMuD0Sig3',None],
              ['LeadMuZ0SinTheta1',None],
              ['METhigher40',None],
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



