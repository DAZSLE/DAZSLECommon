from DAZSLE.PhiBBPlusJet.event_selector import EventSelector
import math

class BaconEventSelector(EventSelector):
	def __init__(self, name="UnnamedBaconEventSelector"):
		super(BaconEventSelector, self).__init__(name)


	def Min_dphi_mu_jet(self):
		phi_mu = self._event.vmuoLoose0_phi
		phi_jet = 0.
		if self._cut_parameters["Min_dphi_mu_jet"]["jet_type"] == "AK8":
			phi_jet = self._event.AK8Puppijet0_phi
		elif self._cut_parameters["Min_dphi_mu_jet"]["jet_type"] == "CA15":
			phi_jet = self._event.CA15Puppijet0_phi
		else:
			print "[BaconEventCutFunctions.Min_dphi_mu_jet] ERROR : Cut parameter jet_type must be AK8 or CA15. Found " +  self._cut_parameters["Min_dphi_mu_jet"]["jet_type"]
			exit(1)
		delta_phi = math.acos(math.cos(phi_mu - phi_jet))
		self._return_data["Min_dphi_mu_jet"] = delta_phi
		return (delta_phi > self._cut_parameters["Min_dphi_mu_jet"]["Min_dphi_mu_jet"])

	def Min_AK8Puppijet0_msd(self):
		self._return_data["Min_AK8Puppijet0_msd"] = self._event.AK8Puppijet0_msd
		return (self._event.AK8Puppijet0_msd >= self._cut_parameters["Min_AK8Puppijet0_msd"])

	def Max_AK8Puppijet0_msd(self):
		self._return_data["Max_AK8Puppijet0_msd"] = self._event.AK8Puppijet0_msd
		return (self._event.AK8Puppijet0_msd <= self._cut_parameters["Max_AK8Puppijet0_msd"])

	def Min_AK8Puppijet0_msd_puppi(self):
		self._return_data["Min_AK8Puppijet0_msd_puppi"] = self._event.AK8Puppijet0_msd_puppi
		return (self._event.AK8Puppijet0_msd_puppi >= self._cut_parameters["Min_AK8Puppijet0_msd_puppi"])

	def Max_AK8Puppijet0_msd_puppi(self):
		self._return_data["Max_AK8Puppijet0_msd_puppi"] = self._event.AK8Puppijet0_msd_puppi
		return (self._event.AK8Puppijet0_msd_puppi <= self._cut_parameters["Max_AK8Puppijet0_msd_puppi"])

	def Min_AK8Puppijet0_rho(self):
		self._return_data["Min_AK8Puppijet0_rho"] = self._event.AK8Puppijet0_rho
		return (self._event.AK8Puppijet0_rho >= self._cut_parameters["Min_AK8Puppijet0_rho"])

	def Max_AK8Puppijet0_rho(self):
		self._return_data["Max_AK8Puppijet0_rho"] = self._event.AK8Puppijet0_rho
		return (self._event.AK8Puppijet0_rho <= self._cut_parameters["Max_AK8Puppijet0_rho"])

	def Min_AK8Puppijet0_pt(self):
		jet_pt = 0.
		systematic = self._cut_parameters["Min_AK8Puppijet0_pt"]["systematic"].lower()
		if (systematic == "nominal"):
			jet_pt = self._event.AK8Puppijet0_pt
		elif (systematic == "jesup"):
			jet_pt = self._event.AK8Puppijet0_pt_JESUp
		elif (systematic == "jesdown"):
			jet_pt = self._event.AK8Puppijet0_pt_JESDown
		elif (systematic == "jerup"):
			jet_pt = self._event.AK8Puppijet0_pt_JERUp
		elif (systematic == "jerdown"):
			jet_pt = self._event.AK8Puppijet0_pt_JERDown
		else:
			print "[Min_AK8Puppijet0_pt] ERROR : Systematic " + systematic + " not known." 
			exit(1)
		self._return_data["Min_AK8Puppijet0_pt"] = jet_pt
		return (jet_pt >= self._cut_parameters["Min_AK8Puppijet0_pt"]["Min_AK8Puppijet0_pt"])

	def Max_AK8Puppijet0_pt(self):
		jet_pt = 0.
		systematic = self._cut_parameters["Max_AK8Puppijet0_pt"]["systematic"].lower()
		if (systematic == "nominal"):
			jet_pt = self._event.AK8Puppijet0_pt
		elif (systematic == "jesup"):
			jet_pt = self._event.AK8Puppijet0_pt_JESUp
		elif (systematic == "jesdown"):
			jet_pt = self._event.AK8Puppijet0_pt_JESDown
		elif (systematic == "jerup"):
			jet_pt = self._event.AK8Puppijet0_pt_JERUp
		elif (systematic == "jerdown"):
			jet_pt = self._event.AK8Puppijet0_pt_JERDown
		else:
			print "[Max_AK8Puppijet0_pt] ERROR : Systematic " + systematic + " not known." 
			exit(1)
		self._return_data["Max_AK8Puppijet0_pt"] = jet_pt
		return (jet_pt <= self._cut_parameters["Max_AK8Puppijet0_pt"]["Max_AK8Puppijet0_pt"])

	def Min_AK8CHSjet0_doublecsv(self):
		self._return_data["Min_AK8CHSjet0_doublecsv"] = self._event.AK8CHSjet0_doublecsv
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		self._return_data["AK8Puppijet0_tau21"] = self._event.AK8Puppijet0_tau21
		self._return_data["AK8Puppijet0_tau32"] = self._event.AK8Puppijet0_tau32
		return (self._event.AK8CHSjet0_doublecsv >= self._cut_parameters["Min_AK8CHSjet0_doublecsv"])

	def Max_AK8CHSjet0_doublecsv(self):
		self._return_data["Max_AK8CHSjet0_doublecsv"] = self._event.AK8CHSjet0_doublecsv
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		self._return_data["AK8Puppijet0_tau21"] = self._event.AK8Puppijet0_tau21
		self._return_data["AK8Puppijet0_tau32"] = self._event.AK8Puppijet0_tau32
		return (self._event.AK8CHSjet0_doublecsv <= self._cut_parameters["Max_AK8CHSjet0_doublecsv"])

	def Min_AK8Puppijet0_doublecsv(self):
		self._return_data["Min_AK8Puppijet0_doublecsv"] = self._event.AK8Puppijet0_doublecsv
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		self._return_data["AK8Puppijet0_tau21"] = self._event.AK8Puppijet0_tau21
		self._return_data["AK8Puppijet0_tau32"] = self._event.AK8Puppijet0_tau32
		return (self._event.AK8Puppijet0_doublecsv >= self._cut_parameters["Min_AK8Puppijet0_doublecsv"])

	def Max_AK8Puppijet0_doublecsv(self):
		self._return_data["Max_AK8Puppijet0_doublecsv"] = self._event.AK8Puppijet0_doublecsv
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		self._return_data["AK8Puppijet0_tau21"] = self._event.AK8Puppijet0_tau21
		self._return_data["AK8Puppijet0_tau32"] = self._event.AK8Puppijet0_tau32
		return (self._event.AK8Puppijet0_doublecsv <= self._cut_parameters["Max_AK8Puppijet0_doublecsv"])

	def Min_nmuLoose(self):
		self._return_data["Min_nmuLoose"] = self._event.nmuLoose
		return (self._event.nmuLoose >= self._cut_parameters["Min_nmuLoose"])

	def Max_nmuLoose(self):
		self._return_data["Max_nmuLoose"] = self._event.nmuLoose
		return (self._event.nmuLoose <= self._cut_parameters["Max_nmuLoose"])

	def Min_vmuoLoose0_pt(self):
		self._return_data["Min_vmuoLoose0_pt"] = self._event.vmuoLoose0_pt
		return (self._event.vmuoLoose0_pt >= self._cut_parameters["Min_vmuoLoose0_pt"])

	def Max_vmuoLoose0_pt(self):
		self._return_data["Max_vmuoLoose0_pt"] = self._event.vmuoLoose0_pt
		return (self._event.vmuoLoose0_pt <= self._cut_parameters["Max_vmuoLoose0_pt"])

	def Min_vmuoLoose0_abseta(self):
		self._return_data["Min_vmuoLoose0_abseta"] = self._event.vmuoLoose0_eta
		return (abs(self._event.vmuoLoose0_eta) >= self._cut_parameters["Min_vmuoLoose0_abseta"])

	def Max_vmuoLoose0_abseta(self):
		self._return_data["Max_vmuoLoose0_abseta"] = self._event.vmuoLoose0_eta
		return (abs(self._event.vmuoLoose0_eta) <= self._cut_parameters["Max_vmuoLoose0_abseta"])

	def Min_neleLoose(self):
		self._return_data["Min_neleLoose"] = self._event.neleLoose
		return (self._event.neleLoose >= self._cut_parameters["Min_neleLoose"])

	def Max_neleLoose(self):
		self._return_data["Max_neleLoose"] = self._event.neleLoose
		return (self._event.neleLoose <= self._cut_parameters["Max_neleLoose"])

	def Min_ntau(self):
		self._return_data["Min_ntau"] = self._event.ntau
		return (self._event.ntau >= self._cut_parameters["Min_ntau"])

	def Max_ntau(self):
		self._return_data["Max_ntau"] = self._event.ntau
		return (self._event.ntau <= self._cut_parameters["Max_ntau"])

	def Min_nphoLoose(self):
		self._return_data["Min_nphoLoose"] = self._event.nphoLoose
		return (self._event.nphoLoose >= self._cut_parameters["Min_nphoLoose"])

	def Max_nphoLoose(self):
		self._return_data["Max_nphoLoose"] = self._event.nphoLoose
		return (self._event.nphoLoose <= self._cut_parameters["Max_nphoLoose"])

	def AK8Puppijet0_isTightVJet(self):
		self._return_data["AK8Puppijet0_isTightVJet"] = self._event.AK8Puppijet0_isTightVJet
		return (self._event.AK8Puppijet0_isTightVJet == 1)

	def Min_puppet(self):
		this_puppet = 0.
		systematic = self._cut_parameters["Min_puppet"]["systematic"].lower()
		if (systematic == "nominal"):
			this_puppet = self._event.puppet
		elif (systematic == "jesup"):
			this_puppet = self._event.puppet_JESUp
		elif (systematic == "jesdown"):
			this_puppet = self._event.puppet_JESDown
		elif (systematic == "jerup"):
			this_puppet = self._event.puppet_JERUp
		elif (systematic == "jerdown"):
			this_puppet = self._event.puppet_JERDown
		else:
			print "[Min_puppet] ERROR : Systematic " + systematic + " not known." 
			exit(1)
		self._return_data["Min_puppet"] = this_puppet
		return (this_puppet >= self._cut_parameters["Min_puppet"]["Min_puppet"])

	def Max_puppet(self):
		this_puppet = 0.
		systematic = self._cut_parameters["Max_puppet"]["systematic"].lower()
		if (systematic == "nominal"):
			this_puppet = self._event.puppet
		elif (systematic == "jesup"):
			this_puppet = self._event.puppet_JESUp
		elif (systematic == "jesdown"):
			this_puppet = self._event.puppet_JESDown
		elif (systematic == "jerup"):
			this_puppet = self._event.puppet_JERUp
		elif (systematic == "jerdown"):
			this_puppet = self._event.puppet_JERDown
		else:
			print "[Max_puppet] ERROR : Systematic " + systematic + " not known." 
			exit(1)
		self._return_data["Max_puppet"] = this_puppet
		return (this_puppet <= self._cut_parameters["Max_puppet"]["Max_puppet"])

	def Min_pfmet(self):
		this_pfmet = 0.
		systematic = self._cut_parameters["Min_pfmet"]["systematic"].lower()
		if (systematic == "nominal"):
			this_pfmet = self._event.pfmet
		elif (systematic == "jesup"):
			this_pfmet = self._event.pfmet_JESUp
		elif (systematic == "jesdown"):
			this_pfmet = self._event.pfmet_JESDown
		elif (systematic == "jerup"):
			this_pfmet = self._event.pfmet_JERUp
		elif (systematic == "jerdown"):
			this_pfmet = self._event.pfmet_JERDown
		else:
			print "[Min_pfmet] ERROR : Systematic " + systematic + " not known." 
			exit(1)
		self._return_data["Min_pfmet"] = this_pfmet
		return (this_pfmet >= self._cut_parameters["Min_pfmet"]["Min_pfmet"])

	def Max_pfmet(self):
		this_pfmet = 0.
		systematic = self._cut_parameters["Max_pfmet"]["systematic"].lower()
		if (systematic == "nominal"):
			this_pfmet = self._event.pfmet
		elif (systematic == "jesup"):
			this_pfmet = self._event.pfmet_JESUp
		elif (systematic == "jesdown"):
			this_pfmet = self._event.pfmet_JESDown
		elif (systematic == "jerup"):
			this_pfmet = self._event.pfmet_JERUp
		elif (systematic == "jerdown"):
			this_pfmet = self._event.pfmet_JERDown
		else:
			print "[Max_pfmet] ERROR : Systematic " + systematic + " not known." 
			exit(1)
		self._return_data["Max_pfmet"] = this_pfmet
		return (this_pfmet <= self._cut_parameters["Max_pfmet"]["Max_pfmet"])

	def Max_nAK4PuppijetsPt30dR08_0(self):
		self._return_data["Max_nAK4PuppijetsPt30dR08_0"] = self._event.nAK4PuppijetsPt30dR08_0
		return (self._event.nAK4PuppijetsPt30dR08_0 <= self._cut_parameters["Max_nAK4PuppijetsPt30dR08_0"])

	def Min_nAK4PuppijetsMPt50dR08_0(self):
		self._return_data["Min_nAK4PuppijetsMPt50dR08_0"] = self._event.nAK4PuppijetsMPt50dR08_0
		return (self._event.nAK4PuppijetsMPt50dR08_0 >= self._cut_parameters["Min_nAK4PuppijetsMPt50dR08_0"])

	def Min_AK8Puppijet0_tau21(self):
		self._return_data["Min_AK8Puppijet0_tau21"] = self._event.AK8Puppijet0_tau21
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		return (self._event.AK8Puppijet0_tau21 >= self._cut_parameters["Min_AK8Puppijet0_tau21"])

	def Max_AK8Puppijet0_tau21(self):
		self._return_data["Max_AK8Puppijet0_tau21"] = self._event.AK8Puppijet0_tau21
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		self._return_data["AK8CHSjet0_doublecsv"] = self._event.AK8CHSjet0_doublecsv
		return (self._event.AK8Puppijet0_tau21 <= self._cut_parameters["Max_AK8Puppijet0_tau21"])

	def Min_AK8Puppijet0_tau21DDT(self):
		self._return_data["Min_AK8Puppijet0_tau21DDT"] = self._event.AK8Puppijet0_tau21DDT
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		return (self._event.AK8Puppijet0_tau21DDT >= self._cut_parameters["Min_AK8Puppijet0_tau21DDT"])

	def Max_AK8Puppijet0_tau21DDT(self):
		self._return_data["Max_AK8Puppijet0_tau21DDT"] = self._event.AK8Puppijet0_tau21DDT
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		self._return_data["AK8CHSjet0_doublecsv"] = self._event.AK8CHSjet0_doublecsv
		return (self._event.AK8Puppijet0_tau21DDT <= self._cut_parameters["Max_AK8Puppijet0_tau21DDT"])

	def Min_AK8Puppijet0_N2DDT(self):
		self._return_data["Min_AK8Puppijet0_N2DDT"] = self._event.AK8Puppijet0_N2DDT
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		return (self._event.AK8Puppijet0_N2DDT >= self._cut_parameters["Min_AK8Puppijet0_N2DDT"])

	def Max_AK8Puppijet0_N2DDT(self):
		self._return_data["Max_AK8Puppijet0_N2DDT"] = self._event.AK8Puppijet0_N2DDT
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		self._return_data["AK8CHSjet0_doublecsv"] = self._event.AK8CHSjet0_doublecsv
		return (self._event.AK8Puppijet0_N2DDT <= self._cut_parameters["Max_AK8Puppijet0_N2DDT"])

	def Min_AK8Puppijet0_tau32(self):
		self._return_data["Min_AK8Puppijet0_tau32"] = self._event.AK8Puppijet0_tau32
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		self._return_data["AK8CHSjet0_doublecsv"] = self._event.AK8CHSjet0_doublecsv
		return (self._event.AK8Puppijet0_tau32 >= self._cut_parameters["Min_AK8Puppijet0_tau32"])

	def Max_AK8Puppijet0_tau32(self):
		self._return_data["Max_AK8Puppijet0_tau32"] = self._event.AK8Puppijet0_tau32
		self._return_data["AK8Puppijet0_pt"] = self._event.AK8Puppijet0_pt
		return (self._event.AK8Puppijet0_tau32 <= self._cut_parameters["Max_AK8Puppijet0_tau32"])

	def Min_CA15Puppijet0_N2DDT(self):
		self._return_data["Min_CA15Puppijet0_N2DDT"] = self._event.CA15Puppijet0_N2DDT
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		return (self._event.CA15Puppijet0_N2DDT >= self._cut_parameters["Min_CA15Puppijet0_N2DDT"])

	def Max_CA15Puppijet0_N2DDT(self):
		self._return_data["Max_CA15Puppijet0_N2DDT"] = self._event.CA15Puppijet0_N2DDT
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		self._return_data["CA15CHSjet0_doublecsv"] = self._event.CA15CHSjet0_doublecsv
		return (self._event.CA15Puppijet0_N2DDT <= self._cut_parameters["Max_CA15Puppijet0_N2DDT"])

	def Min_CA15Puppijet0_msd(self):
		self._return_data["Min_CA15Puppijet0_msd"] = self._event.CA15Puppijet0_msd
		return (self._event.CA15Puppijet0_msd >= self._cut_parameters["Min_CA15Puppijet0_msd"])

	def Max_CA15Puppijet0_msd(self):
		self._return_data["Max_CA15Puppijet0_msd"] = self._event.CA15Puppijet0_msd
		return (self._event.CA15Puppijet0_msd <= self._cut_parameters["Max_CA15Puppijet0_msd"])

	def Min_CA15Puppijet0_msd_puppi(self):
		self._return_data["Min_CA15Puppijet0_msd_puppi"] = self._event.CA15Puppijet0_msd_puppi
		return (self._event.CA15Puppijet0_msd_puppi >= self._cut_parameters["Min_CA15Puppijet0_msd_puppi"])

	def Max_CA15Puppijet0_msd_puppi(self):
		self._return_data["Max_CA15Puppijet0_msd_puppi"] = self._event.CA15Puppijet0_msd_puppi
		return (self._event.CA15Puppijet0_msd_puppi <= self._cut_parameters["Max_CA15Puppijet0_msd_puppi"])

	def Min_CA15Puppijet0_rho(self):
		self._return_data["Min_CA15Puppijet0_rho"] = self._event.CA15Puppijet0_rho
		return (self._event.CA15Puppijet0_rho >= self._cut_parameters["Min_CA15Puppijet0_rho"])

	def Max_CA15Puppijet0_rho(self):
		self._return_data["Max_CA15Puppijet0_rho"] = self._event.CA15Puppijet0_rho
		return (self._event.CA15Puppijet0_rho <= self._cut_parameters["Max_CA15Puppijet0_rho"])

	def CA15Puppijet0_isTightVJet(self):
		self._return_data["CA15Puppijet0_isTightVJet"] = self._event.CA15Puppijet0_isTightVJet
		return (self._event.CA15Puppijet0_isTightVJet == 1)

	def Min_CA15CHSjet0_doublecsv(self):
		self._return_data["Min_CA15CHSjet0_doublecsv"] = self._event.CA15CHSjet0_doublecsv
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		self._return_data["CA15Puppijet0_tau21"] = self._event.CA15Puppijet0_tau21
		self._return_data["CA15Puppijet0_tau32"] = self._event.CA15Puppijet0_tau32
		return (self._event.CA15CHSjet0_doublecsv >= self._cut_parameters["Min_CA15CHSjet0_doublecsv"])
	
	def Max_CA15CHSjet0_doublecsv(self):
		self._return_data["Max_CA15CHSjet0_doublecsv"] = self._event.CA15CHSjet0_doublecsv
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		self._return_data["CA15Puppijet0_tau21"] = self._event.CA15Puppijet0_tau21
		self._return_data["CA15Puppijet0_tau32"] = self._event.CA15Puppijet0_tau32
		return (self._event.CA15CHSjet0_doublecsv <= self._cut_parameters["Max_CA15CHSjet0_doublecsv"])
	
	def Min_CA15Puppijet0_doublesub(self):
		self._return_data["Min_CA15Puppijet0_doublesub"] = self._event.CA15Puppijet0_doublesub
		return (self._event.CA15Puppijet0_doublesub >= self._cut_parameters["Min_CA15Puppijet0_doublesub"])
	
	def Max_CA15Puppijet0_doublesub(self):
		self._return_data["Max_CA15Puppijet0_doublesub"] = self._event.CA15Puppijet0_doublesub
		return (self._event.CA15Puppijet0_doublesub <= self._cut_parameters["Max_CA15Puppijet0_doublesub"])
	
	def Min_CA15Puppijet0_pt(self):
		jet_pt = 0.
		systematic = self._cut_parameters["Min_CA15Puppijet0_pt"]["systematic"].lower()
		if (systematic == "nominal"):
			jet_pt = self._event.CA15Puppijet0_pt
		elif (systematic == "jesup"):
			jet_pt = self._event.CA15Puppijet0_pt_JESUp
		elif (systematic == "jesdown"):
			jet_pt = self._event.CA15Puppijet0_pt_JESDown
		elif (systematic == "jerup"):
			jet_pt = self._event.CA15Puppijet0_pt_JERUp
		elif (systematic == "jerdown"):
			jet_pt = self._event.CA15Puppijet0_pt_JERDown
		else:
			print "[Min_CA15Puppijet0_pt] ERROR : Systematic " + systematic + " not known, or not implemented for CA15Puppi jets." 
			exit(1)
		self._return_data["Min_CA15Puppijet0_pt"] = jet_pt
		return (jet_pt >= self._cut_parameters["Min_CA15Puppijet0_pt"]["Min_CA15Puppijet0_pt"])
	
	def Max_CA15Puppijet0_pt(self):
		jet_pt = 0.
		systematic = self._cut_parameters["Max_CA15Puppijet0_pt"]["systematic"].lower()
		if (systematic == "nominal"):
			jet_pt = self._event.CA15Puppijet0_pt
		elif (systematic == "jesup"):
			jet_pt = self._event.CA15Puppijet0_pt_JESUp
		elif (systematic == "jesdown"):
			jet_pt = self._event.CA15Puppijet0_pt_JESDown
		elif (systematic == "jerup"):
			jet_pt = self._event.CA15Puppijet0_pt_JERUp
		elif (systematic == "jerdown"):
			jet_pt = self._event.CA15Puppijet0_pt_JERDown
		else:
			print "[Max_CA15Puppijet0_pt] ERROR : Systematic " + systematic + " not known, or not implemented for CA15Puppi jets." 
			exit(1)
		self._return_data["Max_CA15Puppijet0_pt"] = jet_pt
		return (jet_pt <= self._cut_parameters["Max_CA15Puppijet0_pt"]["Max_CA15Puppijet0_pt"])
	
	def Min_CA15CHSjet0_pt(self):
		jet_pt = 0.
		systematic = self._cut_parameters["Min_CA15CHSjet0_pt"]["systematic"].lower()
		if (systematic == "nominal"):
			jet_pt = self._event.CA15CHSjet0_pt
		elif (systematic == "jesup"):
			jet_pt = self._event.CA15CHSjet0_pt_JESUp
		elif (systematic == "jesdown"):
			jet_pt = self._event.CA15CHSjet0_pt_JESDown
		elif (systematic == "jerup"):
			jet_pt = self._event.CA15CHSjet0_pt_JERUp
		elif (systematic == "jerdown"):
			jet_pt = self._event.CA15CHSjet0_pt_JERDown
		else:
			print "[Min_CA15CHSjet0_pt] ERROR : Systematic " + systematic + " not known, or not implemented for CA15CHS jets." 
			exit(1)
		self._return_data["Min_CA15CHSjet0_pt"] = jet_pt
		return (jet_pt >= self._cut_parameters["Min_CA15CHSjet0_pt"]["Min_CA15CHSjet0_pt"])
	
	def Max_CA15CHSjet0_pt(self):
		jet_pt = 0.
		systematic = self._cut_parameters["Max_CA15CHSjet0_pt"]["systematic"].lower()
		if (systematic == "nominal"):
			jet_pt = self._event.CA15CHSjet0_pt
		elif (systematic == "jesup"):
			jet_pt = self._event.CA15CHSjet0_pt_JESUp
		elif (systematic == "jesdown"):
			jet_pt = self._event.CA15CHSjet0_pt_JESDown
		elif (systematic == "jerup"):
			jet_pt = self._event.CA15CHSjet0_pt_JERUp
		elif (systematic == "jerdown"):
			jet_pt = self._event.CA15CHSjet0_pt_JERDown
		else:
			print "[Max_CA15CHSjet0_pt] ERROR : Systematic " + systematic + " not known, or not implemented for CA15CHS jets." 
			exit(1)
		self._return_data["Max_CA15CHSjet0_pt"] = jet_pt
		return (jet_pt <= self._cut_parameters["Max_CA15CHSjet0_pt"]["Max_CA15CHSjet0_pt"])
	
	def Min_CA15Puppijet0_abseta(self):
		self._return_data["Min_CA15Puppijet0_abseta"] = self._event.CA15Puppijet0_eta
		return (TMath.Abs(self._event.CA15Puppijet0_eta) >= self._cut_parameters["Min_CA15Puppijet0_abseta"])
	
	def Max_CA15Puppijet0_abseta(self):
		self._return_data["Max_CA15Puppijet0_abseta"] = self._event.CA15Puppijet0_eta
		return (TMath.Abs(self._event.CA15Puppijet0_eta) <= self._cut_parameters["Max_CA15Puppijet0_abseta"])
	
	def Min_CA15Puppijet0_phi(self):
		self._return_data["Min_CA15Puppijet0_phi"] = self._event.CA15Puppijet0_phi
		return (self._event.CA15Puppijet0_phi >= self._cut_parameters["Min_CA15Puppijet0_phi"])
	
	def Max_CA15Puppijet0_phi(self):
		self._return_data["Max_CA15Puppijet0_phi"] = self._event.CA15Puppijet0_phi
		return (self._event.CA15Puppijet0_phi <= self._cut_parameters["Max_CA15Puppijet0_phi"])
	
	def Min_CA15CHSjet1_doublecsv(self):
		self._return_data["Min_CA15CHSjet1_doublecsv"] = self._event.CA15CHSjet1_doublecsv
		return (self._event.CA15CHSjet1_doublecsv >= self._cut_parameters["Min_CA15CHSjet1_doublecsv"])
	
	def Max_CA15CHSjet1_doublecsv(self):
		self._return_data["Max_CA15CHSjet1_doublecsv"] = self._event.CA15CHSjet1_doublecsv
		return (self._event.CA15CHSjet1_doublecsv <= self._cut_parameters["Max_CA15CHSjet1_doublecsv"])
	
	def Min_CA15Puppijet1_doublesub(self):
		self._return_data["Min_CA15Puppijet1_doublesub"] = self._event.CA15Puppijet1_doublesub
		return (self._event.CA15Puppijet1_doublesub >= self._cut_parameters["Min_CA15Puppijet1_doublesub"])
	
	def Max_CA15Puppijet1_doublesub(self):
		self._return_data["Max_CA15Puppijet1_doublesub"] = self._event.CA15Puppijet1_doublesub
		return (self._event.CA15Puppijet1_doublesub <= self._cut_parameters["Max_CA15Puppijet1_doublesub"])
	
	def Min_CA15Puppijet1_pt(self):
		self._return_data["Min_CA15Puppijet1_pt"] = self._event.CA15Puppijet1_pt
		return (self._event.CA15Puppijet1_pt >= self._cut_parameters["Min_CA15Puppijet1_pt"])
	
	def Max_CA15Puppijet1_pt(self):
		self._return_data["Max_CA15Puppijet1_pt"] = self._event.CA15Puppijet1_pt
		return (self._event.CA15Puppijet1_pt <= self._cut_parameters["Max_CA15Puppijet1_pt"])
	
	def Min_CA15Puppijet1_abseta(self):
		self._return_data["Min_CA15Puppijet1_abseta"] = self._event.CA15Puppijet1_eta
		return (TMath.Abs(self._event.CA15Puppijet1_eta) >= self._cut_parameters["Min_CA15Puppijet1_abseta"])
	
	def Max_CA15Puppijet1_abseta(self):
		self._return_data["Max_CA15Puppijet1_abseta"] = self._event.CA15Puppijet1_eta
		return (TMath.Abs(self._event.CA15Puppijet1_eta) <= self._cut_parameters["Max_CA15Puppijet1_abseta"])
	
	def Min_CA15Puppijet1_phi(self):
		self._return_data["Min_CA15Puppijet1_phi"] = self._event.CA15Puppijet1_phi
		return (self._event.CA15Puppijet1_phi >= self._cut_parameters["Min_CA15Puppijet1_phi"])
	
	def Max_CA15Puppijet1_phi(self):
		self._return_data["Max_CA15Puppijet1_phi"] = self._event.CA15Puppijet1_phi
		return (self._event.CA15Puppijet1_phi <= self._cut_parameters["Max_CA15Puppijet1_phi"])
	
	def Min_CA15CHSjet2_doublecsv(self):
		self._return_data["Min_CA15CHSjet2_doublecsv"] = self._event.CA15CHSjet2_doublecsv
		return (self._event.CA15CHSjet2_doublecsv >= self._cut_parameters["Min_CA15CHSjet2_doublecsv"])
	
	def Max_CA15CHSjet2_doublecsv(self):
		self._return_data["Max_CA15CHSjet2_doublecsv"] = self._event.CA15CHSjet2_doublecsv
		return (self._event.CA15CHSjet2_doublecsv <= self._cut_parameters["Max_CA15CHSjet2_doublecsv"])
	
	def Min_CA15Puppijet2_doublesub(self):
		self._return_data["Min_CA15Puppijet2_doublesub"] = self._event.CA15Puppijet2_doublesub
		return (self._event.CA15Puppijet2_doublesub >= self._cut_parameters["Min_CA15Puppijet2_doublesub"])
	
	def Max_CA15Puppijet2_doublesub(self):
		self._return_data["Max_CA15Puppijet2_doublesub"] = self._event.CA15Puppijet2_doublesub
		return (self._event.CA15Puppijet2_doublesub <= self._cut_parameters["Max_CA15Puppijet2_doublesub"])
	
	def Min_CA15Puppijet2_pt(self):
		self._return_data["Min_CA15Puppijet2_pt"] = self._event.CA15Puppijet2_pt
		return (self._event.CA15Puppijet2_pt >= self._cut_parameters["Min_CA15Puppijet2_pt"])
	
	def Max_CA15Puppijet2_pt(self):
		self._return_data["Max_CA15Puppijet2_pt"] = self._event.CA15Puppijet2_pt
		return (self._event.CA15Puppijet2_pt <= self._cut_parameters["Max_CA15Puppijet2_pt"])
	
	def Min_CA15Puppijet2_abseta(self):
		self._return_data["Min_CA15Puppijet2_abseta"] = self._event.CA15Puppijet2_eta
		return (TMath.Abs(self._event.CA15Puppijet2_eta) >= self._cut_parameters["Min_CA15Puppijet2_abseta"])
	
	def Max_CA15Puppijet2_abseta(self):
		self._return_data["Max_CA15Puppijet2_abseta"] = self._event.CA15Puppijet2_eta
		return (TMath.Abs(self._event.CA15Puppijet2_eta) <= self._cut_parameters["Max_CA15Puppijet2_abseta"])
	
	def Min_CA15Puppijet2_phi(self):
		self._return_data["Min_CA15Puppijet2_phi"] = self._event.CA15Puppijet2_phi
		return (self._event.CA15Puppijet2_phi >= self._cut_parameters["Min_CA15Puppijet2_phi"])
	
	def Max_CA15Puppijet2_phi(self):
		self._return_data["Max_CA15Puppijet2_phi"] = self._event.CA15Puppijet2_phi
		return (self._event.CA15Puppijet2_phi <= self._cut_parameters["Max_CA15Puppijet2_phi"])

	def Min_CA15Puppijet0_tau21(self):
		self._return_data["Min_CA15Puppijet0_tau21"] = self._event.CA15Puppijet0_tau21
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		return (self._event.CA15Puppijet0_tau21 >= self._cut_parameters["Min_CA15Puppijet0_tau21"])

	def Max_CA15Puppijet0_tau21(self):
		self._return_data["Max_CA15Puppijet0_tau21"] = self._event.CA15Puppijet0_tau21
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		self._return_data["CA15CHSjet0_doublecsv"] = self._event.CA15CHSjet0_doublecsv
		return (self._event.CA15Puppijet0_tau21 <= self._cut_parameters["Max_CA15Puppijet0_tau21"])

	def Min_CA15Puppijet0_tau21DDT(self):
		self._return_data["Min_CA15Puppijet0_tau21DDT"] = self._event.CA15Puppijet0_tau21DDT
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		return (self._event.CA15Puppijet0_tau21DDT >= self._cut_parameters["Min_CA15Puppijet0_tau21DDT"])

	def Max_CA15Puppijet0_tau21DDT(self):
		self._return_data["Max_CA15Puppijet0_tau21DDT"] = self._event.CA15Puppijet0_tau21DDT
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		self._return_data["CA15CHSjet0_doublecsv"] = self._event.CA15CHSjet0_doublecsv
		return (self._event.CA15Puppijet0_tau21DDT <= self._cut_parameters["Max_CA15Puppijet0_tau21DDT"])

	def Min_CA15Puppijet0_tau32(self):
		self._return_data["Min_CA15Puppijet0_tau32"] = self._event.CA15Puppijet0_tau32
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		self._return_data["CA15CHSjet0_doublecsv"] = self._event.CA15CHSjet0_doublecsv
		return (self._event.CA15Puppijet0_tau32 >= self._cut_parameters["Min_CA15Puppijet0_tau32"])

	def Max_CA15Puppijet0_tau32(self):
		self._return_data["Max_CA15Puppijet0_tau32"] = self._event.CA15Puppijet0_tau32
		self._return_data["CA15Puppijet0_pt"] = self._event.CA15Puppijet0_pt
		return (self._event.CA15Puppijet0_tau32 <= self._cut_parameters["Max_CA15Puppijet0_tau32"])

	# Override Cutflow::add_cut, in order to make automatic N-1 histograms
	def add_cut(self, cut_name, cut_parameters=None):
		super(BaconEventSelector, self).add_cut(cut_name, cut_parameters)
		if cut_name == "Min_dphi_mu_jet":
			self.add_nminusone_histogram(cut_name, cut_name, "#Delta#phi(#mu, jet)", 100, -2.*math.pi, 2.*math.pi);
		elif cut_name == "Min_AK8Puppijet0_msd":
			self.add_nminusone_histogram(cut_name, cut_name, "m_{SD} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_AK8Puppijet0_msd":
			self.add_nminusone_histogram(cut_name, cut_name, "m_{SD} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_AK8Puppijet0_msd_puppi":
			self.add_nminusone_histogram(cut_name, cut_name, "m_{SD}^{(PUPPI)} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_AK8Puppijet0_msd_puppi":
			self.add_nminusone_histogram(cut_name, cut_name, "m_{SD}^{(PUPPI)} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_AK8Puppijet0_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_AK8Puppijet0_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_AK8CHSjet0_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Max_AK8CHSjet0_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Min_AK8Puppijet0_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Max_AK8Puppijet0_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Min_nmuLoose":
			self.add_nminusone_histogram(cut_name, cut_name, "n_{#mu}", 11, -0.5, 10.5);
		elif cut_name == "Max_nmuLoose":
			self.add_nminusone_histogram(cut_name, cut_name, "n_{#mu}", 11, -0.5, 10.5);
		elif cut_name == "Min_vmuoLoose0_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "#mu p_{T} [GeV]", 1000, 0., 1000.);
		elif cut_name == "Max_vmuoLoose0_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "#mu p_{T} [GeV]", 1000, 0., 1000.);
		elif cut_name == "Min_vmuoLoose0_abseta":
			self.add_nminusone_histogram(cut_name, cut_name, "#mu #eta", 50, -5., 5.);
		elif cut_name == "Max_vmuoLoose0_abseta":
			self.add_nminusone_histogram(cut_name, cut_name, "#mu #eta", 50, -5., 5.);
		elif cut_name == "Min_neleLoose":
			self.add_nminusone_histogram(cut_name, cut_name, "n_{e}", 11, -0.5, 10.5);
		elif cut_name == "Max_neleLoose":
			self.add_nminusone_histogram(cut_name, cut_name, "n_{e}", 11, -0.5, 10.5);
		elif cut_name == "Min_ntau":
			self.add_nminusone_histogram(cut_name, cut_name, "n_{#tau}", 11, -0.5, 10.5); 
		elif cut_name == "Max_ntau":
			self.add_nminusone_histogram(cut_name, cut_name, "n_{#tau}", 11, -0.5, 10.5); 
		elif cut_name == "Min_nphoLoose":
			self.add_nminusone_histogram(cut_name, cut_name, "n_{#gamma}", 11, -0.5, 10.5); 
		elif cut_name == "Max_nphoLoose":
			self.add_nminusone_histogram(cut_name, cut_name, "n_{#gamma}", 11, -0.5, 10.5); 
		elif cut_name == "AK8Puppijet0_isTightVJet":
			self.add_nminusone_histogram(cut_name, cut_name, "Is tight VJet", 2, -0.5, 1.5); 
		elif cut_name == "CA15Puppijet0_isTightVJet":
			self.add_nminusone_histogram(cut_name, cut_name, "Is tight VJet", 2, -0.5, 1.5);
		elif cut_name == "Min_pfmet":
			self.add_nminusone_histogram(cut_name, cut_name, "PF MET [GeV]", 100, 0., 1000.); 
		elif cut_name == "Max_pfmet":
			self.add_nminusone_histogram(cut_name, cut_name, "PF MET [GeV]", 100, 0., 1000.); 
		elif cut_name == "Min_puppet":
			self.add_nminusone_histogram(cut_name, cut_name, "PUPPET [GeV]", 100, 0., 1000.); 
		elif cut_name == "Max_puppet":
			self.add_nminusone_histogram(cut_name, cut_name, "PUPPET [GeV]", 100, 0., 1000.); 
		elif cut_name == "Max_nAK4PuppijetsPt30dR08_0":
			self.add_nminusone_histogram(cut_name, cut_name, "Max_nAK4PuppijetsPt30dR08_0", 21, -0.5, 20.5);
		elif cut_name == "Min_nAK4PuppijetsMPt50dR08_0":
			self.add_nminusone_histogram(cut_name, cut_name, "Min_nAK4PuppijetsMPt50dR08_0", 21, -0.5, 20.5);
		elif cut_name == "Min_AK8Puppijet0_tau21":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{21}", 50, 0., 1.);
		elif cut_name == "Max_AK8Puppijet0_tau21":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{21}", 50, 0., 1.);
		elif cut_name == "Min_AK8Puppijet0_tau21DDT":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{21}^{DDT}", 50, 0., 1.);
		elif cut_name == "Max_AK8Puppijet0_tau21DDT":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{21}^{DDT}", 50, 0., 1.);
		elif cut_name == "Min_AK8Puppijet0_N2DDT":
			self.add_nminusone_histogram(cut_name, cut_name, "#N_{2}^{DDT}", 100, -5., 5.);
		elif cut_name == "Max_AK8Puppijet0_N2DDT":
			self.add_nminusone_histogram(cut_name, cut_name, "#N_{2}^{DDT}", 100, -5., 5.);
		elif cut_name == "Min_AK8Puppijet0_tau32":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{32}", 50, 0., 1.);
		elif cut_name == "Max_AK8Puppijet0_tau32":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{32}", 50, 0., 1.);
		elif cut_name == "Min_CA15Puppijet0_msd":
			self.add_nminusone_histogram(cut_name, cut_name, "m_{SD} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_CA15Puppijet0_msd":
			self.add_nminusone_histogram(cut_name, cut_name, "m_{SD} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_CA15Puppijet0_msd_puppi":
			self.add_nminusone_histogram(cut_name, cut_name, "m_{SD}^{(PUPPI)} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_CA15Puppijet0_msd_puppi":
			self.add_nminusone_histogram(cut_name, cut_name, "m_{SD}^{(PUPPI)} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_CA15CHSjet0_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Max_CA15CHSjet0_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Min_CA15Puppijet0_doublesub":
			self.add_nminusone_histogram(cut_name, cut_name, "Double sub", 40, -2., 2.);
		elif cut_name == "Max_CA15Puppijet0_doublesub":
			self.add_nminusone_histogram(cut_name, cut_name, "Double sub", 40, -2., 2.);
		elif cut_name == "Min_CA15Puppijet0_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_CA15Puppijet0_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_CA15CHSjet0_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_CA15CHSjet0_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_CA15Puppijet0_abseta":
			self.add_nminusone_histogram(cut_name, cut_name, "#eta", 50, -5., 5.);
		elif cut_name == "Max_CA15Puppijet0_abseta":
			self.add_nminusone_histogram(cut_name, cut_name, "#eta", 50, -5., 5.);
		elif cut_name == "Min_CA15Puppijet0_phi":
			self.add_nminusone_histogram(cut_name, cut_name, "#phi", 50, -5, 5);
		elif cut_name == "Max_CA15Puppijet0_phi":
			self.add_nminusone_histogram(cut_name, cut_name, "#phi", 50, -5, 5);
		elif cut_name == "Min_CA15CHSjet1_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Max_CA15CHSjet1_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Min_CA15Puppijet1_doublesub":
			self.add_nminusone_histogram(cut_name, cut_name, "Double sub", 40, -2., 2.);
		elif cut_name == "Max_CA15Puppijet1_doublesub":
			self.add_nminusone_histogram(cut_name, cut_name, "Double sub", 40, -2., 2.);
		elif cut_name == "Min_CA15Puppijet1_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_CA15Puppijet1_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_CA15Puppijet1_abseta":
			self.add_nminusone_histogram(cut_name, cut_name, "#eta", 50, -5., 5.);
		elif cut_name == "Max_CA15Puppijet1_abseta":
			self.add_nminusone_histogram(cut_name, cut_name, "#eta", 50, -5., 5.);
		elif cut_name == "Min_CA15Puppijet1_phi":
			self.add_nminusone_histogram(cut_name, cut_name, "#phi", 50, -5, 5);
		elif cut_name == "Max_CA15Puppijet1_phi":
			self.add_nminusone_histogram(cut_name, cut_name, "#phi", 50, -5, 5);
		elif cut_name == "Min_CA15CHSjet2_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Max_CA15CHSjet2_doublecsv":
			self.add_nminusone_histogram(cut_name, cut_name, "Double b-tag", 40, -2., 2.);
		elif cut_name == "Min_CA15Puppijet2_doublesub":
			self.add_nminusone_histogram(cut_name, cut_name, "Double sub", 40, -2., 2.);
		elif cut_name == "Max_CA15Puppijet2_doublesub":
			self.add_nminusone_histogram(cut_name, cut_name, "Double sub", 40, -2., 2.);
		elif cut_name == "Min_CA15Puppijet2_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Max_CA15Puppijet2_pt":
			self.add_nminusone_histogram(cut_name, cut_name, "p_{T} [GeV]", 200, 0., 2000.);
		elif cut_name == "Min_CA15Puppijet2_abseta":
			self.add_nminusone_histogram(cut_name, cut_name, "#eta", 50, -5., 5.);
		elif cut_name == "Max_CA15Puppijet2_abseta":
			self.add_nminusone_histogram(cut_name, cut_name, "#eta", 50, -5., 5.);
		elif cut_name == "Min_CA15Puppijet2_phi":
			self.add_nminusone_histogram(cut_name, cut_name, "#phi", 50, -5, 5);
		elif cut_name == "Max_CA15Puppijet2_phi":
			self.add_nminusone_histogram(cut_name, cut_name, "#phi", 50, -5, 5);
		elif cut_name == "Min_CA15Puppijet0_tau21":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{21}", 50, 0., 1.);
		elif cut_name == "Max_CA15Puppijet0_tau21":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{21}", 50, 0., 1.);
		elif cut_name == "Min_CA15Puppijet0_tau21DDT":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{21}^{DDT}", 50, 0., 1.);
		elif cut_name == "Max_CA15Puppijet0_tau21DDT":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{21}^{DDT}", 50, 0., 1.);
		elif cut_name == "Min_CA15Puppijet0_tau32":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{32}", 50, 0., 1.);
		elif cut_name == "Max_CA15Puppijet0_tau32":
			self.add_nminusone_histogram(cut_name, cut_name, "#tau_{32}", 50, 0., 1.);
		elif cut_name == "Min_CA15Puppijet0_N2DDT":
			self.add_nminusone_histogram(cut_name, cut_name, "#N_{2}^{DDT}", 100, -5., 5.);
		elif cut_name == "Max_CA15Puppijet0_N2DDT":
			self.add_nminusone_histogram(cut_name, cut_name, "#N_{2}^{DDT}", 100, -5., 5.);		
