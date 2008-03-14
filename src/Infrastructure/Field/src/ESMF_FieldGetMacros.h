#if 0
! $Id: ESMF_FieldGetMacros.h,v 1.15.2.7 2008/03/14 04:14:18 theurich Exp $
!
! Earth System Modeling Framework
! Copyright 2002-2007, University Corporation for Atmospheric Research,
! Massachusetts Institute of Technology, Geophysical Fluid Dynamics
! Laboratory, University of Michigan, National Centers for Environmental
! Prediction, Los Alamos National Laboratory, Argonne National Laboratory,
! NASA Goddard Space Flight Center.
! Licensed under the University of Illinois-NCSA License.
!
!==============================================================================
!
#endif
#if 0
!------------------------------------------------------------------------------
! Macros for the Field class Get methods.
!------------------------------------------------------------------------------
#endif

#define FieldGetDataPtrDoc() \
!------------------------------------------------------------------------------ @\
! <Created by macro - do not edit directly > @\
!BOP @\
! !IROUTINE: ESMF_FieldGetDataPtr - Get the Fortran data pointer from a Field @\
! @\
! !INTERFACE: @\
! ! Private name; call using ESMF_FieldGetDataPtr() @\
!   subroutine ESMF_FieldGetDataPtr<rank><type><kind>(field, farray, & @\
!          localDE, exclusiveLBound, exclusiveUBound, exclusiveCount, & @\
!          computationalLBound, computationalUBound, computationalCount, & @\
!          totalLBound, totalUBound, totalCount, & @\
!          rc) @\
! @\
! !ARGUMENTS: @\
!      type(ESMF_Field), intent(in)            :: field @\
!      <type> (ESMF_KIND_<kind>), dimension(<rank>), pointer  :: farray @\
!      integer,          intent(in) , optional :: localDE @\
!      integer,          intent(out), optional :: exclusiveLBound(:) @\
!      integer,          intent(out), optional :: exclusiveUBound(:) @\
!      integer,          intent(out), optional :: exclusiveCount(:) @\
!      integer,          intent(out), optional :: computationalLBound(:) @\
!      integer,          intent(out), optional :: computationalUBound(:) @\
!      integer,          intent(out), optional :: computationalCount(:) @\
!      integer,          intent(out), optional :: totalLBound(:) @\
!      integer,          intent(out), optional :: totalUBound(:) @\
!      integer,          intent(out), optional :: totalCount(:) @\
!      integer,          intent(out), optional :: rc @\
! @\
! !DESCRIPTION: @\
!     Get a Fortran pointer to DE-local memory allocation within {\tt field}. @\
!     For convenience DE-local bounds can be queried at the same time. @\
! @\
!     The arguments are: @\
!     \begin{description} @\
!     \item [field]  @\
!       {\tt ESMF\_Field} object. @\
!     \item [farray] @\
!       Fortran array pointer which will be pointed at DE-local memory allocation. @\
!     \item[{[localDE]}] @\
!       The local DE from which to get the information.  If not set, defaults to  @\
!       the first DE on this PET. (localDE starts at 0 for each PET) @\
!     \item[{[exclusiveLBound]}] @\
!       Upon return this holds the lower bounds of the exclusive region. @\
!       {\tt exclusiveLBound} must be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item[{[exclusiveUBound]}] @\
!       Upon return this holds the upper bounds of the exclusive region. @\
!       {\tt exclusiveUBound} must be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item[{[exclusiveCount]}] @\
!       Upon return this holds the number of items in the exclusive region per dimension @\
!       (i.e. {\tt exclusiveUBound-exclusiveLBound+1}). {\tt exclusiveCount} must @\
!       be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item[{[computationalLBound]}] @\
!       Upon return this holds the lower bounds of the computational region. @\
!       {\tt computationalLBound} must be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item[{[computationalUBound]}] @\
!       Upon return this holds the lower bounds of the computational region. @\
!       {\tt computationalLBound} must be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item[{[computationalCount]}] @\
!       Upon return this holds the number of items in the computational region per dimension @\
!       (i.e. {\tt computationalUBound-computationalLBound+1}). {\tt computationalCount} must @\
!       be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item[{[totalLBound]}] @\
!       Upon return this holds the lower bounds of the total region. @\
!       {\tt totalLBound} must be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item[{[totalUBound]}] @\
!       Upon return this holds the lower bounds of the total region. @\
!       {\tt totalUBound} must be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item[{[totalCount]}] @\
!       Upon return this holds the number of items in the total region per dimension @\
!       (i.e. {\tt totalUBound-totalLBound+1}). {\tt computationalCount} must @\
!       be allocated to be of size equal to {\tt field}|s {\tt dimCount}. @\
!       See section \ref{sec:field:usage:bounds} for a description @\
!       of the regions and their associated bounds and counts.  @\
!     \item [{[rc]}]  @\
!       Return code; equals {\tt ESMF\_SUCCESS} if there are no errors. @\
!     \end{description} @\
! @\
!EOP @\

