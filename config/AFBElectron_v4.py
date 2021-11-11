from tnpConfig import tnpConfig

############## samples ################
samples={
    'data2016a':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2016preVFP/data/SingleElectron',
    'mi2016a':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2016preVFP/mc/DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos',
    'mg2016a':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2016preVFP/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'data2016b':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2016postVFP/data/SingleElectron',
    'mi2016b':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2016postVFP/mc/DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos',
    'mg2016b':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2016postVFP/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'data2017':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2017/data/SingleElectron',
    'mi2017':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2017/mc/DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos',
    'mg2017':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2017/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
    'data2018':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2018/data/EGamma',
    'mi2018':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2018/mc/DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos',
    'mg2018':'/gv0/Users/hsseo/EgammaTnP/2021-08-24/UL2018/mc/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8',
}
############## binning ################
bin_ID = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5], 'title':'#eta_{SC}' },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 15, 20, 25, 30, 35, 40, 45, 70, 100, 500], 'title':'p_{T} [GeV]' },
]
bin_Ele35 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5], 'title':'#eta_{SC}' },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 31, 35, 37, 40, 45, 70, 100, 500], 'title':'p_{T} [GeV]' },
]
bin_Ele32 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5], 'title':'#eta_{SC}' },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 28, 31, 33, 35, 38, 40, 45, 70, 100, 500], 'title':'p_{T} [GeV]' },
]
bin_Ele28 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5], 'title':'#eta_{SC}' },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 24, 28, 30, 32, 35, 40, 45, 70, 100, 500], 'title':'p_{T} [GeV]' },
]
bin_Ele27 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5], 'title':'#eta_{SC}' },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 23, 26, 28, 30, 32, 35, 40, 45, 70, 100, 500], 'title':'p_{T} [GeV]' },
]
bin_Ele23 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5], 'title':'#eta_{SC}' },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 19, 23, 25, 27, 30, 35, 40, 45, 70, 100, 500], 'title':'p_{T} [GeV]' },
]
bin_Ele12 = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.1, -1.80, -1.566, -1.4442, -1.1, -0.8, -0.4, 0.0, 0.4, 0.8, 1.1, 1.4442, 1.566, 1.80, 2.1, 2.5], 'title':'#eta_{SC}' },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10, 12, 15, 18, 20, 25, 30, 35, 40, 45, 70, 100, 500], 'title':'p_{T} [GeV]' },
]


############### Expr ################
## selection
tight_mcTrue='mcTrue && el_et/mc_probe_et>0.9 && el_et/mc_probe_et < 1.1 && (el_eta-mc_probe_eta)*(el_eta-mc_probe_eta)+(el_phi-mc_probe_phi)*(el_phi-mc_probe_phi)<0.01'
medium_mcTrue='mcTrue && el_et/mc_probe_et>0.8 && el_et/mc_probe_et < 1.2 && (el_eta-mc_probe_eta)*(el_eta-mc_probe_eta)+(el_phi-mc_probe_phi)*(el_phi-mc_probe_phi)<0.01'
loose_mcTrue='mcTrue && el_et/mc_probe_et>0.5 && el_et/mc_probe_et < 1.5 && (el_eta-mc_probe_eta)*(el_eta-mc_probe_eta)+(el_phi-mc_probe_phi)*(el_phi-mc_probe_phi)<0.01'

## fits
fit_nominal = [
    "HistPdf::sigPhysPass(x,histPass_genmatching,2)",
    "HistPdf::sigPhysFail(x,histFail_genmatching,2)",
    "Gaussian::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[0.02,0.02,4.0])",
    "Gaussian::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[0.02,0.02,4.0])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "RooCMSShape::bkgPass(x,acmsP[60.,50.,80.],betaP[0.05,0.01,0.08],gammaP[0.1, 0, 1],peakP[90.0])",
    "RooCMSShape::bkgFail(x,acmsF[60.,50.,80.],betaF[0.05,0.01,0.08],gammaF[0.1, 0, 1],peakF[90.0])",
]

