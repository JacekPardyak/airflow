from subprocess import Popen
#fmt = '@ECHO OFF
#cd %s
#python.exe "%s" --output="%s"  "%s"'
#p = Popen("batch.bat", cwd=r"C:\Users\jacek\OneDrive\Documents\inkscape.py")
#stdout, stderr = p.communicate()

import tempfile
import os
import stat
import subprocess
bat = tempfile.NamedTemporaryFile(suffix='.bat').name

text = '''@echo off
winget install -e --id Inkscape.Inkscape
inkscape --version
'''
print(text)
with open(bat, mode='w') as f:
    f.write(text)
print(bat)
#p = Popen(bat, cwd=r"C:\Users\jacek\AppData\Local\Temp", stdout=subprocess.PIPE)
#stdout, stderr = p.communicate()

subprocess.call([bat])

subprocess.call(args=[bat])
bat

import subprocess

subprocess.run(["ls", "-l"]) 

