import os
import ROOT
from array import array

ROOT.gROOT.SetBatch(True)
rcol = [ROOT.kBlack,ROOT.kBlue+1,
   ROOT.kRed,
   ROOT.kRed+1, 
   ROOT.kRed+2,
   ROOT.kRed+3,
   ROOT.kGreen,
   ROOT.kGreen+1,
   ROOT.kGreen+2,
   ROOT.kGreen+3,
   ROOT.kBlue,
   ROOT.kBlue+1,
   ROOT.kBlue+2,
   ROOT.kBlue+3,
   ROOT.kMagenta, 
   ROOT.kMagenta+1,
   ROOT.kMagenta+2,
   ROOT.kMagenta+3,
   ROOT.kYellow,
   ROOT.kYellow+1,
   ROOT.kYellow+2,
   ROOT.kYellow+3]


c_all = ROOT.TCanvas("c_all_ff","c_all_ff",650,600)
c_all.SetTopMargin(0.05)
c_all.SetBottomMargin(0.13)
c_all.SetLeftMargin(0.13)
c_all.SetRightMargin(0.05)
c_all.SetTickx()
c_all.SetTicky()


for i in xrange(1,9):
  num_file = ROOT.TFile.Open("hists_mulead_pt_FAKESFR%s_NUM.root"%i,"READ")
  den_file = ROOT.TFile.Open("hists_mulead_pt_FAKESFR%s_DEN.root"%i,"READ")

  h_nom = num_file.Get("h_FAKESFR%s_NUM_nominal_fakes"%i).Clone()
  h_nom.SetNameTitle("h_nom","h_nom")
  h_den = den_file.Get("h_FAKESFR%s_DEN_nominal_fakes"%i).Clone()
  h_den.SetNameTitle("h_den","h_den")

  #new_bins = array('d', [22.,23.,24.,26.,28.,30.,34.,38.,45.,80.])
  #new_bins = array('d', [12.,16.,20.,24.,28.,33.,40.,60.,150.])
  #new_bins = array('d', [20.,30.,40.,50.,60.,70.,80.,90.,100.])
  new_bins = array('d', [22.,23.,25.,28.,32.,36.,40.,45.,60.,100.])
 
  h_new_nom = h_nom.Rebin(len(new_bins)-1,"h_new_nom",new_bins)
  h_new_den = h_den.Rebin(len(new_bins)-1,"h_new_den",new_bins)
 
  h_ff = h_new_nom.Clone()
  h_ff.Divide(h_new_den)
 
  h_ff.SetNameTitle("h_ff_FR%s"%i,"")
  h_ff.GetYaxis().SetTitle("Fake-factor")
  h_ff.GetYaxis().SetTitleOffset(1.1)
  h_ff.GetXaxis().SetTitleOffset(1.1)
  h_ff.GetXaxis().SetRangeUser(0.,100.)
  h_ff.SetLineColor(rcol[i-1])
  h_ff.SetMarkerColor(rcol[i-1])
  h_ff.SetMarkerSize(0.01)
  h_ff.SetMaximum(1.0)
  h_ff.SetMinimum(0)
  
  c_all.cd()
  if i==1: h_ff.Draw("E1 SAME")
  else: h_ff.Draw("E1 SAME")
  
  c = ROOT.TCanvas("c_ff_FR%s"%i,"c_ff_FR%s"%i,650,600)
  c.SetTopMargin(0.05)
  c.SetBottomMargin(0.13)
  c.SetLeftMargin(0.13)
  c.SetRightMargin(0.05)
  c.SetTickx()
  c.SetTicky()
  c.cd() 
  
  h_ff.Draw("E1")
  
  ff_file = ROOT.TFile.Open("histsys_ff_DebugFF%s.root"%i,"RECREATE")
  
  ff_file.WriteTObject(h_ff)
  ff_file.WriteTObject(c)

#ff_all_file = ROOT.TFile.Open("histsys_ff__AllFinFF.root","RECREATE")
#ff_all_file.WriteTObject(c_all)
 


