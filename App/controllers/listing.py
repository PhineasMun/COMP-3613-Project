from App.models import Listing
from App.database import db

# Set request status for a listing (Edit/Delete/None)
def set_request(id, request):
    listing = get_listing(id)

    if listing:
        if request == 'Delete':
            listing.request = request
        elif request == 'Edit':
            listing.request = request
        else:
            listing.request = 'None'
        db.session.add(listing)
        db.session.commit()

    return listing

# Get a listing by its ID
def get_listing(id):
    return Listing.query.filter_by(id=id).first()

# Get a listing by its title
def get_listing_title(listing_title):
    return Listing.query.filter_by(title=listing_title).first()

# Get all listings
def get_all_listings():
    return Listing.query.all()

# Get all applicants for a given listing
def get_all_applicants(id):
    listing = get_listing(id)
    return listing.get_applicants()

# Get all listings in JSON format
def get_all_listings_json():
    listings = get_all_listings()
    if not listings:
        return []
    listings = [listing.get_json() for listing in listings]
    return listings

# Handle application notifications for a listing
def handle_application_notification(application, listing):
    # Local imports to avoid circular imports
    from App.controllers import send_employee_notification, send_notification

    # Notify the employees associated with the listing
    applicant_name = f"{application.alumni.first_name} {application.alumni.last_name}"
    send_employee_notification(listing, applicant_name)

    # Notify all alumni (if needed, based on the job categories they are subscribed to)
    job_categories = listing.job_categories
    send_notification(job_categories)