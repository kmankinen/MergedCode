import ROOT
import array
import os

from ROOT import *

#from ssdilep.samples import samples
#from ssdilep.plots   import vars
#from systematics     import *

#--------- one and three prong ------------#

f = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_pt_PROBE_TIGHT.root')
hist_Zmumu_pt_tight = f.Get('h_PROBE_TIGHT_nominal_data')

g = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_pt_PROBE_TIGHT_TRIGMATCHED.root')
hist_Zmumu_pt_tight_trigmatched = g.Get('h_PROBE_TIGHT_TRIGMATCHED_nominal_data')

h = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_eta_PROBE_TIGHT.root')
hist_Zmumu_eta_tight = h.Get('h_PROBE_TIGHT_nominal_data')

i = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_eta_PROBE_TIGHT_TRIGMATCHED.root')
hist_Zmumu_eta_tight_trigmatched = i.Get('h_PROBE_TIGHT_TRIGMATCHED_nominal_data')

j = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_phi_PROBE_TIGHT.root')
hist_Zmumu_phi_tight = j.Get('h_PROBE_TIGHT_nominal_data')

k = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_phi_PROBE_TIGHT_TRIGMATCHED.root')
hist_Zmumu_phi_tight_trigmatched = k.Get('h_PROBE_TIGHT_TRIGMATCHED_nominal_data')

l = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_pt_PROBE_LOOSE.root')
hist_Zmumu_pt_loose = l.Get('h_PROBE_LOOSE_nominal_data')

m = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_pt_PROBE_LOOSE_TRIGMATCHED.root')
hist_Zmumu_pt_loose_trigmatched = m.Get('h_PROBE_LOOSE_TRIGMATCHED_nominal_data')

n = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_eta_PROBE_LOOSE.root')
hist_Zmumu_eta_loose = n.Get('h_PROBE_LOOSE_nominal_data')

o = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_eta_PROBE_LOOSE_TRIGMATCHED.root')
hist_Zmumu_eta_loose_trigmatched = o.Get('h_PROBE_LOOSE_TRIGMATCHED_nominal_data')

p = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_phi_PROBE_LOOSE.root')
hist_Zmumu_phi_loose = p.Get('h_PROBE_LOOSE_nominal_data')

q = ROOT.TFile('/coepp/cephfs/mel/skeyte/SSDiLep/test/hists_probe_phi_PROBE_LOOSE_TRIGMATCHED.root')
hist_Zmumu_phi_loose_trigmatched = q.Get('h_PROBE_LOOSE_TRIGMATCHED_nominal_data')


print hist_Zmumu_pt_tight, hist_Zmumu_pt_tight_trigmatched, hist_Zmumu_eta_tight, hist_Zmumu_eta_tight_trigmatched, hist_Zmumu_phi_tight, hist_Zmumu_phi_tight_trigmatched, hist_Zmumu_pt_loose, hist_Zmumu_pt_loose_trigmatched, hist_Zmumu_eta_loose, hist_Zmumu_eta_loose_trigmatched, hist_Zmumu_phi_loose, hist_Zmumu_phi_loose_trigmatched, 

hist_Zmumu_pt_tight.SetXTitle('')
hist_Zmumu_pt_tight.SetYTitle('Efficiency')
hist_Zmumu_pt_tight.SetTitle('')
hist_Zmumu_pt_tight_trigmatched.SetXTitle('')
hist_Zmumu_pt_tight_trigmatched.SetYTitle('Efficiency')
hist_Zmumu_pt_tight_trigmatched.SetTitle('')

hist_Zmumu_eta_tight.SetXTitle('')
hist_Zmumu_eta_tight.SetYTitle('Efficiency')
hist_Zmumu_eta_tight.SetTitle('')
hist_Zmumu_eta_tight_trigmatched.SetXTitle('')
hist_Zmumu_eta_tight_trigmatched.SetYTitle('Efficiency')
hist_Zmumu_eta_tight_trigmatched.SetTitle('')

hist_Zmumu_phi_tight.SetXTitle('')
hist_Zmumu_phi_tight.SetYTitle('Efficiency')
hist_Zmumu_phi_tight.SetTitle('')
hist_Zmumu_phi_tight_trigmatched.SetXTitle('')
hist_Zmumu_phi_tight_trigmatched.SetYTitle('Efficiency')
hist_Zmumu_phi_tight_trigmatched.SetTitle('')

