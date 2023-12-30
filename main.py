from wrfvis.core import write_html
from wrfvis.core import get_wrf_timeseries
#from wrfvis.grid import haversine
#from wrfvis.grid import find_nearest_gridcell
#from wrfvis.grid import find_nearest_vlevel
from wrfvis.Two_dim_plot import df_2D, plot_2D, df_2D_geo, plot_topo, da_GPH #, find_geopotential_height_all_locations

import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import matplotlib.pyplot as plt
from skimage.measure import block_reduce
from wrfvis import grid
import argparse

def main():
    
    '''parser = argparse.ArgumentParser(description='Parameter selections')
    parser.add_argument('--variable', type=str, default=None, help='Valriable selection')
    parser.add_argument('--time', type=int, default=None, help='Valriable selection')
    parser.add_argument('--level', type=int, default=None, help='Valriable selection')

    args = parser.parse_args()'''
    
    time = 0
    z_lvl = 0
    var = 'T'
    #time = args.time
    #z_lvl = args.level
    #var = args.variable
    #da = da_GPH(z_lvl,time)
    #print(da)
    
    
    #T_= df_2D('T', z_lvl, time)
    #T_g = df_2D('T', z_lvl, time)
    #Alpha = df_2D('ALBEDO', z_lvl, time)
    #HF = df_2D('HFX', z_lvl, time)
    #HF = df_2D(grid.wrf_zagl, z_lvl, time)
    
    T_ = df_2D(var, z_lvl, time)
    T_g = df_2D_geo(var, z_lvl, time)
    
    #lon = da['XLONG'].values[0, :, :]
    #lat = da['XLAT'].values[0, :, :]
    
    #print(T_.indexes)
    #print(Alpha.indexes)
    #print(HF.indexes)
 
    a = plot_2D(T_, time, z_lvl)
    plt.show(a)
    #plot_topo(HGT, )
    b = plot_2D(T_g, time, z_lvl)
    plt.show(b)
    #plot_2D(Alpha, z_lvl, time)
    #plot_2D(HF, z_lvl, time)
    
    

if __name__=="__main__":
    main()
    