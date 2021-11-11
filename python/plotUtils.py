import os,sys,copy,math
import numpy
import ROOT
from efficiencyUtils import Efficiency,ScaleFactor,EfficiencyHist,ScaleFactorHist
def Setup():
    ROOT.TH1.SetDefaultSumw2(True)
    ROOT.gStyle.SetCanvasDefH(600)
    ROOT.gStyle.SetCanvasDefW(600)
    ROOT.gStyle.SetPadLeftMargin(0.15)
    ROOT.gStyle.SetPadBottomMargin(0.12)
    ROOT.gStyle.SetPadColor(0)
    ROOT.gStyle.SetFrameFillStyle(0)
    ROOT.gStyle.SetTitleFontSize(0)
    ROOT.TGaxis.SetExponentOffset(-0.06,0)
    return

def GetHist(filename,histname):
    f=ROOT.TFile(filename)
    h=f.Get(histname)
    h.SetDirectory(0)
    h.SetStats(0)
    return h

def GetAxisParent(pad=None):
    if pad is None: pad=ROOT.gPad
    if pad:
        l=pad.GetListOfPrimitives()
        for obj in l:
            if obj.InheritsFrom("THStack"): return obj.GetHistogram()
            if obj.InheritsFrom("TH1"): return obj
            if obj.InheritsFrom("TGraph"): return obj.GetHistogram()
    return None
    
def DrawPreliminary(args,pad=None):
    if pad==None: pad=ROOT.gPad
    if pad:
        pad.cd();
        latex=ROOT.TLatex()
        latex.SetTextSize(0.03);
        latex.SetNDC();
        latex.SetTextAlign(11)
        latex.DrawLatex(0.16,0.91,"CMS #bf{#it{Preliminary}}")
        latex.SetTextAlign(31)
        latex.DrawLatex(0.9,0.95,"Run "+args.era)
        if args.era=="2016preVFP":
            latex.DrawLatex(0.9,0.91,"19.5 fb^{-1} (13 TeV)")
        if args.era=="2016postVFP":
            latex.DrawLatex(0.9,0.91,"16.8 fb^{-1} (13 TeV)")
        if args.era=="2016":
            latex.DrawLatex(0.9,0.91,"36.3 fb^{-1} (13 TeV)")
        if args.era=="2017":
            latex.DrawLatex(0.9,0.91,"41.5 fb^{-1} (13 TeV)")
        if args.era=="2018":
            latex.DrawLatex(0.9,0.91,"59.8 fb^{-1} (13 TeV)")
        if args.era=="Run2":
            latex.DrawLatex(0.9,0.91,"137 fb^{-1} (13 TeV)")
        latex.SetTextColor(2)
        latex.SetTextAlign(11)
        latex.DrawLatex(0.38,0.91,"#it{Working in progress}")
    return

class Arguments(object):
    def __str__(self):
        return self.__dict__.__str__()
    def era_short(self):
        return self.era.replace("preVFP","a").replace("postVFP","b")
    def clone(self,**kwargs):
        out=copy.deepcopy(self)
        for key in kwargs:
            setattr(out,key,kwargs[key])
        return out

def GetFileName(args):
    for required in ["home","channel","era","id","charge"]:
        if not hasattr(args,required) or getattr(args,required) is None: 
            return None
    filename="_".join([args.id,args.charge])+".root"
    if hasattr(args,"trigger") and args.trigger not in ["",None]:
        filename=args.trigger+"_"+filename
    return "/".join([args.home,"root",args.channel,args.era,filename])

def GetHistName(args):
    if not hasattr(args,"type") or getattr(args,"type") is None: 
        return None
    return args.type

