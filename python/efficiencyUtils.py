import math,copy
import ROOT

def add_error_maxdiff(nominal,syss):
    for ibin in range(nominal.GetNcells()):
        maxdiff=0
        for sys in syss:
            diff=abs(sys.GetBinContent(ibin)-nominal.GetBinContent(ibin))
            if diff>maxdiff: maxdiff=diff
        nominal.SetBinError(ibin,math.sqrt(nominal.GetBinError(ibin)**2+maxdiff**2))
    return nominal

def make_combined_hist(hists,stat=True):
    ## s0m0 is nominal one with stat err.
    ## clone with name data_s0m0 -> data, sim_s0m0 -> sim, sf_s0m0 -> sf
    combined=hists[0][0].Clone(hists[0][0].GetName().split("_",1)[0])
    combined.SetDirectory(0)
    if not stat:
        for ibin in range(combined.GetNcells()):
            combined.SetBinError(ibin,0.)
        combined.SetName(combined.GetName()+"_sys")
    for members in hists:
        add_error_maxdiff(combined,members)
    return combined

class Efficiency(object):
    def __init__(self,val=None,err=None):
        self.val=val
        self.err=err
        return

    def __add__(self,other):
        n1=self.GetEffectiveEntries()
        n2=other.GetEffectiveEntries()
        if n1==0: return other.clone()
        if n2==0: return self.clone()
        result=self.clone()
        w1=n1/(n1+n2)
        w2=n2/(n1+n2)
        result.val=w1*self.val+w2*other.val
        result.err=[[w1*self.err[i][j]+w2*other.err[i][j] for j in range(len(self.err[i]))] for i in range(len(self.err))]
        result.err[0][0]=(result.val*(1-result.val)/(n1+n2))**0.5
        return result

    def __str__(self):
        if self.val==None and self.err==None:
            return "Empty efficiency"
        out="{:.4} +- {:.4} +- {:.4}".format(self.val,self.err[0][0],self.GetError(stat=False))
        for i in range(1,len(self.err)):
            out+=" [ "+" ".join(["{:+.4}".format(self.err[i][j]) for j in range(len(self.err[i]))])+" ]"                
        return out
        
    def GetEffectiveEntries(self):
        if self.val==None and self.err==None: return 0.
        if self.err[0][0]==0: return 0.
        return self.val*(1-self.val)/self.err[0][0]**2

    def GetError(self,stat=True,syst=True,iset=None,imem=None):
        if self.err is None: return 0.
        if iset is not None and imem is not None:
            return self.err[iset][imem]
        err=0
        if stat:
            err+=(err**2+self.err[0][0]**2)**0.5
        if syst:
            for i in range(1,len(self.err)):
                maxerr=0
                for j in range(len(self.err[i])):
                    if abs(self.err[i][j])>maxerr: maxerr=abs(self.err[i][j])
                err=(err**2+maxerr**2)**0.5
        return err
    def GetStructure(self):
        out=[]
        for i in range(len(self.err)):
            for j in range(len(self.err[i])):
                out+=[(i,j)]
        return out

    def clone(self):
        return copy.deepcopy(self)
        
class ScaleFactor(Efficiency):
    def __add__(self,other):
        n1=self.GetEffectiveEntries()
        n2=other.GetEffectiveEntries()
        if n1==0: return other.clone()
        if n2==0: return self.clone()
        result=self.clone()
        w1=n1/(n1+n2)
        w2=n2/(n1+n2)
        result.val=w1*self.val+w2*other.val
        result.err=[[w1*self.err[i][j]+w2*other.err[i][j] for j in range(len(self.err[i]))] for i in range(len(self.err))]
        result.err[0][0]=((w1*self.err[0][0])**2+(w2*other.err[0][0])**2)**0.5
        return result

    def GetEffectiveEntries(self):
        if self.val==None and self.err==None: return 0.
        if self.err[0][0]==0: return 0.
        return (self.val/self.err[0][0])**2
    

