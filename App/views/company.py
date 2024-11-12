from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from .index import index_views


from App.controllers import(
    get_user_by_username,
    get_all_listings,
    get_company_listings,
    add_listing,
    add_categories,
    get_listing,
    set_request
)

from App.models import(
    Alumni,
    Company,
    Admin
)

company_views = Blueprint('company_views', __name__, template_folder='../templates')

@company_views.route('/view_applications/<int:job_id>', methods=['GET'])
@jwt_required()
def view_applications_page(job_id):

    # get the listing
    listing = get_listing(job_id)

    response = None
    print(listing)

    try:
        applicants = listing.get_applicants()
        print(applicants)
        return render_template('viewapp-company.html', applicants=applicants)

    except Exception:
        flash('Error receiving applicants', 'unsuccessful')
        response = redirect(url_for('index_views.index_page'))

    return response

@company_views.route('/add_listing', methods=['GET'])
@jwt_required()
def add_listing_page():

    return render_template('companyform.html')

@company_views.route('/add_listing', methods=['POST'])
@jwt_required()
def add_listing_action():
    data = request.form

    response = None

    try:
        remote = False
        national = False

        if 'remote_option' in data and data['remote_option'] == 'Yes':
            remote = True

        if 'national_tt' in data and data['national_tt'] == 'Yes':
            national = True

        listing = add_listing(data['title'], data['description'], current_user.company_name, data['salary'], data['position_type'],
                              remote, national, data['desired_candidate_type'], data['job_area'], None)
        flash('Created job listing', 'success')
        response = redirect(url_for('index_views.index_page'))
    except Exception:
        flash('Error creating listing', 'unsuccessful')
        response = redirect(url_for('company_views.add_listing_page'))
    
    return response

@company_views.route('/request_delete_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def request_delete_listing_action(job_id):

    listing = set_request(job_id, 'Delete')
    response = None

    if listing is not None:
        flash('Request for deletion sent!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Error sending request', 'unsuccessful')
        response = redirect(url_for('index_views.login_page'))

    return response

@company_views.route('/request_edit_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def request_edit_listing_action(job_id):

    listing = set_request(job_id, 'Edit')
    response = None
    print(listing.request)

    if listing is not None:
        flash('Request for edit sent!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Error sending request', 'unsuccessful')
        response = redirect(url_for('index_views.login_page'))

    return response