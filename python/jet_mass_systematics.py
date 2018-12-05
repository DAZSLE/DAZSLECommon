import os
import sys
import math
from ROOT import RooRealVar, RooFormulaVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet


def MassScaling(hist_nominal, truth_mass):
	# Measured mean of W in data and MC
	mean_data = 82.657
	mean_data_err = 0.313
	mean_mc = 82.548
	mean_mc_err = 0.191

	# Scale factors to transform MC shape into data shape
	mass_shift = mean_data / mean_mc
	mass_shift_unc = math.sqrt((mean_data_err / mean_data) * (mean_data_err / mean_data) + (mean_mc_err / mean_mc) * (mean_mc_err / mean_mc)) * 10.  # (10 sigma shift)

	# Mass shift histogram
	shift_param = truth_mass * (1. -mass_shift)
	xvar =   RooRealVar("x", "x", hist_nominal.GetXaxis().GetXmin(), hist_nominal.GetXaxis().GetXmax())
	xvar.setBins(hist_nominal.GetNbinsX())
	dxvar = RooRealVar("dx", "dx", 0., -10., 10.)
	shiftvar = RooFormulaVar("shift", "x-dx", RooArgList(xvar, dxvar))

	datahist_shift = RooDataHist(hist_nominal.GetName()+"_rdh_shift" ,hist_nominal.GetName()+"_rdh_shift" , RooArgList(xvar), hist_nominal)
	histpdf_shift = RooHistPdf(hist_nominal.GetName() + "_rhp_shift", hist_nominal.GetName() + "_rhp_shift", RooArgList(shiftvar), RooArgList(xvar), datahist_shift)

	dxvar.setVal(shift_param)
	hist_massscale_up = histpdf_shift.createHistogram("x")
	hist_massscale_up.SetTitle(hist_nominal.GetTitle() + "_scaleUp")
	hist_massscale_up.SetName(hist_nominal.GetName() + "_scaleUp")
	hist_massscale_up.Scale(hist_nominal.Integral())

	dxvar.setVal(-1. * shift_param)
	hist_massscale_down = histpdf_shift.createHistogram("x")
	hist_massscale_down.SetTitle(hist_nominal.GetTitle() + "_scaleDown")
	hist_massscale_down.SetName(hist_nominal.GetName() + "_scaleDown")
	hist_massscale_down.Scale(hist_nominal.Integral())

	return (hist_massscale_up, hist_massscale_down)


def MassSmearing(hist_nominal):
	# Measured sigma of W in data and MC
	sigma_data = 8.701
	sigma_data_err = 0.433
	sigma_mc = 8.027
	sigma_mc_err = 0.607

	# Scale factors to transform MC shape into data shape
	res_shift = sigma_data / sigma_mc
	res_shift_unc = math.sqrt((sigma_data_err / sigma_data) * (sigma_data_err / sigma_data) + (sigma_mc_err / sigma_mc) * (sigma_mc_err / sigma_mc)) * 2.  # (2 sigma shift)

	# Mass smear histogram
	smear_param = res_shift - 1
	xvar =   RooRealVar("x", "x", hist_nominal.GetXaxis().GetXmin(), hist_nominal.GetXaxis().GetXmax())
	xvar.setBins(hist_nominal.GetNbinsX())
	dxvar = RooRealVar("dx", "dx", 0., 0., 2.)
	smearvar = RooFormulaVar("smear","(x-{})/dx+{}".format(hist_nominal.GetMean(), hist_nominal.GetMean()), RooArgList(xvar, dxvar))

	datahist_smear = RooDataHist(hist_nominal.GetName()+"_rdh_smear" ,hist_nominal.GetName()+"_rdh_smear" , RooArgList(xvar), hist_nominal)
	histpdf_smear = RooHistPdf(hist_nominal.GetName() + "_rhp_smear", hist_nominal.GetName() + "_rhp_smear", RooArgList(smearvar), RooArgList(xvar), datahist_smear)

	dxvar.setVal(1. + smear_param)
	hist_massres_up = histpdf_smear.createHistogram("x")
	hist_massres_up.SetTitle(hist_nominal.GetTitle() + "_smearUp")
	hist_massres_up.SetName(hist_nominal.GetName() + "_smearUp")
	hist_massres_up.Scale(hist_nominal.Integral())

	dxvar.setVal(1. - smear_param)
	hist_massres_down = histpdf_smear.createHistogram("x")
	hist_massres_down.SetTitle(hist_nominal.GetTitle() + "_smearDown")
	hist_massres_down.SetName(hist_nominal.GetName() + "_smearDown")
	hist_massres_down.Scale(hist_nominal.Integral())

	return (hist_massres_up, hist_massres_down)

