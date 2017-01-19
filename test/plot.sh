#!bin/bash



# ------------
# FAKE FACTORS
# ------------
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F1" --lab="numerator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F1" --lab="denominator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F2" --lab="numerator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F2" --lab="denominator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F3" --lab="numerator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F3" --lab="denominator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F4" --lab="numerator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F4" --lab="denominator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F5" --lab="numerator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F5" --lab="denominator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F6" --lab="numerator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F6" --lab="denominator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F7" --lab="numerator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F7" --lab="denominator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F8" --lab="numerator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F8" --lab="denominator" --tag="bound" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="jetlead_pt" --reg="FAKES_DEN_F1" --lab="denominator" --tag="rew" --icut="6" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanFF" --output="./" --makeplot=False --fakest="Subtraction"


# -------------
# TAG AND PROBE
# -------------
python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R1" --lab="FakeFilter_SS" --tag="fakefilter_ss" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R2" --lab="AntiTruth_SS" --tag="antitruth_ss" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R3" --lab="FakeFilter_OS" --tag="fakefilter_os" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R4" --lab="AntiTruth_OS" --tag="antitruth_os" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R1" --lab="FakeFilter_SS" --tag="fakefilter_ss" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R2" --lab="AntiTruth_SS" --tag="antitruth_ss" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R3" --lab="FakeFilter_OS" --tag="fakefilter_os" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R4" --lab="AntiTruth_OS" --tag="antitruth_os" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="probe_ujet_pt" --reg="ProbeLoose_F1" --lab="TruthFilter_SS" --tag="truthfilter_ss" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="probe_ujet_pt" --reg="ProbeLoose_F2" --lab="TruthFilter_OS" --tag="truthfilter_os" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanTP" --output="./" --makeplot=False --fakest="Subtraction"

# ----------
# VALIDATION
# ----------
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR2_MAINREG" --lab="VR" --tag="v1" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist17JanV1VR" --output="./" --makeplot=True --fakest="ReducedRegions"
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR1_MAINREG" --lab="VR" --tag="v2" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/Hist18JanV2VR" --output="./" --makeplot=True --fakest="ReducedRegions"




