#! $PYTHONEXE
import sys
sys.path = ["$REPLACEPATH"]+sys.path

import numpy as nm
import numpy.random as ra
import numpy.linalg as la
import clik.parobject as php
import clik
import re
import os.path as osp
import os
import shutil
import h5py
import clik.egfs

def exprep(inar):
  outar = nm.zeros((inar.shape[0]+1,inar.shape[1]-1),dtype=nm.double)
  outar[1:] = inar[:,1:]
  return outar

def gettpl(pars,name,default):
  if hasattr(pars,name):
    fcib = getattr(pars,name)
  else:
    fcib = osp.join(os.environ["CLIK_DATA"],"egfs/%s"%default)
  cibc=nm.loadtxt(fcib)
  ribc = exprep(cibc)
  return ribc
 
def pack256(*li):
  rr=""
  for l in li:
    rr += l+'\0'*(256-len(l))
  return rr

def main(argv):
  pars = clik.miniparse(argv[1])
  
  template_names = ["cib_clustering_template","patchy_ksz_template","homogeneous_ksz_template","tsz_template"]
  # read the templates
  tpls = [gettpl(pars,name,default) for name,default in zip(
    template_names,
    ["clustered_flat.dat","ksz_patchy.dat","ksz_ov.dat","tsz.dat"])]
  
  # read defaults
  defaults = pars.str_array(default=[]).defaults
  values = pars.str_array(default=[]).values
  
  #read pars
  vpars = pars.str_array.pars
  
  codels = pars.str_array(default=[]).models
  
  defs,vpars,pv = clik.egfs.default_models(defmodels=codels,varpars=vpars)
  oefs = dict(zip(defaults,values))
  
  defs.update(oefs)
  defaults = defs.keys()
  values = [defs[k] for k in defaults]
  
  # frequency
  frq = pars.freq
  n_frq = pars.norm_freq
  
  models = ["cib_clustering","cib_poisson","radio_poisson","tsz","ksz"]
  
  defaults += ["nfr"] + ["eff_fr_"+v for v in models] + ["norm_fr_"+v for v in models]
  values   += ["%d"%len(frq.split())]   + [frq]*5                       + [n_frq]*5
  
  # flux cut
  defaults += ["rg_flux_cut"    , "norm_rg_flux_cut"]
  values   += [pars.rg_flux_cut , pars.norm_rg_flux_cut]
  
  shutil.copyfile(pars.input_object,pars.res_object)
  outhf = h5py.File(pars.res_object,"r+")

  lmin = outhf["clik/lkl_0"].attrs["lmin"]
  lmax = outhf["clik/lkl_0"].attrs["lmax"]
  
  if outhf["clik/lkl_0"].attrs["lkl_type"].lower() in ("ivg","gauss","lowly"):
    addon_egfs(outhf,vpars,defaults,values,lmin,lmax,template_names,tpls)
  elif outhf["clik/lkl_0"].attrs["lkl_type"].lower() in ("smica",):
    smica_egfs(outhf,vpars,defaults,values,lmin,lmax,template_names,tpls,frq)

  if "check_param" in outhf["clik"]:
    cls = outhf["clik/check_param"]
    del(outhf["clik/check_param"])
    del(outhf["clik/check_value"])
    outhf.close()
    if hasattr(pars,"test_values"):
      tval = pars.float_array.test_values
      php.add_selfcheck(pars.res_object,nm.concatenate((cls,tval)))
 

def add_xxx(outhf,n_name,name,vpars,defaults,values,lmin,lmax,template_names,tpls):     
  nc = 0
  if n_name in outhf["clik/lkl_0"].attrs.keys():
    nc = outhf["clik/lkl_0"].attrs[n_name]
  agrp = outhf.create_group("clik/lkl_0/%s_%d"%(name,nc))
  nc+=1
  outhf["clik/lkl_0"].attrs[n_name] = nc
  agrp.attrs["ndim"] = len(vpars)
  agrp.attrs["keys"] = pack256(*vpars)
  
  agrp.attrs["ndef"] = len(defaults)
  agrp.attrs["defaults"] = pack256(*defaults)
  agrp.attrs["values"] = pack256(*values)

  agrp.attrs["lmin"] = lmin
  agrp.attrs["lmax"] = lmax

  for nnm,vvv in zip(template_names,tpls):
    agrp.create_dataset(nnm, data=vvv.flat[:])

  return agrp
  
 
def addon_egfs(outhf,vpars,defaults,values,lmin,lmax,template_names,tpls):     
  agrp = add_xxx(outhf,"n_addons","addon",vpars,defaults,values,lmin,lmax,template_names,tpls)
  
  agrp.attrs["addon_type"] = "egfs_single"

def smica_egfs(outhf,vpars,defaults,values,lmin,lmax,template_names,tpls,frq):
  agrp = add_xxx(outhf,"n_component","component",vpars,defaults,values,lmin,lmax,template_names,tpls)
  agrp.attrs["component_type"] = "egfs"

    
import sys
if __name__=="__main__":
  main(sys.argv)