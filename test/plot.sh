#!bin/bash

# Strings are passed to the script but this is redundant!

python ../ssdilep/scripts/merge.py --var="probe_pt" --reg="PROBE_LOOSE" --lab="signal region" --icut="4" --input="/coepp/cephfs/mel/skeyte/ssdilep/Hist18Aug" --output="./" --makeplot=False --fakest="Subtraction"

#python ../ssdilep/scripts/merge.py --var="mumu_reldeltapt" --reg="SR_NUM" --lab="signal region" --icut="5" --input="/coepp/cephfs/mel/skeyte/ssdilep/HistTEST" --output="./" --makeplot=True --fakest="FakeFactor"

#python ../ssdilep/scripts/merge.py --var="mumu_deltapt" --reg="SR_NUM" --lab="signal region" --icut="5" --input="/coepp/cephfs/mel/skeyte/ssdilep/HistTEST" --output="./" --makeplot=True --fakest="FakeFactor"

#python ../ssdilep/scripts/merge.py --var="mumu_mVis" --reg="SR_NUM" --lab="signal region" --icut="5" --input="/coepp/cephfs/mel/skeyte/ssdilep/HistTEST" --output="./" --makeplot=True --fakest="FakeFactor"
