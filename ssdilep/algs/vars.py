#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import os
from itertools import combinations
from copy import copy, deepcopy
from types import MethodType

import pyframe
import ROOT

GeV = 1000.0

import logging
log = logging.getLogger(__name__)

def fatal(message):
    sys.exit("Fatal error in %s: %s" % (__file__, message))

#------------------------------------------------------------------------------
class BuildTrigConfig(pyframe.core.Algorithm):
    """
    Algorithm to configure the trigger chain
    """
    #__________________________________________________________________________
    def __init__(self, 
          cutflow           = None,
          required_triggers = None,
          key               = None):
        pyframe.core.Algorithm.__init__(self, name="TrigConfig", isfilter=True)
        self.cutflow           = cutflow
        self.required_triggers = required_triggers
        self.key               = key
    
    #__________________________________________________________________________
    def initialize(self):
        log.info('initialize trigger config for %s...' % self.key)

    #__________________________________________________________________________
    def execute(self, weight):
        
      assert len(self.chain.passedTriggers) == len(self.chain.triggerPrescales), "ERROR: # passed triggers != # trigger prescales !!!"
      
      if not "reqTrig" in self.store.keys():
        self.store["reqTrig"] = self.required_triggers
      
      if not "passTrig" in self.store.keys():
        self.store["passTrig"] = {}
        for trig,presc in zip(self.chain.passedTriggers,self.chain.triggerPrescales):
          self.store["passTrig"][trig] = presc

      if self.key == "muons":
        self.store["singleMuTrigList"]  = {}
        
        # the muon_listTrigChains is filled 
        # in the ntuple if # muons>0. If more 
        # than one muon exists skip repetitions
        for i,trig in enumerate(self.chain.muon_listTrigChains):
          if trig in self.store["singleMuTrigList"].keys(): continue
          self.store["singleMuTrigList"][trig] = i 
        
      return True

#-------------------------------------------------------------------------------
class Particle(pyframe.core.ParticleProxy):
    """
    Variables added to the particle
    """
    #__________________________________________________________________________
    def __init__(self, particle, **kwargs):
        pyframe.core.ParticleProxy.__init__(self, 
             tree_proxy = particle.tree_proxy,
             index      = particle.index,
             prefix     = particle.prefix)   
        self.particle = particle
        self.__dict__ = particle.__dict__.copy() 
    
    #__________________________________________________________________________
    def isMatchedToTrigChain(self):
      return self.isTrigMatched

    # https://svnweb.cern.ch/trac/atlasoff/browser/PhysicsAnalysis/MCTruthClassifier/tags/MCTruthClassifier-00-00-26/MCTruthClassifier/MCTruthClassifierDefs.h
    # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MCTruthClassifier 
    #__________________________________________________________________________
    def isTrueNonIsoMuon(self):
      matchtype = self.truthType in [5,7,8]
      return self.isTruthMatchedToMuon and matchtype
    #__________________________________________________________________________
    def isTrueIsoMuon(self):
      matchtype = self.truthType in [6]
      return self.isTruthMatchedToMuon and matchtype


class ParticlesBuilder(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, name="ParticlesBuilder", key=""):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key  = key
    #__________________________________________________________________________
    def initialize(self):
        log.info('initialize single particles for %s ...' % self.key)
    #__________________________________________________________________________
    def execute(self,weight):
        self.store[self.key] = [Particle(copy(l)) for l in self.store[self.key]]


