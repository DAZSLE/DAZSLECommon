# Slice up the pt vs msd histogram into 1D msd histograms
# - Optionally, apply the rho cut based on the bin center
def SliceHistogram(hist2d, pt_categories, rho_range=None):
	# Make sure the requested pt bins correspond to boundaries
	pt_axis = hist2d.GetYaxis()
	histogram_pt_boundaries = []
	for bin in xrange(1, pt_axis.GetNbins() + 1):
		histogram_pt_boundaries.append(pt_axis.GetBinLowEdge(bin))
	histogram_pt_boundaries.append(pt_axis.GetBinUpEdge(pt_axis.GetNbins()))

	for pt_category in pt_categories:
		if not pt_category[0] in histogram_pt_boundaries:
			print "[run_histograms::SliceSignalHistogram] ERROR : Bin boundary {} does not correspond to a histogram bin boundary.".format(pt_category[0])
			print histogram_pt_boundaries
			sys.exit(1)
		if not pt_category[1] in histogram_pt_boundaries:
			print "[run_histograms::SliceSignalHistogram] ERROR : Bin boundary {} does not correspond to a histogram bin boundary.".format(pt_category[1])
			print histogram_pt_boundaries
			sys.exit(1)

	histogram_slices = {}
	for islice in xrange(len(pt_categories)):
		ptmin = pt_categories[islice][0]
		ptmax = pt_categories[islice][1]
		binmin = 1e10
		binmax = -1e10
		for bin in xrange(1, hist2d.GetNbinsY() + 1):
			low_edge = hist2d.GetYaxis().GetBinLowEdge(bin)
			up_edge = hist2d.GetYaxis().GetBinUpEdge(bin)
			# Is this bin inside this pt slice (+epsilon)?
			if ptmin - 1.e-5 < low_edge and up_edge < ptmax + 1.e-5:
				if bin < binmin:
					binmin = bin
				if bin > binmax:
					binmax = bin
		histogram_slices[islice] = hist2d.ProjectionX(hist2d.GetName() + "_" + str(islice), binmin, binmax)
		histogram_slices[islice].SetDirectory(0)

		if rho_range:
			bin_pt = pt_categories[islice][0] + (pt_categories[islice][1] - pt_categories[islice][0]) * 0.3
			for xbin in xrange(1, histogram_slice[islice].GetNbinsX() + 1):
				bin_mass = histogram_slice[islice].GetXaxis().GetBinCenter(xbin)
				bin_rho = 2. * math.log(bin_mass / bin_pt)
				if bin_rho < rho_range[0] or bin_rho > rho_range[1]:
					histogram_slice[islice].SetBinContent(xbin, 0)
					histogram_slice[islice].SetBinError(xbin, 0)
	return histogram_slices
