import autoinstall_lib as atl

version = "hdf5-1.8.7"
tool = "hdf5"

#print "-> loading %s autoinstall (using version %s)"%(tool,version)

def options(opt):
  atl.add_lib_option(tool,opt,install=True)
  
def configure(ctx):
  atl.conf_lib(ctx,tool,["hdf5","hdf5_hl"],"H5Fcreate","hdf5.h",defines="HAS_HDF5",install=installhdf5)  
  try:
    kw={}
    kw["fragment"] = '''#include "hdf5.h"
    #include <stdio.h> 
    int main() {
    herr_t res;
    unsigned int majnum,minnum,relnum;
    res = H5get_libversion(&majnum, &minnum, &relnum );
    if (res<0) return -1;
    printf("%d.%d.%d",majnum,minnum,relnum);
    return 0;}'''
    kw["use"] = "hdf5"
    kw["execute"] = "true"
    kw['compiler']='c'
    kw['define_ret'] = "HDF5_VERSION"
    ctx.validate_c(kw)
    ctx.start_msg('Checking for hdf5 version (>1.8)')
    ret=None
    try:
      ret=ctx.run_c_code(**kw)
    except ctx.errors.ConfigurationError ,e:
      ctx.end_msg(kw['errmsg'],'YELLOW')
      if Logs.verbose>1:
        raise
      else:
        ctx.fatal('The configuration failed')
    else:
      if int(ret.split(".")[1])!=8:
        ctx.end_msg(ret,"YELLOW")
        raise Exception("Atrgl")
      else:
        ctx.end_msg(ret)
  except Exception,e:
    print e
    atl.conf_lib(ctx,tool,["hdf5","hdf5_hl"],"H5Fcreate","hdf5.h",defines="HAS_HDF5",install=installhdf5,forceinstall=True)  
        
def installhdf5(ctx):
  filen = version+".tar.gz"
  atl.installsmthg_pre(ctx,"http://www.hdfgroup.org/ftp/HDF5/prev-releases/"+version+"/src/"+filen,filen)
  atl.installsmthg_post(ctx,version,tool)
