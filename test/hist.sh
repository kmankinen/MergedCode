#!/bin/bash

## Batch

INPATH="/coepp/cephfs/mel/fscutti/ssdilep/HIGG3D3_v2_p2689/merged/nominal"
INSCRIPT="../ssdilep/run"
SCRIPT="j.plotter_FFEff_Loose.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00276262.root --sampletype="data" #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_NNPDF30NNLO_Zmumu_Pt70_140_BFilter.root --sampletype="mc" --events=500 #--config="sys:FF_DN"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00300687.root --sampletype="data" --events=500 #--config="sys:FF_DN"