hist_Zmumu_pt_loose.SetXTitle('')
hist_Zmumu_pt_loose.SetYTitle('Efficiency')
hist_Zmumu_pt_loose.SetTitle('')
hist_Zmumu_pt_loose_trigmatched.SetXTitle('')
hist_Zmumu_pt_loose_trigmatched.SetYTitle('Efficiency')
hist_Zmumu_pt_loose_trigmatched.SetTitle('')

hist_Zmumu_eta_loose.SetXTitle('')
hist_Zmumu_eta_loose.SetYTitle('Efficiency')
hist_Zmumu_eta_loose.SetTitle('')
hist_Zmumu_eta_loose_trigmatched.SetXTitle('')
hist_Zmumu_eta_loose_trigmatched.SetYTitle('Efficiency')
hist_Zmumu_eta_loose_trigmatched.SetTitle('')

hist_Zmumu_phi_loose.SetXTitle('')
hist_Zmumu_phi_loose.SetYTitle('Efficiency')
hist_Zmumu_phi_loose.SetTitle('')
hist_Zmumu_phi_loose_trigmatched.SetXTitle('')
hist_Zmumu_phi_loose_trigmatched.SetYTitle('Efficiency')
hist_Zmumu_phi_loose_trigmatched.SetTitle('')

#pt efficiency plots

rebin1 = [0.,15.,16.,17.,18.,20.,22.,25.,28.,30.,32.,34.,36.,39.,40.,52.,64.,80.,100.,150.,300.]
hist_Zmumu_pt_tight = hist_Zmumu_pt_tight.Rebin(len(rebin1)-1,"hist_Zmumu_pt_tight",array.array('d',rebin1))
hist_Zmumu_pt_tight_trigmatched = hist_Zmumu_pt_tight_trigmatched.Rebin(len(rebin1)-1,"hist_Zmumu_pt_tight_trigmatched",array.array('d',rebin1))

hist_Zmumu_pt_loose = hist_Zmumu_pt_loose.Rebin(len(rebin1)-1,"hist_Zmumu_pt_loose",array.array('d',rebin1))
hist_Zmumu_pt_loose_trigmatched = hist_Zmumu_pt_loose_trigmatched.Rebin(len(rebin1)-1,"hist_Zmumu_pt_loose_trigmatched",array.array('d',rebin1))

#print " *** pT data *** " 
#hist_Zmumu_pt_tight.Print("all")
#hist_Zmumu_pt_tight_trigmatched.Print("all")

#hist_Zmumu_pt_loose.Print("all")
#hist_Zmumu_pt_loose_trigmatched.Print("all")


h_trigger_efficiency_Zmumu_pt_tight = hist_Zmumu_pt_tight_trigmatched.Clone()
h_trigger_efficiency_Zmumu_pt_tight.Divide(hist_Zmumu_pt_tight_trigmatched, hist_Zmumu_pt_tight, 1.0, 1.0, "B")

h_trigger_efficiency_Zmumu_pt_loose = hist_Zmumu_pt_loose_trigmatched.Clone()
h_trigger_efficiency_Zmumu_pt_loose.Divide(hist_Zmumu_pt_loose_trigmatched, hist_Zmumu_pt_loose, 1.0, 1.0, "B")


#phi efficiency plots

rebin2 = [-3.2,-2.56,-1.92,-1.28,-0.64,0.,0.64,1.28,1.92,2.56]
hist_Zmumu_phi_tight = hist_Zmumu_phi_tight.Rebin(len(rebin2)-1,"hist_Zmumu_phi_tight",array.array('d',rebin2))
hist_Zmumu_phi_tight_trigmatched = hist_Zmumu_phi_tight_trigmatched.Rebin(len(rebin2)-1,"hist_Zmumu_phi_tight_trigmatched",array.array('d',rebin2))

hist_Zmumu_phi_loose = hist_Zmumu_phi_loose.Rebin(len(rebin2)-1,"hist_Zmumu_phi_loose",array.array('d',rebin2))
hist_Zmumu_phi_loose_trigmatched = hist_Zmumu_phi_loose_trigmatched.Rebin(len(rebin2)-1,"hist_Zmumu_phi_loose_trigmatched",array.array('d',rebin2))

