#!/bin/bash

## Batch
#python ../ZprimeTauTauHadHad2012/run/j.plotter_thesis.py \
#--input /lustre/atlas/group/higgs/TauTauHadHad/TNT/full/batch_p1443_current_merged/nominal/Wtaunu280_500_BJet.root \
#--sampletype="mc" #--config="sys:FWEIGHT_UP"

#python ../ZprimeTauTauHadHad2012/run/j.plotter.py \
#--input /lustre/atlas/group/higgs/TauTauHadHad/TNT/full/batch_p1443_current_merged/nominal/periodB.root --sampletype="data"


##python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/steve/DCH300.root --sampletype="mc" 
##python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/testarea/merged/ZqqZll_tree.root --sampletype="mc" 
##python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/testarea/merged/physics_Main_tree_00284006.root --sampletype="data" 

#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/multitrig/merged/nominal/llll.root --sampletype="mc" 
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/multitrig/merged/nominal/DCH300.root --sampletype="mc" 
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/multitrig/merged/nominal/Wmunu_Pt0_70_CFilterBVeto.root --sampletype="mc" 
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/multitrig/merged/nominal/Zmumu_Pt140_280_CVetoBVeto.root --sampletype="mc" 


#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/menu_HLT_2mu10/merged/nominal/DCH300.root --sampletype="mc" 
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/menu_HLT_2mu10/merged/nominal/physics_Main_00276262.root --sampletype="data"

#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/menu_lowptasym/merged/nominal/physics_Main_00276262.root --sampletype="data"
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/menu_lowptasym/merged/nominal/Zmumu_Pt500_700_CVetoBVeto.root --sampletype="mc"
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/menu_lowptasym/merged/nominal/Zee_Pt140_280_CFilterBVeto.root --sampletype="mc"

python ../ssdilep/run/j.plotter_VR_TwoMu.py --input /data/fscutti/ssdilep/menu_singlemu/merged/nominal/physics_Main_00276262.root --sampletype="data"
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/menu_nonisosingle/merged/nominal/physics_Main_00276262.root --sampletype="data"

#python ../ZprimeTauTauHadHad2012/run/j.plotter.py \
#--input /lustre/atlas/group/higgs/TauTauHadHad/TNT/full/batch_p1443_current_merged/nominal/ttbar_allhad.root --sampletype="mc" ##--config="sys:FWEIGHT_UP"


#python ../ZprimeTauTauHadHad2012/run/j.plotter.py \
#--input /lustre/atlas/group/higgs/TauTauHadHad/TNT/full/batch_p1443_v00-02-10_merged/nominal/ggHtautauhh_MA1000TB20.root --sampletype="mc" ###--config="sys:FWEIGHT_UP,FW_unc_is_stat:Wplusjets"


#python ../ssdilep/run/j.plotter_VR.py --input /data/fscutti/ssdilep/presc/merged/nominal/physics_Main_00276262.root --sampletype="data" #--config="sys:FF_DN"

#python ../ssdilep/run/j.plotter_VR.py --input /data/fscutti/test/user.fscutti.8548367._000001.tree.root --sampletype="data" #--config="sys:FF_DN"
#python ../ssdilep/run/j.plotter_VR.py --input /data/fscutti/test/user.fscutti.8550085._000001.tree.root --sampletype="mc" #--config="sys:FF_DN"


#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/presc/merged/nominal/physics_Main_00283608.root --sampletype="data"
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/presc/merged/nominal/llll.root --sampletype="mc"
#python ../ssdilep/run/j.plotter.py --input /data/fscutti/ssdilep/presc/merged/nominal/Wmunu_Pt140_280_CVetoBVeto.root --sampletype="mc"


## test TNT
#python ../ZprimeTauTauHadHad2012/run/j.plotter.py \
#--input /lustre/atlas/group/higgs/TauTauHadHad/TNT/full/test_tnt_ggHtautauhh_MA400TB20.root --sampletype="mc" 
## old TNT
#python ../ZprimeTauTauHadHad2012/run/j.plotter.py \
#--input /lustre/atlas/group/higgs/TauTauHadHad/TNT/full/batch_p1443_current_merged/nominal/ggHtautauhh_MA400TB20.root \
#--sampletype="mc" 
