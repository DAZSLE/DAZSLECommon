This is a repository for (bacon bits > histograms > limits) common to DAZSLE analyses, i.e. an attempt to consolidate the divergent branches of ZPrimePlusJet. No analysis-specific code should be added.

### C++ classes:
- Class BaconTree: TTree:MakeSelector()s for bacon bits
   - Derived class BaconData adds some useful functions, like selecting the jet of interest and computing N2DDT.
- Class HistogramManager: utility class for managing histograms.

### python modules:
- python/rhalphabet: original rhalphabet code from 2016 H(bb) analysis
- python/combine_helper: python package for constructing Rhalphabet datacards (based on original rhalphabet code, intended for better flexibility with multiple SRs)
- python/analyzer: 
   - Class AnalysisBase: defines an interface for bacon -> histograms step. 
   - Class Cutflow: base class for EventSelector, defining cutflow and N-1 histogram functionality.
   - Class EventSelector: class for performing a sequence of event-level cuts on BaconData. (Cuts are added with decorators, see https://github.com/DryRun/PhiBBPlusJet/blob/zqq/analysis/histograms.py for an example)

### python helpers:
- python/cross_sections.py: cross sections of MC samples
- python/seaborn_colors: provides colors from the Seaborn module.

### Data:
- data/SimpleN2DDT: 3D histograms (N2 vs pt vs rho) from QCD MC for computing simple N2DDT on the fly

### Wish list:
- Cristina's new N2DDT code
- N2/double b-tag/mass scale factor code? This might be worth its own repository.
