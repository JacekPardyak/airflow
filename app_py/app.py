from shiny import App, render, ui, reactive
import pandas as pd
from plotnine import ggplot, geom_density, aes, theme_light, geom_point, stat_smooth
from pathlib import Path

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("mass", "Mass", 2000, 8000, 6000),
            ui.input_checkbox("smoother", "Add Smoother"),
        ),
        ui.panel_main(
            ui.output_plot(id="scatter"),
            ui.output_plot(id="mass_distribution"),
        ),
    )
)


def server(input, output, session):
    infile = Path(__file__).parent / "penguins.csv"
    df = pd.read_csv(infile)

    @reactive.Calc
    def filtered_data():
        filt_df = df.copy()
        filt_df = filt_df.loc[df["Body Mass (g)"] < input.mass()]
        return filt_df

    @output
    @render.plot
    def mass_distribution():
        return dist_plot(filtered_data())

    @output
    @render.plot
    def scatter():
        return scatter_plot(filtered_data(), input.smoother())


def dist_plot(df):
    plot = (
        ggplot(df, aes(x="Body Mass (g)", fill="Species"))
        + geom_density(alpha=0.2)
        + theme_light()
    )
    return plot


def scatter_plot(df, smoother):
    plot = (
        ggplot(
            df,
            aes(
                x="Bill Length (mm)",
                y="Bill Depth (mm)",
                color="Species",
                group="Species",
            ),
        )
        + geom_point()
        + theme_light()
    )

    if smoother:
        plot = plot + stat_smooth()

    return plot


app = App(app_ui, server)
