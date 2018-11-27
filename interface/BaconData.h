#ifndef BaconData_h
#define BaconData_h

#include <typeinfo>
#include "DAZSLE/PhiBBPlusJet/interface/BaconTree.h"
#include "TMath.h"
#include "TH1D.h"
#include "TF1.h"
#include "TH2D.h"
#include "TH3D.h"
 /**
  * @brief      Class for exposing data from bacon ntuples.
  */
 

class BaconData : public BaconTree {
public:

	BaconData(TTree *tree=0);

	~BaconData();

	Int_t GetEntry(Long64_t entry);

	Double_t PUPPIweight(double pt, double eta) const;

	Bool_t IsVMatched(double matching_dR) const;

	TH2D* ComputeDDTMap(TH3D *h3_n2_pt_msd, double wp) const;

	double ComputeDDT(TH2D *ddt_map, double n2, double rho, double pt) const;

public:
	// Enums for specifying the jet type and jet selection
	enum JetType_t {
		kAK8,
		kCA15
	};
	JetType_t _jettype;

	enum JetOrdering_t {
		kPt,
		kDbtag,
		kN2DDT,
	};
	JetOrdering_t _jetordering;

	inline void SetJetSelection(JetType_t jettype, JetOrdering_t jetordering) {
		_jettype = jettype;
		_jetordering = jetordering;
	}

	enum WhichJet_t {
		kAK8_0,
		kAK8_1, 
		kAK8_2, 
		kCA15_0, 
		kCA15_1, 
		kCA15_2
	};

	// Computed variables
	Double_t AK8Puppijet0_tau21DDT;
	Double_t CA15Puppijet0_tau21DDT;
	Double_t AK8Puppijet0_rho;
	Double_t CA15Puppijet0_rho;
	Double_t AK8Puppijet0_N2DDT; // Old DDT: pre-compute WP 0.26
	Double_t CA15Puppijet0_N2DDT; // Old DDT: pre-compute WP 0.26
	std::map<double, double> AK8Puppijet0_N2DDT_wp; // New DDT: compute on the fly
	std::map<double, double> AK8Puppijet1_N2DDT_wp; 
	std::map<double, double> AK8Puppijet2_N2DDT_wp; 
	std::map<double, double> CA15Puppijet0_N2DDT_wp; // New DDT: compute on the fly
	std::map<double, double> CA15Puppijet1_N2DDT_wp; 
	std::map<double, double> CA15Puppijet2_N2DDT_wp; 
	Double_t CA15CHSjet0_N2DDT;
	Double_t AK8Puppijet0_msd_puppi;
	Double_t CA15Puppijet0_msd_puppi;

	Double_t AK8Puppijet1_tau21DDT;
	Double_t CA15Puppijet1_tau21DDT;
	Double_t AK8Puppijet1_rho;
	Double_t CA15Puppijet1_rho;
	Double_t AK8Puppijet1_N2DDT;
	Double_t CA15Puppijet1_N2DDT;
	Double_t CA15CHSjet1_N2DDT;
	Double_t AK8Puppijet1_msd_puppi;
	Double_t CA15Puppijet1_msd_puppi;

	Double_t AK8Puppijet2_tau21DDT;
	Double_t CA15Puppijet2_tau21DDT;
	Double_t AK8Puppijet2_rho;
	Double_t CA15Puppijet2_rho;
	Double_t AK8Puppijet2_N2DDT;
	Double_t CA15Puppijet2_N2DDT;
	Double_t CA15CHSjet2_N2DDT;
	Double_t AK8Puppijet2_msd_puppi;
	Double_t CA15Puppijet2_msd_puppi;

	Double_t puppet_JESUp;
	Double_t puppet_JESDown;
	Double_t puppet_JERUp;
	Double_t puppet_JERDown;
	Double_t pfmet_JESUp;
	Double_t pfmet_JESDown;
	Double_t pfmet_JERUp;
	Double_t pfmet_JERDown;

