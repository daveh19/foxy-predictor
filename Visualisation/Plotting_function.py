import plotly
plotly.tools.set_credentials_file(username='zandermoore1994', api_key='dund3fgcUIRA82LX6JxJ')
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import scipy as sp
import plotly as py
import pandas
plotly.offline.init_notebook_mode()
import plotly.offline as offline
import jinja2
from plotly import tools

def plot_graphs(data_new):
    CDUstr="CDU/CSU"
    SPDstr="SPD"
    GRÜNEstr="GRÜNE"
    LINKEstr='LINKE'
    FDPstr='FDP'
    AfDstr='AfD'
    parties=[CDUstr,SPDstr,GRÜNEstr,LINKEstr,AfDstr]
    total=np.sum(data_new[parties].iloc[0])
    base_chart = { "values": [40, 10, 10, 10, 10, 10, 10], "domain": {"x": [0, .48]},
                   "marker": {"colors": ['rgb(255, 255, 255)','rgb(255, 255, 255)','rgb(255, 255, 255)',
                                         'rgb(255, 255, 255)','rgb(255, 255, 255)','rgb(255, 255, 255)',
                                         'rgb(255, 255, 255)'],"line": {"width": 0}}, "name": "Predictor",
                   "hole": .4,"type": "pie","direction": "clockwise", "rotation": 180, "showlegend": False,
                   "hoverinfo": "none", "textinfo": "none", "textposition": "outside"}
    meter_chart = {"values": [total, data_new[CDUstr][0], data_new[SPDstr][0], data_new[GRÜNEstr][0],
                              data_new[AfDstr][0],data_new[LINKEstr][0]],
                   "labels": [" ", "CDU/CSU", "SPD", "Green", "AFD", "Die Linke"],
                   "marker": {'colors': ['rgb(255, 255, 255)','rgb(0,0,0)','rgb(165,0,38)','rgb(154,205,50)',
                                         'rgb(0,204,255)','rgb(153,102,255)']},
                   "domain": {"x": [0, 0.48]},"name": "% Representation","hole": .3, "type": "pie",
                   "direction": "clockwise", "rotation": 90,
                   "showlegend": False, "textinfo": "label", "textposition": "outside", "hoverinfo": "none"}

    fig_1 = {"data": [base_chart, meter_chart],}
    #offline.plot(fig_1 , output_type='file', filename='SeatChart',image='png')


    timeline= data_new.index[::-1]
    CDU_data=data_new[CDUstr][::-1]
    SPD_data=data_new[SPDstr][::-1]
    Green_data=data_new[GRÜNEstr][::-1]
    Linke_data=data_new[LINKEstr][::-1]
    AFD_data=data_new[AfDstr][::-1]
    FDP_data=data_new[FDPstr][::-1]


    upper_bound_CDU = go.Scatter(
        name='Upper Bound CDU',
        x=timeline,
        y=CDU_data+0.05,
        mode='lines',
        marker=dict(color="444"),
        line=dict(width=0),
        opacity=0.25,
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='none',
        showlegend=False)


    CDU = go.Scatter(
      x=timeline,
      y=CDU_data,
      name="CDU",
      line=dict(color='rgb(0,0,0)'),
      opacity=0.8,
      )

    lower_bound_CDU = go.Scatter(
      name='Lower Bound CDU',
      x=timeline,
      y=CDU_data-0.05,
      marker=dict(color="444"),
      line=dict(width=0),
      mode='lines',
      opacity=0.25,
      fill='tonextx',
      showlegend=False
      )


    SPD = go.Scatter(
      x=timeline,
      y=SPD_data,
      name = "SPD",
      line = dict(color = 'rgb(165,0,38)'),
      opacity = 0.8,
      )

    upper_bound_SPD = go.Scatter(
      name='Upper Bound SPD',
      x=timeline,
      y=SPD_data+0.05,
      mode='lines',
      marker=dict(color='rgb(165,0,38)'),
      line=dict(width=0),
      opacity=0.25,
      fill='none',
      showlegend=False)

    lower_bound_SPD = go.Scatter(
      name='Lower Bound SPD',
      x=timeline,
      y=SPD_data-0.05,
      marker=dict(color='rgb(165,0,38)'),
      line=dict(width=0),
      mode='lines',
      opacity=0.25,
      fill='tonextx',
      showlegend=False
      )

    Gruene = go.Scatter(
        x=timeline,
        y=Green_data,
        name = "Gruene",
        line = dict(color = 'rgb(154,205,50)'),
        opacity = 0.8,
        )

    upper_bound_Gruene = go.Scatter(
        name='Upper Bound Gruene',
        x=timeline,
        y=Green_data+0.005,
        mode='lines',
        marker=dict(color='rgb(154,205,50)'),
        line=dict(width=0),
        opacity=0.1,
        fill='none',
        showlegend=False)

    lower_bound_Gruene = go.Scatter(
        name='Lower Bound Gruene',
        x=timeline,
        y=Green_data-0.005,
        marker=dict(color='rgb(154,205,50)'),
        line=dict(width=0),
        mode='lines',
        opacity=0.1,
        fill='tonextx',
        showlegend=False
        )

    Linke = go.Scatter(
        x=timeline,
        y=Linke_data,
        name = "Linke",
        line = dict(color = 'rgb(0,204,255)'),
        opacity = 0.8,
        )

    upper_bound_Linke = go.Scatter(
        name='Upper Bound Linke',
        x=timeline,
        y=Linke_data+0.005,
        mode='lines',
        marker=dict(color='rgb(0,204,255)'),
        line=dict(width=0),
        opacity=0.1,
        fill='none',
        showlegend=False)

    lower_bound_Linke = go.Scatter(
        name='Lower Bound Linke',
        x=timeline,
        y=Linke_data-0.005,
        marker=dict(color='rgb(0,204,255)'),
        line=dict(width=0),
        mode='lines',
        opacity=0.1,
        fill='tonextx',
        showlegend=False
        )
    FDP = go.Scatter(
        x=timeline,
        y=FDP_data,
        name = "FDP",
        line = dict(color = 'rgb(255,255,0)'),
        opacity = 0.8,
        )

    upper_bound_FDP = go.Scatter(
        name='Upper Bound FDP',
        x=timeline,
        y=FDP_data+0.005,
        mode='lines',
        marker=dict(color='rgb(255,255,0)'),
        line=dict(width=0),
        opacity=0.1,
        fill='none',
        showlegend=False)

    lower_bound_FDP = go.Scatter(
        name='Lower Bound FDP',
        x=timeline,
        y=FDP_data-0.005,
        marker=dict(color='rgb(255,255,0)'),
        line=dict(width=0),
        mode='lines',
        opacity=0.1,
        fill='tonextx',
        showlegend=False
        )

    AFD = go.Scatter(
        x=timeline,
        y=AFD_data,
        name = "AfD",
        line = dict(color = 'rgb(153,102,255)'),
        opacity = 0.8,
        )

    upper_bound_AFD = go.Scatter(
        name='Upper Bound AfD',
        x=timeline,
        y=AFD_data+0.01,
        mode='lines',
        marker=dict(color='rgb(153,102,255)'),
        line=dict(width=0),
        opacity=0.1,
        fill='none',
        showlegend=False)

    lower_bound_AFD = go.Scatter(
        name='Lower Bound AfD',
        x=timeline,
        y=AFD_data-0.01,
        marker=dict(color='rgb(153,102,255)'),
        line=dict(width=0),
        mode='lines',
        opacity=0.1,
        fill='tonextx',
        showlegend=False
        )

    data = [CDU,upper_bound_CDU,lower_bound_CDU,SPD,upper_bound_SPD,lower_bound_SPD]


    layout = dict(
        title='Evolution of Second Vote Prediction',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='timeline'
    )
    )
    fig_5 = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)


    fig_5.append_trace(CDU, 1,1)
    fig_5.append_trace(upper_bound_CDU, 1,1)
    fig_5.append_trace(lower_bound_CDU, 1,1)
    fig_5.append_trace(SPD, 1,1)
    fig_5.append_trace(upper_bound_SPD, 1,1)
    fig_5.append_trace(lower_bound_SPD, 1,1)

    fig_5.append_trace(Gruene, 2,1)
    fig_5.append_trace(upper_bound_Gruene, 2,1)
    fig_5.append_trace(lower_bound_Gruene, 2,1)
    fig_5.append_trace(AFD, 2,1)
    fig_5.append_trace(upper_bound_AFD, 2,1)
    fig_5.append_trace(lower_bound_AFD, 2,1)
    fig_5.append_trace(Linke, 2,1)
    fig_5.append_trace(upper_bound_Linke, 2,1)
    fig_5.append_trace(lower_bound_Linke, 2,1)
    fig_5.append_trace(FDP, 2,1)
    fig_5.append_trace(upper_bound_FDP, 2,1)
    fig_5.append_trace(lower_bound_FDP, 2,1)



    fig_5['layout'].update(title='Evolution of Second Vote Prediction')

    xx=offline.plot(fig_1 ,show_link=False, output_type='div', filename='SeatChart.html',image='None', image_width=80, image_height=60)
    xxx=offline.plot(fig_5 ,show_link=False, output_type='div', filename='TimeEvolution.html',image='None', image_width=80, image_height=60)
    template= jinja2.Template("""
        <!DOCTYPE html>
        <html>
        <head>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
              google.charts.load('current', {
                'packages':['geochart'],
                // Note: you will need to get a mapsApiKey for your project.
                // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
                'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
              });
              google.charts.setOnLoadCallback(drawRegionsMap);

              function drawRegionsMap() {
                var data = google.visualization.arrayToDataTable([
                  ['State', 'Name', 'Party Majority', 'CDU'],
                  ['DE-BW', 'Baden-Württemberg', 1, 40],
                  ['DE-BY', 'Bayern', 4, 40],
                  ['DE-BE', 'Berlin', 6, 31],
                  ['DE-BB', 'Brandenburg', 3, 31],
                  ['DE-HH', 'Hamburg', 3, 31],
                  ['DE-HE', 'Hessen', 1, 31],
                  ['DE-MV', 'Mecklenburg-Vorpommern', 4, 31],
                  ['DE-NI', 'Niedersachsen', 1, 40],
                  ['DE-NW', 'Nordrhein-Westfalen', 6, 31],
                  ['DE-RP', 'Rheinland-Pfalz', 2, 31],
                  ['DE-SL', 'Saarland', 4, 40],
                  ['DE-SN', 'Sachsen', 1, 31],
                  ['DE-ST', 'Sachsen-Anhalt', 3, 40],
                  ['DE-SH', 'Schleswig-Holstein', 5, 31],
                  ['DE-TH', 'Thüringen', 5, 40]
                ]);

                var options = {
                region: 'DE', // Germany
                displayMode: 'regions',
                resolution: 'provinces',
        	colorAxis: {
        		colors: ['rgb(0,0,0)', 'rgb(165,0,38)', 'rgb(154,205,50)','rgb(0,204,255)', 'rgb(153,102,255)', 'rgb(255,255,0)'],
        		values: ['1', '2', '3', '4', '5', '6']
        	},
        	legend: 'none',
            	//datalessRegionColor: '#eeddff'
                };

                var chart = new google.visualization.GeoChart(document.getElementById('geochart-colors'));
                chart.draw(data, options);
              };
        </script>

        <style>
        header, footer {
            padding: 1em;
            color: white;
            background-color: black;
            clear: left;
            text-align: center;
        }

        .flex-container {
            display: -webkit-flex;
            display: flex;
            -webkit-flex-direction: row;
            flex-direction: row;
            -webkit-flex-wrap: wrap;
            flex-wrap: wrap;
            -webkit-align-items: center;
            align-items: center;
            width: 1250px;
            height: 1100px;
            background-color: white;
        }

        .flex-item {
            background-color: white;
            width: 600px;
            height: 350px;
            margin: 0px;
            flex-grow: 0.2
            margin-right: 40px;
            margin-down: 0px;
            border-right: 0px solid gray;
            align-items: stretch;


        }

        header {
            width: 1200px;

        }
        footer {
            width: 1200px;
            bottom: 0;
            font-size: small;

        }


        </style>
        </head>
        <body>
        <header>
           <h1>Foxy Predictor</h1>
        </header>


        <div class="flex-container">
          <div class="flex-item">{{attrs[1]}}</div>
          <div class='flex-item' id="geochart-colors" style="width: 600px; height: 350px;"></div>
          <div class="flex-item">{{attrs[0]}}</div>
          <div class="flex-item">Here we present visual representations of our predictions for the German Election 2017.</div>
        </div>

        <footer>
           <h1>Copyright @ Foxy Predictor</h1>
        </footer>
        </body>
        </html>


        <ul>
          {% for attr in attrs %}
          <li>{{attr}}</li>
          {% endfor %}
        </ul>
        </html>
        """)

    output= template.render({'attrs': [xx, xxx]})

    Html_file= open("Dashboard.html","w")
    Html_file.write(output)
    Html_file.close()
