#!/usr/bin/env python

### python specific import
import os,sys,argparse
import math
import time
from zipfile import ZipFile
import ROOT as rt

TNP_BASE=os.getenv("TNP_BASE")
if TNP_BASE is None or TNP_BASE=="":
    print("[tnp_tamsa] Please source setup.sh")
    exit(1)

parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('settings'     , help = 'setting file [mandatory]')
parser.add_argument('config'       , help = 'config name [mandatory]')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check bining definition')
parser.add_argument('--checkConfig', action='store_true'  , help = 'check configuration')
parser.add_argument('--step'       , default="hist,fit,sum", help = 'steps: hist(ogram),fit,sum(mary)')
parser.add_argument('--set','-s'   , type = int           , help = 'systematic set index (0 refers nominal)')
parser.add_argument('--member','-m', type = int           , help = 'systematic member index (s0m0 refers nominal)')
parser.add_argument('--bin', '-b'  , dest = 'bins'   , type = str, help='bin numbers separated by comma')
parser.add_argument('--data', dest='isData', action='store_true')
parser.add_argument('--sim', dest='isSim', action='store_true')
parser.add_argument('--log'        , action='store_true'     , help = 'keep logs')
parser.add_argument('--njob', '-n' , default="100,20", help = 'condor njob per job submission for each step: "HIST,FIT". Or you can use one number for all steps')
parser.add_argument('--ijob', '-i' , type = int, help = 'condor job index (for internal use)')
parser.add_argument('--nmax'       , default=300, type = int, help = 'condor nmax job (concurrency limits)')
parser.add_argument('--no-condor'  , dest = "condor", action='store_false' )
#parser.add_argument('--log'        , action='store_false'     , help = 'keep logs')

parser.add_argument('--fit'   )
parser.add_argument('--select'   , action='store_true'  )
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--doDraw'     , action='store_true' )
parser.add_argument('--doCnC'      , action='store_true' )

args = parser.parse_args()

####################################################################
##### condor functions
####################################################################
def check_condor(clusterid,njob):
    os.system("sleep 2")
    lines=os.popen("condor_history {} -limit {} -scanlimit 20000 -af exitcode out err".format(clusterid,njob)).read().splitlines()
    for line in lines:
        words=line.split()
        if words[0]!="0":
            print "[tnp_tamsa] Non-zero exit code. Check the log"
            print words[2]
            print words[1]
            return False
        if os.system("grep -q 'Error in' {}".format(words[2]))==0:
            print "[tnp_tamsa] Error occurs. Check the log"
            print words[2]
            print words[1]
            return False
    return True

def submit_condor(jdspath):
    clusterid=int(os.popen('condor_submit '+jdspath+'|grep -o "cluster [0-9]*"').read().split()[1])
    return clusterid

####################################################################
##### argument handling
####################################################################
## time stamp
startTime = time.time()
print 'Starts at', time.strftime('%c', time.localtime(startTime))

## check step argument
args.step=args.step.lower().split(",")
for step in args.step:
    if step not in ["hist","fit","sum"]:
        print "[tnp_tamsa] Unknown step "+step
        exit(1)

## check bins argument
if args.bins:
    args.bins=[int(i) for i in args.bins.split(",")]

## check config argument
importSetting = 'import %s as tnpConf' % args.settings.replace('/','.').split('.py')[0]
exec(importSetting)

if not args.config in tnpConf.Configs.keys():
    print '[tnp_tamsa] config %s not found in config definitions' % args.config
    print '  --> define in settings first'
    print '  In settings I found configs: '
    for key in sorted(tnpConf.Configs.keys()):
        print key
    exit(1)

print '[tnp_tamsa] Use Configs["{}"] from {}'.format(args.config,args.settings)
config=tnpConf.Configs[args.config]
if hasattr(tnpConf,'OutputDir'):
    config.path=tnpConf.OutputDir+"/"+args.config
else:
    config.path="/".join([TNP_BASE,"results",os.path.basename(args.settings).split(".",1)[0],args.config])
os.system("mkdir -p {}".format(config.path))
with open(config.path+"/config.txt","w") as f:
    f.write(config.__str__())

args.njob=[int(i) for i in args.njob.split(",")]

####################################################################
##### check Bins
####################################################################
if args.checkBins:
    for ib in range(len(config.bins)):
        print config.bins[ib]['name']
        print '  - cut: ',config.bins[ib]['cut']
    sys.exit(0)

