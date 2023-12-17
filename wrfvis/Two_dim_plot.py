#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 15:05:29 2023

@author: mattia
"""
import os
from tempfile import mkdtemp
import shutil

import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import matplotlib.pyplot as plt
import dask.array as da


from wrfvis import cfg, grid, graphics


def df_2D(param, zagl, t):
    
    '''
    Parameters
    ----------
    param : it is the variable
    zagl : it is the level
    t : it is the time

    Returns 
    -------
    data_array : data array that contains latitude, longitude and the associated
    variable
    wrf_hgt : it returns the elevation data array

    '''
    
    with xr.open_dataset(cfg.wrfout) as ds:
        # Convert binary times to datetime
        wrf_time = pd.to_datetime(
            [bytes.decode(time) for time in ds.Times.data], 
            format='%Y-%m-%d_%H:%M:%S'
        ) 
        # Replace time coordinate (1-len(time)) with datetime times
        ds = ds.assign_coords({'Time': wrf_time})

        # Extract lon, lat, and variable values for a fixed time and altitude
        lon = ds.XLONG[0, :, :]
        lat = ds.XLAT[0, :, :]

        if param == 'T':
            # WRF output is perturbation potential temperature
            vararray = ds[param][t, zagl, :, :] + 300
        else:
            vararray = ds[param][t, zagl, :, :]

    #Data array creation
    data_array = xr.DataArray(
        vararray.values,
        coords={'lat': lat.values[:, 0], 'lon': lon.values[0, :]},
        dims=['lat', 'lon']
    )

    # Add attributes to the data array
    data_array.attrs['variable_name'] = param
    data_array.attrs['variable_units'] = ds[param].units
    data_array.attrs['grid_point_elevation'] = zagl
    data_array.attrs['time'] = t

    return data_array

def plot_2D(data_array, time, elevation):
    
    '''
    Parameters
    ----------
    data_array : TYPE
        DESCRIPTION.
    time : TYPE
        DESCRIPTION.
    elevation : TYPE
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    '''
    
    attributes = data_array.attrs
    var_name = attributes['variable_name']
    var_units = attributes['variable_units']
    elevation = attributes['grid_point_elevation']
    time = attributes['time']
    print(attributes)
  
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_position([0.1, 0.1, 0.75, 0.85])
    ax.set_xlabel('Longitude ($^{\circ}$)', fontsize = 16)
    ax.set_ylabel('Latitude ($^{\circ}$)', fontsize = 16)
    
    da_plt = data_array.plot(ax=ax, add_colorbar=False)
    
    # Aggiungi una colorbar
    cbax = fig.add_axes([0.75, 0.1, 0.02, 0.75])
    plt.axis('off')
    cb = plt.colorbar(da_plt, ax=ax, fraction=0.1, format='%.0f')
    cb.ax.set_ylabel(f'${var_name}$ ({var_units})', fontsize = 15)
    plt.suptitle(f'${var_name}$[{var_units}] t={time} z={elevation}', x=0.5, y=0.95, ha='center', fontsize = 15)
    
    plt.xlabel('Longitude(°)')
    plt.ylabel('Latitude(°)')
    
    
    return fig


