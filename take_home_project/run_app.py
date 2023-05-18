import pandas as pd
from dash import Dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output, State
from take_home_project.get_data import get_data
from take_home_project.components.temperature import temperature_div
from take_home_project.components.pH import pH_div
from take_home_project.components.distilled_O2 import distilledO2_div
from take_home_project.components.pressure import pressure_div


def main():
    #getting the data
    df_temp, df_pH, df_O2, df_pressure = get_data()

    #create mappings for row_index_number : timestamp value, this is to create a range-slider for each of the graphs
    # The range slider does not accept timestamp-values given in the df['values'] column

    #mappings for temperature dataframe
    # creating a list of number of rows
    numdate1 = [x for x in range(len(df_temp['time']))]
    # creating a dictionary to map row_number to corresponding timestamp
    numdate1_to_df = {numd:date for numd,date in zip(numdate1, df_temp['time'])}

    #mappings for pH dataframe
    # creating a list of number of rows
    numdate2 = [x for x in range(len(df_pH['time']))]
    # creating a dictionary to map row_number to corresponding timestamp
    numdate2_to_df = {numd:date for numd,date in zip(numdate2, df_pH['time'])}

    #mappings for Distilled O2 dataframe
    # creating a list of number of rows
    numdate3 = [x for x in range(len(df_O2['time']))]
    # creating a dictionary to map row_number to corresponding timestamp
    numdate3_to_df = {numd:date for numd,date in zip(numdate3, df_O2['time'])}

    #mappings for Pressure dataframe
    # creating a list of number of rows
    numdate4 = [x for x in range(len(df_pressure['time']))]
    # creating a dictionary to map row_number to corresponding timestamp
    numdate4_to_df = {numd:date for numd,date in zip(numdate4, df_pressure['time'])}

    # creating dash app
    app = Dash(__name__)
    app.title = "Ark Biotech"
    

    app.layout = html.Div(children = [
                                        html.H1(
                                                children = "Ark Biotech Dashboard", 
                                                className="main-heading"),
                                        
                                        #Temperature div
                                        temperature_div(df_temp),

                                        # pH div
                                        pH_div(df_pH),
                                        
                                        # Ditilled O2
                                        distilledO2_div(df_O2),
                                        
                                        # Pressure Div
                                        pressure_div(df_pressure)
                                    
                                    ],
                                    className="main-div"
                        )
    
    
    # Updating Graphs
    @app.callback(
        [Output('Temp-graph', 'figure'),
        Output('PH-graph', 'figure'),
        Output('O2-graph', 'figure'),
        Output('Pressure-graph', 'figure')],

        [Input('Temp-slider', 'value'),
        Input('PH-slider', 'value'),
        Input('O2-slider', 'value'),
        Input('Pressure-slider', 'value')]
    )

    def update_graph(temp_time, ph_time, O2_time, pressure_time):
        # Filter the data based on the slider values
        filtered_df_temp = df_temp[(df_temp['time'] >= numdate1_to_df[temp_time[0]]) & (df_temp['time'] <= numdate1_to_df[temp_time[1]])]
        filtered_df_ph = df_pH[(df_pH['time'] >= numdate2_to_df[ph_time[0]]) & (df_pH['time'] <= numdate2_to_df[ph_time[1]])]
        filtered_df_O2 = df_O2[(df_O2['time'] >= numdate3_to_df[O2_time[0]]) & (df_O2['time'] <= numdate3_to_df[O2_time[1]])]
        filtered_df_pressure = df_pressure[(df_pressure['time'] >= numdate4_to_df[pressure_time[0]]) & (df_pressure['time'] <= numdate4_to_df[pressure_time[1]])]

        # Create figure for Temperature vs Time graph
        fig1 = px.line(filtered_df_temp, x='time', y='value')
        # Updating figure layout
        fig1.update_layout({
                'plot_bgcolor': 'rgb(176,211,209)',
                'paper_bgcolor': 'rgb(176,211,209)',
                'font_color': 'rgb(0,85,111)',
                'font_family': 'Arial, sans-serif',
                'yaxis_title':'Celsius',
                'font_size':16
            })
        fig1.update_traces(line_color='#00556f')

        # Create figure for PH vs Time graph
        fig2 = px.line(filtered_df_ph, x='time', y='value')
        fig2.update_layout({
                            'plot_bgcolor': 'rgb(176,211,209)',
                            'paper_bgcolor': 'rgb(176,211,209)',
                            'font_color': 'rgb(0,85,111)',
                            'font_family': 'Arial, sans-serif',
                            'font_size':16
            })
        fig2.update_traces(line_color='#00556f')

        # Create figure for O2 vs Time graph
        fig3 = px.line(filtered_df_O2, x='time', y='value')
        fig3.update_layout({
                            'plot_bgcolor': 'rgb(176,211,209)',
                            'paper_bgcolor': 'rgb(176,211,209)',
                            'font_color': 'rgb(0,85,111)',
                            'font_family': 'Arial, sans-serif',
                            'yaxis_title':'Percentage %',
                            'font_size':16
                        })
        fig3.update_traces(line_color='#00556f')

        # Create figure for Pressure vs Time graph
        fig4 = px.line(filtered_df_pressure, x='time', y='value')
        fig4.update_layout({
                            'plot_bgcolor': 'rgb(176,211,209)',
                            'paper_bgcolor': 'rgb(176,211,209)',
                            'font_color': 'rgb(0,85,111)',
                            'font_family': 'Arial, sans-serif',
                            'yaxis_title':'psi',
                            'font_size':16
            })
        fig4.update_traces(line_color='#00556f')

        # Return all the figures as output
        return fig1,fig2,fig3,fig4



    # Download Button for Temperature Graph
    @app.callback(
        Output("download-dataframe-csv-temp", "data"),
        [Input("btn_csv_temp", "n_clicks")],
        [State('Temp-slider', 'value')],
        prevent_initial_call=True
    )
    def update_btn_temp(n_clicks_temp, temp_time):
        # Filter the DataFrame based on the selected time range
        filtered_df_temp = df_temp[(df_temp['time'] >= numdate1_to_df[temp_time[0]]) & (df_temp['time'] <= numdate1_to_df[temp_time[1]])]
        filtered_df_temp = filtered_df_temp[['time','value']]
        # create a CSV file of the filtered temperature dataset
        temp_csv = dcc.send_data_frame(filtered_df_temp.to_csv, "temperature.csv")
        # Return the CSV data for download
        return temp_csv
    
    # Download Button for PH Graph
    @app.callback(
        Output("download-dataframe-csv-pH", "data"),
        [Input("btn_csv_pH", "n_clicks")],
        [State('PH-slider', 'value')],
        prevent_initial_call=True
    )

    def update_btn_pH(n_clicks_pH, ph_time):
        # Filter the DataFrame based on the selected time range
        filtered_df_ph = df_pH[(df_pH['time'] >= numdate2_to_df[ph_time[0]]) & (df_pH['time'] <= numdate2_to_df[ph_time[1]])]
        filtered_df_pf = filtered_df_pf[['time','value']]
        # create a CSV file of the filtered pH dataset
        ph_csv = dcc.send_data_frame(filtered_df_ph.to_csv, "pH.csv")
        # return the CSV file for download
        return ph_csv

    # Download Button for Distilled O2 Graph
    @app.callback(
        Output("download-dataframe-csv-O2", "data"),
        [Input("btn_csv_O2", "n_clicks")],
        [State('O2-slider', 'value')],
        prevent_initial_call=True
    )
    def update_btn_O2(n_clicks_O2, O2_time):
        # Filter the DataFrame based on the selected time range
        filtered_df_O2 = df_O2[(df_O2['time'] >= numdate3_to_df[O2_time[0]]) & (df_O2['time'] <= numdate3_to_df[O2_time[1]])]
        filtered_df_O2 = filtered_df_O2[['time','value']]
        # create a CSV file of the filtered O2 dataset
        O2_csv = dcc.send_data_frame(filtered_df_O2.to_csv, "distilled_O2.csv")
        # return the CSV file for download
        return O2_csv

    # Download Button for Pressure Graph
    @app.callback(
        Output("download-dataframe-csv-pressure", "data"),
        [Input("btn_csv_pressure", "n_clicks")],
        [State('Pressure-slider', 'value')],
        prevent_initial_call=True
    )

    def update_btn_pressure(n_clicks_pressure,pressure_time):
        # Filter the DataFrame based on the selected time range
        filtered_df_pressure = df_pressure[(df_pressure['time'] >= numdate4_to_df[pressure_time[0]]) & (df_pressure['time'] <= numdate4_to_df[pressure_time[1]])]
        filtered_df_pressure = filtered_df_pressure[['time','value']]
        # create a CSV file of the filtered O2 dataset
        pressure_csv = dcc.send_data_frame(filtered_df_pressure.to_csv, "pressure.csv")
        # return the CSV file for download
        return pressure_csv

    # run server
    app.run_server("0.0.0.0", 8888, debug=True)



if __name__ == "__main__":
    main()