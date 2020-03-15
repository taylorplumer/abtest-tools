import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

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
