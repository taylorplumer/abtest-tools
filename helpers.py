import plotly.graph_objs as go
import numpy as np
import math
from scipy import stats, special

def create_curve(mu=.02,visitors=100_000):
    sd = np.sqrt( mu * ( 1 - mu ) / visitors)
    x = np.linspace(mu - 4*sd,mu + 4*sd, visitors)
    y = stats.norm.pdf(x,mu,sd)
    return x, y, sd


def create_plot(control_x, control_y, treatment_x, treatment_y, mu, sd):
    control_trace = go.Scatter(x = control_x,y = control_y)
    treatment_trace = go.Scatter(x = treatment_x,y = treatment_y)

    fig = go.Figure(data=[control_trace, treatment_trace])

    #fig.update_layout(xaxis = dict(range=(mu - (6*(sd)), mu + (6*(sd)))))
    return fig

def calculate_pvalue(relative_uplift, control_sd, treatment_sd):
    z_score = relative_uplift/np.sqrt(treatment_sd**2 + control_sd**2)
    p_value = 1- special.ndtr(z_score)
    return p_value
