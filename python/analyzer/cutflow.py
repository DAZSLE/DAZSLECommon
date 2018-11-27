import os
import sys
import ROOT
from ROOT import *
import abc

class Cutflow:
	__metaclass__ = abc.ABCMeta

	def __init__(self, name="UnnamedCutflow"):
		self._name = name
		self._object_name = ""
		self._cut_list = []
		self._cut_parameters = {}
		self._cut_functions = {}

		# N-1 histogram stuff
		self._return_data = {} # Container for storing the variables to be filled in the N-1 histograms. Should be set when the cut function is called.
		self._nm1_variables = {} # Map from the cut name to the variable name
		self._nm1_histograms = {}

		# Cutflow counting containers
		self._pass_calls = 0
		self._pass_calls_weighted = 0.
		self._cut_counter = {}
		self._cutflow_counter = {}
		self._pass_counter = {}
		self._cut_counter_weighted = {}
		self._cutflow_counter_weighted = {}
		self._pass_counter_weighted = {}

	# Add a cut that is predefined in the index self._cut_functions
	def add_cut(self, cut_name, cut_parameters=None):
		self._cut_list.append(cut_name)
		self._cut_parameters[cut_name] = cut_parameters # Maybe should deep copy this?
		self._nm1_histograms[cut_name] = {}

		# Initialize cut counters
		self._cut_counter[cut_name] = 0
		self._cutflow_counter[cut_name] = 0
		self._pass_counter[cut_name] = 0
		self._cut_counter_weighted[cut_name] = 0
		self._cutflow_counter_weighted[cut_name] = 0
		self._pass_counter_weighted[cut_name] = 0

	# Add a cut string, which is evaluated using python eval (note, must make sense within the class! Perhaps better to use predefined cuts)
	def add_cut_string(self, cut_name, cut_string, cut_parameters):
		#self._cut_functions[cut_name] = eval("lambda: " + cut_string)
		setattr(self, cut_name, eval("lambda: " + cut_string))
		self.add_cut(cut_name, cut_parameters)

	#############################
	### N-1 histogram methods ###
	#############################

	# Creates a histograms of variable_name that is filled if all cuts except cut_name are True.
	# self._cut_functions[cut_name] must set self._return_data[cut_name][variable_name]. 
	def add_nm1_histogram(self, cut_name, variable_name, xtitle, nbins, xmin, xmax):
		if not cut_name in self._nm1_histograms:
			self._nm1_histograms[cut_name] = {}
		if not cut_name in self._return_data:
			self._return_data[cut_name] = {}
		self._nm1_histograms[cut_name][variable_name] = TH1D("h_nm1_{}_CUT_{}_VAR_{}".format(self._name, cut_name, variable_name), "h_nm1_{}_{}_{}".format(self._name, cut_name, variable_name), nbins, xmin, xmax)
		self._nm1_histograms[cut_name][variable_name].SetDirectory(0)
		self._nm1_histograms[cut_name][variable_name].Sumw2()
		self._nm1_histograms[cut_name][variable_name].GetXaxis().SetTitle(xtitle)
		self._return_data[cut_name][variable_name] = None

	def save_nm1_histograms(self, directory):
		directory.cd()
		for cut, hist_dict in self._nm1_histograms.iteritems():
			for var, hist in hist_dict.iteritems():
				hist.Write()


	#######################
	### Cutflow methods ###
	#######################
	def print_cutflow(self):
		print "[Cutflow::print_cutflow] INFO : Printing cut flow"
		print "[Cutflow::print_cutflow] INFO : \tInclusive => {}".format(self._pass_calls)
		for cut_name in self._cut_list:
			print "[Cutflow::print_cutflow] INFO : \t{} => {}".format(cut_name, self._pass_counter[cut_name])


	def make_cutflow_histograms(self, directory):
		directory.cd()

		n_cuts = len(self._cut_list)
		h_cutflow_counter = TH1D("CutFlowCounter_" + self._name, "CutFlowCounter_" + self._name, n_cuts + 2, -0.5, n_cuts + 2.5)
		h_cutflow_counter.GetXaxis().SetTitle("Cut Name")
		if self._object_name != "":
			h_cutflow_counter.GetYaxis().SetTitle(self._object_name + "s Remaining")
		else:
			h_cutflow_counter.GetYaxis().SetTitle("Objects Remaining")
		h_cutflow_counter_weighted = h_cutflow_counter.Clone()
		h_cutflow_counter_weighted.SetName(h_cutflow_counter_weighted.GetName() + "_weighted")

		h_cut_counter = TH1D("CutCounter_" + self._name, "CutCounter_" + self._name, n_cuts + 2, -0.5, n_cuts + 2.5)
		h_cut_counter.GetXaxis().SetTitle("Cut Name");
		if self._object_name != "":
			h_cut_counter.GetYaxis().SetTitle(self._object_name + "s Failing Cut")
		else:
			h_cut_counter.GetYaxis().SetTitle("Objects Failing Cut")
		h_cut_counter_weighted = h_cut_counter.Clone();
		h_cut_counter_weighted.SetName(h_cut_counter_weighted.GetName() + "_weighted");

		bin = 1
		h_cutflow_counter.SetBinContent(bin, self._pass_calls)
		h_cutflow_counter.GetXaxis().SetBinLabel(bin, "Inclusive")
		h_cut_counter.SetBinContent(bin, self._pass_calls)
		h_cut_counter.GetXaxis().SetBinLabel(bin, "Total")

		h_cutflow_counter_weighted.SetBinContent(bin, self._pass_calls_weighted)
		h_cutflow_counter_weighted.GetXaxis().SetBinLabel(bin, "Inclusive")
		h_cut_counter_weighted.SetBinContent(bin, self._pass_calls_weighted)
		h_cut_counter_weighted.GetXaxis().SetBinLabel(bin, "Total")
		bin += 1

		for cut_name in self._cut_list:
			h_cutflow_counter.SetBinContent(bin, self._pass_counter[cut_name])
			h_cutflow_counter.GetXaxis().SetBinLabel(bin, cut_name)

			h_cut_counter.SetBinContent(bin, self._cut_counter[cut_name])
			h_cut_counter.GetXaxis().SetBinLabel(bin, cut_name)
			
			h_cutflow_counter_weighted.SetBinContent(bin, self._pass_counter_weighted[cut_name])
			h_cutflow_counter_weighted.GetXaxis().SetBinLabel(bin, cut_name)

			h_cut_counter_weighted.SetBinContent(bin, self._cut_counter_weighted[cut_name])
			h_cut_counter_weighted.GetXaxis().SetBinLabel(bin, cut_name)

			bin += 1
		h_cutflow_counter.Write()
		h_cutflow_counter_weighted.Write()
		h_cut_counter.Write()
		h_cut_counter_weighted.Write()

