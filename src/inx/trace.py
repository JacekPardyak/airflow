import validators
import tempfile
import requests
import shutil
from PIL import Image
import os
import stat
import subprocess
from sys import platform

def run_lin(input, options):
  input_file_path = tempfile.NamedTemporaryFile(suffix='.png').name
  input_bitmap_path = tempfile.NamedTemporaryFile(suffix='.bmp').name
  output = tempfile.NamedTemporaryFile(suffix='.svg').name
  if validators.url(input):
    headers = {'User-Agent': 'INX bot)'}
    r = requests.get(input, allow_redirects=True, headers=headers)
    open(input_file_path, 'wb').write(r.content)
  else:
    shutil.copyfile(input, input_file_path)
  Image.open(input_file_path).save(input_bitmap_path)
  bat = tempfile.NamedTemporaryFile(suffix='.sh').name
  text = f"#!/bin/bash \n potrace \"{input_bitmap_path}\" --output=\"{output}\" {options} \n"
  with open(bat, mode='w') as f:
    f.write(text)
  st = os.stat(bat)
  os.chmod(bat, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
  subprocess.call([bat])
  return output

def run_win(input, options):
  output = "TO DO"
  return output

def run(input, options):
  if platform == "win32":
    output = run_win(input, options)
  else :
    output = run_lin(input, options)
  return output
