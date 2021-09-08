import os,sys,math
import ROOT
from array import array
import time

##################
# Helper functions
##################

def mkdirp(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Check if a string can be a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def normalizeToEffectiveEntries(h):
    neffective=h.GetEffectiveEntries()
    integral=h.Integral()
    if neffective!=integral:
        h.Scale(neffective/integral)
    return

def removeNegativeBins(h):
    for i in range(h.GetNbinsX()+2):
        if (h.GetBinContent(i) < 0):
            h.SetBinContent(i,0)
            h.SetBinError(i,0)
    return

def GetAllHists(tdir):
    if type(tdir) is str:
        tdir=ROOT.TFile(tdir)
    hists=[]
    for key in tdir.GetListOfKeys():
        obj=key.ReadObj()
        if obj.InheritsFrom("TDirectory"):
            hists+=GetAllHists(obj)
        elif obj.InheritsFrom("TH1"):
            obj.SetDirectory(0)
            obj.SetName(key.GetMotherDir().GetPath().split(":")[1].lstrip("/")+"/"+key.GetName())
            hists+=[obj]
    hists.sort(key=lambda x: x.GetName())
    return hists
    
def postProcess(filename):
    tempname=filename.replace(".root","_TEMP.root")
    os.system("mv {} {}".format(filename,tempname))
    hists=GetAllHists(tempname)
    outfile=ROOT.TFile(filename,"recreate")
    for hist in hists:
        #normalizeToEffectiveEntries(hist)
        removeNegativeBins(hist)
        dirname=os.path.dirname(hist.GetName())
        basename=os.path.basename(hist.GetName())
        if not outfile.GetDirectory(dirname):
            outfile.mkdir(dirname)
        outfile.cd(dirname)
        hist.Write(basename)
    outfile.Close()
    os.system("rm "+tempname)
    return    

##################################
# To Fill Tag and Probe histograms
##################################

def makePassFailHistograms( configs, njob, ijob ):
    ROOT.TH1.SetDefaultSumw2()
    
    if not type(configs) is list:
        configs=[configs]

    ###############################
    # Read in Tag and Probe Ntuples
    ###############################
    tree = ROOT.TChain(configs[0].tree)
    if os.path.isdir(configs[0].sample):
        rootfiles=os.popen('find '+configs[0].sample+' -type f -name \'*.root\' | sort -V').read().split()
    elif os.path.isfile(configs[0].sample):
        rootfiles=[configs[0].sample]
    else:
        print "Error: {} doesn't exists".format(configs[0].sample)
        exit(1)
    if len(rootfiles)<njob:
        split_events=True
    else:
        split_events=False
        quotient=len(rootfiles)//njob
        remainder=len(rootfiles)%njob
        structure=[quotient+1]*remainder+[quotient]*(njob-remainder)
        if sum(structure) != len(rootfiles):
            print "Error: something wrong in rootfile splitting"
            exit(1)
        rootfiles=rootfiles[sum(structure[:ijob]):sum(structure[:ijob+1])]

    hist_file=configs[0].path+"/"+configs[0].hist_file.replace(".root",".d/job{}.root".format(ijob))

    for p in rootfiles:
        print ' adding rootfile: ', p
        tree.Add(p)

    #################################
    # Prepare hists, cuts and outfile
    #################################

    mkdirp(hist_file)
    outfile = ROOT.TFile(hist_file,'recreate')
    bins=configs[0].bins
    bin_cuts=[]
    hists=[[] for i in range(len(bins))]
    formulars=[[] for i in range(len(bins))]
    xs=[[] for i in range(len(bins))]

    for config in configs:
        for ib in range(len(bins)):
            bin_cuts+=[ROOT.TTreeFormula('{}{}_BinCut'.format(config.hist_prefix,bins[ib]['name']), bins[ib]['cut'], tree)]
            formular="({})".format(config.expr)
            if config.weight:
                formular+="*({})".format(config.weight)

            hists[ib]+=[ROOT.TH1D('{}{}_Pass'.format(config.hist_prefix,bins[ib]['name']),bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]
            formulars[ib]+=[ROOT.TTreeFormula('{}{}_Pass_Formula'.format(config.hist_prefix,bins[ib]['name']), "({})*({})".format(formular,config.test), tree)]
            xs[ib]+=[config.mass]

            hists[ib]+=[ROOT.TH1D('{}{}_Fail'.format(config.hist_prefix,bins[ib]['name']),bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]
            formulars[ib]+=[ROOT.TTreeFormula('{}{}_Fail_Formula'.format(config.hist_prefix,bins[ib]['name']), "({})*!({})".format(formular,config.test), tree)]
            xs[ib]+=[config.mass]

            if config.genmatching:
                hists[ib]+=[ROOT.TH1D('{}{}_Pass_genmatching'.format(config.hist_prefix,bins[ib]['name']),bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]
                formulars[ib]+=[ROOT.TTreeFormula('{}{}_Pass_Formula_genmatching'.format(config.hist_prefix,bins[ib]['name']), "({})*({})*({})".format(formular,config.test,config.genmatching), tree)]
                xs[ib]+=[config.mass]

                hists[ib]+=[ROOT.TH1D('{}{}_Fail_genmatching'.format(config.hist_prefix,bins[ib]['name']),bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]
                formulars[ib]+=[ROOT.TTreeFormula('{}{}_Fail_Formula_genmatching'.format(config.hist_prefix,bins[ib]['name']), "({})*!({})*({})".format(formular,config.test,config.genmatching), tree)]
                xs[ib]+=[config.mass]

            if config.genmass:
                hists[ib]+=[ROOT.TH1D('{}{}_Pass_genmass'.format(config.hist_prefix,bins[ib]['name']),bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]
                formulars[ib]+=[ROOT.TTreeFormula('{}{}_Pass_Formula_genmass'.format(config.hist_prefix,bins[ib]['name']), "({})*({})".format(formular,config.test), tree)]
                xs[ib]+=[config.genmass]

                hists[ib]+=[ROOT.TH1D('{}{}_Fail_genmass'.format(config.hist_prefix,bins[ib]['name']),bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]
                formulars[ib]+=[ROOT.TTreeFormula('{}{}_Fail_Formula_genmass'.format(config.hist_prefix,bins[ib]['name']), "({})*!({})".format(formular,config.test), tree)]
                xs[ib]+=[config.genmass]

                if config.genmatching:
                    hists[ib]+=[ROOT.TH1D('{}{}_Pass_genmatching_genmass'.format(config.hist_prefix,bins[ib]['name']),bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]
                    formulars[ib]+=[ROOT.TTreeFormula('{}{}_Pass_Formula_genmatching_genmass'.format(config.hist_prefix,bins[ib]['name']), "({})*({})*({})".format(formular,config.test,config.genmatching), tree)]
                    xs[ib]+=[config.genmass]

                    hists[ib]+=[ROOT.TH1D('{}{}_Fail_genmatching_genmass'.format(config.hist_prefix,bins[ib]['name']),bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]
                    formulars[ib]+=[ROOT.TTreeFormula('{}{}_Fail_Formula_genmatching_genmass'.format(config.hist_prefix,bins[ib]['name']), "({})*!({})*({})".format(formular,config.test,config.genmatching), tree)]
                    xs[ib]+=[config.genmass]

    print len(configs),len(bins),len(hists),len(hists[0])
    notify_list=ROOT.TList()
    for formular in bin_cuts+[f for ff in formulars for f in ff]:
        notify_list.Add(formular)
    tree.SetNotify(notify_list)

    ######################################
    # Deactivate branches and set adresses
    ######################################
    # Find out with variables are used to activate the corresponding branches
    replace_patterns = ['&', '|', '+', '-', 'max(', 'cos(', 'sqrt(', 'fabs(', 'abs(', '(', ')', '>', '<', '=', '!', '*', '/', '?', ':', ',']
    branches=""
    for config in configs:
        branches+=" {}".format(config.mass)
        branches+=" {}".format(config.expr)
        branches+=" {}".format(config.test)
        branches+=" {}".format(config.weight)
        branches+=" {}".format(config.genmatching)
        branches+=" {}".format(config.genmass)
        branches+=" {}".format(" ".join(config.vars))
        
    for p in replace_patterns:
        branches = branches.replace(p, ' ')

    branches = set([x for x in branches.split(" ") if x != '' and not is_number(x) and x!="None"])

    # Activate only branches which matter for the tag selection
    tree.SetBranchStatus("*", 0)
    for br in branches:
        tree.SetBranchStatus(br, 1)

    ################
    # Loop over Tree
    ################
    
    nevents = tree.GetEntries()
    startevent = 0
    endevent = nevents
    if split_events:        
        startevent=ijob*(nevents//njob)
        endevent=(ijob+1)*(nevents//njob)
        if ijob==njob-1: endevent=nevents
    
    frac_of_nevts = (endevent-startevent)/20

    print("Starting event loop to fill histograms..")

    ts=time.time()
    for index in range(startevent,endevent):
        if index >= nevents: break
        if (index-startevent) % frac_of_nevts == 0:
            print index-startevent,"/",endevent-startevent
            sys.stdout.flush()

        tree.GetEntry(index)
        for ib in range(len(bins)):
            if bin_cuts[ib].EvalInstance():
                for ih in range(len(hists[ib])):
                    weight = formulars[ib][ih].EvalInstance()
                    #print weight
                    if weight:
                        if math.isnan(weight):
                            print 'Error: nan weight!!! continue'
                            continue
                        hists[ib][ih].Fill(getattr(tree,xs[ib][ih]),weight)
                break

    te=time.time()
    print(te-ts)
    #####################
    # Deal with the Hists
    #####################
    print(len([h for hh in hists for h in hh]))
    for hist in [h for hh in hists for h in hh]:
        dirname=os.path.dirname(hist.GetName())
        basename=os.path.basename(hist.GetName())
        if not outfile.GetDirectory(dirname):
            outfile.mkdir(dirname)
        outfile.cd(dirname)
        hist.Write(basename)

    ##########
    # Clean up
    ##########
    outfile.Close()
    tree.Delete()
