#!bin/bash

# Strings are passed to the script but this is redundant!

python ../ssdilep/scripts/merge.py --var="mumu_mulead_pt" --reg="FAKESVR2_NUM" --lab="TEST REGION" --icut="5" --input="/coepp/cephfs/mel/fscutti/ssdilep/HistQUOKKA" --output="./" --makeplot=False --fakest="Subtraction"

