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