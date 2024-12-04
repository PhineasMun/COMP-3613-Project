from App.models import Company, Listing
from App.database import db

def add_company(company_name, company_address, contact, company_website):
    newCompany = Company(company_name, company_address, contact, company_website)
    try:
        db.session.add(newCompany)
        db.session.commit()
        return newCompany
    except:
        db.session.rollback()
        return None

def send_notification(job_categories=None):
    # get all the subscribed alumni who have the job categories
    from App.controllers import get_all_subscribed_alumni

    subbed = get_all_subscribed_alumni()

    job_categories = set(job_categories)
    notif_alumni = []

    for alumni in subbed:
        jobs = set(alumni.get_categories())
        common_jobs = list(jobs.intersection(job_categories))

        if common_jobs:
            notif_alumni.append(alumni)

    # Send notification (e.g., using Mailchimp or other service)
    print(notif_alumni, job_categories)
    return notif_alumni, job_categories

def add_listing(title, description, company_name, salary, position, remote, ttnational, desiredcandidate, area, job_categories=None):
    # manually validate that the company actually exists
    company = get_company_by_name(company_name)
    if not company:
        return None

    newListing = Listing(title, description, company_name, job_categories, salary, position, remote, ttnational, desiredcandidate, area)
    
    try:
        db.session.add(newListing)
        db.session.commit()

        return newListing
    except:
        db.session.rollback()
        return None

def get_company_by_name(company_name):
    return Company.query.filter_by(company_name=company_name).first()

def get_company_listings(company_name):
    company = get_company_by_name(company_name)
    return company.listings

def get_all_companies():
    return Company.query.all()

def get_all_companies_json():
    companies = get_all_companies()
    if not companies:
        return []
    companies = [company.get_json() for company in companies]
    return companies

def update(self, listing, applicant_name):
    print(f"Company '{self.company_name}' notified of {applicant_name}'s application to '{listing.title}'")
    self.forward_to_subscribed_employees(listing, applicant_name)

def forward_to_subscribed_employees(self, listing, applicant_name):
    for employee in self.employees:
        if employee.subscribed:
            print(f"Notification sent to {employee.first_name} {employee.last_name} about {applicant_name}'s application to '{listing.title}'")