import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    'packages': ['sys', 'PySide.QtCore', 'PySide.QtGui', 'irods', 'irods.session'],
    'excludes': ['Tkinter', 'Tkconstants', 'tcl'],
    'build_exe': 'build',
}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
      name='irodsbrowser',
      version='0.1.0',
      author='Nick Eddy',
      options = {'build_exe': build_exe_options},
      executables = [Executable('irodsbrowser.py', base=base)],
      requires=['PySide', 'cx_Freeze',]
      )