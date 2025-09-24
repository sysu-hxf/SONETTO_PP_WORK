from utilities import *
from IObasic import Model_lat, Model_lon

def profilePLOT(figtype, target_value, tfield1, tfield2, ghfield3, ghfield4):
    
    if figtype == 'meridional':
       # 经向剖面图  
       lon_target   = target_value                    # set the target 
       lon_delta    = np.abs(Model_lon-lon_target)    # Δlon
       loc          = np.where(lon_delta == np.min(lon_delta))

       print(f'当前选取的垂直剖面经度是：{Model_lon[loc[0][0]].values}°E')

       t_dif  = np.array(tfield1[:,:,loc[0][0]]) - np.array(tfield2[:,:,loc[0][0]])
       gh_dif = np.array(ghfield3[:,:,loc[0][0]]) - np.array(ghfield4[:,:,loc[0][0]])
       fig = plt.figure(figsize=[8,10])
       ax1 = fig.add_subplot(111)
       cf1 = ax1.contourf(Model_lat,levels, t_dif, 
                    cmap='bwr',levels = [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6])
       CS1 = ax1.contour(Model_lat,levels, gh_dif,colors = 'black')
       ax1.clabel(CS1, inline=True, fontsize=12)
       ax1.invert_yaxis()
       ax1.set_xlabel('Latitude')
       ax1.set_ylabel('Log Pres')
       ax1.set_yticks(levels)
       ax1.set_yscale('log')                                                                              # 对数气压坐标
       plt.colorbar(cf1, ax=ax1)
    elif figtype == 'zonal':
         #纬向剖面图
         lat_target = target_value
         lat_delta  = np.abs(Model_lat-lat_target)
         loc        = np.where(lat_delta == np.min(lat_delta))
         print(f'当前选取的垂直剖面纬度是：{Model_lat[loc[0][0]].values}°E')
         t_dif  = np.array(tfield1[:,loc[0][0],:]) - np.array(tfield2[:,loc[0][0],:])
         gh_dif = np.array(ghfield3[:,loc[0][0],:]) - np.array(ghfield4[:,loc[0][0],:])

         fig = plt.figure(figsize=[8,10])
         ax1 = fig.add_subplot(111)
         cf1 = ax1.contourf(Model_lon,levels, t_dif, 
                    cmap='bwr',levels = [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6])
         CS1 = ax1.contour(Model_lon,levels, gh_dif,colors = 'black',levels = 5)
         ax1.clabel(CS1, inline=True, fontsize=12)
         ax1.invert_yaxis()
         ax1.set_xlabel('Longtitude')
         #ax1.set_ylabel('Log Pres')
         ax1.set_yticks(levels)
         #ax1.set_yscale('log')                                                                           # 对数气压坐标
         plt.colorbar(cf1, ax=ax1)         
    plt.savefig(outpath + figtype + '_' + str(target_value) + '.png', bbox_inches='tight')

