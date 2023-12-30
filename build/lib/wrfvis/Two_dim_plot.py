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

'''def find_geopotential_height_all_locations(ds, level_index, param, ztarget):
    """
    Find geopotential height for all lon-lat pairs at a specific vertical level.

    Parameters
    ----------
    ds: xarray dataset
        Needs to contain the variables PHB, PH, HGT, and param.
    level_index: int
        Index of the vertical level for which to calculate geopotential height.
    param: str
        Variable for which to determine the nearest vertical level.
    ztarget: float
        Target height AGL.

    Returns
    -------
    wrf_zagl: xarray DataArray
        Height above ground level for all lon-lat pairs and time steps.
    nlind: numpy array, integer
        Index of nearest vertical level at each time.
    nlhgt: numpy array, float
        Height of nearest vertical level at each time.
    """

    # Explicitly align variables along common dimensions
    ds_aligned = xr.align(ds['PHB'], ds['HGT'], join='exact')
    #print(ds_aligned)
    
    # Extract aligned variables
    phb_aligned = ds_aligned[0]
    hgt_aligned = ds_aligned[1]
    
    # Now, you can perform operations without dimension conflicts
    geopot_hgt = (phb_aligned + ds['PH'][:, level_index, :, :]) / 9.81

    geopot_hgt_subset = geopot_hgt[:, :hgt_aligned.shape[1], :hgt_aligned.shape[2]]
    # Geopotential height
    #geopot_hgt = (ds['PHB'][:, level_index, :, :] + ds['PH'][:, level_index, :, :]) / 9.81

    # Unstagger the geopotential height to half levels
    if 'bottom_top' in ds.dims:
        #geopot_hgt = 0.5 * (geopot_hgt[:, :-1] + geopot_hgt[:, 1:])
        geopot_hgt_subset = 0.5 * (geopot_hgt_subset[:, :-1] + geopot_hgt_subset[:, 1:])

    # Subtract topo height to get height above ground
    #wrf_zagl = geopot_hgt - hgt_aligned
    #wrf_zagl = geopot_hgt - ds['HGT'][:, :, :]
    wrf_zagl = geopot_hgt_subset - hgt_aligned
    
    # Debugging: Print shapes
    print("geopot_hgt shape:", geopot_hgt.shape)
    print("hgt_aligned shape:", hgt_aligned.shape)
    print('ssssssssss', wrf_zagl.dims)

    # Find nearest vertical level
    nlind = np.argmin(np.abs(wrf_zagl - ztarget).to_numpy(), axis=0)
    #print(nlind.shape)
    #nlhgt = wrf_zagl.to_numpy()[np.arange(len(nlind)), nlind, :, :]
    #nlhgt = wrf_zagl[:, nlind., :, :]
    
    return wrf_zagl, nlind #, nlhgt'''

def da_GPH(zagl, t):
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
    return ds
    
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
        
    
        if param == 'T' and np.ndim(ds[param]) >= 4:
            # WRF output is perturbation potential temperature
            vararray = ds[param][t, zagl, :, :] + 300
        
        elif np.ndim(ds[param]) >= 4:
            vararray = ds[param][t, zagl, :, :]
        
        else:
            vararray = ds[param][t, :, :]
            
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

'''def df_2D_geo(param, target_potential_temperature, time):
    """
    Parameters:
    - param: variable name
    - target_potential_temperature: target potential temperature
    - time: datetime object representing the desired time
    
    Returns:
    - data_array: xarray DataArray containing latitude, longitude, and the associated variable
    - wrf_hgt: elevation xarray DataArray
    """
    with xr.open_dataset(cfg.wrfout) as ds:
        # Replace time coordinate with datetime times
        ds = ds.assign_coords({'Time': pd.to_datetime(ds.Times.data.astype(str), format='%Y-%m-%d_%H:%M:%S')})
        
        # Extract lon, lat, and variable values
        lon = ds.XLONG[0, :, :]
        lat = ds.XLAT[0, :, :]
        
        # Calculate geopotential height (example: sum of geopotential and terrain height)
        geopotential_height = ds['PH'].values + ds['PHB'].values
        terrain_height = ds['HGT'].values
        terrain_height_expanded = np.zeros_like(geopotential_height[:, :1, :, :])
        print("geopotential_height shape:", geopotential_height.shape)
        print("terrain_height_expanded shape:", terrain_height_expanded.shape)
        total_geopotential_height = geopotential_height + terrain_height_expanded
        print("total_geopotential_height shape:", total_geopotential_height.shape)


        # Define the target potential temperature
    target_index = np.argmin(np.abs(ds['T'].values - target_potential_temperature), axis=1)
    
    if param in ds.variables:
        # Extract variable values at the level corresponding to the target potential temperature
        vararray = ds[param].values[:, target_index, :, :].squeeze()
    else:
        raise ValueError(f"Variable '{param}' not found in the dataset.")
            
    # DataArray creation
    data_array = xr.DataArray(
        vararray,
        coords={'Time': ds['Time'], 'lat': lat.values[:, 0], 'lon': lon.values[0, :]},
        dims=['Time', 'lat', 'lon'])

    # Add attributes to the data array
    data_array.attrs['variable_name'] = param
    data_array.attrs['variable_units'] = ds[param].units
    data_array.attrs['target_potential_temperature'] = target_potential_temperature

    return data_array'''

