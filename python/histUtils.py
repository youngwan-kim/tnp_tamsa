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

def smearNegativeBins(h):
    for i in range(1,h.GetNbinsX()+1):
        if h.GetBinContent(i) < 0:
            remain_content=abs(h.GetBinContent(i))
            remain_error2=h.GetBinError(i)**2
            targets=[]
            for j in range(1,7):
                if h.GetBinContent(i+j)>0: targets+=[i+j]
                if h.GetBinContent(i-j)>0: targets+=[i-j]
                if len(targets): break
            if len(targets)==0: continue            
            target_content=sum([h.GetBinContent(k) for k in targets])
            smear_content=min(target_content,remain_content)
            smear_error2=remain_error2*smear_content/remain_content
            smear_weights=[h.GetBinContent(k)/target_content for k in targets]
            for j in range(len(targets)):
                k=targets[j]
                h.SetBinContent(k,h.GetBinContent(k)-smear_content*smear_weights[j])
                h.SetBinError(k,math.sqrt(h.GetBinError(k)**2+smear_error2*smear_weights[j]))
            remain_content=remain_content-smear_content
            remain_error2=remain_error2-smear_error2
            if remain_error2<0 and abs(remain_error2)<1e-6: remain_error2=0
            h.SetBinContent(i,-remain_content)
            h.SetBinError(i,math.sqrt(remain_error2))
    return

def removeNegativeBins(h):
    for i in range(h.GetNbinsX()+2):
        if h.GetBinContent(i) < 0:
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
        for i in range(10):
            smearNegativeBins(hist)
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
        rootfiles=[rootfiles[i] for i in range(len(rootfiles)) if i%njob==ijob]

    hist_file=configs[0].path+"/"+configs[0].hist_file.replace(".root",".d/job{}.root".format(ijob))

    for p in rootfiles:
        print ' adding rootfile: ', p
        tree.Add(p)

    #################################
    # Prepare hists, cuts and outfile
    #################################

    mkdirp(os.path.dirname(hist_file))
    outfile = ROOT.TFile(hist_file,'recreate')
    bins=configs[0].bins
    bin_formulars=[None]*len(bins)
    expr_formulars=[None]*len(configs)
    hists=[[[] for i in range(len(bins))] for i in range(len(configs))]
    xs=[[[] for i in range(len(bins))] for i in range(len(configs))]
    weight_formulars=[[[] for i in range(len(bins))] for i in range(len(configs))]
    
    for ib in range(len(bins)):
        bin_formulars[ib]=ROOT.TTreeFormula('{}_BinCut'.format(bins[ib]['name']), bins[ib]['cut'], tree)

    for ic in range(len(configs)):
        config=configs[ic]
        expr_formulars[ic]=ROOT.TTreeFormula('{}_expr'.format(config.hist_prefix), config.expr, tree)
        for ib in range(len(bins)):
            for isPass,genmatching,genmass in [[i%2==0,(i//2)%2==1,(i//4)%2==1] for i in range(2**3)]:
                if not config.genmatching and genmatching: continue
                if not config.genmass and genmass: continue
                histname=config.get_histname(ib,isPass=isPass,genmatching=genmatching,genmass=genmass)
                hists[ic][ib]+=[ROOT.TH1D(histname,bins[ib]['title'],config.hist_nbins,config.hist_range[0],config.hist_range[1])]

                if isPass: 
                    weight="({})".format(config.test)
                else:
                    weight="!({})".format(config.test)
                if genmatching:
                    weight+="*({})".format(config.genmatching)
                if config.weight:
                    weight+="*({})".format(config.weight)                    
                weight_formulars[ic][ib]+=[ROOT.TTreeFormula('{}_weight'.format(histname), weight, tree)]

                if genmass:
                    xs[ic][ib]+=[config.genmass]
                else:
                    xs[ic][ib]+=[config.mass]

    print len(configs),len(bins),len(hists),len(hists[0]),len(hists[0][0])
    notify_list=ROOT.TList()
    for formular in expr_formulars+bin_formulars+[f for fff in weight_formulars for ff in fff for f in ff]:
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
        for ic in range(len(configs)):
            expr=expr_formulars[ic].EvalInstance()
            if not expr: continue
            for ib in range(len(bins)):
                bincut=bin_formulars[ib].EvalInstance()
                if not bincut: continue
                for ih in range(len(hists[ic][ib])):
                    weight = weight_formulars[ic][ib][ih].EvalInstance()
                    if not weight: continue
                    if math.isnan(weight):
                        print 'Error: nan weight!!! continue'
                        continue
                    if math.isinf(weight):
                        print 'Error: inf weight!!! continue'
                        continue
                    if hasattr(configs[ic],"maxweight") and abs(weight)>configs[ic].maxweight:
                        weight=math.copysign(configs[ic].maxweight,weight)
                    hists[ic][ib][ih].Fill(getattr(tree,xs[ic][ib][ih]),expr*bincut*weight)
                break

    te=time.time()
    print(te-ts)
    #####################
    # Deal with the Hists
    #####################
    print(len([h for hhh in hists for hh in hhh for h in hh]))
    for hist in [h for hhh in hists for hh in hhh for h in hh]:
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
