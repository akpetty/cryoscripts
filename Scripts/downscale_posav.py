############################################################## 
# Date: 25/05/16
# Name: downscale_posav.py
# Author: Alek Petty
# Description: Script to downscale the *really large* posav files and apply GPS-UTC offset
# Input requirements: posAV data

# Numpy import
import numpy as np
from pylab import *
import scipy.io
from scipy.io import netcdf
from mpl_toolkits.basemap import Basemap
from glob import glob


def downscale_POS(wholeFilePath):
	print wholeFilePath
	flightYear  = wholeFilePath[-12:-8]
	flightMonth = wholeFilePath[-8:-6]
	fid = open(wholeFilePath, 'rb')

	dataT = fromfile(file=fid, dtype='d')
	dataT=dataT.reshape((-1, numCols)).T

	timeres = dataT[0, 1]-dataT[0, 0]
	freq = 1./timeres
	dataTS=dataT[:,::200]

	gpsTimeDays  = dataTS[0]/(24*60*60)
	gpsTime     = dataTS[0]-(floor(gpsTimeDays)*(24*60*60))

	if (year>=2016):
		utcTime=gpsTime-17
		print 'gps offet = 17s'
	elif (year>=2013):
		utcTime=gpsTime-16
		print 'gps offet = 16s'
	elif (year>=2010):
		utcTime=gpsTime-15
		print 'gps offet = 15s'
	elif (year==2009):
		utcTime=gpsTime
		print 'gps-utc offset ALREADY APPLIED TO POSAV DATA I THINK?'

	data_out = np.zeros((7, dataTS.shape[1]))
	data_out[0] = utcTime
	data_out[1] = np.degrees(dataTS[1])
	data_out[2] = np.degrees(dataTS[2])
	data_out[3] = dataTS[3]
	data_out[4] = sqrt(dataTS[4]**2+dataTS[5]**2)
	data_out[5] = np.degrees(dataTS[8])
	data_out[6] = np.degrees(dataTS[7])


	savetxt(FilePaths+wholeFilePath[-17:]+'.txt', data_out.T, fmt='%.3f', header='UTCtime (s)  Lat (deg)  Lon (deg)  Alt (m), Vel (m/s) Pitch (deg) Roll (deg)')


numCols = 17
year=2009
pole ='GR'
FilePaths='../../../DATA/ICEBRIDGE/POSAV/SEA_ICE/'+pole+'/'+str(year)+'_'+pole+'_NASA/'

files=glob(FilePaths+'*.out')
for x in xrange(size(files)):
	wholeFilePath=files[x]
	downscale_POS(wholeFilePath)






# data = data';
# %--------------------------------------------------------------------------


# %--------------------------------------------------------------------------
# % Assigns data to variable names
# %--------------------------------------------------------------------------

# %..........................................................................
# % converts GPS time to UTC time
# %..........................................................................
# gpsTime     = data(:,1); 
# utcimeDays  = gpsTime./(24*60*60);
# utcTime     = gpsTime-(floor(utcimeDays)*(24*60*60));

# k           = strfind(wholeFilePath,'sbet');
# flightYear  = str2num(wholeFilePath(k+[5:8]));
# flightMonth = str2num(wholeFilePath(k+[9:10]));

# pos.gpsTime = gpsTime;

# if flightYear >= 2012 && flightMonth >= 7
#     pos.utcTime = utcTime-16;
# else
#     pos.utcTime = utcTime-15;
# end
# %..........................................................................

# pos.latitude           = radtodeg(data(:,2)); % (degrees)
# pos.longitude          = radtodeg(data(:,3)); % (degrees)
# pos.altitude           = data(:,4);           % (meters)

# pos.xWaVelocity        = data(:,5);           % (meters/second)
# pos.yWaVelocity        = data(:,6);           % (meters/second)
# pos.zWaVelocity        = data(:,7);           % (meters/second)

# pos.roll               = data(:,8);           % (radians)
# pos.pitch              = data(:,9);           % (radians)

# pos.platformHeading    = data(:,10);          % (radians)
# pos.wanderAngle        = data(:,11);          % (radians)
# pos.trueHeading        = pos.platformHeading+pos.wanderAngle;

# pos.xBodySpecificForce = data(:,12);          % (meters/second)
# pos.yBodySpecificForce = data(:,13);          % (meters/second)
# pos.zBodySpecificForce = data(:,14);          % (meters/second)

# pos.xBodyAngularRate   = data(:,15);          % (radians/second)
# pos.yBodyAngularRate   = data(:,16);          % (radians/second)
# pos.zBodyAngularRate   = data(:,17);          % (radians/second)


