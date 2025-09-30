# 导入所需的模块

import sys
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import metpy.calc as mpcalc
from metpy.units import units
import warnings
warnings.filterwarnings('ignore')
font = {'color'  : 'black',
        'weight' : 'normal',
        'size'   : '6',
        'family':'Times New Roman'}
# 这里使用的postvar和ERA5数据都是17个垂直层级
levels = [1000.,  925.,  850.,  700.,  600.,  500.,  400.,  300.,  250.,  200.,
  150.,  100.,   70.,   50.,   30.,   20.,   10.]

# 设置剖面分析的中心经纬度
LATC = 16.6
LONC = 126.34 
# 设置数据文件路径
file_era5 = 'D:/yangliu/data/ERA.nc'                      # ERA5数据文件路径
file_ECM = 'D:/yangliu/data/CMA_GD_ECM/postvar000.nc'
file_GGF = 'D:/yangliu/data/CMA_GD_GGF/postvar000.nc'     # CMA_GD_GGF      postvar000.nc
file_GGFMT = 'D:/yangliu/data/CMA_GD_GGF_MT/postvar000.nc'# CMA_GD_GGF_MT   postvar000.nc

# 保存路径
outpath = 'D:/yangliu/yangliu/PP/figs/'


