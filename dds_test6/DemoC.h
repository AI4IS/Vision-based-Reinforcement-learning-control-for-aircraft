// -*- C++ -*-
/**
 * Code generated by the The ACE ORB (TAO) IDL Compiler v3.1.0
 * TAO and the TAO IDL Compiler have been developed by:
 *       Center for Distributed Object Computing
 *       Washington University
 *       St. Louis, MO
 *       USA
 * and
 *       Distributed Object Computing Laboratory
 *       University of California at Irvine
 *       Irvine, CA
 *       USA
 * and
 *       Institute for Software Integrated Systems
 *       Vanderbilt University
 *       Nashville, TN
 *       USA
 *       https://www.isis.vanderbilt.edu/
 *
 * Information about TAO is available at:
 *     https://www.dre.vanderbilt.edu/~schmidt/TAO.html
 **/

// TAO_IDL - Generated from
// C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_codegen.cpp:148

#ifndef _TAO_IDL_DEMOC_Y4HZIF_H_
#define _TAO_IDL_DEMOC_Y4HZIF_H_

#include /**/ "ace/pre.h"


#include /**/ "ace/config-all.h"

#if !defined (ACE_LACKS_PRAGMA_ONCE)
# pragma once
#endif /* ACE_LACKS_PRAGMA_ONCE */


#include "tao/ORB.h"
#include "tao/Basic_Types_IDLv4.h"
TAO_BEGIN_VERSIONED_NAMESPACE_DECL

namespace CORBA
{
  using namespace IDLv4;
}

TAO_END_VERSIONED_NAMESPACE_DECL

#include "tao/String_Manager_T.h"
#include "tao/VarOut_T.h"
#include "tao/Arg_Traits_T.h"
#include "tao/Basic_Arguments.h"
#include "tao/Special_Basic_Arguments.h"
#include "tao/Any_Insert_Policy_T.h"
#include "tao/Fixed_Size_Argument_T.h"
#include "tao/Var_Size_Argument_T.h"
#include "tao/UB_String_Arguments.h"
#include /**/ "tao/Version.h"
#include /**/ "tao/Versioned_Namespace.h"

#if TAO_MAJOR_VERSION != 3 || TAO_MINOR_VERSION != 1 || TAO_MICRO_VERSION != 0
#error This file should be regenerated with TAO_IDL
#endif
// TAO_IDL - Generated from
// C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_visitor_module\module_ch.cpp:34

namespace DemoIdlModule
{
  // TAO_IDL - Generated from
  // C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_type.cpp:257

  

  struct DemoTopic1;
  using DemoTopic1_var = ::TAO_Var_Var_T<DemoTopic1>;
  using DemoTopic1_out = ::TAO_Out_T<DemoTopic1>;

  
  // TAO_IDL - Generated from
  // C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_visitor_structure\structure_ch.cpp:47

  

  struct  DemoTopic1
  {
    // TAO_IDL - Generated from
    // C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_type.cpp:296

    
    using _var_type = DemoTopic1_var;
    using _out_type = DemoTopic1_out;
    
    ::CORBA::Long id;
    ::CORBA::Long counter;
    ::TAO::String_Manager text;
  };


// TAO_IDL - Generated from
// C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_visitor_module\module_ch.cpp:62


} // module DemoIdlModule
// TAO_IDL - Generated from
// C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_visitor_arg_traits.cpp:64



TAO_BEGIN_VERSIONED_NAMESPACE_DECL


// Arg traits specializations.
namespace TAO
{
  // TAO_IDL - Generated from
  // C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_visitor_arg_traits.cpp:931

  

  template<>
  class Arg_Traits< ::DemoIdlModule::DemoTopic1>
    : public
        Var_Size_Arg_Traits_T<
            ::DemoIdlModule::DemoTopic1,
            TAO::Any_Insert_Policy_Noop
          >
  {
  };
}

TAO_END_VERSIONED_NAMESPACE_DECL


// TAO_IDL - Generated from
// C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_visitor_traits.cpp:58



TAO_BEGIN_VERSIONED_NAMESPACE_DECL

// Traits specializations.
namespace TAO
{
}
TAO_END_VERSIONED_NAMESPACE_DECL


// TAO_IDL - Generated from
// C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_visitor_structure\cdr_op_ch.cpp:37


TAO_BEGIN_VERSIONED_NAMESPACE_DECL

 ::CORBA::Boolean operator<< (TAO_OutputCDR &, const DemoIdlModule::DemoTopic1 &);
 ::CORBA::Boolean operator>> (TAO_InputCDR &, DemoIdlModule::DemoTopic1 &);

TAO_END_VERSIONED_NAMESPACE_DECL


// TAO_IDL - Generated from
// C:\Users\admin\Desktop\opendds\ACE_wrappers\TAO\TAO_IDL\be\be_codegen.cpp:1648

#if defined (__ACE_INLINE__)
#include "DemoC.inl"
#endif /* defined INLINE */

#include /**/ "ace/post.h"

#endif /* ifndef */

