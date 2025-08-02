/*
 * Copyright (c) 2024
 *	Side Effects Software Inc.  All rights reserved.
 *
 * Redistribution and use of Houdini Development Kit samples in source and
 * binary forms, with or without modification, are permitted provided that the
 * following conditions are met:
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 * 2. The name of Side Effects Software may not be used to endorse or
 *    promote products derived from this software without specific prior
 *    written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY SIDE EFFECTS SOFTWARE `AS IS' AND ANY EXPRESS
 * OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
 * NO EVENT SHALL SIDE EFFECTS SOFTWARE BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
 * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *----------------------------------------------------------------------------
 * The <TEMPLATE> SOP
 */

#include "SOP_<TEMPLATE>.h"

// This is an automatically generated header file based on theDsFile, below,
// to provide SOP_<TEMPLATE>Parms, an easy way to access parameter values from
// SOP_<TEMPLATE>Verb::cook with the correct type.
#include "SOP_<TEMPLATE>.proto.h"

#include <GU/GU_Detail.h>
#include <OP/OP_Operator.h>
#include <OP/OP_OperatorTable.h>
#include <PRM/PRM_Include.h>
#include <PRM/PRM_TemplateBuilder.h>
#include <UT/UT_DSOVersion.h>
#include <UT/UT_Interrupt.h>
#include <UT/UT_StringHolder.h>
#include <SYS/SYS_Math.h>
#include <limits.h>

using namespace UT::Literal;
using namespace HDK_Sample;

const UT_StringHolder SOP_<TEMPLATE>::theSOPTypeName("hdk_<TEMPLATE>"_sh);

void
newSopOperator(OP_OperatorTable *table)
{
    table->addOperator(new OP_Operator(
        SOP_<TEMPLATE>::theSOPTypeName,
        "<TEMPLATE>",
        SOP_<TEMPLATE>::myConstructor,
        SOP_<TEMPLATE>::buildTemplates(),
        0,
        0,
        nullptr,
        OP_FLAG_GENERATOR));
}

static const char *theDsFile = R"THEDSFILE(
{
    name        parameters
    // No parameters defined
}
)THEDSFILE";

PRM_Template*
SOP_<TEMPLATE>::buildTemplates()
{
    static PRM_TemplateBuilder templ("SOP_<TEMPLATE>.C"_sh, theDsFile);
    return templ.templates();
}

class SOP_<TEMPLATE>Verb : public SOP_NodeVerb
{
public:
    SOP_<TEMPLATE>Verb() {}
    virtual ~SOP_<TEMPLATE>Verb() {}

    virtual SOP_NodeParms *allocParms() const { return new SOP_<TEMPLATE>Parms(); }
    virtual UT_StringHolder name() const { return SOP_<TEMPLATE>::theSOPTypeName; }

    virtual CookMode cookMode(const SOP_NodeParms *parms) const { return COOK_GENERIC; }

    virtual void cook(const CookParms &cookparms) const;

    static const SOP_NodeVerb::Register<SOP_<TEMPLATE>Verb> theVerb;
};

const SOP_NodeVerb::Register<SOP_<TEMPLATE>Verb> SOP_<TEMPLATE>Verb::theVerb;

const SOP_NodeVerb *
SOP_<TEMPLATE>::cookVerb() const 
{ 
    return SOP_<TEMPLATE>Verb::theVerb.get();
}

void
SOP_<TEMPLATE>Verb::cook(const SOP_NodeVerb::CookParms &cookparms) const
{
    GU_Detail *detail = cookparms.gdh().gdpNC();
    // Clear any existing geometry
    detail->clearAndDestroy();
}