def df_2D_geo(param, target_potential_temperature, time):
    '''
    Parameters:
    - param: nome della variabile
    - target_potential_temperature: temperatura potenziale target
    - time: oggetto datetime che rappresenta il tempo desiderato
    
    Returns:
    - data_array: xarray DataArray contenente latitudine, longitudine e la variabile associata
    - wrf_hgt: elevazione xarray DataArray
    '''
    with xr.open_dataset(cfg.wrfout) as ds:
        # Sostituisci la coordinata del tempo con i tempi datetime
        ds = ds.assign_coords({'Time': pd.to_datetime(ds.Times.data.astype(str), format='%Y-%m-%d_%H:%M:%S')})
        
        # Estrai lon, lat e valori della variabile
        lon = ds.XLONG[0, :, :]
        lat = ds.XLAT[0, :, :]
        
        # Calcola l'altezza geopotenziale (esempio: somma di altezza geopotenziale ed altezza del terreno)
        geopotential_height = ds['PH'].values + ds['PHB'].values
        terrain_height = ds['HGT'].values
        terrain_height_expanded = terrain_height[:, np.newaxis, :, :]
        total_geopotential_height = geopotential_height + terrain_height_expanded

        # Definisci la temperatura potenziale target
        target_index = np.argmin(np.abs(ds['T'].values[:, :, :, :] - target_potential_temperature), axis=1)
        print(target_index.shape)
        
        if param in ds.variables:
            # Estrai i valori della variabile al livello corrispondente alla temperatura potenziale target
            vararray = ds[param].values[:, int(target_potential_temperature), target_index[0, :, :], target_index[1, :, :]]
        else:
            raise ValueError(f"Variabile '{param}' non trovata nel dataset.")
            
    # Creazione di DataArray
    data_array = xr.DataArray(
        vararray,
        coords={'Time': ds['Time'], 'lat': lat.values[:, 0], 'lon': lon.values[0, :]},
        dims=['Time', 'lat', 'lon']
    )

    # Aggiungi attributi al data array
    data_array.attrs['variable_name'] = param
    data_array.attrs['variable_units'] = ds[param].units
    data_array.attrs['target_potential_temperature'] = target_potential_temperature

    return data_array



def plot_topo(topo, lonlat):
    """plot topography

    Parameters
    ----------
    topo: xarray DataArray
        WRF topography

    lonlat: tuple
        longitude, latitude of WRF grid cell
    """

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_position([0.1, 0.1, 0.75, 0.85])
    ax.set_xlabel('Longitude ($^{\circ}$)')
    ax.set_ylabel('Latitude ($^{\circ}$)')

    clevels = np.arange(cfg.topo_min, cfg.topo_max, 200)
    hc = ax.contourf(topo.XLONG, topo.XLAT, topo.data, levels=clevels, cmap='terrain', 
                     vmin=cfg.topo_min, vmax=cfg.topo_max, extend='both')
    ax.scatter(*lonlat, s=30, c='black', marker='s')

    # colorbar
    cbax = fig.add_axes([0.88, 0.1, 0.02, 0.85])
    plt.axis('off')
    cb = plt.colorbar(hc, ax=cbax, fraction=1, format='%.0f')
    cb.ax.set_ylabel('$z$ (MSL)')

    return fig

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
    print(attributes)
    var_name = attributes['variable_name']
    var_units = attributes['variable_units']
    if 'grid_point_elevation' in attributes:
        elevation = attributes['grid_point_elevation']
        time = attributes['time']
    else:
        elevation = attributes['target_potential_temperature']
        time = 0
    
  
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


