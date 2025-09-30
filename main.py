from IObasic import *
from ana_profile_group import profilePLOT
from ana_profile import profilePLOTsi
from ana_weather import weather_ana
from ana_base import create_fig
from tqdm import tqdm
import time

if __name__ == "__main__":
    start = time.time()
    pbar = tqdm(total=100, desc="progress", unit="task")
    
    # #单点剖面差异
    #profilePLOTsi('meridional', LONC, t_GGFMT, t_era5_INTE, gh_GGFMT, gh_era5_INTE)
    #profilePLOTsi('zonal', LATC, t_GGFMT, t_era5_INTE, gh_GGFMT, gh_era5_INTE)
    #pbar.update(2)
    # #全域剖面组
    while LATC<=max(Model_lat) and LONC>=min(Model_lon):
        profilePLOT(LONC, LATC, t_GGFMT, t_ECM, gh_GGFMT, gh_ECM)
        pbar.update(1)
        LATC = LATC + 1
        LONC = LONC - 1
    print(LATC,LONC)
    # #天气形势
    for lv, name in [(5, "500hPa"), (2, "850hPa")]:
       for src in ['era5_INTE', 'ECM', 'GGF', 'GGFMT']:
    # for lv, name in [(5,"500hpa")]:    
    #     for src in ['ECM','GGF', 'GGFMT']:
    #         print(src+'\n')
            data = locals()[f't_{src}'], locals()[f'u_{src}'], locals()[f'v_{src}'], locals()[f'gh_{src}']
            weather_ana(src, *data, lv)
            pbar.update(1)
    # #基本要素场
            for plot_type in ['twind', 'ghwind','vo']:
                create_fig(src, plot_type, *data, lv)
                pbar.update(1)

    pbar.close()
    print(f"总用时: {time.time()-start:.2f}秒")