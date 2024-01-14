"""Plenty of useful functions doing useful things.  """

import os
from tempfile import mkdtemp
import shutil

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from windrose import WindroseAxes

from wrfvis import cfg, grid, graphics, Two_dim_plot, mywindrose, skewT

def get_wrf_timeseries(param, lon, lat, zagl):
    """Read the time series from the WRF output file.
    
    Parameters
    ----------
    param: str
        WRF output variable (only 3D variables implemented so far)
    lon : float
        the longitude
    lat : float
        the latitude
    zagl : float
        height above ground level

    Returns
    -------
    df: pd.DataFrame 
        timeseries of param with additional attributes (grid cell lon, lat, dist, ...)
    wrf_hgt: xarray DataArray
        WRF topography
    """

    with xr.open_dataset(cfg.wrfout) as ds:
        # find nearest grid cell
        ngcind, ngcdist = grid.find_nearest_gridcell(
                          ds.XLONG[0,:,:], ds.XLAT[0,:,:], lon, lat)

        # find nearest vertical level
        nlind, nlhgt = grid.find_nearest_vlevel(
                       ds[['PHB', 'PH', 'HGT', param]], ngcind, param, zagl)

        # convert binary times to datetime
        wrf_time = pd.to_datetime(
                   [bytes.decode(time) for time in ds.Times.data], 
                   format='%Y-%m-%d_%H:%M:%S') 
        # replace time coordinate (1-len(time)) with datetime times
        ds = ds.assign_coords({'Time': wrf_time})

        # extract time series
        if param == 'T':
            # WRF output is perturbation potential temperature
            vararray = ds[param][np.arange(len(ds.Time)), nlind, ngcind[0], ngcind[1]] + 300
        else:
            vararray = ds[param][np.arange(len(ds.Time)), nlind, ngcind[0], ngcind[1]]
        df = vararray[:,0].to_dataframe()

        # add information about the variable
        df.attrs['variable_name'] = param
        df.attrs['variable_units'] = ds[param].units

        # add information about the location
        df.attrs['distance_to_grid_point'] = ngcdist
        df.attrs['lon_grid_point'] = ds.XLONG.to_numpy()[0, ngcind[0], ngcind[1]]
        df.attrs['lat_grid_point'] = ds.XLAT.to_numpy()[0, ngcind[0], ngcind[1]]
        df.attrs['grid_point_elevation_time0'] = nlhgt[0]

        # terrain elevation
        wrf_hgt = ds.HGT[0,:,:]

    return df, wrf_hgt


def mkdir(path, reset=False):
    """Check if directory exists and if not, create one.
        
    Parameters
    ----------
    path: str
        path to directory
    reset: bool 
        erase the content of the directory if it exists

    Returns
    -------
    path: str
        path to directory
    """
    
    if reset and os.path.exists(path):
        shutil.rmtree(path)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    return path


