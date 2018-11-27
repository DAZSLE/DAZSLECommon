import os
import sys
import ROOT

# Container class for histograms, to manage the TH*, RooDataHist, 
class RoofitHistContainer():
	def __init__(self, th1, xvar, name=None, normalization_var=None):
		if name:
			self._name = name
		else:
			self._name = th1.GetName()
		self._xvar = xvar
		self._th1 = th1
		self._rdh = ROOT.RooDataHist("{}_rdh".format(self._name), "{}_rdh".format(self._name), ROOT.RooArgList(self._xvar), self._th1)
		self._rhp = ROOT.RooHistPdf("{}_rhp".format(self._name), "{}_rhp".format(self._name), ROOT.RooArgSet(self._xvar), self._rdh)
		if normalization_var:
			self._normalization = normalization_var
		else:
			hist_integral = self._th1.Integral()
			self._normalization = ROOT.RooRealVar("{}_norm".format(self._name), "{}_norm".format(self._name), hist_integral, 0., 10. * hist_integral)
		self._epdf = ROOT.RooExtendPdf("{}_rep".format(self._name), "{}_rep".format(self._name), self._rhp, self._normalization)

	def RooDataHist(self):
		return self._rdh

	def RooHistPdf(self):
		return self._rhp

	def RooExtendPdf(self):
		return self._rep

	def NormalizationVar(self):
		return self._normalization

	def TH1(self):
		return self._th1

	def Integral(self):
		return self._th1.Integral()