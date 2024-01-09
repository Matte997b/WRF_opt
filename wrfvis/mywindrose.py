"""
Created on Wed Jan  3 11:37:17 2024

@author: Johanna Silbernagl

making a Windrose plot for the wrfvis package

command to run the code:
    my_windrose(ds, lat, lon)
"""
# import needed modules:

import numpy as np
import xarray as xr
from wrfvis import cfg
from wrfvis.grid import find_nearest_gridcell

# modules for the plots:
from windrose import WindroseAxes
import matplotlib.pyplot as plt


def my_windrose(ds, lat, lon):
    """ computes the winddirection and windspeed needed for the windrose plots
    for the specified location (lat,lon) from the dataset ds, and plots the
    windrose. The WindroseAxes function of the windrose package is needed.
    https://github.com/python-windrose/windrose .
    The dataset ds should be a WRF model output.
    @author: Johanna Silbernagl
    
    Parameters
    ----------
    ds: xarray dataset
        needs to contain the variables U, V
    lat: float
        latitude
    lon: float
        longitude

    Returns
    -------
    windrose plot for the specified location

    Raises
    ------
    ValueError:
        when chosen coordinates are not in range latitude[-90,90] and
        longitude [0-180]
    """

    # we don't need the whole dataset for the windrose-plot,
    # only the horizontal wind components
    print("Dimensions of 'U':", ds['U'].dims)
    print("Dimensions of 'V':", ds['V'].dims)
    print("Coordinates of 'U':", ds['U'].coords)
    print("Coordinates of 'V':", ds['V'].coords)
    
    variables_extract = ['U', 'V']
    wind_ds = ds[variables_extract]

    # Define the indices of the cell at the chosen latitude and longitude
    # latitude[-90,90] [NS] and longitude [0-180] [WE]
    if lat > 90 or lat < -90 or lon < 0 or lon > 180:
        raise ValueError(f'coordinates {lat} {lon} not available. Choose '
                         f'values for lat between -90 and 90 and for lon '
                         f'between 0 and 180.')
    target_latitude = lat
    target_longitude = lon
    index_of_cell = find_nearest_gridcell(wind_ds.XLONG, wind_ds.XLAT,
                                          target_longitude, target_latitude)
    # output = indices of nearest gridcell and distance to nearest cell

    # Extract the data at this cell
    cell_data = wind_ds.isel(south_north=index_of_cell[0][0],
                             west_east=index_of_cell[0][1])

    # unstagger the stagged dimensions (U = west_est_stag, V= south_north_stag)
    U_unstaggered = 0.5 * (cell_data.U[:, :, :-1] + cell_data.U[:, :, 1:])
    V_unstaggered = 0.5 * (cell_data.V[:, :-1, :] + cell_data.V[:, 1:, :])

    # Slice the larger array (U_unstaggered) to match the dimensions
    # 'bottom-top' of the smaller array (V_unstaggered)
    U_aligned = U_unstaggered.isel(bottom_top=slice(None, len(
        V_unstaggered.bottom_top)))

    # Now both U_aligned and V_unstaggered should have the same
    # dimensions, but are too large for the computation, so we reduce the
    # precision to float16 and do a downsample
    U_aligned = U_aligned.astype(np.float16)
    V_unstaggered = V_unstaggered.astype(np.float16)

    n = 60  # this value can be adhusted to downsample more or less
    U_downsampled = U_aligned.isel(bottom_top=slice(None, None, n))
    V_downsampled = V_unstaggered.isel(bottom_top=slice(None, None, n))

    # Calculate wind speed
    ws_downsampled = (U_downsampled ** 2 + V_downsampled ** 2) ** 0.5
    ws = ws_downsampled

    # Calculate wind direction (in radians), convert to degrees and shift to
    # north-centered convention
    wind_direction = np.arctan2(V_downsampled, U_downsampled)
    wind_direction_degrees = np.degrees(wind_direction) + 180.0
    wind_direction_degrees %= 360.0  # Ensure values are within 0-360 range
    wd = wind_direction_degrees

    # Reshape the arrays ws and wd to match the expected format of the plot
    # functions, 1D Arrays
    wd_1d = wd.stack(all_dims=['Time', 'bottom_top', 'south_north_stag',
                               'west_east_stag'])
    wd_reshaped = wd_1d.values
    ws_1d = ws.stack(all_dims=['Time', 'bottom_top', 'west_east_stag',
                               'south_north_stag'])
    ws_reshaped = ws_1d.values

    # plotting the windrose
    fig = WindroseAxes.from_ax()
    fig.bar(wd_reshaped, ws_reshaped, normed=True, opening=0.8,
           edgecolor="white")
    fig.set_legend()
    plt.title(f'Windspeed in m/s and winddirection at location latitude {lat} longitude {lon}')

    return fig
