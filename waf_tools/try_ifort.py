import re
import sys
import Options
import os.path as osp
from waflib import Logs
from waflib import  Context
from waflib import Errors

def options(ctx):
  ctx.add_option("--gfortran",action="store_true",default=False,help="Do not test for ifort and only use gfortran")
  ctx.add_option("--fortran_flagline",action="store",default="",help="flagline to link fortran object using ld")

def configure(ctx):
  if ctx.options.fortran_flagline:
    conf.parse_flags(ctx.options.fortran_flagline,uselib="fc_runtime")
  if sys.platform.lower()=="darwin":
    ctx.env.fcshlib_PATTERN = 'lib%s.dylib'


  if not Options.options.gfortran:
    try:
      ifort_conf(ctx)
      return
    except Exception,e:
      Logs.pprint("PINK", "ifort not found, defaulting to gfortran (cause: '%s')"%e)
  gfortran_conf(ctx)
  
  
def ifort_conf(ctx):
  ctx.check_tool('ifort')
  if sys.platform.lower()=="darwin":
    ctx.env.LINKFLAGS_fcshlib = ['-dynamiclib']
  ctx.env.append_value('FCFLAGS',ctx.env.mopt.split())
  ctx.env.append_value("FCFLAGS_fc_omp","-openmp")
  if not ctx.options.fortran_flagline:
    if "/" not in ctx.env.FC:
      ctx.env.FC = ctx.cmd_and_log("which %s"%ctx.env.FC).strip()
      print ctx.env.FC
    ifort_path = osp.dirname(osp.realpath(ctx.env.FC))
    #print ifort_path
    if ctx.options.m32:
      try:
        f=open(osp.join(ifort_path,'ifortvars_ia32.sh'))
      except:
        raise Errors.WafError("Can't locate ifort configuration file")
    else:
      try:
        f=open(osp.join(ifort_path,'ifortvars_intel64.sh'))
      except:
        raise Errors.WafError("Can't locate ifort configuration file")

    txt = f.read()
    f.close()
    #print txt
    if sys.platform.lower()=="darwin":
      sp = "DYLD_LIBRARY_PATH"
    else:
      sp = "LD_LIBRARY_PATH"
    res = re.findall("\s"+sp+"\s*=\s*\"(.+)\"",txt)[0]
    for pth in res.split(":"):
      ctx.env.append_value("LIBPATH_fc_runtime",pth)
      ctx.env.append_value("RPATH_fc_runtime",pth)
    ctx.env.append_value("LIB_fc_runtime",["ifcore","intlc","ifport","imf","irc","svml","iomp5","pthread"])
    ctx.env.FCSHLIB_MARKER = [""]
    ctx.env.FCSTLIB_MARKER = [""]

  
def gfortran_conf(ctx):
  ctx.check_tool('gfortran')
  ctx.env.append_value("FCFLAGS_fc_omp","-fopenmp")
  ctx.env.append_value("FCFLAGS","-DGFORTRAN")
  mopt = ctx.env.mopt
  if sys.platform.lower()=="darwin":
    if "i386" in ctx.env.mopt:
      ctx.env.append_value('FCFLAGS','-m32')
      mopt = "-m32"
    else:
      ctx.env.append_value('FCFLAGS','-m64')
      mopt = "-m64"
  else:
    ctx.env.append_value('FCFLAGS',ctx.env.mopt.split())
  
  v90 = ctx.cmd_and_log(ctx.env.FC+" --version",quiet=Context.STDOUT).split("\n")[0].strip()
  version90 = re.findall("(4\.[0-9]\.[0-9])",v90)
  if len(version90)<1:
    Logs.pprint("PINK","Can't get gfortran version... Let's hope for the best")
  else:
    version90 = version90[0]
    vmid = int(version90.split(".")[1])
    if vmid<3:
      raise Errors.WafError("need gfortran version above 4.3 got %s"%version90)
  lgfpath = ctx.cmd_and_log(ctx.env.FC+" %s -print-file-name=libgfortran.dylib"%mopt,quiet=Context.STDOUT)    
  lpath = [osp.dirname(osp.realpath(lgfpath))]
  lgfpath = ctx.cmd_and_log(ctx.env.FC+" %s -print-file-name=libgomp.dylib"%mopt,quiet=Context.STDOUT)    
  lpath += [osp.dirname(osp.realpath(lgfpath))]
  lpath = set(lpath)
  
  ctx.env.append_value("LIB_fc_runtime",["gfortran","gomp"])
  ctx.env.append_value("LIBPATH_fc_runtime",list(lpath))
  ctx.env.append_value("RPATH_fc_runtime",list(lpath))
  # kludge !
  ctx.env.FCSHLIB_MARKER = [""]
  ctx.env.FCSTLIB_MARKER = [mopt]
  