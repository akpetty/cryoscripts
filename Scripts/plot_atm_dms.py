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
#may need this if reading in ATM data after 2013 (hdf5 format)
#import h5py


rcParams['axes.labelsize'] =8
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})


def get_atm_from_dms(res):
	# FIND ATM FILE THAT STARTED BEFORE THE DMS GPS TIME
	# SHOULD MAINLY WORK BUT COULD BE PROBLEMS DUE TO SLIGHT OFFSET - CHECK THIS
	atm_files = glob(ATM_path+'/'+date+'/*')

	for j in xrange(size(atm_files)):
		atm_time = float(atm_files[j][-17:-11])
		
		if (atm_time>float(dms_time[0:-2])):
			break

	return atm_files[j-1]

def get_dms(image_path):
	geo = gdal.Open(image_path) 
	band1 = geo.GetRasterBand(1)
	band2 = geo.GetRasterBand(2)
	band3 = geo.GetRasterBand(3)
	red = band1.ReadAsArray()
	green = band2.ReadAsArray()
	blue = band3.ReadAsArray()

	dms = (0.299*red + 0.587*green + 0.114*blue)
	dms = ma.masked_where(dms<1, dms)

	trans = geo.GetGeoTransform()
	width = geo.RasterXSize
	height = geo.RasterYSize

	x1 = np.linspace(trans[0], trans[0] + width*trans[1] + height*trans[2], width)
	y1 = np.linspace(trans[3], trans[3] + width*trans[4] + height*trans[5], height)
	xT, yT = meshgrid(x1, y1)
	return xT, yT, dms, geo

def get_atmqih5(atm_file, year, res, utc_time=1):

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

def plot_probdist():

	fig = figure(figsize=(3,3))
	ax=gca()
	im3 = plot(bins[0:-1], hist, 'k')

	axvline(x=level_elev, color='b')
	axvline(x=level_elevl, linestyle='--', color='r')
	axvline(x=level_elevu, linestyle='--', color='r')
	ax.set_ylabel('Prob Density', labelpad=1)
	ax.set_xlabel('Relative elevation (m)', labelpad=1)
	tight_layout()
	savefig(figpath+'atm_dmsdist_'+str(xy_res)+'mxy_'+date+'_'+dms_time+int_method+str(int(min_ridge_height*100))+'_cm2.png', dpi=300)


datapath='../Data_output/'
rawdatapath = '../Data/'
ATM_path = rawdatapath+'ATM/'
dms_path = rawdatapath+'DMS/'
posAV_path =rawdatapath+'POSAV/'
figpath='../Figures/'

#norm = ro.MidpointNormalize(midpoint=0)

m=pyproj.Proj("+init=EPSG:3413")

date = '20110323'
dms_time = '18045984'

year = int(date[0:4])
image_path = glob(dms_path+'*'+date+'_'+dms_time+'.tif')
xT, yT, dms, geo = get_dms(image_path[0])
lonDMS, latDMS = m(xT[0, 0], yT[0, 0], inverse=True)
lonDMS_str = '%.2f' %lonDMS
latDMS_str = '%.2f' %latDMS

# Determine which ATM file we need
atm_file = get_atm_from_dms(res=1)
print 'atm file needed:', atm_file
# Get ATM data
lon, lat, elevation = get_atmqih5(atm_file, year, 1, utc_time=0)
# Project ATM onto DMS/IB projection
x, y = m(lon, lat)
#--------------------------------------------------

# Get DMS corners and shift DMS/ATM data accordingly
minX = xT[-1, 0]
minY = yT[-1, 0]
xT = xT - minX
yT = yT - minY
x = x - minX
y = y - minY

print lonDMS, latDMS, date[0:4]

#-------------- CHECK BOUNDS OF ATM/DMS ----------------
print 'tiff lims x:', np.amin(xT),np.amax(xT)
print 'tiff lims y:', np.amin(yT),np.amax(yT)
print 'ATM lims x:', np.amin(x),np.amax(x)
print 'ATM lims y:', np.amin(y),np.amax(y)
#--------------------------------------------------
#-------------- MASK ELEVATION AND X/Y BASED ON DMS BOUNDS  ------------------
elevation_maL = ma.masked_where((x<np.amin(xT)) | (x>np.amax(xT)) | (y<np.amin(yT)) | (y>np.amax(yT)), elevation)
elevation_ma = ma.compressed(elevation_maL)
mask = ma.getmask(elevation_maL)
indexT = np.where(mask==False)
xatm = x[indexT]
yatm = y[indexT]
#--------------------------------------------------

# GET HISTOGRAM OF ATM DATA IF SO DESIRED
hist, bins = histogram(elevation_ma, bins=100, density=True)
#PLOT OUT PROB DISTRIBUTION FOR CHECKING
#plot_probdist()

sizex = np.amax(xT) - np.amin(xT)
sizey = np.amax(yT) - np.amin(yT)
ratio = sizey/sizex

minval = np.round(np.percentile(elevation_ma, 1), decimals=1)
maxval = np.round(np.percentile(elevation_ma, 99), decimals=1)
res=1
textwidth=4
fig = figure(figsize=(textwidth,textwidth*1.25*ratio))
ax=gca()
im2 = pcolormesh(xT[::res, ::res], yT[::res, ::res], dms[::res, ::res], vmin = 0, vmax = 255, cmap = cm.gist_gray, rasterized=True)
im21 = scatter(xatm, yatm, c = elevation_ma, vmin = minval, vmax = maxval, s=2, lw = 0, cmap = cm.RdYlBu_r, rasterized=True)


ax.set_xlim(np.amin(xT),np.amax(xT))
ax.set_ylim(np.amin(yT),np.amax(yT))
ax.set_xlabel('y (m)', labelpad=1)
ax.set_ylabel('x (m)', labelpad=1)
ax.yaxis.grid(True)
ax.xaxis.grid(True)


fig.text(0.06, 0.96, 'DMS Date: '+date+'  DMS Time: '+dms_time+'     '+latDMS_str+'N, '+lonDMS_str+'E')

cax = fig.add_axes([0.13, 0.2, 0.15, 0.04])
cbar = colorbar(im21,cax=cax, orientation='horizontal', extend='both', use_gridspec=True)
cbar.set_label('Elevation to \n WGS84 (m)', labelpad=4)
xticks1 = np.linspace(minval, maxval, 3)
cbar.set_ticks(xticks1)

subplots_adjust(bottom=0.09, left=0.11, top = 0.94, right=0.99, hspace=0.22)
savefig(figpath+'atm_dms.png', dpi=300)
close(fig)






