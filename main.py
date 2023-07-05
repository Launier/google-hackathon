# app.py
import io
from flask import Flask, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import gmaps
import gmaps.datasets
from shapely import wkt

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Was auch immer'

@app.route('/plot')
def plot():
    # Your BigQuery SQL query
    sql_query = """
    SELECT *
    FROM `qwiklabs-gcp-04-ad75353ab664.hackathon.road_config`
    """

    # Load your data from BigQuery
    data = pd.read_gbq(query=sql_query, project_id="qwiklabs-gcp-04-ad75353ab664")

    # Convert the LineStrings from text to geometric objects
    data['geom'] = data['geom'].apply(wkt.loads)

    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(data, geometry='geom')

    # Now, create your plot
    fig, ax = plt.subplots(1, 1)
    gdf.plot(column='no2_ppb', ax=ax, legend=True)

    # Save it to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Return the plot as a PNG
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
