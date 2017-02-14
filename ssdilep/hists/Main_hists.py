from histconfig import *


hist_list = []


# -------
# event
# -------
hist_list.append(h_averageIntPerXing)
hist_list.append(h_actualIntPerXing)
#hist_list.append(h_correct_mu)
hist_list.append(h_NPV)
hist_list.append(h_nmuons)
hist_list.append(h_nelectrons)
hist_list.append(h_njets)
hist_list.append(h_muons_chargeprod)
hist_list.append(h_muons_dphi)
hist_list.append(h_muons_deta)
hist_list.append(h_muons_mVis)
hist_list.append(h_muons_mTtot)
hist_list.append(h_electrons_chargeprod)
hist_list.append(h_electrons_dphi)
hist_list.append(h_electrons_deta)
hist_list.append(h_electrons_mVis)
hist_list.append(h_electrons_mTtot)


# -------
# muons
# -------

# mulead
hist_list.append(h_mulead_pt)
hist_list.append(h_mulead_eta)
hist_list.append(h_mulead_phi)
hist_list.append(h_mulead_trkd0)
hist_list.append(h_mulead_trkd0sig)
hist_list.append(h_mulead_trkz0)
hist_list.append(h_mulead_trkz0sintheta)
hist_list.append(h_mulead_ptvarcone30)

# musublead
hist_list.append(h_musublead_pt)
hist_list.append(h_musublead_eta)
hist_list.append(h_musublead_phi)
hist_list.append(h_musublead_trkd0)
hist_list.append(h_musublead_trkd0sig)
hist_list.append(h_musublead_trkz0)
hist_list.append(h_musublead_trkz0sintheta)
hist_list.append(h_musublead_ptvarcone30)


# -------
# electrons
# -------

# elelead
hist_list.append(h_elelead_pt)
hist_list.append(h_elelead_eta)
hist_list.append(h_elelead_phi)
hist_list.append(h_elelead_trkd0)
hist_list.append(h_elelead_trkd0sig)
hist_list.append(h_elelead_trkz0)
hist_list.append(h_elelead_trkz0sintheta)
hist_list.append(h_elelead_ptvarcone30)

# elesublead
hist_list.append(h_elesublead_pt)
hist_list.append(h_elesublead_eta)
hist_list.append(h_elesublead_phi)
hist_list.append(h_elesublead_trkd0)
hist_list.append(h_elesublead_trkd0sig)
hist_list.append(h_elesublead_trkz0)
hist_list.append(h_elesublead_trkz0sintheta)
hist_list.append(h_elesublead_ptvarcone30)

# -------
# MET
# -------
hist_list.append(h_met_clus_et)
hist_list.append(h_met_clus_phi)
hist_list.append(h_met_trk_et)
hist_list.append(h_met_trk_phi)
hist_list.append(h_met_clus_sumet)
hist_list.append(h_met_trk_sumet)


# EOF






