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

#std
import itertools
from itertools import combinations
from copy import copy
# pyframe
import pyframe

# pyutils
import rootutils

GeV = 1000.0

#------------------------------------------------------------------------------
class TrigPresc(pyframe.core.Algorithm):
    """
    Algorithm to unprescale data
    Applies the prescale according to a specific list of triggers
    """
    #__________________________________________________________________________
    def __init__(self, 
          cutflow     = None,
          use_avg     = None,
          SKIP        = None,
          key         = None):
        pyframe.core.Algorithm.__init__(self, name="TrigPresc", isfilter=True)
        self.cutflow     = cutflow
        self.use_avg     = use_avg
        self.SKIP        = SKIP
        self.key         = key
    #__________________________________________________________________________
    def execute(self, weight):
        trigpresc = 1.0
        
        # luminosity weighted prescales
        presc_dict = {
            "HLT_mu20_L1MU15"     : 354.153, 
            "HLT_mu24"            : 47.64, 
            "HLT_mu50"            : 1.0,
            "HLT_mu26_imedium"    : 1.949,
            #"HLT_mu26_ivarmedium" : 1.097,
            "HLT_mu26_ivarmedium" : 1.000,
            }

        if "data" in self.sampletype:
          ineff_list = []
          for trig in self.store["reqTrig"]: 
            if trig in self.store["passTrig"].keys():
              if not self.use_avg:
                 if self.store["passTrig"][trig] != 0:
                   ineff_list.append(1. - 1. / self.store["passTrig"][trig])
                 else:
                   ineff_list.append(1. - 1. / presc_dict[trig])
              else:
                 ineff_list.append(1. - 1. / presc_dict[trig])

          if ineff_list:
            tot_ineff = 1.0
            for ineff in ineff_list: tot_ineff *= ineff
            trigpresc -= tot_ineff
        
        trigpresc = 1. / trigpresc
        
        if self.SKIP:  trigpresc = 1.0
        
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
class OneOrTwoBjetsSF(pyframe.core.Algorithm):
    """                                                                                                                                                                            
    OneOrTwoBjetsSF                                                                                                                                                                
    """
    #__________________________________________________________________________                                                                                                    
    def __init__(self, name="OneOrTwoBjetsSF",
            key            = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key

        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________                                                                                                     
    def initialize(self):
      pass
    #_________________________________________________________________________                                                                                                     
    def execute(self, weight):
      sf=1.0
      if "mc" in self.sampletype:
          jets = self.store['jets']
          for jet in jets:
              if jet.isFix77:
                  sf *= getattr(jet,"jvtSF").at(0)
                  sf *= getattr(jet,"SFFix77").at(0)

      if self.key:
        self.store[self.key] = sf
      return True

#------------------------------------------------------------------------------                                                                                                   
class EleTrigSF(pyframe.core.Algorithm):
    """
    Implementation of electron trigger scale factors

    """
    #__________________________________________________________________________
    def __init__(self, name="EleTrigSF",
            trig_list      = None,
            key            = None,
            scale           = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.trig_list         = trig_list
        self.key               = key
        self.scale             = scale

        assert key, "Must provide key for storing ele trig sf"
    #_________________________________________________________________________
    def initialize(self):

      self.isoLevels = [
      "",
      "_isolLoose",
      "_isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]
      if not self.trig_list: self.trig_list = "HLT_2e17lhloose"

    #_________________________________________________________________________
    def execute(self, weight):

      sf = 1.0
      electrons = self.store['electrons']

      if(len(electrons)==0 or "mc" not in self.sampletype):
          if self.key:
              self.store[self.key] = sf
          return True

      #first loop on electrons to see if the pass the tight criteria requirements
      is_TightOrLoose = []
      for ele in electrons:
          if(ele.LHMedium and ele.isIsolated_Loose):
              is_TightOrLoose.append(1)
          else: is_TightOrLoose.append(0)
                 
      SFTight = "TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_MediumLLH_isolLoose"
      SFLoose = "TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_LooseAndBLayerLLH"
      EffTight = "TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_MediumLLH_isolLoose"
      EffLoose = "TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_LooseAndBLayerLLH"


      if(len(electrons)==2):
          for ele in range(len(electrons)):
              if(is_TightOrLoose[ele] ==1): sf *= getattr(electrons[0],SFTight).at(0)
              if(is_TightOrLoose[ele] ==0): sf *= getattr(electrons[1],SFLoose).at(0)

          if self.key:
              self.store[self.key] = sf
          return True

      elif(len(electrons)==3):
          P2passD  = 0
          P2passMC = 0
          P3passD  = 1
          P3passMC = 1
          for pair in itertools.combinations(electrons,2) :
              combinationProbD  = 1 # e1*SF1 * e2*SF2 * (1-e3*SF3)
              combinationProbMC = 1 # e1     * e2     * (1-e3    )
              for eleFail in electrons:
                  if eleFail not in pair:
                      for elePass in pair:
                          if elePass.LHMedium and elePass.isIsolated_Loose:
                              combinationProbD  *= getattr(elePass,SFTight).at(0)*getattr(elePass,EffTight).at(0)
                              combinationProbMC *= getattr(elePass,EffTight).at(0)
                          else:
                              combinationProbD  *= getattr(elePass,SFLoose).at(0)*getattr(elePass,EffLoose).at(0)
                              combinationProbMC *= getattr(elePass,EffLoose).at(0)
                      if eleFail.LHMedium and eleFail.isIsolated_Loose:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFTight).at(0)**getattr(elePass,EffTight).at(0))
                          combinationProbMC *= 1 -   getattr(eleFail,EffTight).at(0)                  
                      else:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFLoose).at(0)*getattr(elePass,EffLoose).at(0))
                          combinationProbMC *= 1 -   getattr(eleFail,EffLoose).at(0)
                      break
              P2passD  += combinationProbD   # a*b*(1-c) + a*c*(1-b) + b*c*(1-d) 
              P2passMC += combinationProbMC  # a*b*(1-c) + a*c*(1-b) + b*c*(1-d)
          for ele in electrons:
              if ele.LHMedium and ele.isIsolated_Loose:
                  P3passD  *= getattr(ele,SFTight).at(0)*getattr(elePass,EffTight).at(0)
                  P3passMC *= getattr(ele,EffTight).at(0)
              else:
                  P3passD  *= getattr(ele,SFLoose).at(0)*getattr(elePass,EffLoose).at(0)
                  P3passMC *= getattr(ele,EffLoose).at(0)
           
          if(P2passD==0 and P2passMC==0 and P3passD==0 and P3passMC ==0):
              print "No SF available for these leptons"
              sf == 0
              
          else : sf = (P2passD+P3passD)/(P2passMC+P3passMC)
          if self.key: 
              self.store[self.key] = sf
          return True

      elif(len(electrons)==4):
          P2passD  = 0
          P2passMC = 0
          P3passD  = 1
          P3passMC = 1
          P4passD  = 1
          P4passMC = 1
          for pair in itertools.combinations(electrons,2) :
              combinationProbD  = 1 # e1*SF1 * e2*SF2 * (1-e3*SF3) * (1-e4*SF4)
              combinationProbMC = 1 # e1     * e2     * (1-e3    ) * (1-e4    )
              for eleFail in electrons:
                  if eleFail not in pair:
                      for elePass in pair:
                          if elePass.LHMedium and elePass.isIsolated_Loose:
                              combinationProbD  *= getattr(elePass,SFTight).at(0)*getattr(elePass,EffTight).at(0)
                              combinationProbMC *= getattr(elePass,EffTight).at(0)
                          else:
                              combinationProbD  *= getattr(elePass,SFLoose).at(0)*getattr(elePass,EffLoose).at(0)
                              combinationProbMC *= getattr(elePass,EffLoose).at(0)
                      if eleFail.LHMedium and eleFail.isIsolated_Loose:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFTight).at(0)**getattr(elePass,EffTight).at(0))
                          combinationProbMC *= 1 -   getattr(eleFail,EffTight).at(0)                  
                      else:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFLoose).at(0)*getattr(elePass,EffLoose).at(0))
                          combinationProbMC *= 1 -   getattr(eleFail,EffLoose).at(0)
                      break
              P2passD  += combinationProbD   # a*b*(1-c)*(1-d) + a*c*(1-b)*(1-d) + b*c*(1-d)*(1-a) etc. 
              P2passMC += combinationProbMC  # a*b*(1-c)*(1-d) + a*c*(1-b)*(1-d) + b*c*(1-d)*(1-a) + etc
          for pair in itertools.combinations(electrons,3) :
              combinationProbD  = 1 # e1*SF1 * e2*SF2 * e3*SF3 * (1-e4*SF4)
              combinationProbMC = 1 # e1     * e2     * e3     * (1-e4)
              for eleFail in electrons:
                  if eleFail not in pair:
                      for elePass in pair:
                          if elePass.LHMedium and elePass.isIsolated_Loose:
                              combinationProbD  *= getattr(elePass,SFTight).at(0)*getattr(elePass,EffTight).at(0)
                              combinationProbMC *= getattr(elePass,EffTight).at(0)
                          else:
                              combinationProbD  *= getattr(elePass,SFLoose).at(0)*getattr(elePass,EffLoose).at(0)
                              combinationProbMC *= getattr(elePass,EffLoose).at(0)
                      if eleFail.LHMedium and eleFail.isIsolated_Loose:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFTight).at(0)**getattr(elePass,EffTight).at(0))
                          combinationProbMC *= 1 -   getattr(eleFail,EffTight).at(0)                  
                      else:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFLoose).at(0)*getattr(elePass,EffLoose).at(0))
                          combinationProbMC *= 1 -   getattr(eleFail,EffLoose).at(0)
                      break
              P3passD  += combinationProbD   # a*b*(1-c) + a*c*(1-b) + b*c*(1-d) 
              P3passMC += combinationProbMC  # a*b*(1-c) + a*c*(1-b) + b*c*(1-d)
          for ele in electrons:
              if ele.LHMedium and ele.isIsolated_Loose:
                  P4passD  *= getattr(ele,SFTight).at(0)*getattr(elePass,EffTight).at(0)
                  P4passMC *= getattr(ele,EffTight).at(0)
              else:
                  P4passD  *= getattr(ele,SFLoose).at(0)*getattr(elePass,EffLoose).at(0)
                  P4passMC *= getattr(ele,EffLoose).at(0)
           
          if(P2passD==0 and P2passMC==0 and P3passD==0 and P3passMC ==0 and P4passMC==0 and P4passD==0):
              print "No sf available for this event"
              sf == 0
              
          else : sf = (P2passD+P3passD+P4passD)/(P2passMC+P3passMC+P4passMC)
          if self.key: 
              self.store[self.key] = sf
          return True



