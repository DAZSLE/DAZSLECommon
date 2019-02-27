import os

txt_folder = os.path.expandvars("$CMSSW_BASE/src/DAZSLE/DAZSLECommon/data/baconbits")

baconbits_lists = {
	2016:{
		# For large samples, use un-hadded files on lxplus
		"JetHTRun2016B":"{}/2016/lxplus/JetHTRun2016B.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016B_PromptReco_v2_resub.root"]
		"JetHTRun2016C":"{}/2016/lxplus/JetHTRun2016C.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016C_PromptReco_v2.root"]
		"JetHTRun2016D":"{}/2016/lxplus/JetHTRun2016D.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016D_PromptReco_v2.root"]
		"JetHTRun2016E":"{}/2016/lxplus/JetHTRun2016E.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016E_PromptReco_v2.root"]
		"JetHTRun2016F":"{}/2016/lxplus/JetHTRun2016F.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016F_PromptReco_v1.root"]
		"JetHTRun2016G":"{}/2016/lxplus/JetHTRun2016G.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016G_PromptReco_v1.root"]
		"JetHTRun2016H":"{}/2016/lxplus/JetHTRun2016H.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016H_PromptReco_v2.root"]
		"SingleMuRun2016B":"{}/2016/lxplus/SingleMuRun2016B.txt".format(txt_folder), 
		"SingleMuRun2016C":"{}/2016/lxplus/SingleMuRun2016C.txt".format(txt_folder), 
		"SingleMuRun2016D":"{}/2016/lxplus/SingleMuRun2016D.txt".format(txt_folder), 
		"SingleMuRun2016E":"{}/2016/lxplus/SingleMuRun2016E.txt".format(txt_folder), 
		"SingleMuRun2016F":"{}/2016/lxplus/SingleMuRun2016F.txt".format(txt_folder), 
		"SingleMuRun2016G":"{}/2016/lxplus/SingleMuRun2016G.txt".format(txt_folder), 
		"SingleMuRun2016H":"{}/2016/lxplus/SingleMuRun2016H.txt".format(txt_folder), 
		"JetHTRun2016B_ps10":"{}/2016/lxplus/JetHTRun2016B.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016B_PromptReco_v2_resub.root"]
		"JetHTRun2016C_ps10":"{}/2016/lxplus/JetHTRun2016C.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016C_PromptReco_v2.root"]
		"JetHTRun2016D_ps10":"{}/2016/lxplus/JetHTRun2016D.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016D_PromptReco_v2.root"]
		"JetHTRun2016E_ps10":"{}/2016/lxplus/JetHTRun2016E.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016E_PromptReco_v2.root"]
		"JetHTRun2016F_ps10":"{}/2016/lxplus/JetHTRun2016F.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016F_PromptReco_v1.root"]
		"JetHTRun2016G_ps10":"{}/2016/lxplus/JetHTRun2016G.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016G_PromptReco_v1.root"]
		"JetHTRun2016H_ps10":"{}/2016/lxplus/JetHTRun2016H.txt".format(txt_folder), #["root://cmsxrootd-site.fnal.gov//store/user/jduarte1/zprimebits-v11.062/JetHTRun2016H_PromptReco_v2.root"]
		"SingleMuRun2016B_ps10":"{}/2016/lxplus/SingleMuRun2016B.txt".format(txt_folder), 
		"SingleMuRun2016C_ps10":"{}/2016/lxplus/SingleMuRun2016C.txt".format(txt_folder), 
		"SingleMuRun2016D_ps10":"{}/2016/lxplus/SingleMuRun2016D.txt".format(txt_folder), 
		"SingleMuRun2016E_ps10":"{}/2016/lxplus/SingleMuRun2016E.txt".format(txt_folder), 
		"SingleMuRun2016F_ps10":"{}/2016/lxplus/SingleMuRun2016F.txt".format(txt_folder), 
		"SingleMuRun2016G_ps10":"{}/2016/lxplus/SingleMuRun2016G.txt".format(txt_folder), 
		"SingleMuRun2016H_ps10":"{}/2016/lxplus/SingleMuRun2016H.txt".format(txt_folder), 
		"QCD_HT100to200":"{}/2016/lxplus/QCD_HT100to200_13TeV.txt".format(txt_folder),
		"QCD_HT200to300":"{}/2016/lxplus/QCD_HT200to300_13TeV.txt".format(txt_folder),
		"QCD_HT300to500":"{}/2016/lxplus/QCD_HT300to500_13TeV.txt".format(txt_folder),
		"QCD_HT500to700":"{}/2016/lxplus/QCD_HT500to700_13TeV.txt".format(txt_folder),
		"QCD_HT700to1000":"{}/2016/lxplus/QCD_HT700to1000_13TeV.txt".format(txt_folder),
		"QCD_HT1000to1500":"{}/2016/lxplus/QCD_HT1000to1500_13TeV.txt".format(txt_folder),
		"QCD_HT1500to2000":"{}/2016/lxplus/QCD_HT1500to2000_13TeV.txt".format(txt_folder),
		"QCD_HT2000toInf":"{}/2016/lxplus/QCD_HT2000toInf_13TeV.txt".format(txt_folder),

		# Smaller samples can stay on cmslpc
		"GluGluHToBB_M125_13TeV_powheg_pythia8_CKKW":"{}/2016/cmslpc/GluGluHToBB_M125_13TeV_powheg_pythia8_CKKW.txt".format(txt_folder),
		"VBFHToBB_M_125_13TeV_powheg_pythia8":"{}/2016/cmslpc/VBFHToBB_M_125_13TeV_powheg_pythia8.txt".format(txt_folder),
		"WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8":"{}/2016/cmslpc/WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8.txt".format(txt_folder),
		"WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8":"{}/2016/cmslpc/WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8.txtt".format(txt_folder),
		"ttHTobb_M125_13TeV_powheg_pythia8":"{}/2016/cmslpc/ttHTobb_M125_13TeV_powheg_pythia8.txt".format(txt_folder),
		"ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8":"{}/2016/cmslpc/ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8.txt".format(txt_folder),
		"ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8":"{}/2016/cmslpc/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8.txt".format(txt_folder),
		"ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8":"{}/2016/cmslpc/ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8.txt".format(txt_folder),
		"ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8":"{}/2016/cmslpc/ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8.txt".format(txt_folder),
		"WWTo4Q_13TeV_powheg":"{}/2016/cmslpc/WWTo4Q_13TeV_powheg.txt".format(txt_folder),
		"ZZ_13TeV_pythia8":"{}/2016/cmslpc/ZZ_13TeV_pythia8.txt".format(txt_folder),
		"WZ_13TeV_pythia8":"{}/2016/cmslpc/WZ_13TeV_pythia8.txt".format(txt_folder),
		"DYJetsToQQ_HT180_13TeV":"{}/2016/cmslpc/DYJetsToQQ_HT180_13TeV.txt".format(txt_folder),
		"DYJetsToLL_M_50_13TeV":"{}/2016/cmslpc/DYJetsToLL_M_50_13TeV.txt".format(txt_folder),
		"ST_t_channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV_powhegV2_madspin":"{}/2016/cmslpc/ST_t_channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV_powhegV2_madspin.txt".format(txt_folder),
		"ST_t_channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV_powhegV2_madspin":"{}/2016/cmslpc/ST_t_channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV_powhegV2_madspin.txt".format(txt_folder),
		"ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M2T4":"{}/2016/cmslpc/ST_tW_antitop_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M2T4.txt".format(txt_folder),
		"ST_tW_top_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M2T4":"{}/2016/cmslpc/ST_tW_top_5f_inclusiveDecays_13TeV_powheg_pythia8_TuneCUETP8M2T4.txt".format(txt_folder),
		"WJetsToQQ_HT_600ToInf_13TeV":"{}/2016/cmslpc/WJetsToQQ_HT_600ToInf_13TeV.txt".format(txt_folder),
		"WJetsToQQ_HT180_13TeV":"{}/2016/cmslpc/WJetsToQQ_HT180_13TeV.txt".format(txt_folder),
		"WJetsToLNu_HT_70To100_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_70To100_13TeV.txt".format(txt_folder),
		"WJetsToLNu_HT_600To800_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_600To800_13TeV.txtt".format(txt_folder),
		"WJetsToLNu_HT_100To200_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_100To200_13TeV.txt".format(txt_folder),
		"WJetsToLNu_HT_200To400_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_200To400_13TeV.txt".format(txt_folder),
		"WJetsToLNu_HT_400To600_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_400To600_13TeV.txt".format(txt_folder),
		"WJetsToLNu_HT_600To800_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_600To800_13TeV.txt".format(txt_folder),
		"WJetsToLNu_HT_800To1200_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_800To1200_13TeV.txt".format(txt_folder),
		"WJetsToLNu_HT_1200To2500_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_1200To2500_13TeV.txt".format(txt_folder),
		"WJetsToLNu_HT_2500ToInf_13TeV":"{}/2016/cmslpc/WJetsToLNu_HT_2500ToInf_13TeV.txt".format(txt_folder),
		"TT_powheg":"{}/2016/cmslpc/TT_powheg.txt".format(txt_folder),

	},
	2017:{},
	2018:{
		"WJetsToQQ_HT400to600":"{}/2018/WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV.txt".format(txt_folder),
		"WJetsToQQ_HT600to800":"{}/2018/WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV.txt".format(txt_folder),
		"WJetsToQQ_HT800toInf":"{}/2018/WJetsToQQ_HT800toInf_qc19_3j_TuneCP5_13TeV.txt".format(txt_folder),
		"ZJetsToQQ_HT400to600":"{}/2018/ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV.txt".format(txt_folder),
		"ZJetsToQQ_HT600to800":"{}/2018/ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV.txt".format(txt_folder),
		"ZJetsToQQ_HT800toInf":"{}/2018/ZJetsToQQ_HT800toInf_qc19_4j_TuneCP5_13TeV.txt".format(txt_folder),
	},
}

baconbits = {}
for year, sampledict in baconbits_lists.iteritems():
	baconbits[year] = {}
	for sample, txt_path in sampledict.iteritems():
		baconbits[year][sample] = [line.strip() for line in open(txt_path, 'r')]