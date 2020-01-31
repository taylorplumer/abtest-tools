import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import pandas as pd
from min_sample_size import min_sample_size
import scipy.stats as scs

elements = ['baseline_conversion_rate', 'effect_size', 'power', 'sig_level']

def create_row(element):
    row = html.Div([
            html.Div([
            html.P(element)], className="six columns", style = {'width': '48%', 'display': 'inline-block'}),
            html.Div([
            dcc.Input(id=element,
                            placeholder='Enter {}...'.format(element),
                            type='number')], className="six columns", style = {'width': '48%', 'display': 'inline-block'})
            ], className="row", style = {'border-style': 'solid', 'border-width': '.5px'})

    return row


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
                    create_row(element) for element in elements
                    ]),
                    html.H2(id='min_sample_size-output', children="Minimum Sample Size is ....")
                ])


@app.callback(Output('min_sample_size-output','children'),
                [Input(element, 'value') for element in elements])

def update_output(baseline_conversion_rate,effect_size,power,sig_level):
    min_N = round(min_sample_size(float(baseline_conversion_rate),float(effect_size),float(power),float(sig_level)),0)
    return 'Minimum sample size is "{}"'.format(min_N)

if __name__ == '__main__':
    app.run_server()
