############################################################## 
# Date: 25/05/16
# Name: plot_icebridge_thickness.py
# Author: Alek PettyIB thicknessCS2 data
# Input requirements: IB thickness data


import matplotlib
matplotlib.use("AGG")
# Numpy import
from pylab import *
from netCDF4 import Dataset
from matplotlib import rc
import numpy.ma as ma
from mpl_toolkits.basemap import Basemap
from glob import glob

rcParams['ytick.major.size'] = 2
rcParams['axes.linewidth'] = .5
rcParams['lines.linewidth'] = .5
rcParams['patch.linewidth'] = .5
rcParams['axes.labelsize'] = 8
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

def read_icebridgeALL(mplot, rawdatapath, year, mask_hi=1, mask_nonarctic=1):
	lats_total=[] 
	lons_total=[]
	thickness_total=[]
	snow_thickness_total=[]
	if (year>2013):
		files = glob(rawdatapath+'/ICEBRIDGE_HI/QLOOK/'+str(year)+'*/*.txt')
	else:
		files = glob(rawdatapath+'/ICEBRIDGE_HI/IDCSI4/'+str(year)+'.*/*.txt')
	
	for x in xrange(size(files)):
		data = genfromtxt(files[x], delimiter=',', skip_header=1, dtype=str)
		# data is a table-like structure (a numpy recarray) in which you can access columns and rows easily
		lats = data[:, 0].astype(float)
		lons = data[:, 1].astype(float)
		thickness = data[:, 2].astype(float)
		snow_thickness = data[:, 7].astype(float)
		lats_total.extend(lats)
		lons_total.extend(lons)
		thickness_total.extend(thickness)
		snow_thickness_total.extend(snow_thickness)

	thickness_total=array(thickness_total)
	snow_thickness_total=array(snow_thickness_total)
	lats_total=array(lats_total)
	lons_total=array(lons_total)

	if (mask_hi==1):
		good_data=where((thickness_total>=0.)&(thickness_total<=20.))
		thickness_total = thickness_total[good_data]
		snow_thickness_total=snow_thickness_total[good_data]
		lats_total = lats_total[good_data]
		lons_total = lons_total[good_data]
	if (mask_nonarctic==1):
		xptsIB, yptsIB = mplot(lons_total, lats_total)
		region_maskR = griddata((xptsM.flatten(), yptsM.flatten()),region_mask.flatten(), (xptsIB, yptsIB), method='nearest')
		good_data = where((region_maskR==8))
		lats_total = lats_total[good_data]
		lons_total=lons_total[good_data]
		thickness_total=thickness_total[good_data]
		snow_thickness_total=snow_thickness_total[good_data]

	xpts,ypts = mplot(lons_total, lats_total)

	return xpts,ypts, lats_total, lons_total, thickness_total, snow_thickness_total	

def plot_icebridge():


	fig = figure(figsize=(textwidth,(textwidth*1.3*aspect)))
	subplots_adjust(left = 0.01, right = 0.99, bottom=0.23, top = 0.99, wspace = 0.02, hspace=0.01)
	ax1=gca()
	minval = 0.
	maxval = 5.

	im1 = m.pcolormesh(xpts_type , ypts_type, ice_type, edgecolors='white', vmin=0, vmax=2, cmap=cm.Greys,shading='gouraud', zorder=1, rasterized=True)
	im11 = ax1.hexbin(xpts, ypts, C=thickness, gridsize=100, vmin=minval, vmax=maxval, cmap=cm.cubehelix_r, zorder=2, rasterized=True)
	m.fillcontinents(color='w',lake_color='grey', zorder=3)
	m.drawcoastlines(linewidth=0.25, zorder=5)
	m.drawparallels(np.arange(90,-90,-5), linewidth = 0.25, zorder=10)
	m.drawmeridians(np.arange(-180.,180.,30.), latmax=85, linewidth = 0.25, zorder=10)
	xS, yS = m(177, 64.2)


	cax = fig.add_axes([0.2, 0.16, 0.6, 0.05])
	cbar = colorbar(im11,cax=cax, orientation='horizontal', extend='max',use_gridspec=True)
	#cbar.set_alpha(1)
	#cbar.draw_all()
	cbar.set_label('Ice thickness (m)', labelpad=0)
	cbar.solids.set_rasterized(True)
	xticks = np.linspace(minval, maxval, 6)
	cbar.set_ticks(xticks)

	savefig(figpath+'/icebridge_thickness_'+str(year)+'.png', dpi=300)

def get_ice_type(mplot, rawdatapath, year, res=1):
	ice_type_path = rawdatapath+'/ICETYPE/'+str(year)+'/'
	files = glob(ice_type_path+'*.nc')
	#just pick one for now!
	file=files[0]
	f = Dataset(file, 'r')
	lats = f.variables['lat'][::res, ::res]
	lons = f.variables['lon'][::res, ::res]
	xpts_type, ypts_type = mplot(lons, lats)
	
	f = Dataset(file, 'r')
	ice_typeT = f.variables['ice_type'][0,::res, ::res]
	#open water
	ice_typeT = np.where(ice_typeT==1, 0., ice_typeT)
	#first year ice
	ice_typeT = np.where(ice_typeT==2, 0.5, ice_typeT)
	#multi-year ice
	ice_typeT = np.where(ice_typeT==3, 1, ice_typeT)
	#ambiguous
	ice_typeT = np.where(ice_typeT==4, 0.75, ice_typeT)

	return ice_typeT, xpts_type, ypts_type

#m = Basemap(projection='npstere',boundinglat=66,lon_0=0, resolution='l'  )
m=Basemap(projection='stere', lat_0=74, lon_0=-90,llcrnrlon=-150, llcrnrlat=58,urcrnrlon=10, urcrnrlat=72)

#my_cmap=perceptual_colormap("Linear_L", rawdatapath+'OTHER/CMAPS/', reverse=1)

rawdatapath='../DATA/'
figpath='../Figures/'
textwidth=3.
aspect = m.ymax/m.xmax


year=2015
xpts,ypts, lats, lons, thickness, snow= read_icebridgeALL(m, rawdatapath,year, mask_hi=1, mask_nonarctic=0)

ice_type, xpts_type, ypts_type=get_ice_type(m, rawdatapath, year, res=1)


plot_icebridge()