	// Containers for selected jet variables
	Double_t        SelectedJet_pt;
	Double_t        SelectedJet_eta;
	Double_t        SelectedJet_phi;
	Double_t        SelectedJet_csv;
	Double_t        SelectedJet_CHF;
	Double_t        SelectedJet_NHF;
	Double_t        SelectedJet_NEMF;
	Double_t        SelectedJet_tau21;
	Double_t        SelectedJet_tau32;
	Double_t        SelectedJet_msd;
	Double_t        SelectedJet_rho;
	Double_t        SelectedJet_minsubcsv;
	Double_t        SelectedJet_maxsubcsv;
	Double_t        SelectedJet_doublecsv;
	Double_t        SelectedJet_doublesub;
	Double_t        SelectedJet_ptraw;
	Double_t        SelectedJet_genpt;
	Double_t        SelectedJet_e2_b1;
	Double_t        SelectedJet_e3_b1;
	Double_t        SelectedJet_e3_v1_b1;
	Double_t        SelectedJet_e3_v2_b1;
	Double_t        SelectedJet_e4_v1_b1;
	Double_t        SelectedJet_e4_v2_b1;
	Double_t        SelectedJet_e2_b2;
	Double_t        SelectedJet_e3_b2;
	Double_t        SelectedJet_e3_v1_b2;
	Double_t        SelectedJet_e3_v2_b2;
	Double_t        SelectedJet_e4_v1_b2;
	Double_t        SelectedJet_e4_v2_b2;
	Double_t        SelectedJet_e2_sdb1;
	Double_t        SelectedJet_e3_sdb1;
	Double_t        SelectedJet_e3_v1_sdb1;
	Double_t        SelectedJet_e3_v2_sdb1;
	Double_t        SelectedJet_e4_v1_sdb1;
	Double_t        SelectedJet_e4_v2_sdb1;
	Double_t        SelectedJet_e2_sdb2;
	Double_t        SelectedJet_e3_sdb2;
	Double_t        SelectedJet_e3_v1_sdb2;
	Double_t        SelectedJet_e3_v2_sdb2;
	Double_t        SelectedJet_e4_v1_sdb2;
	Double_t        SelectedJet_e4_v2_sdb2;
	Double_t        SelectedJet_N2sdb1;
	Double_t        SelectedJet_N2sdb2;
	Double_t        SelectedJet_M2sdb1;
	Double_t        SelectedJet_M2sdb2;
	Double_t        SelectedJet_D2sdb1;
	Double_t        SelectedJet_D2sdb2;
	Double_t        SelectedJet_N2b1;
	Double_t        SelectedJet_N2b2;
	Double_t        SelectedJet_M2b1;
	Double_t        SelectedJet_M2b2;
	Double_t        SelectedJet_D2b1;
	Double_t        SelectedJet_D2b2;
	Double_t        SelectedJet_pt_old;
	Double_t        SelectedJet_pt_JESUp;
	Double_t        SelectedJet_pt_JESDown;
	Double_t        SelectedJet_pt_JERUp;
	Double_t        SelectedJet_pt_JERDown;
	Int_t           SelectedJet_isTightVJet;
	Double_t 		SelectedJet_tau21DDT;
	Double_t 		SelectedJet_N2DDT;
	std::map<double, double> SelectedJet_N2DDT_wp;
	Double_t 		SelectedJet_msd_puppi;
	Int_t           SelectedJet_nParticles;
private:
	std::map<double, TH2D*> n2_ddt_transformation_AK8_;
	std::map<double, TH2D*> n2_ddt_transformation_CA15_;
	std::vector<double> n2ddt_wps_;
	TH3D* n2_pt_rho_AK8_; // Base histograms for deriving N2 DDT
	TH3D* n2_pt_rho_CA15_; // Base histograms for deriving N2 DDT
	TF1* puppi_corr_gen_;
	TF1* puppi_corr_reco_cen_;
	TF1* puppi_corr_reco_for_;

};


#endif