from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
# from App.controllers import create_user

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from .index import index_views


from App.controllers import(
    get_user_by_username,
    is_alumni_subscribed,
    subscribe,
    unsubscribe,
    set_modal_window
)

from App.models import(
    Alumni,
    Company,
    Admin
)

alumni_views = Blueprint('alumni_views', __name__, template_folder='../templates')

@alumni_views.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe_action():
    # get form data
    data = request.form
    response = None

    # print(data)
    # print([data['category']])
    # print(current_user.alumni_id)

    try:
        alumni = subscribe(current_user.alumni_id, data['category'])
        set_modal_window(alumni.alumni_id)
        # print(alumni.get_json())
        response = redirect(url_for('index_views.index_page'))
        flash('Subscribed!', 'success')

    except Exception:
        # db.session.rollback()
        flash('Error subscribing', 'unsuccessful')
        response = redirect(url_for('auth_views.login_page'))

    return response

@alumni_views.route('/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe_action():
    # get form data
    # data = request.form
    response = None

    # print(data)

    try:
        alumni = unsubscribe(current_user.alumni_id)
        # print(alumni.get_json())
        response = redirect(url_for('index_views.index_page'))
        flash('Unsubscribed!', 'success')

    except Exception:
        # db.session.rollback()
        flash('Error unsubscribing', 'unsuccessful')
        response = redirect(url_for('auth_views.login_page'))

    return response

#200 and 500 necessary for HTTP status 
@alumni_views.route('/update_modal_window', methods=['POST'])
@jwt_required()
def modal_window():
    try:
        alumni = current_user  
        set_modal_window(alumni.alumni_id)  
        db.session.commit() 
        return jsonify(message="Update successful."), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(message="Server error when updating modal."), 500
	