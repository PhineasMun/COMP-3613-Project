from App.database import db

class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String, unique=True, nullable=False)
    company_address = db.Column(db.String(120))
    contact = db.Column(db.String())
    company_website = db.Column(db.String(120))

    # set up relationship with Listing object (1-M)
    listings = db.relationship('Listing', backref='company', lazy=True)
    # Relationship with Employee (1-M)
    employees = db.relationship('Employee', back_populates='company', lazy=True)


    def __init__(self, company_name, company_address, contact, company_website):
        self.company_name = company_name
        self.company_address = company_address
        self.contact = contact
        self.company_website = company_website
        
    def get_json(self):
        return{
            'id': self.company_id,
            'company_name': self.company_name,
            'email': self.email,
            'company_address':self.company_address,
            'contact':self.contact,
            'company_website':self.company_website
        }
    
    def get_name(self):
        return self.company_name