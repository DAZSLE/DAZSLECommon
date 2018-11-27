#!/usr/bin/env python
import ROOT as r, sys, math, os
from multiprocessing import Process
from optparse import OptionParser
from operator import add
import math
import sys
import time
import array
import re

#r.gSystem.Load("~/Dropbox/RazorAnalyzer/python/lib/libRazorRun2.so")
r.gSystem.Load(os.getenv('CMSSW_BASE')+'/lib/'+os.getenv('SCRAM_ARCH')+'/libHiggsAnalysisCombinedLimit.so')


# including other directories
import DAZSLE.DAZSLECommon.rhalphabet.tools as tools
from DAZSLE.DAZSLECommon.rhalphabet.RootIterator import RootIterator
from DAZSLE.DAZSLECommon.rhalphabet.histogram_container import HistogramContainer, uncorrelate

re_sbb = re.compile("Sbb(?P<mass>\d+)")
re_ptbin = re.compile("cat(?P<ptbin>\d+)")

##############################################################################
##############################################################################
#### B E G I N N I N G   O F   C L A S S
##############################################################################
##############################################################################

class RhalphabetBuilder():
	def __init__(self, pass_hists, fail_hists, input_file, out_dir, nr=2, np=1, mass_nbins=23, mass_lo=40, mass_hi=201, blind_lo=110, blind_hi=131, rho_lo=-6, rho_hi=-2.1, blind=False, mass_fit=False, freeze_poly=False, quiet=False, signal_names=None, background_names=["wqq", "zqq", "qcd", "tqq", "hqq125","tthqq125","vbfhqq125","whqq125","zhqq125"]):
		self._quiet = quiet
		self._pass_hists = pass_hists
		self._fail_hists = fail_hists
		if set(self._pass_hists.keys()) != set(self._fail_hists.keys()):
			print "[RhalphabetBuilder::__init__] ERROR : Key mismatch between pass_hists and fail_hists."
			print "[RhalphabetBuilder::__init__] ERROR : pass_hists keys = ",
			print self._pass_hists.keys()
			print "[RhalphabetBuilder::__init__] ERROR : fail_hists keys = ",
			print self._fail_hists.keys()
		self._processes = self._pass_hists.keys()
		self._mass_fit = mass_fit
		self._freeze = freeze_poly
		self._inputfile = input_file
		self._systematics = ['JES', 'JER', 'trigger', 'mcstat','Pu', "scalept", "smear"]

		self._output_path = "{}/base.root".format(out_dir)
		self._rhalphabet_output_path = "{}/rhalphabase.root".format(out_dir)

		self._outfile_validation = r.TFile.Open("{}/validation.root".format(out_dir), "RECREATE");

		self._mass_nbins = mass_nbins
		self._mass_lo = mass_lo
		self._mass_hi = mass_hi
		self._blind = blind
		self._mass_blind_lo = blind_lo
		self._mass_blind_hi = blind_hi
		self._rho_lo = rho_lo
		self._rho_hi = rho_hi
		# self._mass_nbins = pass_hists[0].GetXaxis().GetNbins()
		# self._mass_lo    = pass_hists[0].GetXaxis().GetBinLowEdge( 1 )
		# self._mass_hi    = pass_hists[0].GetXaxis().GetBinUpEdge( self._mass_nbins )

		if not self._quiet:
			print "number of mass bins and lo/hi: ", self._mass_nbins, self._mass_lo, self._mass_hi;

		# polynomial order for fit
		self._poly_degree_rho = nr  # 1 = linear ; 2 is quadratic
		self._poly_degree_pt = np  # 1 = linear ; 2 is quadratic

		self._nptbins = pass_hists["data_obs"].GetYaxis().GetNbins()
		self._pt_lo = pass_hists["data_obs"].GetYaxis().GetBinLowEdge(1)
		self._pt_hi = pass_hists["data_obs"].GetYaxis().GetBinUpEdge(self._nptbins)
		self._ptbins = []
		for ipt in range(0,self._nptbins+1):
			self._ptbins.append(pass_hists["data_obs"].GetYaxis().GetBinLowEdge(ipt+1))

		# define RooRealVars
		self._lMSD = r.RooRealVar("x", "x", self._mass_lo, self._mass_hi)
		self._lMSD.setRange('Low', self._mass_lo, self._mass_blind_lo)
		self._lMSD.setRange('Blind', self._mass_blind_lo, self._mass_blind_hi)
		self._lMSD.setRange('High', self._mass_blind_hi, self._mass_hi)
		# self._lMSD.setBins(self._mass_nbins)
		self._lPt = r.RooRealVar("pt", "pt", self._pt_lo, self._pt_hi)
		self._lPt.setBins(self._nptbins)
		self._lRho = r.RooFormulaVar("rho", "log(x*x/pt/pt)", r.RooArgList(self._lMSD, self._lPt))

		self._lEff = r.RooRealVar("veff", "veff", 0.5, 0., 1.0)

		self._lEffQCD = r.RooRealVar("qcdeff", "qcdeff", 0.01, 0., 10.)
		qcd_pass_integral = 0
		qcd_fail_integral = 0
		for i in range(1, fail_hists["qcd"].GetNbinsX() + 1):
			for j in range(1, fail_hists["qcd"].GetNbinsY() + 1):
				if fail_hists["qcd"].GetXaxis().GetBinCenter(i) > self._mass_lo and fail_hists[
					"qcd"].GetXaxis().GetBinCenter(i) < self._mass_hi:
					qcd_fail_integral += fail_hists["qcd"].GetBinContent(i, j)
					qcd_pass_integral += pass_hists["qcd"].GetBinContent(i, j)
		if qcd_fail_integral > 0:
			qcdeff = qcd_pass_integral / qcd_fail_integral
			self._lEffQCD.setVal(qcdeff)
		print "qcdeff = %f" % qcdeff
		self._lDM = r.RooRealVar("dm", "dm", 0., -10, 10)
		self._lShift = r.RooFormulaVar("shift", self._lMSD.GetName() + "-dm", r.RooArgList(self._lMSD, self._lDM))

		self._all_vars = []
		self._all_shapes = []
		self._all_data = []
		self._all_pars = []

		self._background_names = background_names
		self._signal_names = signal_names
		# for Pbb
		#for mass in [50,75,125,100,150,200,250,300]:
		#    self._signal_names.append("DMSbb" + str(mass))
		# for mass in [50,75,125,100,150,250,300]:
		#    self._signal_names.append("Pbb_" + str(mass))
		# for Hbb
		#for mass in [125]:
		#    for sig in ["hqq", "zhqq", "whqq", "vbfhqq", "tthqq"]:
		#        self._signal_names.append(sig + str(mass))

	def set_background_names(self, background_names):
		self._background_names = background_names

	def set_signal_names(self, signal_names):
		self._signal_names = signal_names

	# Add systematics, for systematics involving histograms
	# - systematics = list of systematics e.g. ["JER", "JES", "mcstat", ...]
	# - pass_hists_syst, fail_hists_syst = dictionaries, e.g. {"JERUp":h_jerup, "JERDown":h_jerdown, ...}
	def add_systematics(self, systematics, pass_hists_syst, fail_hists_syst):
		# Check that the list of systematics corresponds to the histograms
		for syst in systematics:
			for direction in ["Up", "Down"]:
				if not syst + direction in pass_hists_syst:
					print "[RhalphabetBuilder::add_systematics_histograms] ERROR : " + syst + direction +  " is not in pass_hists_syst."
					sys.exit(1)
				if not syst + direction in fail_hists_syst:
					print "[RhalphabetBuilder::add_systematics_histograms] ERROR : " + syst + direction +  " is not in fail_hists_syst."
					sys.exit(1)
		self._systematics = systematics
		self._pass_hists_syst = pass_hists_syst
		self._fail_hists_syst = fail_hists_syst
		print "[RhalphabetBuilder::add_systematics_histograms] INFO : Including systematics: ",
		print self._systematics

	def set_poly_order(self, nr, np):
		self._poly_degree_rho = nr  # 1 = linear ; 2 is quadratic
		self._poly_degree_pt = np  # 1 = linear ; 2 is quadratic

	def set_mass_bins(self, mass_nbins, mass_lo, mass_hi):
		self._mass_nbins = mass_nbins
		self._mass_lo = mass_lo
		self._mass_hi = mass_hi

	def set_blind_range(self, blind_lo, blind_hi):
		blind = True
		self._mass_blind_lo = blind_lo
		self._mass_blind_hi = blind_hi

	def set_rho_range(self, rho_lo, rho_hi):
		self._rho_lo = rho_lo
		self._rho_hi = rho_hi


	def run(self):
		self.LoopOverPtBins()

	def addHptShape(self):
		fbase = r.TFile.Open(self._output_path, 'update')

		categories = ['pass_cat1', 'pass_cat2', 'pass_cat3', 'pass_cat4', 'pass_cat5', 'pass_cat6',
					  'fail_cat1', 'fail_cat2', 'fail_cat3', 'fail_cat4', 'fail_cat5', 'fail_cat6']

		wbase = {}
		for cat in categories:
			wbase[cat] = fbase.Get('w_%s' % cat)
		x = wbase[categories[0]].var('x')
		rooCat = r.RooCategory('cat', 'cat')

		histpdf = {}
		datahist = {}
		hptpdfUp_s = {}
		hptpdfDown_s = {}
		signorm = {}
		all_int = 0
		all_int_rescale_Down = 0
		all_int_rescale_Up = 0
		proc = 'hqq125'
		#total_unc = 1.3 # -> cat6 has 130% SF w.r.t cat1
		#total_unc = 1.6 # -> cat6 has 160% SF w.r.t. cat1
		total_unc = 3.0 # -> cat6 has 300% SF w.r.t. cat1
		iptlo = self._ptbins[0]
		ipthi = self._ptbins[-2]
		for cat in categories:
			iptbin = int(cat[-1])-1 # returns 0 for cat1, 1 for cat2, etc.
			ipt = self._ptbins[iptbin]
			rooCat.defineType(cat)
			datahist['%s_%s' % (proc, cat)] = wbase[cat].data('%s_%s' % (proc, cat))
			myint = datahist['%s_%s' % (proc, cat)].sumEntries()
			all_int_rescale_Up += myint * (1 + (ipt-iptlo) * (total_unc-1.) / (ipthi-iptlo))
			all_int_rescale_Down += myint / (1 + (ipt-iptlo) * (total_unc-1.) / (ipthi-iptlo))
			all_int += myint
			if not self._quiet:
				print cat, (1 + (ipt-iptlo) * (total_unc-1.) / (ipthi-iptlo))

		for cat in categories:           
			iptbin = int(cat[-1])-1 # returns 0 for cat1, 1 for cat2, etc.
			ipt = self._ptbins[iptbin]
			rooCat.defineType(cat)
			histpdf['%s_%s' % (proc, cat)] = r.RooHistPdf('histpdf_%s_%s' % (proc, cat),
														  'histpdf_%s_%s' % (proc, cat),
														  r.RooArgSet(wbase[cat].var('x')),
														  datahist['%s_%s' % (proc, cat)])

			hist_up = histpdf['%s_%s' % (proc, cat)].createHistogram("x")
			hist_down = histpdf['%s_%s' % (proc, cat)].createHistogram("x")

			rescaled_int_up = datahist['%s_%s' % (proc, cat)].sumEntries() * (1. + (ipt-iptlo) * (total_unc-1.) / (ipthi-iptlo)) * (all_int / all_int_rescale_Up)
			rescaled_int_down = datahist['%s_%s' % (proc, cat)].sumEntries() / (1. + (ipt-iptlo) * (total_unc-1.) / (ipthi-iptlo)) * (all_int / all_int_rescale_Down)

			hist_up.Scale(rescaled_int_up/hist_up.Integral())
			hist_down.Scale(rescaled_int_down/hist_down.Integral())

			# validation
			self._outfile_validation.cd()
			hist_up.SetName('%s_%s_%s'%(proc,cat,'hqq125ptShapeUp'))
			hist_up.Write()
			hist_down.SetName('%s_%s_%s'%(proc,cat,'hqq125ptShapeDown'))
			hist_down.Write()

			hptpdfUp_s[cat] = r.RooDataHist('%s_%s_%s'%(proc,cat,'hqq125ptShapeUp'), '%s_%s_%s'%(proc,cat,'hqq125ptShapeUp'), r.RooArgList(x), hist_up)
			hptpdfDown_s[cat] = r.RooDataHist('%s_%s_%s'%(proc,cat,'hqq125ptShapeDown'), '%s_%s_%s'%(proc,cat,'hqq125ptShapeDown'), r.RooArgList(x), hist_down)

			getattr(wbase[cat], 'import')(hptpdfUp_s[cat], r.RooFit.RecycleConflictNodes())
			getattr(wbase[cat], 'import')(hptpdfDown_s[cat], r.RooFit.RecycleConflictNodes())

		up = 0
		down = 0
		nom = 0
		for cat in categories:
			nom  += datahist['%s_%s' % (proc, cat)].sumEntries()
			up += hptpdfUp_s[cat].sumEntries()
			down += hptpdfDown_s[cat].sumEntries()
			if not self._quiet:
				print cat, datahist['%s_%s' % (proc, cat)].sumEntries()
				print cat, hptpdfUp_s[cat].sumEntries()
				print cat, hptpdfDown_s[cat].sumEntries()
		if not self._quiet:
			print "total", nom
			print "total", up
			print "total", down
		
		icat = 0
		for cat in categories:
			if icat == 0:
				wbase[cat].writeToFile(self._output_path, True)
			else:
				wbase[cat].writeToFile(self._output_path, False)
			icat += 1

	def prefit(self, fix_pars={}, fix_pars_rhalphabet={}, category_indices=None):
		print "\n\n*** PREFIT ***"
		fbase = r.TFile.Open(self._output_path, 'update')
		fbase.ls()
		fralphabase = r.TFile.Open(self._rhalphabet_output_path, 'update')
		fralphabase.ls()
		categories = []
		for cat in category_indices:
			categories.append("pass_cat{}".format(cat))
			categories.append("fail_cat{}".format(cat))
		#categories = ['pass_cat1', 'pass_cat2', 'pass_cat3', 'pass_cat4', 'pass_cat5', 'pass_cat6','fail_cat1', 'fail_cat2', 'fail_cat3', 'fail_cat4', 'fail_cat5', 'fail_cat6']

		wbase = {}
		wralphabase = {}
		for cat in categories:
			wbase[cat] = fbase.Get('w_%s' % cat)
			wralphabase[cat] = fralphabase.Get('w_%s' % cat)
			for parname, parval in fix_pars.iteritems():
				if wbase[cat].var(parname):
					wbase[cat].var(parname).setVal(parval)
					wbase[cat].var(parname).setConstant(True)
				else:
					print "[rhalphabet_builder::prefit] WARNING : parameter {} doesn't exist, ignoring".format(parname)

			for parname, parval in fix_pars_rhalphabet.iteritems():
				if wralphabase[cat].var(parname):
					wralphabase[cat].var(parname).setVal(parval)
					wralphabase[cat].var(parname).setConstant(True)
				else:
					print "[rhalphabet_builder::prefit] WARNING : parameter {} doesn't exist, ignoring".format(parname)

		w = r.RooWorkspace('w')
		w.factory('mu[1.,0.,20.]')
		x = wbase[categories[0]].var('x')
		rooCat = r.RooCategory('cat', 'cat')

		mu = w.var('mu')
		epdf_b = {}
		epdf_s = {}
		datahist = {}
		histpdf = {}
		histpdfnorm = {}
		data = {}
		signorm = {}
		for cat in categories:
			rooCat.defineType(cat)

		for cat in categories:
			norms_b = r.RooArgList()
			norms_s = r.RooArgList()
			norms_b.add(wralphabase[cat].function('qcd_%s_norm' % cat))
			norms_s.add(wralphabase[cat].function('qcd_%s_norm' % cat))
			pdfs_b = r.RooArgList()
			pdfs_s = r.RooArgList()
			pdfs_b.add(wralphabase[cat].pdf('qcd_%s' % cat))
			pdfs_s.add(wralphabase[cat].pdf('qcd_%s' % cat))

			if not wbase[cat]:
				print "ERROR : wbase[{}] doesn't exist! Printing file...".format(cat)
				fbase.ls()
			data[cat] = wbase[cat].data('data_obs_%s' % cat)
			for proc in (self._background_names + self._signal_names):
				if proc == 'qcd': continue

				datahist['%s_%s' % (proc, cat)] = wbase[cat].data('%s_%s' % (proc, cat))
				if not datahist['%s_%s' % (proc, cat)]:
					print "ERROR : Couldn't load data {}_{} from workspace {} in file {}".format(proc, cat, "w_"+cat, fbase.GetPath())
					sys.exit(1)
				histpdf['%s_%s' % (proc, cat)] = r.RooHistPdf('histpdf_%s_%s' % (proc, cat),
															  'histpdf_%s_%s' % (proc, cat),
															  r.RooArgSet(wbase[cat].var('x')),
															  datahist['%s_%s' % (proc, cat)])
				getattr(w, 'import')(datahist['%s_%s' % (proc, cat)], r.RooFit.RecycleConflictNodes())
				getattr(w, 'import')(histpdf['%s_%s' % (proc, cat)], r.RooFit.RecycleConflictNodes())
				if proc in self._signal_names:
					# signal
					signorm['%s_%s' % (proc, cat)] = r.RooRealVar('signorm_%s_%s' % (proc, cat),
																  'signorm_%s_%s' % (proc, cat),
																  datahist['%s_%s' % (proc, cat)].sumEntries(),
																  0, 10. * datahist['%s_%s' % (proc, cat)].sumEntries())
					signorm['%s_%s' % (proc, cat)].setConstant(True)
					getattr(w, 'import')(signorm['%s_%s' % (proc, cat)], r.RooFit.RecycleConflictNodes())
					histpdfnorm['%s_%s' % (proc, cat)] = r.RooFormulaVar('histpdfnorm_%s_%s' % (proc, cat),
																		 '@0*@1', r.RooArgList(mu, signorm[
							'%s_%s' % (proc, cat)]))
					pdfs_s.add(histpdf['%s_%s' % (proc, cat)])
					norms_s.add(histpdfnorm['%s_%s' % (proc, cat)])
				else:
					# background
					histpdfnorm['%s_%s' % (proc, cat)] = r.RooRealVar('histpdfnorm_%s_%s' % (proc, cat),
																	  'histpdfnorm_%s_%s' % (proc, cat),
																	  datahist['%s_%s' % (proc, cat)].sumEntries(),
																	  0, 10. * datahist[
																		  '%s_%s' % (proc, cat)].sumEntries())
					histpdfnorm['%s_%s' % (proc, cat)].setConstant(True)
					getattr(w, 'import')(histpdfnorm['%s_%s' % (proc, cat)], r.RooFit.RecycleConflictNodes())
					pdfs_b.add(histpdf['%s_%s' % (proc, cat)])
					pdfs_s.add(histpdf['%s_%s' % (proc, cat)])
					norms_b.add(histpdfnorm['%s_%s' % (proc, cat)])
					norms_s.add(histpdfnorm['%s_%s' % (proc, cat)])

			epdf_b[cat] = r.RooAddPdf('epdf_b_' + cat, 'epdf_b_' + cat, pdfs_b, norms_b)
			epdf_s[cat] = r.RooAddPdf('epdf_s_' + cat, 'epdf_s_' + cat, pdfs_s, norms_s)

			getattr(w, 'import')(epdf_b[cat], r.RooFit.RecycleConflictNodes())
			getattr(w, 'import')(epdf_s[cat], r.RooFit.RecycleConflictNodes())

		## arguments = ["data_obs","data_obs",r.RooArgList(x),rooCat]

		## m = r.std.map('string, RooDataHist*')()
		## for cat in categories:
		##    m.insert(r.std.pair('string, RooDataHist*')(cat, data[cat]))
		## arguments.append(m)

		## combData = getattr(r,'RooDataHist')(*arguments)

		cat = categories[0]
		args = data[cat].get(0)

		combiner = r.CombDataSetFactory(args, rooCat)

		for cat in categories:
			combiner.addSetBin(cat, data[cat])
		combData = combiner.done('data_obs', 'data_obs')

		simPdf_b = r.RooSimultaneous('simPdf_b', 'simPdf_b', rooCat)
		simPdf_s = r.RooSimultaneous('simPdf_s', 'simPdf_s', rooCat)
		for cat in categories:
			simPdf_b.addPdf(epdf_b[cat], cat)
			simPdf_s.addPdf(epdf_s[cat], cat)

		mu.setVal(1.)

		getattr(w, 'import')(simPdf_b, r.RooFit.RecycleConflictNodes())
		getattr(w, 'import')(simPdf_s, r.RooFit.RecycleConflictNodes())
		getattr(w, 'import')(combData, r.RooFit.RecycleConflictNodes())

		if not self._quiet:
			w.Print('v')
		simPdf_b = w.pdf('simPdf_b')
		simPdf_s = w.pdf('simPdf_s')
		combData = w.data('data_obs')
		x = w.var('x')
		rooCat = w.cat('cat')
		mu = w.var('mu')
		CMS_set = r.RooArgSet()
		CMS_set.add(rooCat)
		CMS_set.add(x)

		opt = r.RooLinkedList()
		opt.Add(r.RooFit.CloneData(False))
		allParams = simPdf_b.getParameters(combData)
		r.RooStats.RemoveConstantParameters(allParams)
		opt.Add(r.RooFit.Constrain(allParams))

		mu.setVal(0.)
		mu.setConstant(True)

		nll = simPdf_s.createNLL(combData)
		m2 = r.RooMinimizer(nll)
		m2.setStrategy(2)
		m2.setMaxFunctionCalls(100000)
		m2.setMaxIterations(100000)
		m2.setPrintLevel(-1)
		m2.setPrintEvalErrors(-1)
		m2.setEps(1e-5)
		m2.optimizeConst(2)

		migrad_status = m2.minimize('Minuit2', 'migrad')
		improve_status = m2.minimize('Minuit2', 'improve')
		hesse_status = m2.minimize('Minuit2', 'hesse')
		fr = m2.save()
		if not self._quiet:
			fr.Print('v')

		icat = 0
		for cat in categories:
			for parname, parval in fix_pars.iteritems():
				if wbase[cat].var(parname):
					wbase[cat].var(parname).setConstant(False)
			for parname, parval in fix_pars_rhalphabet.iteritems():
				if wralphabase[cat].var(parname):
					wralphabase[cat].var(parname).setConstant(False)
			reset(wralphabase[cat], fr)
			if icat == 0:
				getattr(wralphabase[cat], 'import')(fr)
				wralphabase[cat].writeToFile(self._rhalphabet_output_path, True)
			else:
				wralphabase[cat].writeToFile(self._rhalphabet_output_path, False)
			icat += 1

	def loadfit(self, fitToLoad):

		fralphabase_load = r.TFile.Open(fitToLoad, 'read')
		fr = fralphabase_load.Get('w_pass_cat1').obj('nll_simPdf_s_data_obs')

		fbase = r.TFile.Open(self._output_path, 'update')
		fralphabase = r.TFile.Open(self._rhalphabet_output_path, 'update')

		categories = ['pass_cat1', 'pass_cat2', 'pass_cat3', 'pass_cat4', 'pass_cat5', 'pass_cat6',
					  'fail_cat1', 'fail_cat2', 'fail_cat3', 'fail_cat4', 'fail_cat5', 'fail_cat6']

		wbase = {}
		wralphabase = {}
		for cat in categories:
			wbase[cat] = fbase.Get('w_%s' % cat)
			wralphabase[cat] = fralphabase.Get('w_%s' % cat)

		icat = 0
		for cat in categories:
			reset(wralphabase[cat], fr, exclude='qcd_fail_cat')
			if icat == 0:
				wralphabase[cat].writeToFile(self._rhalphabet_output_path, True)
			else:
				wralphabase[cat].writeToFile(self._rhalphabet_output_path, False)
			icat += 1

	def LoopOverPtBins(self):
		print "number of pt bins = ", self._nptbins;
		for pt_bin in range(1, self._nptbins + 1):
			# for pt_bin in range(1,2):
			print "------- pT bin number ", pt_bin

			# 1d histograms in each pT bin (in the order... data, w, z, qcd, top, signals)
			pass_hists_ptbin = {}
			fail_hists_ptbin = {}
			for process in self._processes:
				pass_hists_ptbin[process] = tools.proj("cat", str(pt_bin), self._pass_hists[process], self._mass_nbins, self._mass_lo,
													self._mass_hi)
				fail_hists_ptbin[process] = tools.proj("cat", str(pt_bin), self._fail_hists[process], self._mass_nbins, self._mass_lo,
													self._mass_hi)

			# make RooDataset, RooPdfs, and histograms
			# GetWorkspaceInputs returns: RooDataHist (data), then RooHistPdf of each electroweak
			(data_pass_rdh, data_fail_rdh, pass_rhps, fail_rhps) = self.GetWorkspaceInputs(pass_hists_ptbin, fail_hists_ptbin, "cat" + str(pt_bin))
			# Get approximate pt bin value
			this_pt = self._pass_hists["data_obs"].GetYaxis().GetBinLowEdge(pt_bin) + self._pass_hists["data_obs"].GetYaxis().GetBinWidth(pt_bin) * 0.3;
			print "------- this bin pT value ", this_pt

			# Make the rhalphabet fit for this pt bin
			(rhalphabet_hist_pass, rhalphabet_hist_fail) = self.MakeRhalphabet(["data_obs", "wqq", "zqq", "tqq", "hqq125","tthqq125","vbfhqq125","whqq125","zhqq125"], pass_hists_ptbin, fail_hists_ptbin, this_pt, "cat" + str(pt_bin))

			# Get signals
			(signal_rdhs_pass, signal_rdhs_fail) = self.GetSignalInputs(pass_hists_ptbin, fail_hists_ptbin, "cat" + str(pt_bin))
			pass_rhps.update(signal_rdhs_pass)
			fail_rhps.update(signal_rdhs_fail)

			# Systematics
			# - Get the pt slice for each systematic histogram
			# - For mcstat, make the bin-by-bin "uncorrelated" copies
			pass_rdhs_syst = {}
			fail_rdhs_syst = {}
			for process in self._processes:
				pass_rdhs_syst[process] = {}
				fail_rdhs_syst[process] = {}
				for syst in self._systematics:
					if not process in self._pass_hists_syst[syst + "Up"]:
						continue
					tmph_pass_up   = tools.proj('cat', str(pt_bin), self._pass_hists_syst[syst + "Up"][process], self._mass_nbins, self._mass_lo,self._mass_hi)
					tmph_pass_down = tools.proj('cat', str(pt_bin), self._pass_hists_syst[syst + "Down"][process], self._mass_nbins, self._mass_lo,self._mass_hi)
					tmph_fail_up   = tools.proj('cat', str(pt_bin), self._fail_hists_syst[syst + "Up"][process], self._mass_nbins, self._mass_lo,self._mass_hi)
					tmph_fail_down = tools.proj('cat', str(pt_bin), self._fail_hists_syst[syst + "Down"][process], self._mass_nbins, self._mass_lo,self._mass_hi)
					if syst == "mcstat":
						tmph_pass_central = tools.proj('cat', str(pt_bin), self._pass_hists[process], self._mass_nbins, self._mass_lo, self._mass_hi)
						pass_name_base = "{}_pass_cat{}_{}cat{}".format(process, pt_bin, process, pt_bin)
						pass_hists_mcstat_uncorr = {"{}_pass_cat{}".format(process, pt_bin):tmph_pass_central, pass_name_base + "mcstatUp":tmph_pass_up, pass_name_base + "mcstatDown":tmph_pass_down}
						uncorrelate(pass_hists_mcstat_uncorr, "{}cat{}mcstat".format(process, pt_bin))
						#print pass_hists_mcstat_uncorr
						del pass_hists_mcstat_uncorr["{}_pass_cat{}".format(process, pt_bin)]

						tmph_fail_central = tools.proj('cat', str(pt_bin), self._fail_hists[process], self._mass_nbins, self._mass_lo, self._mass_hi)
						fail_name_base = "{}_fail_cat{}_{}cat{}".format(process, pt_bin, process, pt_bin)
						fail_hists_mcstat_uncorr = {"{}_fail_cat{}".format(process, pt_bin):tmph_fail_central, fail_name_base + "mcstatUp":tmph_fail_up, fail_name_base + "mcstatDown":tmph_fail_down}
						uncorrelate(fail_hists_mcstat_uncorr, "mcstat")
						del fail_hists_mcstat_uncorr["{}_fail_cat{}".format(process, pt_bin)]

						for key, pass_hist_mcstat in pass_hists_mcstat_uncorr.iteritems():
							pass_rdhs_syst[process][key] = r.RooDataHist(pass_hist_mcstat.GetName(), pass_hist_mcstat.GetName(), r.RooArgList(self._lMSD), pass_hist_mcstat)
						for key, fail_hist_mcstat in fail_hists_mcstat_uncorr.iteritems():
							fail_rdhs_syst[process][key] = r.RooDataHist(fail_hist_mcstat.GetName(), fail_hist_mcstat.GetName(), r.RooArgList(self._lMSD), fail_hist_mcstat)
					else:
						pass_rdhs_syst[process][syst + "Up"] = r.RooDataHist("{}_pass_cat{}_{}Up".format(process, pt_bin, syst), tmph_pass_up.GetName(), r.RooArgList(self._lMSD), tmph_pass_up)
						pass_rdhs_syst[process][syst + "Down"] = r.RooDataHist("{}_pass_cat{}_{}Down".format(process, pt_bin, syst), tmph_pass_down.GetName(), r.RooArgList(self._lMSD), tmph_pass_down)
						fail_rdhs_syst[process][syst + "Up"] = r.RooDataHist("{}_fail_cat{}_{}Up".format(process, pt_bin, syst), tmph_fail_up.GetName(), r.RooArgList(self._lMSD), tmph_fail_up)
						fail_rdhs_syst[process][syst + "Down"] = r.RooDataHist("{}_fail_cat{}_{}Down".format(process, pt_bin, syst), tmph_fail_down.GetName(), r.RooArgList(self._lMSD), tmph_fail_down)

			# #Write to file
			if not self._quiet:
				print "pass_rhps = "
				print pass_rhps
			pass_workspace_objects = [data_pass_rdh] + pass_rhps.values()
			for process in self._processes:
				for syst_dir, rdh in pass_rdhs_syst[process].iteritems():
					pass_workspace_objects.append(rdh)
			self.MakeWorkspace(self._output_path, pass_workspace_objects, "pass_cat" + str(pt_bin), True,
							   True, this_pt)
			fail_workspace_objects = [data_fail_rdh] + fail_rhps.values()
			for process in self._processes:
				for syst_dir, rdh in fail_rdhs_syst[process].iteritems():
					fail_workspace_objects.append(rdh)
			self.MakeWorkspace(self._output_path, fail_workspace_objects, "fail_cat" + str(pt_bin), True,
							   True, this_pt)

		if not self._quiet:
			for pt_bin in range(1, self._nptbins + 1):
				for mass_bin in range(1, self._mass_nbins + 1):
					print "qcd_fail_cat%i_Bin%i flatParam" % (pt_bin, mass_bin)

	# iHs = dict of fail histograms
	def MakeRhalphabet(self, samples, pass_histograms, fail_histograms, pt, category):
		print "---- [MakeRhalphabet]"

		rhalph_bkgd_name = "qcd";
		lUnity = r.RooConstVar("unity", "unity", 1.)
		lZero = r.RooConstVar("lZero", "lZero", 0.)

		# Fix the pt (top) and the qcd eff
		self._lPt.setVal(pt)
		self._lEffQCD.setConstant(False)

		polynomial_variables = self.buildPolynomialArray(self._poly_degree_pt, self._poly_degree_rho, "p", "r", -30, 30)
		if not self._quiet:
			print "polynomial_variables=",
			print polynomial_variables

		for n_rho, d1 in polynomial_variables.iteritems():
			for n_pt, poly_var in d1.iteritems():
				poly_var.setVal(1. / (self._poly_degree_rho * self._poly_degree_pt))

		# Now build the function
		pass_bins = r.RooArgList()
		fail_bins = r.RooArgList()

		for mass_bin in range(1, self._mass_nbins + 1):
			self._lMSD.setVal(fail_histograms["data_obs"].GetXaxis().GetBinCenter(mass_bin))
			if self._mass_fit:
				if not self._quiet:
					print ("Pt/mass poly")
				roopolyarray = self.buildRooPolyArray(self._lPt.getVal(), self._lMSD.getVal(), lUnity, lZero,
													  polynomial_variables)
			else:
				if not self._quiet:
					print ("Pt/Rho poly")
				roopolyarray = self.buildRooPolyRhoArrayBernstein(self._lPt.getVal(), self._lRho.getVal(), lUnity, lZero, polynomial_variables)
			if not self._quiet:
				print "RooPolyArray:"
				roopolyarray.Print()
			fail_bin_content = 0
			for sample in samples:
				if sample == "data_obs":
					if not self._quiet:
						print sample, fail_histograms[sample].GetName(), "add data"
					print "\t+={}".format(fail_histograms[sample].GetBinContent(mass_bin))
					fail_bin_content += fail_histograms[sample].GetBinContent(mass_bin)  # add data
				else:
					if not self._quiet:
						print sample, fail_histograms[sample].GetName(), "subtract W/Z/ttbar"
						print "\t-={}".format(fail_histograms[sample].GetBinContent(mass_bin))
					fail_bin_content -= fail_histograms[sample].GetBinContent(mass_bin)  # subtract W/Z/ttbar from data
			if fail_bin_content < 0: fail_bin_content = 0.

			if not self._quiet:
				print rhalph_bkgd_name + "_fail_" + category + "_Bin" + str(mass_bin), fail_bin_content

			# 50 sigma range + 10 events
			fail_bin_unc = math.sqrt(fail_bin_content) * 50. + 10.
			# Define the failing category
			fail_bin_var = r.RooRealVar(rhalph_bkgd_name + "_fail_" + category + "_Bin" + str(mass_bin),
										rhalph_bkgd_name + "_fail_" + category + "_Bin" + str(mass_bin),
										fail_bin_content, 0., max(fail_bin_content + fail_bin_unc, 0.))

			if not self._quiet:
				print "[david debug] fail_bin_var:"
				fail_bin_var.Print()

			# Now define the passing cateogry based on the failing (make sure it can't go negative)
			lArg = r.RooArgList(fail_bin_var, roopolyarray, self._lEffQCD)
			pass_bin_var = r.RooFormulaVar(rhalph_bkgd_name + "_pass_" + category + "_Bin" + str(mass_bin),
										   rhalph_bkgd_name + "_pass_" + category + "_Bin" + str(mass_bin),
										   "@0*max(@1,0.000001)*@2", lArg)
			if not self._quiet:
				print "Pass=fail*poly*eff RooFormulaVar:"
				print pass_bin_var.Print()
				print pass_bin_var.GetName()

			# If the number of events in the failing is small remove the bin from being free in the fit
			#if fail_bin_content < 4:
			#    print "too small number of events", fail_bin_content, "Bin", str(mass_bin)
			#    fail_bin_var.setConstant(True)
			#    pass_bin_var = r.RooRealVar(rhalph_bkgd_name + "_pass_" + category + "_Bin" + str(mass_bin),
			#                                rhalph_bkgd_name + "_pass_" + category + "_Bin" + str(mass_bin), 0, 0, 0)
			#    pass_bin_var.setConstant(True)
			if fail_bin_content == 0:
				print "[MakeRhalphabet] WARNING : ZEROFAIL Fail data = " + str(fail_bin_content) + " in bin " + str(mass_bin) + ". Setting fail, pass, and data to zero."
				fail_bin_var.setConstant(True)
				pass_bin_var = r.RooRealVar(rhalph_bkgd_name + "_pass_" + category + "_Bin" + str(mass_bin),
											rhalph_bkgd_name + "_pass_" + category + "_Bin" + str(mass_bin), 0, 0, 0)
				pass_bin_var.setConstant(True)
				pass_histograms["data_obs"].SetBinContent(mass_bin, 0.)
				pass_histograms["data_obs"].SetBinError(mass_bin, 0.)

			# Add bins to the array
			pass_bins.add(pass_bin_var)
			fail_bins.add(fail_bin_var)
			self._all_vars.extend([pass_bin_var, fail_bin_var])
			self._all_pars.extend([pass_bin_var, fail_bin_var])
			# print  fail_bin_var.GetName(),"flatParam",lPass#,lPass+"/("+lFail+")*@0"

		# print "Printing pass_bins:"
		# for i in xrange(pass_bins.getSize()):
		#    pass_bins[i].Print()
		pass_rparh = r.RooParametricHist(rhalph_bkgd_name + "_pass_" + category, rhalph_bkgd_name + "_pass_" + category,
										 self._lMSD, pass_bins, fail_histograms["data_obs"])
		fail_rparh = r.RooParametricHist(rhalph_bkgd_name + "_fail_" + category, rhalph_bkgd_name + "_fail_" + category,
										 self._lMSD, fail_bins, fail_histograms["data_obs"])
		if not self._quiet:
			print "Print pass and fail RooParametricHists"
			pass_rparh.Print()
			fail_rparh.Print()
		pass_norm = r.RooAddition(rhalph_bkgd_name + "_pass_" + category + "_norm",
								  rhalph_bkgd_name + "_pass_" + category + "_norm", pass_bins)
		fail_norm = r.RooAddition(rhalph_bkgd_name + "_fail_" + category + "_norm",
								  rhalph_bkgd_name + "_fail_" + category + "_norm", fail_bins)
		if not self._quiet:
			print "Printing NPass and NFail variables:"
			pass_norm.Print()
			fail_norm.Print()
		self._all_shapes.extend([pass_rparh, fail_rparh, pass_norm, fail_norm])

		# Now write the wrokspace with the rooparamhist
		pass_workspace = r.RooWorkspace("w_pass_" + str(category))
		fail_workspace = r.RooWorkspace("w_fail_" + str(category))
		getattr(pass_workspace, 'import')(pass_rparh, r.RooFit.RecycleConflictNodes())
		getattr(pass_workspace, 'import')(pass_norm, r.RooFit.RecycleConflictNodes())
		getattr(fail_workspace, 'import')(fail_rparh, r.RooFit.RecycleConflictNodes())
		getattr(fail_workspace, 'import')(fail_norm, r.RooFit.RecycleConflictNodes())
		if not self._quiet:
			print "Printing rhalphabet workspace:"
			pass_workspace.Print()
		if category.find("1") > -1:
			pass_workspace.writeToFile(self._rhalphabet_output_path)
		else:
			pass_workspace.writeToFile(self._rhalphabet_output_path, False)
		fail_workspace.writeToFile(self._rhalphabet_output_path, False)
		return [pass_rparh, fail_rparh]

	def buildRooPolyArray(self, iPt, iMass, iQCD, iZero, iVars):

		# print "---- [buildRooPolyArray]"  
		# print len(iVars);

		lPt = r.RooConstVar("Var_Pt_" + str(iPt) + "_" + str(iMass), "Var_Pt_" + str(iPt) + "_" + str(iMass), (iPt))
		lMass = r.RooConstVar("Var_Mass_" + str(iPt) + "_" + str(iMass), "Var_Mass_" + str(iPt) + "_" + str(iMass),
							  (iMass))
		lMassArray = r.RooArgList()
		for i_rho in range(0, self._poly_degree_rho + 1):
			lTmpArray = r.RooArgList()
			for i_pt in range(0, self._poly_degree_pt + 1):
				if i_rho == 0 and i_pt == 0:
					lTmpArray.add(iQCD)  # for the very first constant (e.g. p0r0), just set that to 1
				else:
					lTmpArray.add(iVars[i_pt][i_rho])
			pLabel = "Var_Pol_Bin_" + str(round(iPt, 2)) + "_" + str(round(iMass, 3)) + "_" + str(i_rho)
			pPol = r.RooPolyVar(pLabel, pLabel, lPt, lTmpArray)
			lMassArray.add(pPol)
			self._all_vars.append(pPol)

		lLabel = "Var_MassPol_Bin_" + str(round(iPt, 2)) + "_" + str(round(iMass, 3))
		lMassPol = r.RooPolyVar(lLabel, lLabel, lMass, lMassArray)
		self._all_vars.extend([lPt, lMass, lMassPol])
		return lMassPol

	def buildRooPolyRhoArray(self, iPt, iRho, iQCD, iZero, iVars):

		# print "---- [buildRooPolyArray]"      

		lPt = r.RooConstVar("Var_Pt_" + str(iPt) + "_" + str(iRho), "Var_Pt_" + str(iPt) + "_" + str(iRho), (iPt))
		lRho = r.RooConstVar("Var_Rho_" + str(iPt) + "_" + str(iRho), "Var_Rho_" + str(iPt) + "_" + str(iRho), (iRho))
		lRhoArray = r.RooArgList()
		for i_rho in range(0, self._poly_degree_rho + 1):
			lTmpArray = r.RooArgList()
			for i_pt in range(0, self._poly_degree_pt + 1):
				if i_rho == 0 and i_pt == 0:
					lTmpArray.add(iQCD);  # for the very first constant (e.g. p0r0), just set that to 1
				else:
					lTmpArray.add(iVars[i_pt][i_rho])
			pLabel = "Var_Pol_Bin_" + str(round(iPt, 2)) + "_" + str(round(iRho, 3)) + "_" + str(i_rho)
			pPol = r.RooPolyVar(pLabel, pLabel, lPt, lTmpArray)
			#print "pPol:"
			#print pPol.Print()
			lRhoArray.add(pPol);
			self._all_vars.append(pPol)

		lLabel = "Var_RhoPol_Bin_" + str(round(iPt, 2)) + "_" + str(round(iRho, 3))
		lRhoPol = r.RooPolyVar(lLabel, lLabel, lRho, lRhoArray)
		self._all_vars.extend([lPt, lRho, lRhoPol])
		return lRhoPol

	def generate_bernstein_string(self, n):
		# x = @(n+1)
		monomials = []
		for v in xrange(0, n+1):
			# Normalization constant = n choose v
			normalization = 1. * math.factorial(n) / (math.factorial(v) * math.factorial(n - v))
			monomials.append("({} * @{} * @{}**{} * (1.-@{})**{})".format(normalization, v, n+1, v, n+1, n-v))
		return " + ".join(monomials)

	def buildRooPolyRhoArrayBernstein(self, iPt, iRho, iQCD, iZero, iVars):
		#print "---- [buildRooPolyArrayBernstein]"
		lPt = r.RooConstVar("Var_Pt_" + str(iPt) + "_" + str(iRho), "Var_Pt_" + str(iPt) + "_" + str(iRho), (iPt))
		lPt_rescaled = r.RooConstVar("Var_Pt_rescaled_" + str(iPt) + "_" + str(iRho),
									 "Var_Pt_rescaled_" + str(iPt) + "_" + str(iRho),
									 ((iPt - self._pt_lo) / (self._pt_hi - self._pt_lo)))
		lRho = r.RooConstVar("Var_Rho_" + str(iPt) + "_" + str(iRho), "Var_Rho_" + str(iPt) + "_" + str(iRho), (iRho))
		lRho_rescaled = r.RooConstVar("Var_Rho_rescaled_" + str(round(iPt, 2)) + "_" + str(round(iRho, 3)),
									  "Var_Rho_rescaled_" + str(round(iPt, 2)) + "_" + str(round(iRho, 3)),
									  ((iRho - self._rho_lo) / (self._rho_hi - self._rho_lo)))

		ptPolyString = self.generate_bernstein_string(self._poly_degree_pt)
		rhoPolyString = self.generate_bernstein_string(self._poly_degree_rho)

		lRhoArray = r.RooArgList()
		lNCount = 0
		for i_rho in range(0, self._poly_degree_rho + 1):
			lTmpArray = r.RooArgList()
			for i_pt in range(0, self._poly_degree_pt + 1):
				if i_rho == 0 and i_pt == 0:
					lTmpArray.add(iQCD)  # for the very first constant (e.g. p0r0), just set that to 1
				else:
					lTmpArray.add(iVars[i_pt][i_rho])
			pLabel = "Var_Pol_Bin_" + str(round(iPt, 2)) + "_" + str(round(iRho, 3)) + "_" + str(i_rho)
			lTmpArray.add(lPt_rescaled)
			#print "lTmpArray: ", lTmpArray.Print()
			pPol = r.RooFormulaVar(pLabel, pLabel, ptPolyString, lTmpArray)
			#print "pPol:"
			#print pPol.Print("V")
			lRhoArray.add(pPol)
			self._all_vars.append(pPol)

		lLabel = "Var_RhoPol_Bin_" + str(round(iPt, 2)) + "_" + str(round(iRho, 3))
		lRhoArray.add(lRho_rescaled)
		print "lRhoArray: ", lRhoArray.Print()
		lRhoPol = r.RooFormulaVar(lLabel, lLabel, rhoPolyString, lRhoArray)
		self._all_vars.extend([lPt_rescaled, lRho_rescaled, lRhoPol])
		return lRhoPol

	# iNVar0  = max degree of first variable
	# iNVar1  = max degree of second variable
	# iLabel0 = name prefix of first variable
	# iLabel1 = name prefix of second variable
	# iXMin0  = minimum value of coefficients
	# iXMax0  = maximum value of coefficients
	def buildPolynomialArray(self, iNVar0, iNVar1, iLabel0, iLabel1, iXMin0, iXMax0):

		print "---- [buildPolynomialArray]"
		## form of polynomial
		## (p0r0 + p1r0 * pT + p2r0 * pT^2 + ...) + 
		## (p0r1 + p1r1 * pT + p2r1 * pT^2 + ...) * rho + 
		## (p0r2 + p1r2 * pT + p2r2 * pT^2 + ...) * rho^2 + ...
		'''
		r0p0    =    0, pXMin,pXMax
		r1p0    =   -3.7215e-03 +/-  1.71e-08
		r2p0    =    2.4063e-06 +/-  2.76e-11
			r0p1    =   -2.1088e-01 +/-  2.72e-06I  
			r1p1    =    3.6847e-05 +/-  4.66e-09
			r2p1    =   -3.8415e-07 +/-  7.23e-12
			r0p2    =   -8.5276e-02 +/-  6.90e-07
			r1p2    =    2.2058e-04 +/-  1.10e-09
			r2p2    =   -2.2425e-07 +/-  1.64e-12
		'''
		value = [0.,
				 -3.7215e-03,
				 2.4063e-06,
				 -2.1088e-01,
				 3.6847e-05,
				 -3.8415e-07,
				 -8.5276e-02,
				 2.2058e-04,
				 -2.2425e-07]
		error = [iXMax0,
				 1.71e-08,
				 2.76e-11,
				 2.72e-06,
				 4.66e-09,
				 7.23e-12,
				 6.90e-07,
				 1.10e-09,
				 1.64e-12]
		ret_vars = {}
		for i0 in range(iNVar0 + 1):
			ret_vars[i0] = {}
			for i1 in range(iNVar1 + 1):
				pVar = iLabel1 + str(i1) + iLabel0 + str(i0);
				if self._freeze:

					start = value[i0 * 3 + i1]
					pXMin = value[i0 * 3 + i1] - error[i0 * 3 + i1]
					pXMax = value[i0 * 3 + i1] + error[i0 * 3 + i1]

				else:
					start = 0.0
					pXMin = iXMin0
					pXMax = iXMax0

				ret_vars[i0][i1] = r.RooRealVar(pVar, pVar, 0.0, pXMin, pXMax)
				# print("========  here i0 %s i1 %s"%(i0,i1))
				if not self._quiet:
					print pVar
				# print(" is : %s  +/- %s"%(value[i0*3+i1],error[i0*3+i1]))
				self._all_vars.append(ret_vars[i0][i1])
		return ret_vars

	def GetWorkspaceInputs(self, pass_histograms, fail_histograms,iBin):
		# Protect against zero norm?
		for background in ["wqq", "zqq", "tqq", "hqq125","tthqq125","vbfhqq125","whqq125","zhqq125"]:
			if pass_histograms[background].Integral() == 0:
				print "[GetWorkspaceInputs] WARNING : Zero norm for histogram {}. Filling with (500, 1.e-10).".format(pass_histograms[background].GetName())
				pass_histograms[background].Fill(500., 1.e-10)
			if fail_histograms[background].Integral() == 0:
				print "[GetWorkspaceInputs] WARNING : Zero norm for histogram {}. Filling with (500, 1.e-10).".format(fail_histograms[background].GetName())
				fail_histograms[background].Fill(500., 1.e-10)

		roocategories = r.RooCategory("sample","sample") 
		roocategories.defineType("pass",1) 
		roocategories.defineType("fail",0) 
		data_rdh_pass = r.RooDataHist("data_obs_pass_"+iBin,"data_obs_pass_"+iBin,r.RooArgList(self._lMSD), pass_histograms["data_obs"])
		data_rdh_fail = r.RooDataHist("data_obs_fail_"+iBin,"data_obs_fail_"+iBin,r.RooArgList(self._lMSD), fail_histograms["data_obs"])
		data_rdh_comb  = r.RooDataHist("comb_data_obs","comb_data_obs",r.RooArgList(self._lMSD),r.RooFit.Index(roocategories),r.RooFit.Import("pass",data_rdh_pass),r.RooFit.Import("fail",data_rdh_fail)) 

		roofit_shapes = {}
		for sample in ["wqq", "zqq", "qcd", "tqq", "hqq125","tthqq125","vbfhqq125","whqq125","zhqq125"]:
			roofit_shapes[sample] = self.GetRoofitHistObjects(pass_histograms[sample], fail_histograms[sample], sample,
															  iBin)

		total_pdf_pass = r.RooAddPdf("tot_pass" + iBin, "tot_pass" + iBin,
									 r.RooArgList(roofit_shapes["qcd"]["pass_epdf"]))
		total_pdf_fail = r.RooAddPdf("tot_fail" + iBin, "tot_fail" + iBin,
									 r.RooArgList(roofit_shapes["qcd"]["fail_epdf"]))
		ewk_pdf_pass = r.RooAddPdf("ewk_pass" + iBin, "ewk_pass" + iBin,
								   r.RooArgList(roofit_shapes["wqq"]["pass_epdf"], roofit_shapes["zqq"]["pass_epdf"],roofit_shapes["tqq"]["pass_epdf"], roofit_shapes["hqq125"]["pass_epdf"], roofit_shapes["tthqq125"]["pass_epdf"], roofit_shapes["vbfhqq125"]["pass_epdf"], roofit_shapes["whqq125"]["pass_epdf"], roofit_shapes["zhqq125"]["pass_epdf"]))
		ewk_pdf_fail = r.RooAddPdf("ewk_fail" + iBin, "ewk_fail" + iBin,
								   r.RooArgList(roofit_shapes["wqq"]["fail_epdf"], roofit_shapes["zqq"]["fail_epdf"],
												roofit_shapes["tqq"]["fail_epdf"], roofit_shapes["hqq125"]["fail_epdf"], roofit_shapes["tthqq125"]["fail_epdf"], roofit_shapes["vbfhqq125"]["fail_epdf"], roofit_shapes["whqq125"]["fail_epdf"], roofit_shapes["zhqq125"]["fail_epdf"]))
		total_simulpdf = r.RooSimultaneous("tot", "tot", roocategories)
		total_simulpdf.addPdf(total_pdf_pass, "pass")
		total_simulpdf.addPdf(total_pdf_fail, "fail")
		self._all_data.extend([data_rdh_pass, data_rdh_fail])
		self._all_shapes.extend([total_pdf_pass, total_pdf_fail, ewk_pdf_pass, ewk_pdf_fail])

		## find out which to make global
		## RooDataHist (data), then RooHistPdf of each electroweak
		# Previous return values 2 and 3 (RooAbsPdf (qcd,ewk)) removed by David on 19/1/2017, because they don't seem to be used. 
		return [
			data_rdh_pass,
			data_rdh_fail,
			# {"qcd":total_pdf_pass, "ewk":ewk_pdf_pass},
			# {"qcd":total_pdf_fail, "ewk":ewk_pdf_fail},
			{"wqq": roofit_shapes["wqq"]["pass_rdh"], "zqq": roofit_shapes["zqq"]["pass_rdh"],
			 "tqq": roofit_shapes["tqq"]["pass_rdh"], "hqq125":roofit_shapes["hqq125"]["pass_rdh"], "tthqq125":roofit_shapes["tthqq125"]["pass_rdh"], "vbfhqq125":roofit_shapes["vbfhqq125"]["pass_rdh"], "whqq125":roofit_shapes["whqq125"]["pass_rdh"], "zhqq125":roofit_shapes["zhqq125"]["pass_rdh"]},
			{"wqq": roofit_shapes["wqq"]["fail_rdh"], "zqq": roofit_shapes["zqq"]["fail_rdh"],
			 "tqq": roofit_shapes["tqq"]["fail_rdh"], "hqq125":roofit_shapes["hqq125"]["fail_rdh"], "tthqq125":roofit_shapes["tthqq125"]["fail_rdh"], "vbfhqq125":roofit_shapes["vbfhqq125"]["fail_rdh"], "whqq125":roofit_shapes["whqq125"]["fail_rdh"], "zhqq125":roofit_shapes["zhqq125"]["fail_rdh"]},
		]



	# Get (RooHistPdf, RooExtendPdf, RooDataHist) for a pair of pass/fail histograms
	# - The RooExtendPdfs are coupled via their normalizations, N*eff or N*(1-eff). 
	def GetRoofitHistObjects(self, hist_pass, hist_fail, label="w", category="_cat0"):
		# normalization
		total_norm = r.RooRealVar(label + "norm" + category, label + "norm" + category,
								  (hist_pass.Integral() + hist_fail.Integral()), 0.,
								  5. * (hist_pass.Integral() + hist_fail.Integral()))
		pass_norm = r.RooFormulaVar(label + "fpass" + category, label + "norm" + category + "*(veff)",
									r.RooArgList(total_norm, self._lEff))
		fail_norm = r.RooFormulaVar(label + "fqail" + category, label + "norm" + category + "*(1-veff)",
									r.RooArgList(total_norm, self._lEff))

		# shapes
		pass_rdh = r.RooDataHist(label + "_pass_" + category, label + "_pass_" + category, r.RooArgList(self._lMSD),
								 hist_pass)
		fail_rdh = r.RooDataHist(label + "_fail_" + category, label + "_fail_" + category, r.RooArgList(self._lMSD),
								 hist_fail)
		pass_rhp = r.RooHistPdf(label + "passh" + category, label + "passh" + category, r.RooArgList(self._lShift),
								r.RooArgList(self._lMSD), pass_rdh, 0)
		fail_rhp = r.RooHistPdf(label + "failh" + category, label + "failh" + category, r.RooArgList(self._lShift),
								r.RooArgList(self._lMSD), fail_rdh, 0)

		# extended likelihood from normalization and shape above
		pass_epdf = r.RooExtendPdf(label + "_passe_" + category, label + "pe" + category, pass_rhp, pass_norm)
		fail_epdf = r.RooExtendPdf(label + "_faile_" + category, label + "fe" + category, fail_rhp, fail_norm)

		# lHist   = [pass_pdf,fail_rhp,pass_epdf,fail_epdf,pass_rdh,fail_rdh]
		return_dict = {
			"pass_rdh": pass_rdh,
			"fail_rdh": fail_rdh,
			"pass_pdf": pass_rhp,
			"fail_pdf": fail_rhp,
			"pass_epdf": pass_epdf,
			"fail_epdf": fail_epdf
		}
		self._all_vars.extend([total_norm, pass_norm, fail_norm])
		self._all_shapes.extend(return_dict.values())
		return return_dict

	def GetSignalInputs(self, iHP, iHF, iBin):
		# get signals
		lPSigs = {}
		lFSigs = {}
		for signal_name in self._signal_names:
			roofit_shapes = self.GetRoofitHistObjects(iHP[signal_name], iHF[signal_name], signal_name,iBin)
			lPSigs[signal_name] = roofit_shapes["pass_rdh"]
			lFSigs[signal_name] = roofit_shapes["fail_rdh"]
		return (lPSigs, lFSigs)

	# def MakeWorkspace(self,iOutput,iDatas,iFuncs,iVars,iCat="cat0",iShift=True):
	#def MakeWorkspace(self, output_path, import_objects, category="cat0", do_shift=True, do_syst=True, pt_val=500.):
	def MakeWorkspace(self, output_path, import_objects, category="cat0", do_shift=True, do_syst=True, pt_val=500.):
		print "Making workspace " + "w_" + str(category)
		workspace = r.RooWorkspace("w_" + str(category))

		# get the pT bin
		match_ptbin = re_ptbin.search(category)
		iPt = match_ptbin.group("ptbin")
		#iPt = category[-1:]

		for import_object in import_objects:
			import_object.Print()
			process = import_object.GetName().split('_')[0]
			cat = import_object.GetName().split('_')[1]
			print "Importing {}".format(import_object.GetName())
			getattr(workspace, 'import')(import_object, r.RooFit.RecycleConflictNodes())

		if category.find("pass_cat1") == -1:
			workspace.writeToFile(output_path, False)
		else:
			workspace.writeToFile(output_path)
		workspace.Print()
		# workspace.writeToFile(output_path)   


##############################################################################
##############################################################################
#### E N D   O F   C L A S S
##############################################################################
##############################################################################


def reset(w, fr, exclude=None):
	for p in RootIterator(fr.floatParsFinal()):
		if exclude is not None and exclude in p.GetName(): continue
		if w.var(p.GetName()):
			print 'setting %s = %e +/- %e from %s' % (p.GetName(), p.getVal(), p.getError(), fr.GetName())
			w.var(p.GetName()).setVal(p.getVal())
			w.var(p.GetName()).setError(p.getError())
	return True
