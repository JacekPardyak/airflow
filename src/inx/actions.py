import validators
import tempfile
import requests
import shutil
import os
import stat
import subprocess
  
def run_lin(input, actions, ext):

  input_file_path = tempfile.NamedTemporaryFile(suffix='.svg').name
  if validators.url(input):
    headers = {'User-Agent': 'INX bot)'}
    r = requests.get(input, allow_redirects=True, headers=headers)
    open(input_file_path, 'wb').write(r.content)
  else:
    shutil.copyfile(input, input_file_path)
  output = tempfile.NamedTemporaryFile(suffix = ext).name
  bat = tempfile.NamedTemporaryFile(suffix='.sh').name
  act = f"--actions=\"{actions}export-filename:{output};export-do\""
  text = f"#!/bin/bash \n inkscape --batch-process {act} \"{input_file_path}\"\n"
  with open(bat, mode='w') as f:
    f.write(text)
  st = os.stat(bat)
  os.chmod(bat, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
  subprocess.call([bat])
  return output

def run_win(input, actions, ext):
  input_file_path = tempfile.NamedTemporaryFile(suffix='.svg').name
  if validators.url(input):
    headers = {'User-Agent': 'INX bot)'}
    r = requests.get(input, allow_redirects=True, headers=headers)
    open(input_file_path, 'wb').write(r.content)
  else:
    shutil.copyfile(input, input_file_path)
  output = tempfile.NamedTemporaryFile(suffix = ext).name
  bat = tempfile.NamedTemporaryFile(suffix='.bat').name
  act = f"--actions=\"{actions}export-filename:{output};export-do\""
  text = f"@ECHO OFF \n inkscape --batch-process {act} \"{input_file_path}\"\n"
  with open(bat, mode='w') as f:
    f.write(text)
  st = os.stat(bat)
  os.chmod(bat, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
  subprocess.call([bat])
  return output

def run(input, actions, ext):
  from sys import platform
  if platform == "win32":
    output = run_win(input, actions, ext)
  else :
    output = run_lin(input, actions, ext)
  return output