#------------------------------------------------------------------------------
class TagAndProbeVars(pyframe.core.Algorithm):
    """
    computes variables for the tag-and-probe selection
    in the di-muon channel
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'VarsAlg',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_met = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]
        met = self.store[self.key_met]
        muon1 = muons[0] 
        muon2 = muons[1] 

        # ------------------
        # at least two muons
        # ------------------
          
        # definition of tag and probe 
        lead_mu_is_tight = bool(muon1.isIsolated_FixedCutTightTrackOnly and muon1.trkd0sig<3.)
        lead_mu_is_loose = bool(not muon1.isIsolated_FixedCutTightTrackOnly and muon1.trkd0sig<10.)

        sublead_mu_is_tight = bool(muon2.isIsolated_FixedCutTightTrackOnly and muon2.trkd0sig<3.)
        sublead_mu_is_loose = bool(not muon2.isIsolated_FixedCutTightTrackOnly and muon2.trkd0sig<10.)
        
        if lead_mu_is_tight and sublead_mu_is_tight:
          if muon1.trkcharge > 0.0:
            self.store['tag'] = copy(muon1)
            self.store['probe'] = copy(muon2) 
          else:
            self.store['tag'] = copy(muon2)
            self.store['probe'] = copy(muon1) 
        elif lead_mu_is_loose or sublead_mu_is_tight:
          self.store['tag'] = copy(muon2)
          self.store['probe'] = copy(muon1) 
        elif sublead_mu_is_loose or lead_mu_is_tight:
          self.store['tag'] = copy(muon1)
          self.store['probe'] = copy(muon2) 

        return True



#------------------------------------------------------------------------------
class DiJetVars(pyframe.core.Algorithm):
          
    """
    computes variables for the di-jet selection used for
    muon fake-factor measurement
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'VarsAlg',
                 key_muons = 'muons',
                 key_jets  = 'jets',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_jets = key_jets
        self.key_met = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]
        met = self.store[self.key_met]
        jets = self.store[self.key_jets]
        
        # -------------------------
        # at least a muon and a jet
        # -------------------------
        
        if bool(len(jets)) and bool(len(muons)):
          self.store['mujet_dphi'] = muons[0].tlv.DeltaPhi(jets[0].tlv)
          scdphi = 0.0
          scdphi += ROOT.TMath.Cos(met.tlv.Phi() - muons[0].tlv.Phi())
          scdphi += ROOT.TMath.Cos(met.tlv.Phi() - jets[0].tlv.Phi())
          self.store['scdphi'] = scdphi
        
        return True



