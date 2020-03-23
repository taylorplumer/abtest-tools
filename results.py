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
from helpers import create_curve, create_plot, calculate_pvalue


test_data_keys = ['Visitors A', 'Conversions A', 'Visitors B', 'Conversions B']
default_values = [100000, 3000, 100000, 3200]
default_dict = dict(zip(test_data_keys, default_values))
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
                html.P('Confidence Level'),
                dcc.RadioItems(id= 'confidence-level-radio',
                    options = [
                        {'label': '90%', 'value': 0.90},
                        {'label': '95%', 'value': 0.95},
                        {'label': '99%', 'value': 0.99}
                    ],
                    value = 0.95,
                    labelStyle={'display': 'inline-blickk'}
                    )
])


app.layout= html.Div([
            header_,
             dcc.Markdown('''
             **Are your test results significant?** Input your test data below.
             '''),
             html.Div([
                 create_row(key,value) for key, value in default_dict.items()
                 ]),
            html.Button('Submit', id='submit-button'),
            html.Div([
                test_type,
                confidence_level
            ]),
            html.Div([
                html.H2(id='results-text', children="The Results are...")
            ]),
            html.Div([
                dcc.Graph(id = 'results-graph')
            ])
             ])


@app.callback([Output('results-graph', 'figure'), Output('results-text', 'children')],
                [Input('submit-button', 'n_clicks'), Input('confidence-level-radio', 'value')],
                [State(element, 'value') for element in test_data_keys])

def update_results(n_clicks, confidence_, control_visitors, control_conversions, treatment_visitors, treatment_conversions):
    control_mu = int(control_conversions)/int(control_visitors)
    treatment_mu = int(treatment_conversions)/int(treatment_visitors)
    control_x, control_y, control_sd = create_curve(mu=int(control_conversions)/int(control_visitors), visitors=int(control_visitors))
    treatment_x, treatment_y, treatment_sd = create_curve(mu=int(treatment_conversions)/int(treatment_visitors), visitors=int(treatment_visitors))

    figure = create_plot(control_x, control_y, treatment_x, treatment_y, control_mu, control_sd)

    if treatment_mu > control_mu:
        winning_variation = 'Variation B'
        relative_uplift = (treatment_mu/control_mu) - 1
        difference_mu = treatment_mu - control_mu
        text_1 = "Variation B's observed conversion rate ({}) was {} higher than Variation A's conversion rate ({}).".format(str(treatment_mu*100)+'%', str(round(relative_uplift*100, 2)) + '%', str(control_mu*100)+'%')
    elif control_mu > treatment_mu:
        winning_variation = 'Variation A'
        elative_uplift = (control_mu/treatment_mu) - 1
        difference_mu = control_mu - treatment_mu
        text_1 = "Variation A's observed conversion rate ({}) was {} higher than Variation B's conversion rate ({}).".format(str(control_mu*100)+'%',str(round(relative_uplift*100, 2)) + '%', str(treatment_mu*100)+'%')


    p_value = calculate_pvalue(difference_mu, control_sd, treatment_sd)

    if p_value < (1-confidence_):
        text_2 = "You can be {} confident that {} has a higher conversion rate.".format(confidence_, winning_variation)
    else:
        text_2 = " The difference however isn't sufficicient, so you cannot be confident that this result is a consequence of the treatment."

    text = text_1 + text_2

    return figure, text

if __name__ == '__main__':
 app.run_server()
