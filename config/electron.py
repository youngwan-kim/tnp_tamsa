from tnpConfig import tnpConfig

############## samples ################
samples={
    'data2016a':'/gv0/Users/hsseo/EgammaTnP/UL2016preVFP/data/SingleElectron',
    'mi2016a':'/gv0/Users/hsseo/EgammaTnP/UL2016preVFP/mc/DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos',
    'mg2016a':'/gv0/Users/hsseo/EgammaTnP/UL2016preVFP/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'data2016b':'/gv0/Users/hsseo/EgammaTnP/UL2016postVFP/data/SingleElectron',
    'mi2016b':'/gv0/Users/hsseo/EgammaTnP/UL2016postVFP/mc/DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos',
    'mg2016b':'/gv0/Users/hsseo/EgammaTnP/UL2016postVFP/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
}
############## binning ################
bin_ID = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 15, 20, 25, 30, 35, 40, 45, 70, 100, 500] },
]
bin_Ele35 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 31, 35, 37, 40, 45, 55, 70, 100, 500] },
]
bin_Ele32 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 28, 31, 33, 35, 38, 40, 45, 55, 70, 100, 500] },
]
bin_Ele28 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 24, 28, 30, 32, 35, 40, 45, 55, 70, 100, 500] },
]
bin_Ele27 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 23, 26, 28, 30, 32, 35, 40, 45, 55, 70, 100, 500] },
]
bin_Ele23 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 19, 23, 25, 27, 30, 35, 40, 45, 55, 70, 100, 500] },
]
bin_Ele12 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 12, 15, 18, 20, 25, 30, 35, 40, 45, 55, 70, 100, 500] },
]


############### Expr ################
## selection
tight_mcTrue='el_pt>20 || (el_et/mc_probe_et>0.8 && el_et/mc_probe_et < 1.2 && (el_eta-mc_probe_eta)*(el_eta-mc_probe_eta)+(el_phi-mc_probe_phi)*(el_phi-mc_probe_phi)<0.0004 )'
mtcut='(el_pt>20 || (tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45))'

## fits
fit_nominal = [
    "HistPdf::sigPhysPass(x,histPassMatched,2)",
    "HistPdf::sigPhysFail(x,histFailMatched,2)",
    "Gaussian::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[0.5,0.02,4.0])",
    "Gaussian::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[0.5,0.02,4.0])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "RooCMSShape::bkgPass(x,acmsP[60.,50.,80.],betaP[0.05,0.01,0.08],gammaP[0.1, 0, 1],peakP[90.0])",
    "RooCMSShape::bkgFail(x,acmsF[60.,50.,80.],betaF[0.05,0.01,0.08],gammaF[0.1, 0, 1],peakF[90.0])",
]

fit_altsig = [
    "HistPdf::sigRefPass(x,histPassMatched,2)",
    "HistPdf::sigRefFail(x,histFailMatched,2)",
    "HistPdf::sigPhysPass(x,histPassMatchedGen,2)",
    "HistPdf::sigPhysFail(x,histFailMatchedGen,2)",
    "RooCBShape::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[1,0.3,10.0],alphaP[2.0,1.2,3.5],nP[3,-5,5])",
    "RooCBShape::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[1,0.3,10.0],alphaF[2.0,1.2,3.5],nF[3,-5,5])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "Fit sigPass histPassMatched",
    "Fit sigFail histFailMatched",
    "SetConstant alphaP nP alphaF nF",
    "RooCMSShape::bkgPass(x,acmsP[60.,50.,80.],betaP[0.05,0.01,0.08],gammaP[0.1, 0, 1],peakP[90.0])",
    "RooCMSShape::bkgFail(x,acmsF[60.,50.,80.],betaF[0.05,0.01,0.08],gammaF[0.1, 0, 1],peakF[90.0])",
]

