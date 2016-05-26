############################################################## 
# Date: 01/01/16
# Name: plot_extent.py
# Author: Alek Petty
# Description: Script to plot monthly Arctic ice extent
# Input requirements: Arctic ice extent file

import matplotlib
matplotlib.use("AGG")
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
import numpy.ma as ma
from matplotlib import rc
from glob import glob
import pandas as pd
from scipy import stats

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

def get_ice_extent(rawdatapath, Month, start_year):
	extent_data_path=rawdatapath+'/ICE_CONC/gsfc.nasateam.month.extent.1978-2013.n.txt'
	ice_extent_data=pd.read_csv(extent_data_path, delim_whitespace=True,header=(0),index_col=False)
	#ice_extent_data = np.loadtxt(extent_data_path, delimiter=',',skiprows=1)
	Extent_month = ice_extent_data['TotalArc']/1e6
	Month = ice_extent_data['Mon']
	Year = ice_extent_data['Year']
	# #Select the ice extent month we are concerned with (9=September)
	Extent=Extent_month[Month==9]
	Year_sep=Year[Month==9]
	#if (addSEP==1):
	#	Years.append(2014)
	#	Years.append(2014)
	#	Extent.append
	Years=array(Year_sep[start_year-1979:])
	Extent=array(Extent[start_year-1979:])

	return Years, Extent

def correlate(var1, var2):
	#correlate two variables using stats.linregress
	# can also use statsmodel if desired. Gives you more outputs.
    trend, intercept, r_a, prob, stderr = stats.linregress(var1, var2)
    sig = 100*(1-prob)
    return trend, sig, r_a, intercept 


datapath = './DATA'
figpath='./Figures/'

start_year=1980
month=9

Years, Extent=get_ice_extent(datapath, month, start_year)
ext_trend, ext_sig, ext_r, ext_int = correlate(Years, Extent) 
ext_line = (Years*ext_trend)+ext_int

fig = figure(figsize=(3,2))
ax1 = gca()

plot(Years, Extent, linestyle='-',marker='',markersize=3,linewidth=1, color='k')
plot(Years, ext_line,linestyle='--', color='k')

ext_trend_str = '%.1f' % (ext_trend*100)
ext_sig_str = '%2d' % ext_sig
ax1.annotate(ext_trend_str+r'$\times$10$^{4}$ km$^2$/yr (>'+ext_sig_str+'%)' , xy=(0.25, 0.4), xycoords='axes fraction', color='k', fontsize=9, horizontalalignment='left', verticalalignment='bottom')

#ax1.yaxis.grid(True)
#ax1.xaxis.grid(True, which='major')
#ax1.set_ylim(13, 16)
ax1.set_yticks(np.arange(3, 8, 1.))
ax1.set_xlim(Years[0], Years[-1])
ax1.set_ylabel( 'Ice extent'+r' (10$^{6}$ km$^2$)')
ax1.set_xlabel( 'Years')

subplots_adjust( right = 0.98, left = 0.12, top=0.96, bottom=0.16)
savefig(figpath+'/Arctic_extent.png', dpi=1000)
close(fig)









