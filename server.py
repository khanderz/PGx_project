"""server for PGx project"""

from flask import (Flask, render_template, request)
from jinja2 import StrictUndefined
import requests


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/load_options')
def load_options():
    """If flowchart is not null, load drug name onto options list"""    

    url = 'https://data.cpicpgx.org/v1/drug?flowchart=neq.(null)'
    res = requests.get(url)
    data = res.json()

    # json data returned:
        # [{
        #     "drugid":"RxNorm:38400",
        #     "name":"atomoxetine",
        #     "pharmgkbid":"PA134688071",
        #     "rxnormid":"38400",
        #     "drugbankid":"DB00289",
        #     "atcid":["N06BA09"],
        #     "umlscui":null,
        #     "flowchart":"https://files.cpicpgx.org/images/flow_chart/Atomoxetine_CDS_Flow_Chart.jpg",
        #     "version":40,
        #     "guidelineid":104243,
        # }]

        # to access name: data[i]['name']


    drugs_with_flowcharts = []

    for key in data:
       drugs_with_flowcharts.append(key['name'])

  

    return render_template('index.html', drugs_with_flowcharts=drugs_with_flowcharts)


@app.route('/results')
def render_results():
    """View results page"""

    drug_name = request.args.get('drug')
    print(drug_name, "****************************drug name")

    url = 'https://data.cpicpgx.org/v1/drug?name=in.("' + drug_name + '")'
    print(url, "**************************** url")

    res = requests.get(url)
    data = res.json()
    flowchart = data[0]['flowchart']

    print(flowchart, "****************************RESULTS")


    return render_template('results.html', 
                            flowchart=flowchart)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)