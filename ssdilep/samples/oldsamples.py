# encoding: utf-8
'''
samples.py

description:

'''

#------------------------------------------------------------------------------
# All MC xsections can be found here:
# https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/CentralMC15ProductionList
#------------------------------------------------------------------------------

## modules
from sample import Sample
import ROOT


## colors
black = ROOT.kBlack
white = ROOT.kWhite
red   = ROOT.kRed
green = ROOT.kGreen+1



#-------------------------------------------------------------------------------
# data
#-------------------------------------------------------------------------------
GRL = []

GRL += [
        # 2015 
        "276262","276329","276336","276416","276511","276689",
        "276778","276790","276952","276954","278880","278912",
        "278968","279169","279259","279279","279284","279345",
        "279515","279598","279685","279764","279813","279867",
        "279928","279932","279984","280231","280319","280368",
        "280423","280464","280500","280520","280614","280673",
        "280753","280853","280862","280950","280977","281070",
        "281074","281075","281317","281385","281411","282625",
        "282631","282712","282784","282992","283074","283155",
        "283270","283429","283608","283780","284006","284154",
        "284213","284285","284420","284427","284484",
        #2016 
        "297730","298595","298609","298633","298687","298690",
        "298771","298773","298862","298967","299055","299144",
        "299147","299184","299243","299584","300279","300345",
        "300415","300418","300487","300540","300571","300600",
        "300655","300687","300784","300800","300863","300908",
        "301912","301918","301932","301973","302053","302137",
        "302265","302269","302300","302347","302380","302391",
        "302393","302737", 
        ]

ds_name = 'physics_Main_00%s'

for run in GRL:
    name = ds_name % run
    globals()[name] = Sample(
            name = name,
            type = "data"
            )

list_runs =[globals()[ds_name%(run)] for run in GRL]

data = Sample(name         = "data",
              tlatex       = "Data 2015",
              fill_color   = white,
              fill_style   = 0,
              line_color   = black,
              line_style   = 1,
              marker_color = black,
              marker_style = 20,
              daughters    = list_runs,
              )


#-------------------------------------------------------------------------------
# data-driven background
#-------------------------------------------------------------------------------
"""
fakes_TL = Sample( name         = 'fakes_TL',
                   tlatex       = 'Fakes TL',
                   fill_color   = ROOT.kGreen,
                   line_color   = ROOT.kGreen,
                   marker_color = ROOT.kGreen,
                   daughters    = list_runs,
                   type         = "datadriven",
                   )

fakes_LT = Sample( name         = 'fakes_LT',
                   tlatex       = 'Fakes LT',
                   fill_color   = ROOT.kBlue,
                   line_color   = ROOT.kBlue,
                   marker_color = ROOT.kBlue,
                   daughters    = list_runs,
                   type         = "datadriven",
                   )

fakes_TT = Sample( name         = 'fakes_TT',
                   tlatex       = 'Fakes TT',
                   fill_color   = ROOT.kRed,
                   line_color   = ROOT.kRed,
                   marker_color = ROOT.kRed,
                   daughters    = list_runs,
                   type         = "datadriven",
                   )

"""
fakes_cr    = Sample( name      = "fakes_cr",
                   tlatex       = "Fakes CR",
                   fill_color   = ROOT.kGray,
                   line_color   = ROOT.kGray+1,
                   line_style   = 1,
                   marker_color = ROOT.kGray+1,
                   marker_style = 20,
                   type         = "datadriven",
                   )


fakes    = Sample( name         = "fakes",
                   tlatex       = "Fakes",
                   fill_color   = ROOT.kGray,
                   line_color   = ROOT.kGray+1,
                   line_style   = 1,
                   marker_color = ROOT.kGray+1,
                   marker_style = 20,
                   #daughters    = [fakes_TL,fakes_LT,fakes_TT],
                   daughters    = list_runs,
                   type         = "datadriven",
                   )


#-----------------------------------------------------------------------------
# VV (Sherpa)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryDibosonSherpa
#-----------------------------------------------------------------------------
llll            = Sample( name = "llll",           xsec = 12.849     )
lllvSFMinus     = Sample( name = "lllvSFMinus",    xsec = 1.8442     )
lllvOFMinus     = Sample( name = "lllvOFMinus",    xsec = 3.6254     )
lllvSFPlus      = Sample( name = "lllvSFPlus",     xsec = 2.5618     )
lllvOFPlus      = Sample( name = "lllvOFPlus",     xsec = 5.0248     )
llvv            = Sample( name = "llvv",           xsec = 14.0       )
llvvjj_ss_EW4   = Sample( name = "llvvjj_ss_EW4",  xsec = 0.025797   )
llvvjj_ss_EW6   = Sample( name = "llvvjj_ss_EW6",  xsec = 0.043004   )
lllvjj_EW6      = Sample( name = "lllvjj_EW6",     xsec = 0.042017   )
lllljj_EW6      = Sample( name = "lllljj_EW6",     xsec = 0.031496   )
WplvWmqq        = Sample( name = "WplvWmqq",       xsec = 25.995     )
WpqqWmlv        = Sample( name = "WpqqWmlv",       xsec = 26.4129606 )
WlvZqq          = Sample( name = "WlvZqq",         xsec = 12.543     )
WqqZll          = Sample( name = "WqqZll",         xsec = 3.7583     )
WqqZvv          = Sample( name = "WqqZvv",         xsec = 7.4151     )
ZqqZll          = Sample( name = "ZqqZll",         xsec = 2.3645727  )
ZqqZvv          = Sample( name = "ZqqZvv",         xsec = 4.63359232 )

diboson_sherpa = Sample( name =   'diboson_sherpa',
                  tlatex = 'Di-boson (Sherpa)',
                  fill_color = ROOT.kYellow-7,
                  line_color =  ROOT.kYellow-6,
                  marker_color =  ROOT.kYellow-6,
                  daughters = [
                                llll,         
                                lllvSFMinus,  
                                lllvOFMinus,  
                                lllvSFPlus,   
                                lllvOFPlus,   
                                #llvv,          # histograms fail
                                llvvjj_ss_EW4,
                                llvvjj_ss_EW6,
                                lllvjj_EW6,   
                                lllljj_EW6,   
                                #WplvWmqq,     
                                #WpqqWmlv,     
                                #WlvZqq,       
                                #WqqZll,       
                                #WqqZvv,       
                                #ZqqZll,       
                                #ZqqZvv,
                              ],
                ) 

