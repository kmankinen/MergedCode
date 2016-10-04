#!/bin/bash

## Batch

INPATH="/coepp/cephfs/mel/fscutti/ssdilep/HIGG3D3_p2689/merged/nominal"
INSCRIPT="../ssdilep/run"
SCRIPT="j.plotter_FF.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00282992.root --sampletype="data" --events=200 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00302380.root --sampletype="data" --events=200 #--config="sys:FF_DN"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_BFilter.root --sampletype="mc" --events=200   #--config="sys:FF_DN" 
