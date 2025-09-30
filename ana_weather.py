from utilities import *
from ana_base import preprocess, map_initial
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

def weather_ana(title, t, u, v, h, lv=5):
    lon, lat, t, u, v, h = preprocess(t, u, v, h, lv)
    fig = plt.figure(figsize=[10, 6], dpi=300)
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    map_initial(ax1)
    
    # 计算网格间距（假设经纬度网格是均匀的）
    lon_spacing = np.mean(np.diff(lon))
    lat_spacing = np.mean(np.diff(lat))
    
    # 寻找多个极值点并确保最小距离
    def find_extrema(data, mode='max', num_points=3, min_distance=5):
        """
        寻找多个极值点并确保最小距离
        :param data: 二维数据数组
        :param mode: 'max' 或 'min'
        :param num_points: 要寻找的点数
        :param min_distance: 最小距离（经纬度网格数）
        :return: 极值点坐标列表
        """
        points = []
        data_temp = data.copy()  # 使用副本避免修改原始数据
        
        for _ in range(num_points):
            if mode == 'max':
                idx = np.unravel_index(np.argmax(data_temp), data_temp.shape)
            else:  # min
                idx = np.unravel_index(np.argmin(data_temp), data_temp.shape)
                
            points.append(idx)
            
            # 创建排除区域（确保最小距离）
            i, j = idx
            # 计算排除区域的边界（基于网格数）
            i_min = max(0, int(i - min_distance/lat_spacing))
            i_max = min(data_temp.shape[0], int(i + min_distance/lat_spacing) + 1)
            j_min = max(0, int(j - min_distance/lon_spacing))
            j_max = min(data_temp.shape[1], int(j + min_distance/lon_spacing) + 1)
            
            # 将排除区域设置为极端值（确保不会被再次选中）
            if mode == 'max':
                data_temp[i_min:i_max, j_min:j_max] = np.min(data_temp)
            else:
                data_temp[i_min:i_max, j_min:j_max] = np.max(data_temp)
                
        return points
    
    # 高压中心（H） - 寻找3个最大值点，最小距离5个经纬度网格
    high_points = find_extrema(h, mode='max', num_points=3, min_distance=5)
    
    for idx in high_points:
        max_lon, max_lat = lon[idx[1]], lat[idx[0]]
        # print("高压中心\n")
        # print(max_lon.values, max_lat.values)
        # print(h[idx])
        ax1.text(max_lon, max_lat, 'H', fontsize=8, fontfamily='Times New Roman',
                 ha='center', va='center', transform=ccrs.PlateCarree(),
                 color='green', fontweight='bold')  # 绿色粗体
    
    # 低压中心（L） - 寻找3个最小值点，最小距离5个经纬度网格
    low_points = find_extrema(h, mode='min', num_points=3, min_distance=5)
            
    for idx in low_points:
        min_lon, min_lat = lon[idx[1]], lat[idx[0]]
        # print("低压中心")
        # print(min_lon.values, min_lat.values)
        # print(h[idx])
        ax1.text(min_lon, min_lat, 'L', fontsize=8, fontfamily='Times New Roman',
                 ha='center', va='center', transform=ccrs.PlateCarree(),
                 color='purple', fontweight='bold')  # 紫色粗体
    
    # 暖中心（W） - 寻找3个最大值点，最小距离5个经纬度网格
    warm_points = find_extrema(t, mode='max', num_points=3, min_distance=5)
    
    for idx in warm_points:
        warm_lon, warm_lat = lon[idx[1]], lat[idx[0]]
        ax1.text(warm_lon, warm_lat, 'W', fontsize=8, fontfamily='Times New Roman',
                 ha='center', va='center', transform=ccrs.PlateCarree(),
                 color='red', fontweight='bold')  # 红色粗体
    
    # 冷中心（C） - 寻找3个最小值点，最小距离5个经纬度网格
    cold_points = find_extrema(t, mode='min', num_points=3, min_distance=5)
    
    for idx in cold_points:
        cold_lon, cold_lat = lon[idx[1]], lat[idx[0]]
        ax1.text(cold_lon, cold_lat, 'C', fontsize=8, fontfamily='Times New Roman',
                 ha='center', va='center', transform=ccrs.PlateCarree(),
                 color='blue', fontweight='bold')  # 蓝色粗体

    # 位势高度填色底图
    if lv == 5:
        clevels = np.arange(555, 595, 1)
    elif lv == 2:
        clevels = np.arange(120, 160, 1)
    else:
        clevels = np.arange(np.floor(np.min(h)), np.ceil(np.max(h)), 1)
    
    contour = ax1.contourf(lon, lat, h, transform=ccrs.PlateCarree(),
                           cmap='terrain', levels=clevels,extend = 'both')
    
    # 流场
    ax1.streamplot(lon, lat, u, v, linewidth=.6, color='k',
                   arrowsize=0.6, arrowstyle='fancy',
                   minlength=0.2, density=4, transform=ccrs.PlateCarree())
    
    cbar = plt.colorbar(contour)
    cbar.set_ticks(clevels[::2])
    
    # 风羽图
    skip = 30  # 稀疏化
    ax1.barbs(lon[::skip], lat[::skip], 
              u[::skip, ::skip], v[::skip, ::skip],
              length=4, pivot='middle', barbcolor='grey',
              transform=ccrs.PlateCarree())
        
    plt.title(f'data:{title}\nlevel = {str(levels[lv]).strip()}', fontdict=font, loc='left')
    plt.savefig(outpath + title + '_weather_' + str(levels[lv]).strip() + 'hPa.png', bbox_inches='tight')