from batdataparser import BatData
from plotnine import ggplot, aes, geom_line, guides, guide_legend


def geom_cv(data: BatData, cycle: list):

    _i = data.statis["Step"][data.statis["Status"] != "搁置"].loc[cycle]

    _df = data.detail.loc[_i].reset_index()

    _df["cycle"] = _df["Cycle"].apply(lambda x: f"${x:7d}$")

    return (
        # aes(_df, aes(x="Capacity", y="Voltage", group="Step"))
        geom_line(
            aes(x="Capacity", y="Voltage", group="Step", color="cycle"),
            data=_df,
            alpha=0.5,
            show_legend=True,
        )
    )
