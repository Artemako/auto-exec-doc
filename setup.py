import sys

from cx_Freeze import setup, Executable

setup(name = "AutoExecDoc",
      version = "0.1",
      description = "AutoExecDoc",
      executables = [Executable("main.py")])