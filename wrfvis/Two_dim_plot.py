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
    """Read the time series from the WRF output file.
    
    Parameters
    ----------
    param: str
        WRF output variable (only 3D variables implemented so far)
    
    zagl : float
        height above ground level

    Returns
    -------
    df: pd.DataFrame 
        timeseries of param with additional attributes (grid cell lon, lat, dist, ...)
    wrf_hgt: xarray DataArray
        WRF topography
    """

    """Plenty of useful functions doing useful things.  """
    
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

       # Create a DataFrame with lon, lat, and variable values
       df = pd.DataFrame({
           'lon': lon.values.flatten(),
           'lat': lat.values.flatten(),
           'variable': vararray.values.flatten()
       })

    # add information about the variable
    df.attrs['variable_name'] = param
    df.attrs['variable_units'] = ds[param].units

    # add information about the location
    df.attrs['grid_point_elevation_time0'] = zagl

    # terrain elevation
    wrf_hgt = ds.HGT[0,:,:]

    return df, wrf_hgt

def plot_2D(var, lon, lat):
    ''' plot variable

    Parameters
    ----------
    topo: xarray DataArray
        WRF topography

    lonlat: tuple
        longitude, latitude of WRF grid cell
    '''
    

  
    '''# Assuming lon and lat are 1D arrays
    lon, lat = np.meshgrid(lon, lat)
    # Use the actual data for your variable instead of linspace
    var_2d = np.array(var.iloc[2]).reshape(len(lat), len(lon))
    
    var_min = var.iloc[2].min()
    var_max = var.iloc[2].max()
    
    # Convert Pandas Series to NumPy array and reshape
    var_2d = np.array(var).reshape(len(lat), len(lon))
    
    # Create a Dask array from the original variable
    dask_var = da.from_array(var_2d, chunks=(100, 100))  # Adjust the chunk size as needed
    
    # Downsample using Dask
    var_2d_downsampled = dask_var.mean(axis=0).compute()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_position([0.1, 0.1, 0.75, 0.85])
    ax.set_xlabel('Longitude ($^{\circ}$)')
    ax.set_ylabel('Latitude ($^{\circ}$)')
    
    hc = ax.contourf(lon, lat, var_2d_downsampled, cmap='viridis', 
                 vmin=var_min, vmax=var_max, extend='both')

    # Scatter points at every grid cell
    ax.scatter(lon.flatten(), lat.flatten(), s=30, c='black', marker='s')
        
    
    lon, lat = np.meshgrid(np.linspace(lon.min(), lon.max(), 10000), np.linspace(lat.min(), lat.max(), 10000))
    #lon, lat = np.meshgrid(lon, lat)
    
    # Convert Pandas Series to NumPy array and reshape
    var_1d = np.linspace(var_min, var_max, 100000000)
    var_2d = var_1d.reshape(len(lat), len(lon))
    
    hc = ax.contourf(lon, lat, var_2d, cmap='viridis', 
                     vmin=var_min, vmax=var_max, extend='both')
    
    # Scatter points at every grid cell
    ax.scatter(lon.flatten(), lat.flatten(), s=30, c='black', marker='s')

    # colorbar
    cbax = fig.add_axes([0.88, 0.1, 0.02, 0.85])
    plt.axis('off')
    cb = plt.colorbar(hc, ax=cbax, fraction=1, format='%.0f')
    cb.ax.set_ylabel('$z$ (MSL)')'''
    
    var_min = var.iloc[2].min()
    var_max = var.iloc[2].max()
    
    
    # Assuming lon and lat are 1D arrays
    lon, lat = np.meshgrid(lon, lat)
    
    # Convert Pandas Series to NumPy array and reshape
    var_2d = np.array(var).reshape(len(lat), len(lon))
    
    # Create a Dask array from the original variable
    dask_var = da.from_array(var_2d, chunks=(100, 100))  # Adjust the chunk size as needed
    
    # Downsample using Dask
    var_2d_downsampled = dask_var.mean(axis=0).compute()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_position([0.1, 0.1, 0.75, 0.85])
    ax.set_xlabel('Longitude ($^{\circ}$)')
    ax.set_ylabel('Latitude ($^{\circ}$)')
    
    hc = ax.contourf(lon, lat, var_2d_downsampled, cmap='viridis', 
                     vmin=var_min, vmax=var_max, extend='both')
    
    # Scatter points at every grid cell
    ax.scatter(lon.flatten(), lat.flatten(), s=30, c='black', marker='s')
    
    # Colorbar
    cbax = fig.add_axes([0.88, 0.1, 0.02, 0.85])
    plt.axis('off')
    cb = plt.colorbar(hc, ax=cbax, fraction=1, format='%.0f')
    cb.ax.set_ylabel('$z$ (MSL)')
    
    plt.show()


    return fig