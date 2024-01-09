# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 14:05:08 2024

@author: Stella Hell

this part is not working yet!!

I was sick alot over the lecture free time and could not spend the needed time 
on this project yet.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import dates

from wrfvis import cfg

def plot_hovmueller(df, filepath=None):
    ''' plot Hovmueller diagramm
    
    Parameters
    -----------
    df: pandas dataframe
        timeseries of df.variable_name
    '''
    # load needed longitudes and latitudes **EDIT HERE**
    lon = df.long.slice(-20, 60) # I still have to figure out how to access the longitude variable
    lat = df.lat.slice(40, -40) # I still have to figure out how to access the latitude variable
    
    parameter = df[df.attrs['variable_name']]
    # I need the more than the daily data for the parameter, at least a year,
    # better several years. I am not sure if that is the right command
    
    plt.figure(figsize=(10,4))
    
    # make monthly means of the parameter
    hov = parameter(lon, lat).groupby('time.month').mean(dim='time') - 273.15
    hov_z = hov.mean(dim='longitude')
    # plot
    hov_z.T.plot() # transpose the data with T, so that you have months on the xaxis
    
    # make labels **EDIT**
    # plt.ylabel(f"{df.attrs['variable_name']} ({df.attrs['variable_units']})")
    
    # make png - file (or something else) to include graph in html
    if filepath is not None:
        plt.savefig(filepath, dpi=150)
        plt.close()
        
    return plt.show()

