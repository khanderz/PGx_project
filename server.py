"""server for PGx project"""

from flask import (Flask, render_template, request, jsonify)
from jinja2 import StrictUndefined
import requests
import os
import json
from model import connect_to_db, db, Drug
import crud


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


API_KEY = os.environ['FDA_KEY']

drug_datafile = open('data/fda_labeling.json')

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/load_options')
def load_options():
    """load gene symbols and results onto option list"""    

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


    gene_symbol = set([])
    results = set([])

    for key in data:
       gene_symbol.add(key['genesymbol'])
       results.add(key['result'])


    return render_template('index.html', gene_symbol=gene_symbol, results=results)


@app.route('/results')
def render_results():
    """render custom search query on CPIC API"""

    gene = request.args.get('gene')
    result = request.args.get('result')
    print(gene, result, "^^^^^^^^^^^^^^^gene and result")

    url = 'https://data.cpicpgx.org/v1/gene_result?genesymbol=in.("' + gene + '")&result=in.("' + result + '")'

    res = requests.get(url)
    data = res.json()
    cds = data[0]['consultationtext']

    print(cds, "****************************RESULTS")


    return render_template('results.html', 
                            cds=cds)

@app.route('/pharmgkb_id')
def retrieve_pharmgkb_id():
    """get pharmgkbid from CPIC API"""

    url = 'https://data.cpicpgx.org/v1/drug'
    res = requests.get(url)
    data = res.json()

    drugs = []

    for key in data:
        drugs.append(key['name'])

    return render_template('pharmgkb_search.html', drugs=drugs)    

@app.route('/pharmgkb_search')
def query_pharmgkb():
    drug = request.args.get('drug')
    print(drug, "****************************drug")

    url = 'https://data.cpicpgx.org/v1/drug?name=in.("' + drug + '")'
    res = requests.get(url)
    data = res.json()
    print(data, "****************************data")

    pharmgkb_id = data[0]['pharmgkbid']
    print(pharmgkb_id, "****************************pharmgkb ID")

    url = "https://api.pharmgkb.org/v1/data/guideline?relatedChemicals.accessionId=" + pharmgkb_id 
    print(url, "****************************url")
    res = requests.get(url)
    print(res, "****************************res")

    data = res.json()


    return render_template('pharmgkb_results.html', data=data)

@app.route('/fda_search')    
def query_fda_for_dosing():
    drug = "aripiprazole"

    url = 'https://api.fda.gov/drug/label.json?api_key=' + API_KEY + '&search=description:' + drug

    res = requests.get(url)
    print(res, "****************************res")

    data = res.json()

    # lists is one big list
    lists = data['results']


    # # results is converted to json string
    # results = json.dumps(lists)

    # result = json.loads(results)

    # # result is converted to list
    # result = json.loads(results)

    # keys = result.keys()

    return render_template('fda_results.html', data=lists)

@app.route('/drug_search')    
def render_drugdata():

    lists = crud.get_all_generic_names()

    drugs = []

    for i in lists:
        el=str(i)
        drug = el.strip("('',)")
        drugs.append(drug)


    return render_template('drug_search.html', drugs=drugs)

@app.route('/drug_data')   
def drug_search():
    drug = request.args.get("drug_json")
    print(drug, "*******************Drug" )

    drug_data = crud.get_drug_by_name(drug)  
    print(drug_data, "*******************Drug data" )
    print(type(drug_data), "&&&&&&&&&&&&&&&&TYPE")

    return render_template('drug_data.html', drug_data=drug_data)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=False)