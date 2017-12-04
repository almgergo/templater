# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 10:33:33 2017

@author: almasyg
"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"includes": ["PyQt5.QtCore","PyQt5.QtWidgets","PyQt5.QtGui"],"packages": ["errno","os","sys","re","codecs"], "excludes": []}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(  name = "Templater",
        version = "0.1",
        description = "Templating stuff!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("templater.py", base=base)])