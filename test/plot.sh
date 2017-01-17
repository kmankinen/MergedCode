#!bin/bash


# -------------------------------

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F0" --lab="numerator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistFianlFF" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F0" --lab="denominator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F1" --lab="numerator" --tag="corr" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F1" --lab="denominator" --tag="corr" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistBound2FF" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="FAKES_NUM_F0" --lab="numerator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="FAKES_DEN_F0" --lab="denominator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mujet_dphi" --reg="FAKES_NUM_F0" --lab="numerator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mujet_dphi" --reg="FAKES_DEN_F0" --lab="denominator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"


# main region of VR
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR1_MAINREG" --lab="VR" --tag="full" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="FullRegions"
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR2_MAINREG" --lab="VR" --tag="full" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="FullRegions"
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR3_MAINREG" --lab="VR" --tag="full" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="FullRegions"

python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKESVR1_MAINREG" --lab="VR" --tag="testV1" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistNewTESTV1" --output="./" --makeplot=True --fakest="ReducedRegions"
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR2_MAINREG" --lab="VR" --tag="redu" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="ReducedRegions"
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR3_MAINREG" --lab="VR" --tag="redu" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="ReducedRegions"



#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKESVR1_TT" --lab="VR" --tag="redu" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR1_LL" --lab="VR" --tag="redu" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR1_LT" --lab="VR" --tag="redu" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR1_LL" --lab="VR" --tag="redu" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistVRFullMatrix" --output="./" --makeplot=True --fakest="Subtraction"



#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R1" --lab="numerator" --tag="mc" --icut="3" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistNewWTTFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R1" --lab="denominator" --tag="mc" --icut="3" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistNewWTTFakes" --output="./" --makeplot=False --fakest="Subtraction"


#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R1" --lab="numerator" --tag="mc" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMCFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R1" --lab="denominator" --tag="mc" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMCFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R2" --lab="numerator" --tag="mc" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMCFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R2" --lab="denominator" --tag="mc" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMCFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R3" --lab="numerator" --tag="mc" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMCFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R3" --lab="denominator" --tag="mc" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMCFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeTight_R4" --lab="numerator" --tag="mc" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMCFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="ProbeLoose_R4" --lab="denominator" --tag="mc" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMCFakes" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F1" --lab="numerator" --tag="mc" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistDiJetFakes" --output="./" --makeplot=False --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F1" --lab="denominator" --tag="mc" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistDiJetFakes" --output="./" --makeplot=False --fakest="Subtraction"
