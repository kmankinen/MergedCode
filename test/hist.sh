#!/bin/bash

## Batch

INPATH="/coepp/cephfs/mel/fscutti/ssdilep/menu_singlemu/merged/nominal"
INSCRIPT="../ssdilep/run"
SCRIPT="j.plotter_OPT.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00276262.root --sampletype="data" #--config="sys:FF_DN"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/llll.root --sampletype="mc" #--config="sys:FF_DN"
