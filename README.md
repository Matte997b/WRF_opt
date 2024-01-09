# A visualization package for WRF model output

**wrfvis** offers command line tools to display WRF model output in your browser.

It was written for the University of Innsbruck's
[scientific programming](https://manuelalehner.github.io/scientific_programming)
course as a package template for the semester project and is based on the 
example packages [scispack](https://github.com/fmaussion/scispack) and
[climvis](https://github.com/fmaussion/climvis) written by
[Fabien Maussion](https://fabienmaussion.info).
Modification of the original code are provided by Battisti Mattia

## HowTo

Make sure you have all dependencies installed. These are:
- numpy
- pandas
- xarray
- matplotlib
- pytest
- metpy
- windrose

Download the package and install it in development mode. From the root directory,
do:

    $ pip install -e .

If you are on a university computer, you should use:

    $ pip install --user -e .

## Command line interface

#NB in cfg it necessary to indicate the path data

``setup.py`` defines an "entry point" for a script to be used as a
command line program. Currently, the only command installed is ``wrfvis_gridcell``.

After installation, just type

    $ wrfvis_gridcell_o -h for help
    $ wrfvis_parameters_o -h for help

to see what the tool can do.

# NB the wrfvis_parameters_o give the 2D_plot and windrose, for skewT and Hovmuller
# further works is needed 

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

