from hists import *


"""
This contains the histogram
configuration. Do not create
other config files !!!
"""


# -------
# event
# -------
h_averageIntPerXing = Hist1D( hname  = "h_averageIntPerXing",
                              xtitle = "averageInteractionsPerCrossing",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -0.5,
                              xmax   = 49.5,
                              dir    = "event",
                              vexpr  = "self.chain.averageInteractionsPerCrossing",
                            )

h_actualIntPerXing = Hist1D( hname  = "h_actualIntPerXing",
                              xtitle = "actualInteractionsPerCrossing",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -0.5,
                              xmax   = 49.5,
                              dir    = "event",
                              vexpr  = "self.chain.actualInteractionsPerCrossing",
                            )

h_correct_mu = Hist1D( hname  = "h_correct_mu",
                              xtitle = "<#mu_{corr}>",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -0.5,
                              xmax   = 49.5,
                              dir    = "event",
                              vexpr  = "self.chain.correct_mu",
                            )

h_NPV = Hist1D( hname  = "h_NPV",
                              xtitle = "NPV",
                              ytitle = "Events", 
                              nbins  = 35,
                              xmin   = 0.,
                              xmax   = 35.0,
                              dir    = "event",
                              vexpr  = "self.chain.NPV",
                            )

h_nmuons = Hist1D( hname  = "h_nmuons",
                              xtitle = "N_{#mu}",
                              ytitle = "Events", 
                              nbins  = 8,
                              xmin   = 0,
                              xmax   = 8,
                              dir    = "event",
                              vexpr  = "self.chain.nmuon",
                            )

h_nelectrons = Hist1D( hname  = "h_nelectrons",
                              xtitle = "N_{e}",
                              ytitle = "Events", 
                              nbins  = 8,
                              xmin   = 0,
                              xmax   = 8,
                              dir    = "event",
                              vexpr  = "self.chain.nel",
                            )

h_njets = Hist1D( hname  = "h_njets",
                              xtitle = "N_{jet}",
                              ytitle = "Events", 
                              nbins  = 8,
                              xmin   = 0,
                              xmax   = 8,
                              dir    = "event",
                              vexpr  = "self.chain.njets",
                            )

h_muons_chargeprod  = Hist1D( hname  = "h_muons_chargeprod",
                              xtitle = "q(#mu_{lead}) #timesq (#mu_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['charge_product']",
                            )

h_muons_dphi  = Hist1D( hname  = "h_muons_dphi",
                              xtitle = "#Delta#phi(#mu_{lead},#mu_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['muons_dphi']",
                            )

h_muons_deta  = Hist1D( hname  = "h_muons_deta",
                              xtitle = "#Delta#eta(#mu_{lead},#mu_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['muons_deta']",
                            )

h_muons_mVis  = Hist1D( hname  = "h_muons_mVis",
                              xtitle = "m_{vis}(#mu_{lead},#mu_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis']/GeV",
                            )

h_muons_mTtot  = Hist1D( hname  = "h_muons_mTtot",
                              xtitle = "m^{tot}_{T}(#mu_{lead},#mu_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mTtot']/GeV",
                            )

h_mujet_dphi  = Hist1D( hname  = "h_mujet_dphi",
                              xtitle = "#Delta#phi(#mu_{lead},jet_{lead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['mujet_dphi']",
                            )

h_scdphi  = Hist1D( hname  = "h_scdphi",
                              xtitle = "#Sigma cos#Delta#phi",
                              ytitle = "Events", 
                              nbins  = 400,
                              xmin   = -2.,
                              xmax   = 2.,
                              dir    = "event",
                              vexpr  = "self.store['scdphi']",
                            )

h_electrons_chargeprod  = Hist1D( hname  = "h_electrons_chargeprod",
                              xtitle = "q(e_{lead}) #timesq (e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['charge_product']",
                            )

h_electrons_dphi  = Hist1D( hname  = "h_electrons_dphi",
                              xtitle = "#Delta#phi(e_{lead},e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['electrons_dphi']",
                            )

h_electrons_deta  = Hist1D( hname  = "h_electrons_deta",
                              xtitle = "#Delta#eta(e_{lead},e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['electrons_deta']",
                            )

h_electrons_mVis  = Hist1D( hname  = "h_electrons_mVis",
                              xtitle = "m_{vis}(e_{lead},e_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis']/GeV",
                            )

h_ejet_dphi  = Hist1D( hname  = "h_ejet_dphi",
                              xtitle = "#Delta#phi(e_{lead},jet_{lead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['ejet_dphi']",
)


