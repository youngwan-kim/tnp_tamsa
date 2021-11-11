import sys
import ROOT
from efficiencyUtils import make_combined_hist

def PostProcess_fix_ptbelow20(filename):
    fin=ROOT.TFile(filename)
    keys=[k.GetName() for k in fin.GetListOfKeys()]
    keys=[k for k in keys if "data" in k]
    keys=[k for k in keys if "_s" in k]
    hists=[]
    hsf_s0=fin.Get("sf_s0m0").Clone()
    for key in keys:
        hdata=fin.Get(key).Clone()
        hsim=fin.Get(key.replace("data","sim")).Clone()
        
        pt20bin=hdata.GetYaxis().FindBin(20.1)
        for ix in range(hdata.GetNbinsX()+2):
            for iy in range(pt20bin):
                sf=hsf_s0.GetBinContent(ix,pt20bin)/hsf_s0.GetBinContent(ix,iy) if hsf_s0.GetBinContent(ix,iy) else 0.
                hdata.SetBinContent(ix,iy,sf*hdata.GetBinContent(ix,iy))
                hdata.SetBinError(ix,iy,sf*hdata.GetBinError(ix,iy))
        hists+=[hdata.Clone(),hsim.Clone()]
    
    hists_out=[]

    data_hists=[]
    for iset in range(20):
        hist_set=[h for h in hists if "data_s{}".format(iset) in h.GetName()]
        if len(hist_set)==0: break
        data_hists+=[hist_set]        
    hist=fin.Get("data_s0m0").Clone()
    hist.SetNameTitle("data_s{}m0".format(iset),"pT below 20")
    data_hists+=[[hist.Clone()]]
    hists_out+=[make_combined_hist(data_hists)]
    hists_out+=[make_combined_hist(data_hists,stat=False)]
    hists_out+=[h for ms in data_hists for h in ms]

    sim_hists=[]
    for iset in range(20):
        hist_set=[h for h in hists if "sim_s{}".format(iset) in h.GetName()]
        if len(hist_set)==0: break
        sim_hists+=[hist_set]        
    hist=fin.Get("sim_s0m0").Clone()
    hist.SetNameTitle("sim_s{}m0".format(iset),"pT below 20")
    sim_hists+=[[hist.Clone()]]
    hists_out+=[make_combined_hist(sim_hists)]
    hists_out+=[make_combined_hist(sim_hists,stat=False)]
    hists_out+=[h for ms in sim_hists for h in ms]
                
    sf_hists=[[h.Clone(h.GetName().replace("data_","sf_")) for h in members] for members in data_hists]
    for i in range(len(sf_hists)):
        for j in range(len(sf_hists[i])):
            sf_hists[i][j].Divide(sim_hists[i][j])
    hists_out+=[make_combined_hist(sf_hists)]
    hists_out+=[make_combined_hist(sf_hists,stat=False)]
    hists_out+=[h for ms in sf_hists for h in ms]

    fout=ROOT.TFile(filename.replace(".root","_modified.root"),"recreate")
    for h in hists_out:
        h.Write()
    
if __name__=="__main__":
    PostProcess_fix_ptbelow20(sys.argv[1])
