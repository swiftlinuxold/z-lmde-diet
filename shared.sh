#!/bin/bash
# Proper header for a Bash script.

# Check for root user login
if [ ! $( id -u ) -eq 0 ]; then
	echo "You must be root to run this script."
	echo "Please enter su before running this script again."
	exit 2
fi

# Get your username (not root)
UNAME=$(awk -v val=1000 -F ":" '$3==val{print $1}' /etc/passwd)
DIR_DEVELOP=''

# The remastering process uses chroot mode.
# Check to see if this script is operating in chroot mode.
# /home/mint directory only exists in chroot mode
IS_CHROOT=0
if [ -d "/home/mint" ]; then
	IS_CHROOT=1 # in chroot mode
	DIR_DEVELOP=/usr/local/bin/develop 
else
	DIR_DEVELOP=/home/$UNAME/develop 
fi

# Everything up to this point is common to the script shared-*.sh and all Bash scripts called by shared-*.sh
#=====================================================================================================

# This is the script for transforming Regular Swift Linux into Diet Swift Linux.

# Setting up apt-get/Synaptic MUST come first, because
# some repositories require installing packages.
python $DIR_DEVELOP/diet/main.py

# Final touches
python $DIR_DEVELOP/final/main.py # Must come last

exit 0