def ParseArgs(kwargs=None,**kwargs_):
    if kwargs is None: kwargs=kwargs_
    if type(kwargs) is dict:
        args=Arguments()
        for key in kwargs:
            setattr(args,key,kwargs[key])
    else:
        args=kwargs.clone()
    if not hasattr(args,"home"):
        setattr(args,"home",os.getenv("ANEFFDIR"))
    if hasattr(args,"trigger"):
        if type(args.trigger) is int:
            if args.channel=="Electron":
                if args.trigger==0:
                    args.trigger="Ele32"
                    if args.era.startswith("2016"):
                        args.trigger="Ele27"
                elif args.trigger==1:
                    args.trigger="Ele23Leg1"
                elif args.trigger==2:
                    args.trigger="Ele12Leg2"
            elif args.channel=="Muon":
                if args.trigger==0:
                    args.trigger="IsoMu24"
                    if args.era=="2017":
                        args.trigger="IsoMu27"
                elif args.trigger==1:
                    args.trigger="Mu17Leg1"
                elif args.trigger==2:
                    args.trigger="Mu8Leg2"
    if not hasattr(args,"ptmin"):
        args.ptmin=10.
        if hasattr(args,"trigger") and args.trigger not in [None,""]:
            if args.trigger.startswith("Ele12"): args.ptmin=15.
            if args.trigger.startswith("Ele23"): args.ptmin=25.
            if args.trigger.startswith("Ele27"): args.ptmin=30.
            if args.trigger.startswith("Ele32"): args.ptmin=35.
            if args.trigger.startswith("Mu8"): args.ptmin=10.
            if args.trigger.startswith("Mu17"): args.ptmin=20.
            if args.trigger.startswith("IsoMu24"): args.ptmin=27.
            if args.trigger.startswith("IsoMu27"): args.ptmin=30.
    if not hasattr(args,"filename"):
        filename=GetFileName(args)
        if filename: setattr(args,"filename",filename)
    if not hasattr(args,"histname"):
        histname=GetHistName(args)
        if histname: setattr(args,"histname",histname)
    return args

def GetPlotEfficiencyPt(args=None,**kwargs):
    if args is None: args=ParseArgs(kwargs)

def GetEfficiencyHist(args=None,**kwargs):
    if args is None: args=kwargs
    args=ParseArgs(args)
    return EfficiencyHist(args.filename+":"+args.histname)

def GetListOfArgs(channels=None,eras=None,ids=None,triggers=None,types=None,charges=None):
    if channels is None: channels=["Electron","Muon"]
    if eras is None: eras=["2016preVFP","2016postVFP","2017","2018"]
    if ids is None: ids=["MediumID","TightID_SelQ","MediumID_LooseTrkIso"]
    if triggers is None: triggers=[None,0,1,2]
    if types is None: types=["data","sim","sf"]
    if charges is None: charges=["Plus","Minus"]
    largs=[]
    for channel in channels:
        for era in eras:
            for ID in ids:
                for trigger in triggers:
                    for charge in charges:
                        for TYPE in types:
                            if channel=="Electron" and ID=="MediumID_LooseTrkIso": continue
                            if channel=="Electron" and ID=="TightID_SelQ" and trigger in [1,2]: continue
                            if channel=="Muon" and ID in ["MediumID","TightID_SelQ"]: continue
                            largs+=[ParseArgs(channel=channel,era=era,id=ID,trigger=trigger,type=TYPE,charge=charge)]
    return largs

def Find(lobj,name=None,title=None,classname=None):
    for obj in lobj:
        if name and obj.GetName()!=name: continue
        if title and obj.GetTitle()!=title: continue
        if classname and obj.ClassName()!=classname: continue
        return obj
    return None

