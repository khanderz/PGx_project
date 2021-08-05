from model import connect_to_db, db, Drug, Dosage, Pharmacokinetics, Pharmacogenomics

def create_drug(generic_name, brand_name, pharmGKB_ID, pgx_moa):
    """create and return new drug"""

    drug = Drug(generic_name=generic_name, 
                brand_name=brand_name, 
                pharmGKB_ID=pharmGKB_ID, 
                pgx_moa=pgx_moa)

    db.session.add(drug)
    db.session.commit()

    return drug    

def create_dosage(dosing, special_populations, pgx):
    """create dosing for drug"""

    dosage = Dosage(dosing=dosing, 
                    special_populations=special_populations,
                    pgx=pgx)

    db.session.add(dosage)
    db.session.commit()

    return dosage                    

def create_pk(overview, absorption, food, distribution, elimination, special_populations, ddi_studies):
    """create pk on pk class"""

    pk = Pharmacokinetics(overview=overview, 
                        absorption=absorption, 
                        food=food, 
                        distribution=distribution, 
                        elimination=elimination, 
                        special_populations=special_populations, 
                        ddi_studies=ddi_studies)

    db.session.add(pk)
    db.session.commit()

    return pk           


def create_pgx(overview, dosage, special_populations, ddis, lab_tests, precautions):
    """create pgx on pgx class"""

    pgx = Pharmacogenomics(overview=overview, 
                            dosage=dosage, 
                            special_populations=special_populations, 
                            ddis=ddis, 
                            lab_tests=lab_tests, 
                            precautions=precautions)

    db.session.add(pgx)
    db.session.commit()

    return pgx                         


def get_drugs():
    """Return all drugs"""
    return Drug.query.all()

def get_drug_by_name(generic_name):
    """Return drug by drug id"""

    return Drug.query.filter_by(generic_name=generic_name).first()   

def get_all_generic_names():
    """Return generic names
    
    returns:
    [
    ('amifampridine',), 
    ('amifampridine phosphate',), 
    ('aripiprazole',), 
    ('aripiprazole lauroxil',), 
    ('atomoxetine',)...
    ]
    """

    return db.session.query(Drug.generic_name).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
