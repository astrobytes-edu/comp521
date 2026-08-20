import panel as pn
from bokeh.plotting import figure

pn.extension(sizing_mode="stretch_width")
radius_ratio = pn.widgets.FloatSlider(name="Planet/star radius ratio, p", start=0.02, end=0.50, step=0.01, value=0.10)

def summary(p):
    depth = p**2
    return pn.Row(
        pn.Column("### Blocked fraction", f"## {depth:.3f}", width=175),
        pn.Column("### Normalized flux", f"## {1 - depth:.3f}", width=175),
        pn.Column(
            "### What this means",
            "The blocked fraction is an **area ratio**, so it follows p². "
            "Doubling p makes the depth four times larger.",
            sizing_mode="stretch_width",
        ),
        sizing_mode="stretch_width",
    )

def depth_plot(p):
    values = [i / 100 for i in range(2, 51)]
    plot = figure(height=300, x_range=(0, 0.5), y_range=(0, 0.26), x_axis_label="radius ratio p", y_axis_label="blocked fraction p²", title="Uniform-source transit model", toolbar_location="above")
    plot.line(values, [value**2 for value in values], line_width=3, color="#195c8f")
    plot.scatter([p], [p**2], size=10, color="#e57200")
    return plot

app = pn.Column(
    "## Predict → change → explain",
    "Before moving the slider, predict whether the orange point follows a line or a curve.",
    radius_ratio,
    pn.bind(summary, radius_ratio),
    pn.bind(depth_plot, radius_ratio),
    sizing_mode="stretch_width",
)
