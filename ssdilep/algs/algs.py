#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
algs.py

This module contains a set of analysis specific algs 
for calculating variables, applying selection and 
plotting.
"""

## std modules
import itertools
import os
import math
import ROOT

## logging
import logging
log = logging.getLogger(__name__)

## python
from itertools import combinations
from copy import copy
import sys

## pyframe
import pyframe

GeV = 1000.0

#------------------------------------------------------------------------------
class CutAlg(pyframe.core.Algorithm):
    """
    Filtering alg for applying a single cut.  The predefined cuts must be
    implemeneted as a function with the prefix "cut_". One can then specify the
    cut to be applied by passing the cut=<cut name> in the constructor, which
    will execture the cut_<cut name>() function.
    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = None,
                 cut      = None,
                 cutflow  = None,
                 isfilter = True,
                 ):
        pyframe.core.Algorithm.__init__(self, name if name else cut,isfilter=isfilter)
        self.cutflow = cutflow
         
    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)

        return self.apply_cut(self.name)

    #__________________________________________________________________________
    def apply_cut(self,cutname):
        if self.store.has_key(cutname): return self.store[cutname]
        cut_function = 'cut_%s'%cutname
        assert hasattr(self,cut_function),"cut %s doesnt exist!'"%(cutname)
        self.store[cutname] = result = getattr(self,cut_function)()
        return result
    
    #__________________________________________________________________________
    def cut_AtLeastTwoMuons(self):
      return self.chain.nmuon > 1
    #__________________________________________________________________________
    def cut_AtLeastTwoSSMuons(self):
      muons = self.store['muons']
      if self.chain.nmuon >= 2:
        for p in combinations(muons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: return True
      return False
    #__________________________________________________________________________
    def cut_AtLeastTwoSSMuonPairs(self):
      muons = self.store['muons']
      if self.chain.nmuon >= 4:
        for p in combinations(muons,4):
          if p[0].trkcharge * p[1].trkcharge * p[2].trkcharge * p[3].trkcharge > 0.0: return True
      return False
    
    #__________________________________________________________________________
    def cut_AtLeastOneMuPt28(self):
        muons = self.store['muons']
        for m in muons:
          if m.tlv.Pt()>28*GeV: return True
        return False
    #__________________________________________________________________________
    def cut_LeadMuPt30(self):
        muons = self.store['muons']
        return muons[0].tlv.Pt()>30*GeV
    
    #__________________________________________________________________________
    def cut_OneMuon(self):
        return self.chain.nmuon == 1
    #__________________________________________________________________________
    def cut_TwoMuons(self):
        return self.chain.nmuon == 2
    #__________________________________________________________________________
    def cut_ThreeMuons(self):
        return self.chain.nmuon == 3
    #__________________________________________________________________________
    def cut_FourMuons(self):
        return self.chain.nmuon == 4
    
    #__________________________________________________________________________
    def cut_TwoSSMuons(self):
      muons  = self.store['muons']
      if len(muons)==2:
        if muons[0].trkcharge * muons[1].trkcharge > 0.0:
          return True
      return False
    
    #__________________________________________________________________________
    def cut_TwoOSMuons(self):
      muons  = self.store['muons']
      if len(muons)==2:
        if muons[0].trkcharge * muons[1].trkcharge < 0.0:
          return True
      return False
    
    #__________________________________________________________________________
    def cut_OneJet(self):
        return self.chain.njets == 1
    
    #__________________________________________________________________________
    def cut_AllMuPt25(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and m.tlv.Pt()>=25.0*GeV
      return passed
    
    #__________________________________________________________________________
    def cut_AllMuEta247(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and abs(m.tlv.Eta())<2.47
      return passed
    
    #__________________________________________________________________________
    def cut_MuTT(self):
      muons = self.store['muons']
      lead_is_tight    = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = muons[0].isTrueIsoMuon()
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_tight and sublead_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuTL(self):
      muons = self.store['muons']
      lead_is_tight    = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = sublead_is_real   

      return lead_is_tight and sublead_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLT(self):
      muons = self.store['muons']
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter = lead_is_real   

      return lead_is_loose and sublead_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLL(self):
      muons = self.store['muons']
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      pass_mc_filter   = True

      if self.sampletype=="mc":
        lead_is_real     = muons[0].isTrueIsoMuon()
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = lead_is_real or sublead_is_real     

      return lead_is_loose and sublead_is_loose and pass_mc_filter
    
    
    #__________________________________________________________________________
    def cut_MuTTT(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real   

      return mu0_is_tight and mu1_is_tight and mu2_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuTTL(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_loose     = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu2_is_real   

      return mu0_is_tight and mu1_is_tight and mu2_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuTLT(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_loose     = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu1_is_real      = muons[1].isTrueIsoMuon()
        pass_mc_filter   = mu1_is_real   

      return mu0_is_tight and mu1_is_loose and mu2_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLTT(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_loose     = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real   

      return mu0_is_loose and mu1_is_tight and mu2_is_tight and pass_mc_filter
    
    
    #__________________________________________________________________________
    def cut_MuTTTT(self):
      muons = self.store['muons']
      if len(muons) < 4: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      mu3_is_tight     = bool(muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        mu3_is_real      = muons[3].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real and mu3_is_real

      return mu0_is_tight and mu1_is_tight and mu2_is_tight and mu3_is_tight and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_MuTTTL(self):
      muons = self.store['muons']
      if len(muons) < 4: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      mu3_is_loose     = bool(not muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu3_is_real      = muons[3].isTrueIsoMuon()
        pass_mc_filter   = mu3_is_real

      return mu0_is_tight and mu1_is_tight and mu2_is_tight and mu3_is_loose and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_MuTTLT(self):
      muons = self.store['muons']
      if len(muons) < 4: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_loose     = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)
      mu3_is_tight     = bool(muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu2_is_real

      return mu0_is_tight and mu1_is_tight and mu2_is_loose and mu3_is_tight and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_MuTLTT(self):
      muons = self.store['muons']
      if len(muons) < 4: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_loose     = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      mu3_is_tight     = bool(muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu1_is_real      = muons[1].isTrueIsoMuon()
        pass_mc_filter   = mu1_is_real

      return mu0_is_tight and mu1_is_loose and mu2_is_tight and mu3_is_tight and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_MuLTTT(self):
      muons = self.store['muons']
      if len(muons) < 4: return False
      
      mu0_is_loose     = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      mu3_is_tight     = bool(muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real

      return mu0_is_loose and mu1_is_tight and mu2_is_tight and mu3_is_tight and pass_mc_filter
    
    
    
    #__________________________________________________________________________
    def cut_AllMuLoose(self):
      muons = self.store['muons']
      lead_mu = muons[0]

      for m in muons:
        is_loose = bool(m.isLoose) or bool(m.isMedium) or bool(m.isTight)
        if not is_loose: return False
      return True
    
    #__________________________________________________________________________
    def cut_LeadMuIsLoose(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      is_loose = bool(lead_mu.isLoose) or bool(lead_mu.isMedium) or bool(lead_mu.isTight)
      return is_loose
    #__________________________________________________________________________
    def cut_LeadMuIsMedium(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      is_medium = bool(lead_mu.isMedium) or bool(lead_mu.isTight)
      return is_medium
    #__________________________________________________________________________
    def cut_LeadMuIsTight(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      is_tight = bool(lead_mu.isTight)
      return is_tight
    
    #__________________________________________________________________________
    def cut_LeadMuIsoFixedCutTightTrackOnly(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return lead_mu.isIsolated_FixedCutTightTrackOnly
    #__________________________________________________________________________
    def cut_LeadMuIsoNotFixedCutTightTrackOnly(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return not lead_mu.isIsolated_FixedCutTightTrackOnly
    #__________________________________________________________________________
    def cut_LeadMuIsoGradient(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return lead_mu.isIsolated_Gradient
    #__________________________________________________________________________
    def cut_LeadMuIsoNotGradient(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return not lead_mu.isIsolated_Gradient
    
    
    #__________________________________________________________________________
    def cut_MZwindow(self):
      mZ = 91.1876*GeV
      muons = self.store['muons']
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis - mZ) < 10*GeV
    
    #__________________________________________________________________________
    def cut_VetoMZwindow(self):
      mZ = 91.1876*GeV
      muons = self.store['muons']
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis - mZ) > 20 * GeV
    
    #__________________________________________________________________________
    def cut_AllPairsM20(self):
      muons = self.store['muons']
      if self.chain.nmuon >= 2:
        for p in combinations(muons,2):
          if (p[0].tlv + p[1].tlv).M()<20*GeV: return False
      return True
    
    
    #__________________________________________________________________________
    def cut_M15(self):
      muons = self.store['muons']
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis)>15*GeV
    
    #__________________________________________________________________________
    def cut_Mlow200(self):
      muons = [self.store['muon1'],self.store['muon2']]
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis)<200*GeV
    
    #__________________________________________________________________________
    def cut_PassAndMatch(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()
      
      muons = self.store['muons']
      for m in muons:
        for trig in required_triggers:
          if trig in self.store["singleMuTrigList"].keys():
            muon_is_matched    = bool( m.isTrigMatchedToChain.at(self.store["singleMuTrigList"][trig]) )
            event_is_triggered = bool( trig in passed_triggers )
            if muon_is_matched and event_is_triggered: 
              return True
      return False
    
    #__________________________________________________________________________
    def cut_PassAndMatchPresc(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()

      muons = self.store['muons']
      for m in muons:
        for trig in required_triggers:
          if trig in self.store["singleMuTrigList"].keys():
            muon_is_matched    = bool( m.isTrigMatchedToChain.at(self.store["singleMuTrigList"][trig]) )
            event_is_triggered = bool( trig in passed_triggers )
            if muon_is_matched and event_is_triggered: 
              if m.tlv.Pt()>50*GeV and trig != "HLT_mu50": continue 
              if m.tlv.Pt()>24*GeV and m.tlv.Pt()<50*GeV and trig != "HLT_mu24": continue 
              if m.tlv.Pt()>20*GeV and m.tlv.Pt()<24*GeV and trig != "HLT_mu20_L1MU15": continue
              return True
      return False
    
    
    #__________________________________________________________________________
    def cut_PassAndMatchPrescRed(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()

      dGeV = GeV / 1.03

      muons = self.store['muons']
      for m in muons:
        for trig in required_triggers:
          if trig in self.store["singleMuTrigList"].keys():
            muon_is_matched    = bool( m.isTrigMatchedToChain.at(self.store["singleMuTrigList"][trig]) )
            event_is_triggered = bool( trig in passed_triggers )
            if muon_is_matched and event_is_triggered: 
              if m.tlv.Pt()>50*dGeV and trig != "HLT_mu50": continue 
              if m.tlv.Pt()>24*dGeV and m.tlv.Pt()<50*dGeV and trig != "HLT_mu24": continue 
              if m.tlv.Pt()>20*dGeV and m.tlv.Pt()<24*dGeV and trig != "HLT_mu20_L1MU15": continue
              return True
      return False
    
    
    #__________________________________________________________________________
    def cut_PassAndMatchHLTmu50(self):
      required_triggers = ['HLT_mu50']
      passed_triggers   = self.store["passTrig"].keys()
      
      muons = self.store['muons']
      for m in muons:
        for trig in required_triggers:
          if trig in self.store["singleMuTrigList"].keys():
            muon_is_matched    = bool( m.isTrigMatchedToChain.at(self.store["singleMuTrigList"][trig]) )
            event_is_triggered = bool( trig in passed_triggers )
            if muon_is_matched and event_is_triggered: return True
      return False
    
    #__________________________________________________________________________
    def cut_PassAndMatchHLTmu24(self):
      required_triggers = ['HLT_mu24']
      passed_triggers   = self.store["passTrig"].keys()
      
      muons = self.store['muons']
      for m in muons:
        for trig in required_triggers:
          if trig in self.store["singleMuTrigList"].keys():
            muon_is_matched    = bool( m.isTrigMatchedToChain.at(self.store["singleMuTrigList"][trig]) )
            event_is_triggered = bool( trig in passed_triggers )
            if muon_is_matched and event_is_triggered: return True
      return False
    
    
    #__________________________________________________________________________
    def cut_LeadMuTruthFilter(self):
      muons = self.store['muons'] 
      if self.sampletype == "mc":
        return muons[0].isTrueIsoMuon()
      return True
    
   
    #__________________________________________________________________________
    def cut_LeadMuD0Sig2(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<2. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig3(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<3. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig4(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<4. 
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinTheta05(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)<0.5
    
    #__________________________________________________________________________
    def cut_METlow40(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 40 * GeV
    #__________________________________________________________________________
    def cut_METlow50(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 50 * GeV
    #__________________________________________________________________________
    def cut_METlow30(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 30 * GeV
    
    #__________________________________________________________________________
    def cut_MuJetDphi27(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.7
      else: return False
    #__________________________________________________________________________
    def cut_MuJetDphi28(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.8
      else: return False
    #__________________________________________________________________________
    def cut_MuJetDphi26(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.6
      else: return False
    
    #__________________________________________________________________________
    def cut_AllJetPt35(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 35 * GeV: return False
      return True
    #__________________________________________________________________________
    def cut_AllJetPt40(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 40 * GeV: return False
      return True
    
    #__________________________________________________________________________
    def cut_PASS(self):
      return True
    
#------------------------------------------------------------------------------
class PlotAlg(pyframe.algs.CutFlowAlg,CutAlg):
  
    #__________________________________________________________________________
    def __init__(self,
                 name          = 'PlotAlg',
                 region        = '',
                 hist_list     = [], # list of histograms to be filled
                 cut_flow      = None,
                 plot_all      = True,
                 do_var_check  = False,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow     = cut_flow
        self.region       = region
        self.plot_all     = plot_all
        self.hist_list    = hist_list
        self.do_var_check = do_var_check
    
    #_________________________________________________________________________
    def initialize(self):
        
        # remove eventual repetitions from list of histograms
        h_dict = {}
        for h in self.hist_list: h_dict[h.hname] = h
        self.hist_list = h_dict.values()

        pyframe.algs.CutFlowAlg.initialize(self)
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               self.plot(region, passed, list_cuts, cut, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):

        # -----------------
        # Create histograms
        # -----------------
        for h in self.hist_list:
            if h.get_name() == "Hist1D":
              h.instance = self.hist(h.hname, "ROOT.TH1F('$', ';%s;%s', %d, %lf, %lf)" % (h.xtitle,h.ytitle,h.nbins,h.xmin,h.xmax), dir=os.path.join(region, '%s'%h.dir))
            elif h.get_name() == "Hist2D": 
              h.instance = self.hist(h.hname, "ROOT.TH2F('$', ';%s;%s', %d, %lf, %lf, %d, %lf, %lf)" % (h.hname,h.hname,h.nbinsx,h.xmin,h.xmax,h.nbinsy,h.ymin,h.ymax), dir=os.path.join(region, '%s'%h.dir))
              h.set_axis_titles()

        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          for h in self.hist_list:
            
            if self.do_var_check:
              exec ( "present = %s"%h.varcheck() )
              if not present: 
                sys.exit( "ERROR: variable %s  not found for hist %s"%(h.vexpr,h.hname) )
            
            if h.get_name() == "Hist1D":
              exec( "var = %s" % h.vexpr ) # so dirty !!!
              if h.instance and var: h.fill(var, weight)
            
            elif h.get_name() == "Hist2D":
              exec( "varx,vary = %s" % h.vexpr ) # so dirty !!!
              if h.instance and varx and vary: h.fill(varx,vary, weight)
          
    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            if cn == 'ALL': continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
        return cut_passed
    
    
#__________________________________________________________________________
def log_bins(nbins,xmin,xmax):
    xmin_log = math.log(xmin)
    xmax_log = math.log(xmax)
    log_bins = [ float(i)/float(nbins)*(xmax_log-xmin_log) + xmin_log for i in xrange(nbins+1)]
    bins = [ math.exp(x) for x in log_bins ]
    return bins

#__________________________________________________________________________
def log_bins_str(nbins,xmin,xmax):
    bins = log_bins(nbins,xmin,xmax)
    bins_str = "%d, array.array('f',%s)" % (len(bins)-1, str(bins))
    return bins_str 


