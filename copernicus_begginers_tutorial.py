# Import libraries
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# To avoid warning messages
import warnings
warnings.filterwarnings('ignore')


# Define the paths to the NetCDF files
# Model temperature dataset
path_mod = 'nc_files/mod_bio.nc'
# satellite observation dataset
path_sat = 'nc_files/chl_sat.nc'
# in situ dataset
path_mooring = 'nc_files/MO_TS_MO_Olympiada.nc'

# %run opendap_config.py

# Open the product with OPeNDAP and store it in a Python variable
# sat_opendap = xr.open_dataset('https://nrt.cmems-du.eu/thredds/dodsC/dataset-oc-med-chl-olci-l4-chl_300m_monthly-rt')

# Open the files and store them in a Python variable
mod = xr.open_dataset(path_mod)
sat = xr.open_dataset(path_sat)
mooring = xr.open_dataset(path_mooring)

sat

# sat.thetao.sel(time='2022-05-22').plot()
# plt.show()

# Use the variable as a DataArray
chl_sat = sat.CHL
# or 
chl_sat = sat['CHL']

# Display the content of the variable
chl_sat


# Store the variable as an array in Python
chl_data = sat.CHL.data

# Display the content of the variable. The command displays the extremities of the map, filled with NaN
chl_data


# Check the date times included in the file
sat['time']

# If you know the exact date
sat.sel(time='2021-11-01')

# If you don't know the exact date and want to take the nearest one
sat.sel(time='2021-11-05T00', method='nearest')

sat.sel(time=slice('2021-08-01','2021-12-31'))

sat

# Plot a time series-----------
# Get the location of the mooring
lon = mooring.LONGITUDE.data[0]
lat = mooring.LATITUDE.data[0]
depth = mooring.DEPH.data[0][0]

# Define the caracteristics of the plot
f = plt.figure(figsize=(12,10))                                       # create a figure and define its size
ax = f.add_subplot(111)                                               # create the axes of the plot
ax.grid()                                                             # add the grid lines
ax.set_title("Chlorophyll concentration (mg/m3)",fontsize=24)         # add the figure title
f.suptitle('Longitude : ' +str(lon) +'?E\nLatitude : ' + str(lat)+'?N\nDepth : '+ str(depth)+'m\n',
           fontsize=18,horizontalalignment='left',x=0.12)             # Display the coordinates on the plot
f.autofmt_xdate()                                                     # format the dates in the x axis 
im = ax.plot(mooring['TIME'],mooring['CPHL'])                         # plot the time serie

# Display the location of the point on a mini map
ax_mini_map = f.add_axes([0.73, 0.91, 0.2, 0.15], projection=ccrs.PlateCarree()) # create the minimap and define its projection
gl = ax_mini_map.gridlines(draw_labels=True)                                     # add the coastlines
gl.right_labels = False                                                          # remove latitude labels on the right
gl.top_labels = False                                                            # remove longitude labels on the top
ax_mini_map.add_feature(cfeature.LAND, zorder=1, edgecolor='k')                  # add land mask 
ax_mini_map.set_extent([-2, 35, 30, 46],crs=ccrs.PlateCarree())          # define the extent of the map [lon_min,lon_max,lat_min,lat_max]
ax_mini_map.scatter(lon, lat, 30,transform=ccrs.PlateCarree())           # plot the location of the point

# Save figure
plt.savefig('figures/temp_time_series.png')





# Select the temperature parameter, at the date and depth we want, and store it in a variable.
chl_sat = sat['CHL'].sel(time='2022-01-01').squeeze()

# Define the caracteristics of the plot
f = plt.figure(figsize=(15, 8))                                                    # create a figure and define its size
ax = plt.axes(projection=ccrs.PlateCarree())                                       # create an ax and select the projection of the map
ax.coastlines()                                                                    # add the coastlines
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)                        # add the longitude / latitude lines
gl.right_labels = False                                                            # remove latitude labels on the right
gl.top_labels = False                                                              # remove longitude labels on the top
ax.add_feature(cfeature.LAND, zorder=1, edgecolor='k')                             # add land mask
ax.set_extent([-2, 35, 30, 46],crs=ccrs.PlateCarree())                             # define the extent of the map [lon_min,lon_max,lat_min,lat_max]

# Plot the sea surface temperature, set the min/max values of the colorbar and the colormap to use
im = ax.pcolor(chl_sat['lon'].data, chl_sat['lat'].data,chl_sat,vmin=0,vmax=1.2,cmap='viridis')
    

# Add the titles and legend
f.suptitle('Sea surface chlorophyll in January 2022',fontsize=25)                 # add a title to the figure
cbar = f.colorbar(im,ax=ax,fraction=0.03,pad=0.04,orientation='horizontal')       # add the colorbar
cbar.set_label('mg/m3',fontsize=20)                                               # add the title of the colorbar

plt.show()

# Save figure
plt.savefig('figures/chl_map.png')

# vertical profile------
mod

# Define the coordinates of the point on which to plot the time series
lon, lat = 5, 42
date1, date2 = '2022-01-01', '2022-02-01'

# Select the temperature variable from the product, at this point and this date
chl_mod_1 = mod['chl'].sel(longitude=lon,latitude=lat,time=date1,method='nearest')
chl_mod_2 = mod['chl'].sel(longitude=lon,latitude=lat,time=date2,method='nearest')

# Display the content of the new variable
chl_mod_1

#save as nctcdf
chl_mod_1.to_netcdf("chl_mod_1.nc")

# Define the caracteristics of the plot
f = plt.figure(figsize=(8,12))                                       # create a figure and define its size
ax = f.add_subplot(111)                                              # create the axes of the plot
ax.grid()                                                            # add the grid lines
ax.set_title("Chlorophyll concentration (mg/m3)",fontsize=10)                     # add the figure title
ax.invert_yaxis()                                                    # reverse the y axis
ax.set_xlabel("mg/m3",fontsize=10)                                   # set x axis label
ax.set_ylabel("Depth (m)",fontsize=10)                               # set y axis label 

im1 = ax.plot(chl_mod_1,chl_mod_1['depth'],label=date1)              # plot the vertical profile
im2 = ax.plot(chl_mod_2,chl_mod_2['depth'],label=date2)              # plot the vertical profile


# Display the locations of the glider on a mini map
ax_mini_map = f.add_axes([0.73, 0.91, 0.2, 0.15], projection=ccrs.PlateCarree()) # create the minimap and define its projection
gl = ax_mini_map.gridlines(draw_labels=True)                                     # add the coastlines
gl.right_labels = False                                                          # remove latitude labels on the right
gl.top_labels = False                                                            # remove longitude labels on the top
ax_mini_map.add_feature(cfeature.LAND, zorder=1, edgecolor='k')       # add land mask 
ax_mini_map.set_extent([-2, 35, 30, 46],crs=ccrs.PlateCarree())       # define the extent of the map [lon_min,lon_max,lat_min,lat_max]
ax_mini_map.scatter(lon, lat, 10,transform=ccrs.PlateCarree())      # plot the first location
ax_mini_map.scatter(lon, lat, 10,transform=ccrs.PlateCarree())      # plot the second location
ax.legend(loc="upper left") 

plt.show()


## plot a slice

# Set the coordinates of the line
lon_min, lon_max = 13.2, 16.5
lat = 43.7

# Get the temperature values along this line for a defined date
chl_mod = mod.sel(latitude=lat,method='nearest').sel(longitude=slice(lon_min,lon_max)).isel(time=[0]).squeeze()

#save as nctcdf
#save as nctcdf
chl_mod.to_netcdf("nc_files/chl_mod_slice.nc")