#------------------------------------------------------------------------------
class MuTrigSF(pyframe.core.Algorithm):
    """
    Muon trigger scale factor (OR of signle muon triggers)
    """
    #__________________________________________________________________________
    def __init__(self, name="MuTrigSF",
            trig_list   = None,
            match_all   = False,
            mu_iso      = None,
            mu_reco     = None,
            key         = None,
            scale       = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.trig_list   = trig_list # if for some reason a different list is needed
        self.match_all   = match_all
        self.mu_iso      = mu_iso
        self.mu_reco     = mu_reco
        self.key         = key
        self.scale       = scale

        assert key, "Must provide key for storing mu reco sf"
    #_________________________________________________________________________
    def initialize(self):
      
      if not self.mu_reco:      self.mu_reco = "Loose"
      if not self.mu_iso:       self.mu_iso  = "FixedCutTightTrackOnly"
      
      if "Not" in self.mu_iso:  self.mu_iso  = "Loose"
      if "Not" in self.mu_reco: self.mu_reco = "Loose"

      if not self.trig_list: self.trig_list = self.store["reqTrig"]

    #_________________________________________________________________________
    def execute(self, weight):
        trig_sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          
          eff_data_chain = 1.0 
          eff_mc_chain   = 1.0
          
          for i,m in enumerate(muons):
          
            eff_data_muon = 1.0 
            eff_mc_muon   = 1.0

            if m.isTruthMatchedToMuon: 
              for trig in self.trig_list:
                
                sf_muon  = getattr(m,"_".join(["TrigEff","SF",trig,"Reco"+self.mu_reco,"Iso"+self.mu_iso])).at(0)
                eff_muon = getattr(m,"_".join(["TrigMCEff",trig,"Reco"+self.mu_reco,"Iso"+self.mu_iso])).at(0)
                
                # EXOT12 for v1 ntuples
                #sf_muon  = getattr(m,"_".join(["TrigEff","SF",self.mu_reco,self.mu_iso])).at(0)
                #eff_muon = getattr(m,"_".join(["TrigMCEff",self.mu_reco,self.mu_iso])).at(0)
                
                eff_data_muon *= 1 - sf_muon * eff_muon
                eff_mc_muon   *= 1 - eff_muon
              
              eff_data_muon = ( 1 - eff_data_muon )
              eff_mc_muon   = ( 1 - eff_mc_muon )
              
              if self.match_all:
                eff_data_chain *= eff_data_muon
                eff_mc_chain   *= eff_mc_muon
              else:
                eff_data_chain *= 1. - eff_data_muon
                eff_mc_chain   *= 1. - eff_mc_muon
          
          if not self.match_all: 
            eff_data_chain = ( 1 - eff_data_chain )
            eff_mc_chain   = ( 1 - eff_mc_chain )
          
          if eff_mc_chain > 0:
            trig_sf = eff_data_chain / eff_mc_chain
          
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

        # check particular quality 
        # of muons in the SS pair
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
