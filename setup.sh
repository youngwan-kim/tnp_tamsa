#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_0/src/
eval `scramv1 runtime -sh`
cd -
export TNP_BASE=`pwd`
export PYTHONPATH=$TNP_BASE/python${PYTHONPATH:+:$PYTHONPATH}
