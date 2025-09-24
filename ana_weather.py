from utilities import *
from ana_base import preprocess, map_initial

def weather_ana(title, t,u,v,h,lv = 5):
    lon, lat, t, u, v, h = preprocess(t, u, v, h, lv)
    fig = plt.figure(figsize=[10,6],dpi=300)
    ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
    map_initial(ax1)
      
    # 高压中心（H） - 位势高度最大值点
    max_idx = np.unravel_index(np.argmax(h), h.shape)
    max_lon, max_lat = lon[max_idx[1]], lat[max_idx[0]]
    ax1.text(max_lon, max_lat, 'H', fontsize=10, weight='bold', 
            ha='center', va='center', transform=ccrs.PlateCarree(),
            bbox=dict(facecolor='white', alpha=0.4, boxstyle='round'))
    
    # 低压中心（L） - 位势高度最小值点
    min_idx = np.unravel_index(np.argmin(h), h.shape)
    min_lon, min_lat = lon[min_idx[1]], lat[min_idx[0]]
    ax1.text(min_lon, min_lat, 'L', fontsize=10, weight='bold', 
            ha='center', va='center', transform=ccrs.PlateCarree(),
            bbox=dict(facecolor='white', alpha=0.4, boxstyle='round'))
    
    # 暖中心（W） - 温度最大值点
    warm_idx = np.unravel_index(np.argmax(t), t.shape)
    warm_lon, warm_lat = lon[warm_idx[1]], lat[warm_idx[0]]
    ax1.text(warm_lon, warm_lat, 'W', fontsize=10, weight='bold', 
            ha='center', va='center', transform=ccrs.PlateCarree(),
            bbox=dict(facecolor='white', alpha=0.4, boxstyle='round'))
    
    # 冷中心（C） - 温度最小值点
    cold_idx = np.unravel_index(np.argmin(t), t.shape)
    cold_lon, cold_lat = lon[cold_idx[1]], lat[cold_idx[0]]
    ax1.text(cold_lon, cold_lat, 'C', fontsize=10, weight='bold', 
            ha='center', va='center', transform=ccrs.PlateCarree(),
            bbox=dict(facecolor='white', alpha=0.4, boxstyle='round'))

    # 温度填色底图
    clevels = np.arange(np.floor(np.min(t)),np.ceil(np.max(t)),1)
    contour = ax1.contourf(lon,lat, t,transform=ccrs.PlateCarree()
                        ,cmap = 'bwr',levels = clevels)

    # 流场   
    ax1.streamplot(lon, lat, u, v, linewidth=.6, color='k',
                   arrowsize = 0.6,
                   arrowstyle = 'fancy',
                   minlength = 0.2,
                   density=4,transform=ccrs.PlateCarree())  
    cbar = plt.colorbar(contour)
    cbar.set_ticks(clevels)

    # 风羽图
    skip = 30  # 稀疏化       
    ax1.barbs(lon[::skip], lat[::skip], 
              u[::skip,::skip], v[::skip,::skip],
         length=4, pivot='middle', barbcolor = 'grey',
         transform=ccrs.PlateCarree())
        
    plt.title(f'data:{title}\nlevel = {str(levels[lv]).strip()}',fontdict=font,loc = 'left')
    plt.savefig(outpath + title + '_weather_' + str(levels[lv]).strip() + 'hPa.png', bbox_inches='tight')