#-----------------------------------------------------------------------------
# VV (PowHeg)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryDibosonPowheg
#-----------------------------------------------------------------------------
WWlvlv                     = Sample( name =  "WWlvlv",                    xsec = 10.631      )
WZlvll_mll4                = Sample( name =  "WZlvll_mll4",               xsec = 4.5023      )
WZlvvv_mll4                = Sample( name =  "WZlvvv_mll4",               xsec = 2.7778      )
ZZllll_mll4                = Sample( name =  "ZZllll_mll4",               xsec = 1.2673      )
ZZvvll_mll4                = Sample( name =  "ZZvvll_mll4",               xsec = 0.91795     )
ZZvvvv_mll4                = Sample( name =  "ZZvvvv_mll4",               xsec = 0.54901     )
WWlvqq                     = Sample( name =  "WWlvqq",                    xsec = 44.18       )
WZqqll_mll20               = Sample( name =  "WZqqll_mll20",              xsec = 3.2777      )
WZqqvv                     = Sample( name =  "WZqqvv",                    xsec = 5.7576      )
WZlvqq_mqq20               = Sample( name =  "WZlvqq_mqq20",              xsec = 10.086      )
ZZvvqq_mqq20               = Sample( name =  "ZZvvqq_mqq20",              xsec = 3.9422      )
ZZqqll_mqq20mll20          = Sample( name =  "ZZqqll_mqq20mll20",         xsec = 2.2699      )
ZZllll_mll4_m4l_500_13000  = Sample( name =  "ZZllll_mll4_m4l_500_13000", xsec = 0.004658938, feff =  0.0037 )

diboson_powheg = Sample( name =   'diboson_powheg',
                  tlatex = 'Di-boson (Powheg)',
                  fill_color = ROOT.kYellow-7,
                  line_color =  ROOT.kYellow-6,
                  marker_color =  ROOT.kYellow-6,
                  daughters = [
                                WWlvlv,                   
                                WZlvll_mll4,              
                                WZlvvv_mll4,              
                                ZZllll_mll4,              
                                ZZvvll_mll4,              
                                ZZvvvv_mll4,              
                                WWlvqq,                   
                                WZqqll_mll20,             
                                WZqqvv,                   
                                WZlvqq_mqq20,             
                                ZZvvqq_mqq20,             
                                #ZZqqll_mqq20mll20,        
                                #ZZllll_mll4_m4l_500_13000,
                              ],
                ) 


#-----------------------------------------------------------------------------
# W + jets (Sherpa)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryWjetsSherpaLight (light filter)
#                         https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryWjetsSherpaC     (C filter) 
#                         https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryWjetsSherpaB     (B filter) 
# for my tags!!!
# https://twiki.cern.ch/twiki/pub/AtlasProtected/CentralMC15ProductionList/XSections_13TeV_e3651_e4133.txt
#-----------------------------------------------------------------------------

#-----
# Wenu
#-----

Wenu_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt0_70_CVetoBVeto",         xsec = 17217.7589809,  feff =  0.8907,  kfactor = 0.9082) 
Wenu_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt70_140_CVetoBVeto",       xsec = 419.458902664,  feff =  0.7288,  kfactor = 0.9082)
Wenu_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt140_280_CVetoBVeto",      xsec = 55.812213827,   feff =  0.6816,  kfactor = 0.9082)
Wenu_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt280_500_CVetoBVeto",      xsec = 3.415293894 * 1.1,    feff =  0.6527,  kfactor = 0.9082)
Wenu_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt500_700_CVetoBVeto",      xsec = 0.204156559 * 1.1,    feff =  0.6317,  kfactor = 0.9082)
Wenu_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt700_1000_CVetoBVeto",     xsec = 0.033518757 * 1.1,    feff =  0.6096,  kfactor = 0.9082)
Wenu_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt1000_2000_CVetoBVeto",    xsec = 0.004526723 * 1.1,    feff =  0.6292,  kfactor = 0.9082)
Wenu_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt2000_E_CMS_CVetoBVeto",   xsec = 1.788e-05 * 1.1,      feff =  0.6384,  kfactor = 0.9082)
                                                                                                                   
Wenu_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt0_70_CFilterBVeto",       xsec = 957.166425598,  feff =  0.0493,  kfactor = 0.9082)
Wenu_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt70_140_CFilterBVeto",     xsec = 101.537442087,  feff =  0.1768,  kfactor = 0.9082)
Wenu_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt140_280_CFilterBVeto",    xsec = 16.838461137,   feff =  0.2059,  kfactor = 0.9082)
Wenu_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt280_500_CFilterBVeto",    xsec = 1.159086019 * 1.1,    feff =  0.2215,  kfactor = 0.9082)
Wenu_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt500_700_CFilterBVeto",    xsec = 0.076063692 * 1.1,    feff =  0.2436,  kfactor = 0.9082)
Wenu_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt700_1000_CFilterBVeto",   xsec = 0.011205872 * 1.1,    feff =  0.2028,  kfactor = 0.9082)
Wenu_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt1000_2000_CFilterBVeto",  xsec = 0.001755119 * 1.1,    feff =  0.238,   kfactor = 0.9082)
Wenu_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt2000_E_CMS_CFilterBVeto", xsec = 7.71e-06 * 1.1,       feff =  0.2728,  kfactor = 0.9082)
                                                                                                                   
Wenu_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt0_70_BFilter",            xsec = 1161.20628355,  feff =  0.0598,  kfactor = 0.9082)
Wenu_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt70_140_BFilter",          xsec = 55.459634594,   feff =  0.0967,  kfactor = 0.9082)
Wenu_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt140_280_BFilter",         xsec = 9.19142934,     feff =  0.1123,  kfactor = 0.9082)
Wenu_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt280_500_BFilter",         xsec = 0.679805485 * 1.1,    feff =  0.131,   kfactor = 0.9082)
Wenu_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt500_700_BFilter",         xsec = 0.048845728 * 1.1,    feff =  0.1552,  kfactor = 0.9082)
Wenu_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt700_1000_BFilter",        xsec = 0.00959807 * 1.1,     feff =  0.1687,  kfactor = 0.9082)
Wenu_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt1000_2000_BFilter",       xsec = 0.001258268 * 1.1,    feff =  0.1731,  kfactor = 0.9082)
Wenu_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt2000_E_CMS_BFilter",      xsec = 4.68e-06 * 1.1,       feff =  0.1652,  kfactor = 0.9082)

