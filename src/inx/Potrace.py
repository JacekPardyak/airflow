import tempfile
import os
import stat
import subprocess
from sys import platform
  
def install_lin():
  bat = tempfile.NamedTemporaryFile(suffix='.sh').name
  print(bat)
  text = '''#!/bin/bash
sudo apt-get update > /dev/null 2>&1
sudo apt-get install potrace > /dev/null 2>&1
potrace --version
'''
  with open(bat, mode='w') as f:
    f.write(text)
  st = os.stat(bat)
  os.chmod(bat, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
  subprocess.call([bat])
  print("Potrace has been installed")

def install_win():
  "TO DO"
  bat = tempfile.NamedTemporaryFile(suffix='.bat').name
  print(bat)
  text = '''@echo off
winget install -e --id Inkscape.Inkscape
inkscape --version
'''
  print(text)
  with open(bat, mode='w') as f:
    f.write(text)
  subprocess.call([bat])
  print("Potrace has been installed")

def install():
  if platform == "win32":
    install_win()
  else :
    install_lin()

def version():
  try:
    p = subprocess.check_output(["potrace", "--version"]).decode().replace("\n", "")
  except:
    p = "Potrace is not installed. Try Potrace.install()"
  return p
