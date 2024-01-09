import matplotlib.pyplot as plt
from metpy.plots import SkewT
import xarray as xr
from wrfvis import grid, cfg


def skewt_prep(lon, lat):
    """ Read the necessary data for a Skew-T diagram from the WRF output file and transcribe it into a Pandas DataFrame
    for smaller use of RAM and subsequent plotting.

    Parameters
    ----------
    lon : float
        the longitude
    lat : float
        the latitude

    Returns
    -------
    df : pandas DataFrame
        Containing only the necessary data for the diagram in order to save memory.

    @author: Lucas Martins Castanho
    """

    # To-do:
    # Copy needed variables from WRF to DataFrame according to given variables.
    # Verify if memory usage is indeed lower and if doing this process is justifiable, otherwise only use plot_skewt()
    # and directly use data from WRF.

    # Goal:
    # Obtain (or derive) air pressure, air temperature, dew point, horizontal wind, and vertical wind from WRF;
    # store all the data in a DataFrame.

    with xr.open_dataset(cfg.wrfout) as ds:
        # find nearest grid cell
        ngcind, ngcdist = grid.find_nearest_gridcell(
            ds.XLONG[0, :, :], ds.XLAT[0, :, :], lon, lat)

    


def plot_skewt(df):
    # from metpy.plots import SkewT   # new!
    """
    Parameters
    ----------
    df: pandas DataFrame

    @author: Lucas Martins Castanho
    """

    # To-do:
    # Using metpy.plots.SkewT, create a Skew-T diagram using the data obtained with skewt_prep() and the draft below;
    # draft needs moist and dry adiabats, title and so on.
    # Create a test file to ensure the function outputs a valid diagram.

    # Goal:
    # Come out with a diagram that looks similar to this:
    # https://miro.medium.com/max/1104/1*M2ffqprzguzmGX-yYSKTUg.png

    height = df['height'].values
    p = df['pressure'].values
    T = df['temperature'].values
    Td = df['dewpoint'].values
    u = df['u_wind'].values
    v = df['v_wind'].values

    # make figure and `SkewT` object
    fig = plt.figure(figsize=(9, 9))
    skewt = SkewT(fig=fig, rotation=45)

    # plot sounding data
    skewt.plot(p, T, 'r')  # air temperature
    skewt.plot(p, Td, 'b')  # dew point
    skewt.plot_barbs(p[p >= 100], u[p >= 100], v[p >= 100])  # wind barbs
    
    