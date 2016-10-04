#!bin/bash

# Strings are passed to the scrieta but this is redundant!


python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR1_NUM" --lab="numerator" --tag="Sherpa" --icut="8" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=True --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR1_DEN" --lab="numerator" --tag="Sherpa" --icut="8" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=True --fakest="Subtraction"

<<"COMMENT"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR2_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR2_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR3_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR3_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR4_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR4_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR5_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR5_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR6_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR6_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR7_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR7_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"

python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR8_NUM" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"
python ../ssdilep/scripts/merge.py --var="mulead_eta" --reg="FAKESFR8_DEN" --lab="numerator" --tag="Sherpa" --icut="9" --input="/coepp/cephfs/mel/pttaylor/ssdilep/HistTEST" --output="./" --makeplot=False --fakest="Subtraction"
COMMENT



