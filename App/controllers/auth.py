from flask_jwt_extended import create_access_token,set_access_cookies, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User, Admin, Alumni, Company, Listing
from App.controllers import get_user_by_username

from flask import jsonify

def login_user(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
      token = create_access_token(identity=username)
      response = jsonify(access_token=token)
      set_access_cookies(response, token)
      return response
    return None

def login(username, password):
  user = get_user_by_username(username)
  
  if user and user.check_password(password):
    token = create_access_token(identity=username)
    print('token created')
    return (token)
  return None


def setup_jwt(app):
  jwt = JWTManager(app)

  # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    admin = Admin.query.filter_by(username=identity).one_or_none()
    if admin:
      return admin.username

    alumni = Alumni.query.filter_by(username=identity).one_or_none()
    if alumni:
      return alumni.username

    company = Company.query.filter_by(username=identity).one_or_none()
    if company:
      return company.username

    return None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]

    admin = Admin.query.filter_by(username=identity).one_or_none()
    if admin:
      return admin

    alumni = Alumni.query.filter_by(username=identity).one_or_none()
    if alumni:
      return alumni

    company = Company.query.filter_by(username=identity).one_or_none()
    if company:
      return company
  return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          username = get_jwt_identity()
          current_user = get_user_by_username(username)
          is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)