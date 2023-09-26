def run_lin(input, actions, ext):
  import validators
  import tempfile
  import requests
  import shutil
  import os
  import stat
  import subprocess
  input_file_path = tempfile.NamedTemporaryFile(suffix='.svg').name
  if validators.url(input):
    headers = {'Accept': '*/*', 'X-User-IP': '1.1.1.1'}
    r = requests.get(input, headers=headers, allow_redirects=True)
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
  #path = subprocess.check_output(["inkscape", "--shell", act, input_file_path]) #.decode()
  return output

def run_win(input, actions, ext):
  import validators
  import tempfile
  import requests
  import shutil
  import os
  import stat
  import subprocess
  input_file_path = tempfile.NamedTemporaryFile(suffix='.svg').name
  if validators.url(input):
    headers = {'Accept': '*/*', 'X-User-IP': '1.1.1.1'}
    r = requests.get(input, headers=headers, allow_redirects=True)
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
  #path = subprocess.check_output(["inkscape", "--shell", act, input_file_path]) #.decode()
  return output

def run(input, actions, ext):
  from sys import platform
  if platform == "win32":
    output = run_win(input, actions, ext)
  else :
    output = run_lin(input, actions, ext)
  return output