def GetSystematicPlot(filename,axis="x",ibin=None,ymin=None):
    c=ROOT.TCanvas()
    c.Divide(1,4)
    c.GetPad(1).SetPad(0,0.12+0.26*2,1,1)
    c.GetPad(1).SetTopMargin(0.1/(0.1+0.26))
    c.GetPad(1).SetBottomMargin(0)
    c.GetPad(2).SetPad(0,0.12+0.26,1,0.12+0.26*2)
    c.GetPad(2).SetTopMargin(0)
    c.GetPad(2).SetBottomMargin(0)
    c.GetPad(3).SetPad(0,0,1,0.12+0.26)
    c.GetPad(3).SetTopMargin(0)
    c.GetPad(3).SetBottomMargin(0.12/(0.12+0.26))
    c.GetPad(4).SetPad(0,0,1,1)
    for i in range(1,5):
        c.GetPad(i).SetLeftMargin(0.15)
        c.GetPad(i).SetFillStyle(0)
    types=["data","sim","sf"]
    histss=[]
    for i in range(1,4):
        hists=[]
        c.cd(i)
        effhist=EfficiencyHist(filename+":"+types[i-1])
        if axis=="x":
            h=effhist.ProjectionX(ibin,ibin)
        elif axis=="y":
            h=effhist.ProjectionY(ibin,ibin)
        norm=h.MakeTH(stat=False,syst=False)
        if 2*norm.GetBinWidth(norm.GetXaxis().GetFirst())<norm.GetBinWidth(norm.GetXaxis().GetLast()):
            ROOT.gPad.SetLogx()

        hist=h.MakeTH()
        hist.SetFillStyle(3003)
        hist.SetFillColor(1)
        hist.SetMarkerStyle(0)
        hist.SetOption("e2")
        hists+=[hist.Clone("total")]

        hist=h.MakeTH(syst=False)
        hist.SetMarkerStyle(0)
        hists+=[hist.Clone("stat")]
        for iset,imem in h.GetStructure()[1:]:
            hist=h.MakeTH(iset=iset,imem=imem)
            hist.SetLineColor(iset+1)
            hist.SetLineWidth(2)
            hists+=[hist.Clone("s{}m{}".format(iset,imem))]
        
        for hist in hists:
            hist.Divide(norm)
            for ib in range(hist.GetNcells()):
                val=hist.GetBinContent(ib)
                if val!=0:
                    hist.SetBinContent(ib,val-1)
            draw=False
            for ib in range(hist.GetNcells()):
                if hist.GetBinContent(ib)!=0. or hist.GetBinError(ib)!=0.:
                    draw=True
                    break
            if not draw: continue

            if GetAxisParent():
                hist.Draw("same")
            else:
                hist.SetStats(0)
                hist.SetTitle("")
                hist.GetXaxis().SetMoreLogLabels()
                hist.SetTitleSize(0.04/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"X")
                hist.SetLabelSize(0.04/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"X")
                hist.SetTitleSize(0.03/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"Y")
                hist.SetLabelSize(0.03/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"Y")
                hist.SetTitleOffset(1.8*min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"Y")
                hist.GetYaxis().SetNdivisions(505)
                hist.GetYaxis().SetTickLength(0.01)
                hist.Draw()
        ROOT.gPad.RedrawAxis()
        histss+=[hists]
    GetAxisParent(c.GetPad(1)).GetYaxis().SetTitle("#varepsilon_{data} Rel. Unc. ")
    GetAxisParent(c.GetPad(2)).GetYaxis().SetTitle("#varepsilon_{sim} Rel. Unc. ")
    GetAxisParent(c.GetPad(3)).GetYaxis().SetTitle("SF Rel. Unc. ")
    c.cd(4)
    latex=ROOT.TLatex()
    latex.SetTextSize(0.03)
    latex.SetTextAlign(33)
    if ibin is not None:
        if axis=="x":
            latex.DrawLatex(0.89,0.89,"{:.1f} < {} < {:.1f}".format(effhist.hist.GetYaxis().GetBinLowEdge(ibin),effhist.hist.GetYaxis().GetTitle(),effhist.hist.GetYaxis().GetBinUpEdge(ibin)))
        elif axis=="y":
            latex.DrawLatex(0.89,0.89,"{:.1f} < {} < {:.1f}".format(effhist.hist.GetXaxis().GetBinLowEdge(ibin),effhist.hist.GetXaxis().GetTitle(),effhist.hist.GetXaxis().GetBinUpEdge(ibin)))
    else:
        latex.DrawLatex(0.89,0.89,"Average")            

    leg=ROOT.TLegend(0.5,0.33,0.89,0.43)
    leg.SetNColumns(2)
    leg.AddEntry(Find(hists,name="total"),"total unc.","f")
    leg.AddEntry(Find(hists,name="stat"),"stat. unc.","l")
    for i in range(1,20):
        hist=Find(hists,name="s{}m0".format(i))
        if not hist: break
        title=hist.GetTitle()
        leg.AddEntry(hist,title,"l")
    leg.Draw()
    setattr(c,"legend",leg)

    values=[]
    for hists in histss:
        h=Find(hists,name="total")
        for i in range(h.GetNcells()):
            if h.GetBinContent(i) or h.GetBinError(i):
                values+=[abs(h.GetBinContent(i))+h.GetBinError(i)]
    values=sorted(values)
    #ymax=values[int((len(values)-1)*0.8)]*2
    while numpy.mean(values)+3*numpy.std(values)<values[-1]:
        values=values[:-1]
    ymax=2*numpy.mean(values)
    ymax=math.ceil(ymax*100)/100.-0.001
    GetAxisParent(c.GetPad(1)).GetYaxis().SetRangeUser(-ymax,ymax)
    GetAxisParent(c.GetPad(2)).GetYaxis().SetRangeUser(-ymax,ymax)
    GetAxisParent(c.GetPad(3)).GetYaxis().SetRangeUser(-ymax,ymax)

    c.Update()
    c.Modified()
    setattr(c,"hists",[h for hh in histss for h in hh])
    return c

