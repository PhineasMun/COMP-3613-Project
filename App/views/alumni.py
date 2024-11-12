from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db

from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from .index import index_views


from App.controllers import(
    get_user_by_username,
    is_alumni_subscribed,
    subscribe,
    unsubscribe
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
    data = request.form
    response = None

    try:
        alumni = subscribe(current_user.alumni_id, data['category'])
        response = redirect(url_for('index_views.index_page'))
        flash('Subscribed!', 'success')

    except Exception:
        flash('Error subscribing', 'unsuccessful')
        response = redirect(url_for('auth_views.login_page'))

    return response

@alumni_views.route('/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe_action():
    response = None

    try:
        alumni = unsubscribe(current_user.alumni_id)
        response = redirect(url_for('index_views.index_page'))
        flash('Unsubscribed!', 'success')

    except Exception:
        flash('Error unsubscribing', 'unsuccessful')
        response = redirect(url_for('auth_views.login_page'))

    return response