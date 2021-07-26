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
    """load gene symbols onto option list"""    

    url = 'https://data.cpicpgx.org/v1/gene_result'
    res = requests.get(url)
    data = res.json()

    # json data returned:
    # [{
    #     "id":829397,
    #     "genesymbol":"CFTR",
    #     "result":"ivacaftor responsive in CF patients",
    #     "activityscore":"n/a",
    #     "ehrpriority":null,
    #     "consultationtext":null,
    #     "version":1,
    #     "frequency":null
    #     }

        # to access name: data[i]['key']


    drug_gene_symbol = []

    for key in data:
       drug_gene_symbol.append(key['genesymbol'])

  

    return render_template('index.html', drug_gene_symbol=drug_gene_symbol)


@app.route('/results')
def render_results():
    """View results page"""

    gene = request.args.get('gene')
    print(gene, "****************************gene name")

    url = 'https://data.cpicpgx.org/v1/gene_result?genesymbol=in.("' + gene + '")'

    res = requests.get(url)
    data = res.json()
    cds = data[0]['consultationtext']

    print(cds, "****************************RESULTS")


    return render_template('results.html', 
                            cds=cds)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)