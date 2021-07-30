from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drug(db.Model):
    """a drug"""

    __tablename__ = 'drugs'

    drug_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    generic_name = db.Column(db.String)         
    brand_name = db.Column(db.String)
    pharmGKB_ID = db.Column(db.String)
    pharmacokinetics = db.Column(db.Text)
    dosage_and_administration = db.Column(db.Text)
    pharmacogenomics = db.Column(db.Text)
    pgx_moa = db.Column(db.String)
             

    def __repr__(self):
        return f'<drug_id={self.drug_id} generic={self.generic_name} brand={self.brand_name}>'  


def connect_to_db(flask_app, db_uri='postgresql:///drugs', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app    
    connect_to_db(app)      