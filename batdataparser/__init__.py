import pandas
from typing import List
from numpy import int64
from plotnine import ggplot, aes, geom_line, guides, guide_legend
from dataclasses import dataclass

@dataclass
class BatData():
    cycle: pandas.DataFrame
    detail: pandas.DataFrame
    statis: pandas.DataFrame
    filename: str = ''
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
        
    def plot_cv(self, cycle: List[int]) -> ggplot:
        
        _i = self.statis['Step'][self.statis['Status'] != '搁置'].loc[cycle]

        _df = self.detail.loc[_i].reset_index()

        _df['cycle'] = _df['Cycle'].astype(str).str.rjust(7, ' ').str.center(9, '$')

        return (ggplot(_df, aes(x='Capacity', y='Voltage', group='Step')) 
                + geom_line(aes(color='cycle'), alpha=0.5, show_legend=True)
                + guides(color=guide_legend())
                )