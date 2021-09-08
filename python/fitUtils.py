import os,math
import ctypes
import ROOT as rt

def calc_eff(valp,valf,errp=None,errf=None):
    eff=valp/(valp+valf)
    if errp is None and errf is None:
        return eff
    ## FIXME more precise error formular 
    ## at https://root.cern.ch/doc/master/TH1_8cxx_source.html#l03026
    ## but need to understand. use naive one for now
    err=math.sqrt(eff*(1-eff)*(errp**2+errf**2)/(valp+valf)**2)
    return eff,err

def calc_eff_from_hist(hpass,hfail,xmin=None,xmax=None):
    ixmin,ixmax=0,-1
    if xmin is not None and xmax is not None:
        ixmin=hpass.FindBin(xmin)
        ixmax=hpass.FindBin(xmax)
        if abs(xmax-hpass.GetBinLowEdge(ixmax))<hpass.GetBinWidth(ixmax)*1e-5:
            ixmax-=1
    errp=ctypes.c_double(0.)
    errf=ctypes.c_double(0.)
    valp=hpass.IntegralAndError(ixmin,ixmax,errp)
    valf=hfail.IntegralAndError(ixmin,ixmax,errf)
    errp=errp.value
    errf=errf.value
    return calc_eff(valp,valf,errp,errf)

