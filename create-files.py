#! /usr/bin/env python

# Check for root user login
import os, sys
if os.geteuid()==0:
    sys.exit('\nYou MUST be NON-ROOT to run this script.\n')

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

import shutil # Needed for copying files

dir_develop = '/home/' + uname + '/develop'
dir_build = dir_develop + '/1-build'
dir_temp = dir_develop + '/temp-diet'

def change_text (filename, text_old, text_new):
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)

def copy_file (file_old, file_new, text_old, text_new):
    ret = os.access(file_new, os.F_OK)
    if (ret):
        os.remove (file_new)
    shutil.copy2 (file_old, file_new)
    change_text(file_new, text_old, text_new)
    
def elim_dir (dir_to_elim): 
    if (os.path.exists(dir_to_elim)):
        shutil.rmtree (dir_to_elim)

def create_dir (dir_to_create):
    if not (os.path.exists(dir_to_create)):
        os.mkdir (dir_to_create)

elim_dir (dir_temp)
create_dir (dir_temp)

# Adapt build-regular.sh
file_regular = dir_build + '/build-regular.sh'
file_diet = dir_temp + '/build.sh'
text_regular = 'linuxmint-201109-gnome-dvd-32bit.iso'
text_diet = 'regular.iso'
copy_file (file_regular, file_diet, text_regular, text_diet)
print file_regular, file_diet, text_regular, text_diet

text_regular = '$DIR_DEVELOP/remaster/main.sh'
text_diet = '$DIR_DEVELOP/temp-diet/remaster.sh'
change_text (file_diet, text_regular, text_diet)

# file_regular = DIR_DEVELOP + '/build-regular.sh'
# file_diet = dir_build+'/build-diet.sh'
# copy_file (file_diet, file_regular, 'diet', 'regular')
