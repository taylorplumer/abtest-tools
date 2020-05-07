import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import pandas as pd
from min_sample_size import min_sample_size
from create_row import create_row
from scipy import stats
from helpers import create_curve, create_plot, calculate_pvalue
from app import create_form
from scipy import stats, special


test_data_keys = ['Visitors A', 'Conversions A', 'Visitors B', 'Conversions B']
default_values = [100000, 3000, 100000, 3800]
default_dict = dict(zip(test_data_keys, default_values))

app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])


navbar = dbc.NavbarSimple(
    brand="AB Test Results Significance Calculator",
    brand_href="#",
    color="primary",
    dark=True
)
form = create_form(default_dict)
test_type = dbc.Container(html.Div([
                html.P('Test Type'),
                dbc.RadioItems(id= 'test-type-radio',
                    options=[
                        {'label': 'One-sided', 'value': 'One-sided'},
                        {'label': 'Two-sided', 'value': 'Two-sided'}
                    ],
                    value = 'One-sided',
                    labelStyle={'display': 'inline-blickk'}
                    )
]))

confidence_level = dbc.Container(html.Div([
                html.P('Confidence Level'),
                dbc.RadioItems(id= 'confidence-level-radio',
                    options = [
                        {'label': '90%', 'value': 0.90},
                        {'label': '95%', 'value': 0.95},
                        {'label': '99%', 'value': 0.99}
                    ],
                    value = 0.95,
                    labelStyle={'display': 'inline-blickk'}
                    )
]))

output_text = dbc.Container(html.H2(id='results-text', children="The Results are..."))
output_graph = dbc.Container(dcc.Graph(id = 'results-graph'))

app.layout = html.Div([navbar,
                        form,
                        test_type,
                        confidence_level,
                        output_text,
                        output_graph
                    ])

@app.callback([Output('results-graph', 'figure'), Output('results-text', 'children')],
                [Input('submit-button', 'n_clicks'), Input('confidence-level-radio', 'value')],
                [State(element, 'value') for element in test_data_keys])

def update_results(n_clicks, confidence_, control_visitors, control_conversions, treatment_visitors, treatment_conversions):
    control_mu = float(control_conversions)/float(control_visitors)
    treatment_mu = float(treatment_conversions)/float(treatment_visitors)
    difference_mu = abs(float(control_mu - treatment_mu))
    control_x, control_y, control_sd = create_curve(mu=float(control_conversions)/float(control_visitors), visitors=int(control_visitors))
    treatment_x, treatment_y, treatment_sd = create_curve(mu=float(treatment_conversions)/float(treatment_visitors), visitors=int(treatment_visitors))

    figure = create_plot(control_x, control_y, treatment_x, treatment_y, control_mu, control_sd)

    def create_resulting_text(control_mu, treatment_mu, difference_mu):
        if treatment_mu > control_mu:
            winning_variation = 'Variation B'
            relative_uplift = (treatment_mu/control_mu) - 1
            text_1 = "Variation B's observed conversion rate ({}) was {} higher than Variation A's conversion rate ({})."\
            .format(str(round(treatment_mu*100, 2))+'%', str(round(relative_uplift*100, 2)) + '%', str(round(control_mu*100, 2))+'%')
        elif control_mu > treatment_mu:
            winning_variation = 'Variation A'
            relative_uplift = (control_mu/treatment_mu) - 1
            text_1 = "Variation A's observed conversion rate ({}) was {} higher than Variation B's conversion rate ({})."\
            .format(str(round(control_mu*100, 2))+'%',str(round(relative_uplift*100, 2)) + '%', str(round(treatment_mu*100, 2))+'%')

        z_score = difference_mu/np.sqrt(treatment_sd**2 + control_sd**2)
        p_value = 1- special.ndtr(z_score)

        if p_value < (1-confidence_):
            text_2 = "You can be {} confident that {} has a higher conversion rate.".format(str((float(confidence_) * 100))+'%', winning_variation)
        else:
            text_2 = " The difference however isn't sufficient, so you cannot be confident that this result is a consequence of the treatment."

        return text_1, text_2

    text_1, text_2 = create_resulting_text(control_mu, treatment_mu, difference_mu)
    text= text_1 + text_2


    return figure, text

if __name__ == '__main__':
 app.run_server()