Wenu = Sample( name =   'Wenu',
                  tlatex = 'W #rightarrow e#nu+jets',
                  fill_color = ROOT.kRed+1,
                  line_color =  ROOT.kRed+2,
                  marker_color =  ROOT.kRed+2,
                  daughters = [
                               Wenu_Pt0_70_CVetoBVeto,        
                               Wenu_Pt70_140_CVetoBVeto,                                    
                               Wenu_Pt140_280_CVetoBVeto,     
                               Wenu_Pt280_500_CVetoBVeto,     
                               Wenu_Pt500_700_CVetoBVeto,     
                               Wenu_Pt700_1000_CVetoBVeto,    
                               Wenu_Pt1000_2000_CVetoBVeto,   
                               Wenu_Pt2000_E_CMS_CVetoBVeto,  
                               Wenu_Pt0_70_CFilterBVeto,      
                               Wenu_Pt70_140_CFilterBVeto,    
                               Wenu_Pt140_280_CFilterBVeto,   
                               Wenu_Pt280_500_CFilterBVeto,   
                               Wenu_Pt500_700_CFilterBVeto,   
                               Wenu_Pt700_1000_CFilterBVeto,  
                               Wenu_Pt1000_2000_CFilterBVeto, 
                               Wenu_Pt2000_E_CMS_CFilterBVeto,
                               Wenu_Pt0_70_BFilter,           
                               Wenu_Pt70_140_BFilter,         
                               Wenu_Pt140_280_BFilter,        
                               Wenu_Pt280_500_BFilter,        
                               Wenu_Pt500_700_BFilter,        
                               Wenu_Pt700_1000_BFilter,       
                               Wenu_Pt1000_2000_BFilter,      
                               Wenu_Pt2000_E_CMS_BFilter,     
                              ],
                ) 


#------
# Wmunu
#------

Wmunu_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt0_70_CVetoBVeto",         xsec = 17340.6393371, feff = 0.8925, kfactor = 0.9082)
Wmunu_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt70_140_CVetoBVeto",       xsec = 419.506840815, feff = 0.7284, kfactor = 0.9082) 
Wmunu_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt140_280_CVetoBVeto",      xsec = 55.841494484,  feff = 0.6842, kfactor = 0.9082)
Wmunu_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt280_500_CVetoBVeto",      xsec = 3.432031461 * 1.1,   feff = 0.6536, kfactor = 0.9082)
Wmunu_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt500_700_CVetoBVeto",      xsec = 0.202350513 * 1.1,   feff = 0.6311, kfactor = 0.9082)
Wmunu_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt700_1000_CVetoBVeto",     xsec = 0.035335673 * 1.1,   feff = 0.6326, kfactor = 0.9082)
Wmunu_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt1000_2000_CVetoBVeto",    xsec = 0.004290787 * 1.1,   feff = 0.5979, kfactor = 0.9082)
Wmunu_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt2000_E_CMS_CVetoBVeto",   xsec = 1.7355e-05 * 1.1,    feff = 0.6179, kfactor = 0.9082)
                                                                                                                     
Wmunu_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt0_70_CFilterBVeto",       xsec = 919.838769744, feff =  0.0474,  kfactor = 0.9082)
Wmunu_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt70_140_CFilterBVeto",     xsec = 100.564174092, feff =  0.175,   kfactor = 0.9082)
Wmunu_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt140_280_CFilterBVeto",    xsec = 16.649629005,  feff =  0.2035,  kfactor = 0.9082)
Wmunu_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt280_500_CFilterBVeto",    xsec = 1.160810758 * 1.1,   feff =  0.2225,  kfactor = 0.9082)
Wmunu_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt500_700_CFilterBVeto",    xsec = 0.075282837 * 1.1,   feff =  0.2398,  kfactor = 0.9082)
Wmunu_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt700_1000_CFilterBVeto",   xsec = 0.012748102 * 1.1,   feff =  0.2277,  kfactor = 0.9082)
Wmunu_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt1000_2000_CFilterBVeto",  xsec = 0.001699121 * 1.1,   feff =  0.2364,  kfactor = 0.9082)
Wmunu_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt2000_E_CMS_CFilterBVeto", xsec = 7.738e-06 * 1.1,     feff =  0.2679,  kfactor = 0.9082)
                                                                                                                     
Wmunu_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt0_70_BFilter",            xsec = 1158.97092326, feff =  0.0597,  kfactor = 0.9082)
Wmunu_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt70_140_BFilter",          xsec = 55.568454407,  feff =  0.0967,  kfactor = 0.9082)
Wmunu_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt140_280_BFilter",         xsec = 9.22013311,    feff =  0.1125,  kfactor = 0.9082)
Wmunu_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt280_500_BFilter",         xsec = 0.680142792 * 1.1,   feff =  0.1307,  kfactor = 0.9082)
Wmunu_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt500_700_BFilter",         xsec = 0.051706999 * 1.1,   feff =  0.1635,  kfactor = 0.9082)
Wmunu_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt700_1000_BFilter",        xsec = 0.00874855 * 1.1,    feff =  0.1601,  kfactor = 0.9082)
Wmunu_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt1000_2000_BFilter",       xsec = 0.001139207 * 1.1,   feff =  0.1596,  kfactor = 0.9082)
Wmunu_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt2000_E_CMS_BFilter",      xsec = 6.058e-06 * 1.1,     feff =  0.1928,  kfactor = 0.9082)

Wmunu = Sample( name =   'Wmunu',
                  tlatex = 'W #rightarrow #mu#nu+jets',
                  fill_color = ROOT.kGreen+1,
                  line_color =  ROOT.kGreen+2,
                  marker_color =  ROOT.kGreen+2,
                  daughters = [
                               Wmunu_Pt0_70_CVetoBVeto,        
                               Wmunu_Pt70_140_CVetoBVeto,                                    
                               Wmunu_Pt140_280_CVetoBVeto,     
                               Wmunu_Pt280_500_CVetoBVeto,     
                               Wmunu_Pt500_700_CVetoBVeto,     
                               Wmunu_Pt700_1000_CVetoBVeto,    
                               Wmunu_Pt1000_2000_CVetoBVeto,   
                               Wmunu_Pt2000_E_CMS_CVetoBVeto,  
                               Wmunu_Pt0_70_CFilterBVeto,      
                               Wmunu_Pt70_140_CFilterBVeto,    
                               Wmunu_Pt140_280_CFilterBVeto,   
                               Wmunu_Pt280_500_CFilterBVeto,   
                               Wmunu_Pt500_700_CFilterBVeto,   
                               Wmunu_Pt700_1000_CFilterBVeto,  
                               Wmunu_Pt1000_2000_CFilterBVeto, 
                               Wmunu_Pt2000_E_CMS_CFilterBVeto,
                               Wmunu_Pt0_70_BFilter,           
                               Wmunu_Pt70_140_BFilter,         
                               Wmunu_Pt140_280_BFilter,        
                               Wmunu_Pt280_500_BFilter,        
                               Wmunu_Pt500_700_BFilter,        
                               Wmunu_Pt700_1000_BFilter,       
                               Wmunu_Pt1000_2000_BFilter,      
                               Wmunu_Pt2000_E_CMS_BFilter,     
                              ],
                ) 