#if 0
!------------------------------------------------------------------------------
! Get the data pointer from a ESMF_Field
!------------------------------------------------------------------------------
#endif

#define FieldGetDataPtrMacro(mname, mtypekind, mrank, mdim, mlen, mrng, mloc) \
!------------------------------------------------------------------------------ @\
! <Created by macro - do not edit directly > @\
^undef  ESMF_METHOD @\
^define ESMF_METHOD "ESMF_FieldGetDataPtr" @\
    subroutine ESMF_FieldGetDataPtr##mrank##D##mtypekind(field, farray, & @\
          localDE, exclusiveLBound, exclusiveUBound, exclusiveCount, & @\
          computationalLBound, computationalUBound, computationalCount, & @\
          totalLBound, totalUBound, totalCount, & @\
          rc) @\
 @\
! input arguments @\
      type(ESMF_Field), intent(in)            :: field @\
      mname (ESMF_KIND_##mtypekind), dimension(mdim), pointer :: farray @\
      integer,          intent(in) , optional :: localDE @\
      integer,          intent(out), optional :: exclusiveLBound(:) @\
      integer,          intent(out), optional :: exclusiveUBound(:) @\
      integer,          intent(out), optional :: exclusiveCount(:) @\
      integer,          intent(out), optional :: computationalLBound(:) @\
      integer,          intent(out), optional :: computationalUBound(:) @\
      integer,          intent(out), optional :: computationalCount(:) @\
      integer,          intent(out), optional :: totalLBound(:) @\
      integer,          intent(out), optional :: totalUBound(:) @\
      integer,          intent(out), optional :: totalCount(:) @\
      integer,          intent(out), optional :: rc @\
 @\
! local variables @\
      integer          :: localrc, lde @\
 @\
      if (present(rc)) rc = ESMF_RC_NOT_IMPL @\
      localrc = ESMF_RC_NOT_IMPL @\
 @\
      ! check variables @\
      ESMF_INIT_CHECK_DEEP(ESMF_FieldGetInit,field,rc) @\
 @\
      call ESMF_ArrayGet(field%ftypep%array, farrayPtr=farray, rc=localrc) @\
 @\
      if (ESMF_LogMsgFoundError(localrc, & @\
          ESMF_ERR_PASSTHRU, & @\
          ESMF_CONTEXT, rc)) return @\
 @\
      if(present(localDE)) then @\
            lde = localDE @\
      else @\
            lde = 0 @\
      end if @\
      call ESMF_FieldGetDataBounds(field, lde, & @\
          exclusiveLBound, exclusiveUBound, exclusiveCount, & @\
          computationalLBound, computationalUBound, computationalCount, & @\
          totalLBound, totalUBound, totalCount, & @\
          rc = localrc) @\
 @\
      if (ESMF_LogMsgFoundError(localrc, & @\
          ESMF_ERR_PASSTHRU, & @\
          ESMF_CONTEXT, rc)) return @\
 @\
      if (present(rc)) rc = ESMF_SUCCESS @\
 @\
    end subroutine ESMF_FieldGetDataPtr##mrank##D##mtypekind  @\
 @\
! < end macro - do not edit directly >  @\
!------------------------------------------------------------------------------ @\

