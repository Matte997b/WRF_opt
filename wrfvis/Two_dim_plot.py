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


'''def df_2D_geo_var(param, target_geopotential_height, time_step, level):
    """
    Work in progress function
    
    Parameters:
    - param: variable name
    - target_geopotential_height: float target geopotential height
    - time_step: int selected time step
    
    Returns:
    - variable_at_height: data extracted at selected time, target geopotential height
    """
    with xr.open_dataset(cfg.wrfout) as ds:
        # Convert time step to the corresponding time index
        time_index = time_step

        # Calcola l'altezza geopotenziale totale
        geopotential_total = ds['PH'] + ds['PHB']
        
        varray = geopotential_total[int(time_step), :, :, :]

    return varray'''



def df_2D_geo_var(param, target_geopotential_height, time_step, level):
    """
    Work in progress function
    
    Parameters:
    - param: variable name
    - target_geopotential_height: float target geopotential height
    - time_step: int selected time step
    
    Returns:
    - variable_at_height: data extracted at selected time, target geopotential height
    - variable_at_same_height: data extracted from the same variable at the same geopotential height
    """
    with xr.open_dataset(cfg.wrfout) as ds:
        # Convert time step to the corresponding time index
        time_index = time_step

        # Calcola l'altezza geopotenziale totale
        print(ds['PH'])
        print('PH', ds['PH'][time_step, :, :, :].attrs)
        print('PHB', ds['PHB'][time_step, :, :, :].attrs)
        geopotential_total = ((ds['PHB'][time_step, 0, :, :] + ds['PH'][time_step, 0, :, :]) - ds['HGT'][0, :, :])
        plt.imshow(geopotential_total[:,:])
        plt.colorbar(label='Valori della variabile')  # Aggiungi la barra dei colori
        # Trova gli indici dove l'altezza geopotenziale è vicina al valore target
        indices_same_geopotential = np.where(np.isclose(geopotential_total.isel(Time=time_index).values, target_geopotential_height))

        # Estrai i valori della variabile alla stessa altezza geopotenziale
        variable_at_same_geopotential = ds[param].isel(Time=time_index, bottom_top=level,
                                                      south_north=indices_same_geopotential[1],
                                                      west_east=indices_same_geopotential[2])

        # Rimuovi eventuali dimensioni aggiuntive di grandezza 1
        variable_at_same_geopotential = variable_at_same_geopotential.squeeze()

        # Estrai i valori della variabile per l'intero dominio alla stessa altezza geopotenziale
        variable_at_height = ds[param].isel(Time=time_index, bottom_top=level) + 300

    #return variable_at_height






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
    plt.suptitle(f'${var_name}$[{var_units}] t={time} z={elevation}', x=0.5, 
                 y=0.95, ha='center', fontsize = 15)
    
    plt.xlabel('Longitude(°)')
    plt.ylabel('Latitude(°)')
    
    return fig