h_trigger_efficiency_Zmumu_phi_tight = hist_Zmumu_phi_tight_trigmatched.Clone()
h_trigger_efficiency_Zmumu_phi_tight.Divide(hist_Zmumu_phi_tight_trigmatched, hist_Zmumu_phi_tight, 1.0, 1.0, "B")

h_trigger_efficiency_Zmumu_phi_loose = hist_Zmumu_phi_loose_trigmatched.Clone()
h_trigger_efficiency_Zmumu_phi_loose.Divide(hist_Zmumu_phi_loose_trigmatched, hist_Zmumu_phi_loose, 1.0, 1.0, "B")

#eta efficiency plots

rebin3 = [-2.5,-2.,-1.5,-1.,-0.5,0.,0.5,1.,1.5,2.]
hist_Zmumu_eta_tight = hist_Zmumu_eta_tight.Rebin(len(rebin3)-1,"hist_Zmumu_eta_tight",array.array('d',rebin3))
hist_Zmumu_eta_tight_trigmatched = hist_Zmumu_eta_tight_trigmatched.Rebin(len(rebin3)-1,"hist_Zmumu_eta_tight_trigmatched",array.array('d',rebin3))

hist_Zmumu_eta_loose = hist_Zmumu_eta_loose.Rebin(len(rebin3)-1,"hist_Zmumu_eta_loose",array.array('d',rebin3))
hist_Zmumu_eta_loose_trigmatched = hist_Zmumu_eta_loose_trigmatched.Rebin(len(rebin3)-1,"hist_Zmumu_eta_loose_trigmatched",array.array('d',rebin3))

h_trigger_efficiency_Zmumu_eta_tight = hist_Zmumu_eta_tight_trigmatched.Clone()
h_trigger_efficiency_Zmumu_eta_tight.Divide(hist_Zmumu_eta_tight_trigmatched, hist_Zmumu_eta_tight, 1.0, 1.0, "B")

h_trigger_efficiency_Zmumu_eta_loose = hist_Zmumu_eta_loose_trigmatched.Clone()
h_trigger_efficiency_Zmumu_eta_loose.Divide(hist_Zmumu_eta_loose_trigmatched, hist_Zmumu_eta_loose, 1.0, 1.0, "B")

outfile = ROOT.TFile('Zmumu_trigger_efficiency.root','recreate')

h_trigger_efficiency_Zmumu_pt_tight.Write()
h_trigger_efficiency_Zmumu_pt_loose.Write()
h_trigger_efficiency_Zmumu_phi_tight.Write()
h_trigger_efficiency_Zmumu_phi_loose.Write()
h_trigger_efficiency_Zmumu_eta_tight.Write()
h_trigger_efficiency_Zmumu_eta_loose.Write()
outfile.Close()