def SaveSystematicPlots(filename):
    Setup()
    tempbatch=ROOT.gROOT.IsBatch()
    tempignorelevel=ROOT.gErrorIgnoreLevel
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel=ROOT.kWarning

    h=EfficiencyHist(filename+":data").MakeTH()
    if not h:
        print "No data in "+filename
        return
    plotdir="/".join([os.path.dirname(filename),"plots/summary"])
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
    for i in range(1,h.GetNbinsY()+1):
        c=GetSystematicPlot(filename,axis="x",ibin=i)
        c.SaveAs(plotdir+"/syst_x{}.pdf".format(i))
        c.SaveAs(plotdir+"/syst_x{}.png".format(i))
    c=GetSystematicPlot(filename,axis="x")
    c.SaveAs(plotdir+"/syst_x.pdf".format(i))
    c.SaveAs(plotdir+"/syst_x.png".format(i))
        
    for i in range(1,h.GetNbinsX()+1):
        c=GetSystematicPlot(filename,axis="y",ibin=i)
        c.SaveAs(plotdir+"/syst_y{}.pdf".format(i))
        c.SaveAs(plotdir+"/syst_y{}.png".format(i))
    c=GetSystematicPlot(filename,axis="y")
    c.SaveAs(plotdir+"/syst_y.pdf".format(i))
    c.SaveAs(plotdir+"/syst_y.png".format(i))
    
    ROOT.gROOT.SetBatch(tempbatch)
    ROOT.gErrorIgnoreLevel=tempignorelevel
    return

def GetEfficiencyPlot(filename,axis="y",ibin=None):
    ehdata2d=EfficiencyHist(filename+":data")
    ehsim2d=EfficiencyHist(filename+":sim")

    if type(ibin) is not list:
        ibin=[ibin]

    hists=[]
    sfs=[]
    colors=[1,2,3,4,6,7,8,9]
    icolor=0
    for i in ibin:
        if axis=="x":
            hdata=ehdata2d.ProjectionX(i,i).MakeTH()
            hsim=ehsim2d.ProjectionX(i,i).MakeTH()
            hsf=ScaleFactorHist(ehdata2d.ProjectionX(i,i),ehsim2d.ProjectionX(i,i)).MakeTH()
        elif axis=="y":
            hdata=ehdata2d.ProjectionY(i,i).MakeTH()
            hsim=ehsim2d.ProjectionY(i,i).MakeTH()
            hsf=ScaleFactorHist(ehdata2d.ProjectionY(i,i),ehsim2d.ProjectionY(i,i)).MakeTH()
            
        if i is None:
            rangestring="average"
            if len(ibin)>1:
                hdata.SetLineWidth(2)
                hsim.SetLineWidth(2)
                hsf.SetLineWidth(2)
        else:
            if axis=="x":
                rangestring="{:.1f} < {} < {:.1f}".format(ehdata2d.hist.GetYaxis().GetBinLowEdge(i),ehdata2d.hist.GetYaxis().GetTitle().replace(" [GeV]",""),ehdata2d.hist.GetYaxis().GetBinUpEdge(i))
            elif axis=="y":
                rangestring="{:.1f} < {} < {:.1f}".format(ehdata2d.hist.GetXaxis().GetBinLowEdge(i),ehdata2d.hist.GetXaxis().GetTitle().replace(" [GeV]",""),ehdata2d.hist.GetXaxis().GetBinUpEdge(i))
        hdata.SetTitle("data "+rangestring)
        hsim.SetTitle("sim "+rangestring)
        hsf.SetTitle("sf "+rangestring)
            
        hdata.SetLineColor(colors[icolor])
        hdata.SetMarkerColor(colors[icolor])
        hdata.SetMarkerStyle(20)
        hdata.SetMarkerSize(0.7)
        hists+=[hdata]
        
        hsim.SetLineStyle(2)
        hsim.SetLineColor(colors[icolor])
        hsim.SetMarkerStyle(1)
        hists+=[hsim]

        hsf.SetLineColor(colors[icolor])
        sfs+=[hsf]

        icolor+=1

    c=ROOT.TCanvas()
    c.Divide(1,3)

    c.cd(2)
    ROOT.gPad.SetPad(0,0.35,1,1)
    ROOT.gPad.SetFillStyle(0)
    ROOT.gPad.SetBottomMargin(0.0)
    ROOT.gPad.SetTopMargin(c.GetTopMargin()/0.65)
    if 2*hdata.GetBinWidth(hdata.GetXaxis().GetFirst())<hdata.GetBinWidth(hdata.GetXaxis().GetLast()):
        ROOT.gPad.SetLogx()
    for hist in hists:
        if GetAxisParent(): 
            hist.Draw("same hist e")
        else: 
            hist.Draw("hist e")
        
    GetAxisParent().GetYaxis().SetTitle("Efficiency")
    GetAxisParent().GetYaxis().SetRangeUser(0.11,1.04)
    GetAxisParent().SetTitleSize(0.04/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"XYZ")
    GetAxisParent().SetTitleOffset(2*min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"Y")
    GetAxisParent().SetLabelSize(0.04/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"XYZ")

    c.cd(3)
    ROOT.gPad.SetPad(0,0,1,0.35)
    ROOT.gPad.SetGridy()
    ROOT.gPad.SetFillStyle(0)
    ROOT.gPad.SetTopMargin(0.0)
    ROOT.gPad.SetBottomMargin(c.GetBottomMargin()/0.35)
    if 2*hdata.GetBinWidth(hdata.GetXaxis().GetFirst())<hdata.GetBinWidth(hdata.GetXaxis().GetLast()):
        ROOT.gPad.SetLogx()
    for hist in sfs:
        if GetAxisParent(): 
            hist.Draw("same hist e")
        else:
            hist.Draw("hist e")
    GetAxisParent().SetTitle("")
    GetAxisParent().GetXaxis().SetMoreLogLabels()
    GetAxisParent().GetYaxis().SetRangeUser(0.81,1.19)
    GetAxisParent().GetYaxis().SetNdivisions(205)
    GetAxisParent().GetYaxis().SetTitle("SF")
    GetAxisParent().SetTitleSize(0.04/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"XYZ")
    GetAxisParent().SetTitleOffset(2*min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"Y")
    GetAxisParent().SetTitleOffset(1.3*ROOT.gPad.GetWNDC(),"X")
    GetAxisParent().SetLabelSize(0.04/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"XYZ")

    c.cd(1)
    ROOT.gPad.SetPad(0,0,1,1)
    ROOT.gPad.SetFillStyle(0)

    leg=ROOT.TLegend(0.89,0.37,0.6,0.55)
    leg.SetBorderSize(0)
    for hist in hists:
        leg.AddEntry(hist,"","l")
    leg.Draw()
    setattr(c,"legend",leg)
    
    GetAxisParent(c.GetPad(2)).SetTitle("")
    c.Update()
    c.Modified()
    setattr(c,"hists",hists+sfs)

    return c
    
