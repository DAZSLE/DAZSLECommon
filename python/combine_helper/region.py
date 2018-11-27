import os
import sys
import ROOT
from DAZSLE.PhiBBPlusJet.combine_helper.roofit_hist_container import RoofitHistContainer

class Region():
	def __init__(self, name):
		self._region_name = name
		self._background_names = []
		self._backgrounds = {}
		self._signal_name = None
		self._signal = None
		self._data = None
		self._xvar = None
		self._systematics_norm = {} # {syst_name : {process : unc.}}
		self._systematics_shape = {} # {syst_name : {process : [value, hist_up, hist_down]}}

	def name(self):
		return self._region_name

	def add_xvar(self, xvar):
		print "[Region::add_xvar] DEBUG : Adding xvar: ",
		print xvar
		self._xvar = xvar

	# syst_norm = {syst_name : unc. value}
	# syst_shape = {syst_name : [value, hist_up, hist_down]}
	def add_background(self, bkgd_name, hist, normalization_var=None, syst_norm={}, syst_shape={}):
		if not self._xvar:
			print "[Region::add_background] ERROR : Need to add an independent variable with add_xvar(xvar) first."
			sys.exit(1)
		if hist.Integral() == 0:
			print "[Region::add_background] WARNING : Histogram from background {}, region {} has zero norm. Ignoring.".format(bkgd_name, self._region_name)
			return
		self._background_names.append(bkgd_name)
		self._backgrounds[bkgd_name] = RoofitHistContainer(hist, self._xvar, name="{}_{}".format(bkgd_name, self._region_name), normalization_var=normalization_var)

		for syst_name, syst_value in syst_norm.iteritems():
			if not syst_name in self._systematics_norm:
				self._systematics_norm[syst_name] = {}
			self._systematics_norm[syst_name][bkgd_name] = syst_value

		for syst_name, syst_shape_hists in syst_shape.iteritems():
			if not syst_name in self._systematics_shape:
				self._systematics_shape[syst_name] = {}
			shape_hist_value = syst_shape_hists[0]
			shape_hist_up = RoofitHistContainer(syst_shape_hists[1], self._xvar, name="{}_{}_{}".format(bkgd_name, self._region_name, syst_name))
			shape_hist_down = RoofitHistContainer(syst_shape_hists[2], self._xvar, name="{}_{}_{}".format(bkgd_name, self._region_name, syst_name))
			self._systematics_shape[syst_name][bkgd_name] = (shape_hist_value, shape_hist_up, shape_hist_down)


	def add_signal(self, signal_name, hist, normalization_var=None, syst_norm={}, syst_shape={}):
		if not self._xvar:
			print "[Region::add_signal] ERROR : Need to add an independent variable with add_xvar(xvar) first."
			sys.exit(1)
		self._signal_name = signal_name
		self._signal = RoofitHistContainer(hist, self._xvar, name="{}_{}".format(signal_name, self._region_name), normalization_var=normalization_var)

		for syst_name, syst_value in syst_norm.iteritems():
			if not syst_name in self._systematics_norm:
				self._systematics_norm[syst_name] = {}
			self._systematics_norm[syst_name][signal_name] = syst_value

		for syst_name, syst_shape_hists in syst_shape.iteritems():
			if not syst_name in self._systematics_shape:
				self._systematics_shape[syst_name] = {}
			shape_hist_value = syst_shape_hists[0]
			shape_hist_up = RoofitHistContainer(syst_shape_hists[1], self._xvar, name="{}_{}_{}".format(signal_name, self._region_name, syst_name))
			shape_hist_down = RoofitHistContainer(syst_shape_hists[2], self._xvar, name="{}_{}_{}".format(signal_name, self._region_name, syst_name))
			self._systematics_shape[syst_name][signal_name] = (shape_hist_value, shape_hist_up, shape_hist_down)

	def add_data(self, data_name, hist):
		if not self._xvar:
			print "[Region::add_data] ERROR : Need to add an independent variable with add_xvar(xvar) first."
			sys.exit(1)
		self._data = RoofitHistContainer(hist, self._xvar, name="{}_{}".format(data_name, self._region_name))

	#def add_syst_norm(self, name, syst_dict):
	#	self._systematics_norm[name] = syst_dict

	def write(self, datacard_path, ws_path):
		ws_name = "ws_{}".format(self._region_name)
		# Create datacard
		with open(datacard_path, 'w') as datacard:
			datacard.write("imax 1 number of channels\n")
			datacard.write("jmax * number of processes minus 1\n")
			datacard.write("kmax * number of nuisance parameters\n")
			datacard.write("---------------\n")
			# shapes * bin_name file wsname:histogramname($PROCESS, $SYSTEMATIC)
			datacard.write("shapes * bin0 {} {}:$PROCESS_{}\n".format(os.path.basename(ws_path), ws_name, self._region_name))
			datacard.write("---------------\n")
			datacard.write("bin bin0\n")
			datacard.write("observation -1.0\n")
			datacard.write("---------------\n")
			datacard.write("bin {}\n".format(" bin0"*(len(self._background_names)+1)))
			datacard.write("process {} {}\n".format(self._signal_name, " ".join(self._background_names)))

			all_processes = [self._signal_name]
			all_processes.extend(self._background_names)

			process_index_string = "process "
			for i in xrange(len(all_processes)):
				process_index_string += " " + str(i)
			datacard.write(process_index_string + "\n")
			rate_string = "rate "
			for i in all_processes:
				rate_string += " -1"
			datacard.write(rate_string + "\n")
			datacard.write("---------------\n")

			for systematic in self._systematics_norm.keys():
				this_syst_string = systematic + " lnN "
				for process in all_processes:
					if process in self._systematics_norm[systematic]:
						this_syst_string += " {}".format(self._systematics_norm[systematic][process])
					else:
						this_syst_string += " -"
				datacard.write(this_syst_string + "\n")

			for systematic in self._systematics_shape.keys():
				this_syst_string = systematic + " shape "
				for process in all_processes:
					if process in self._systematics_shape[systematic]:
						this_syst_string += " {}".format(self._systematics_shape[systematic][process][0])
					else:
						this_syst_string += " -"
				datacard.write(this_syst_string + "\n")

		# Create workspace
		ws = ROOT.RooWorkspace(ws_name)
		for background_name in self._background_names:
			self._backgrounds[background_name].RooDataHist().SetName("{}_{}".format(background_name, self._region_name))
			getattr(ws, "import")(self._backgrounds[background_name].RooDataHist())
		self._signal.RooDataHist().SetName("{}_{}".format(self._signal_name, self._region_name))
		getattr(ws, "import")(self._signal.RooDataHist())
		self._data.RooDataHist().SetName("{}_{}".format("data_obs", self._region_name))
		getattr(ws, "import")(self._data.RooDataHist())
		for syst_name in self._systematics_shape.keys():
			for process, syst_shape_hists in self._systematics_shape[syst_name].iteritems():
				getattr(ws, "import")(syst_shape_hists[1])
				getattr(ws, "import")(syst_shape_hists[2])
		ws.writeToFile(ws_path)		
