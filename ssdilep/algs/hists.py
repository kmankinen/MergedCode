# encoding: utf-8
'''
hist.py
description: histogram class for plotting algorithm
'''

## modules


# - - - - - - - - - - - class defs  - - - - - - - - - - - - #
#------------------------------------------------------------
class Hist1D(object):
    '''
    class to hold histogram info for plotting
    '''
    #________________________________________________________
    def __init__(self,
            hname    = None,
            xtitle   = None,
            ytitle   = None,
            nbins    = None,
            xmin     = None,
            xmax     = None,
            dir      = None,
            instance = None,
            vexpr    = None,
            **kw):
       
       self.hname    = hname
       self.xtitle   = xtitle
       self.ytitle   = ytitle
       self.nbins    = nbins
       self.xmin     = xmin
       self.xmax     = xmax
       self.dir      = dir
       self.instance = instance
       self.vexpr    = vexpr
        
       ## set additional key-word args
       # -------------------------------------------------------
       for k,w in kw.iteritems():
           setattr(self, k, w)
    
    #________________________________________________________
    def fill(self,var,weight):
      if self.instance:
        self.instance.Fill(var,weight)
      return
    
    #________________________________________________________
    def varcheck(self):
      if self.vexpr:
        if "store" in self.vexpr:
          var = self.vexpr.split("'")[1]
          return  "bool('%s' in self.store.keys())" % var 
          #return  "bool(len(self.store['%s'])>=1)" % var 
        if "chain" in self.vexpr:
          pref,mid,var = self.vexpr.split(".")
          return "bool(hasattr(self.chain, '%s'))" % var 


"""
#------------------------------------------------------------
class Hist2D(object):
    '''
    class to hold histogram info for plotting
    '''
    #________________________________________________________
    def __init__(self,
            hname    = None,
            xtitle   = None,
            ytitle   = None,
            nbinsx   = None,
            nbinsy   = None,
            xmin     = None,
            xmax     = None,
            ymin     = None,
            ymax     = None,
            dir      = None,
            instance = None,
            ):
       
       self.hname    = hname,
       self.xtitle   = xtitle,
       self.ytitle   = ytitle,
       self.nbinsx   = nbinsx,
       self.nbinsy   = nbinsy,
       self.xmin     = xmin,
       self.xmax     = xmax,
       self.ymin     = ymin,
       self.ymax     = ymax,
       self.dir      = dir,
       self.instance = instance,

## EOF


"""


