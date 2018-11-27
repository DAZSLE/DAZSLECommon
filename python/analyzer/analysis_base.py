import os
import sys
from abc import ABCMeta, abstractmethod
import time
import datetime
import ROOT
from ROOT import *

#ROOT.gROOT.ProcessLine('template HBHEDigi BaconData::Digi<HBHEDigi>(int i);') # Unfortunate hack needed for pyroot to recognize templated member functions

class AnalysisBase(object):
	__metaclass__ = ABCMeta
	def __init__(self, tree_name="otree"):
		self._files = []
		self._chain = ROOT.TChain(tree_name)

	def add_file(self, filename):
		self._chain.Add(filename)
		self._files.append(filename)

	def start_timer(self):
		self._ts_start = time.time()
		print "[Analysis::start_timer] INFO : Start time: {}".format(datetime.datetime.fromtimestamp(self._ts_start).strftime('%Y-%m-%d %H:%M:%S'))

	def print_progress(self, this_event, first_event, last_event, print_every):
		if this_event % print_every == 0:
			print "[Analysis::print_progress] INFO : Processing event {} / {}".format(this_event + 1, last_event)
			if this_event != first_event:
				if self._ts_start > 0 :
					elapsed_time = time.time() - self._ts_start
					estimated_completion = self._ts_start + (1. * elapsed_time * (last_event - first_event) / (this_event - first_event))
					m, s = divmod(elapsed_time, 60)
					h, m = divmod(m, 60)
					print "[Analysis::print_progress] INFO : \tElapsed time: {} : {} : {:.3}".format(int(round(h, 0)), int(round(m, 0)), s)
					print "[Analysis::print_progress] INFO : \tEstimated finish time: {}".format(datetime.datetime.fromtimestamp(estimated_completion).strftime('%Y-%m-%d %H:%M:%S'))
				else:
					print "[Analysis::print_progress] INFO : \tFor time estimates, call self.start_timer() right before starting the event loop"


	# Anything before looping over the tree.
	# Histogram definitions go here.
	@abstractmethod
	def start(self):
		pass

	# Main event loop.
	# Fill histograms here. 
	@abstractmethod
	def run(self, max_nevents=-1, first_event=0, nprint=-1):
		pass

	# Anything after looping over the tree.
	# Histogram postprocessing and output go here.
	@abstractmethod
	def finish(self):
		pass