####################################################################
##### check Config
####################################################################
if args.checkConfig:
    if not args.set or not args.member:
        print(config)
    else:
        configs=config.make_systematics()
        print(configs[args.set][args.member])
    sys.exit(0)

####################################################################
##### Create Histograms
####################################################################
if "hist" in args.step:
    import histUtils
    hist_configs=config.make_hist_configs()
    njob=args.njob[0]
    if args.condor==False:
        histUtils.makePassFailHistograms( hist_configs[args.set], njob, args.ijob)
    elif args.condor==True:
        for iconf in range(len(hist_configs)):
            if args.set!=None and args.set!=iconf: continue
            hist_config=hist_configs[iconf]
            print '[Histogram] Create histograms for {}'.format(hist_config[0].sample)
            jobbatchname='{}_{}_{}'.format(os.path.basename(args.settings).split(".",1)[0],args.config,hist_config[0].hist_file.split(".",1)[0])
            working_dir="/".join([hist_config[0].path,hist_config[0].hist_file.replace(".root",".d")])
            os.system('mkdir -p '+working_dir)

            open(working_dir+'/run.sh','w').write(
'''#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py {} {} --step hist --set {} --njob {} --ijob $1 --no-condor
exit $?
'''.format(args.settings,args.config,iconf,njob)
            )
            os.system("chmod +x "+working_dir+'/run.sh')

            open(working_dir+'/condor.jds','w').write(
'''executable = {0}/run.sh
arguments = $(Process)
output = {0}/job$(Process).out
error = {0}/job$(Process).err
log = {0}/condor.log
concurrency_limits = {1}
jobbatchname = {2}
getenv = True
queue {3}
'''.format(working_dir,"n{}.{}".format(args.nmax,os.getenv("USER")),jobbatchname,njob)
            )

            clusterid=submit_condor(working_dir+'/condor.jds')
            print '  Submit', njob, 'jobs. Waiting...'
            os.system('condor_wait '+working_dir+'/condor.log > /dev/null')
            if not check_condor(clusterid,njob):
                exit(1)
            outfiles=["{}/job{}.root".format(working_dir,i) for i in range(njob)]
            exitcode=os.system('condor_run -a jobbatchname={} -a request_cpus=8 -a concurrency_limits=n32.tnphadd hadd -j 8 -f {} {} > /dev/null'.format(jobbatchname+"_hadd","/".join([hist_config[0].path,hist_config[0].hist_file]),' '.join(outfiles)))
            if exitcode!=0:
                print "hadd failed"
                exit(exitcode)
            os.system('rm {}'.format(" ".join(outfiles)))
            if not args.log:
                os.system("rm -r "+working_dir)
            histUtils.postProcess("/".join([hist_config[0].path,hist_config[0].hist_file]))

####################################################################
##### Actual Fitter
####################################################################
#import libfitUtils as fitUtils
from fitUtils import tnpFitter
if "fit" in args.step:
    configs=config.make_systematics()
    if args.condor==False:
        if not args.isSim and not args.isData:
            print "Wrong"
            exit(1)
        for ibin in args.bins:
            fitter=tnpFitter(configs[args.set][args.member].clone(isSim=args.isSim))
            fitter.run(ibin)
    elif args.condor==True:
        condorlogs={}
        for iset in range(len(configs)):
            if args.set and args.set!=iset: continue
            for imem in range(len(configs[iset])):
                if args.member and args.member!=imem: continue
                for isSim in [False,True]:
                    c=configs[iset][imem].clone(isSim=isSim)
                    jobbatchname='{}_{}_{}_{}'.format(os.path.basename(args.settings).split(".",1)[0],args.config,c.fit_file.split(".",1)[0],c.name)
                    working_dir="/".join([c.path,c.fit_file.replace(".root",".d"),c.name])
                    os.system('mkdir -p '+working_dir)

                    open(working_dir+'/run.sh','w').write(
'''#!/bin/bash
cd $TNP_BASE
python tnp_tamsa.py {} {} --step fit --set {} --member {} {} --bin $1 --no-condor
exit $?
'''.format(args.settings,args.config,iset,imem,"--sim" if isSim else "--data")
                    )
                    os.system("chmod +x "+working_dir+'/run.sh')
                    
                    njob=min(args.njob[-1],len(c.bins))
                    condor_arguments=[",".join([str(i) for i in range(len(c.bins)) if i%njob==j]) for j in range(njob)]
                    open(working_dir+'/condor.jds','w').write(
'''executable = {0}/run.sh
arguments = $(Process)
output = {0}/job$(Process).out
error = {0}/job$(Process).err
log = {0}/condor.log
concurrency_limits = {1}
jobbatchname = {2}
getenv = True
queue arguments from (
{3}
)
'''.format(working_dir,"n{}.{}".format(args.nmax,os.getenv("USER")),jobbatchname,"\n".join(condor_arguments))
                    )
                    print '[Fitting] {} {}'.format(c.fit_file.split(".",1)[0],c.name)
                    clusterid=submit_condor(working_dir+'/condor.jds')
                    condorlogs[clusterid]=working_dir+'/condor.log'
        print '  Waiting...'
        for clusterid in condorlogs:
            os.system('condor_wait '+condorlogs[clusterid]+' > /dev/null')
            if not check_condor(clusterid,njob):
                exit(1)

