# 这个模块提供分析高度层信息、初始化地图、矢量风场绘制， 提取分析域（限制经纬度范围，温度K -> ℃以便作图）的基本函数供其它analyse_*.py模块调用
# 这个模块还包含：针对postvar数据的温度+风场 位势高度风场 水汽水平散度场 的绘制工具

from utilities import *
from IObasic import Model_lat, Model_lon
def levU(lv):
    if lv == 2:
        lvl = ' 850hpa '
        U_flag = 15
        U_flaglabel = '15m/s'
    elif lv == 5:
        lvl = ' 500hpa'
        U_flag = 25
        U_flaglabel = '25m/s'
    elif lv == 9:
        lvl = ' 200hpa '
        U_flag = 35
        U_flaglabel = '35m/s'
    elif lv == 0:
        lvl = 'Surface'     
        U_flag = 10
        U_flaglabel = '10m/s'
    else:
        print('Error: lv should be 0,2,5,9')
        sys.exit()
    return lvl, U_flag, U_flaglabel

def map_initial(ax): # 初始化子图地图：经纬度范围、海岸线、边界、省界、网格线、网格标签
    ax.set_extent([105, 126.3, 16.6, 40], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.2)
    ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.2)
    province_borders = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        edgecolor='grey',
        facecolor='none'
    )
    ax.add_feature(province_borders, linewidth=0.3, edgecolor='gray', alpha=0.8)

    gl = ax.gridlines(
        draw_labels=True,
        linewidth=0.5,
        color='grey',
        alpha=0.5,
    )
    gl.top_labels, gl.bottom_labels, gl.right_labels, gl.left_labels = False, True, False, True
    gl.xlabel_style = {'size': 3}
    gl.ylabel_style = {'size': 3}

def windquiver(ax,lon,lat,uvar,vvar, U_flag, U_flaglabel,scale = 450, stride = 20):
    # 间隔stride: 每相隔20个矢量箭头作图
    # scale: 箭头缩放比例
    q = ax.quiver(
    lon[::stride], lat[::stride],
    uvar[::stride, ::stride], vvar[::stride, ::stride],
    color='k',             
    pivot='middle',
    scale = scale,
    transform=ccrs.PlateCarree()
)
    ax.quiverkey(
        q, X=0.85, Y=1.03, U=U_flag,
        label=U_flaglabel, labelpos='E',
        fontproperties={'size': 6}
    )

def preprocess(t,u,v,h,lv):
    t = t[lv] - 273.15  # K to C    
    u = u[lv]
    v = v[lv]   
    h = h[lv]
    lon, lat = Model_lon, Model_lat

    lon_min, lon_max = 105, 126.3
    lat_min, lat_max = 16.6, 40
    lat, lon = Model_lat, Model_lon
    lat_inds = np.where((lat >= lat_min) & (lat <= lat_max))[0]
    lon_inds = np.where((lon >= lon_min) & (lon <= lon_max))[0]
    
    t = t.values[lat_inds, :][:, lon_inds]  
    u = u.values[lat_inds, :][:, lon_inds]
    v = v.values[lat_inds, :][:, lon_inds]
    h = h.values[lat_inds, :][:, lon_inds]
    
    lat = lat[lat_inds]
    lon = lon[lon_inds]
    return lon, lat, t, u, v, h

def plot_tempwind(title,t,u,v,lon,lat,lvl,U_flag,U_flaglabel):
    fig = plt.figure(figsize=[5,5],dpi=300)
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    map_initial(ax)
    clevels = np.arange(np.floor(np.min(t)),np.ceil(np.max(t)),1)
    contour = ax.contourf(lon,lat, t,transform=ccrs.PlateCarree(),cmap = 'bwr',levels = clevels) 
    windquiver(ax,lon,lat,u,v, U_flag, U_flaglabel)
    cb = fig.colorbar(contour)
    cb.ax.tick_params(labelsize=6)
    cb.set_label('Temperature (℃)',fontdict=font)
    ax.set_title(lvl +" Temperature-Wind Field\n"+title,loc = 'left',fontdict=font)
    plt.savefig(outpath + title + '_twind_' + lvl.strip() + '.png')

def plot_ghwind(title,h,u,v,lon,lat,lvl,U_flag,U_flaglabel):
    fig = plt.figure(figsize=[5,5],dpi=300)
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    map_initial(ax)
    clevels = np.arange(np.floor(np.min(h)),np.ceil(np.max(h)),1)
    contour = ax.contourf(lon,lat, h,transform=ccrs.PlateCarree(),cmap = 'viridis',levels = clevels) 
    # 绘制位势高度场等值线
    cbar = ax.contour(lon, lat, h, colors='crimson', linewidths=0.7, levels=clevels, transform=ccrs.PlateCarree())
    plt.clabel(cbar, levels=clevels, inline=True, fmt='%d', fontsize=4, colors='crimson')
    windquiver(ax,lon,lat,u,v, U_flag, U_flaglabel)

    cb = fig.colorbar(contour)
    cb.ax.tick_params(labelsize=6)
    cb.set_label('Geopotential Height (10 gpm)',fontdict=font)
    ax.set_title(lvl +" Geopotential Height-Wind Field\n"+title,loc = 'left',fontdict=font)
    plt.savefig(outpath + title + '_ghwind_' + lvl.strip() + '.png')

def create_fig(title,figtype,t,u,v,gh,lv):

    lvl, U_flag, U_flaglabel = levU(lv)
    lon, lat, t, u, v, h = preprocess(t,u,v,gh,lv)

    if figtype == 'twind': # 温度+风场
        plot_tempwind(title,t,u,v,lon,lat,lvl,U_flag,U_flaglabel)
    elif figtype == 'ghwind': # 位势高度+风场
        plot_ghwind(title,h,u,v,lon,lat,lvl,U_flag,U_flaglabel)