#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
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

      dGeV = GeV / 1.03

      if self.key == "muons":
        self.store["singleMuTrigList"]  = {}  
        self.store["singleMuTrigSlice"] = {}  # this is for prescale slicing
        self.store["singleMuTrigThr"]   = {}  # this is for prescale slicing
        low_thr  = []
        high_thr = []

        
        # the muon_listTrigChains is filled 
        # in the ntuple if # muons>0. If more 
        # than one muon exists skip repetitions

        for i,trig in enumerate(self.chain.muon_listTrigChains):
          if trig in self.store["singleMuTrigList"].keys(): continue
          self.store["singleMuTrigList"][trig] = i
              
        for trig in self.store["reqTrig"]:
          for thr in trig.split("_"):
            if thr.startswith("mu"): 
              self.store["singleMuTrigThr"][trig] = float( thr.replace("mu","") ) * GeV
              low_thr.append(float( thr.replace("mu","") ) * dGeV)
              high_thr.append(float( thr.replace("mu","") ) * dGeV)
        
        if low_thr and high_thr: 
          low_thr  = sorted(low_thr) 
          high_thr = sorted(high_thr)
          high_thr.remove(low_thr[0])
          high_thr.append(1000000000.)

        for low,high in zip(low_thr,high_thr):
          for trig,thr in self.store["singleMuTrigThr"].iteritems():
            if thr>=low and thr<high: self.store["singleMuTrigSlice"][trig] = (low,high)
      
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
                 name      = 'TagAndProbeVars',
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
        
        if len(muons)<2: 
          return True
        
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
          if random.randint(0,9) > 4:
            self.store['tag'] = muon1
            self.store['probe'] = muon2 
          else:
            self.store['tag'] = muon2
            self.store['probe'] = muon1 
        elif lead_mu_is_loose or sublead_mu_is_tight:
          self.store['tag'] = muon2
          self.store['probe'] = muon1
        elif sublead_mu_is_loose or lead_mu_is_tight:
          self.store['tag'] = muon1
          self.store['probe'] = muon2


        return True


#------------------------------------------------------------------------------
class ProbeVars(pyframe.core.Algorithm):
    """
    computes variables for the tag-and-probe selection
    in the di-muon channel
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'ProbeVars',
                 key_tag   = 'tag',
                 key_probe = 'probe',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        
        self.key_tag   = key_tag
        self.key_probe = key_probe
    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_tag), "tag key: %s not found in store!" % (self.key_tag)
        assert self.store.has_key(self.key_probe), "probe key: %s not found in store!" % (self.key_probe)
        tag   = self.store[self.key_tag]
        probe = self.store[self.key_probe]
       
        """
        iso/pt<0.8
        ----------
        from linear fit with RMS errors:
        p0  = -15.1535   +/-   6.76762     
        p1  =  1.37198   +/-   0.0605992 
        
        from linear fit with Gaussian errors:
        p0  = -10.0398   +/-   8.47404     
        p1  =  1.31456   +/-   0.0727542
        """
        
        p0  = -15.1535
        p1  =  1.37198

        # RMS is in GeV
        RMS = {}

        RMS["ptiso_20_24"]   = 0.0
        RMS["ptiso_25_29"]   = 12.2314540491
        RMS["ptiso_30_34"]   = 13.1127516361
        RMS["ptiso_35_39"]   = 14.1917679216
        RMS["ptiso_40_44"]   = 15.817468499
        RMS["ptiso_45_49"]   = 17.8695115984
        RMS["ptiso_50_54"]   = 19.514311385
        RMS["ptiso_55_59"]   = 20.766518158
        RMS["ptiso_60_64"]   = 22.3766186773
        RMS["ptiso_65_69"]   = 24.3229342864
        RMS["ptiso_70_74"]   = 28.015614951
        RMS["ptiso_75_79"]   = 28.4611393362
        RMS["ptiso_80_84"]   = 29.0236009038
        RMS["ptiso_85_89"]   = 30.6822437481
        RMS["ptiso_90_94"]   = 31.8781585634
        RMS["ptiso_95_99"]   = 32.6372947862
        RMS["ptiso_100_104"] = 33.6500618996
        RMS["ptiso_105_109"] = 34.7148773178
        RMS["ptiso_110_114"] = 35.8474480687
        RMS["ptiso_115_119"] = 36.5361582603
        RMS["ptiso_120_124"] = 37.8015831265
        RMS["ptiso_125_129"] = 37.9881270296
        RMS["ptiso_130_134"] = 39.2558316829
        RMS["ptiso_135_139"] = 40.7675806346
        RMS["ptiso_140_144"] = 40.4074404055
        RMS["ptiso_145_149"] = 43.3341308017
        RMS["ptiso_150_154"] = 43.7714581889
        RMS["ptiso_155_159"] = 44.5093543214
        RMS["ptiso_160_164"] = 46.6781205525
        RMS["ptiso_165_169"] = 47.7095699232
        RMS["ptiso_170_174"] = 45.7109500836
        RMS["ptiso_175_179"] = 49.0192695547
        RMS["ptiso_180_184"] = 50.9815966197
        RMS["ptiso_185_189"] = 47.3741332188
        RMS["ptiso_190_194"] = 50.2230812026
        RMS["ptiso_195_199"] = 55.7351980424
        RMS["ptiso_200_204"] = 55.8915357924
        RMS["ptiso_205_209"] = 49.6060680421
        RMS["ptiso_210_214"] = 56.2265318556
        RMS["ptiso_215_219"] = 56.3887385468
        RMS["ptiso_220_224"] = 59.6691710375
        RMS["ptiso_225_229"] = 52.474950576
        RMS["ptiso_230_234"] = 62.044322334
        RMS["ptiso_235_239"] = 58.086148415
        RMS["ptiso_240_244"] = 59.0719022682
        RMS["ptiso_245_249"] = 58.1418574345
        RMS["ptiso_250_254"] = 46.3266117434
        RMS["ptiso_255_259"] = 52.5704088976
        RMS["ptiso_260_264"] = 62.5374917136
        RMS["ptiso_265_269"] = 64.8968495402
        RMS["ptiso_270_274"] = 68.2074938861
        RMS["ptiso_275_279"] = 70.3073936368
        RMS["ptiso_280_284"] = 64.1250913742
        RMS["ptiso_285_289"] = 95.5317413219
        RMS["ptiso_290_294"] = 68.043090922
        RMS["ptiso_295_299"] = 48.4110180296
        RMS["ptiso_300_304"] = 75.2142772351
        RMS["ptiso_305_309"] = 76.7616181484
        RMS["ptiso_310_314"] = 46.147625137
        RMS["ptiso_315_319"] = 81.5080364136
        
        probe_ptiso = ( probe.tlv.Pt() + probe.ptvarcone30 ) / GeV

        probe_RMS = 81. # last bin!
        
        for k,v in RMS.iteritems():
          if probe_ptiso >= float(k.split("_")[1]) and probe_ptiso < float(k.split("_")[2]) + 1.:
            probe_RMS = v
       
        self.store["probe_ujet_pt"] =  p1 * probe_ptiso + p0 + random.gauss(0.,probe_RMS)

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
                 name      = 'MultiMuVars',
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


