import sys
from cx_Freeze import setup, Executable

include_files = ['images/dir.png', 'images/file.png', 'images/cdtoparent.png']
build_exe_options = {
    'packages': [],#'sys', 'PySide.QtCore', 'PySide.QtGui', 'irods', 'irods.session'],
    'excludes': ['Tkinter', 'Tkconstants', 'tcl'],
    #'build_exe': 'build',
    'include_files': include_files
}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
      name='irodsbrowser',
      version='0.1.0',
      author='Nick Eddy',
      options = {'build_exe': build_exe_options, 'install_exe': { 'build_dir': 'dist' }},
      executables = [Executable('irodsbrowser.py', base=base)],
      requires=['PySide', 'cx_Freeze',]
      )
