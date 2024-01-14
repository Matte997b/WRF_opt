""" Configuration module containing settings and constants. """
import os

wrfout = '/home/mattia/Documents/Scientific_programming/WRF_project/WRF_out.nc'

# location of data directory
pkgdir = os.path.dirname(__file__)

# Author: Battisti Mattia
# These templetes contains the structure of html file plots
html_template = os.path.join(pkgdir, 'data', 'template.html')
html_template_o = os.path.join(pkgdir, 'data', 'template_o.html')
html_template_o_1 = os.path.join(pkgdir, 'data', 'template_o_1.html')

test_ts_df = os.path.join(pkgdir, 'data', 'test_df_timeseries.pkl')
test_hgt = os.path.join(pkgdir, 'data', 'test_hgt.nc')

# minimum and maximum elevations for topography plot
topo_min = 0
topo_max = 3200