fit_altsig = [
    "HistPdf::sigPhysPass(x,histPass_genmatching_genmass,2)",
    "HistPdf::sigPhysFail(x,histFail_genmatching_genmass,2)",
    "RooCBShape::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[1,0.3,10.0],alphaP[2.0,1.2,3.5],nP[3,-5,5])",
    "RooCBShape::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[1,0.3,10.0],alphaF[2.0,1.2,3.5],nF[3,-5,5])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "Fit sigPass histPass_genmatching",
    "Fit sigFail histFail_genmatching",
    "SetConstant alphaP nP alphaF nF",
    "RooCMSShape::bkgPass(x,acmsP[60.,50.,80.],betaP[0.05,0.01,0.08],gammaP[0.1, 0, 1],peakP[90.0])",
    "RooCMSShape::bkgFail(x,acmsF[60.,50.,80.],betaF[0.05,0.01,0.08],gammaF[0.1, 0, 1],peakF[90.0])",
]

fit_altbkg = [
    "HistPdf::sigPhysPass(x,histPass_genmatching,2)",
    "HistPdf::sigPhysFail(x,histFail_genmatching,2)",
    "Gaussian::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[0.02,0.02,4.0])",
    "Gaussian::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[0.02,0.02,4.0])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "Exponential::bkgPass(x, alphaP[0.,-5.,5.])",
    "Exponential::bkgFail(x, alphaF[0.,-5.,5.])",
]

fit_nominal_random = [
    "HistPdf::sigPhysPass(x,histPass_genmatching_random,2)",
    "HistPdf::sigPhysFail(x,histFail_genmatching_random,2)",
    "Gaussian::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[0.02,0.02,4.0])",
    "Gaussian::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[0.02,0.02,4.0])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "RooCMSShape::bkgPass(x,acmsP[60.,50.,80.],betaP[0.05,0.01,0.08],gammaP[0.1, 0, 1],peakP[90.0])",
    "RooCMSShape::bkgFail(x,acmsF[60.,50.,80.],betaF[0.05,0.01,0.08],gammaF[0.1, 0, 1],peakF[90.0])",
]

fit_altsig_random = [
    "HistPdf::sigPhysPass(x,histPass_genmatching_genmass_random,2)",
    "HistPdf::sigPhysFail(x,histFail_genmatching_genmass_random,2)",
    "RooCBShape::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[1,0.3,10.0],alphaP[2.0,1.2,3.5],nP[3,-5,5])",
    "RooCBShape::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[1,0.3,10.0],alphaF[2.0,1.2,3.5],nF[3,-5,5])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "Fit sigPass histPass_genmatching",
    "Fit sigFail histFail_genmatching",
    "SetConstant alphaP nP alphaF nF",
    "RooCMSShape::bkgPass(x,acmsP[60.,50.,80.],betaP[0.05,0.01,0.08],gammaP[0.1, 0, 1],peakP[90.0])",
    "RooCMSShape::bkgFail(x,acmsF[60.,50.,80.],betaF[0.05,0.01,0.08],gammaF[0.1, 0, 1],peakF[90.0])",
]

fit_altbkg_random = [
    "HistPdf::sigPhysPass(x,histPass_genmatching_random,2)",
    "HistPdf::sigPhysFail(x,histFail_genmatching_random,2)",
    "Gaussian::sigResPass(x,meanP[-0.0,-5.0,5.0],sigmaP[0.02,0.02,4.0])",
    "Gaussian::sigResFail(x,meanF[-0.0,-5.0,5.0],sigmaF[0.02,0.02,4.0])",
    "FCONV::sigPass(x, sigPhysPass , sigResPass)",
    "FCONV::sigFail(x, sigPhysFail , sigResFail)",
    "Exponential::bkgPass(x, alphaP[0.,-5.,5.])",
    "Exponential::bkgFail(x, alphaF[0.,-5.,5.])",
]



########### Configs ##############
Configs={}

