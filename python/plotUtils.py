import os,sys,copy
import ROOT
from efficiencyUtils import Efficiency,ScaleFactor,EfficiencyHist
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

def SavePlotSystematicPt(args=None,**kwargs):
    c=ROOT.TCanvas("c")
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
        ROOT.gPad.SetLogx()
        this_args=ParseArgs(args.clone(type=types[i-1]))
        h=GetEfficiencyHist(this_args).ProjectionY()
        norm=h.MakeTH(stat=False,syst=False)

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
            for ibin in range(hist.GetNcells()):
                val=hist.GetBinContent(ibin)
                if val!=0:
                    hist.SetBinContent(ibin,val-1)
            draw=False
            for ibin in range(hist.GetNcells()):
                if hist.GetBinContent(ibin)!=0. or hist.GetBinError(ibin)!=0.:
                    draw=True
                    break
            if not draw: continue

            if GetAxisParent():
                hist.GetXaxis().SetRangeUser(this_args.ptmin,hist.GetXaxis().GetXmax())
                hist.Draw("same")
            else:
                hist.SetStats(0)
                hist.SetTitle("")
                hist.GetXaxis().SetRangeUser(this_args.ptmin,hist.GetXaxis().GetXmax())
                hist.GetXaxis().SetMoreLogLabels()
                hist.SetTitleSize(0.04/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"X")
                hist.SetLabelSize(0.04/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"X")
                hist.SetTitleSize(0.03/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"Y")
                hist.SetLabelSize(0.03/min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"Y")
                hist.SetTitleOffset(1.8*min(ROOT.gPad.GetHNDC(),ROOT.gPad.GetWNDC()),"Y")
                hist.GetYaxis().SetRangeUser(-0.059,+0.059)
                if hasattr(args,"trigger") and args.trigger not in ["",None]:
                    hist.GetYaxis().SetRangeUser(-0.019,+0.019)
                if args.channel=="Muon":
                    hist.GetYaxis().SetRangeUser(-0.019,+0.019)
                hist.GetYaxis().SetNdivisions(505)
                hist.GetYaxis().SetTickLength(0.01)
                hist.Draw()
        ROOT.gPad.RedrawAxis()
        histss+=[hists]
    GetAxisParent(c.GetPad(1)).GetYaxis().SetTitle("#varepsilon_{data} Rel. Unc. ")
    GetAxisParent(c.GetPad(2)).GetYaxis().SetTitle("#varepsilon_{sim} Rel. Unc. ")
    GetAxisParent(c.GetPad(3)).GetYaxis().SetTitle("SF Rel. Unc. ")

    c.cd(4)
    DrawPreliminary(args)
    latex=ROOT.TLatex()
    latex.SetTextSize(0.03)
    latex.SetNDC()
    latex.SetTextAlign(33)
    if hasattr(args,"trigger") and args.trigger not in ["",None]:
        latex.DrawText(0.89,0.63,args.trigger)
    latex.DrawText(0.89,0.60,args.id)
    if args.charge=="Plus":
        latex.DrawText(0.89,0.57,"Q > 0")
    else:
        latex.DrawText(0.89,0.57,"Q < 0")

    xtitle="e" if args.channel=="Electron" else "#mu"
    xtitle+="^{+}" if args.charge=="Plus" else "^{-}"
    xtitle+=" p_{T} [GeV]"
    GetAxisParent(c.GetPad(3)).GetXaxis().SetTitle(xtitle)

    leg=ROOT.TLegend(0.6,0.28,0.89,0.47)
    leg.AddEntry(Find(hists,name="total"),"total unc.","f")
    leg.AddEntry(Find(hists,name="stat"),"stat. unc.","l")
    if args.channel=="Electron":
        leg.AddEntry(Find(hists,name="s1m0"),"Bkg. model","l")
        leg.AddEntry(Find(hists,name="s2m0"),"Sig. model","l")
        leg.AddEntry(Find(hists,name="s3m0"),"tag selection","l")
        leg.AddEntry(Find(hists,name="s4m0"),"Alt. simulation","l")
    if args.channel=="Muon":
        leg.AddEntry(Find(hists,name="s1m0"),"mass window","l")
        leg.AddEntry(Find(hists,name="s2m0"),"tag selection","l")
        if Find(hists,name="s3m0"):
            leg.AddEntry(Find(hists,name="s3m0"),"number of mass bin","l")
    leg.Draw()

    c.Update()
    c.Modified()

    plotname=args.era_short()
    if hasattr(args,"trigger") and args.trigger not in ["",None]:
        plotname+="_"+args.trigger.replace("Leg1","").replace("Leg2","").lower()
    plotname+="_medium" if "Medium" in args.id else "_tight"
    plotname+="_"+args.charge.lower()
    plotpath="/".join([args.home,"fig/syst",args.channel.lower(),plotname])
    if not os.path.exists(os.path.dirname(plotpath)):
        os.makedirs(os.path.dirname(plotpath))
    c.SaveAs(plotpath+".pdf")
    c.SaveAs(plotpath+".png")

