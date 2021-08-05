from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drug(db.Model):
    """a drug"""

    __tablename__ = 'drugs'

    drug_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    pk_id = db.Column(db.Integer, db.ForeignKey('pks.pk_id')) 
    pgx_id = db.Column(db.Integer, db.ForeignKey('pgx.pgx_id'))
    dosage_id = db.Column(db.Integer, db.ForeignKey('dosage.dosage_id'))

    dosage = db.relationship("Dosage", backref="drug")
    pharmacokinetics = db.relationship("Pharmacokinetics", backref="drug")
    pharmacogenomics = db.relationship("Pharmacogenomics", backref="drugs")

    generic_name = db.Column(db.String)         
    brand_name = db.Column(db.String)
    pharmGKB_ID = db.Column(db.String)

    pgx_moa = db.Column(db.String)
             

    def __repr__(self):
        return f'<drug_id={self.drug_id} generic={self.generic_name} brand={self.brand_name}>'  

class Dosage(db.Model):
    """dosing for a drug"""

    __tablename__ = "dosage"

    dosage_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    dosing = db.Column(db.Text)
    special_populations = db.Column(db.Text)
    pgx = db.Column(db.Text)        

    def __repr__(self):
        return f'<dosing_id={self.dosage_id} dosing ={self.dosing}>' 

class Pharmacokinetics(db.Model):
    """PK of a drug"""

    __tablename__ = 'pks'

    pk_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)

    overview = db.Column(db.Text)
    absorption = db.Column(db.Text)
    distribution = db.Column(db.Text)
    elimination = db.Column(db.Text)
    special_populations = db.Column(db.Text)
    ddi_studies = db.Column(db.Text)

    def __repr__(self):
        return f'<pk id ={self.pk_id} drug ={self.overview}>'        

class Pharmacogenomics(db.Model):
    """PGx of a drug"""

    __tablename__ = "pgx"

    pgx_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)

    overview = db.Column(db.Text)
    dosage = db.Column(db.Text)
    special_populations = db.Column(db.Text)
    ddis = db.Column(db.Text)
    lab_tests = db.Column(db.Text)
    precautions = db.Column(db.Text)

    def __repr__(self):
        return f'<pgx id ={self.pgx_id} drug ={self.overview}>'


def connect_to_db(flask_app, db_uri='postgresql:///drugs', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app    
    connect_to_db(app)      