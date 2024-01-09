#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Battisti Mattia
"""
# This is an additional module that contains functions to extract and plot file.nc data in 2D
# Further information can be found in the REDME.txt that contains a list of necessary modules
# and the commands available

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from wrfvis import cfg, grid, graphics


def df_2D(param, zagl, t):
    """
    Extract data from file.nc at fixed time and grid level
    
    This is very useful to simplify the visualization of data structure
    
    Parameters
    ----------
    param : str
        String that contains the variable to plot
    zagl : int
        Integer that represent the grid level
    t : TYPE
        Integer that represent the time 

    Returns
    -------
    data_array : it contains the data extracted from original file.nc at fixed 
                    time and grid level

    """
    
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
            vararray = ds[param][int(t), int(zagl), :, :] + 300
        elif np.ndim(ds[param]) >= 4:
            vararray = ds[param][t, zagl, :, :]
        elif np.ndim(ds[param]) <= 2:
            vararray = ds[param][:, :]
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


def df_2D_geo(param, target_potential_temperature, time):
    """
    Work in progress function
    NB the command line in the README.txt works anyway
    
    Parameters:
    - param: variable name
    - target_potential_temperature: int target potential temperature
    - time: int selected time
    
    Returns:
    - data_array: data ectracted at selected time and geopotential hight
    - wrf_hgt: elevazione xarray DataArray
    """
    
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


def plot_2D(data_array, time, elevation):
    """
    Plot of data extracted using the df_2D(param, zagl, t)
    
    Useful to visualize the data and understand better the meaning
    Time and elevation is used only to describe the figure obtained

    Parameters
    ----------
    data_array : it contains the data extracted
    time : int that contains the selected time
    elevation : int that contains the selected grid level

    Returns
    -------
    fig : plot of data on the overall region

    """
    
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


