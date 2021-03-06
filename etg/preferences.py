#---------------------------------------------------------------------------
# Name:        etg/preferences.py
# Author:      Robin Dunn
#
# Created:     28-Feb-2013
# Copyright:   (c) 2013-2018 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "preferences"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxPreferencesEditor",
           "wxPreferencesPage",
           "wxStockPreferencesPage",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPreferencesEditor')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.find('AddPage.page').transfer = True

    c = module.find('wxPreferencesPage')
    c.addPrivateCopyCtor()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