# -------
# jets
# -------
h_jetlead_pt  = Hist1D( hname  = "h_jetlead_pt",
                              xtitle = "p_{T}(jet_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "jets",
                              vexpr  = "self.store['jets'][0].tlv.Pt()/GeV",
                            )


# -------
# muons
# -------

# mulead
# ------
h_mulead_pt = Hist1D( hname  = "h_mulead_pt",
                              xtitle = "p_{T}(#mu_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].tlv.Pt() / GeV",
                            )

h_mulead_eta = Hist1D( hname  = "h_mulead_eta",
                              xtitle = "#eta(#mu_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].tlv.Eta()",
                            )

h_mulead_phi = Hist1D( hname  = "h_mulead_phi",
                              xtitle = "#phi(#mu_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].tlv.Phi()",
                            )

h_mulead_trkd0 = Hist1D( hname  = "h_mulead_trkd0",
                              xtitle = "d^{trk}_{0}(#mu_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].trkd0",
                            )

h_mulead_trkd0sig = Hist1D( hname  = "h_mulead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (#mu_{lead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].trkd0sig",
                            )

h_mulead_trkz0 = Hist1D( hname  = "h_mulead_trkz0",
                              xtitle = "z^{trk}_{0}(#mu_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].trkz0",
                            )

h_mulead_trkz0sintheta  = Hist1D( hname  = "h_mulead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(#mu_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].trkz0sintheta",
                            )

h_mulead_ptvarcone30  = Hist1D( hname  = "h_mulead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(#mu_{lead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].ptvarcone30 / self.store['muons'][0].tlv.Pt()",
                            )

# musublead
# ---------
h_musublead_pt = Hist1D( hname  = "h_musublead_pt",
                              xtitle = "p_{T}(#mu_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].tlv.Pt() / GeV",
                            )

h_musublead_eta = Hist1D( hname  = "h_musublead_eta",
                              xtitle = "#eta(#mu_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].tlv.Eta()",
                            )

h_musublead_phi = Hist1D( hname  = "h_musublead_phi",
                              xtitle = "#phi(#mu_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].tlv.Phi()",
                            )

h_musublead_trkd0 = Hist1D( hname  = "h_musublead_trkd0",
                              xtitle = "d^{trk}_{0}(#mu_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].trkd0",
                            )

h_musublead_trkd0sig = Hist1D( hname  = "h_musublead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (#mu_{sublead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].trkd0sig",
                            )

h_musublead_trkz0 = Hist1D( hname  = "h_musublead_trkz0",
                              xtitle = "z^{trk}_{0}(#mu_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].trkz0",
                            )

h_musublead_trkz0sintheta  = Hist1D( hname  = "h_musublead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(#mu_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].trkz0sintheta",
                            )

h_musublead_ptvarcone30  = Hist1D( hname  = "h_musublead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(#mu_{sublead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].ptvarcone30 / self.store['muons'][1].tlv.Pt()",
                            )

# -------------
# tag and probe
# -------------
h_tag_pt = Hist1D( hname  = "h_tag_pt",
                              xtitle = "p_{T}(#mu_{tag}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['tag'].tlv.Pt() / GeV",
                            )

h_probe_pt = Hist1D( hname  = "h_probe_pt",
                              xtitle = "p_{T}(#mu_{probe}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['probe'].tlv.Pt() / GeV",
                            )

h_probe_ptiso = Hist1D( hname  = "h_probe_ptiso",
                              xtitle = "p_{T}(#mu_{probe}) + ptvarcone30 [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 1000,
                              xmin   = 0.0,
                              xmax   = 1000.0,
                              dir    = "muons",
                              vexpr  = "( self.store['probe'].tlv.Pt() + self.store['probe'].ptvarcone30 ) / GeV",
                            )

h_probe_ujet_pt = Hist1D( hname  = "h_probe_ujet_pt",
                              xtitle = "p_{T}(#mu_{probe} underlying jet) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2100,
                              xmin   = -100.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['probe_ujet_pt']",
                            )

h_tag_ptvarcone30  = Hist1D( hname  = "h_tag_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(#mu_{tag})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['tag'].ptvarcone30 / self.store['tag'].tlv.Pt()",
                            )
h_probe_ptvarcone30  = Hist1D( hname  = "h_probe_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(#mu_{probe})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['probe'].ptvarcone30 / self.store['probe'].tlv.Pt()",
                            )

# -------
# MET
# -------
h_met_clus_et  = Hist1D( hname  = "h_met_clus_et",
                              xtitle = "E^{miss}_{T}(clus) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.,
                              xmax   = 2000.,
                              dir    = "met",
                              vexpr  = "self.store['met_clus'].tlv.Pt()/GeV",
                            )

