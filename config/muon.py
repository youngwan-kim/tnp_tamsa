from tnpConfig import tnpConfig

############## samples ################
muondir = '/data9/Users/wonjun/public/TnP_Trees/Spark_Trees/'
samples={
    'data2016a':muondir+'TnPTreeZ_21Feb2020_UL2016_HIPM_SingleMuon_MiniAOD_Run2016BCDEFv1_Skimmed.root',
    'mi2016a':muondir+'TnPTreeZ_106XSummer20_UL16MiniAODAPV_DYJetsToMuMu_M50_powhegMiNNLO.root',
    'mg2016a':muondir+'TnPTreeZ_106XSummer20_UL16MiniAODAPV_DYJetsToLL_M50_MadgraphMLM.root',
    'data2016b':muondir+'TnPTreeZ_21Feb2020_UL2016_SingleMuon_MiniAOD_Run2016FGHv1_Skimmed.root',
    'mi2016b':muondir+'TnPTreeZ_106XSummer20_UL16MiniAOD_DYJetsToMuMu_M50_powhegMiNNLO.root',
    'mg2016b':muondir+'TnPTreeZ_106XSummer20_UL16MiniAOD_DYJetsToLL_M50_MadgraphMLM.root',
    'data2017':muondir+'TnPTreeZ_09Aug2019_UL2017_SingleMuon_Run2017BCDEFv1_Skimmed.root',
    'mi2017':muondir+'TnPTreeZ_106XSummer20_UL17MiniAOD_DYJetsToMuMu_M50_massWgtFix_powhegMiNNLO.root',
    'mg2017':muondir+'TnPTreeZ_106XSummer20_UL17MiniAOD_DYJetsToLL_M50_MadgraphMLM.root',
}
############## binning ################
binnings={
    'Mu8':[              ### For ID or Mu8
        { 'var' : 'probe_eta' , 'type': 'float', 'bins': [round(i/10.,2) for i in range(-24,25)] },
        { 'var' : 'probe_pt' , 'type': 'float', 'bins': [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 120] },
    ],
    'Mu17':[            ### For Mu17
        { 'var' : 'probe_eta' , 'type': 'float', 'bins': [round(i/10.,2) for i in range(-24,25)] },
        { 'var' : 'probe_pt' , 'type': 'float', 'bins': [14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 60, 120] },
    ],
    'IsoMu24':[            ### For IsoMu24
        { 'var' : 'probe_eta' , 'type': 'float', 'bins': [round(i/10.,2) for i in range(-24,25)] },
        { 'var' : 'probe_pt' , 'type': 'float', 'bins': [20, 22, 24, 26, 28, 30, 35, 40, 45, 50, 60, 120] },
    ],
    'IsoMu27':[          ### For IsoMu27 (Regacy 2017)
        { 'var' : 'eta' , 'type': 'float', 'bins': [round(i/10.,2) for i in range(-24,25)] },
        { 'var' : 'pt' , 'type': 'float', 'bins': [29, 32, 35, 40, 45, 50, 60, 120] },
    ],
}
############### Expr ################
## variables
IsoMu24 =   'hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09'
IsoTkMu24 = 'hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09'
Mu17Mu8_17leg =     'probe_hltL3fL1sDoubleMu114L1f0L2f10OneMuL3Filtered17 && probe_hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4'
Mu17TkMu8_17leg =   'probe_hltL3fL1sDoubleMu114L1f0L2f10L3Filtered17 && probe_hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4'
TkMu17TkMu8_17leg = 'probe_hltL3fL1sDoubleMu114TkFiltered17Q && probe_hltDiMuonTrk17Trk8RelTrkIsoFiltered0p4'
Mu17Mu8_8leg =      'probe_hltL3pfL1sDoubleMu114ORDoubleMu125L1f0L2pf0L3PreFiltered8 && probe_hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4'
Mu17TkMu8_8leg =    'probe_hltDiMuonGlbFiltered17TrkFiltered8 && probe_hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4'
TkMu17TkMu8_8leg =  'probe_hltDiTkMuonTkFiltered17TkFiltered8 && probe_hltDiMuonTrk17Trk8RelTrkIsoFiltered0p4'
tag_PFIso = '(tag_pfIso04_charged + max(0, tag_pfIso04_neutral+tag_pfIso04_photon-(0.5 * tag_pfIso04_sumPU)))/tag_pt'

## fits


