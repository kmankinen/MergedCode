#!/bin/bash

## Batch

INPATH="/coepp/cephfs/mel/fscutti/ssdilep/menu_singlemu/merged/nominal"
INSCRIPT="../ssdilep/run"
SCRIPT="j.plotter_SigEff.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00276262.root --sampletype="data" #--config="sys:FF_DN"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Zmumu_Pt1000_2000_CVetoBVeto.root --sampletype="mc" #--config="sys:FF_DN"


