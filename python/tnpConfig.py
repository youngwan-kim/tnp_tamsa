import os,copy
from array import array
import random as rd
import ROOT

class tnpConfig(object):
    def __init__(self,**kwargs):
        self.data_hist_file="hists_data.root"
        self.sim_hist_file="hists_sim.root"
        self.data_fit_file="fits_data.root"
        self.sim_fit_file="fits_sim.root"
        self.data_weight=None
        self.data_genmatching=None
        self.data_genmass=None
        self.name="s0m0"
        self.title="stat"
        self.hist_prefix=""
        self.option=""
        for key in kwargs:
            setattr(self,key,kwargs[key])

    def __str__(self):
        print_first=["name","isSim","path","sample","data","sim","weight","genmatching","genmass","tree","mass","vars","bins","expr","test","hist_file","hist_prefix","hist_nbins","hist_range","method","fit_file","fit_parameter","fit_range","count_range","systematic"]
        print_keys=[]
        for key in print_first:
            if hasattr(self,key) and getattr(self,key) is not None:
                print_keys+=[key]
            if hasattr(self,"data_"+key) and getattr(self,"data_"+key) is not None:
                print_keys+=["data_"+key]
            if hasattr(self,"sim_"+key) and getattr(self,"sim_"+key) is not None:
                print_keys+=["sim_"+key]
        for key in sorted(vars(self).keys()):
            if key in print_keys:
                continue
            if getattr(self,key) is None:
                continue
            print_keys+=[key]
        out=[]
        for key in print_keys:            
            if key in ["bins","data_bins","sim_bins"]:
                out+=["{} = {}".format(key.replace("bins","nbins"),len(getattr(self,key)))]
            elif key in ["systematic","data_systematic","sim_systematic"]:
                out+=["{} = ".format(key)]+["  "+str(s) for s in getattr(self,key)]
            elif key in ["fit_parameter","data_fit_parameter","sim_fit_parameter"]:
                out+=["{} = ".format(key)]+["  "+str(s) for s in getattr(self,key)]
            else:
                out+=["{} = {}".format(key,getattr(self,key))]

        return "\n".join(out)
        
    def __setattr__(self,key,val):
        if key=="fit_parameter":
            val=copy.deepcopy(val)
        elif key=="isSim":
            if val==False:
                self.sample=self.data
                for k in vars(self).keys():
                    if k.startswith("data_"):
                        setattr(self,k[len("data_"):],getattr(self,k))
            elif val==True:
                self.sample=self.sim
                for k in vars(self).keys():
                    if k.startswith("sim_"):
                        setattr(self,k[len("sim_"):],getattr(self,k))
        elif key=="systematic":
            if type(val) is not list:
                print "[tnpConfig.__setattr__] Error, 'systematic' should be a list"
                exit(1)
            for iset in range(len(val)):
                if type(val[iset]) is not list:
                    print "[tnpConfig.__setattr__] Error, 'systematic set {}' should be a list".format(iset)
                    exit(1)
                for imem in range(len(val[iset])):
                    if type(val[iset][imem]) is not dict:
                        print "[tnpConfig.__setattr__] Error, 'systematic set {} member {}' should be a dict".format(iset,imem)
                        exit(1)
            val=copy.deepcopy(val)
        elif key=="bins":
            bins=val
            listOfIndex = [[]]
            ### first map nD bins in a single list
            for iv in range(len(bins)):
                var = bins[iv]['var']
                if not bins[iv].has_key('type') or not bins[iv].has_key('bins'):
                    print 'bins is not complete for var %s' % var
                    return None
                nb1D = 1
                if   bins[iv]['type'] == 'float' :
                    nb1D = len(bins[iv]['bins'])-1
                elif bins[iv]['type'] == 'int' :
                    nb1D = len(bins[iv]['bins'])

                listOfIndexNew = []
                for ib_v in range(nb1D):
                    for index in listOfIndex:
                        listOfIndexNew+=[index+[ib_v]]
                listOfIndex=listOfIndexNew

            listOfBins = []
            nbins = len(listOfIndex)
            for ibin in range(nbins):
                ix=listOfIndex[ibin]
                ### make bin definition
                binCut   = None
                binName  = 'bin%02d'%ibin
                if nbins > 100   :  binName  = 'bin%03d'%ibin
                if nbins > 1000  :  binName  = 'bin%04d'%ibin
                if nbins > 10000 :  binName  = 'bin%d'%ibin

                binTitle = ''
                binVars = {}

                for iv in range(len(ix)):
                    var     = bins[iv]['var']
                    bins1D  = bins[iv]['bins']
                    varType = bins[iv]['type']
                    if varType == 'float' :
                        if binCut is None: 
                            binCut   = '(%s >= %f && %s < %f)' % (var,bins1D[ix[iv]],var,bins1D[ix[iv]+1])
                            binTitle = '%1.3f < %s < %1.3f'  % (bins1D[ix[iv]],var,bins1D[ix[iv]+1])
                        else:
                            binCut   = '%s * (%s >= %f && %s < %f)' % (binCut  ,var,bins1D[ix[iv]],var,bins1D[ix[iv]+1])
                            binTitle = '%s; %1.3f < %s < %1.3f'    % (binTitle,bins1D[ix[iv]],var,bins1D[ix[iv]+1])
                        binName  = '%s_%s_%1.2fTo%1.2f'  % (binName ,var.replace("/","_"),bins1D[ix[iv]],bins1D[ix[iv]+1])
                        binVars[var] = { 'min': bins1D[ix[iv]], 'max': bins1D[ix[iv]+1]}


                    if varType == 'int' :
                        if binCut is None: 
                            binCut   = '%s == %d' % (var,bins1D[ix[iv]])
                            binTitle = '%s = %d'  % (var,bins1D[ix[iv]])
                        else:
                            binCut   = '%s && %s == %d' % (binCut,var,bins1D[ix[iv]])
                            binTitle = '%s; %s = %d'    % (binTitle,var,bins1D[ix[iv]])
                        binName  = '%s_%sEq%d' % (binName ,var,bins1D[ix[iv]])
                        binVars[var] = { 'min': bins1D[ix[iv]], 'max': bins1D[ix[iv]]}

                    binName = binName.replace('-','m')
                    binName = binName.replace('.','p')

                listOfBins.append({'cut' : binCut, 'title': binTitle, 'name' : binName, 'vars' : binVars })

            listOfVars = []
            for iv in  range(len(bins)):
                listOfVars.append(bins[iv]['var'])

            self.vars=listOfVars
            val=listOfBins
        super(tnpConfig,self).__setattr__(key,val)
        return

    def get_hist(self,ibin,isPass,genmatching=False,genmass=False,random=None):
        this_hist_file=self.path+"/"+self.hist_file
        if not os.path.exists(this_hist_file):
            print "No file "+this_hist_file
            return None
        f=ROOT.TFile(this_hist_file)
        h=f.Get(self.get_histname(ibin,isPass,genmatching,genmass))
        if h:
            h.SetDirectory(0)
            if random:
                rd.seed(random)
                for ibin in range(h.GetNcells()):
                    val=rd.gauss(h.GetBinContent(ibin),h.GetBinError(ibin))
                    if val<0: 
                        val=0
                    h.SetBinContent(ibin,val)
        return h

    def get_histname(self,ibin,isPass,genmatching=False,genmass=False):
        histname=self.hist_prefix+self.bins[ibin]['name']
        if isPass:
            histname+="_Pass"
        else:
            histname+="_Fail"
        if genmatching:
            histname+="_genmatching"
        if genmass:
            histname+="_genmass"
        return histname

    def get_eff(self,ibin):
        f=ROOT.TFile("/".join([self.path,self.fit_file]))
        c=f.Get(self.name+"/"+self.bins[ibin]['name']+"_Canv")
        c.cd(1)
        words=c.GetPad(1).GetPrimitive("efficiency").GetLine(0).GetTitle().split()
        return float(words[2]),float(words[4])

    def make_eff_hist(self):
        ndim=min(len(self.vars),3)
        bins=[[] for i in range(ndim)]
        for iaxis in range(ndim):
            for b in self.bins:
                var=self.vars[iaxis]
                bins[iaxis]+=[b['vars'][var]['min'],b['vars'][var]['max']]
            bins[iaxis]=sorted(set(bins[iaxis]))
        histname="sim" if self.isSim==True else "data"
        histname+="_"+self.name
        if ndim==1:
            hist=ROOT.TH1D(histname,self.title,len(bins[0])-1,array('f',bins[0]))
        elif ndim==2:
            hist=ROOT.TH2D(histname,self.title,len(bins[0])-1,array('f',bins[0]),len(bins[1])-1,array('f',bins[1]))
        elif ndim==3:
            hist=ROOT.TH3D(histname,self.title,len(bins[0])-1,array('f',bins[0]),len(bins[1])-1,array('f',bins[1]),len(bins[2])-1,array('f',bins[2]))
        hist.SetDirectory(0)

        for ibin in range(len(self.bins)):
            b=self.bins[ibin]
            if ndim==1:
                x=0.5*(b['vars'][self.vars[0]]['min']+b['vars'][self.vars[0]]['max'])
                hist_ibin=hist.FindBin(x)
            elif ndim==2:
                x=0.5*(b['vars'][self.vars[0]]['min']+b['vars'][self.vars[0]]['max'])
                y=0.5*(b['vars'][self.vars[1]]['min']+b['vars'][self.vars[1]]['max'])
                hist_ibin=hist.FindBin(x,y)
            elif ndim==3:
                x=0.5*(b['vars'][self.vars[0]]['min']+b['vars'][self.vars[0]]['max'])
                y=0.5*(b['vars'][self.vars[1]]['min']+b['vars'][self.vars[1]]['max'])
                z=0.5*(b['vars'][self.vars[2]]['min']+b['vars'][self.vars[2]]['max'])
                hist_ibin=hist.FindBin(x,y,z)
            eff,err=self.get_eff(ibin)
            hist.SetBinContent(hist_ibin,eff)
            hist.SetBinError(hist_ibin,err)
        return hist

    def make_systematics(self,isSim=None):
        out=[[self.clone(isSim=isSim)]]
        for iset in range(len(self.systematic)):
            members=[]
            for imem in range(len(self.systematic[iset])):
                modifier=self.systematic[iset][imem]
                member=self.clone(modifier=modifier,isSim=isSim)
                member.name="s{}m{}".format(iset+1,imem) ## iset+1 since 0 is reserved for the nominal
                if "sim" in [key.split(".",1)[0] for key in modifier]:
                    member.sim_hist_file="hists_altsim.root"
                for key in ["tree","sim_weight","sim_genmatching","sim_genmass","mass","expr","hist_nbins","hist_range"]: 
                    if key in [k.split(".",1)[0] for k in modifier]:
                        member.hist_prefix="s{}m{}/".format(iset+1,imem) ## iset+1 since 0 is reserved for the nominal
                        break
                members+=[member]
            out+=[members]
        return out

    def make_hist_configs(self):
        systematics=self.make_systematics()
        systematics=[s for ss in systematics for s in ss]
        cands=[s.clone(isSim=False) for s in systematics]+[s.clone(isSim=True) for s in systematics]
        out=[]
        for cand in cands:
            if cand.hist_file not in [s[0].hist_file for s in out]:
                out+=[[cand]]
                continue
            for s in out:
                if cand.hist_file==s[0].hist_file:
                    if cand.hist_prefix not in [m.hist_prefix for m in s]:
                        s+=[cand]
                        break
        return out

    def clone(self,modifier=None,**kwargs):
        out=copy.deepcopy(self)
        if modifier:
            for key in modifier:
                if ".replace" in key:
                    key_=key.split(".",1)[0]
                    setattr(out,key_,getattr(out,key_).replace(modifier[key][0],modifier[key][1]))
                else:
                    setattr(out,key,modifier[key])
        for key in kwargs:
            setattr(out,key,kwargs[key])
        return out
