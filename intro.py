# basic imports 
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

# dash-specific imports 
import dash
import dash_core_components as dcc # unlocks the UI components provided by Dash
import dash_html_components as html # Python-ized HTML/CSS/Javascript components
from dash.dependencies import Input, Output # utilized for callbacks

app = dash.Dash(__name__) # initialize the app through Dash
server = app.server

# data import and cleaning
df = pd.read_csv('intro_bees.csv') # path to the file, can be something else if in other folder/path. Could be SQL/whatever

# include only this data, perform a mean as the grouping function
# this could be point by which to adjust data aggregation ***

df = df.groupby(['State', 'ANSI', 'Affected by', "Year", "state_code"])[['Pct of Colonies Impacted']].mean() 
df.reset_index(inplace=True) # realign data
# print(df[:5]) # demonstrate that the data is in the desired format

# ------------------------------------------------------------------------------------------------
# App layout - this includes components, charts, and any other HTML elements

# the html.Div function creates a div container where elements are included as components in a list
app.layout = html.Div([

    # produce an h1 HTML element where arg1 is the text and arg2 is a key/value pair styling
    html.H1("Percent of Bee Colonies Affected by Various Factors", style={'text-align':'center'}),

    # create a Dropdown component from Dash's core components library where each argument corresponds with attributes
    dcc.Dropdown(id="slct_year",
                options=[
                    {"label":"2015","value": 2015},  # value needs to match the corresponding data (in this case, filter by year means the value needs to match the year)
                    {"label":"2016","value": 2016},
                    {"label":"2017","value": 2017},
                    {"label":"2018","value": 2018}], # list is the set of k,v pairs of labels and values for the dropdown box
                    multi=False, # disable multiple choice
                    value=2015,  # default value
                    style={'width':'40%'} # css styling
                    ),

    dcc.Dropdown(id="afft_by",
                options=[
                    {"label":"Disease","value": "Disease"},  
                    {"label":"Other","value": "Other"},
                    {"label":"Pesticides","value": "Pesticides"},
                    {"label":"Pests excluding Varroa","value": "Pests_excl_Varroa"},
                    {"label":"Varroa Mites","value": "Varroa_mites"}], 
                    multi=True, # disable multiple choice
                    value=["Disease","Other","Pesticides","Pests_excl_Varroa","Varroa_mites"],  # default value
                    style={'width':'40%'} # css styling
                    ),

    html.Div(id='output_container', children=[]), # set an empty list to store the children objects into later
    html.Br(), # html break

    dcc.Graph(id='my_bee_map', figure={}) # set an empty figure for the graph to be populated later

])

# ------------------------------------------------------------------------------------------------
# Callback functions to connect the Dash Components to the Plotly graphs

@app.callback(
    # output components -- locations where data will be rendered from the callback
    [Output(component_id="output_container", component_property="children"), # component id matches the id prop, property matches the type of prop on the component
     Output(component_id='my_bee_map', component_property="figure")], 

    # input components -- the interactive UI components that'll send values to the callback
    [Input(component_id='slct_year', component_property='value'), 
     Input(component_id='afft_by', component_property='value')] # works the same as output, but for interactive components
) # the callback takes in a list that identifies the inputs and outputs within the application


# callback functions
def update_graph(year_selected, affected_selected):
    """takes in the option selected from the dropdown component and updates the graph to reflect the data. 
    Needed to add the """
    print(year_selected) # ensure the value is being passed down properly
    print(type(year_selected)) # print type of value; ensure filtering errors are not occurring because of mismatched types


    container = f"The year chosen was: {year_selected}" # this is just to alert the user of the selected date

    dff = df.copy() # make a copy of the dataframe to perform filtering on
    dff = dff[dff['Year'] == year_selected] # filter the new df to only include the selected year

    filtered_df = dff['Affected by'].isin(affected_selected)

    dff = dff[filtered_df] 

    # Ploty Express (PX)
    fig = px.choropleth(
        data_frame=dff, # use the new dataframe
        locationmode='USA-states', # the map used
        locations='state_code', # the data that will be used to plot on the map 
        scope="usa", 
        color='Pct of Colonies Impacted', # the value to assign a color scale to
        hover_data=['State', 'Pct of Colonies Impacted'], # the data to appear on hover
        color_continuous_scale=px.colors.sequential.YlOrRd, # color scale to use
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'}
    )

    
    return container, fig # this return is getting passed into the Output. Because there are two outputs, there will be two objects that get returned

# ------------------------------------------------------------------------------------------------
# main function run

if __name__ == '__main__':
    app.run_server(debug=True)