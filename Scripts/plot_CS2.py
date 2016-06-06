############################################################## 
# Date: 25/05/16
# Name: plot_CS2.py
# Author: Alek Petty
# Description: Script to plot CS2 data
# Input requirements: CS2 data
# Notes - may need to install netCDF4 library. Can do this with the scipy netcdf reader also, btu I prefer this one.


import matplotlib
matplotlib.use("AGG")
# Numpy import
from pylab import *
from netCDF4 import Dataset
from matplotlib import rc
import numpy.ma as ma
from mpl_toolkits.basemap import Basemap

#SET SOME FIGURE PARAMETERS
rcParams['xtick.labelsize']=9
rcParams['font.size']=9
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

# DECIDE ON MAP PROJECTION
m = Basemap(projection='npstere',boundinglat=66,lon_0=0, resolution='l'  )

datapath = '../DATA/CS2/'
outpath = '../Figures/'

date_str = '201503'

# READ IN NETCDF DATA. 
# Note that the scipy netcdf reader is a bit more simplistic (doesn't automatically apply offsets etc) so I prefer this one. Might need to install that library though.
f = Dataset(datapath+date_str+'_cs2thickness.nc', 'r')
lats = f.variables['lat'][:]
lons = f.variables['lon'][:]
thickness = f.variables['sea_ice_thickness'][:]

#get x/y position of lon/lat gird points on te given projection
xpts,ypts = m(lons, lats)

#mask the thickness above 88 due to the CS2 pole hole.
thickness_ma=ma.masked_where(lats>88, thickness)

#SET MIN/MAX ICE THICKNESS
minval=0
maxval=5

fig = figure(figsize=(4.,4.))
ax=gca()
# HERE YOU CAN CHOOSE THE COLORBAR ETC. 
#I often need to rasterize=True to improve the quality of the output. See colorbar also.
im0 = pcolormesh(xpts , ypts, thickness_ma, vmin=minval, vmax=maxval, cmap=cm.cubehelix_r, zorder=1, rasterized=True)

# 
m.fillcontinents(color='0.8',lake_color='0.9', zorder=2)
m.drawparallels(np.arange(90,-90,-10), linewidth = 0.25, zorder=3)
m.drawmeridians(np.arange(-180.,180.,30.), linewidth = 0.25, zorder=3)

#ADD COLORBAR TO MAP
cax = fig.add_axes([0.05, 0.95, 0.2, 0.03])
cbar = colorbar(im0,cax=cax, orientation='horizontal', extend='both', use_gridspec=True)
cbar.set_label('Ice thickness (m)')
cbar.set_ticks(np.arange(minval, maxval+1, 1))
cbar.solids.set_rasterized(True)
#SHIFT COLOR SPACE SO OFF WHITE COLOR IS AT 0 m
#cbar.set_clim(-0.5, maxval)

#TRIM WHITE SPACE AROUND THE SIDES
subplots_adjust(bottom=0.0, left=0.0, top = 0.99, right=1.0)
savefig(outpath+'NASAcryosat'+date_str+'.png', dpi=300)
close(fig)


