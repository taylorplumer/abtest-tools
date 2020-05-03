import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
import pandas as pd
from min_sample_size import min_sample_size
import scipy.stats as scs

variables = ['conversion_rate', 'effect_size', 'power', 'sig_level']
default_values = [0.20, 0.05, 0.80, 0.05]
default_dict = dict(zip(variables, default_values))

app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

navbar = dbc.NavbarSimple(
    brand="Minimum Sample Size Calculator",
    brand_href="#",
    color="primary",
    dark=True
)


def create_form(default_dict):
    form_dict = {}
    for element, value_ in default_dict.items():
        form_dict[element] = dbc.FormGroup(
                                    [
                                        dbc.Label(element, html_for= "example-{}-row".format(element), width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="number",
                                                id="{}".format(element),
                                                placeholder="Enter number of votes",
                                                value = value_
                                            ),
                                            width=10,
                                        ),
                                    ],
                                    row=True,
                                )

    form_dict['button'] = dbc.Button("Submit", color="primary", size='lg', block=True)

    form = dbc.Container(dbc.Form(list(form_dict.values())))

    return form


button = dbc.Button("Submit", color="primary", size='lg', block=True)

form = create_form(default_dict)

output_ = dbc.Container(html.H1(id="min_sample_size-output"))

app.layout = html.Div([navbar, form, output_])

@app.callback(Output('min_sample_size-output','children'),
                [Input(variable, 'value') for variable in variables])

def update_output(baseline_conversion_rate,effect_size,power,sig_level):
    min_N = int(round(min_sample_size(float(baseline_conversion_rate),float(effect_size),float(power),float(sig_level)),0))
    return 'Minimum sample size is "{}"'.format(min_N)

if __name__ == '__main__':
    app.run_server()
