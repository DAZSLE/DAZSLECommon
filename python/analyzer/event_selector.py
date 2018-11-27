import os
import sys
from ROOT import *
from cutflow import Cutflow
from types import MethodType
import math

# Decorator for adding a cut function to the selector.
''' Example: 
sr_selector = EventSelector()

@add_cut(sr_selector)
@add_nm1_hist(sr_selector, [("pt", "p_{T} [GeV]", 120, 0., 1200.)])
def min_pt(self, event):
	self._return_data["min_pt"]["pt"] = event.SelectedJet_pt
	return event.SelectedJet_pt > 400.

''' 
def add_cut(selector):
    def decorator(cut_func):
        #@wraps(cut_func) 
        #def wrapper(self, *args, **kwargs): 
        #    return cut_func(*args, **kwargs)

        # Note we are not binding cut_func, but wrapper which accepts self but does exactly the same as cut_func
        #setattr(selector, cut_func.__name__, wrapper) # Maybe this works, but probably best to use MethodType
        #exec("selector.{} = types.MethodType(cut_func, selector, EventSelector)".format(cut_func.__name__))
        
        # My method
        setattr(selector, cut_func.__name__, MethodType(cut_func, selector))
        selector.register_cut(cut_func.__name__)

        return cut_func # returning cut_func means cut_func can still be used normally
    return decorator

def add_nm1_hist(selector, variable_name, xtitle, nbins, xmin, xmax):
	def decorator(cut_func):
		selector.add_nm1_histogram(cut_func.__name__, variable_name, xtitle, nbins, xmin, xmax)
		return cut_func
	return decorator



# Specialization of Cutflow to event selection. 
class EventSelector(Cutflow):
	def __init__(self, name="UnnamedEventSelector", event=None):
		super(EventSelector, self).__init__(name)
		self._event = event
		self._object_selectors = {}
		self._event_pass = False
		self._event_pass_nm1 = {}
		self._cut_results = {}
		self._object_name = "Event"

	def add_object_selector(self, object_name, object_selector):
		self._object_selectors[object_name] = object_selector

	def get_object_pass(self, object_name, i):
		return self._object_selectors[object_name].get_object_pass(i)

	def event(self):
		return self._event

	# Set pointer to the event data. If the event instance is constant, better to set this in the constructor; this method enables changing the pointer, if it happens to be reallocated.
	def set_event(self, event):
		self._event = event

	def process_event(self, event, weight=1):
		self.reset()
		self._pass_calls += 1
		self._pass_calls_weighted += weight

		for object_selector in self._object_selectors:
			object_selector.process_event(weight)

		# Run cuts
		this_pass = True
		for cut in self._cut_list:
			self._cut_results[cut] = getattr(self, cut)(event) # Or self._cut_functions[cut](self._event)?
			if not self._cut_results[cut]:
				if this_pass:
					this_pass = False
					self._cutflow_counter[cut] += 1
					self._cutflow_counter_weighted[cut] += weight
				self._cut_counter[cut] += 1
				self._cut_counter_weighted[cut] += weight
			if this_pass:
				self._pass_counter[cut] += 1
				self._pass_counter_weighted[cut] += weight
		self._event_pass = this_pass

		# N-1 histograms
		for cut in self._cut_list:
			# Calculate N-1
			self._event_pass_nm1[cut] = True
			for cut2 in self._cut_list:
				if cut == cut2:
					continue
				if not self._cut_results[cut2]:
					self._event_pass_nm1[cut] = False
					break

			# Fill histograms
			if self._event_pass_nm1[cut]:
				if cut in self._nm1_histograms:
					for variable_name, histogram in self._nm1_histograms[cut].iteritems():
						if self._return_data[cut][variable_name] == None:
							print "[EventSelector::process_event] ERROR : Return data was not set, selector {}, self._return_data[{}][{}]".format(self._name, cut, variable_name)
							sys.exit(1)
						histogram.Fill(self._return_data[cut][variable_name])
		# Reset return data
		for cut_name, cut_data in self._return_data.iteritems():
			for variable_name in cut_data.keys():
				cut_data[variable_name] = None

	def event_pass(self):
		return self._event_pass

	def event_pass_nm1(self, cut_name):
		return self._event_pass_nm1[cut_name]

	def event_passes_cut(self, cut_name):
		return self._cut_results[cut_name]

	def reset(self):
		self._event = None
		self._cut_results.clear()
		self._event_pass = False
		self._event_pass_nm1.clear()

	# Add a cut to the selector
	def register_cut(self, cut_name):
		self._cut_list.append(cut_name)
		self._pass_counter[cut_name] = 0
		self._pass_counter_weighted[cut_name] = 0
		self._cutflow_counter[cut_name] = 0
		self._cutflow_counter_weighted[cut_name] = 0
		self._cut_counter[cut_name] = 0
		self._cut_counter_weighted[cut_name] = 0

	# Add a cut to the selector, including defining the function from a string
	# - cut_name = name of cut. The function is named <selector_name>_<cut_name>.
	# - cut_logic = logic of cut (python string). It must define a variable cut_result=True/False
	def add_cut(self, cut_name, cut_logic, return_data=None):
		register_cut(cut_name)

		# Create the cut function
		function_name = "{}_{}".format(self._name, cut_name)
		exec("""
def {}(self, event):
	{}
	return cut_result
""".format(function_name, cut_logic))

		# Attach cut function to this instance
		exec("self.{} = MethodType({}, self, EventSelector)".format(cut_name, function_name))