"""
h_samp_list = []
h_samp_list.append(h_efficiency_simple_mc)
h_total = funcs.histutils.add_hists(h_samp_list)
h_total_stat = funcs.make_stat_hist(h_total)
g_stat = funcs.make_band_graph_from_hist(h_total_stat)
g_stat.SetFillColor(ROOT.kGray+1)
g_tot = None

h_data = h_efficiency_simple_subztt.Clone()
h_ratio = h_data.Clone()
h_ratio.Divide(h_efficiency_simple_mc)
h_data.SetStats(0)

yaxistitle = ""

nLegend = 2
x_legend = 0.63
x_leg_shift = 0
y_leg_shift = 0.0
legYCompr = 8.0
legYMax = 0.5
legYMin = legYMax - (legYMax - (0.2 + y_leg_shift)) / legYCompr * nLegend
legXMin = x_legend + x_leg_shift
legXMax = legXMin + 0.4

leg = ROOT.TLegend(0.6,0.5,0.7,0.6) #ROOT.TLegend(legXMin,legYMin,legXMax,legYMax)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.AddEntry(h_efficiency_simple_subztt,"Data",'PL')
leg.AddEntry(h_efficiency_simple_mc,"Z#rightarrow#tau#tau",'F')

c = ROOT.TCanvas("efficiency","efficiency",750,800)
xmin = h_total.GetBinLowEdge(1)
xmax = 300 
ymin = 0
ymax = 1.1 #h_total.GetMaximum()
#ymax *= 1.8
xtitle = ""

rsplit = 0.3
pad1 = ROOT.TPad("pad1","top pad",0.,rsplit,1.,1.)
pad1.SetLeftMargin(0.15)
pad1.SetTicky()
pad1.SetTickx()
pad1.SetBottomMargin(0.04)
pad1.SetLogx()
pad1.Draw()

pad2 = ROOT.TPad("pad2","bottom pad",0,0,1,rsplit)
pad2.SetTopMargin(0.04)
pad2.SetBottomMargin(0.40)
pad2.SetLeftMargin(0.15)
pad2.SetTicky()
pad2.SetTickx()
pad2.SetGridy()
pad2.SetLogx()
pad2.Draw()
pad1.cd()

ytitle = "Efficiency"
#ytitle = yaxistitle

fr1 = pad1.DrawFrame(xmin,ymin,xmax,ymax,';%s;%s'%(xtitle,ytitle))
fr1.GetXaxis().SetTitleSize(0)
fr1.GetXaxis().SetLabelSize(0)
xaxis1 = fr1.GetXaxis()
yaxis1 = fr1.GetYaxis()
scale = (1.3+rsplit)
yaxis1.SetTitleSize( yaxis1.GetTitleSize() * scale )
yaxis1.SetTitleOffset( 2.1 * yaxis1.GetTitleOffset() / scale )
yaxis1.SetLabelSize( 0.8 * yaxis1.GetLabelSize() * scale )
yaxis1.SetLabelOffset( 1. * yaxis1.GetLabelOffset() / scale )
xaxis1.SetNdivisions(510)
yaxis1.SetNdivisions(510)
yaxis1.SetTitle("Efficiency")

h_efficiency_simple_mc.Draw("E2")
h_efficiency_simple_subztt.Draw("same")

leg.Draw()
pad1.RedrawAxis()
tlatex = ROOT.TLatex()
tlatex.SetNDC()
tlatex.SetTextSize(0.05)
lx = 0.5 # for ATLAS internal
ly = 0.845
tlatex.SetTextFont(42)

ty = 0.4
th = 0.05
tx = 0.5
latex_y = ty-2.*th
latex_yb = ty-4.*th
#tlatex.SetTextAlign(10)
tlatex.DrawLatex(0.6,0.3,'#intL dt = 3.2 fb^{-1}, #sqrt{s} = 13 TeV}' ) #(tx,latex_y,'#intL dt = 3.2 fb^{-1}, #sqrt{s} = 13 TeV}' )
tlatex.DrawLatex(0.6,0.2,'HLT_tau35_medium1_tracktwo') #(tx,latex_yb,'HLT_tau35_medium1_tracktwo')
tlatex.SetTextSize=0.001
pad2.cd()

fr2 = pad2.DrawFrame(xmin,0.8,xmax,1.2,';%s;SF'%('Tau Pt'))

xaxis2 = fr2.GetXaxis()
yaxis2 = fr2.GetYaxis()

scale = (1. / rsplit)
yaxis2.SetTitleSize( yaxis2.GetTitleSize() * scale )
yaxis2.SetLabelSize( yaxis2.GetLabelSize() * scale )
yaxis2.SetTitleOffset( 2.1* yaxis2.GetTitleOffset() / scale  )
yaxis2.SetLabelOffset(0.2 * yaxis2.GetLabelOffset() * scale )
xaxis2.SetTitleSize( xaxis2.GetTitleSize() * scale )
xaxis2.SetLabelSize( 0.8 * xaxis2.GetLabelSize() * scale )
xaxis2.SetTickLength( xaxis2.GetTickLength() * scale )
xaxis2.SetTitleOffset( 3.2* xaxis2.GetTitleOffset() / scale  )
xaxis2.SetLabelOffset( 2.5* xaxis2.GetLabelOffset() / scale )
yaxis2.SetNdivisions(510)
xaxis2.SetNdivisions(510)
yaxis2.SetTitle("SF")

g_stat.Draw("E2")
h_ratio.Draw("Same")
pad2.RedrawAxis()
plotsfile = os.path.join("./","eff_2015_threeprong_35med.root")
#c.SaveAs("Test")
fout = ROOT.TFile.Open(plotsfile,'UPDATE')
fout.WriteTObject(c)
fout.Close()
"""
