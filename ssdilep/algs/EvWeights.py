#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EvWeights.py:
weights applied
to the event
"""

from math import sqrt
from array import array
from copy import copy
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
class TrigPresc(pyframe.core.Algorithm):
    """
    Algorithm to unprescale data
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="TrigPresc", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "data" in self.sampletype: 
            #trigpresc = self.chain.triggerPrescales.at(0)
            print self.chain.triggerPrescales
            #if self.key: self.store[self.key] = trigpresc
            #self.set_weight(trigpresc*weight)
        return True

#------------------------------------------------------------------------------
class DataUnPresc(pyframe.core.Algorithm):
    """
    Algorithm to unprescale data
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="TrigPresc", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "data" in self.sampletype: 
            trigpresc = self.chain.prescale_DataWeight
            if self.key: self.store[self.key] = trigpresc
            self.set_weight(trigpresc*weight)
        return True


#------------------------------------------------------------------------------
class Pileup(pyframe.core.Algorithm):
    """
    multiply event weight by pileup weight

    if 'key' is specified the pileup weight will be put in the store
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="Pileup", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            wpileup = self.chain.weight_pileup
            if self.key: self.store[self.key] = wpileup
            self.set_weight(wpileup*weight)
        return True


#------------------------------------------------------------------------------
class MCEventWeight(pyframe.core.Algorithm):
    """
    multiply event weight by MC weight

    if 'key' is specified the MC weight will be put in the store
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="MCEventWeight", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            wmc = self.chain.mcEventWeight
            if self.key: self.store[self.key] = wmc
            self.set_weight(wmc*weight)
        return True


#------------------------------------------------------------------------------
class LPXKfactor(pyframe.core.Algorithm):
    """
    multiply event weight by Kfactor from LPX tool

    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="LPXKfactor", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            wkf = self.chain.LPXKfactor
            if self.key: self.store[self.key] = wkf
            self.set_weight(wkf*weight)
        return True


