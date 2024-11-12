
import pandas
from typing import Iterable
from numpy import int64
from plotnine import ggplot, aes, geom_line, guides, guide_legend
from dataclasses import dataclass

@dataclass
class BatData():
    cycle: pandas.DataFrame
    detail: pandas.DataFrame
    statis: pandas.DataFrame
    filename: str = None
    activatemass: float = 1.0

    def set_activate(self, activateMass: float):
        self.activatemass = activateMass
        self.cycle['CCapacity'] = self.cycle['CCapacity'] / self.activatemass
        self.cycle['DCapacity'] = self.cycle['DCapacity'] / self.activatemass
        self.detail['Capacity'] = self.detail['Capacity'] / self.activatemass
        self.statis['Capacity'] = self.statis['Capacity'] / self.activatemass

        self.detail['Current'] = self.detail['Current'] / self.activatemass
        self.statis['AvgmCurrent'] = (self.statis['StartCurrent'] + self.statis['EndCurrent']) / 2 / self.activatemass
        
    def drop_cycle(self, cycle: int):
        self.cycle.drop(cycle, inplace=True)
        self.detail.drop(self.detail[self.detail['Cycle'] == cycle].index, inplace=True)
        self.statis.drop(self.statis[self.statis['Cycle'] == cycle].index, inplace=True)
        
    def plot_cv(self, cycno: Iterable[int]) -> ggplot:
        _df = self.detail.where(self.detail['Step'].isin(self.statis['Step'][self.statis['Cycle'].isin(cycno) & (self.statis['Status'] != '搁置')]))
        
        _df.dropna(inplace=True)
        
        _df['cycle'] = _df['Cycle'].dropna().astype(int64).astype(str).str.rjust(7, ' ')
        return (ggplot(_df, aes(x='Capacity', y='Voltage', group='Step')) 
                + geom_line(aes(color='cycle'), alpha=0.5, show_legend=True)
                + guides(color=guide_legend())
                )