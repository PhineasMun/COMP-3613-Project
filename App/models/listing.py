import uuid
from App.database import db
from sqlalchemy import CheckConstraint
from App.models import application

# categories list for possible job categories
categories = [
    'Software Engineer', 'Database Manager', 'Programming', 'Web Design', 'Cyber Security', 
    'Big Data', 'Algorithms', 'N/A']

class Listing(db.Model):
    listing_id = db.Column(db.String, primary_key=True)  # Unique identifier
    title = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.String(500))
    company_id = db.Column(db.String, db.ForeignKey('company.company_id'), nullable=False)  # Foreign key to Company
    salary = db.Column(db.String(), nullable=False)
    position = db.Column(db.String(), nullable=False)
    remote = db.Column(db.Boolean, default=False)
    ttnational = db.Column(db.Boolean, default=False)
    desired_candidate = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(120), nullable=False)
    # requests for deletion?----- Don't take out this comment yet... ~Tamia
    approved = db.Column(db.Boolean, default=False)

    # Relationship with applications (1-to-many)
    applications = db.relationship('Application', backref='listing', lazy=True, cascade="all, delete-orphan")

    # Foreign key to the Company table
    company_id = db.Column(db.String, db.ForeignKey('company.company_id'), nullable=False)

    # Relationship with Company (M-1)
    company = db.relationship('Company', back_populates='listing')

    def __init__(self, listing_id, title, description, company_id, salary, position, remote, ttnational, desired_candidate, area, approved=False):
        self.listing_id = listing_id
        self.title = title
        self.description = description
        self.company_id = company_id
        self.salary = salary
        self.position = position
        self.remote = remote
        self.ttnational = ttnational
        self.desired_candidate = desired_candidate
        self.area = area
        self.approved = approved

    def submit_application(self, alumini_id,date_applied,listing_id):
        new_application = application.Application(
            application_id = str(uuid.uuid4()),
            listing_id = self.listing_id,
            alumini_id = alumini_id,
            date_applied = date_applied,
        )
        
        # Add to the database session
        db.session.add(new_application)
        db.session.commit()

        return {
            "message": "Application submitted successfully.",
            "application_id": new_application.application_id
        }
    
    def get_categories(self):
        return self.category.split('|')

    def get_json(self):
        return {
            'listing_id': self.listing_id,
            'title': self.title,
            'description': self.description,
            'company_id': self.company_id,
            'salary': self.salary,
            'position': self.position,
            'remote': self.remote,
            'ttnational': self.ttnational,
            'desired_candidate': self.desired_candidate,
            'area': self.area,
            'jobCategories': [self.applications.get_json() for category in self.categories],
            'approved': self.approved,
            'applications': [self.applications.get_json() for application in self.applications],
        }
