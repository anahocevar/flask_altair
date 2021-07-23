from flask import Flask, render_template, request

import numpy as np
import pandas as pd
import altair as alt

import requests
import folium

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', this=None)


@app.route('/plot')
def altair_plot():
    n = int(request.args.get('n', 0))
    
    x = np.random.random(n) * 10
    y = np.random.random(n) * 10
    s = np.random.random(n)
    
    df = pd.DataFrame({'x':x, 'y':y, 'size': s})
    
    chart = alt.Chart(df, width=300,
                      height=300).mark_point().encode(
                x='x',
                y='y',
                size=alt.Size('size', legend=None),
                tooltip=['size']
    ).interactive()
    myjson = chart.to_json()
        
    return render_template('plot.html', json=myjson)

@app.route('/largeplot')
def largealtair_plot():
    n = int(request.args.get('n', 0)) 
    chart = alt.Chart(f'altair_data.json?n={n}', width=300,
                      height=300).mark_point().encode(
                x='x:Q',
                y='y:Q',
                size=alt.Size('size:Q', legend=None),
                tooltip=['size:Q']
    ).interactive()
    json = chart.to_json()
        
    return render_template('plot.html', json=json)

@app.route('/altair_data.json')
def data_serving():
    n = int(request.args.get('n', 100))    
    x = np.random.random(n) * 10
    y = np.random.random(n) * 10
    s = np.random.random(n)
    
    df = pd.DataFrame({'x':x, 'y':y, 'size': s})
    return df.to_json(orient='records')
            
if __name__ == '__main__':
    app.run(port=8000, debug=True)