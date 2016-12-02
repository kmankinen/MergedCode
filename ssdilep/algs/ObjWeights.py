#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ObjWeights.py: 
weights applied 
to single objects
"""

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

GeV = 1000.0

#------------------------------------------------------------------------------
class MuAllSF(pyframe.core.Algorithm):
    """
    Single muon efficiencies: reco + iso + ttva
    """
    #__________________________________________________________________________
    def __init__(self, name="MuAllSF",
            mu_index   = None,
            mu_iso     = None,
            mu_reco    = None,
            mu_ttva    = None, # not really any choice here!
            key        = None,
            scale      = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.mu_index  = mu_index
        self.mu_iso    = mu_iso
        self.mu_reco   = mu_reco
        self.mu_ttva   = mu_ttva
        self.key       = key
        self.scale     = scale

        assert key, "Must provide key for storing mu iso sf"
    
    #_________________________________________________________________________
    def initialize(self): 
      pass
    
    #_________________________________________________________________________
    def execute(self, weight):
        
        sf=1.0
        muons = self.store['muons']
        
        if self.mu_index < len(muons): 
        
          if "mc" in self.sampletype: 
            muon = muons[self.mu_index]
            
            if muon.isTruthMatchedToMuon:
              if not ("Not" in self.mu_iso):
                # HIGG3D3 
                sf *= getattr(muon,"_".join(["IsoEff","SF","Iso"+self.mu_iso])).at(0)
                # EXOT12 v1 ntuples 
                #sf *= getattr(muon,"_".join(["IsoEff","SF",self.mu_iso])).at(0)
              if not ("Not" in self.mu_reco):
                # HIGG3D3 
                sf *= getattr(muon,"_".join(["RecoEff","SF","Reco"+self.mu_reco])).at(0)
                # EXOT12 v1 ntuples 
                #sf *= getattr(muon,"_".join(["RecoEff","SF",self.mu_reco])).at(0)
              
              sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(0)
          
              if self.scale: pass

        if self.key: 
          self.store[self.key] = sf
        return True


#------------------------------------------------------------------------------
class MuFakeFactorGraph(pyframe.core.Algorithm):
    """
    Applies the fake-factors to muon pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="MuFakeFactor",config_file=None,mu_index=None,key=None,scale=None):
        pyframe.core.Algorithm.__init__(self,name=name)
        self.config_file    = config_file
        self.mu_index       = mu_index
        self.key            = key
        self.scale          = scale
        
        assert config_file, "Must provide config file!"
        assert key, "Must provide key for storing fakefactor"
    #_________________________________________________________________________
    def initialize(self):
        f = ROOT.TFile.Open(self.config_file)
        assert f, "Failed to open fake-factor config file: %s"%(self.config_file)

        g_ff = f.Get("g_ff_stat_sys")
        assert g_ff, "Failed to get 'g_ff' from %s"%(self.config_file)
        
        self.g_ff = g_ff.Clone()
        f.Close()
    #_________________________________________________________________________
    def execute(self, weight):
        
        ff_mu = 1.0 
        muons = self.store['muons']
         
        if self.mu_index < len(muons): 
        
          mu = muons[self.mu_index]
          pt_mu = mu.tlv.Pt()/GeV  
          
          for ibin_mu in xrange(1,self.g_ff.GetN()):
            edlow = self.g_ff.GetX()[ibin_mu] - self.g_ff.GetEXlow()[ibin_mu]
            edhi  = self.g_ff.GetX()[ibin_mu] + self.g_ff.GetEXhigh()[ibin_mu]
            if pt_mu>=edlow and pt_mu<edhi: break
          
          # error bars are asymmetric
          ff_mu = self.g_ff.GetY()[ibin_mu]
          eff_up_mu = self.g_ff.GetEYhigh()[ibin_mu]
          eff_dn_mu = self.g_ff.GetEYlow()[ibin_mu]
          
          if self.scale == 'up': ff_mu +=eff_up_mu
          if self.scale == 'dn': ff_mu -=eff_dn_mu
       
        if self.key: 
          self.store[self.key] = ff_mu

        return True


# EOF