#-------
# Wtaunu
#-------

Wtaunu_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt0_70_CVetoBVeto",         xsec = 17314.4290983,  feff =  0.8914,  kfactor = 0.9082)
Wtaunu_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt70_140_CVetoBVeto",       xsec = 419.122578495,  feff =  0.7261,  kfactor = 0.9082) 
Wtaunu_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt140_280_CVetoBVeto",      xsec = 55.916387347,   feff =  0.684,   kfactor = 0.9082)
Wtaunu_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt280_500_CVetoBVeto",      xsec = 3.406527101 * 1.1,    feff =  0.6474,  kfactor = 0.9082)
Wtaunu_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt500_700_CVetoBVeto",      xsec = 0.197106496 * 1.1,    feff =  0.6289,  kfactor = 0.9082)
Wtaunu_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt700_1000_CVetoBVeto",     xsec = 0.034681733 * 1.1,    feff =  0.6274,  kfactor = 0.9082)
Wtaunu_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt1000_2000_CVetoBVeto",    xsec = 0.004373938 * 1.1,    feff =  0.6071,  kfactor = 0.9082)
Wtaunu_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt2000_E_CMS_CVetoBVeto",   xsec = 1.6536e-05 * 1.1,     feff =  0.5454,  kfactor = 0.9082)
                                                                                                                       
Wtaunu_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt0_70_CFilterBVeto",       xsec =  945.692972992, feff =  0.0487,  kfactor = 0.9082)
Wtaunu_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt70_140_CFilterBVeto",     xsec =  101.503853138, feff =  0.1763,  kfactor = 0.9082)
Wtaunu_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt140_280_CFilterBVeto",    xsec =  16.794548709,  feff =  0.205,   kfactor = 0.9082)
Wtaunu_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt280_500_CFilterBVeto",    xsec =  1.149628406 * 1.1,   feff =  0.2189,  kfactor = 0.9082)
Wtaunu_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt500_700_CFilterBVeto",    xsec =  0.074064213 * 1.1,   feff =  0.2305,  kfactor = 0.9082)
Wtaunu_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt700_1000_CFilterBVeto",   xsec =  0.012089998 * 1.1,   feff =  0.22,    kfactor = 0.9082)
Wtaunu_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt1000_2000_CFilterBVeto",  xsec =  0.001705245 * 1.1,   feff =  0.238,   kfactor = 0.9082)
Wtaunu_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt2000_E_CMS_CFilterBVeto", xsec =  6.707e-06 * 1.1,     feff =  0.2423,  kfactor = 0.9082)
                                                                                                                       
Wtaunu_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt0_70_BFilter",            xsec =  1159.25995066, feff =  0.0597,  kfactor = 0.9082)
Wtaunu_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt70_140_BFilter",          xsec =  55.038425769,  feff =  0.0957,  kfactor = 0.9082)
Wtaunu_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt140_280_BFilter",         xsec =  9.259878116,   feff =  0.1131,  kfactor = 0.9082)
Wtaunu_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt280_500_BFilter",         xsec =  0.692107677 * 1.1,   feff =  0.1325,  kfactor = 0.9082)
Wtaunu_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt500_700_BFilter",         xsec =  0.05020675 * 1.1,    feff =  0.1595,  kfactor = 0.9082)
Wtaunu_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt700_1000_BFilter",        xsec =  0.008573241 * 1.1,   feff =  0.1555,  kfactor = 0.9082)
Wtaunu_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt1000_2000_BFilter",       xsec =  0.001282272 * 1.1,   feff =  0.176,   kfactor = 0.9082)
Wtaunu_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt2000_E_CMS_BFilter",      xsec =  5.693e-06 * 1.1,     feff =  0.196,   kfactor = 0.9082)

Wtaunu = Sample( name =   'Wtaunu',
                  tlatex = 'W #rightarrow #tau#nu+jets',
                  fill_color = ROOT.kBlue+1,
                  line_color =  ROOT.kBlue+2,
                  marker_color =  ROOT.kBlue+2,
                  daughters = [
                               Wtaunu_Pt0_70_CVetoBVeto,        
                               Wtaunu_Pt70_140_CVetoBVeto,                                    
                               Wtaunu_Pt140_280_CVetoBVeto,     
                               Wtaunu_Pt280_500_CVetoBVeto,     
                               Wtaunu_Pt500_700_CVetoBVeto,     
                               Wtaunu_Pt700_1000_CVetoBVeto,    
                               Wtaunu_Pt1000_2000_CVetoBVeto,   
                               Wtaunu_Pt2000_E_CMS_CVetoBVeto,  
                               Wtaunu_Pt0_70_CFilterBVeto,      
                               Wtaunu_Pt70_140_CFilterBVeto,    
                               Wtaunu_Pt140_280_CFilterBVeto,   
                               Wtaunu_Pt280_500_CFilterBVeto,   
                               Wtaunu_Pt500_700_CFilterBVeto,   
                               Wtaunu_Pt700_1000_CFilterBVeto,  
                               Wtaunu_Pt1000_2000_CFilterBVeto, 
                               Wtaunu_Pt2000_E_CMS_CFilterBVeto,
                               Wtaunu_Pt0_70_BFilter,           
                               Wtaunu_Pt70_140_BFilter,         
                               Wtaunu_Pt140_280_BFilter,        
                               Wtaunu_Pt280_500_BFilter,        
                               Wtaunu_Pt500_700_BFilter,        
                               Wtaunu_Pt700_1000_BFilter,       
                               Wtaunu_Pt1000_2000_BFilter,      
                               Wtaunu_Pt2000_E_CMS_BFilter,     
                              ],
                ) 


#-----------------------------------------------------------------------------
# Z + jets (Sherpa)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryZjetsSherpaLight (light filter)
#                         https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryZjetsSherpaC     (C filter) 
#                         https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryZjetsSherpaB     (B filter) 
# for my tags!!!
# https://twiki.cern.ch/twiki/pub/AtlasProtected/CentralMC15ProductionList/XSections_13TeV_e3651_e4133.txt
#-----------------------------------------------------------------------------

#-----
# Zee
#-----