####################################################################
##### dumping plots
####################################################################
#    shutil.copy('etc/inputs/index.php.listPlots','%s/index.php' % plottingDir)
#            fitzip = '%s/%s/fitCanvas.zip'%(tnpConf.baseOutDir,flag)
#            with ZipFile(fitzip, 'w') as pngzip:
#                for ib in range(len(tnpBins['bins'])) if args.binNumber<0 else args.binNumber:
#                    tnpRoot.histPlotter( fitfile, tnpBins['bins'][ib], plottingDir )
#                    pngzip.write('%s/%s.png' %(plottingDir,tnpBins['bins'][ib]['name']))

                    #os.remove('%s/%s.png' %(plottingDir,tnpBins['bins'][ib]['name'])) # To save fitcanvas only in zip file. (They are too many to view on web)
#                pngzip.write('%s/index.php' % plottingDir)
#                os.remove('%s/index.php' % plottingDir)
                #os.rmdir('%s/' %plottingDir)
#            print ' ===> Plots saved in <======='
#            print fitzip
#>>>>>>> won/MuonTnP_Spark_v1

####################################################################
##### dumping egamma txt file 
####################################################################
#tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )
#outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)
#flag.histFile='%s/%s_hist.root' % ( outputDirectory , args.flag )
#flag=tnpConf.flags[args.flag]
#flag.fitFile='%s/%s_fit.root' % ( outputDirectory,args.flag )
if "sum" in args.step:
    from efficiencyUtils import make_combined_hist
    print '[Summary] hadd {}'.format(config.data_fit_file)
    exitcode=os.system("hadd -f {0}/{1} $(find {0}/{2} -type f -name '*.root'|sort -V) > /dev/null 2>&1".format(config.path,config.data_fit_file,config.data_fit_file.replace(".root",".d")))
    if exitcode!=0:
        print "hadd failed"
        exit(exitcode)
    print '[Summary] hadd {}'.format(config.sim_fit_file)
    exitcode=os.system("hadd -f {0}/{1} $(find {0}/{2} -type f -name '*.root'|sort -V) > /dev/null 2>&1".format(config.path,config.sim_fit_file,config.sim_fit_file.replace(".root",".d")))
    if exitcode!=0:
        print "hadd failed"
        exit(exitcode)

    hists=[]

    data_hists=[]
    for members in config.make_systematics(isSim=False):
        hist_set=[]
        for member in members:
            hist_set+=[member.make_eff_hist()]
        data_hists+=[hist_set]
    hists+=[make_combined_hist(data_hists)]
    hists+=[make_combined_hist(data_hists,stat=False)]
    hists+=[h for ms in data_hists for h in ms]

    sim_hists=[]
    for members in config.make_systematics(isSim=True):
        hist_set=[]
        for member in members:
            hist_set+=[member.make_eff_hist()]
        sim_hists+=[hist_set]
    hists+=[make_combined_hist(sim_hists)]
    hists+=[make_combined_hist(sim_hists,stat=False)]
    hists+=[h for ms in sim_hists for h in ms]

    sf_hists=[[h.Clone(h.GetName().replace("data_","sf_")) for h in members] for members in data_hists]
    for i in range(len(sf_hists)):
        for j in range(len(sf_hists[i])):
            sf_hists[i][j].Divide(sim_hists[i][j])
    hists+=[make_combined_hist(sf_hists)]
    hists+=[make_combined_hist(sf_hists,stat=False)]
    hists+=[h for ms in sf_hists for h in ms]
    
    f=rt.TFile(config.path+"/efficiency.root","recreate")
    for h in hists:
        h.Write()
    f.Close()

endTime=time.time()
print 'Ends at ', time.strftime('%c',time.localtime(endTime))
print 'Time took', endTime-startTime,'seconds.'
