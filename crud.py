from model import connect_to_db, db, Drug

def create_drug(generic_name, brand_name, pharmGKB_ID, pharmacokinetics, dosage_and_administration, pharmacogenomics, pgx_moa):
    """create and return new drug"""

    drug = Drug(generic_name=generic_name, 
                brand_name=brand_name, 
                pharmGKB_ID=pharmGKB_ID, 
                pharmacokinetics=pharmacokinetics, 
                dosage_and_administration=dosage_and_administration, 
                pharmacogenomics=pharmacogenomics, 
                pgx_moa=pgx_moa)

    db.session.add(drug)
    db.session.commit()

    return drug            

def get_drugs():
    """Return all drugs"""
    return Drug.query.all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