#from ROOT import tnpFitter
class tnpFitter(object):
    def __init__(self,config):
        self.config=config.clone()
        rt.gROOT.SetBatch(1)
        rt.RooMsgService.instance().setGlobalKillBelow(rt.RooFit.ERROR)
        
    def run(self,ibin):
        config=self.config
        method=config.method.split()
        isFit="fit" in method
        
        work=rt.RooWorkspace("w")
        work.factory("x[{},{}]".format(config.hist_range[0],config.hist_range[1]))
        x=work.var("x")
        histPass=config.get_hist(ibin,True,genmatching="genmatching" in method,genmass="genmass" in method)
        histFail=config.get_hist(ibin,False,genmatching="genmatching" in method,genmass="genmass" in method)
        work.Import(rt.RooDataHist("histPass","histPass",x,histPass))
        work.Import(rt.RooDataHist("histFail","histFail",x,histFail))

        if isFit:
            sim_config=config.clone(isSim=True)
            for spass in ["Pass","Fail"]:
                for smatched in ["_genmatching",""]:
                    for sgen in ["_genmass",""]:
                        for srandom in ["_random",""]:
                            key="hist"+spass+smatched+sgen+srandom
                            if key in ["histPass","histFail"]: continue
                            if key in " ".join(config.fit_parameter):
                                hist=sim_config.get_hist(ibin,isPass=spass=="Pass",genmatching=smatched=="_genmatching",genmass=sgen=="_genmass",random=hash(config.path+str(ibin)) if srandom=="_random" else None)
                                work.Import(rt.RooDataHist(key,key,x,hist))

            for line in config.fit_parameter:
                words=line.split()
                if words[0]=="SetConstant":
                    for word in words[1:]:
                        work.var(word).setConstant()
                elif words[0]=="Fit":
                    self.fit_hist(work.pdf(words[1]),work.data(words[2]))
                else:
                    work.factory(line)

            bin80=histPass.FindBin(80)
            bin100=histPass.FindBin(100)
            work.factory("nSigP[{},0.5,{}]".format(histPass.Integral(bin80,bin100),histPass.Integral()*2));
            work.factory("nBkgP[{},0.5,{}]".format(histPass.Integral()-histPass.Integral(bin80,bin100),histPass.Integral()*2));
            work.factory("nSigF[{},0.5,{}]".format(histFail.Integral(bin80,bin100),histFail.Integral()*2));
            work.factory("nBkgF[{},0.5,{}]".format(histFail.Integral()-histFail.Integral(bin80,bin100),histFail.Integral()*2));
            work.factory("SUM::pdfPass(nSigP*sigPass,nBkgP*bkgPass)");
            work.factory("SUM::pdfFail(nSigF*sigFail,nBkgF*bkgFail)");
            
            if "hsseo" in config.option:
                if config.bins[ibin]['vars']['el_pt']['max']<31:
                    if work.var("sigmaP"):
                        work.var("sigmaP").setConstant()
                    if work.var("sigmaF"):
                        work.var("sigmaF").setConstant()                    

            resultPass=self.fit_hist(work.pdf("pdfPass"),work.data("histPass"))
            resultFail=self.fit_hist(work.pdf("pdfFail"),work.data("histFail"))

        plotPass=x.frame(config.hist_range[0],config.hist_range[1]);
        plotFail=x.frame(config.hist_range[0],config.hist_range[1]);
        plotPass.SetTitle("passing probe");
        plotFail.SetTitle("failing probe");

        work.data("histPass").plotOn(plotPass);
        work.data("histFail").plotOn(plotFail);
        if isFit:
            work.pdf("pdfPass").plotOn(plotPass,rt.RooFit.LineColor(rt.kRed));
            work.pdf("pdfPass").plotOn(plotPass,rt.RooFit.Components("bkgPass"),rt.RooFit.LineColor(rt.kBlue),rt.RooFit.LineStyle(rt.kDashed));
            work.pdf("pdfFail").plotOn(plotFail,rt.RooFit.LineColor(rt.kRed));
            work.pdf("pdfFail").plotOn(plotFail,rt.RooFit.Components("bkgFail"),rt.RooFit.LineColor(rt.kBlue),rt.RooFit.LineStyle(rt.kDashed));

        binname=config.bins[ibin]['name']
        c=rt.TCanvas("{}_Canv".format(binname),"{}".format(binname),1100,450);
        c.Divide(3,1);
        c.cd(1)
        text1=rt.TPaveText(0,0.6,1,0.9)
        text1.SetName("efficiencies")
        text1.SetFillColor(0)
        text1.SetBorderSize(0)
        text1.SetTextAlign(12)
        if isFit:
            text1.AddText("* fit status pass: {}, fail : {}".format(resultPass.status(),resultFail.status()))
            ## fit errors should be scaled. See comment on fitTo function.
            fit_valp=work.var("nSigP").getVal()
            fit_errp=work.var("nSigP").getError()*(histPass.Integral()/histPass.GetEffectiveEntries())**0.5
            fit_valf=work.var("nSigF").getVal()
            fit_errf=work.var("nSigF").getError()*(histFail.Integral()/histFail.GetEffectiveEntries())**0.5
            fit_eff,fit_err=calc_eff(fit_valp,fit_valf,fit_errp,fit_errf)
            text1.AddText("fit_eff[{},{}] = {:.4f} #pm {:.4f}".format(config.fit_range[0],config.fit_range[1],fit_eff,fit_err))
            if hasattr(config,"count_range") and getattr(config,"count_range"):
                xarg=rt.RooArgSet(x)        
                x.setRange("fit_range",config.fit_range[0],config.fit_range[1])
                x.setRange("count_range",config.count_range[0],config.count_range[1])
                fracPass=work.pdf("sigPass").createIntegral(xarg,rt.RooFit.NormSet(xarg),rt.RooFit.Range("count_range")).getVal()/work.pdf("sigPass").createIntegral(xarg,rt.RooFit.NormSet(xarg),rt.RooFit.Range("fit_range")).getVal()
                fracFail=work.pdf("sigFail").createIntegral(xarg,rt.RooFit.NormSet(xarg),rt.RooFit.Range("count_range")).getVal()/work.pdf("sigFail").createIntegral(xarg,rt.RooFit.NormSet(xarg),rt.RooFit.Range("fit_range")).getVal()
                fit_valp=fit_valp*fracPass
                fit_errp=fit_errp/math.sqrt(fracPass)
                fit_valf=fit_valf*fracFail
                fit_errf=fit_errf/math.sqrt(fracFail)
                fit_eff,fit_err=calc_eff(fit_valp,fit_valf,fit_errp,fit_errf)
                text1.AddText("fit_eff[{},{}] = {:.4f} #pm {:.4f}".format(config.count_range[0],config.count_range[1],fit_eff,fit_err))
                
        count_eff,count_err=calc_eff_from_hist(histPass,histFail)
        text1.AddText("count_eff[{},{}] = {:.4f} #pm {:.4f}".format(config.hist_range[0],config.hist_range[1],count_eff,count_err))
        if hasattr(config,"count_range") and getattr(config,"count_range"):
            count_eff,count_err=calc_eff_from_hist(histPass,histFail,config.count_range[0],config.count_range[1])
            text1.AddText("count_eff[{},{}] = {:.4f} #pm {:.4f}".format(config.count_range[0],config.count_range[1],count_eff,count_err))
        
        text2=rt.TPaveText(0,0,1,0.6)
        text2.SetName("parameters")
        text2.SetFillColor(0)
        text2.SetBorderSize(0)
        text2.SetTextAlign(12)
        if isFit:
            text2.AddText("* parmeters ")
            for par in resultPass.floatParsFinal():
                text2.AddText("{} \t= {:.3f} #pm {:.3f}".format(par.GetName(),par.getVal(),par.getError()))
            for par in resultPass.constPars():
                text2.AddText("{} \t= {:.3f} [Fixed]".format(par.GetName(),par.getVal()))
            for par in resultFail.floatParsFinal():
                text2.AddText("{} \t= {:.3f} #pm {:.3f}".format(par.GetName(),par.getVal(),par.getError()))
            for par in resultFail.constPars():
                text2.AddText("{} \t= {:.3f} [Fixed]".format(par.GetName(),par.getVal()))


        text_eff=rt.TPaveText(0,0.9,1,1)
        text_eff.SetName("efficiency")
        text_eff.SetFillColor(0)
        text_eff.SetBorderSize(0)
        text_eff.SetTextAlign(12)
        if isFit:
            text_eff.AddText("eff = {:.4f} #pm {:.4f}".format(fit_eff,fit_err))
        else:
            text_eff.AddText("eff = {:.4f} #pm {:.4f}".format(count_eff,count_err))            

        text_eff.Draw()
        text1.Draw()
        text2.Draw()
        c.cd(2)
        c.GetPad(2).SetLeftMargin(0.15)
        c.GetPad(2).SetRightMargin(0.05)
        plotPass.Draw();
        c.cd(3)
        c.GetPad(3).SetLeftMargin(0.15)
        c.GetPad(3).SetRightMargin(0.05)
        plotFail.Draw();

        fpath="/".join([config.path,config.fit_file.replace(".root",".d"),config.name,"bin{}.root".format(ibin)])
        os.system("mkdir -p "+os.path.dirname(fpath))
        fout=rt.TFile(fpath,"recreate")
        fout.mkdir(config.name)
        fout.cd(config.name)
        c.Write("{}_Canv".format(binname))
        if isFit:
            resultPass.Write("{}_resP".format(binname))
            resultFail.Write("{}_resF".format(binname))
        fout.Close()

        plotpath="/".join([config.path,"plots","sim" if config.isSim else "data",config.name])
        os.system("mkdir -p "+plotpath)
        c.SaveAs("{}/{}.png".format(plotpath,binname))

        return

    def fit_hist(self,function,hist):
        for i in range(20):
            ## SumW2Error or AsymptoticError can be used. but it seems to make the fitting unstable. Instead just scale the uncertainty later
            result=function.fitTo(hist,rt.RooFit.Range(self.config.fit_range[0],self.config.fit_range[1]),rt.RooFit.Save(True),rt.RooFit.PrintLevel(-1))
            nSigF=result.floatParsFinal().find("nSigF")
            ## prevent 0 nSigF
            if nSigF and nSigF.getVal()<1.:
                nSigF.setVal(100)
                continue
            if result.status()==0:
                return result
        print "Warning: non-zero fit status {}".format(result.status())
        return result