h_met_clus_phi  = Hist1D( hname  = "h_met_clus_phi",
                              xtitle = "#phi(E^{miss}_{T}(clus))",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "met",
                              vexpr  = "self.store['met_clus'].tlv.Phi()",
                            )

h_met_trk_et  = Hist1D( hname  = "h_met_trk_et",
                              xtitle = "E^{miss}_{T}(trk) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.,
                              xmax   = 2000.,
                              dir    = "met",
                              vexpr  = "self.store['met_trk'].tlv.Pt()/GeV",
                            )

h_met_trk_phi  = Hist1D( hname  = "h_met_trk_phi",
                              xtitle = "#phi(E^{miss}_{T}(trk))",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "met",
                              vexpr  = "self.store['met_trk'].tlv.Phi()",
                            )

h_met_clus_sumet  = Hist1D( hname  = "h_met_clus_sumet",
                              xtitle = "#Sigma E_{T}(clus) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.,
                              xmax   = 2000.,
                              dir    = "met",
                              vexpr  = "self.store['met_clus'].sumet/GeV",
                          )

h_met_trk_sumet  = Hist1D( hname  = "h_met_trk_sumet",
                              xtitle = "#Sigma E_{T}(trk) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.,
                              xmax   = 2000.,
                              dir    = "met",
                              vexpr  = "self.store['met_trk'].sumet/GeV",
                          )


# --------
# 2D hists
# --------
h_mulead_ptiso_jetlead_pt  = Hist2D( hname      = "h_mulead_ptiso_jetlead_pt",
                              xtitle  = "p_{T}(#mu_{lead}) + ptvarcone30 [GeV]",
                              ytitle  = "p_{T}(jet_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = "( self.store['muons'][0].tlv.Pt() + self.store['muons'][0].ptvarcone30 ) / GeV , self.store['jets'][0].tlv.Pt() / GeV",
                          )


h_mulead_pt_mulead_iso  = Hist2D( hname      = "h_mulead_pt_mulead_iso",
                              xtitle  = "p_{T}(#mu_{lead}) [GeV]",
                              ytitle  = "ptvarcone30(#mu_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = "self.store['muons'][0].tlv.Pt() / GeV , self.store['muons'][0].ptvarcone30 / GeV",
                          )

h_mulead_pt_jetlead_pt  = Hist2D( hname      = "h_mulead_pt_jetlead_pt",
                              xtitle  = "p_{T}(#mu_{lead}) [GeV]",
                              ytitle  = "p_{T}(jet_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = " self.store['muons'][0].tlv.Pt() / GeV , self.store['jets'][0].tlv.Pt() / GeV",
                          )

#-----------
# electrons
#-----------

h_electrons_chargeprod  = Hist1D( hname  = "h_electrons_chargeprod",
                              xtitle = "q(e_{lead}) #timesq (e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['charge_product']",
                            )

h_electrons_dphi  = Hist1D( hname  = "h_electrons_dphi",
                              xtitle = "#Delta#phi(e_{lead},e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['electrons_dphi']",
                            )

h_electrons_deta  = Hist1D( hname  = "h_electrons_delta",
                              xtitle = "#Delta#eta(e_{lead},e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['electrons_deta']",
                            )

h_electrons_mVis  = Hist1D( hname  = "h_electrons_mVis",
                              xtitle = "m_{vis}(e_{lead},e_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis']/GeV",
                            )

h_electrons_mTtot  = Hist1D( hname  = "h_electrons_mTtot",
                              xtitle = "m^{tot}_{T}(e_{lead},e_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mTtot']/GeV",
                            )

h_ejet_dphi  = Hist1D( hname  = "h_ejet_dphi",
                              xtitle = "#Delta#phi(e_{lead},jet_{lead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['ejet_dphi']",
)

# ele lead
# ------
h_elelead_pt = Hist1D( hname  = "h_elelead_pt",
                              xtitle = "p_{T}(e_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].tlv.Pt() / GeV",
                            )

h_elelead_eta = Hist1D( hname  = "h_elelead_eta",
                              xtitle = "#eta(e_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].tlv.Eta()",
                            )

h_elelead_phi = Hist1D( hname  = "h_elelead_phi",
                              xtitle = "#phi(e_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].tlv.Phi()",
                            )

h_elelead_trkd0 = Hist1D( hname  = "h_elelead_trkd0",
                              xtitle = "d^{trk}_{0}(e_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].trkd0",
                            )

h_elelead_trkd0sig = Hist1D( hname  = "h_elelead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (e_{lead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].trkd0sig",
                            )

