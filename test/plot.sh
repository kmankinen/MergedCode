#!bin/bash


# -------------------------------

#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F0" --lab="numerator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F0" --lab="denominator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_NUM_F1" --lab="numerator" --tag="corr" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mulead_pt" --reg="FAKES_DEN_F1" --lab="denominator" --tag="corr" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="FAKES_NUM_F0" --lab="numerator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="met_clus_et" --reg="FAKES_DEN_F0" --lab="denominator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mujet_dphi" --reg="FAKES_NUM_F0" --lab="numerator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"
#python ../ssdilep/scripts/merge.py --var="mujet_dphi" --reg="FAKES_DEN_F0" --lab="denominator" --tag="corr" --icut="1" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistPassAndMatch" --output="./" --makeplot=True --fakest="Subtraction"


python ../ssdilep/scripts/merge.py --var="muons_mVis" --reg="FAKESVR6_MAINREG" --lab="VR" --tag="test" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistNewVR" --output="./" --makeplot=True --fakest="ReducedRegions"




