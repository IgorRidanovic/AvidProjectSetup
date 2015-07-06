#! /usr/bin/env python

#Automates creation of Media Composer project and auxiliary storage path based on the name of the bin with final sequence. Igor Ridanovic igor@hdhead.com

#Version 1.0

import string
import sys
import os
import shutil
import glob
import smtplib
import time

# Define OS and environment specific paths.
client = 'MAKPictures'
projBasePath = '/home/igor/Desktop'
templatePath = '/home/igor/sbin/MCprojectsetup/Template/TemplateProj'
#mediaPath = '/Volumes/media/'avid Mediafiles'/MXF'
mediaBasePath = '/home/igor/Desktop'
#storageBasePath = '/Volumes/media/storage/MAKPictures'
storageBasePath = '/home/igor/Desktop/storage'

# Storage directories
dirs = ['bin',
		'credits',
		'audio']

if len(sys.argv) == 1:
	sys.exit('Sets up MC project. Usage: createproject.py filename.avb')

if not os.path.isfile(sys.argv[1]):
	sys.exit('Error: %s file not found' % sys.argv[1])

binName = sys.argv[1]

# Parse bin name. If name contains spaces must enclose argument in quotes.
binNameSplit = binName.split('_')
showName = binNameSplit[0]
epsNumber = binNameSplit[1].translate(None, string.ascii_letters + ' ') # Remove characters
showNameNumber = showName + epsNumber

# Copy project files and rename
projName = client + '_' + showNameNumber
projPath = os.path.join(projBasePath, projName)

try:
	shutil.copytree(templatePath, projPath)
except:
	sys.exit('Exception: Unable to save template project.')

templateFiles = ['TemplateProj.avp',
				'TemplateProj Settings.avs',
				'TemplateProj Settings.xml']

for i in templateFiles:
	renameSource = os.path.join(projPath, i)
	extension = os.path.splitext(i)[1]
	if extension == '.avs':
		extension = ' Settings.avs'
	if extension == '.xml':
		extension = ' Settings.xml'
	renameDestination = os.path.join(projPath, projName + extension)
	os.rename(renameSource, renameDestination)

for bin in glob.glob(os.path.join(projPath, '*.avb')):
	binNewName = os.path.basename(bin)
	binNewName = showNameNumber + '_' + binNewName
	renameDestination = os.path.join(projPath, binNewName)
	os.rename(bin, renameDestination)

# Copy and rename the original final bin
finalBinCopy = os.path.join(projPath, showNameNumber + '_ORIGINAL.avb')
shutil.copyfile(binName, finalBinCopy)
finalBinCopy = os.path.join(projPath, showNameNumber + '_SEQ.avb')
shutil.copyfile(binName, finalBinCopy)
	
# Create media path
mediaPath = os.path.join(mediaBasePath, showNameNumber)
try:
   os.makedirs(mediaPath)
except:
	sys.exit('Exception: unable to create %s media storage.' % mediaPath)

# Create storage directory tree
storagePath = os.path.join(storageBasePath, showName, showNameNumber)
try:
	os.makedirs(storagePath)
except:
	sys.exit('Exception: unable to create %s storage.' % storagePath)

for d in dirs:
	os.makedirs(os.path.join(storagePath, d))

# Backup final bin to storage to 'bin' directory
finalBinCopy = os.path.join(storagePath, 'bin', binName)
shutil.copyfile(binName, finalBinCopy)

# Send email and SMS alerts
receivers = ['igor@hdhead.com',
			'2134949511@tmomail.net']
localtime = time.asctime(time.localtime(time.time()))
username = 'somesmtpacc@gmail.com'  
password = 'Hjas54$d0' 
sender = 'somesmtpacc@gmail.com'
message = """From: MAK Pictures Automation
To: all recepients
Subject: %s Finishing Project Created

%s finishing project was created on %s.
""" % (showNameNumber, showNameNumber, localtime)
server = smtplib.SMTP('smtp.gmail.com:587')  
server.starttls()  
server.login(username,password)  
server.sendmail(sender, receivers, message)  
server.quit()