#### 2016a
## ID
config=tnpConfig(
    data=samples['data2016a'],
    sim=samples['mi2016a'],
    sim_weight='totWeight',
    sim_maxweight=10000.,
    sim_genmatching=loose_mcTrue,
    sim_genmass="mcMass",
    tree='tnpEleIDs/fitter_tree',
    mass="pair_mass",
    bins=bin_ID,
    expr='( tag_Ele_pt>30 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passingCutBasedMedium94XV2',
    hist_nbins=98,
    hist_range=(52,150),
    method="fit",
    fit_parameter=fit_nominal,
    fit_range=(60,140),
    systematic=[
        [{'title':'altbkg','fit_parameter':fit_altbkg}],
        [{'title':'altsig','fit_parameter':fit_altsig}],
        [{'title':'alttag','expr.replace':('tag_Ele_pt>30','tag_Ele_pt>35')}],
        [{'title':'altmc','sim.replace':('DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos','DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8')}],
        [{'title':'altsub','expr.replace':('(el_q*tag_Ele_q<0?1.:-1.)','(el_q*tag_Ele_q<0?1.:-0.6)')}],
        [{'title':'nogenmatching','sim_genmatching':"(1)"}],
    ],
    option="fix_ptbelow20",
)
Configs['2016a_MediumID_Plus']=config.clone(test='passingCutBasedMedium94XV2')
Configs['2016a_TightID_SelQ_Plus']=config.clone(test='passingCutBasedTight94XV2&&el_3charge')

## trigger
config=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='( passingCutBasedMedium94XV2 && tag_Ele_pt>30 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
)
Configs['2016a_Ele23Leg1_MediumID_Plus']=config.clone(
    bins=bin_Ele23,
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match&&el_l1et>L1ThesholdHLTEle23Ele12CaloIdLTrackIdLIsoVL',
)
Configs['2016a_Ele12Leg2_MediumID_Plus']=config.clone(
    bins=bin_Ele12,
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2',
)
Configs['2016a_Ele27_MediumID_Plus']=config.clone(
    bins=bin_Ele27,
    test='passHltEle27WPTightGsf',
)
Configs['2016a_Ele27_TightID_SelQ_Plus']=config.clone(
    bins=bin_Ele27,
    expr='( passingCutBasedTight94XV2&&el_3charge && tag_Ele_pt>30 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle27WPTightGsf',
)

#### 2016b
Configs_2016b={}
for key in Configs:
    if "2016a_" in key:
        Configs_2016b[key.replace("2016a_","2016b_")]=Configs[key].clone(data=samples["data2016b"],sim=samples["mi2016b"])
Configs.update(Configs_2016b)

#### 2017
## ID
config=config.clone(
    data=samples['data2017'],
    sim=samples['mi2017'],
    tree='tnpEleIDs/fitter_tree',
    expr='( tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    systematic=[
        [{'title':'altbkg','fit_parameter':fit_altbkg}],
        [{'title':'altsig','fit_parameter':fit_altsig}],
        [{'title':'alttag','expr.replace':('tag_Ele_pt>35','tag_Ele_pt>38')}],
        [{'title':'altmc','sim.replace':('DYJetsToEE_M-50_massWgtFix_TuneCP5_13TeV-powhegMiNNLO-pythia8-photos','DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8')}],
        [{'title':'altsub','expr.replace':('(el_q*tag_Ele_q<0?1.:-1.)','(el_q*tag_Ele_q<0?1.:-0.6)')}],
        [{'title':'nogenmatching','sim_genmatching':"(1)"}],
    ],
)
Configs['2017_MediumID_Plus']=config.clone(test='passingCutBasedMedium94XV2')
Configs['2017_TightID_SelQ_Plus']=config.clone(test='passingCutBasedTight94XV2&&el_3charge')