class EfficiencyHist:
    def __init__(self,path=None,isSF=None,hist=None,bins=None):
        self.hist=None
        self.bins=None
        if path:
            self.InitWithFile(path,isSF)
        if hist and bins:
            self.InitWithHistBins(hist,bins)
        return

    def __str__(self):
        out=[]
        for b in self.bins:
            out+=[b.__str__()]
        return "\n".join(out)

    def InitWithHistBins(self,hist,bins):
        self.hist=hist.Clone()
        self.hist.SetDirectory(0)
        self.bins=copy.deepcopy(bins)
        return
        
    def InitWithFile(self,path,isSF=None):
        filename,histname=path.split(":",1)
        if histname=="sf" and isSF==None:
            isSF=True
        fin=ROOT.TFile(filename)
        keys=[key.GetName() for key in fin.GetListOfKeys() if key.GetName().startswith(histname+"_s")]
        hists=[]
        for i in range(100):
            memberkeys=[key for key in keys if key.startswith(histname+"_s{}m".format(i))]
            if len(memberkeys)==0:
                break
            hists+=[[fin.Get(key) for key in memberkeys]]
        
        self.hist=hists[0][0].Clone(histname)
        self.hist.Reset()
        self.hist.SetDirectory(0)
            
        self.bins=[]
        for ibin in range(self.hist.GetNcells()):
            val=hists[0][0].GetBinContent(ibin)
            err=[[hists[i][j].GetBinContent(ibin)-val for j in range(len(hists[i]))] for i in range(len(hists))]
            err[0][0]=hists[0][0].GetBinError(ibin)
            if isSF:
                self.bins+=[ScaleFactor(val,err)]
            else:
                self.bins+=[Efficiency(val,err)]
        return

    def GetDimension(self):
        return self.hist.GetDimension()

    def GetBin(self,ix,iy=0,iz=0):
        return self.hist.GetBin(ix,iy,iz)
    def GetBinXYZ(self,ibin):
        ix=ROOT.long()
        iy=ROOT.long()
        iz=ROOT.long()
        self.hist.GetBinXYZ(ix,iy,iz)
        return int(ix),int(iy),int(iz)
    def FindBin(self,x,y=0,z=0):
        return self.hist.FindBin(x,y,z)

    def GetBinContent(self,ibin):
        return self.bins[ibin].val
    def GetBinError(self,ibin,stat=True,syst=True,iset=None,imem=None):
        return self.bins[ibin].GetError(stat,syst,iset,imem)

    def GetXaxis(self):
        return self.hist.GetXaxis()
    def GetYaxis(self):
        return self.hist.GetYaxis()
    def GetZaxis(self):
        return self.hist.GetZaxis()
    
    def GetCombined(self,ixmin=None,ixmax=None,iymin=None,iymax=None,izmin=None,izmax=None):
        if ixmin==None: ixmin=1
        if ixmax==None: ixmax=self.GetXaxis().GetNbins()
        if iymin==None: iymin=1
        if iymax==None: iymax=self.GetYaxis().GetNbins()
        if izmin==None: izmin=1
        if izmax==None: izmax=self.GetZaxis().GetNbins()
        b=type(self.bins[0])()
        for ix in range(ixmin,ixmax+1):
            for iy in range(iymin,iymax+1):
                for iz in range(izmin,izmax+1):
                    b+=self.bins[self.GetBin(ix,iy,iz)]
        return b

    def GetStructure(self):
        return self.bins[0].GetStructure()
        
    def ProjectionX(self,iymin=None,iymax=None,izmin=None,izmax=None):
        if iymin==None: iymin=1
        if iymax==None: iymax=self.GetYaxis().GetNbins()
        if izmin==None: izmin=1
        if izmax==None: izmax=self.GetZaxis().GetNbins()
        hist=self.hist.ProjectionX().Clone()
        bins=[type(self.bins[0])() for i in range(hist.GetNcells())]
        for ix in range(hist.GetNcells()):
            for iy in range(iymin,iymax+1):
                for iz in range(izmin,izmax+1):
                    bins[ix]+=self.bins[self.GetBin(ix,iy,iz)]
        return EfficiencyHist(hist=hist,bins=bins)
        
    def ProjectionY(self,ixmin=None,ixmax=None,izmin=None,izmax=None):
        if ixmin==None: ixmin=1
        if ixmax==None: ixmax=self.GetXaxis().GetNbins()
        if izmin==None: izmin=1
        if izmax==None: izmax=self.GetZaxis().GetNbins()
        hist=self.hist.ProjectionY().Clone()
        bins=[type(self.bins[0])() for i in range(hist.GetNcells())]
        for ix in range(ixmin,ixmax+1):
            for iy in range(hist.GetNcells()):
                for iz in range(izmin,izmax+1):
                    bins[iy]+=self.bins[self.GetBin(ix,iy,iz)]
        return EfficiencyHist(hist=hist,bins=bins)
        
    def MakeTH(self,stat=True,syst=True,iset=None,imem=None):
        hist=self.hist.Clone()
        hist.SetDirectory(0)
        for i in range(hist.GetNcells()):
            val=self.GetBinContent(i)
            err=self.GetBinError(i,stat,syst,iset,imem)
            if iset is not None and imem is not None:
                val+=err
                err=0
            hist.SetBinContent(i,val)
            hist.SetBinError(i,err)
        return hist
