#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PairWeights.py:
weights applied to 
pairs in the event
"""

#import fnmatch
#import os
#import sys
from math import sqrt
from array import array
# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# ROOT
import ROOT
import metaroot

# pyframe
import pyframe

# pyutils
import rootutils

import mcutils

GeV = 1000.0

#------------------------------------------------------------------------------
class MuPairsAllSF(pyframe.core.Algorithm):
    """
    Muon pairs reco efficiency
    Apply weight to all pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuPairsAllSF",
            lead_mu_level    = None,
            sublead_mu_level = None,
            key              = None,
            scale            = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.lead_mu_level    = lead_mu_level
        self.sublead_mu_level = sublead_mu_level
        self.key              = key
        self.scale            = scale

        assert key, "Must provide key for storing mu pairs reco sf"
    #_________________________________________________________________________
    def initialize(self):
      self.reco_levels = {"Loose":"Loose", "Medium":"Loose",         "Tight":"Loose"}
      self.iso_levels  = {"Loose":"Loose", "Medium":"FixedCutLoose", "Tight":"FixedCutTightTrackOnly"}
      self.ttva_levels = {"Loose": None,   "Medium": None,           "Tight": None}

      self.lead_mu_levels = ["Loose", "Medium", "Tight"]
      if self.lead_mu_level.startswith("Not"):
        self.lead_mu_levels.remove(self.lead_mu_level.replace("Not",""))
      else:
        assert self.lead_mu_level in self.lead_mu_levels, "ERROR: lead_mu_level %s not recognised!!!" % self.lead_mu_level
        self.lead_mu_levels = [self.lead_mu_level]
      
      self.sublead_mu_levels = ["Loose", "Medium", "Tight"]
      if self.sublead_mu_level.startswith("Not"):
        self.sublead_mu_levels.remove(self.sublead_mu_level.replace("Not",""))
      else:
        assert self.sublead_mu_level in self.sublead_mu_levels, "ERROR: sublead_mu_level %s not recognised!!!" % self.sublead_mu_level
        self.sublead_mu_levels = [self.sublead_mu_level]


    #_________________________________________________________________________
    def execute(self, weight):
        mu_pairs = self.store['mu_pairs']

        for mp in mu_pairs:
          mp.StoreWeight(self.key, 1.0)
          if "mc" in self.sampletype: 
             sf_lead = 1.0
             sf_sublead = 1.0
             
             if mp.lead.isTruthMatchedToMuon:
               sf_lead *= getattr(mp.lead,"_".join(["RecoEff","SF","Loose"])).at(0)
               sf_lead *= getattr(mp.lead,"_".join(["TTVAEff","SF"])).at(0)
               for l in self.lead_mu_levels:
                 if getattr(mp.lead,"isIsolated_"+self.iso_levels[l]):
                   sf_lead *= getattr(mp.lead,"_".join(["IsoEff","SF",self.iso_levels[l]])).at(0)
             
             if mp.sublead.isTruthMatchedToMuon:
               sf_sublead *= getattr(mp.sublead,"_".join(["RecoEff","SF","Loose"])).at(0)
               sf_sublead *= getattr(mp.sublead,"_".join(["TTVAEff","SF"])).at(0)
               for l in self.sublead_mu_levels:
                 if getattr(mp.sublead,"isIsolated_"+self.iso_levels[l]):
                   sf_sublead *= getattr(mp.sublead,"_".join(["IsoEff","SF",self.iso_levels[l]])).at(0)
             
             mp.StoreWeight(self.key, sf_lead * sf_sublead)
               
          #if self.scale: pass
        
        if self.key: 
            self.store[self.key] = 1.0
        
        return True


#------------------------------------------------------------------------------
class MuPairsFakeFactor(pyframe.core.Algorithm):
    """
    Applies the fake-factors to muon pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuPairsFakeFactor",config_file=None,mu_index=None,key=None,scale=None):
        pyframe.core.Algorithm.__init__(self,name=name)
        self.config_file = config_file
        self.mu_index = mu_index
        self.key = key
        self.scale = scale
        
        assert mu_index in [0,1,2], "ERROR: mu_index must be in [0,1,2]"
        assert config_file, "Must provide config file!"
        assert key, "Must provide key for storing fakefactor"
    #_________________________________________________________________________
    def initialize(self):
        f = ROOT.TFile.Open(self.config_file)
        assert f, "Failed to open fake-factor config file: %s"%(self.config_file)

        h_ff = f.Get("h_ff")
        assert h_ff, "Failed to get 'h_ff' from %s"%(self.config_file)

        self.h_ff = h_ff.Clone()
        self.h_ff.SetDirectory(0)
        f.Close()
    #_________________________________________________________________________
    def execute(self, weight):
        mu_pairs = self.store['mu_pairs']
        for mp in mu_pairs:
          #if not self.sampletype == "datadriven": continue
          #if self.sampletype == "mc": continue
          mp.StoreWeight(self.key,1.0)
          pt_lead = mp.lead.tlv.Pt()/GeV  
          pt_sublead = mp.sublead.tlv.Pt()/GeV  
          
          ibin_lead = None
          ibin_sublead = None

          ff_lead = 1.0
          eff_lead = 0.0
           
          ff_sublead = 1.0
          eff_sublead = 0.0
          
          ibin_lead = self.h_ff.GetXaxis().FindBin(pt_lead) 
          ibin_sublead = self.h_ff.GetXaxis().FindBin(pt_sublead) 

          assert ibin_lead, "ERROR: pt bin for lead mu not found!!!"
          assert ibin_sublead, "ERROR: pt bin for sublead mu not found!!!"
          
          # error bars are symmetric
          if self.mu_index == 0 or self.mu_index == 2:
            ff_lead = self.h_ff.GetBinContent(ibin_lead)
            eff_lead = self.h_ff.GetBinError(ibin_lead)
          if self.mu_index == 1 or self.mu_index == 2:
            ff_sublead = self.h_ff.GetBinContent(ibin_sublead)
            eff_sublead = self.h_ff.GetBinError(ibin_sublead)
          
          if self.scale == 'up': 
            ff_lead +=eff_lead
            ff_sublead += eff_sublead
          if self.scale == 'dn': 
            ff_lead -=eff_lead
            ff_sublead -= eff_sublead

          mp.StoreWeight(self.key, ff_lead * ff_sublead)
        
        if self.key: 
          self.store[self.key] = 1.0

        return True


# EOF
