#---------------------------------------------------------------------------
# Name:        etg/_stc.py
# Author:      Robin Dunn
#
# Created:     24-Oct-2012
# Copyright:   (c) 2012 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import PyFunctionDef, PyCodeDef, PyPropertyDef

PACKAGE   = "wx" 
MODULE    = "_stc"
NAME      = "_stc"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxStyledTextCtrl', 
           'wxStyledTextEvent',
          ]    
    

# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "adv" library in a multi-lib build.
INCLUDES = [ ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from the build scripts to get a list of
# sources and/or additional dependencies when building this extension module.
#ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
#DEPENDS = tools.getNonEtgFiles(INCLUDES)
#OTHERDEPS = [  ]


#---------------------------------------------------------------------------
 
def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    module.addHeaderCode('#include <wxpy_api.h>')
    module.addImport('_core')
    module.addPyCode('import wx', order=10)
    module.addInclude(INCLUDES)
 

    #-----------------------------------------------------------------
    
    module.addHeaderCode('#include <wx/stc/stc.h>')
    
    
    c = module.find('wxStyledTextCtrl')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c, False)
    module.addGlobalStr('wxSTCNameStr')
    

    c.find('GetCurLine.linePos').out = True
    c.find('GetCurLineRaw.linePos').out = True
    

    c.find('GetCharacterPointer').ignore()
    c.addCppMethod('PyObject*', 'GetCharacterPointer', '()',
        doc="""\
            Compact the document buffer and return a read-only memoryview 
            object of the characters in the document.""",
        body="""
            const char* ptr = self->GetCharacterPointer();
            Py_ssize_t len = self->GetLength();
            PyObject* rv;
            wxPyBLOCK_THREADS( rv = wxPyMakeBuffer((void*)ptr, len, true) );
            return rv;
            """)
    
    c.find('GetRangePointer').ignore()
    c.addCppMethod('PyObject*', 'GetRangePointer', '(int position, int rangeLength)',
        doc="""\
            Return a read-only pointer to a range of characters in the 
            document. May move the gap so that the range is contiguous, 
            but will only move up to rangeLength bytes.""",
        body="""
            const char* ptr = self->GetRangePointer(position, rangeLength);
            Py_ssize_t len = rangeLength;
            PyObject* rv;
            wxPyBLOCK_THREADS( rv = wxPyMakeBuffer((void*)ptr, len, true) );
            return rv;
            """)

    # TODO:  Add the UTF8 PyMethods from classic (see _stc_utf8_methods.py)
    


    c = module.find('wxStyledTextEvent')
    tools.fixEventClass(c)
    
    c.addPyCode("""\
        EVT_STC_CHANGE = wx.PyEventBinder( wxEVT_STC_CHANGE, 1 )
        EVT_STC_STYLENEEDED = wx.PyEventBinder( wxEVT_STC_STYLENEEDED, 1 )
        EVT_STC_CHARADDED = wx.PyEventBinder( wxEVT_STC_CHARADDED, 1 )
        EVT_STC_SAVEPOINTREACHED = wx.PyEventBinder( wxEVT_STC_SAVEPOINTREACHED, 1 )
        EVT_STC_SAVEPOINTLEFT = wx.PyEventBinder( wxEVT_STC_SAVEPOINTLEFT, 1 )
        EVT_STC_ROMODIFYATTEMPT = wx.PyEventBinder( wxEVT_STC_ROMODIFYATTEMPT, 1 )
        EVT_STC_KEY = wx.PyEventBinder( wxEVT_STC_KEY, 1 )
        EVT_STC_DOUBLECLICK = wx.PyEventBinder( wxEVT_STC_DOUBLECLICK, 1 )
        EVT_STC_UPDATEUI = wx.PyEventBinder( wxEVT_STC_UPDATEUI, 1 )
        EVT_STC_MODIFIED = wx.PyEventBinder( wxEVT_STC_MODIFIED, 1 )
        EVT_STC_MACRORECORD = wx.PyEventBinder( wxEVT_STC_MACRORECORD, 1 )
        EVT_STC_MARGINCLICK = wx.PyEventBinder( wxEVT_STC_MARGINCLICK, 1 )
        EVT_STC_NEEDSHOWN = wx.PyEventBinder( wxEVT_STC_NEEDSHOWN, 1 )
        EVT_STC_PAINTED = wx.PyEventBinder( wxEVT_STC_PAINTED, 1 )
        EVT_STC_USERLISTSELECTION = wx.PyEventBinder( wxEVT_STC_USERLISTSELECTION, 1 )
        EVT_STC_URIDROPPED = wx.PyEventBinder( wxEVT_STC_URIDROPPED, 1 )
        EVT_STC_DWELLSTART = wx.PyEventBinder( wxEVT_STC_DWELLSTART, 1 )
        EVT_STC_DWELLEND = wx.PyEventBinder( wxEVT_STC_DWELLEND, 1 )
        EVT_STC_START_DRAG = wx.PyEventBinder( wxEVT_STC_START_DRAG, 1 )
        EVT_STC_DRAG_OVER = wx.PyEventBinder( wxEVT_STC_DRAG_OVER, 1 )
        EVT_STC_DO_DROP = wx.PyEventBinder( wxEVT_STC_DO_DROP, 1 )
        EVT_STC_ZOOM = wx.PyEventBinder( wxEVT_STC_ZOOM, 1 )
        EVT_STC_HOTSPOT_CLICK = wx.PyEventBinder( wxEVT_STC_HOTSPOT_CLICK, 1 )
        EVT_STC_HOTSPOT_DCLICK = wx.PyEventBinder( wxEVT_STC_HOTSPOT_DCLICK, 1 )
        EVT_STC_CALLTIP_CLICK = wx.PyEventBinder( wxEVT_STC_CALLTIP_CLICK, 1 )
        EVT_STC_AUTOCOMP_SELECTION = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_SELECTION, 1 )
        EVT_STC_INDICATOR_CLICK = wx.PyEventBinder( wxEVT_STC_INDICATOR_CLICK, 1 )
        EVT_STC_INDICATOR_RELEASE = wx.PyEventBinder( wxEVT_STC_INDICATOR_RELEASE, 1 )
        EVT_STC_AUTOCOMP_CANCELLED = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_CANCELLED, 1 )
        EVT_STC_AUTOCOMP_CHAR_DELETED = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_CHAR_DELETED, 1 )    
        """)
    
    #-----------------------------------------------------------------
       
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    

    
#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()