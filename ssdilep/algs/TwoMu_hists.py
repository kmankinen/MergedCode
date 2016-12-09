from histconfig import *


hists_list = []


# -------
# event
# -------
hists_list.append(h_averageIntPerXing)
hists_list.append(h_actualIntPerXing)
#hists_list.append(h_correct_mu)
hists_list.append(h_NPV)
hists_list.append(h_nmuons)
hists_list.append(h_nelectrons)
hists_list.append(h_njets)
hists_list.append(h_muons_chargeprod)
hists_list.append(h_muons_dphi)
hists_list.append(h_muons_deta)
hists_list.append(h_muons_mVis)
hists_list.append(h_muons_mTtot)
hists_list.append(h_scdphi)


# -------
# muons
# -------

# mulead
hists_list.append(h_mulead_pt)
hists_list.append(h_mulead_eta)
hists_list.append(h_mulead_phi)
hists_list.append(h_mulead_trkd0)
hists_list.append(h_mulead_trkd0sig)
hists_list.append(h_mulead_trkz0)
hists_list.append(h_mulead_trkz0sintheta)
hists_list.append(h_mulead_ptvarcone30)

# musublead
hists_list.append(h_musublead_pt)
hists_list.append(h_musublead_eta)
hists_list.append(h_musublead_phi)
hists_list.append(h_musublead_trkd0)
hists_list.append(h_musublead_trkd0sig)
hists_list.append(h_musublead_trkz0)
hists_list.append(h_musublead_trkz0sintheta)
hists_list.append(h_musublead_ptvarcone30)


# -------
# MET
# -------
hists_list.append(h_met_clus_et)
hists_list.append(h_met_clus_phi)
hists_list.append(h_met_trk_et)
hists_list.append(h_met_trk_phi)
hists_list.append(h_met_clus_sumet)
hists_list.append(h_met_trk_sumet)


# EOF






