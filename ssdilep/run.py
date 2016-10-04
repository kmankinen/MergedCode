import os

# -------
# pytools
# -------
import utils


# ----
# ROOT
# ----
import ROOT

GeV = 1000.

INPATH = "/data/fscutti/ssdilep/steve"
INFILE = "llll.root"

input = os.path.join(INPATH,INFILE)
utils.assert_file(input) 

f = ROOT.TFile.Open(input,"READ")
ch = f.Get("physics")
ch.Print()
n_entries = ch.GetEntries()
for i in xrange(n_entries):
  ch.GetEntry(i)
  n_muons = ch.muon_pt.size()
  for m in xrange(n_muons):
    print ch.muon_pt.at(m) / GeV
# EOF






