import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import pandas as pd
from min_sample_size import min_sample_size
from create_row import create_row
import scipy.stats as scs

variables = ['baseline_conversion_rate', 'effect_size', 'power', 'sig_level']
default_values = [0.20, 0.05, 0.80, 0.05]
default_dict = dict(zip(variables, default_values))

app = dash.Dash()

header_ =     html.Div(
                    className="app-header",
                    children=[
                        html.Div('Minimum Sample Size Calculator', className="app-header--title")
                    ]
                )

app.layout= html.Div([
                header_,
                html.Div([
                    create_row(variable, value) for variable, value in default_dict.items()
                    ]),
                    html.H2(id='min_sample_size-output', children="Minimum Sample Size is ....")
                ])


@app.callback(Output('min_sample_size-output','children'),
                [Input(variable, 'value') for variable in variables])

def update_output(baseline_conversion_rate,effect_size,power,sig_level):
    min_N = round(min_sample_size(float(baseline_conversion_rate),float(effect_size),float(power),float(sig_level)),0)
    return 'Minimum sample size is "{}"'.format(min_N)

if __name__ == '__main__':
    app.run_server()
