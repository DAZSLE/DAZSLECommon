import os
import sys
from ROOT import RooRealVar

# Class for creating combine datacards and workspaces

class CombineProject():
	def __init__(self, directory):
		self._region_names = []
		self._regions = {}
		self._directory = directory

	def create_xvar(self, xvar_name, x_range):
		self._xvar = RooRealVar(xvar_name, xvar_name, x_range[0], x_range[1])
		return self._xvar

	def xvar(self):
		if not self._xvar:
			print "[CombineProject::xvar] ERROR : Request for nonexistent xvar"
			sys.exit(1)
		return self._xvar

	def add_region(self, region):
		if region.name() in self._region_names:
			print "[CombineProject::add_region] ERROR : Region already exists: {}".format(region.name())
			sys.exit(1)
		self._region_names.append(region.name())
		self._regions[region.name()] = region

	def write(self):
		# Make individual region datacards and workspaces
		datacard_paths = {}
		ws_paths = {}
		for region_name in self._region_names:
			datacard_paths[region_name] = "{}/datacard_{}.txt".format(self._directory, region_name)
			ws_paths[region_name] = "{}/ws_{}.root".format(self._directory, region_name)
			self._regions[region_name].write(datacard_path=datacard_paths[region_name], ws_path=ws_paths[region_name])

		# Combine the regions into a megacard
		# chdir into the directtory, to avoid pulling in full workspace paths into datacard
		cwd = os.getcwd()
		os.chdir(self._directory)

		combine_card_command = "combineCards.py "
		for region_name in self._region_names:
			combine_card_command += " {}={}".format(region_name, os.path.basename(datacard_paths[region_name]))
		combine_card_command += " > {}/datacard_total.txt".format(self._directory)
		os.system(combine_card_command)

		os.chdir(cwd)