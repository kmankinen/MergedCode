#!/bin/bash

## Batch

#INPATH="/coepp/cephfs/mel/fscutti/ssdilep/EXOT12_common_v1Ntuples/merged/nominal"
INPATH="/coepp/cephfs/mel/fscutti/ssdilep/HIGG3D3_v7/merged/nominal"

INSCRIPT="../ssdilep/run"

SCRIPT="j.plotter_FF.py"
#SCRIPT="j.plotter_FF_C1.py"
#SCRIPT="j.plotter_STUDY.py"
#SCRIPT="j.plotter_VR_TwoMu.py"
#SCRIPT="j.plotter_TAndP.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00280273.root --sampletype="data"  #--events=20000
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00302393.root --sampletype="data"  --events=20000

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00282992.root --sampletype="data" --events=20000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00302380.root --sampletype="data" --events=20000 #--config="sys:FF_DN" # example of triglist probs

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00299243.root --sampletype="data" #--config="sys:FF_DN" # example of triglist probs
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_221_NNPDF30NNLO_Wmunu_MAXHTPTV70_140_CVetoBVeto.root --sampletype="mc" --events=20000   #--config="sys:FF_DN" 
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_NNPDF30NNLO_Zmumu_Pt0_70_BFilter.root  --sampletype="mc" --events=4000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_CT10_VV_muvmuv_2000M3000.root  --sampletype="mc" --events=20000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_CT10_llvv.root  --sampletype="mc" --events=20000   #--config="sys:FF_DN" 
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_CT10_llll.root  --sampletype="mc" --events=1000   #--config="sys:FF_DN" 
