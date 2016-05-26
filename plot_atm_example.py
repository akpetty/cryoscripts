############################################################## 
# Date: 20/05/16
# Name: plot_atm_dms.py
# Author: Alek Petty
# Description: Script to plot ATM overlaid on a DMS image
# Input requirements: DMS image and ATM data for specific case studies

import matplotlib
matplotlib.use("AGG")
import numpy as np
from pylab import *
import numpy.ma as ma
from mpl_toolkits.basemap import Basemap
from matplotlib import rc
import mpl_toolkits.basemap.pyproj as pyproj 
from glob import glob
import os
from osgeo import osr, gdal
import h5py


rcParams['axes.labelsize'] =8
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})


def get_atmqih5(atm_file, year, res=1, utc_time=1):

	if (year>=2013):

		atm = h5py.File(atm_file, 'r')
		elevation = atm['elevation'][::res]
		lon = atm['longitude'][:]
		lat = atm['latitude'][:]
		pitch = atm['instrument_parameters']['pitch'][:]
		roll = atm['instrument_parameters']['roll'][:]
		azi =atm['instrument_parameters']['azimuth'][:]
		#multiply by 1000 to put milliseconds in front of the decimal.
		gps_time=atm['instrument_parameters']['time_hhmmss'][:]*1000
		atm.close()
		if (utc_time==1):
			utc_time = gpshhmmss_to_utc_seconds(gps_time, year)
			return lon, lat, elevation, utc_time
		else:
			return lon, lat, elevation

	else:
		fid = open(atm_file, 'rb')
		if (year<=2010):
			#BIG ENDIAN
			dtypeT='>i4'
		else:
			dtypeT='<i4'

		#header = np.fromfile(fid, dtype='>u4', count=3888)
		numofwords = np.fromfile(fid, dtype=dtypeT, count=1)/4
		blankarray = np.fromfile(fid, dtype=dtypeT, count=numofwords[0]-1)
		initialword = np.fromfile(fid, dtype=dtypeT, count=1)
		skipBytes = np.fromfile(fid, dtype=dtypeT, count=1)
		print skipBytes[0]
		if (skipBytes[0]>20000.):
			if (year==2009):
				skipBytes=[2832]
			elif (year==2010):
				skipBytes=[2928]
			elif (year==2011):
				skipBytes=[3888]
			elif (year==2012):
				skipBytes=[4176]

		fid.seek(0)
		fid.seek(skipBytes[0], os.SEEK_SET)

		data = np.fromfile(fid, dtype=dtypeT)
		data = data.reshape(-1, 12)
		atm=np.zeros((data.shape))
		atm[:, 0] = data[:, 0]/1000.
		atm[:, 1] = data[:, 1]/1000000.
		atm[:, 2] = data[:, 2]/1000000.
		atm[:, 3] = data[:, 3]/1000.
		atm[:, 4] = data[:, 4]
		atm[:, 5] = data[:, 5]
		atm[:, 6] = data[:, 6]/1000.
		atm[:, 7] = data[:, 7]/1000.
		atm[:, 8] = data[:, 8]/1000.
		atm[:, 9] = data[:, 9]/10.
		atm[:, 10] = data[:, 10]
		atm[:, 11] = data[:, 11]

		lat = atm[:, 1]
		lon = atm[:, 2]
		elevation = atm[:, 3]
		pitch = atm[:, 7]
		roll = atm[:, 8]
		gps_time = atm[:, 11]
		azi = atm[:, 6]
		#pulse_s = data[:, 4]
		#ref_s = data[:, 5]
		#azi = data[:, 6]/1000.
		#pdop = data[:, 9]/10.
		#p_width = data[:, 10]

		if (utc_time==1):
			utc_time = gpshhmmss_to_utc_seconds(gps_time, year)
			return lon, lat, elevation, utc_time
		else:
			return lon, lat, elevation

datapath='./Data_output/'
rawdatapath = './Data/'
ATM_path = rawdatapath+'ATM'
figpath='./Figures/'

#norm = ro.MidpointNormalize(midpoint=0)

m=pyproj.Proj("+init=EPSG:3413")

date = '20150401'
atm_files = glob(ATM_path+'/'+date+'/*')
# Get ATM data
lon, lat, elevation = get_atmqih5(atm_files[0], date[0:4], res=1, utc_time=0)

lon=lon[0:100000]
lat=lat[0:100000]
elevation=elevation[0:100000]
# Project ATM onto DMS/IB projection
x, y = m(lon, lat)
#--------------------------------------------------

# SHIFT ATM DATA
minX = np.amin(x)
minY = np.amin(y)
x = x - minX
y = y - minY


sizex = np.amax(x) - np.amin(x)
sizey = np.amax(y) - np.amin(y)
ratio = sizey/sizex

minval = np.round(np.percentile(elevation, 1), decimals=1)
maxval = np.round(np.percentile(elevation, 99), decimals=1)
res=1
textwidth=4
fig = figure(figsize=(textwidth,textwidth*1.5*ratio))
ax=gca()

im21 = scatter(x, y, c = elevation, vmin = minval, vmax = maxval, s=2, lw = 0, cmap = cm.RdYlBu_r, rasterized=True)


ax.set_xlim(np.amin(x),np.amax(x))
ax.set_ylim(np.amin(y),np.amax(y))
ax.set_xlabel('y (m)', labelpad=1)
ax.set_ylabel('x (m)', labelpad=1)
ax.yaxis.grid(True)
ax.xaxis.grid(True)

cax = fig.add_axes([0.8, 0.9, 0.15, 0.04])
cbar = colorbar(im21,cax=cax, orientation='horizontal', extend='both', use_gridspec=True)
cbar.set_label('Elevation to \n WGS84 (m)', labelpad=4)
xticks1 = np.linspace(minval, maxval, 3)
cbar.set_ticks(xticks1)
cbar.solids.set_rasterized(True)

subplots_adjust(bottom=0.2, left=0.11, top = 0.97, right=0.98)
savefig(figpath+'atm_'+date+'.png', dpi=300)
close(fig)