h_elelead_trkz0 = Hist1D( hname  = "h_elelead_trkz0",
                              xtitle = "z^{trk}_{0}(e_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].trkz0",
                            )

h_elelead_trkz0sintheta  = Hist1D( hname  = "h_elelead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(e_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].trkz0sintheta",
                            )

h_elelead_ptvarcone30  = Hist1D( hname  = "h_elelead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(e_{lead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].ptvarcone30 / self.store['electrons'][0].tlv.Pt()",
                            )

# elesublead
# ---------
h_elesublead_pt = Hist1D( hname  = "h_elesublead_pt",
                              xtitle = "p_{T}(e_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].tlv.Pt() / GeV",
                            )

h_elesublead_eta = Hist1D( hname  = "h_elesublead_eta",
                              xtitle = "#eta(e_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].tlv.Eta()",
                            )

h_elesublead_phi = Hist1D( hname  = "h_elesublead_phi",
                              xtitle = "#phi(e_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].tlv.Phi()",
                            )

h_elesublead_trkd0 = Hist1D( hname  = "h_elesublead_trkd0",
                              xtitle = "d^{trk}_{0}(e_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].trkd0",
                            )

h_elesublead_trkd0sig = Hist1D( hname  = "h_elesublead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (e_{sublead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].trkd0sig",
                            )

h_elesublead_trkz0 = Hist1D( hname  = "h_elesublead_trkz0",
                              xtitle = "z^{trk}_{0}(e_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].trkz0",
                            )

h_elesublead_trkz0sintheta  = Hist1D( hname  = "h_elesublead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(e_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].trkz0sintheta",
                            )

h_elesublead_ptvarcone30  = Hist1D( hname  = "h_elesublead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(e_{sublead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].ptvarcone30 / self.store['electrons'][1].tlv.Pt()",
)

# -------------
# tag and probe
# -------------
h_eletag_pt = Hist1D( hname  = "h_eletag_pt",
                              xtitle = "p_{T}(e_{tag}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['tag'].tlv.Pt() / GeV",
                            )

h_eleprobe_pt = Hist1D( hname  = "h_eleprobe_pt",
                              xtitle = "p_{T}(e_{probe}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['probe'].tlv.Pt() / GeV",
                            )

h_eleprobe_ptiso = Hist1D( hname  = "h_eleprobe_ptiso",
                              xtitle = "p_{T}(e_{probe}) + ptvarcone30 [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 1000,
                              xmin   = 0.0,
                              xmax   = 1000.0,
                              dir    = "electrons",
                              vexpr  = "( self.store['probe'].tlv.Pt() + self.store['probe'].ptvarcone30 ) / GeV",
                            )

h_eleprobe_ujet_pt = Hist1D( hname  = "h_eleprobe_ujet_pt",
                              xtitle = "p_{T}(e_{probe} underlying jet) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2100,
                              xmin   = -100.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['probe_ujet_pt']",
                            )

h_eletag_ptvarcone30  = Hist1D( hname  = "h_eletag_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(e_{tag})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['tag'].ptvarcone30 / self.store['tag'].tlv.Pt()",
                            )
h_eleprobe_ptvarcone30  = Hist1D( hname  = "h_eleprobe_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(e_{probe})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['probe'].ptvarcone30 / self.store['probe'].tlv.Pt()",
)

# --------
# 2D hists
# --------
h_elelead_ptiso_jetlead_pt  = Hist2D( hname      = "h_elelead_ptiso_jetlead_pt",
                              xtitle  = "p_{T}(e_{lead}) + ptvarcone30 [GeV]",
                              ytitle  = "p_{T}(jet_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = "( self.store['electrons'][0].tlv.Pt() + self.store['electrons'][0].ptvarcone30 ) / GeV , self.store['jets'][0].tlv.Pt() / GeV",
                          )


h_elelead_pt_elelead_iso  = Hist2D( hname      = "h_elelead_pt_elelead_iso",
                              xtitle  = "p_{T}(e_{lead}) [GeV]",
                              ytitle  = "ptvarcone30(e_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = "self.store['electrons'][0].tlv.Pt() / GeV , self.store['electrons'][0].ptvarcone30 / GeV",
                          )

h_elelead_pt_jetlead_pt  = Hist2D( hname      = "h_elelead_pt_jetlead_pt",
                              xtitle  = "p_{T}(e_{lead}) [GeV]",
                              ytitle  = "p_{T}(jet_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = " self.store['electrons'][0].tlv.Pt() / GeV , self.store['jets'][0].tlv.Pt() / GeV",

                          )

# EOF
