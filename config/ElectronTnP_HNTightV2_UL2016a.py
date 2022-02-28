import tnpSampleDef as tnpSamples

samplesDef = {
    'data'   : tnpSamples.HNtypeI['data2016a'].clone(),
    'mcNom'  : tnpSamples.HNtypeI['mg2016a'].clone(),
    'mcAlt'  : tnpSamples.HNtypeI['amc2016a'].clone(),
    'tagSel' : tnpSamples.HNtypeI['mg2016a'].clone(),
}
#samplesDef["mcNom"].set_cut(tight_mcTrue)
#samplesDef['mcAlt'].set_cut(tight_mcTrue)
samplesDef['tagSel'].rename('mcAltSel_'+samplesDef['tagSel'].name)
#samplesDef['tagSel'].set_cut('tag_Ele_pt > 35 && '+tight_mcTrue)
samplesDef['tagSel'].set_cut('(tag_Ele_pt > 37 && el_idCutForTrigger == 1 && el_1overEminus1overP < 0.01)')

baseOutDir = 'results/HNtypeIElectronID_UL2016a/'
tnpTreeDir = 'tnpEleIDs'
HNID = '(passingCutBasedTight94XV2 == 1 && el_isPOGIP2D == 1 && el_sip < 4.0 && el_idCutForTrigger == 1 && el_dPhiIn < 0.04 && el_isoCutForTrigger == 1 && el_3charge == 1 && el_idCutForTrigger == 1 && el_1overEminus1overP < 0.01)'

flags = {
    'MediumID' : '(passingCutBasedMedium94XV2 == 1)',
    'TightID'  : '(passingCutBasedTight94XV2  == 1)',
    'TightID_Selective'  : '(passingCutBasedTight94XV2  == 1 && el_3charge)',
    'HNTightV2' : HNID,
}


#############################################################
########## bining definition  [can be nD bining]
#############################################################

biningDef = [
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
    ## Official bins for Run2 legacy : [10,20,35,50,100,200,500]
    ## Official bins for Run2 UL : [10,20,35,50,100,500]
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [10,20,35,50,100,500] },
]


#############################################################
########## Cuts definition for all samples
#############################################################

cutBase = 'tag_Ele_pt > 34 && abs(tag_sc_eta) < 2.1 && el_q*tag_Ele_q < 0 && tag_Ele_isPOGIP2D == 1 && tag_Ele_sip < 4.0 && tag_Ele_idCutForTrigger == 1 && tag_Ele_dPhiIn < 0.04 && tag_Ele_isoCutForTrigger == 1 && tag_Ele_3charge == 1'
additionalCutBase = {}
# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts={}
for i in range(10): ### applied for pT < 20 GeV
    additionalCuts[i]='tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45'


#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.02,4.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.02,4.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]

tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.02,4.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.02,4.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]

