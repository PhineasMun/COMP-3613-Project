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
    delete_listing
)

from App.models import(
    Alumni,
    Company,
    Admin
)

admin_views = Blueprint('admin_views', __name__, template_folder='../templates')

@admin_views.route('/delete_listing/<int:job_id>', methods=['GET'])
@jwt_required()
def delete_listing_action(job_id):

    deleted = delete_listing(job_id)

    response = None

    if deleted:
        flash('Job listing deleted!', 'success')
        response = redirect(url_for('index_views.index_page'))
    else:
        flash('Error deleting job listing', 'unsuccessful')
        response = (redirect(url_for('index_views.login_page')))

    return response