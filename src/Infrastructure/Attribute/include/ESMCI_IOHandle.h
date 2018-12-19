// $Id$
//
// Earth System Modeling Framework
// Copyright 2002-2018, University Corporation for Atmospheric Research,
// Massachusetts Institute of Technology, Geophysical Fluid Dynamics
// Laboratory, University of Michigan, National Centers for Environmental
// Prediction, Los Alamos National Laboratory, Argonne National Laboratory,
// NASA Goddard Space Flight Center.
// Licensed under the University of Illinois-NCSA License.
//
//-----------------------------------------------------------------------------

#ifndef ESMCI_IOHANDLE_H
#define ESMCI_IOHANDLE_H

#include <fstream>
#include <vector>

#include <netcdf.h>
#include <pio.h>

#include "ESMCI_Array.h"
#include "ESMCI_Attributes.h"
#include "ESMCI_DistGrid.h"
#include "ESMCI_Metadata.h"
#include "ESMCI_Util.h"
#include "json.hpp"

using json = nlohmann::json;  // Convenience rename for JSON namespace.
using namespace std;

//-----------------------------------------------------------------------------
//BOP
// !CLASS:  IOHandle
//
// !DESCRIPTION:
//
//-----------------------------------------------------------------------------
//
// !USES:

namespace ESMCI {

namespace PIOARG {
  const string DIMIDS = "dimids";
  const string FILENAME = "filename";
  const string IOIDS = "ioids";
  const string IOSYSID = "iosysid";
  const string IOTYPE = "iotype";
  const string MODE = "mode";
  const string NCID = "ncid";
  const string VARIDS = "varids";
}

namespace PIODEF {
  const int REARRANGER = PIO_REARR_SUBSET;
}

//-----------------------------------------------------------------------------

class IOHandle {

public:
  ESMCI::Metadata meta;
  json PIOArgs = json::object();

private:
  int getOrCreateGroup(int& rc);
  int getOrCreateDimension(int& rc);
  int getOrCreateVariable(int& rc);
  int init(int& rc);

public:
  IOHandle(void) = default;  // Default constructor
  ~IOHandle(void) = default; // Default destructor
  IOHandle(IOHandle&&) = delete; // Move constructor
  IOHandle(const IOHandle&) = delete; // Copy constructor
  IOHandle&operator=(const IOHandle&) = delete; // Copy assignment
  IOHandle&operator=(IOHandle&&) = delete; // Move assignment

  void close(int& rc);
  void dodef(int& rc);
  void enddef(int& rc);
  void finalize(int& rc);
  void open(int& rc);
  void read(int& rc);
  void write(const Array& arr, int& rc);

};

//-----------------------------------------------------------------------------

} // namespace

// Fortran interface functions
extern "C" {

}  // extern "C"

#endif  // ifdef barrier