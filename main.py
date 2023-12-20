from wrfvis.core import write_html
from wrfvis.core import get_wrf_timeseries
#from wrfvis.grid import haversine
#from wrfvis.grid import find_nearest_gridcell
#from wrfvis.grid import find_nearest_vlevel
from wrfvis.Two_dim_plot import df_2D, plot_2D

import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import matplotlib.pyplot as plt
from skimage.measure import block_reduce

def main():
    
    #var, hgt = get_wrf_timeseries('T', 15, 10, 0) 
    time = 10
    z_lvl = 0
    T_ = df_2D('T', z_lvl, time)
    Alpha = df_2D('ALBEDO', z_lvl, time)
    HF = df_2D('HFX', z_lvl, time)
    
    print(T_.indexes)
    print(Alpha.indexes)
    print(HF.indexes)
 
    plot_2D(T_, z_lvl, time)
    plot_2D(Alpha, z_lvl, time)
    plot_2D(HF, z_lvl, time)
    
    
if __name__=="__main__":
    main()
    