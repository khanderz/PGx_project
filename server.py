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
    drug_name = "celecoxib"

    url = 'https://data.cpicpgx.org/v1/drug?name=in.("' + drug_name + '")'


    res = requests.get(url)
    data = res.json()
    flowchart = data[0]['flowchart']

    print(flowchart, "****************************RESULTS")


    return render_template('index.html', 
                            flowchart=flowchart)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)