config_id=tnpConfig(
    data=samples['data2016a'],
    sim=samples['mi2016a'],
    sim_weight='genWeight',
    sim_genmatching='tag_isMatchedGen && probe_isMatchedGen',
    sim_genmass="genMass",
    tree='muon/Events',
    mass="pair_mass",
    bins=binnings['Mu8'],
    expr='tag_'+IsoMu24+' && tag_pt > 26 && tag_isTight && '+tag_PFIso+' < 0.15 && tag_charge*probe_charge < 0 && pair_dR > 0.3 && probe_isTracker && probe_charge > 0',
    test='probe_CutBasedIdMedium && probe_TkIsoLoose',
    hist_nbins=80,
    hist_range=(60,140),
    method='fit',
    fit_parameter= [
        "HistPdf::sigPhysPass(x,histPass_genmatching_genmass,2)",
        "HistPdf::sigPhysFail(x,histFail_genmatching_genmass,2)",
        "Gaussian::sigResPass(x,meanGaussP[0.0,-5.0,5.0],sigmaGaussP[0.8, 0.5,3.5])",
        "Gaussian::sigResFail(x,meanGaussF[0.0, -5.0,5.0],sigmaGaussF[0.7, 0.5,3.5])",
        "FCONV::sigPass(x, sigPhysPass , sigResPass)",
        "FCONV::sigFail(x, sigPhysFail , sigResFail)",
        "Exponential::bkgPass(x, aExpoP[-0.1, -1,0.1])",
        "Exponential::bkgFail(x, aExpoF[-0.1, -1,0.1])",
    ],
    fit_range=(70,130),
    count_range=(81,101),
    systematic=[
        [{'fit_range':(60,130),'count_range':(76,106)},{'fit_range':(70,120),'count_range':(86,96)}],
        [{'expr.replace':(tag_PFIso+' < 0.15',tag_PFIso+' < 0.20')},{'expr.replace':(tag_PFIso+' < 0.15',tag_PFIso+' < 0.10')}],
        [{'sim.replace':('DYJetsToMuMu_M50_powhegMiNNLO.root','DYJetsToLL_M50_MadgraphMLM.root'),'sim.replace':('DYJetsToMuMu_M50_massWgtFix_powhegMiNNLO.root','DYJetsToLL_M50_MadgraphMLM.root')}],
        [{'hist_nbins':60},{'hist_nbins':100}],
    ]
)

config_trigger=config_id.clone(
    expr='tag_'+IsoMu24+' && tag_pt > 26 && tag_isTight && '+tag_PFIso+' < 0.15 && tag_charge*probe_charge < 0 && pair_dR > 0.3 && probe_CutBasedIdMedium && probe_TkIsoLoose && probe_charge > 0',
    test='probe_'+IsoMu24+' || probe_'+IsoTkMu24,
    method='count',
    count_range=(81,101),
    systematic=[
        [{'count_range':(76,106)},{'count_range':(86,96)}],
        [{'expr.replace':(tag_PFIso+' < 0.15',tag_PFIso+' < 0.20')},{'expr.replace':(tag_PFIso+' < 0.15',tag_PFIso+' < 0.10')}],
        [{'sim.replace':('DYJetsToMuMu_M50_powhegMiNNLO.root','DYJetsToLL_M50_MadgraphMLM.root'),'sim.replace':('DYJetsToMuMu_M50_massWgtFix_powhegMiNNLO.root','DYJetsToLL_M50_MadgraphMLM.root')}]
    ]
)

########### Configs ##############
Configs={}

Configs['2016a_ID_Plus']=config_id.clone(
    test='probe_CutBasedIdMedium && probe_TkIsoLoose',
    bins=binnings['Mu8'],
)
Configs['2016a_IsoMu24_Plus']=config_trigger.clone(
    test='probe_'+IsoMu24+' || probe_'+IsoTkMu24,
    bins=binnings['IsoMu24'],
)
Configs['2016a_Mu17_Plus']=config_trigger.clone(
    test=Mu17Mu8_17leg+' || '+Mu17TkMu8_17leg,
    bins=binnings['Mu17'],
)
Configs['2016a_Mu8_Plus']=config_trigger.clone(
    test=Mu17Mu8_8leg+' || '+Mu17TkMu8_8leg,
    bins=binnings['Mu8'],
)
## cloning for 2016b
Configs_2016b={}
for key in Configs:
    Configs_era[key.replace("2016a_","2016b_")]=Configs[key].clone(data=samples["data2016b"],sim=samples["mi2016b"])
Configs.update(Configs_era)

## cloning for minus
Configs_minus={}
for key in Configs:
    Configs_minus[key.replace("_Plus","_Minus")]=Configs[key].clone({"expr.replace":("probe_charge > 0","probe_charge < 0")})
Configs.update(Configs_minus)
