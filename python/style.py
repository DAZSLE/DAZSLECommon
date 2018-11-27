import ROOT
from ROOT import *
gSystem.Load("~/DAZSLE/CMSSW_7_4_7/lib/slc6_amd64_gcc491/libMyToolsRootUtils.so")
gInterpreter.Declare("#include \"MyTools/RootUtils/interface/SeabornInterface.h\"")
seaborn = Root.SeabornInterface()
seaborn.Initialize()

background_colors = {
	"qcd":seaborn.GetColorRoot("cubehelixlarge", 0, 24),
	"tqq":seaborn.GetColorRoot("cubehelixlarge", 3, 24),
	"zqq":seaborn.GetColorRoot("cubehelixlarge", 6, 24),
	"wqq":seaborn.GetColorRoot("cubehelixlarge", 9, 24),
	"hbb":seaborn.GetColorRoot("cubehelixlarge", 12, 24),
	"vvqq":seaborn.GetColorRoot("cubehelixlarge", 15, 24),
	"stqq":seaborn.GetColorRoot("cubehelixlarge", 18, 24),
	"zll":seaborn.GetColorRoot("cubehelixlarge", 21, 24),
	"wlnu":seaborn.GetColorRoot("cubehelixlarge", 23, 24),
}
# Higgs aliases
background_colors["hqq"] = background_colors["hbb"]

axis_titles = {
	"msd":"m_{SD} [GeV]",
	"pt":"p_{T} [GeV]",
	"dcsv":"Double b-tag",
	"n2ddt":"N_{2}^{1,DDT}",
	"rho":"#rho",
	"pfmet":"PF E_{T}^{miss}",
	"eta":"#eta"
}

background_legends = {
	"qcd":"QCD",
	"tqq":"t#bar{t}",
	"zqq":"Z#rightarrowq#bar{q}",
	"wqq":"W#rightarrowq#bar{q}",
	"hbb":"H#rightarrow b#bar{b}",
	"vvqq":"Diboson",
	"stqq":"Single t",
	"zll":"Z#rightarrowll",
	"wlnu":"W#rightarrowl#nu"
}