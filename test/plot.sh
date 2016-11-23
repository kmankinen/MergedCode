#!bin/bash

# Strings are passed to the scrieta but this is redundant!
python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR1_NUM" --lab="newxs" --tag="TEST" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR2_NUM" --lab="newxs" --tag="TEST" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR3_NUM" --lab="newxs" --tag="TEST" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR4_NUM" --lab="newxs" --tag="TEST" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR5_NUM" --lab="newxs" --tag="TEST" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"
python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR6_NUM" --lab="newxs" --tag="TEST" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"




#python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR1_TLDEN" --lab="newxs" --tag="TEST" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"
#python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR1_LTDEN" --lab="newxs" --tag="TEST" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"
#python ../ssdilep/scripts/merge.py --var="nmuons" --reg="FAKESVR1_LLDEN" --lab="newxs" --tag="TEST" --icut="4" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistMultiMu" --output="./" --makeplot=True --fakest="FakeFactor"