Zee_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt0_70_CVetoBVeto",                xsec = 1549.26000693, feff =  0.779,   kfactor = 0.9013 ) 
Zee_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt70_140_CVetoBVeto",              xsec = 44.22776987,   feff =  0.6469,  kfactor = 0.9013 )
Zee_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt140_280_CVetoBVeto",             xsec = 6.506584189,   feff =  0.6172,  kfactor = 0.9013 )
Zee_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt280_500_CVetoBVeto",             xsec = 0.407251422 * 1.1,   feff =  0.5889,  kfactor = 0.9013 )
Zee_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt500_700_CVetoBVeto",             xsec = 0.024016122 * 1.1,   feff =  0.5773,  kfactor = 0.9013 )
Zee_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt700_1000_CVetoBVeto",            xsec = 0.004150103 * 1.1,   feff =  0.5661,  kfactor = 0.9013 )
Zee_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt1000_2000_CVetoBVeto",           xsec = 0.000504024 * 1.1,   feff =  0.5369,  kfactor = 0.9013 )
Zee_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt2000_E_CMS_CVetoBVeto",          xsec = 2.004e-06 * 1.1,     feff =  0.5197,  kfactor = 0.9013 )
                                                                                                         
Zee_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt0_70_CFilterBVeto",              xsec = 282.772058138, feff =  0.1423,  kfactor = 0.9013 )
Zee_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt70_140_CFilterBVeto",            xsec = 14.952742932,  feff =  0.2182,  kfactor = 0.9013 )
Zee_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt140_280_CFilterBVeto",           xsec = 2.538900646,   feff =  0.2449,  kfactor = 0.9013 )
Zee_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt280_500_CFilterBVeto",           xsec = 0.17993672 * 1.1,    feff =  0.2617,  kfactor = 0.9013 )
Zee_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt500_700_CFilterBVeto",           xsec = 0.011351653 * 1.1,   feff =  0.2714,  kfactor = 0.9013 )
Zee_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt700_1000_CFilterBVeto",          xsec = 0.002197952 * 1.1,   feff =  0.3002,  kfactor = 0.9013 )
Zee_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt1000_2000_CFilterBVeto",         xsec = 0.000296457 * 1.1,   feff =  0.3098,  kfactor = 0.9013 )
Zee_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt2000_E_CMS_CFilterBVeto",        xsec = 1.538e-06 * 1.1,     feff =  0.3932,  kfactor = 0.9013 )
                                                                                                         
Zee_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt0_70_BFilter",                   xsec = 158.396126791, feff =  0.0797,   kfactor = 0.9013 )
Zee_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt70_140_BFilter",                 xsec = 8.994572804,   feff =  0.1311,   kfactor = 0.9013 )
Zee_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt140_280_BFilter",                xsec = 1.579281881,   feff =  0.1504,   kfactor = 0.9013 )
Zee_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt280_500_BFilter",                xsec = 0.107766448 * 1.1,   feff =  0.1562,   kfactor = 0.9013 )
Zee_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt500_700_BFilter",                xsec = 0.007056014 * 1.1,   feff =  0.1685,   kfactor = 0.9013 )
Zee_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt700_1000_BFilter",               xsec = 0.001344726 * 1.1,   feff =  0.1829,   kfactor = 0.9013 )
Zee_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt1000_2000_BFilter",              xsec = 0.000183289 * 1.1,   feff =  0.1919,   kfactor = 0.9013 )
Zee_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt2000_E_CMS_BFilter",             xsec = 8.3e-07 * 1.1,       feff =  0.2221,   kfactor = 0.9013 )

Zee = Sample( name =   'Zee',
                  tlatex = 'Z #rightarrow ee+jets',
                  fill_color = ROOT.kOrange+1,
                  line_color =  ROOT.kOrange+2,
                  marker_color =  ROOT.kOrange+2,
                  daughters = [
                               Zee_Pt0_70_CVetoBVeto,        
                               Zee_Pt70_140_CVetoBVeto,                                    
                               Zee_Pt140_280_CVetoBVeto,     
                               Zee_Pt280_500_CVetoBVeto,     
                               Zee_Pt500_700_CVetoBVeto,     
                               Zee_Pt700_1000_CVetoBVeto,    
                               Zee_Pt1000_2000_CVetoBVeto,   
                               Zee_Pt2000_E_CMS_CVetoBVeto,  
                               Zee_Pt0_70_CFilterBVeto,      
                               Zee_Pt70_140_CFilterBVeto,    
                               Zee_Pt140_280_CFilterBVeto,   
                               Zee_Pt280_500_CFilterBVeto,   
                               Zee_Pt500_700_CFilterBVeto,   
                               Zee_Pt700_1000_CFilterBVeto,  
                               Zee_Pt1000_2000_CFilterBVeto, 
                               Zee_Pt2000_E_CMS_CFilterBVeto,
                               Zee_Pt0_70_BFilter,           
                               Zee_Pt70_140_BFilter,         
                               Zee_Pt140_280_BFilter,        
                               Zee_Pt280_500_BFilter,        
                               Zee_Pt500_700_BFilter,        
                               Zee_Pt700_1000_BFilter,       
                               Zee_Pt1000_2000_BFilter,      
                               Zee_Pt2000_E_CMS_BFilter,     
                              ],
                ) 


#-------
# Zmumu
#-------

Zmumu_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt0_70_CVetoBVeto",              xsec = 1545.03412569, feff = 0.7784,  kfactor = 0.9013 )
Zmumu_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt70_140_CVetoBVeto",            xsec = 44.406818306,  feff = 0.6491,  kfactor = 0.9013 ) 
Zmumu_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt140_280_CVetoBVeto",           xsec = 6.403162188,   feff = 0.61,    kfactor = 0.9013 )
Zmumu_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt280_500_CVetoBVeto",           xsec = 0.402575488 * 1.1,   feff = 0.5808,  kfactor = 0.9013 )
Zmumu_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_CVetoBVeto",           xsec = 0.023490348 * 1.1,   feff = 0.5664,  kfactor = 0.9013 )
Zmumu_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt700_1000_CVetoBVeto",          xsec = 0.004066761 * 1.1,   feff = 0.5613,  kfactor = 0.9013 )
Zmumu_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt1000_2000_CVetoBVeto",         xsec = 0.000566401 * 1.1,   feff = 0.5491,  kfactor = 0.9013 )
Zmumu_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt2000_E_CMS_CVetoBVeto",        xsec = 2.213e-06 * 1.1,     feff = 0.5973,  kfactor = 0.9013 )
                                                                                                        
