This is a repository for code common to DAZSLE analyses, i.e. an attempt to unify the divergent branches of ZPrimePlusJet. No analysis-specific code should be added.

Initial content:
- data/SimpleN2DDT: 3D histograms (N2 vs pt vs rho) from QCD MC for computing simple N2DDT on the fly
- Class BaconTree: TTree:MakeSelector()s for bacon bits
   - Derived class BaconData adds some useful functions, like selecting the jet of interest and computing N2DDT.
- python/combine_helper: python package for constructing Rhalphabet datacards
- python/cross_sections.py: cross sections of MC samples
- python/analysis_base.py: class AnalysisBase, interface for python analyzer framework