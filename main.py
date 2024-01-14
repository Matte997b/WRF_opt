#Just a module to develope the command proposed by the author in this package
#NB this module can be useful to understand data structure and plots but its limited
#because user cannot choose the variable from command line


from wrfvis.core import write_html
from wrfvis.core import get_wrf_timeseries
from wrfvis.Two_dim_plot import df_2D, plot_2D, df_2D_geo_var#, df_2D_geo find_geopotential_height_all_locations
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from wrfvis.cfg import wrfout

def main():
    
    time = 0
    z_lvl = 0
    var ='T'
    
    #T_= df_2D('T', z_lvl, time)
    #T_g = df_2D('T', z_lvl, time)
    #Alpha = df_2D('ALBEDO', z_lvl, time)
    #HF = df_2D('HFX', z_lvl, time)
    #HF = df_2D(grid.wrf_zagl, z_lvl, time)
    
    #T_ = df_2D(var, z_lvl, time)
    #ds = get_wrf_timeseries(var, 10, 40, 0)
    #T_g = df_2D_geo(var, z_lvl, time)
    
    #lon = da['XLONG'].values[0, :, :]
    #lat = da['XLAT'].values[0, :, :]
    #print(T_.indexes)
    #print(T_)
    #print(Alpha.indexes)
    #print(HF.indexes)
 
    #a = plot_2D(T_, time, z_lvl)
    #plt.show(a)
    #plot_topo(HGT, )
    #b = plot_2D(T_g, time, z_lvl)
    #plt.show(b)
    #plot_2D(Alpha, z_lvl, time)
    #plot_2D(HF, z_lvl, time)
    
    ds = xr.open_dataset(wrfout)
    print(ds.data_vars)
    
    variable_at_height = df_2D_geo_var(var, 5500, 0, 0)
    
    '''# Plotta la matrice in 2D
    plt.imshow(variable_at_height, cmap='viridis', origin='lower')
    plt.colorbar(label='Valori della variabile')  # Aggiungi la barra dei colori
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.title('Rappresentazione 2D della variabile')
    # Mostra il plot
    plt.show()'''
    
    
    

if __name__=="__main__":
    main()
    