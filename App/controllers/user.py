from App.models import User, Admin, Alumni, Employee
from App.database import db

# from sqlalchemy.orm import with_polymorphic

def create_user(username, password, email):
    newuser = User(username=username, password=password, email=email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    # return User.query.filter_by(username=username).first()
    user = None
#   user = User.query.filter_by(username=data['username']).first()
    alumni = Alumni.query.filter_by(username=username).first()
    if alumni:
        user = alumni
    admin = Admin.query.filter_by(username=username).first()
    if admin:
        user = admin
    employee = Employee.query.filter_by(username=username).first()
    if employee:
        user = employee
    
    return user

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return db.session.query(Admin).all() + db.session.query(Alumni).all() + db.session.query(Employee).all()
    # return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    from App.models import User, Admin, Alumni, Employee
from App.database import db

# from sqlalchemy.orm import with_polymorphic

def create_user(username, password, email):
    newuser = User(username=username, password=password, email=email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    # return User.query.filter_by(username=username).first()
    user = None
#   user = User.query.filter_by(username=data['username']).first()
    alumni = Alumni.query.filter_by(username=username).first()
    if alumni:
        user = alumni
    admin = Admin.query.filter_by(username=username).first()
    if admin:
        user = admin
    employee = Employee.query.filter_by(username=username).first()
    if employee:
        user = employee
    
    return user

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return db.session.query(Admin).all() + db.session.query(Alumni).all() + db.session.query(Employee).all()
    # return User.query.all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    