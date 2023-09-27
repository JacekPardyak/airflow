def install_lin():
  import tempfile
  import os
  import stat
  import subprocess
  bat = tempfile.NamedTemporaryFile(suffix='.sh').name
  print(bat)
  text = '''#!/bin/bash
sudo apt install -y software-properties-common > /dev/null 2>&1
sudo apt update > /dev/null 2>&1
sudo add-apt-repository -y ppa:inkscape.dev/stable > /dev/null 2>&1
sudo apt install -y inkscape > /dev/null 2>&1
inkscape --version
'''
  with open(bat, mode='w') as f:
    f.write(text)
  st = os.stat(bat)
  os.chmod(bat, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
  subprocess.call([bat])
  print("Inkscape has been installed")

def install_win():
  import tempfile
  import os
  import stat
  import subprocess
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
  print("Inkscape has been installed")

def install():
  from sys import platform
  if platform == "win32":
    install_win()
  else :
    install_lin()

def version():
  return subprocess.check_output(["inkscape", "--version"]).decode()