#------------------------------------------------------------------------------
class DiMuVars(pyframe.core.Algorithm):
    """
    computes variables for the di-muon selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'DiMuVars',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_met   = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]
        met = self.store[self.key_met]
        
        # ------------------
        # at least two muons
        # ------------------
        
        # dict containing pair 
        # and significance
        ss_pairs = {} 
        if len(muons)>=2:
          
          for p in combinations(muons,2):
            ss_pairs[p] = p[0].trkd0sig + p[1].trkd0sig 
          
          max_sig  = 1000.
          for pair,sig in ss_pairs.iteritems():
            if sig < max_sig: 
              if pair[0].tlv.Pt() > pair[1].tlv.Pt():
                self.store['muon1'] = pair[0]
                self.store['muon2'] = pair[1]
              else: 
                self.store['muon1'] = pair[1]
                self.store['muon2'] = pair[0]
              max_sig = sig 
        
        if ss_pairs:
          muon1 = self.store['muon1'] 
          muon2 = self.store['muon2'] 
          muon1T = ROOT.TLorentzVector()
          muon1T.SetPtEtaPhiM( muon1.tlv.Pt(), 0., muon1.tlv.Phi(), muon1.tlv.M() )
          muon2T = ROOT.TLorentzVector()
          muon2T.SetPtEtaPhiM( muon2.tlv.Pt(), 0., muon2.tlv.Phi(), muon2.tlv.M() )
        
          self.store['charge_product'] = muon2.trkcharge*muon1.trkcharge
          self.store['mVis']           = (muon2.tlv+muon1.tlv).M()
          self.store['mTtot']          = (muon1T + muon2T + met.tlv).M()  
          self.store['muons_dphi']     = muon2.tlv.DeltaPhi(muon1.tlv)
          self.store['muons_deta']     = muon2.tlv.Eta()-muon1.tlv.Eta()
         
        # puts additional muons in the store
        if ss_pairs and len(muons)>2:
           i = 2
           for m in muons:
             if m==self.store['muon1'] or m==self.store['muon2']: continue
             i = i + 1
             self.store['muon%d'%i] = m

        return True


#------------------------------------------------------------------------------
class MultiMuVars(pyframe.core.Algorithm):
    """
    computes variables for the di-muon selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'VarsAlg',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_met   = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]

        #--------------------
        # two same-sign pairs
        #--------------------
        two_pairs = {}
        if len(muons)>=4:
          for q in combinations(muons,4):
            if q[0].trkcharge * q[1].trkcharge * q[2].trkcharge * q[3].trkcharge > 0.0:
              two_pairs[q] = q[0].trkd0sig + q[1].trkd0sig + q[2].trkd0sig + q[3].trkd0sig

          max_sig  = 1000.
          for quad,sig in two_pairs.iteritems():

            if sig < max_sig:
              max_sig = sig 

              #Case 1: total charge 0
              if quad[0].trkcharge + quad[1].trkcharge + quad[2].trkcharge + quad[3].trkcharge == 0:
                for p in combinations(quad,2):
                  if (p[0].trkcharge + p[1].trkcharge) == 2:
                    if p[0].tlv.Pt() > p[1].tlv.Pt():
                      self.store['muon1'] = p[0]
                      self.store['muon2'] = p[1]
                    else:
                      self.store['muon1'] = p[1]
                      self.store['muon2'] = p[0]
                  elif (p[0].trkcharge + p[1].trkcharge) == -2:
                    if p[0].tlv.Pt() > p[1].tlv.Pt():
                      self.store['muon3'] = p[0]
                      self.store['muon4'] = p[1]
                    else:
                      self.store['muon3'] = p[1]
                      self.store['muon4'] = p[0]

              #Case 2: Total Charge = +/- 4
              elif abs(quad[0].trkcharge + quad[1].trkcharge + quad[2].trkcharge + quad[3].trkcharge) == 4:
                print("This event has charge 4!\n") #print for debugging purposes 
                self.store['muon1'] = quad[0]
                self.store['muon2'] = quad[1]
                self.store['muon3'] = quad[2]
                self.store['muon4'] = quad[3]

              #Failsafe
              else:
                print("Error: Something has gone horribly wrong with this event!\n")
                self.store['muon1'] = quad[0]
                self.store['muon2'] = quad[1]
                self.store['muon3'] = quad[2]
                self.store['muon4'] = quad[3]

        if two_pairs:
          muon1 = self.store['muon1']
          muon2 = self.store['muon2']
          muon1T = ROOT.TLorentzVector()
          muon1T.SetPtEtaPhiM( muon1.tlv.Pt(), 0., muon1.tlv.Phi(), muon1.tlv.M() )
          muon2T = ROOT.TLorentzVector()
          muon2T.SetPtEtaPhiM( muon2.tlv.Pt(), 0., muon2.tlv.Phi(), muon2.tlv.M() )

          self.store['charge_product1'] = muon2.trkcharge*muon1.trkcharge
          self.store['charge_sum1']     = muon1.trkcharge + muon2.trkcharge
          self.store['mVis1']           = (muon2.tlv+muon1.tlv).M()
          self.store['muons_dphi1']     = muon2.tlv.DeltaPhi(muon1.tlv)
          self.store['muons_deta1']     = muon2.tlv.Eta()-muon1.tlv.Eta()
          self.store['pTH1']            = (muon2.tlv+muon1.tlv).Pt()
          self.store['muons_dR1']       = math.sqrt(self.store['muons_dphi1']**2 + self.store['muons_deta1']**2)

          muon3 = self.store['muon3']
          muon4 = self.store['muon4']
          muon3T = ROOT.TLorentzVector()
          muon3T.SetPtEtaPhiM( muon3.tlv.Pt(), 0., muon3.tlv.Phi(), muon3.tlv.M() )
          muon4T = ROOT.TLorentzVector()
          muon4T.SetPtEtaPhiM( muon4.tlv.Pt(), 0., muon4.tlv.Phi(), muon4.tlv.M() )

          self.store['charge_product2'] = muon4.trkcharge*muon3.trkcharge
          self.store['charge_sum2']     = muon3.trkcharge + muon4.trkcharge
          self.store['mVis2']           = (muon4.tlv+muon3.tlv).M()
          self.store['muons_dphi2']     = muon4.tlv.DeltaPhi(muon3.tlv)
          self.store['muons_deta2']     = muon4.tlv.Eta()-muon3.tlv.Eta()
          self.store['pTH2']            = (muon4.tlv+muon3.tlv).Pt()
          self.store['muons_dR2']       = math.sqrt(self.store['muons_dphi2']**2 + self.store['muons_deta2']**2)

          self.store['charge_product'] = muon4.trkcharge * muon3.trkcharge * muon2.trkcharge * muon1.trkcharge
          self.store['charge_sum']     = muon1.trkcharge + muon2.trkcharge + muon3.trkcharge + muon4.trkcharge
          self.store['mTtot']          = (muon1T + muon2T + muon3T + muon4T + met.tlv).M()
          self.store['mVis']           = (self.store['mVis1']+self.store['mVis2'])/2
          self.store['dmVis']          = self.store['mVis1'] - self.store['mVis2']
          self.store['pairs_dphi']     = (muon3.tlv+muon4.tlv).DeltaPhi(muon1.tlv+muon2.tlv)
          self.store['pairs_deta']     = (muon3.tlv+muon4.tlv).Eta()-(muon1.tlv+muon2.tlv).Eta()
          self.store['pairs_dR']       = math.sqrt(self.store['pairs_dphi']**2 + self.store['pairs_deta']**2)

        return True


# EOF 