Zmumu_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt0_70_CFilterBVeto",            xsec =  281.969546386, feff = 0.1419,  kfactor = 0.9013 )
Zmumu_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt70_140_CFilterBVeto",          xsec =  15.044569464,  feff = 0.2193,  kfactor = 0.9013 )
Zmumu_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt140_280_CFilterBVeto",         xsec =  2.535541296,   feff = 0.2412,  kfactor = 0.9013 )
Zmumu_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt280_500_CFilterBVeto",         xsec =  0.185533832 * 1.1,   feff = 0.2721,  kfactor = 0.9013 )
Zmumu_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_CFilterBVeto",         xsec =  0.011157277 * 1.1,   feff = 0.2659,  kfactor = 0.9013 )
Zmumu_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt700_1000_CFilterBVeto",        xsec =  0.002053806 * 1.1,   feff = 0.2887,  kfactor = 0.9013 )
Zmumu_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt1000_2000_CFilterBVeto",       xsec =  0.000265446 * 1.1,   feff = 0.2825,  kfactor = 0.9013 )
Zmumu_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt2000_E_CMS_CFilterBVeto",      xsec =  1.207e-06 * 1.1,     feff = 0.3258,  kfactor = 0.9013 )
                                                                                                        
Zmumu_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt0_70_BFilter",                 xsec =  158.199011129, feff =  0.0796, kfactor = 0.9013 )
Zmumu_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt70_140_BFilter",               xsec =  8.937479488,   feff =  0.1303, kfactor = 0.9013 )
Zmumu_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt140_280_BFilter",              xsec =  1.554540292,   feff =  0.148,  kfactor = 0.9013 )
Zmumu_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt280_500_BFilter",              xsec =  0.113373913 * 1.1,   feff =  0.163,  kfactor = 0.9013 )
Zmumu_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_BFilter",              xsec =  0.007371738 * 1.1,   feff =  0.1764, kfactor = 0.9013 )
Zmumu_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt700_1000_BFilter",             xsec =  0.001297194 * 1.1,   feff =  0.1786, kfactor = 0.9013 )
Zmumu_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt1000_2000_BFilter",            xsec =  0.000190262 * 1.1,   feff =  0.198,  kfactor = 0.9013 )
Zmumu_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt2000_E_CMS_BFilter",           xsec =  9.39e-07 * 1.1,      feff =  0.2466, kfactor = 0.9013 )

Zmumu = Sample( name =   'Zmumu',
                  tlatex = 'Z #rightarrow #mu#mu+jets',
                  fill_color = ROOT.kSpring+1,
                  line_color =  ROOT.kSpring+2,
                  marker_color =  ROOT.kSpring+2,
                  daughters = [
                               Zmumu_Pt0_70_CVetoBVeto,        
                               Zmumu_Pt70_140_CVetoBVeto,                                    
                               Zmumu_Pt140_280_CVetoBVeto,     
                               Zmumu_Pt280_500_CVetoBVeto,     
                               Zmumu_Pt500_700_CVetoBVeto,     
                               Zmumu_Pt700_1000_CVetoBVeto,    
                               Zmumu_Pt1000_2000_CVetoBVeto,   
                               Zmumu_Pt2000_E_CMS_CVetoBVeto,  
                               Zmumu_Pt0_70_CFilterBVeto,      
                               Zmumu_Pt70_140_CFilterBVeto,    
                               Zmumu_Pt140_280_CFilterBVeto,   
                               Zmumu_Pt280_500_CFilterBVeto,   
                               Zmumu_Pt500_700_CFilterBVeto,   
                               Zmumu_Pt700_1000_CFilterBVeto,  
                               Zmumu_Pt1000_2000_CFilterBVeto, 
                               Zmumu_Pt2000_E_CMS_CFilterBVeto,
                               Zmumu_Pt0_70_BFilter,           
                               Zmumu_Pt70_140_BFilter,         
                               Zmumu_Pt140_280_BFilter,        
                               Zmumu_Pt280_500_BFilter,        
                               Zmumu_Pt500_700_BFilter,        
                               Zmumu_Pt700_1000_BFilter,       
                               Zmumu_Pt1000_2000_BFilter,      
                               Zmumu_Pt2000_E_CMS_BFilter,     
                              ],
                ) 

#---------
# Ztautau
#---------

Ztautau_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt0_70_CVetoBVeto",         xsec = 1540.4178651, feff = 0.7781,  kfactor = 0.9013 )
Ztautau_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt70_140_CVetoBVeto",       xsec = 44.65676361,  feff = 0.6479,  kfactor = 0.9013 ) 
Ztautau_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt140_280_CVetoBVeto",      xsec = 6.455693712,  feff = 0.6145,  kfactor = 0.9013 )
Ztautau_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt280_500_CVetoBVeto",      xsec = 0.401065 * 1.1,     feff = 0.581,   kfactor = 0.9013 )
Ztautau_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt500_700_CVetoBVeto",      xsec = 0.02348807 * 1.1,   feff = 0.5639,  kfactor = 0.9013 )
Ztautau_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt700_1000_CVetoBVeto",     xsec = 0.004107715 * 1.1,  feff = 0.5602,  kfactor = 0.9013 )
Ztautau_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt1000_2000_CVetoBVeto",    xsec = 0.000532212 * 1.1,  feff = 0.5636,  kfactor = 0.9013 )
Ztautau_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt2000_E_CMS_CVetoBVeto",   xsec = 2.183e-06 * 1.1,    feff = 0.5954,  kfactor = 0.9013 )
                                                                                                        
Ztautau_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt0_70_CFilterBVeto",       xsec = 282.756352896, feff = 0.1423, kfactor = 0.9013 )
Ztautau_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt70_140_CFilterBVeto",     xsec = 15.209340192,  feff = 0.222,  kfactor = 0.9013 )
Ztautau_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt140_280_CFilterBVeto",    xsec = 2.529223599,   feff = 0.2417, kfactor = 0.9013 )
Ztautau_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt280_500_CFilterBVeto",    xsec = 0.176406172 * 1.1,   feff = 0.2558, kfactor = 0.9013 )
Ztautau_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt500_700_CFilterBVeto",    xsec = 0.011224933 * 1.1,   feff = 0.2704, kfactor = 0.9013 )
Ztautau_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt700_1000_CFilterBVeto",   xsec = 0.002156445 * 1.1,   feff = 0.2984, kfactor = 0.9013 )
Ztautau_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt1000_2000_CFilterBVeto",  xsec = 0.000329597 * 1.1,   feff = 0.3483, kfactor = 0.9013 )
Ztautau_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt2000_E_CMS_CFilterBVeto", xsec = 1.415e-06 * 1.1,     feff = 0.36,   kfactor = 0.9013 )
                                                                                                        
