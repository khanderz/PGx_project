from server import app
from model import db, connect_to_db, Drug, Dosage, Pharmacokinetics, Pharmacogenomics
import os
import json
import crud


os.system('dropdb drugs')
os.system('createdb drugs')

connect_to_db(app)
db.create_all()

with open('data/test.json') as f:
    drug_data = json.loads(f.read())

drugs_in_db = []

for drug in drug_data:
    generic_name, brand_name, pharmGKB_ID, pharmacokinetics, overview, absorption, food, distribution, elimination, special_populations, ddi_studies, dosage, dosing, special_populations3, pgx, pharmacogenomics, overview2, dosage2, special_populations2, ddis, lab_tests, precautions, pgx_moa = (drug['generic_name'],
                        drug['brand_name'],
                        drug['pharmGKB_ID'],
                        drug['pharmacokinetics'],
                        drug['pharmacokinetics']['overview'],
                        drug['pharmacokinetics']['absorption'],
                        drug['pharmacokinetics']['food'],
                        drug['pharmacokinetics']['distribution'],
                        drug['pharmacokinetics']['elimination'],
                        drug['pharmacokinetics']['special_populations'],
                        drug['pharmacokinetics']['ddi_studies'],
                        drug['dosage'],
                        drug['dosage']['dosing'],
                        drug['dosage']['special_populations'],
                        drug['dosage']['pgx'],
                        drug['pharmacogenomics'],
                        drug['pharmacogenomics']['overview'],
                        drug['pharmacogenomics']['dosage'],
                        drug['pharmacogenomics']['special_populations'],
                        drug['pharmacogenomics']['ddis'],
                        drug['pharmacogenomics']['lab_tests'],
                        drug['pharmacogenomics']['precautions'],
                        drug['pgx_moa'])        

    db_drug = crud.create_drug(generic_name, 
                                brand_name, 
                                pharmGKB_ID, 
                                pgx_moa)

    db_drug.dosage = crud.create_dosage(dosing,
                                    special_populations3,
                                    pgx)                            

    db_drug.pharmacokinetics = crud.create_pk(overview, 
                                                absorption, 
                                                food, 
                                                distribution, 
                                                elimination, 
                                                special_populations, 
                                                ddi_studies)     

    db_drug.pharmacogenomics = crud.create_pgx(overview2,
                                                dosage2,
                                                special_populations2,
                                                ddis,
                                                lab_tests,
                                                precautions)                                                                 

    drugs_in_db.append(db_drug)
