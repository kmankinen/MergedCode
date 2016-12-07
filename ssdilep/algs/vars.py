#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
met.py - For building met.
"""

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

    #https://svnweb.cern.ch/trac/atlasoff/browser/PhysicsAnalysis/MCTruthClassifier/tags/MCTruthClassifier-00-00-26/MCTruthClassifier/MCTruthClassifierDefs.h
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


# EOF 