def SaveEfficiencyPlots(filename):
    Setup()
    tempbatch=ROOT.gROOT.IsBatch()
    tempignorelevel=ROOT.gErrorIgnoreLevel
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel=ROOT.kWarning

    h=EfficiencyHist(filename+":data").MakeTH()
    if not h:
        print "No data in "+filename
        return
    plotdir="/".join([os.path.dirname(filename),"plots/summary"])
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
    for i in range(1,h.GetNbinsY()+1):
        c=GetEfficiencyPlot(filename,axis="x",ibin=i)
        c.SaveAs(plotdir+"/eff_x{}.pdf".format(i))
        c.SaveAs(plotdir+"/eff_x{}.png".format(i))
    c=GetEfficiencyPlot(filename,axis="x")
    c.SaveAs(plotdir+"/eff_x.pdf")
    c.SaveAs(plotdir+"/eff_x.png")
    c=GetEfficiencyPlot(filename,axis="x",ibin=[None,h.GetYaxis().FindBin(30),h.GetYaxis().FindBin(90)])
    c.SaveAs(plotdir+"/eff_xx.pdf")
    c.SaveAs(plotdir+"/eff_xx.png")
        
    for i in range(1,h.GetNbinsX()+1):
        c=GetEfficiencyPlot(filename,axis="y",ibin=i)
        c.SaveAs(plotdir+"/eff_y{}.pdf".format(i))
        c.SaveAs(plotdir+"/eff_y{}.png".format(i))
    c=GetEfficiencyPlot(filename,axis="y")
    c.SaveAs(plotdir+"/eff_y.pdf")
    c.SaveAs(plotdir+"/eff_y.png")
    c=GetEfficiencyPlot(filename,axis="y",ibin=[None,h.GetXaxis().FindBin(0.0),h.GetXaxis().FindBin(2.39)])
    c.SaveAs(plotdir+"/eff_yy.pdf")
    c.SaveAs(plotdir+"/eff_yy.png")
    
    ROOT.gROOT.SetBatch(tempbatch)
    ROOT.gErrorIgnoreLevel=tempignorelevel
    return

def SavePlots(filename):
    SaveEfficiencyPlots(filename)
    SaveSystematicPlots(filename)
    return

def PrintEfficiency(path):
    data=EfficiencyHist(path+":data")
    sim=EfficiencyHist(path+":sim")
    sf=EfficiencyHist(path+":sf")
    print data.ProjectionY()
    print sim.ProjectionY()
    print sf.ProjectionY()
    return
    
if __name__=="__main__":
    SavePlots(sys.argv[1])
    exit()