#------------------------------------------------------------------------------
class MuTrigSF(pyframe.core.Algorithm):
    """
    Muon trigger scale factor
    """
    #__________________________________________________________________________
    def __init__(self, name="MuTrigSF",
            is_single_mu   = None,
            is_di_mu       = None,
            mu_iso         = None,
            mu_reco        = None,
            mu_trig_chain  = None,
            match_to_trig  = None,
            key            = None,
            scale          = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.is_single_mu      = is_single_mu
        self.is_di_mu          = is_di_mu
        self.mu_iso            = mu_iso
        self.mu_reco           = mu_reco
        self.mu_trig_chain     = mu_trig_chain
        self.match_to_trig     = match_to_trig
        self.key               = key
        self.scale             = scale

        assert key, "Must provide key for storing mu reco sf"
    #_________________________________________________________________________
    def initialize(self):
      if not self.mu_reco: self.mu_reco = "Loose"
      if not self.mu_iso:  self.mu_iso = "FixedCutTightTrackOnly"
      if "Not" in self.mu_iso: self.mu_iso = "Loose"
      if "Not" in self.mu_reco: self.mu_reco = "Loose"

    #_________________________________________________________________________
    def execute(self, weight):
        trig_sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          
          num = 1.0 
          den = 1.0
          
          if self.is_single_mu:
            for i,m in enumerate(muons):
              if m.isTruthMatchedToMuon: 
                sf  = getattr(m,"_".join(["TrigEff","SF",self.mu_reco,self.mu_iso])).at(0)
                eff = getattr(m,"_".join(["TrigMCEff",self.mu_reco,self.mu_iso])).at(0)
                num *= 1 - sf * eff
                den *= 1 - eff
          
          else: pass  
          
          num = ( 1 - num )
          den = ( 1 - den )
          
          if den > 0:
            trig_sf = num / den

          #if self.scale: pass
       
        if self.key: 
          self.store[self.key] = trig_sf
        return True


#------------------------------------------------------------------------------
class EffCorrPair(pyframe.core.Algorithm):
    """
    Applies trigger efficiency correction for muon pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="EffCorrector",
            config_file     = None,
            mu_lead_type    = None,
            mu_sublead_type = None,
            key             = None,
            scale           = None
            ):
        pyframe.core.Algorithm.__init__(self,name=name)
        self.config_file     = config_file
        self.mu_lead_type    = mu_lead_type
        self.mu_sublead_type = mu_sublead_type
        self.key             = key
        self.scale           = scale
        
        assert config_file, "Must provide config file!"
        assert key, "Must provide key for storing fakefactor"
    #_________________________________________________________________________
    def initialize(self):
        f = ROOT.TFile.Open(self.config_file)
        assert f, "Failed to open config file for efficiency correction: %s"%(self.config_file)

        g_loose_eff = f.Get("g_loose_eff")
        g_tight_eff = f.Get("g_tight_eff")
        
        assert self.mu_lead_type in ["Loose","Tight"], "mu_lead_type not Loose or Tight"
        assert self.mu_sublead_type in ["Loose","Tight"], "mu_sublead_type not Loose or Tight"
        
        assert g_loose_eff, "Failed to get 'g_loose_eff' from %s"%(self.config_file)
        assert g_tight_eff, "Failed to get 'g_tight_eff' from %s"%(self.config_file)
        
        self.g_loose_eff = g_loose_eff.Clone()
        self.g_tight_eff = g_tight_eff.Clone()
        f.Close()
    #_________________________________________________________________________
    def execute(self, weight):
        #muons = self.store['muons']
        muons = [self.store['muon1'],self.store['muon2']]
         
        if len(self.store['muons'])>2:
          for i in xrange(3,len(self.store['muons'])+1):
            muons.append(self.store['muon%d'%i])

        mu_lead    = muons[0]
        mu_sublead = muons[1]
        
        pt_lead    = mu_lead.tlv.Pt()/GeV  
        pt_sublead = mu_sublead.tlv.Pt()/GeV  
       
        g_lead_eff    = None
        g_sublead_eff = None

        if self.mu_lead_type == "Loose":      g_lead_eff = self.g_loose_eff
        elif self.mu_lead_type == "Tight":    g_lead_eff = self.g_tight_eff
        
        if self.mu_sublead_type == "Loose":   g_sublead_eff = self.g_loose_eff
        elif self.mu_sublead_type == "Tight": g_sublead_eff = self.g_tight_eff

        eff_lead = 0.0
        eff_sublead = 0.0
        eff_lead_tight = 0.0
        eff_sublead_tight = 0.0

        for ibin_lead in xrange(1,g_lead_eff.GetN()):
          for ibin_sublead in xrange(1,g_sublead_eff.GetN()):
          
            edlow_lead = g_lead_eff.GetX()[ibin_lead] - g_lead_eff.GetEXlow()[ibin_lead]
            edhi_lead  = g_lead_eff.GetX()[ibin_lead] + g_lead_eff.GetEXhigh()[ibin_lead]
            if pt_lead>=edlow_lead and pt_lead<edhi_lead: 
              eff_lead = g_lead_eff.GetY()[ibin_lead]
              eff_lead_tight = self.g_tight_eff.GetY()[ibin_lead]
              
            edlow_sublead = g_sublead_eff.GetX()[ibin_sublead] - g_sublead_eff.GetEXlow()[ibin_sublead]
            edhi_sublead  = g_sublead_eff.GetX()[ibin_sublead] + g_sublead_eff.GetEXhigh()[ibin_sublead]
            if pt_sublead>=edlow_sublead and pt_sublead<edhi_sublead: 
              eff_sublead = g_sublead_eff.GetY()[ibin_sublead]
              eff_sublead_tight = self.g_tight_eff.GetY()[ibin_sublead]
         
         
        ineff_others = 1.0 

        for m in muons[2:]:
          muon_is_loose    = bool(not m.isIsolated_FixedCutTightTrackOnly and m.trkd0sig<10.)
          muon_is_tight    = bool(m.isIsolated_FixedCutTightTrackOnly and m.trkd0sig<3.)
          
          pt_other    = m.tlv.Pt()/GeV  
          eff_other   = 0.0
          g_other_eff = None
          
          if muon_is_loose:
            g_other_eff = self.g_loose_eff
          elif muon_is_tight:
            g_other_eff = self.g_tight_eff
          else: continue
         
          for ibin_other in xrange(1,g_other_eff.GetN()):
            
              edlow_other = g_other_eff.GetX()[ibin_other] - g_other_eff.GetEXlow()[ibin_other]
              edhi_other  = g_other_eff.GetX()[ibin_other] + g_other_eff.GetEXhigh()[ibin_other]
              if pt_other>=edlow_other and pt_other<edhi_other: 
                eff_other = g_other_eff.GetY()[ibin_other]
                
              ineff_others *= (1 - eff_other)
        
        num_pair_eff = 1 - ( 1 - eff_lead_tight ) * ( 1 - eff_sublead_tight ) * ineff_others
        den_pair_eff = 1 - ( 1 - eff_lead ) * ( 1 - eff_sublead ) * ineff_others
       
       
        corr_eff = 1.0
        if den_pair_eff != 0:
          corr_eff =  num_pair_eff / den_pair_eff

        # error bars are asymmetric
        #eff_up_mu = self.g_ff.GetEYhigh()[ibin_mu]
        #eff_dn_mu = self.g_ff.GetEYlow()[ibin_mu]
        
        if self.scale == 'up': pass
        if self.scale == 'dn': pass
       
        if self.key: 
          self.store[self.key] = corr_eff

        return True


# EOF
