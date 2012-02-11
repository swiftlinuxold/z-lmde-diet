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
	dir_user = '/home/mint'
else:
	dir_develop='/home/' + uname + '/develop'
	dir_user = '/home/' + uname

# Everything up to this point is common to all Python scripts called by shared-*.sh
# =================================================================================

print '==============================='
print 'BEGIN CREATING DIET SWIFT LINUX'

import shutil

# Replace text in a file        
def change_text (filename, text_old, text_new):
    text=open(filename, 'r').read()
    text = text.replace(text_old, text_new)
    open(filename, "w").write(text)

def package_elim (name):
    os.system ('echo ELIMINATING ' + name)
    os.system ('apt-get purge -y ' + name)

def package_add (name):
    os.system ('echo ADDING ' + name)
    os.system ('apt-get install -y ' + name)
    
print "BEGIN updating Conky and ROX pinboard"

file1 = dir_user + '/.conkyrc'
change_text (file1, 'Regular Swift Linux', 'Diet Swift Linux')

file1 = '/etc/skel/.conkyrc'
change_text (file1, 'Regular Swift Linux', 'Diet Swift Linux')

file1 = dir_user + '/.config/rox.sourceforge.net/ROX-Filer/pb_swift'
change_text (file1, 'Write', 'AbiWord')
change_text (file1, 'libreoffice-writer.desktop', 'abiword.desktop')
change_text (file1, 'Calc', 'Gnumeric')
change_text (file1, 'libreoffice-calc.desktop', 'gnumeric.desktop')

file1 = '/etc/skel/.config/rox.sourceforge.net/ROX-Filer/pb_swift'
change_text (file1, 'Write', 'AbiWord')
change_text (file1, 'libreoffice-writer.desktop', 'abiword.desktop')
change_text (file1, 'Calc', 'Gnumeric')
change_text (file1, 'libreoffice-calc.desktop', 'gnumeric.desktop')

package_add ('abiword gnumeric')
package_elim ('libreoffice-calc libreoffice-writer libreoffice-base-core')
package_elim ('libreoffice-common libreoffice-core libreoffice-style-tango')


print "FINISHED updating Conky and ROX pinboard"

package_add ('abiword gnumeric')
