__author__ = 'cmccully'
from matplotlib import pyplot
from glob import glob
from astropy.io import fits
import numpy as np
from astropy.io import ascii

def setup_plot():
    pyplot.rcParams['axes.titlesize'] = 'x-large'
    pyplot.rcParams['axes.labelsize'] = 'x-large'
    pyplot.rcParams['axes.labelweight'] = 'normal'
    pyplot.rcParams['lines.linewidth'] = 1.8
    pyplot.rcParams['axes.linewidth'] = 1.8

    pyplot.rcParams['xtick.labelsize'] = 'x-large'
    pyplot.rcParams['xtick.major.pad'] = 8
    pyplot.rcParams['xtick.major.size'] = 8
    pyplot.rcParams['xtick.major.width'] = 1.8
    pyplot.rcParams['xtick.minor.pad'] = 8
    pyplot.rcParams['xtick.minor.size'] = 4
    pyplot.rcParams['xtick.minor.width'] = 1.0

    pyplot.rcParams['ytick.labelsize'] = 'x-large'
    pyplot.rcParams['ytick.major.pad'] = 8
    pyplot.rcParams['ytick.major.size'] = 8
    pyplot.rcParams['ytick.major.width'] = 1.8
    pyplot.rcParams['ytick.minor.pad'] = 8
    pyplot.rcParams['ytick.minor.size'] = 4
    pyplot.rcParams['ytick.minor.width'] = 1.0  # Make 9 panels of plots

def parse():
    #Read in the airmass terms and the MJDs
    fs = glob('*.fits')
    airmasses = []
    mjds = []
    sites = []
    for f in fs:
        airmasses.append(fits.getval(f, 'AIRMASS'))
        mjds.append(fits.getval(f, 'MJD-OBS'))
        sites.append(f[:3])

    mjds = np.array(mjds)
    airmasses = np.array(airmasses)
    sites = np.array(sites)

    ascii.write([mjds, airmasses, sites], 'airmass.dat',
                names=['mjd', 'airmass', 'site'])



def plot():
    #Read in the airmass terms and the MJDs

    data = ascii.read('airmass.dat')
    mjds, airmasses, sites = data['mjd'], data['airmass'], data['site']

    setup_plot()

    colors = {'lsc':'blue', 'cpt':'red', 'coj': 'green'}

    for site in ['lsc', 'cpt', 'coj']:
        where_site = sites == site
        pyplot.plot(mjds[where_site] - 57000, airmasses[where_site],
                    'o', color=colors[site])
    pyplot.xlim(7.7, 10.3)
    pyplot.ylim(2.35, 0.95)
    pyplot.xlabel('MJD - 57000')
    pyplot.ylabel('Airmass')
    a = pyplot.annotate("", xy=(8.75, 1.2),  xycoords='data',xytext=(8.30, 1.2), textcoords='data',
    arrowprops={'arrowstyle':"<->"})
    a.arrow_patch.set_linewidth(2)
    pyplot.text(8.525, 1.17,'Bad Weather', ha='center', fontsize='medium')

    pyplot.legend(labels=['Chile', 'South Africa', 'Australia'], loc=3)
    pyplot.savefig('he0435_airmass.pdf', bbox_inches='tight', pad_inches=0.05)
    pyplot.show()
    pyplot.rcdefaults()
