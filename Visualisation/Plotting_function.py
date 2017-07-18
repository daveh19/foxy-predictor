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
import os
import sys
sys.path.append(os.path.abspath('../Backend'))
sys.path.append(os.path.abspath('../Python_Gui/'))
import wahlrecht_polling_firms
import wahlrecht_states
from vars import PARTIES

def plot_graphs(data_new):
    CDUstr="CDU/CSU"
    SPDstr="SPD"
    GRÜNEstr="GRÜNE"
    LINKEstr='LINKE'
    FDPstr='FdP'
    AfDstr='AfD'

    lower_range = data_new['lower'][::-1]
    mean_range = data_new['mean']
    upper_range = data_new['upper'][::-1]
    histograms = data_new ['hist']
    data_original = data_new['original']
    #data_original[PARTIES] = data_original[PARTIES].applymap(lambda x : x[1])
    data_new = data_new['mean']
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


    timeline= data_new.Datum[::-1]
    CDU_data=data_new[CDUstr][::-1]
    SPD_data=data_new[SPDstr][::-1]
    Green_data=data_new[GRÜNEstr][::-1]
    Linke_data=data_new[LINKEstr][::-1]
    AFD_data=data_new[AfDstr][::-1]

    org_timeline = data_original.Datum
    CDU_original=data_original[CDUstr][::-1]
    SPD_original=data_original[SPDstr][::-1]
    Green_original=data_original[GRÜNEstr][::-1]
    Linke_original=data_original[LINKEstr][::-1]
    AFD_original=data_original[AfDstr][::-1]


    upper_bound_CDU = go.Scatter(
        name='Upper Bound CDU',
        x=timeline,
        y=upper_range[CDUstr],
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
      mode='lines',
      )

    CDU_original = go.Scatter(
        x=org_timeline,
        y=CDU_original,
        name="CDU",
        marker = dict(
        size = 4,
        color = 'rgba(0, 0, 0)',),
        opacity=0.4,
        mode='markers',
        )
    SPD_original = go.Scatter(
        x=org_timeline,
        y=SPD_original,
        name="SPD",
        marker = dict(
        size = 4,
        color = 'rgb(165,0,38)',),
        opacity=0.4,
        mode='markers',
        )
    Green_original = go.Scatter(
        x=org_timeline,
        y=Green_original,
        name="Green",
        marker = dict(
        size = 4,
        color = 'rgb(154,205,50)',),
        opacity=0.4,
        mode='markers',
        )

    Linke_original = go.Scatter(
        x=org_timeline,
        y=Linke_original,
        name="CDU",
        marker = dict(
        size = 4,
        color = 'rgb(0,204,255)',),
        opacity=0.4,
        mode='markers',
        )
    AFD_original = go.Scatter(
        x=org_timeline,
        y=AFD_original,
        name="CDU",
        marker = dict(
        size = 4,
        color = 'rgb(153,102,255)',),
        opacity=0.4,
        mode='markers',
        )


    lower_bound_CDU = go.Scatter(
        name='Lower Bound CDU',
        x=timeline,
        y=lower_range[CDUstr],
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
      y=upper_range[SPDstr],
      mode='lines',
      marker=dict(color='rgb(165,0,38)'),
      line=dict(width=0),
      opacity=0.25,
      fill='none',
      showlegend=False)

    lower_bound_SPD = go.Scatter(
      name='Lower Bound SPD',
      x=timeline,
      y=lower_range[SPDstr],
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
        y=upper_range[GRÜNEstr],
        mode='lines',
        marker=dict(color='rgb(154,205,50)'),
        line=dict(width=0),
        opacity=0.1,
        fill='none',
        showlegend=False)

    lower_bound_Gruene = go.Scatter(
        name='Lower Bound Gruene',
        x=timeline,
        y=lower_range[GRÜNEstr],
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
        y=upper_range[LINKEstr],
        mode='lines',
        marker=dict(color='rgb(0,204,255)'),
        line=dict(width=0),
        opacity=0.1,
        fill='none',
        showlegend=False)

    lower_bound_Linke = go.Scatter(
        name='Lower Bound Linke',
        x=timeline,
        y=lower_range[LINKEstr],
        marker=dict(color='rgb(0,204,255)'),
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
        y=upper_range[AfDstr],
        mode='lines',
        marker=dict(color='rgb(153,102,255)'),
        line=dict(width=0),
        opacity=0.1,
        fill='none',
        showlegend=False)

    lower_bound_AFD = go.Scatter(
        name='Lower Bound AfD',
        x=timeline,
        y=lower_range[AfDstr],
        marker=dict(color='rgb(153,102,255)'),
        line=dict(width=0),
        mode='lines',
        opacity=0.1,
        fill='tonextx',
        showlegend=False
        )

    data = [CDU,CDU_original,upper_bound_CDU,lower_bound_CDU,SPD,upper_bound_SPD,lower_bound_SPD]


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
    #fig_5.append_trace(CDU_original,1,1)
    fig_5.append_trace(upper_bound_CDU, 1,1)
    fig_5.append_trace(lower_bound_CDU, 1,1)
    fig_5.append_trace(SPD, 1,1)
    #fig_5.append_trace(SPD_original,1,1)
    fig_5.append_trace(upper_bound_SPD, 1,1)
    fig_5.append_trace(lower_bound_SPD, 1,1)

    fig_5.append_trace(Gruene, 2,1)
    #fig_5.append_trace(Green_original,2,1)
    fig_5.append_trace(upper_bound_Gruene, 2,1)
    fig_5.append_trace(lower_bound_Gruene, 2,1)
    fig_5.append_trace(AFD, 2,1)
    #fig_5.append_trace(AFD_original,2,1)
    fig_5.append_trace(upper_bound_AFD, 2,1)
    fig_5.append_trace(lower_bound_AFD, 2,1)
    fig_5.append_trace(Linke, 2,1)
    #fig_5.append_trace(Linke_original,2,1)
    fig_5.append_trace(upper_bound_Linke, 2,1)
    fig_5.append_trace(lower_bound_Linke, 2,1)



    fig_5['layout'].update(title='Evolution of Second Vote Prediction')

    histos = []
    for i, party in enumerate(PARTIES):
        histos.append(histograms[:,i])

    CDU_hist = histos[0]
    SPD_hist = histos[1]
    Gruene_hist = histos[2]
    Linke_hist = histos[4]
    AFD_hist = histos[5]
    FDP_hist = histos[3]
    #histograms['CDU'] , histograms['SPD'], histograms['CDU'] , histograms['Gruene'], histograms['Linke'], histograms['AfD'], histograms['FDP']
    CDU_h = go.Histogram(
        x=CDU_hist,
        name = "CDU",
        xbins=dict(
            start=0,
            end=60,
            size=1),
        marker=dict(color='rgb(0,0,0)'),
        opacity=0.5, histnorm='probability')

    SPD_h= go.Histogram(
        x=SPD_hist,
        name = "SPD",
        xbins=dict(
            start=0,
            end=60,
            size=1),
        marker=dict(color='rgb(165,0,38)'),
        opacity=0.5, histnorm='probability')

    Gruene_h = go.Histogram(
        x=Gruene_hist,
        name = "Gruene",
        xbins=dict(
            start=0,
            end=60,
            size=1),
        marker=dict(color='rgb(154,205,50)'),
        opacity=0.5, histnorm='probability')

    Linke_h= go.Histogram(
        x=Linke_hist,
        name = "Linke",
        xbins=dict(
            start=0,
            end=60,
            size=1),
        marker=dict(color='rgb(0,204,255)'),
        opacity=0.5, histnorm='probability')

    AfD_h = go.Histogram(
        x=AFD_hist,
        name = "AfD",
        xbins=dict(
            start=0,
            end=60,
            size=1),
        marker=dict(color='rgb(153,102,255)'),
        opacity=0.5, histnorm='probability')


    data = [CDU_h, SPD_h, Gruene_h, Linke_h, AfD_h]

    layout_h = go.Layout(barmode='stack',
        title='Histogram of Simulation Results',
        xaxis=dict(
            title='Percentage'
        ),
        yaxis=dict(
            title='Probability'
    ))

    hist = go.Figure(data=data, layout=layout_h)



    tables_states = wahlrecht_states.get_tables()
    parties = tables_states['be'].columns[4:]

    most_recent = {}
    for state, table in sorted(tables_states.items()):
        try:
            most_recent[state] = table.iloc[0, 4:]
        except IndexError:
            pass
    majority = [np.where(parties == most_recent[state].argmax())[0][0]+1 for state in sorted(most_recent.keys())]




    xx=offline.plot(fig_1 ,show_link=False, output_type='div', filename='SeatChart.html',image='None', image_width=80, image_height=60)
    xxx=offline.plot(fig_5 ,show_link=False, output_type='div', filename='TimeEvolution.html',image='None', image_width=80, image_height=60)
    xxxx=offline.plot(hist,show_link=False, output_type='div', filename = "Party_Distributions",image='None', image_width=80, image_height=60)


    tmp = """
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
     google.charts.load('current', {{
       'packages':['geochart'],
       // Note: you will need to get a mapsApiKey for your project.
       // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
       'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
     }});
     google.charts.setOnLoadCallback(drawRegionsMap);

     function drawRegionsMap() {{
       var data = google.visualization.arrayToDataTable([
         ['State', 'Name', 'Party Majority'],
         ['DE-BB', 'Brandenburg', {0}],
         ['DE-BE', 'Berlin', {1}],
         ['DE-BW', 'Baden-Württemberg', {2}],
         ['DE-BY', 'Bayern', {3}],
         ['DE-HE', 'Hessen', {4}],
         ['DE-HH', 'Hamburg', {5}],
         ['DE-MV', 'Mecklenburg-Vorpommern', {6}],
         ['DE-NI', 'Niedersachsen', {7}],
         ['DE-NW', 'Nordrhein-Westfalen', {8}],
         ['DE-RP', 'Rheinland-Pfalz', {9}],
         ['DE-SH', 'Schleswig-Holstein', {10}],
         ['DE-SL', 'Saarland', {12}],
         ['DE-SN', 'Sachsen', {12}],
         ['DE-ST', 'Sachsen-Anhalt', {13}],
         ['DE-TH', 'Thüringen', {14}]
       ]);

       var options = {{
       legend:'none',
       region: 'DE', // Germany

       resolution: 'provinces',
       dataMode: 'regions',
    colorAxis: {{
        colors: ['rgb(0,0,0)','rgb(0,0,0)',   'rgb(165,0,38)','rgb(165,0,38)', 'rgb(154,205,50)', 'rgb(154,205,50)', 'rgb(0,204,255)','rgb(0,204,255)', 'rgb(153,102,255)','rgb(153,102,255)', 'rgb(255,255,0)', 'rgb(255,255,0)'],
        values: ['0.5', '1.5',  '1.5', '2.5', '2.5', '3.5', '3.5', '4.5' , '4.5', '5.5' , '5.5' , '6.5']
    }},
       //datalessRegionColor: '#eeddff '
       }};

       var chart = new google.visualization.GeoChart(document.getElementById('geochart-colors'));
       chart.draw(data, options);
     }};
    </script>
        """
    tmp = tmp.format(*majority[:15])



    head = """
           <!DOCTYPE html>
           <html>
           <head>
           """

    tail = """
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
               width: 1400px;
               height: 1100px;
               background-color: white;
           }

           .flex-item {
               background-color: white;
               width: 700px;
               height: 350px;
               margin: 0px;
               flex-grow: 0.2
               margin-right: 150px;
               margin-down: 0px;
               border-right: 0px solid gray;
               align-items: stretch;


           }

           header {
               width: 1400px;

           }
           footer {
               width: 1400px;
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
             <div class="flex-item">{{attrs[2]}}</div>
             <div class="flex-item">{{attrs[0]}}</div>
             <div class='flex-item' id="geochart-colors" style="width: 600px; height: 350px;"></div>
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
           """

    template = head + tmp + tail
    template= jinja2.Template(template)


    output= template.render({'attrs': [xx, xxx,xxxx]})

    Html_file= open("Dashboard.html","w")
    Html_file.write(output)
    Html_file.close()
