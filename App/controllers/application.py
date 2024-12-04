from App.models import db, Application, Alumni

def add_info_to_application(application_id, alumni_id, additional_info):
    """
    Add information from Alumni profile to an Application.
    """
    application = Application.query.filter_by(id=application_id, alumni_id=alumni_id).first()
    if not application:
        return {"error": "Application not found or unauthorized."}
    
    # Fetch Alumni's profile
    alumni = Alumni.query.get(alumni_id)
    if not alumni:
        return {"error": "Alumni not found."}
    
    # Validate and merge additional_info
    if application.additional_info is None:
        application.additional_info = {}
    
    for key, value in additional_info.items():
        if key in alumni.profile:  # Ensure key exists in the profile
            application.additional_info[key] = value
    
    db.session.commit()
    return {"success": "Information added to application."}

def apply_to_listing():
    # Extract data from the incoming request (e.g., from the frontend)
    alumni_id = request.json.get('alumni_id')
    listing_id = request.json.get('listing_id')
    
    # Get the listing and alumni from the database
    alumni = Alumni.query.filter_by(alumni_id=alumni_id).first()
    listing = Listing.query.get(listing_id)

    if not alumni or not listing:
        return jsonify({"message": "Alumni or Listing not found!"}), 404

    # Create the application instance
    application = Application(
        date_applied=db.func.current_timestamp(),
        alumni_id=alumni.alumni_id,
        listing_id=listing.id
    )
    
    # Add the application to the database
    db.session.add(application)
    db.session.commit()

    # Trigger the listing to notify company
    listing.notify_company_of_application(alumni_id.alumni_name)
    
    return jsonify({"message": "Application submitted successfully!"}), 200
