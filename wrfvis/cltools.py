""" contains command line tools of WRFvis

Author:Manuela Lenher
November 2023

Optimization and further modification: Battisti Mattia
December 2023
"""


import sys
import webbrowser

import wrfvis
import xarray as xr
from wrfvis import cfg

HELP = """wrfvis_gridcell: Visualization of WRF output at a single selected grid cell.

Usage:
   -h, --help                       : print the help
   -v, --version                    : print the installed version
   -p, --parameter [PARAM]          : WRF variable to plot
   -l, --location [LON] [LAT] [HGT] : location and height above ground of the grid 
                                      cell for which to plot the data
   --no-browser                     : the default behavior is to open a browser with the
                                      newly generated visualisation. Set to ignore
                                      and print the path to the html file instead
"""


HELP2 = """wrfvis_parameters: Visualization of WRF output at a single selected grid cell.
Change the name of command
Usage:
   -h, --help                       : print the help
   -v, --version                    : print the installed version
   -var, --variable[PARAM]          : WRF variable to plot
   -t, --time                     : WRF time
   -z, --level[HGT]               : WRF level
   -c, --coord [lon lat]          :WEF coordinates
   --no-browser                     : the default behavior is to open a browser with the
                                      newly generated visualisation. Set to ignore
                                      and print the path to the html file instead
EXAMPLE: wrfvis_gridcell -var T -t 0 -z 0 -c 10 40
@author Battisti Mattia
"""


def gridcell(args):
    """The actual wrfvis_gridcell command line tool.

    Parameters
    ----------
    args: list
        output of sys.args[1:]
    """

    if '--parameter' in args:
        args[args.index('--parameter')] = '-p'
    if '--location' in args:
        args[args.index('--location')] = '-l'

    if len(args) == 0:
        print(HELP)
    elif args[0] in ['-h', '--help']:
        print(HELP)
    elif args[0] in ['-v', '--version']:
        print('wrfvis_gridcell: ' + wrfvis.__version__)
        print('Licence: public domain')
        print('wrfvis_gridcell is provided "as is", without warranty of any kind')
    elif ('-p' in args) and ('-l' in args):
        param = args[args.index('-p') + 1]
        lon = float(args[args.index('-l') + 1])
        lat = float(args[args.index('-l') + 2])
        zagl = float(args[args.index('-l') + 3])
        html_path = wrfvis.write_html(param, lon, lat, zagl)
        if '--no-browser' in args:
            print('File successfully generated at: ' + html_path)
        else:
            webbrowser.get().open_new_tab('file://' + html_path)
    else:
        print('wrfvis_gridcell: command not understood. '
              'Type "wrfvis_gridcell --help" for usage information.')
        
def parameters(args_2):
    """
    Author: Battisti Mattia
    The actual wrfvis_parameters command line tool.
    
    The output consists in the opening of an html that contains the desired plots

    Parameters
    ----------
    args_2 : list
        output of sys.args[1:]

    Returns
    -------
    None. 

    """
    level = None
    print("Command-line arguments:", args_2)

    if '--variable' in args_2:
        index = args_2.index('--variable')
        args_2[index] = '-var'
        args_2[index + 1] = args_2[index + 1].lstrip('-')

    if '--time' in args_2:
        args_2[args_2.index('--time')] = '-t'
    if '--level' in args_2:
        args_2[args_2.index('--level')] = '-z'
    
    
    if '--coord' in args_2:
        coord_index = args_2.index('--coord')
        args_2[coord_index] = '-c'
        lon = float(args_2[coord_index + 1])
        lat = float(args_2[coord_index + 2])

    try:
        if '-var' in args_2:
            variable_index = args_2.index('-var') + 1
            variable = args_2[variable_index]

            if variable.startswith('-'):
                raise ValueError("Missing value for option -var")
    except IndexError:
        print("Missing value for option -var")
        return
    print(args_2)

    if len(args_2) == 0:
        print(HELP2)
    elif args_2[0] in ['-h', '--help']:
        print(HELP2)
    elif args_2[0] in ['-v', '--version']:
        print('wrfvis_parameters: ' + wrfvis.__version__)
        print('Licence: public domain')
        print('wrfvis_parameters is provided "as is", without warranty of any kind')
           
    elif ('-var' in args_2) and ('-t' in args_2) and ('-z' in args_2):
        time_index = args_2.index('-t') + 1
        level_option_index = args_2.index('-z')
        variable = args_2[variable_index]
        
        if args_2[time_index].startswith('-'):
            raise ValueError("Missing value for option -t")

        time = int(float(args_2[time_index]))  # Converti il tempo in un intero
        level = (float(args_2[level_option_index + 1]) 
                 if level_option_index + 1 < len(args_2) else None)
    
        if '-c' in args_2:
            coord_index = args_2.index('-c')
            coord = args_2[coord_index + 1:]
            if len(coord) >= 2:
                lon = float(coord[0])
                lat = float(coord[1])
            else:
                print("Missing longitude or latitude values for option -c")
                return
        else:
            lon = None  
            lat = None
    
        print("Variable:", variable)
        print("Time:", time)
        print("Level:", level)
        print(lon, lat)
        
        ds = xr.open_dataset(cfg.wrfout)
        
        if '-c' in args_2:
            html_path = wrfvis.write_html(param=variable, t=time, elevation=level, 
                                          lon=lon, lat=lat,directory=None, ds = ds)
        else:
            html_path = wrfvis.write_html(param=variable, t=time, 
                                          elevation=level, directory=None)
            
        if '--no-browser' in args_2:
            print('File successfully generated at:', html_path)
            
        else:
            webbrowser.get().open_new_tab('file://' + html_path)
            
    else:
        print('wrfvis_parameters_o: command not understood. '
              'Type "wrfvis_parameters --help" for usage information.')



def wrfvis_gridcell():
    """
    Entry point for the wrfvis_gridcell application script
    """

    # Minimal code because we don't want to test for sys.argv
    # (we could, but this is way above the purpose of this package
    gridcell(sys.argv[1:])

def wrfvis_parameters():
    """
    Author: Battisti Mattia
    Entry point for the wrfvis_parameters application script
    """
    parameters(sys.argv[1:])
