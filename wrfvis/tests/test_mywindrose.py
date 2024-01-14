# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 10:13:22 2024

@author: Johanna Silbernagl

test for mywindrose.py
"""

import xarray as xr
from wrfvis import cfg, mywindrose
import matplotlib as mpl
import numpy as np


def test_mywindrose_plot():
    """
    @author: Johanna Silbernagl
    test for the my_windrose function"""
    # load test dataset
    ds = xr.open_dataset(cfg.wrfout)

    # Check that title text is found in figure
    test_lat = 30
    test_lon = 100
    fig = mywindrose.my_windrose(ds, test_lat, test_lon)
    ref = 'Windspeed in m/s and winddirection at location latitude 30 longitude 100'
    test = [ref in t.get_text() for t in fig.findobj(mpl.text.Text)]
    assert np.any(test)
