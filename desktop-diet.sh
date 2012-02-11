#!/bin/bash
# Proper header for a Bash script.

# Check for root user login
if [ ! $( id -u ) -eq 0 ]; then
	echo "You must be root to run this script."
	echo "Please enter su before running this script again."
	exit
fi

# Get your username (not root)
UNAME=$(awk -v val=1000 -F ":" '$3==val{print $1}' /etc/passwd)
DIR_DEVELOP=/home/$UNAME/develop

# This is the script for creating Diet Swift Linux on the desktop.

su -c "sh $DIR_DEVELOP/1-build/preinstall.sh" $UNAME

rm -r $DIR_DEVELOP/temp
su -c "mkdir $DIR_DEVELOP/temp" $UNAME
# sh $DIR_DEVELOP/1-build/shared-regular.sh | tee $DIR_DEVELOP/temp/screenoutput.txt
sh $DIR_DEVELOP/diet/shared-diet.sh | tee $DIR_DEVELOP/temp/screenoutput.txt
chown $UNAME:users $DIR_DEVELOP/temp/screenoutput.txt
