from App.database import db
from sqlalchemy.dialects.postgresql import JSON

class Application (db.Model):
    application_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    date_applied = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Foreign Key to Alumni
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)

     # Additional Information from Profile
     # For storing custom fields such as achievements, certifications, or portfolio links 
     # without altering the database schema for each new type of information.
    additional_info = db.Column(JSON, nullable=True)
    
    # Relationship to Alumni and Listing needed 

    def __init__(self, date_applied, alumni_id, listing_id):
        self.date_applied = date_applied
        self.alumni_id = alumni_id
        self.listing_id = listing_id