def write_html(param=None, lon=None, lat=None, zagl=None, t=None, elevation=None,
               directory=None, ds = None):
    """
    Author: Battisti Mattia
    Write an html page that contains the plots for different commands
    
    The function's variable are set to None because it is used for the different
    command lines of the terminal (README.txt for list of commands available)
    
    Parameters
    ----------
    param : str
        variable name
    lon : int
        longitute
    lat : int
        latitude
    zagl : int
        grid level for original command
    elevation : int
        grid level for module optimization
    t : int
        selected time
    directory : str
        directory where picture are stored and accessed to create the html

    Returns
    -------
    outpath : contains the path in which the htlm is stored

    """
    # create directory for the plot
    if directory is None:
        directory = mkdtemp()
    mkdir(directory)

    # extract timeseries from WRF output
    if t is None:
        print('Extracting timeseries at nearest grid cell')
        df, hgt = get_wrf_timeseries(param, lon, lat, zagl)
        print('Plotting data')
        # plot the timeseries
        png = os.path.join(directory, 'timeseries.png')
        graphics.plot_ts(df, filepath=png)

        # plot a topography map
        png = os.path.join(directory, 'topography.png')
        graphics.plot_topo(hgt, (df.attrs['lon_grid_point'], 
                           df.attrs['lat_grid_point']), filepath=png)
        
        # plot 2D map
        png = os.path.join(directory, '2D_variable.png')

        # create HTML from template
        outpath = os.path.join(directory, 'index.html')
        with open(cfg.html_template, 'r') as infile:
            lines = infile.readlines()
            out = []
            for txt in lines:
                txt = txt.replace('[PLOTTYPE]', 'Timeseries')
                txt = txt.replace('[PLOTVAR]', param)
                txt = txt.replace('[IMGTYPE]', 'timeseries')
                out.append(txt)
            with open(outpath, 'w') as outfile:
                outfile.writelines(out)
    else:
        da = Two_dim_plot.df_2D(param, elevation, t)
        
        if lat is not None and lon is not None:
            df, hgt = get_wrf_timeseries(param, lon, lat, elevation)
            lonlat = [lon, lat]
            
            hgt_path_2D = os.path.join(directory, 'HGT.png')
            graphics.plot_topo(hgt, lonlat, filepath=hgt_path_2D)
            
            png_path_ts = os.path.join(directory, 'timeseries.png')
            graphics.plot_ts(df, filepath=png_path_ts)
            
            png_windrose = os.path.join(directory, 'windrose.png')
            mywindrose.my_windrose(ds, lat, lon)
            plt.savefig(png_windrose)
        
        png_path_2D = os.path.join(directory, 'plot_2D.png')
        Two_dim_plot.plot_2D(da, t, elevation)
        plt.savefig(png_path_2D)
        plt.close()# Chiudi la figura dopo averla salvata
        
        outpath = os.path.join(directory, 'index_o.html')
        # create HTML from template
        if lat is not None and lon is not None:
            with open(cfg.html_template_o_1, 'r') as infile:
                lines = infile.readlines()
        else:
            with open(cfg.html_template_o, 'r') as infile:
                lines = infile.readlines()
        
        out = []
            
        '''for txt in lines:
            txt = txt.replace('[PLOTTYPE_2D]', '2D Map')
            txt = txt.replace('[PLOTVAR_2D]', param)
            txt = txt.replace('[IMGTYPE_2D]', 'plot_2D')
            txt = txt.replace('[IMGPATH_2D]', png_path_2D)
            out.append(txt)'''
                   
        if lat is not None and lon is not None:
            for txt in lines:
                    
                txt = txt.replace('[PLOTTYPE_2D]', '2D Map')
                txt = txt.replace('[PLOTVAR_2D]', param)
                txt = txt.replace('[IMGTYPE_2D]', 'plot_2D')
                txt = txt.replace('[IMGPATH_2D]', png_path_2D)

                txt = txt.replace('[PLOTTYPE_HGT]', 'HGT Map')
                txt = txt.replace('[PLOTVAR_HGT]', param)
                txt = txt.replace('[IMGTYPE_HGT]', 'HGT')
                txt = txt.replace('[IMGPATH_HGT]', hgt_path_2D)
                    
                txt = txt.replace('[PLOTTYPE_ts]', 'Timeseries')
                txt = txt.replace('[PLOTVAR_ts]', param)
                txt = txt.replace('[IMGTYPE_ts]', 'timeseries')
                txt = txt.replace('[IMGPATH_ts]', png_path_ts)
                
                txt = txt.replace('[PLOTTYPE_wr]', 'windrose')
                txt = txt.replace('[PLOTVAR_wr]', 'wind')
                txt = txt.replace('[IMGTYPE_wr]', 'windrose')
                txt = txt.replace('[IMGPATH_wr]', png_windrose)
                
                out.append(txt)
                
        else:
            for txt in lines:
                txt = txt.replace('[PLOTTYPE_2D]', '2D Map')
                txt = txt.replace('[PLOTVAR_2D]', param)
                txt = txt.replace('[IMGTYPE_2D]', 'plot_2D')
                txt = txt.replace('[IMGPATH_2D]', png_path_2D)
                out.append(txt)
                
        with open(outpath, 'w') as outfile:
            outfile.writelines(out)
        
        
                
        print('HTML file generated at:', outpath)
    
    return outpath
   
    
