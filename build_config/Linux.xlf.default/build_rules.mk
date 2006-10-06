# $Id: build_rules.mk,v 1.5.4.9 2006/10/06 18:49:19 theurich Exp $
#
# Linux.xlf.default
#

############################################################
# Default compiler setting.
#
ESMF_F90DEFAULT         = blrts_xlf90
ESMF_CXXDEFAULT         = blrts_xlC

############################################################
# Default MPI setting.
#
ifeq ($(ESMF_COMM),default)
export ESMF_COMM := mpi
endif

############################################################
# MPI dependent settings.
#
ifeq ($(ESMF_COMM),mpiuni)
# MPI stub library -----------------------------------------
ESMF_F90COMPILECPPFLAGS+= -DESMF_MPIUNI
ESMF_CXXCOMPILECPPFLAGS+= -DESMF_MPIUNI
ESMF_CXXCOMPILEPATHS   += -I$(ESMF_DIR)/src/Infrastructure/stubs/mpiuni
ESMF_MPIRUNDEFAULT      = $(ESMF_DIR)/src/Infrastructure/stubs/mpiuni/mpirun
else
ifeq ($(ESMF_COMM),mpi)
# Vendor MPI -----------------------------------------------
ESMF_F90DEFAULT         = mpxlf90
ESMF_F90LINKLIBS       += 
ESMF_CXXDEFAULT         = mpxlC
ESMF_CXXLINKLIBS       += 
ESMF_MPIRUNDEFAULT      = mpirun
else
ifeq ($(ESMF_COMM),user)
# User specified flags -------------------------------------
else
$(error Invalid ESMF_COMM setting: $(ESMF_COMM))
endif
endif
endif

############################################################
# Print compiler version string
#
ESMF_F90COMPILER_VERSION = ${ESMF_F90COMPILER} -qversion
ESMF_CXXCOMPILER_VERSION = ${ESMF_CXXCOMPILER} -qversion

############################################################
# BlueGene does not have support for POSIX IPC (memory mapped files)
#
ESMF_CXXCOMPILECPPFLAGS += -DESMF_NOPOSIXIPC

############################################################
# BlueGene does not have support for Pthreads
#
ESMF_PTHREADS := OFF

############################################################
# xlf90 needs flag to indicate FPP options
#
ESMF_FPPPREFIX           = -WF,

############################################################
# Special debug flags
#
ESMF_F90OPTFLAG_G       += -qcheck -qfullpath
ESMF_CXXOPTFLAG_G       += -qcheck -qfullpath

############################################################
# Blank out variables to prevent rpath encoding
#
ESMF_F90LINKRPATHS      =
ESMF_CXXLINKRPATHS      =

############################################################
# xlf90 does not know about Fortran suffices
#
ESMF_F90COMPILEFREECPP   = -qfree=f90 -qsuffix=cpp=F90
ESMF_F90COMPILEFREENOCPP = -qfree=f90 -qsuffix=f=F
ESMF_F90COMPILEFIXCPP    = -qfixed=132 -qsuffix=cpp=f90
ESMF_F90COMPILEFIXNOCPP  = -qfixed=132 -qsuffix=f=f

############################################################
# Determine link path for xlf frontend
#
ESMF_F90LINKPATHS +=

############################################################
# Determine link path for xlC frontend
#
ESMF_CXXLINKPATHS +=

############################################################
# Link against libesmf.a using the F90 linker front-end
#
ESMF_F90LINKLIBS +=

############################################################
# Link against libesmf.a using the C++ linker front-end
#
ESMF_CXXLINKLIBS +=

############################################################
# Blank out shared library options
#
ESMF_SL_LIBS_TO_MAKE  =
