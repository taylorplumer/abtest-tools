import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import pandas as pd
from min_sample_size import min_sample_size
from create_row import create_row
from scipy import stats
from helpers import create_curve, create_plot


test_data_elements = ['Visitors A', 'Conversions A', 'Visitors B', 'Conversions B']

app = dash.Dash()

header_ =     html.Div(
                 className="app-header",
                 children=[
                     html.Div('AB Test Results Significance Calculator', className="app-header--title")
                 ]
             )


test_type = html.Div([
                html.P('Test Type'),
                dcc.RadioItems(id= 'test-type-radio',
                    options=[
                        {'label': 'One-sided', 'value': 'One-sided'},
                        {'label': 'Two-sided', 'value': 'Two-sided'}
                    ],
                    value = 'One-sided',
                    labelStyle={'display': 'inline-blickk'}
                    )
])

confidence_level = html.Div([
                html.P('Test Type'),
                dcc.RadioItems(id= 'confidence-level-radio',
                    options = [
                        {'label': '90%', 'value': 0.90},
                        {'label': '95%', 'value': 0.95},
                        {'label': '99%', 'value': 0.99}
                    ],
                    value = 'One-sided',
                    labelStyle={'display': 'inline-blickk'}
                    )
])


app.layout= html.Div([
            header_,
             html.P(children='Is your test result signficant? Input your test data below.'),
             html.Div([
                 create_row(element) for element in test_data_elements
                 ]),
            html.Button('Submit', id='submit-button'),
            html.Div([
                test_type,
                confidence_level
            ]),
            html.Div([
                dcc.Graph(id = 'results-graph')
            ])
             ])


@app.callback(Output('results-graph', 'figure'),
                [Input('submit-button', 'n_clicks')],
                [State(element, 'value') for element in test_data_elements])

def update_results(n_clicks, control_visitors, control_conversions, treatment_visitors, treatment_conversions):
    control_mu = int(control_conversions)/int(control_visitors)
    control_x, control_y, control_sd = create_curve(mu=int(control_conversions)/int(control_visitors), visitors=int(control_visitors))
    treatment_x, treatment_y, treatment_sd = create_curve(mu=int(treatment_conversions)/int(treatment_visitors), visitors=int(treatment_visitors))

    figure = create_plot(control_x, control_y, treatment_x, treatment_y, control_mu, control_sd)

    return figure

if __name__ == '__main__':
 app.run_server()
