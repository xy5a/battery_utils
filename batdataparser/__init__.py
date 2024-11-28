import pandas
from typing import List
from math import floor, log10
from plotnine import (
    ggplot,
    aes,
    geom_line,
    guides,
    guide_legend,
    geom_point,
    geom_text,
    theme,
)
from dataclasses import dataclass


@dataclass
class BatData:
    cycle: pandas.DataFrame
    detail: pandas.DataFrame
    statis: pandas.DataFrame
    filename: str = ""
    activatemass: float = 1.0

    def set_activate(self, activateMass: float):
        self.activatemass = activateMass
        self.cycle["CCapacity"] = self.cycle["CCapacity"] / self.activatemass
        self.cycle["DCapacity"] = self.cycle["DCapacity"] / self.activatemass
        self.detail["Capacity"] = self.detail["Capacity"] / self.activatemass
        self.statis["Capacity"] = self.statis["Capacity"] / self.activatemass

        self.detail["Current"] = self.detail["Current"] / self.activatemass
        self.statis["AvgmCurrent"] = (
            (self.statis["StartCurrent"] + self.statis["EndCurrent"])
            / 2
            / self.activatemass
        )

    def drop_cycle(self, cycle: int):
        self.cycle.drop(cycle, inplace=True)
        self.detail.drop(self.detail[self.detail["Cycle"] == cycle].index, inplace=True)
        self.statis.drop(self.statis[self.statis["Cycle"] == cycle].index, inplace=True)

    def plot_cv(self, cycle: List[int]) -> ggplot:

        _i = self.statis["Step"][self.statis["Status"] != "搁置"].loc[cycle]

        _df = self.detail.loc[_i].reset_index()

        _df["cycle"] = _df["Cycle"].apply(lambda x: f"${x:7d}$")

        return (
            ggplot(_df, aes(x="Capacity", y="Voltage", group="Step"))
            + geom_line(aes(color="cycle"), alpha=0.5, show_legend=True)
            + guides(color=guide_legend())
        )

    def plot_rate(self) -> ggplot:

        self.statis["CRate"] = (
            self.statis["AvgmCurrent"] / self.statis["Capacity"].max()
        )

        self.statis["CRate"] = (
            self.statis["CRate"]
            .fillna(0)
            .apply(
                lambda x: f"${0 if x == 0 else round(abs(x), -floor(log10(abs(x))) + 1):10.1f}C$"
            )
        )

        dc = self.statis[self.statis["Status"] == "恒流放电"].copy()
        dc["cycle"] = range(dc.shape[0])
        tagd = dc[["CRate", "Capacity", "cycle"]].copy()
        tagd["g"] = (tagd["CRate"] != tagd["CRate"].shift()).cumsum()
        tagd = (
            tagd.groupby("g")
            .agg({"CRate": "first", "Capacity": "mean", "cycle": "median"})
            .reset_index(drop=True)
        )

        return (
            ggplot()
            + geom_point(
                data=dc,
                mapping=aes(y="Capacity", x=range(dc.shape[0]), color=dc["CRate"]),
                show_legend=False,
            )
            + geom_text(
                data=tagd,
                mapping=aes(label="CRate", x="cycle", y="Capacity"),
                adjust_text={
                    "expand": (0.1, 2),
                    "arrowprops": {"arrowstyle": "-", "color": "red"},
                },
            )
            + guides()
            + theme(figure_size=(10, 5))
        )
