#!/usr/bin/env python
###############################################################################
# (c) Copyright 2000-2018 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import importlib.resources


class LHCbStyle:
    def __init__(self, print_msg=False):
        """
        Load the macro if not already loaded.
        Provide easy access to the pointers declared in the LHCbStyle namespace.
        """
        self._print_msg = print_msg
        if not hasattr(self._ROOT, "lhcbStyle"):
            with importlib.resources.path("lhcbstyle", "lhcbStyle.C") as path:
                self._ROOT.gROOT.LoadMacro(str(path))
        self.lhcbStyle = self._ROOT.LHCbStyle.lhcbStyle
        self.create_label = self._ROOT.LHCbStyle.create_label
        self.lhcbLabel = self._ROOT.LHCbStyle.lhcbLabel
        self.lhcbLatex = self._ROOT.LHCbStyle.lhcbLatex

    def __enter__(self):
        """
        For context management, store the original global style so it can be reset later
        """
        self.old_style = self._ROOT.gStyle.GetName()
        self.apply()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Return the global style to its original state
        """
        self._ROOT.gROOT.SetStyle(self.old_style)

    def apply(self):
        """
        Execute the main function of the macro, which sets the global style to LHCbStyle
        """
        self._ROOT.lhcbStyle(self._print_msg)

    @property
    def _ROOT(self):
        """
        Property to avoid importing ROOT until absolutely necessary
        """
        import ROOT

        return ROOT
