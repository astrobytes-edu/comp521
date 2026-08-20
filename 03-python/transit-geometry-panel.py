import panel as pn
from bokeh.plotting import figure

pn.extension(sizing_mode="stretch_width")
radius_ratio = pn.widgets.FloatSlider(name="Planet/star radius ratio, p", start=0.02, end=0.50, step=0.01, value=0.10)

def metrics(p):
    depth = p**2
    return pn.Column(pn.pane.Markdown(f"### Blocked fraction\n## {depth:.3f}"), pn.pane.Markdown(f"Normalized flux F = 1 − p² = {1-depth:.3f}. Doubling p multiplies the blocked fraction by four."))

def depth_plot(p):
    values = [i / 100 for i in range(2, 51)]
    plot = figure(height=300, x_range=(0, 0.5), y_range=(0, 0.26), x_axis_label="radius ratio p", y_axis_label="blocked fraction p²", title="Uniform-source transit model", toolbar_location="above")
    plot.line(values, [value**2 for value in values], line_width=3, color="#195c8f")
    plot.scatter([p], [p**2], size=10, color="#e57200")
    return plot

app = pn.Column("## Predict → change → explain", "Predict whether the orange point moves linearly or quadratically before moving the slider.", radius_ratio, pn.Row(pn.bind(metrics, radius_ratio), pn.bind(depth_plot, radius_ratio)))
