def run_lin(input, extension, options, ext):
  import validators
  import tempfile
  import requests
  import shutil
  import os
  import stat
  import subprocess
  input_file_path = tempfile.NamedTemporaryFile(suffix='.svg').name
  if validators.url(input):
    r = requests.get(input, allow_redirects=True)
    open(input_file_path, 'wb').write(r.content)
  else:
    shutil.copyfile(input, input_file_path)
  path = subprocess.check_output(["inkscape", "--system-data-directory"]).decode().replace("\n", "")
  inkscape_extension_path = path + "/extensions/" + extension
  output = tempfile.NamedTemporaryFile(suffix=ext).name
  bat = tempfile.NamedTemporaryFile(suffix='.sh').name
  text = f"#!/bin/bash \n python3 \"{inkscape_extension_path}\" --output=\"{output}\" {options} \"{input_file_path}\"\n"
  with open(bat, mode='w') as f:
    f.write(text)
  st = os.stat(bat)
  os.chmod(bat, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
  subprocess.call([bat])
  return output

def run_win(input, extension, options, ext):
  import validators
  import tempfile
  import requests
  import shutil
  import os
  import stat
  import subprocess
  input_file_path = tempfile.NamedTemporaryFile(suffix='.svg').name
  if validators.url(input):
    r = requests.get(input, allow_redirects=True)
    open(input_file_path, 'wb').write(r.content)
  else:
    shutil.copyfile(input, input_file_path)
  path = subprocess.check_output(["inkscape", "--system-data-directory"]).decode().replace("\n", "")
  inkscape_extension_path = path + "/extensions/" + extension
  output = tempfile.NamedTemporaryFile(suffix=ext).name
  bat = tempfile.NamedTemporaryFile(suffix='.sh').name
  text = f"#!/bin/bash \n python3 \"{inkscape_extension_path}\" --output=\"{output}\" {options} \"{input_file_path}\"\n"
  with open(bat, mode='w') as f:
    f.write(text)
  st = os.stat(bat)
  os.chmod(bat, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
  subprocess.call([bat])
  return output

def run(input, extension, options, ext):
  from sys import platform
  if platform == "win32":
    output = run_win(input, extension, options, ext)
  else :
    output = run_lin(input, extension, options, ext)
  return output