fit_altbkg = [
    "HistPdf::sigPhysPass(x,histPassMatched,2)",
    "HistPdf::sigPhysFail(x,histFailMatched,2)",
    "Gaussian::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[0.5,0.02,4.0])",
    "Gaussian::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[0.5,0.02,4.0])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "Exponential::bkgPass(x, alphaP[0.,-5.,5.])",
    "Exponential::bkgFail(x, alphaF[0.,-5.,5.])",
]


config=tnpConfig(
    data=samples['data2016a'],
    sim=samples['mi2016a'],
    sim_weight='totWeight',
    sim_genmatching='mcTrue',
    sim_genmass="mcMass",
    tree='tnpEleIDs/fitter_tree',
    mass="pair_mass",
    bins=bin_ID,
    expr='tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0 && el_q > 0 &&'+mtcut,
    test='passingCutBasedMedium94XV2',
    hist_nbins=80,
    hist_range=(50,130),
    data_method='fit',
    sim_method='count genmatching',
    fit_parameter=fit_nominal,
    fit_range=(60,120),
    #count_range=(70,110),
    systematic=[
        [{'fit_parameter':fit_altbkg}],
        [{'fit_parameter':fit_altsig}],
        [{'sim.replace':('DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos','DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8')}],
        [{'expr.replace':('tag_Ele_pt > 30','tag_Ele_pt > 35')}],
    ]
)

########### Configs ##############
Configs={}

Configs['2016a_MediumID_Plus']=config.clone(
    expr='tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0 && el_q > 0 &&'+mtcut,
    test='passingCutBasedMedium94XV2',
    bins=bin_ID,
)
Configs['2016a_TightID_SelQ_Plus']=config.clone(
    expr='tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0 && el_q > 0 &&'+mtcut,
    test='passingCutBasedTight94XV2 && el_3charge',
    bins=bin_ID,
)
Configs['2016a_Ele27_MediumID_Plus']=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='passingCutBasedMedium94XV2 && tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.4 && el_q*tag_Ele_q < 0 && el_q > 0',
    test='passHltEle27WPTightGsf',
    bins=bin_Ele27,
)
Configs['2016a_Ele23Leg1_MediumID_Plus']=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='passingCutBasedMedium94XV2 && tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.4 && el_q*tag_Ele_q < 0 && el_q > 0',
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match',
    bins=bin_Ele23,
)
Configs['2016a_Ele12Leg2_MediumID_Plus']=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='passingCutBasedMedium94XV2 && tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.4 && el_q*tag_Ele_q < 0 && el_q > 0',
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2',
    bins=bin_Ele12,
)
Configs['2016a_Ele27_TightID_SelQ_Plus']=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='passingCutBasedTight94XV2 && el_3charge passingCutBasedMedium94XV2 && tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.4 && el_q*tag_Ele_q < 0 && el_q > 0',
    test='passHltEle27WPTightGsf',
    bins=bin_Ele27,
)
Configs['2016a_Ele23Leg1_TightID_SelQ_Plus']=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='passingCutBasedTight94XV2 && el_3charge passingCutBasedMedium94XV2 && tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.4 && el_q*tag_Ele_q < 0 && el_q > 0',
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match',
    bins=bin_Ele23,
)
Configs['2016a_Ele12Leg2_TightID_SelQ_Plus']=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='passingCutBasedTight94XV2 && el_3charge && tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.4 && el_q*tag_Ele_q < 0 && el_q > 0',
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2',
    bins=bin_Ele12,
)

## cloning for each era
Configs_era={}
for key in Configs:
    if "2016a_" in key:
        Configs_era[key.replace("2016a_","2016b_")]=Configs[key].clone(data=samples["data2016b"],sim=samples["mi2016b"])
Configs.update(Configs_era)

## cloning for minus
Configs_minus={}
for key in Configs:
    if "_Plus" in key:
        Configs_minus[key.replace("_Plus","_Minus")]=Configs[key].clone({"expr.replace":("el_q > 0","el_q < 0")})
Configs.update(Configs_minus)
