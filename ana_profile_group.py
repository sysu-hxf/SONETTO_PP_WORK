from utilities import *
from IObasic import Model_lat, Model_lon
import matplotlib as mpl
from matplotlib.gridspec import GridSpec

def profilePLOT(target_lon, target_lat, tfield1, tfield2, ghfield3, ghfield4):
    cmap_t = mpl.colormaps['seismic']  
    cmap_gh = mpl.colormaps['PRGn']
    
    fig = plt.figure(figsize=(14, 12), dpi=300)
    gs = GridSpec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1], 
                  hspace=0.25, wspace=0.2)
    
    # 计算经向剖面数据
    lon_delta = np.abs(Model_lon - target_lon)
    loc_lon = np.where(lon_delta == np.min(lon_delta))[0][0]
    lon_value = float(Model_lon[loc_lon].values)
    print(f'当前选取的垂直剖面经度是：{lon_value:.2f}°E')
    
    # 计算纬向剖面数据
    lat_delta = np.abs(Model_lat - target_lat)
    loc_lat = np.where(lat_delta == np.min(lat_delta))[0][0]
    lat_value = float(Model_lat[loc_lat].values)
    print(f'当前选取的垂直剖面纬度是：{lat_value:.2f}°N')
    
    # 计算差异
    t_dif_meridional = np.array(tfield1[:, :, loc_lon]) - np.array(tfield2[:, :, loc_lon])
    gh_dif_meridional = np.array(ghfield3[:, :, loc_lon]) -np.array(ghfield4[:, :, loc_lon])
    
    t_dif_zonal =np.array(tfield1[:, loc_lat, :]) -np.array( tfield2[:, loc_lat, :])
    gh_dif_zonal = np.array(ghfield3[:, loc_lat, :]) -np.array( ghfield4[:, loc_lat, :])
    
    # 创建子图
    ax1 = fig.add_subplot(gs[0, 0])  # 经向温度差异
    ax2 = fig.add_subplot(gs[0, 1])  # 经向高度差异
    ax3 = fig.add_subplot(gs[1, 0])  # 纬向温度差异
    ax4 = fig.add_subplot(gs[1, 1])  # 纬向高度差异
    
    # 经向温度差异图
    vmin_t, vmax_t = -10, 10
    mesh1 = ax1.pcolormesh(Model_lat, np.log(levels), t_dif_meridional, 
                          cmap=cmap_t, vmin=vmin_t, vmax=vmax_t)
    ax1.set_title(f'meridional profile {lon_value:.2f}°E', fontsize=10)
    ax1.set_xlabel('Latitude')
    ax1.set_ylabel('Log Pressure')
    ax1.invert_yaxis()
    
    # 经向高度差异图
    vmin_h, vmax_h = -15, 15
    mesh2 = ax2.pcolormesh(Model_lat, np.log(levels), gh_dif_meridional, 
                          cmap=cmap_gh,vmin=vmin_h, vmax=vmax_h)
    ax2.set_title(f'meridional profile {lon_value:.2f}°E', fontsize=10)
    ax2.set_xlabel('Latitude')
    ax2.invert_yaxis()
    
    # 纬向温度差异图
    mesh3 = ax3.pcolormesh(Model_lon, np.log(levels), t_dif_zonal, 
                          cmap=cmap_t,vmin=vmin_t, vmax=vmax_t)
    ax3.set_title(f'zonal profile {lat_value:.2f}°N', fontsize=10)
    ax3.set_xlabel('Longitude')
    ax3.set_ylabel('Log Pressure')
    ax3.invert_yaxis()
    
    # 纬向高度差异图
    mesh4 = ax4.pcolormesh(Model_lon, np.log(levels), gh_dif_zonal, 
                          cmap=cmap_gh,vmin=vmin_h, vmax=vmax_h)
    ax4.set_title(f'zonal profile {lat_value:.2f}°N', fontsize=10)
    ax4.set_xlabel('Longitude')
    ax4.invert_yaxis()
    
    # 添加共享的colorbar
    cbar_ax_t = fig.add_axes([0.15, 0.05, 0.3, 0.02])  # [left, bottom, width, height]
    cbar_t = fig.colorbar(mesh1, cax=cbar_ax_t, orientation='horizontal')
    cbar_t.set_label('Temperature Difference (K)', fontsize=9)
    
    cbar_ax_gh = fig.add_axes([0.57, 0.05, 0.3, 0.02])
    cbar_gh = fig.colorbar(mesh2, cax=cbar_ax_gh, orientation='horizontal')
    cbar_gh.set_label('Geopotential Height Difference (10 gpm)', fontsize=9)
    
    # 设置共享的y轴刻度
    log_levels = np.log(levels)
    yticks = np.linspace(log_levels.min(), log_levels.max(), 7)
    ytick_labels = [f"{np.exp(y):.0f}" for y in yticks]
    
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_yticks(yticks)
        ax.set_yticklabels(ytick_labels)
    
    # 设置字体
    font_props = {
        'family': 'Times New Roman',
        'size': 12,
        'weight': 'bold',
        'color': 'black'
    }
    
    for ax in [ax1, ax2, ax3, ax4]:
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + 
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontname(font_props['family'])
            item.set_fontsize(font_props['size'])
            item.set_color(font_props['color'])
    
    plt.savefig(outpath + f'combined_profile_{target_lon}_{target_lat}.png', 
               bbox_inches='tight', dpi=300)
    plt.close()