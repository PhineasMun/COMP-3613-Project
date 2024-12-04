from App.database import db
from .user import User

class Employee(User):
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    # Relationship with Company (M-1)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    company = db.relationship('Company', back_populates='employees')

    def __init__(self, username, password, email, employee_id, first_name, last_name, department):
        super().__init__(username, password, email)
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'employeeid': self.employee_id,
            'firstname': self.first_name,
            'lastname': self.last_name,
            'department': self.department
        }

    def get_employee_id(self):
        return self.employee_id