## trigger
config=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='( passingCutBasedMedium94XV2 && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
)
Configs['2017_Ele23Leg1_MediumID_Plus']=config.clone(
    bins=bin_Ele23,
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1&&el_l1et>L1ThesholdHLTEle23Ele12CaloIdLTrackIdLIsoVL',
)
Configs['2017_Ele12Leg2_MediumID_Plus']=config.clone(
    bins=bin_Ele12,
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2',
)
Configs['2017_Ele32DoubleEG_MediumID_Plus']=config.clone(
    bins=bin_Ele32,
    test='passHltEle32DoubleEGWPTightGsf&&passEGL1SingleEGOr',
)
Configs['2017_Ele27_MediumID_Plus']=config.clone(
    bins=bin_Ele27,
    expr='( PrescaleHLTEle27WPTightGsf && passingCutBasedMedium94XV2 && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle27WPTightGsf',
)
Configs['2017_Ele32_MediumID_Plus']=config.clone(
    bins=bin_Ele32,
    expr='( PrescaleHLTEle32WPTightGsf && passingCutBasedMedium94XV2 && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle32WPTightGsf',
)
Configs['2017_Ele27Or_MediumID_Plus']=config.clone(
    bins=bin_Ele27,
    expr='( passingCutBasedMedium94XV2 && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle27WPTightGsf||passHltEle32WPTightGsf',
)
Configs['2017_Ele32DoubleEG_TightID_SelQ_Plus']=config.clone(
    bins=bin_Ele32,
    expr='( passingCutBasedTight94XV2&&el_3charge && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle32DoubleEGWPTightGsf&&passEGL1SingleEGOr',
)
Configs['2017_Ele27_TightID_SelQ_Plus']=config.clone(
    bins=bin_Ele27,
    expr='( PrescaleHLTEle27WPTightGsf && passingCutBasedTight94XV2&&el_3charge && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle27WPTightGsf',
)
Configs['2017_Ele32_TightID_SelQ_Plus']=config.clone(
    bins=bin_Ele32,
    expr='( PrescaleHLTEle32WPTightGsf && passingCutBasedTight94XV2&&el_3charge && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle32WPTightGsf',
)
Configs['2017_Ele27Or_TightID_SelQ_Plus']=config.clone(
    bins=bin_Ele27,
    expr='( passingCutBasedTight94XV2&&el_3charge && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle27WPTightGsf||passHltEle32WPTightGsf',
)

#### 2018
## ID
config=config.clone(
    data=samples['data2018'],
    sim=samples['mi2018'],
    tree='tnpEleIDs/fitter_tree',
    expr='( tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
)
Configs['2018_MediumID_Plus']=config.clone(test='passingCutBasedMedium94XV2')
Configs['2018_TightID_SelQ_Plus']=config.clone(test='passingCutBasedTight94XV2&&el_3charge')

## trigger
config=config.clone(
    tree='tnpEleTrig/fitter_tree',
    expr='( passingCutBasedMedium94XV2 && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
)
Configs['2018_Ele23Leg1_MediumID_Plus']=config.clone(
    bins=bin_Ele23,
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1&&el_l1et>L1ThesholdHLTEle23Ele12CaloIdLTrackIdLIsoVL',
)
Configs['2018_Ele12Leg2_MediumID_Plus']=config.clone(
    bins=bin_Ele12,
    test='passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg2',
)
Configs['2018_Ele32_MediumID_Plus']=config.clone(
    bins=bin_Ele32,
    test='passHltEle32WPTightGsf',
)
Configs['2018_Ele28_MediumID_Plus']=config.clone(
    bins=bin_Ele28,
    expr='( PrescaleHLTEle28WPTightGsf && passingCutBasedMedium94XV2 && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle28WPTightGsf',
)
Configs['2018_Ele28Or_MediumID_Plus']=config.clone(
    bins=bin_Ele28,
    expr='( passingCutBasedMedium94XV2 && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle28WPTightGsf||passHltEle32WPTightGsf',
)
Configs['2018_Ele32_TightID_SelQ_Plus']=config.clone(
    bins=bin_Ele32,
    expr='( passingCutBasedTight94XV2&&el_3charge && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle32WPTightGsf',
)
Configs['2018_Ele28_TightID_SelQ_Plus']=config.clone(
    bins=bin_Ele28,
    expr='( PrescaleHLTEle28WPTightGsf && passingCutBasedTight94XV2&&el_3charge && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle28WPTightGsf',
)
Configs['2018_Ele28Or_TightID_SelQ_Plus']=config.clone(
    bins=bin_Ele28,
    expr='( passingCutBasedTight94XV2&&el_3charge && tag_Ele_pt>35 && el_q>0 )*(el_q*tag_Ele_q<0?1.:-1.)',
    test='passHltEle28WPTightGsf||passHltEle32WPTightGsf',
)

#### minus
Configs_minus={}
for key in Configs:
    if "_Plus" in key:
        Configs_minus[key.replace("_Plus","_Minus")]=Configs[key].clone({"expr.replace":("el_q>0","el_q<0")})
Configs.update(Configs_minus)

if __name__=="__main__":
    for key in sorted(Configs.keys()):
        print key
