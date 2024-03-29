#! /usr/bin/env python

# Check for root user login
import os, sys
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this script\n")

# Get your username (not root)
import pwd
uname=pwd.getpwuid(1000)[0]

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
is_chroot = os.path.exists('/home/mint')
dir_develop=''
if (is_chroot):
	dir_develop='/usr/local/bin/develop'
else:
	dir_develop='/home/' + uname + '/develop'

# ======================================================================================

def elim_dir (dir_to_elim): 
	if (os.path.exists(dir_to_elim)):
		shutil.rmtree (dir_to_elim)

def create_dir (dir_to_create):
    if not (os.path.exists(dir_to_create)):
        os.mkdir (dir_to_create)

def change_text (filename, text_old, text_new):
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)
   

os.system ("echo ===============================")
os.system ("echo BEGIN BUILDING DIET SWIFT LINUX")


os.system ('mount -t vboxsf guest /mnt/host')
base_iso = '/mnt/host/regular.iso'
while not (os.path.isfile (base_iso)):
    print ('Could not find your ' + base_iso + 'file.')
    print ('Please go to your host OS and copy the appropriate file into')
    print ('the /home/(username)/guest directory.')
    print ('Press Enter when you are finished')
    var_dummy = raw_input ('TEST')
    os.system ('mount -t vboxsf guest /mnt/host')

# Prepare the Regular Swift Linux remastering script
os.system ('sh ' + dir_develop + '/remaster/main.sh')

# Change the remastering script
file_remaster = '/usr/lib/linuxmint/mintConstructor/mintConstructor.py'
text_old = 'regular.iso'
text_new = 'diet.iso'
change_text (file_remaster, text_old, text_new)
text_old = 'linuxmint-201204-mate-cinnamon-dvd-32bit'
text_new = 'regular'
change_text (file_remaster, text_old, text_new)
text_old = '/usr/local/bin/develop/1-build/shared-regular.py'
text_new = '/usr/local/bin/develop/diet/main.py'
change_text (file_remaster, text_old, text_new)

# Execute the remastering script
os.system ('echo EXECUTING THE REMASTERING SCRIPT')
command_remaster = 'python /usr/lib/linuxmint/mintConstructor/mintConstructor.py '
os.system (command_remaster)

# Change ownership of file containing screen output
command_chown = 'chown ' + uname + ':users ' + file_output
os.system (command_chown)

os.system ("echo FINISHED BUILDING DIET SWIFT LINUX")
os.system ("echo ==================================")



# PREREQUISITES:
# 1.  All necessary repositories must have already been downloaded
# 2.  The regular.iso file must already be in /mnt/host
