from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


from App.controllers import(
    get_all_listings,
    get_company_listings,
    add_listing,
    apply_listing,
    add_alumni,
    add_admin,
    add_company,
    get_listing
)

from App.models import(
    Alumni,
    Company,
    Admin
)

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/app', methods=['GET'])
@jwt_required()
def index_page():
    jobs = get_all_listings()

    if isinstance(current_user, Alumni):
        return render_template('alumni.html', jobs=jobs )
    
    if isinstance(current_user, Company):
        jobs = get_company_listings(current_user.username)
        return render_template('company-view.html', jobs=jobs)

    if isinstance(current_user, Admin):
        return render_template('admin.html', jobs=jobs)
    
    return redirect('/login')


@index_views.route('/submit_application', methods=['POST'])
@jwt_required()
def submit_application_action():
    # get form data
    data = request.form

    response = None

    print(data)

    try:
        alumni = apply_listing(current_user.alumni_id, data['job_id'])

        response = redirect(url_for('index_views.index_page'))
        flash('Application submitted')

    except Exception:
        flash('Error submitting application')
        response = redirect(url_for('auth_views.login_page'))

    return response

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    add_admin('bob', 'bobpass', 'bob@mail')

    add_alumni('rob', 'robpass', 'rob@mail', '123456789', '1868-333-4444', 'robfname', 'roblname')

    add_company('company1', 'company1', 'compass', 'company@mail',  'company_address', 'contact', 'company_website.com')
    add_company('company2', 'company2', 'compass', 'company@mail2',  'company_address2', 'contact2', 'company_website2.com')

    add_listing('listing1', 'job description1', 'company1',
                8000, 'Part-time', True, 'employmentTerm!', True, 'desiredCandidate?', 'Curepe', ['Database', 'Programming', 'butt'])

    add_listing('listing2', 'job description', 'company2',
                4000, 'Full-time', True, 'employmentTerm?', True, 'desiredCandidate?', 'Curepe', ['Database', 'Programming', 'butt'])

    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})