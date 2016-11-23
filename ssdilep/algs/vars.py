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


#-------------------------------------------------------------------------------
class Particle(pyframe.core.ParticleProxy):
    """
    Variables added to the particle
    """
    #__________________________________________________________________________
    def __init__(self, particle, wdict={"InitWeight":1.0}, cdict={"InitCut":True} , **kwargs):
        pyframe.core.ParticleProxy.__init__(self, 
             tree_proxy = particle.tree_proxy,
             index      = particle.index,
             prefix     = particle.prefix)   
        self.particle = particle
        self.wdict    = wdict
        self.cdict    = cdict
        self.__dict__ = particle.__dict__.copy() 
    
    #__________________________________________________________________________
    def ResetCuts(self):
      self.cdict = {"InitCut":True}
      return 
    #__________________________________________________________________________
    def ResetWeights(self):
      self.wdict = {"InitWeight":1.0}
      return 
    #__________________________________________________________________________
    def HasPassedCut(self,c):
      return self.cdict[c]
    #__________________________________________________________________________
    def GetWeight(self,w):
      return self.wdict[w]
    #__________________________________________________________________________
    def HasPassedAllCuts(self):
      passed = True
      for c in self.cdict.values():
        passed = passed and c
      return passed
    #__________________________________________________________________________
    def GetTotalWeight(self):
      tot_weight = 1.0
      for w in self.wdict.values():
        tot_weight *= w
      return tot_weight 
    #__________________________________________________________________________
    def StoreWeight(self,w,v):
        self.wdict[w] = v
        return 
    #__________________________________________________________________________
    def StoreCut(self,c,v):
        self.cdict[c] = v
        return 
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








