from server import app
from model import db, connect_to_db, Drug
import os
import json
import crud


os.system('dropdb drugs')
os.system('createdb drugs')

connect_to_db(app)
db.create_all()

with open('data/fda_labeling.json') as f:
    drug_data = json.loads(f.read())

drugs_in_db = []

for drug in drug_data:
    generic_name, brand_name, pharmGKB_ID, pharmacokinetics, dosage_and_administration, pharmacogenomics, pgx_moa = (drug['generic_name'],
                        drug['brand_name'],
                        drug['pharmGKB_ID'],
                        drug['pharmacokinetics'],
                        drug['dosage_and_administration'],
                        drug['pharmacogenomics'],
                        drug['pgx_moa'])        

    db_drug = crud.create_drug(generic_name, 
                                brand_name, 
                                pharmGKB_ID, 
                                pharmacokinetics, 
                                dosage_and_administration, 
                                pharmacogenomics, 
                                pgx_moa)

    drugs_in_db.append(db_drug)
