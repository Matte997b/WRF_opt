# GROUP A, visualization package for WRF model output for avition purposes

**wrfvis** offers command line tools to display WRF model output in your browser.

It was written for the University of Innsbruck's
[scientific programming](https://manuelalehner.github.io/scientific_programming)
course as a package template for the semester project and is based on the 
example packages [scispack](https://github.com/fmaussion/scispack) and
[climvis](https://github.com/fmaussion/climvis) written by
[Fabien Maussion](https://fabienmaussion.info).
Modification and new implementation of the original code are provided by Group A.
In partucular functions to:
- New command line [Battisti Mattia]
- Horizontal cross-section [Battisti Mattia]
- SkewT diagram [Lucas Martins Castanho]
- Hovmuller diagram [Stella Hell]
- Windrose [Johanna Silbernagl]

## HowTo
Make sure you have all dependencies installed. These are:
- numpy
- pandas
- xarray
- matplotlib
- pytest
- metpy
- windrose

Two possible setup:

    1- ** Standard setup **
    
        Download the package and install it. From the root directory, do:
    
            $ pip install .
        
        If you are on a computer with different users, you should use:
        
            $ pip install --user .
          
    2- ** Developer setup ** (If you need to work on the package and change it)
    
        Download the package and install it. From the root directory, do:
    
            $ pip install .
        
        If you are on a computer with different users, you should use:
    
            $ pip install --user .

## Command line interface

``setup.py`` defines an "entry point" for a script to be used as a
command line program.

After installation, just type

    - $ wrfvis_gridcell -h for help
    or
    - $ wrfvis_parameters -h for help

to see what the tool can do.

# NB the wrfvis_parameters give the 2D_plot and windrose, for skewT and Hovmuller

## Testing
We recommend to use [pytest](https://docs.pytest.org) for testing. To test
the package, run

    $ pytest .

in the package root directory.

Further understanding of data structure and visualization can be seen into the
main module that it was used to develop the optimization.

## License

With the exception of the ``setup.py`` file, which was adapted from the
[sampleproject](https://github.com/pypa/sampleproject) package, all the
code in this repository is dedicated to the public domain.

## Authors

Mattia Battisti
Stella Hell
Johanna Silbernagl
Lucas Martins Castanho
