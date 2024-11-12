
import pandas
from typing import Iterable
from numpy import int64
from plotnine import ggplot, aes, geom_line, guides, guide_legend


class BatData():
    def __init__(self, filename, channel: str, activateMass: float = 1.0):
        self.filename = filename

        _cycle = pandas.read_excel(filename, sheet_name=f"Cycle_{channel}")
        
        _cycle['capc'] = _cycle['充电容量(mAh)'] / activateMass
        
        _cycle['capo'] = _cycle['放电容量(mAh)'] / activateMass

        _statis = pandas.read_excel(filename, sheet_name=f"Statis_{channel}")
        _statis['capc'] = _statis['充电容量(mAh)'] / activateMass
        
        _statis['capo'] = _statis['放电容量(mAh)'] / activateMass
        
        _detail = pandas.read_excel(filename, sheet_name=f"Detail_{channel}")
        
        _detail['cap'] = _detail['容量(mAh)'] / activateMass
        
        self.cycle: pandas.DataFrame = _cycle
        self.statis: pandas.DataFrame = _statis
        self.detail: pandas.DataFrame = _detail
        self.activateMass = activateMass
        self.channel = channel
        
    def drop_cycle(self, cycleno: int):
        self.cycle.drop(self.cycle[self.cycle['循环序号'] == cycleno].index, inplace=True)
        
        self.detail.drop(self.detail[self.detail['循环'] == cycleno].index, inplace=True)
        
        self.statis.drop(self.statis[self.statis['循环'] == cycleno].index, inplace=True)
        
    def plot_cv(self, cycno: Iterable[int]) -> ggplot:
        _df = self.detail.where(self.detail['步次'].isin(self.statis['步次'][self.statis['循环'].isin(cycno) & (self.statis['状态'] != '搁置')]))
        
        _df.dropna(inplace=True)
        
        _df['cycle'] = _df['循环'].dropna().astype(int64).astype(str).str.rjust(7, ' ')
        return (ggplot(_df, aes(x='cap', y='电压(V)', group='步次')) 
                + geom_line(aes(color='cycle'), alpha=0.5, show_legend=True)
                + guides(color=guide_legend())
                )