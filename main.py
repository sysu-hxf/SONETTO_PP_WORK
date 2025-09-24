from IObasic import *
from ana_profile import profilePLOT
from ana_weather import weather_ana
from ana_base import create_fig
from tqdm import tqdm  
import time

if __name__ == "__main__":
    time_start = time.time()
    # 定义总任务数 
    total_tasks = 22  # 2 (profilePLOT) + 8 (weather_ana) + 12 (create_fig) = 22
    # 初始化进度条
    pbar = tqdm(total=total_tasks, desc="总体进度", unit="task")

    # 剖面分析
    profilePLOT('meridional', LONC, t_GGFMT, t_era5_INTE, gh_GGFMT, gh_era5_INTE)
    pbar.update(1)  # 更新进度条
    pbar.set_postfix_str("已完成经向剖面分析")
    profilePLOT('zonal', LATC, t_GGFMT, t_era5_INTE, gh_GGFMT, gh_era5_INTE)
    pbar.update(1)
    pbar.set_postfix_str("已完成纬向剖面分析")

    # 天气形势分析 - 500hpa
    weather_ana('ERA5', t_era5_INTE, u_era5_INTE, v_era5_INTE, gh_era5_INTE, lv=5)
    pbar.update(1)
    weather_ana('ECM', t_ECM, u_ECM, v_ECM, gh_ECM, lv=5)
    pbar.update(1)
    weather_ana('GGF', t_GGF, u_GGF, v_GGF, gh_GGF, lv=5)
    pbar.update(1)
    weather_ana('GGFMT', t_GGFMT, u_GGFMT, v_GGFMT, gh_GGFMT, lv=5)
    pbar.update(1)
    pbar.set_postfix_str("已完成500hPa天气形势分析")

    # 天气形势分析 - 850hpa
    weather_ana('ERA5', t_era5_INTE, u_era5_INTE, v_era5_INTE, gh_era5_INTE, lv=2)
    pbar.update(1)
    weather_ana('ECM', t_ECM, u_ECM, v_ECM, gh_ECM, lv=2)
    pbar.update(1)
    weather_ana('GGF', t_GGF, u_GGF, v_GGF, gh_GGF, lv=2)
    pbar.update(1)
    weather_ana('GGFMT', t_GGFMT, u_GGFMT, v_GGFMT, gh_GGFMT, lv=2)
    pbar.update(1)
    pbar.set_postfix_str("已完成850hPa天气形势分析")

    # 基本分析图 - 地面场 twind
    create_fig('ERA5','twind', t_era5_INTE, u_era5_INTE, v_era5_INTE, gh_era5_INTE,lv=0)
    pbar.update(1)
    create_fig('ECM','twind', t_ECM, u_ECM, v_ECM, gh_ECM,lv=0)
    pbar.update(1)
    create_fig('GGF','twind', t_GGF, u_GGF, v_GGF, gh_GGF,lv=0)
    pbar.update(1)
    create_fig('GGFMT','twind', t_GGFMT, u_GGFMT, v_GGFMT, gh_GGFMT,lv=0)
    pbar.update(1)

    # 基本分析图 - 地面场 ghwind
    create_fig('ERA5','ghwind', t_era5_INTE, u_era5_INTE, v_era5_INTE, gh_era5_INTE,lv=0)
    pbar.update(1)
    create_fig('ECM','ghwind', t_ECM, u_ECM, v_ECM, gh_ECM,lv=0)
    pbar.update(1)
    create_fig('GGF','ghwind', t_GGF, u_GGF, v_GGF, gh_GGF,lv=0)
    pbar.update(1)
    create_fig('GGFMT','ghwind', t_GGFMT, u_GGFMT, v_GGFMT, gh_GGFMT,lv=0)
    pbar.update(1)
    pbar.set_postfix_str("已完成地面场分析")

    # 基本分析图 - 200hpa twind
    create_fig('ERA5','twind', t_era5_INTE, u_era5_INTE, v_era5_INTE, gh_era5_INTE,lv=9)
    pbar.update(1)
    create_fig('ECM','twind', t_ECM, u_ECM, v_ECM, gh_ECM,lv=9)
    pbar.update(1)
    create_fig('GGF','twind', t_GGF, u_GGF, v_GGF, gh_GGF,lv=9)
    pbar.update(1)
    create_fig('GGFMT','twind', t_GGFMT, u_GGFMT, v_GGFMT, gh_GGFMT,lv=9)
    pbar.update(1)

    # 基本分析图 - 200hpa ghwind
    create_fig('ERA5','ghwind', t_era5_INTE, u_era5_INTE, v_era5_INTE, gh_era5_INTE,lv=9)
    pbar.update(1)
    create_fig('ECM','ghwind', t_ECM, u_ECM, v_ECM, gh_ECM,lv=9)
    pbar.update(1)
    create_fig('GGF','ghwind', t_GGF, u_GGF, v_GGF, gh_GGF,lv=9)
    pbar.update(1)
    create_fig('GGFMT','ghwind', t_GGFMT, u_GGFMT, v_GGFMT, gh_GGFMT,lv=9)
    pbar.update(1)
    pbar.set_postfix_str("已完成200hPa分析")

    # 关闭进度条
    pbar.close()
    time_end = time.time()
    print(f"总用时: {time_end - time_start:.2f} 秒")
    print("所有分析完成！")