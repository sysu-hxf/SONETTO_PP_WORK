# 这个模块读取ERA5, ECM, GGF, GGFMT在起报时刻的温度（K）、位势高度（10 gpm）和水平风(m/s)，并插值到postvar的经纬度网格上
from utilities import *

ds_era5 = xr.open_dataset(file_era5)
ds_ECM = xr.open_dataset(file_ECM)
ds_GGF = xr.open_dataset(file_GGF)
ds_GGFMT = xr.open_dataset(file_GGFMT)

# 统一采用postvar输出的经纬度网格
Model_lon, Model_lat = ds_ECM['lon'], ds_ECM['lat']

# ECM 
t_ECM        = ds_ECM['t'][0,:,:,:]
gh_ECM       = ds_ECM['h'][0,:,:,:]/10   #  转换为10gpm以方便作图
u_ECM, v_ECM = ds_ECM['u'][0,:,:,:], ds_ECM['v'][0,:,:,:]
# GGF
t_GGF        = ds_GGF['t'][0,:,:,:] 
gh_GGF       = ds_GGF['h'][0,:,:,:]/10
u_GGF, v_GGF = ds_GGF['u'][0,:,:,:], ds_GGF['v'][0,:,:,:]
# GGFMT
t_GGFMT      = ds_GGFMT['t'][0,:,:,:]
gh_GGFMT     = ds_GGFMT['h'][0,:,:,:]/10
u_GGFMT, v_GGFMT = ds_GGFMT['u'][0,:,:,:], ds_GGFMT['v'][0,:,:,:]

# ERA5
t_era  = ds_era5['t'][0,:,:,:]
gh_era = ds_era5['z'][0,:,:,:]/98.0665
u_era, v_era = ds_era5['u'][0,:,:,:], ds_era5['v'][0,:,:,:]
# 对ERA5数据进行插值到postvar的经纬度网格上
t_era5_INTE  = t_era.interp(latitude  = Model_lat, longitude = Model_lon)
gh_era5_INTE = gh_era.interp(latitude = Model_lat, longitude = Model_lon)
u_era5_INTE, v_era5_INTE = u_era.interp(latitude = Model_lat, longitude = Model_lon), v_era.interp(latitude = Model_lat, longitude = Model_lon)

