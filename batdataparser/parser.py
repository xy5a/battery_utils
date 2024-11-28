from batdataparser import BatData
from pandas import read_excel


def nw_parse_from_xls(path: str) -> BatData:
    df = read_excel(path, sheet_name=None)

    for i, v in df.items():
        if "Cycle" in i:
            dfc = v.rename(
                columns={
                    "循环序号": "Cycle",
                    "通道": "Channel",
                    "放电容量(mAh)": "DCapacity",
                    "充电容量(mAh)": "CCapacity",
                    "容量保持率(%)": "CapacityRetention",
                }
            ).set_index("Cycle")

        elif "Statis" in i:
            dfs = v.rename(
                columns={
                    "循环": "Cycle",
                    "通道": "Channel",
                    "步次": "Step",
                    "原始步次": "OriginalStep",
                    "状态": "Status",                    "容量(mAh)": "Capacity",

                    "起始电压(V)": "StartVoltage",
                    "结束电压(V)": "EndVoltage",
                    "起始电流(mA)": "StartCurrent",
                    "结束电流(mA)": "EndCurrent",
                }
            ).set_index("Cycle")

        elif "Detail" in i:
            dfd = v.rename(
                columns={
                    "记录序号": "Record",
                    "状态": "Status",
                    "跳转": "Jump",
                    "循环": "Cycle",
                    "步次": "Step",
                    "电流(mA)": "Current",
                    "电压(V)": "Voltage",
                    "容量(mAh)": "Capacity",
                    "能量(mWh)": "Energy",
                    "相对时间(h:min:s.ms)": "RelativeTime",
                    "绝对时间(h:min:s.ms)": "AbsoluteTime",
                }
            ).set_index('Step')

    return BatData(dfc, dfd, dfs, path)