Ztautau_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt0_70_BFilter",            xsec = 157.407818354, feff =  0.0792, kfactor = 0.9013 )
Ztautau_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt70_140_BFilter",          xsec = 8.971250612,   feff =  0.1312, kfactor = 0.9013 )
Ztautau_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt140_280_BFilter",         xsec = 1.494293679,   feff =  0.1421, kfactor = 0.9013 )
Ztautau_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt280_500_BFilter",         xsec = 0.108832258 * 1.1,   feff =  0.1589, kfactor = 0.9013 )
Ztautau_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt500_700_BFilter",         xsec = 0.007076053 * 1.1,   feff =  0.1705, kfactor = 0.9013 )
Ztautau_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt700_1000_BFilter",        xsec = 0.001318545 * 1.1,   feff =  0.1801, kfactor = 0.9013 )
Ztautau_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt1000_2000_BFilter",       xsec = 0.000161628 * 1.1,   feff =  0.1685, kfactor = 0.9013 )
Ztautau_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt2000_E_CMS_BFilter",      xsec = 9.85e-07 * 1.1,      feff =  0.2508, kfactor = 0.9013 )

Ztautau = Sample( name =   'Ztautau',
                  tlatex = 'Z #rightarrow #tau#tau+jets',
                  fill_color = ROOT.kAzure-4,
                  line_color =  ROOT.kAzure-5,
                  marker_color =  ROOT.kAzure-5,
                  daughters = [
                               Ztautau_Pt0_70_CVetoBVeto,        
                               Ztautau_Pt70_140_CVetoBVeto,                                    
                               Ztautau_Pt140_280_CVetoBVeto,     
                               Ztautau_Pt280_500_CVetoBVeto,     
                               Ztautau_Pt500_700_CVetoBVeto,     
                               Ztautau_Pt700_1000_CVetoBVeto,    
                               Ztautau_Pt1000_2000_CVetoBVeto,   
                               Ztautau_Pt2000_E_CMS_CVetoBVeto,  
                               Ztautau_Pt0_70_CFilterBVeto,      
                               Ztautau_Pt70_140_CFilterBVeto,    
                               Ztautau_Pt140_280_CFilterBVeto,   
                               Ztautau_Pt280_500_CFilterBVeto,   
                               Ztautau_Pt500_700_CFilterBVeto,   
                               Ztautau_Pt700_1000_CFilterBVeto,  
                               Ztautau_Pt1000_2000_CFilterBVeto, 
                               Ztautau_Pt2000_E_CMS_CFilterBVeto,
                               Ztautau_Pt0_70_BFilter,           
                               Ztautau_Pt70_140_BFilter,         
                               Ztautau_Pt140_280_BFilter,        
                               Ztautau_Pt280_500_BFilter,   
                               Ztautau_Pt500_700_BFilter,        
                               Ztautau_Pt700_1000_BFilter,       
                               Ztautau_Pt1000_2000_BFilter,      
                               Ztautau_Pt2000_E_CMS_BFilter,     
                              ],
                ) 


#-----------------------------------------------------------------------------
# Top 
#-----------------------------------------------------------------------------

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ttX 
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryTTbarX
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ttW_Np0                               = Sample( name =  "ttW_Np0",        xsec =  0.17656    )  
ttW_Np1                               = Sample( name =  "ttW_Np1",        xsec =  0.14062    ) 
ttW_Np2                               = Sample( name =  "ttW_Np2",        xsec =  0.1368     )
ttZnnqq_Np0                           = Sample( name =  "ttZnnqq_Np0",    xsec =  0.11122    )
ttZnnqq_Np1                           = Sample( name =  "ttZnnqq_Np1",    xsec =  0.095466   )
ttZnnqq_Np2                           = Sample( name =  "ttZnnqq_Np2",    xsec =  0.10512    )
ttee_Np0                              = Sample( name =  "ttee_Np0",       xsec =  0.0088155  )
ttee_Np1                              = Sample( name =  "ttee_Np1",       xsec =  0.01438    )
ttmumu_Np0                            = Sample( name =  "ttmumu_Np0",     xsec =  0.0088422  )                         
ttmumu_Np1                            = Sample( name =  "ttmumu_Np1",     xsec =  0.014375   )
tttautau_Np0                          = Sample( name =  "tttautau_Np0",   xsec =  0.0090148  )
tttautau_Np1                          = Sample( name =  "tttautau_Np1",   xsec =  0.014636   )

ttX = Sample( name =   'ttX',
                  tlatex = 'ttX',
                  fill_color = ROOT.kViolet+1,
                  line_color =  ROOT.kViolet+2,
                  marker_color =  ROOT.kViolet+2,
                  daughters = [
                               ttW_Np0,                
                               ttW_Np1,        
                               ttW_Np2,        
                               ttZnnqq_Np0,    
                               ttZnnqq_Np1,    
                               ttZnnqq_Np2,    
                               ttee_Np0,       
                               ttee_Np1,       
                               ttmumu_Np0,     
                               ttmumu_Np1,     
                               tttautau_Np0,   
                               tttautau_Np1,   
                              ],
                ) 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# single-top
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummarySingleTop
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
SingleTopSchan_noAllHad_top           = Sample( name =  "SingleTopSchan_noAllHad_top",       xsec =  2.0517 )
SingleTopSchan_noAllHad_antitop       = Sample( name =  "SingleTopSchan_noAllHad_antitop",   xsec =  1.2615 )
singletop_tchan_lept_top              = Sample( name =  "singletop_tchan_lept_top",          xsec =  43.739 )
singletop_tchan_lept_antitop          = Sample( name =  "singletop_tchan_lept_antitop",      xsec =  25.778 )
Wt_inclusive_top                      = Sample( name =  "Wt_inclusive_top",                  xsec =  34.009 ) 
Wt_inclusive_antitop                  = Sample( name =  "Wt_inclusive_antitop",              xsec =  33.989 )

singletop = Sample( name =   'singletop',
                    tlatex = 'single-top',
                    fill_color = ROOT.kRed+3,
                    line_color =  ROOT.kRed+4,
                    marker_color =  ROOT.kRed+4,
                    daughters = [
                                 SingleTopSchan_noAllHad_top,    
                                 SingleTopSchan_noAllHad_antitop,
                                 singletop_tchan_lept_top,       
                                 singletop_tchan_lept_antitop,   
                                 Wt_inclusive_top,               
                                 Wt_inclusive_antitop,           
                                ],
                ) 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ttbar bulk samples
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryTTbar 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ttbar_hdamp172p5_nonallhad            = Sample( name =  "ttbar_hdamp172p5_nonallhad", xsec = 451.645679998,  feff = 0.543,  kfactor = 1.1949  )
ttbar_hdamp172p5_allhad               = Sample( name =  "ttbar_hdamp172p5_allhad",    xsec = 380.11432,      feff = 0.457,  kfactor =  1.1947 )
ttbar_nonallhad                       = Sample( name =  "ttbar_nonallhad",            xsec = 451.645680001,  feff = 0.543,  kfactor =  1.1975 )

