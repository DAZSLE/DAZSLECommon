This is a repository for code common to DAZSLE analyses, i.e. an attempt to consolidate the divergent branches of ZPrimePlusJet. No analysis-specific code should be added.

### Data:
- data/SimpleN2DDT: 3D histograms (N2 vs pt vs rho) from QCD MC for computing simple N2DDT on the fly

### C++ classes:
- Class BaconTree: TTree:MakeSelector()s for bacon bits
   - Derived class BaconData adds some useful functions, like selecting the jet of interest and computing N2DDT.
- Class HistogramManager: utility class for managing histograms.

### python modules:
- python/rhalphabet: original rhalphabet code from 2016 H(bb) analysis
- python/combine_helper: python package for constructing Rhalphabet datacards (based on original rhalphabet code, intended for better flexibility with multiple SRs)
- python/analyzer: base class AnalysisBase defines an interface for bacon -> histograms step. Base class Cutflow provides more utilities for automatic creation of cutflows and N-1 histograms in the analyzer.

### python helpers:
- python/cross_sections.py: cross sections of MC samples
- python/seaborn_colors: provides colors from the Seaborn module.