// $Id: ESMC_Fraction.h,v 1.2 2004/11/05 04:07:25 eschwab Exp $
//
// Earth System Modeling Framework
// Copyright 2002-2003, University Corporation for Atmospheric Research,
// Massachusetts Institute of Technology, Geophysical Fluid Dynamics
// Laboratory, University of Michigan, National Centers for Environmental
// Prediction, Los Alamos National Laboratory, Argonne National Laboratory,
// NASA Goddard Space Flight Center.
// Licensed under the GPL.
//
// ESMF Fraction C++ definition include file
//
// (all lines below between the !BOP and !EOP markers will be included in
//  the automated document processing.)
//-------------------------------------------------------------------------
//
 // these lines prevent this file from being read more than once if it
 // ends up being included multiple times

#ifndef ESMC_FRACTION_H
#define ESMC_FRACTION_H

//-------------------------------------------------------------------------

 // Put any constants or macros which apply to the whole component in this file.
 // Anything public or esmf-wide should be up higher at the top level
 // include files.

//-------------------------------------------------------------------------
//BOP
//
// !CLASS: ESMC_Fraction - represent and manipulate rational fractions
//
// !DESCRIPTION:
//      ESMF C++ {\tt ESMC_Fraction} class
//
//-------------------------------------------------------------------------
//
// !USES:
#include <ESMC_Base.h>  // all classes inherit from the ESMC Base class.

// !PUBLIC TYPES:
 class ESMC_Fraction;

// !PRIVATE TYPES:
 // class configuration type:  not needed for ESMC_Fraction

 // class definition type
class ESMC_Fraction
{
  private:
    ESMF_KIND_I8 w;  // Integer (whole) seconds (signed)
    ESMF_KIND_I4 n;  // Integer fraction (exact) n/d; numerator (signed)
    ESMF_KIND_I4 d;  // Integer fraction (exact) n/d; denominator

// !PUBLIC MEMBER FUNCTIONS:

  public:
    // native C++ style Set/Get
    int ESMC_FractionSet(ESMF_KIND_I8 w, ESMF_KIND_I4 n, ESMF_KIND_I4 d);
    int ESMC_FractionSetw(ESMF_KIND_I8 w);
    int ESMC_FractionSetn(ESMF_KIND_I4 n);
    int ESMC_FractionSetd(ESMF_KIND_I4 d);
    ESMF_KIND_I8 ESMC_FractionGetw(void) const;
    ESMF_KIND_I4 ESMC_FractionGetn(void) const;
    ESMF_KIND_I4 ESMC_FractionGetd(void) const;

    // Set/Get to support F90 optional argument style
    int ESMC_FractionSet(ESMF_KIND_I8 *w, ESMF_KIND_I4 *n, ESMF_KIND_I4 *d);
    int ESMC_FractionGet(ESMF_KIND_I8 *w, ESMF_KIND_I4 *n,
                         ESMF_KIND_I4 *d) const;

    int ESMC_FractionNormalize(void);
    int ESMC_FractionReduce(void);
    int ESMC_FractionConvert(ESMF_KIND_I4 denominator);

    // comparison methods (TMG 1.5.3, 2.4.3, 7.2)
    bool operator==(const ESMC_Fraction &) const;
    bool operator!=(const ESMC_Fraction &) const;
    bool operator< (const ESMC_Fraction &) const;
    bool operator> (const ESMC_Fraction &) const;
    bool operator<=(const ESMC_Fraction &) const;
    bool operator>=(const ESMC_Fraction &) const;

    // increment, decrement methods (TMG 1.5.4, 2.4.4, 2.4.5, 2.4.6, 5.1, 5.2,
    //                                   7.2)
    ESMC_Fraction  operator+ (const ESMC_Fraction &) const;
    ESMC_Fraction  operator- (const ESMC_Fraction &) const;
    ESMC_Fraction& operator+=(const ESMC_Fraction &);
    ESMC_Fraction& operator-=(const ESMC_Fraction &);

    // explicit assignment operator to support ESMC_BaseTime::operator=
    // and ESMC_TimeInterval::operator=
    // TODO:  should be implicit ?
    ESMC_Fraction& operator=(const ESMC_Fraction &);

    // internal validation
    int ESMC_FractionValidate(const char *options=0) const;

    // for testing/debugging
    int ESMC_FractionPrint(const char *options=0) const;

    // native C++ constructor/destructors
    ESMC_Fraction(void);
    ESMC_Fraction(ESMF_KIND_I8 w, ESMF_KIND_I4 n=0, ESMF_KIND_I4 d=1);
    ESMC_Fraction(int w, int n=0, int d=1);
    ~ESMC_Fraction(void);

 // < declare the rest of the public interface methods here >

// !PRIVATE MEMBER FUNCTIONS:
//
  private:
//
 // < declare private interface methods here >
//
//EOP
//-------------------------------------------------------------------------

};  // end class ESMC_Fraction

    // related general utility functions which do not operate on fraction
    //   objects directly
    ESMF_KIND_I4 ESMC_FractionGCD(ESMF_KIND_I4 a, ESMF_KIND_I4 b);
    ESMF_KIND_I4 ESMC_FractionLCM(ESMF_KIND_I4 a, ESMF_KIND_I4 b);

#endif // ESMC_FRACTION_H