ttbar = Sample( name =  'ttbar',
                    tlatex = 'ttbar',
                    fill_color = ROOT.kCyan+1,
                    line_color =  ROOT.kCyan+2,
                    marker_color =  ROOT.kCyan+2,
                    daughters = [
                                 #ttbar_hdamp172p5_nonallhad,
                                 #ttbar_hdamp172p5_allhad,   
                                 ttbar_nonallhad,           
                                ],
                ) 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ttbar sliced samples
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryTTbarSliced 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ttbar_hdamp172p5_nonallhad_mtt_1      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_1",  xsec = 3.926242464,   feff = 0.0047,  kfactor = 1.1949 )
ttbar_hdamp172p5_nonallhad_mtt_2      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_2",  xsec = 1.617309099,   feff = 0.0019,  kfactor = 1.1949 )                         
ttbar_hdamp172p5_nonallhad_mtt_3      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_3",  xsec = 0.718018025,   feff = 0.0009,  kfactor = 1.1949 )
ttbar_hdamp172p5_nonallhad_mtt_4      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_4",  xsec = 0.431858588,   feff = 0.0005,  kfactor = 1.1949 )
ttbar_hdamp172p5_nonallhad_mtt_5      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_5",  xsec = 0.25723035,    feff = 0.0003,  kfactor = 1.1949 )
ttbarHT6c_1k_hdamp172p5_nonAH         = Sample( name =  "ttbarHT6c_1k_hdamp172p5_nonAH",     xsec = 19.068284245,  feff = 0.0229,  kfactor = 1.1949 )
ttbarHT1k_1k5_hdamp172p5_nonAH        = Sample( name =  "ttbarHT1k_1k5_hdamp172p5_nonAH",    xsec = 2.665728834,   feff = 0.0032,  kfactor = 1.1949 )
ttbarHT1k5_hdamp172p5_nonAH           = Sample( name =  "ttbarHT1k5_hdamp172p5_nonAH",       xsec = 0.470232424,   feff = 0.0006,  kfactor = 1.1949 )
ttbarMET200_hdamp172p5_nonAH          = Sample( name =  "ttbarMET200_hdamp172p5_nonAH",      xsec = 7.669803669,   feff = 0.0092,  kfactor = 1.1949 )
ttbar_hdamp345_down_nonallhad         = Sample( name =  "ttbar_hdamp345_down_nonallhad",     xsec = 451.645679999, feff = 0.543,   kfactor = 1.0613 ) 
ttbar_hdamp172_up_nonallhad           = Sample( name =  "ttbar_hdamp172_up_nonallhad",       xsec = 451.64568,     feff = 0.543,   kfactor = 1.3611 )
ttbar_hdamp172p5_nonallhad            = Sample( name =  "ttbar_hdamp172p5_nonallhad",        xsec = 451.645679998, feff = 0.543,   kfactor = 1.1949 )


ttbar_slices = Sample( name =  'ttbar_slices',
                    tlatex = 'ttbar',
                    fill_color = ROOT.kCyan+1,
                    line_color =  ROOT.kCyan+2,
                    marker_color =  ROOT.kCyan+2,
                    daughters = [
                                 #ttbar_hdamp172p5_nonallhad_mtt_1,
                                 #ttbar_hdamp172p5_nonallhad_mtt_2,
                                 #ttbar_hdamp172p5_nonallhad_mtt_3,
                                 #ttbar_hdamp172p5_nonallhad_mtt_4,
                                 #ttbar_hdamp172p5_nonallhad_mtt_5,
                                 
                                 #ttbarHT6c_1k_hdamp172p5_nonAH,   
                                 #ttbarHT1k_1k5_hdamp172p5_nonAH,  
                                 #ttbarHT1k5_hdamp172p5_nonAH,     
                                 #ttbarMET200_hdamp172p5_nonAH,    
                                 
                                 #ttbar_hdamp345_down_nonallhad,   
                                 #ttbar_hdamp172_up_nonallhad,     
                                 #ttbar_hdamp172p5_nonallhad,      #just use this one!
                                ],
                ) 

#-----------------------------------------------------------------------------
# Doubly charged Higss 
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryHiggsBSMOthers 
#-----------------------------------------------------------------------------

DCH_name =  'DCH%d'
DCH_tlatex = 'm_{H^{\pm\pm}}=%d GeV'
DCH_masses = [
    300,
    400,
    500,
    600,
    700,
    800,
    900,
    1000,
    1100,
    1200,
    1300,
    ]

for m in DCH_masses:
    name = DCH_name % m
    globals()[name] = Sample(
            name = name,
            tlatex = DCH_tlatex % (m),
            line_color = ROOT.kOrange-3,
            marker_color = ROOT.kOrange-3,
            fill_color = ROOT.kOrange-3,
            line_width  = 3,
            line_style = 1,
            fill_style = 3004,
            )

DCH300.xsec  = 0.020179   
DCH400.xsec  = 0.0059727  
DCH500.xsec  = 0.0021733  
DCH600.xsec  = 0.00089447 
DCH700.xsec  = 0.00040462 
DCH800.xsec  = 0.00019397 
DCH900.xsec  = 9.8716e-05 
DCH1000.xsec = 5.2052e-05
DCH1100.xsec = 2.8246e-05
DCH1200.xsec = 1.5651e-05
DCH1300.xsec = 8.877e-06 

list_DCH =[globals()[DCH_name%(m)] for m in DCH_masses]

all_DCH = Sample( name =  'all_DCH',
                    tlatex = 'm_{H^{\pm\pm}}=all',
                    line_color = ROOT.kOrange-3,
                    marker_color = ROOT.kOrange-3,
                    fill_color = ROOT.kOrange-3,
                    line_width  = 3,
                    line_style = 1,
                    fill_style = 3004,
                    daughters = list_DCH
                ) 

single_DCH = [DCH500]

#-------------------------------------------------------------------------------
# Collections 
#-------------------------------------------------------------------------------

all_data = data.daughters

all_mc = []
#all_mc += diboson_sherpa.daughters
#all_mc += diboson_powheg.daughters
all_mc += Wenu.daughters
all_mc += Wmunu.daughters
all_mc += Wtaunu.daughters
all_mc += Zee.daughters
all_mc += Zmumu.daughters
all_mc += Ztautau.daughters
#all_mc += ttX.daughters
all_mc += singletop.daughters
#all_mc += ttbar.daughters
#all_mc += all_DCH.daughters
#all_mc += single_DCH

## EOF
