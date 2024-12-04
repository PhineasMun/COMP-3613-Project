from App.database import db
from App.models import Listing
from sqlalchemy.dialects.postgresql import JSON

class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    date_applied = db.Column(db.DateTime, default=db.func.current_timestamp())

    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)

    additional_info = db.Column(JSON, nullable=True)

    def __init__(self, date_applied, alumni_id, listing_id):
        self.date_applied = date_applied
        self.alumni_id = alumni_id
        self.listing_id = listing_id

    def get_json(self):
        return {
            'application_id': self.application_id,
            'date_applied': self.date_applied,
            'alumni_id': self.alumni_id,
            'listing_id': self.listing_id,
            'additional_info': self.additional_info,
        }

    #Trigger
    # Notify the company associated with this application
    def notify_company(self):
        listing = Listing.query.get(self.listing_id)
        applicant_name = f"{self.alumni.first_name} {self.alumni.last_name}"
        listing.notify_company_of_application(applicant_name)