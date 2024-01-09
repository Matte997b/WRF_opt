""" contains command line tools of WRFvis

Mattia Battisti
November 2023
"""


import sys
import webbrowser

import wrfvis

HELP = """wrfvis_gridcell_o: Visualization of WRF output at a single selected grid cell.

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
HELP2 = """wrfvis_gridcell_o: Visualization of WRF output at a single selected grid cell.

Usage:
   -h, --help                       : print the help
   -v, --version                    : print the installed version
   -var, --variable[PARAM]          : WRF variable to plot
   -t, --time                     : WRF time
   -z, --level[HGT]               : WRF level
   --no-browser                     : the default behavior is to open a browser with the
                                      newly generated visualisation. Set to ignore
                                      and print the path to the html file instead
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
        print('wrfvis_gridcell_o: ' + wrfvis.__version__)
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
              'Type "wrfvis_gridcell_o --help" for usage information.')

def parameters(args_2):
    """The actual wrfvis_gridcell command line tool.

    Parameters
    ----------
    args: list
        output of sys.args[1:]
    """

    if '--variable' in args_2:
        args_2[args_2.index('--variable')] = '-var'
    if '--time' in args_2:
        args_2[args_2.index('--time')] = '-t'
    if '--level' in args_2:
        args_2[args_2.index('--level')] = '-z'  
    
    if len(args_2) == 0:
        print(HELP2)
    elif args_2[0] in ['-h', '--help']:
        print(HELP2)
    elif args_2[0] in ['-v', '--version']:
        print('wrfvis_gparameters_o: ' + wrfvis.__version__)
        print('Licence: public domain')
        print('wrfvis_gridcell is provided "as is", without warranty of any kind')
    elif ('-v' in args_2) and ('-t' in args_2) and ('-z' in args_2):
        variable = args_2[args_2.index('-var') + 1]
        time = float(args_2[args_2.index('-t') + 1])
        level = float(args_2[args_2.index('-z') + 3])
        html_path = wrfvis.write_html(variable, time, level)
        if '--no-browser' in args_2:
            print('File successfully generated at: ' + html_path)
        else:
            webbrowser.get().open_new_tab('file://' + html_path)
    else:
        print('wrfvis_gridcell: command not understood. '
              'Type "wrfvis_parameters_o --help" for usage information.')


def wrfvis_gridcell():
    """Entry point for the wrfvis_gridcell application script"""

    # Minimal code because we don't want to test for sys.argv
    # (we could, but this is way above the purpose of this package
    gridcell(sys.argv[1:])

def wrfvis_parameters():
    parameters(sys.argv[1:])