def SavePlotSystematicPtAll():
    Setup()
    largs=GetListOfArgs(types=[None])
    for args in largs:
        SavePlotSystematicPt(args)
    return

def PrintEfficiency(path):
    data=EfficiencyHist(path+":data")
    sim=EfficiencyHist(path+":sim")
    sf=EfficiencyHist(path+":sf")
    print data.ProjectionY()
    print sim.ProjectionY()
    print sf.ProjectionY()
    return

def DrawSysLegend(c):
    c.cd(2)
    leg=ROOT.TLegend(0.65,0.85,0.89,0.97)
    leg.SetNColumns(2)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(c.GetPad(2).GetPrimitive("simulation"),"stat.","f")
    leg.AddEntry(c.GetPad(2).GetPrimitive("efficiencySF")," #oplus eff. unc.","f")
    leg.Draw()
    c.leg=leg
    return c

def SavePlotValidationAll():
    outdir="validation"
    if not os.path.exists(outdir): os.makedirs(outdir)
    ROOT.gROOT.ProcessLine(".L {}/Plotter/EfficiencyPlotter.cc".format(os.getenv("SKFlat_WD")))
    muplotter=ROOT.EfficiencyPlotter("data ^minnlo+tau_minnlo+wjets+vv+tttw+1.7*ss_minnlo")
    elplotter=ROOT.EfficiencyPlotter("data ^minnlo+tau_minnlo+wjets+vv+tttw+ss_minnlo")
    for channel in ["ee","el","mm","mu"]:
        for era in ["2016a","2016b","2017"]:
            if channel.startswith("e"):
                c=DrawSysLegend(elplotter.DrawPlot("{}{}/m52to150/lpt".format(channel,era),"xmax:100 sysname:efficiencySF 1:ytitle:Events 2:ytitle:'data/Pred.' 2:xtitle:'electron p_{T} [GeV]' preliminary norm"))
                c.SaveAs(outdir+"/{}{}_lpt.pdf".format(channel,era))
                #raw_input()
                c=DrawSysLegend(elplotter.DrawPlot("{}{}/m52to150/lsceta".format(channel,era),"sysname:efficiencySF xmin:-2.5 xmax:2.5 1:ytitle:Events 2:ytitle:'data/Pred.' 2:xtitle:'electron #eta_{SC}' preliminary norm noleg"))
                c.SaveAs(outdir+"/{}{}_leta.pdf".format(channel,era))
                #raw_input()
            else:
                c=DrawSysLegend(muplotter.DrawPlot("{}{}/m52to150/lpt".format(channel,era),"xmax:100 sysname:efficiencySF 1:ytitle:Events 2:ytitle:'data/Pred.' 2:xtitle:'muon p_{T} [GeV]' preliminary norm"))
                c.SaveAs(outdir+"/{}{}_lpt.pdf".format(channel,era))
                #raw_input()
                c=DrawSysLegend(muplotter.DrawPlot("{}{}/m52to150/leta".format(channel,era),"sysname:efficiencySF 1:ytitle:Events 2:ytitle:'data/Pred.' 2:xtitle:'muon #eta' preliminary norm noleg"))
                c.SaveAs(outdir+"/{}{}_leta.pdf".format(channel,era))
                #raw_input()
                         
    
if __name__=="__main__":
    #SavePlotSystematicPtAll()
    #SavePlotValidationAll()
    PrintEfficiency(sys.argv[1])

