from extensions import db
from datetime import datetime

from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    primary_phone_number = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    profile_picture = db.Column(db.String(255))
    points_balance = db.Column(db.Integer, default=0)
    streak_count = db.Column(db.Integer, default=0)
    
    role = db.Column(Enum("Customer", "SystemAdmin", "CompanyAdmin", name="user_roles"),
                     nullable=False, default="Customer")

    def __repr__(self):
        return "<User {}>".format(self.email)


class ActivityLog(db.Model):
    __tablename__ = 'activity_log'

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)

    activity_type = db.Column(
        Enum('water', 'steps', 'exercise', 'sleep', name='activity_type_enum'),
        nullable=False
    )
    value = db.Column(db.Numeric, nullable=False)

    unit = db.Column(
        Enum('oz', 'steps', 'miles', 'hours', 'min', 'km', name='unit_enum'),
        nullable=True
    )

    exercise_type = db.Column(
        Enum('yoga', 'run', 'cycling', 'strength', name='exercise_type_enum'),
        nullable=True
    )

    proof = db.Column(db.Boolean, default=False)
    proof_valid = db.Column(db.Boolean, nullable=True)
    proof_url = db.Column(db.String(255), nullable=True)

    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    def addWater(self, ounces_water, proof=False):
        self.activity_type = 'water'
        self.value = ounces_water
        self.unit = 'oz'
        self.exercise_type = None
        self.proof = proof
        self.proof_valid = None if proof else False
        return self.value

    def addSteps(self, num_steps, proof=False):
        self.activity_type = 'steps'
        self.value = num_steps
        self.unit = 'steps'
        self.exercise_type = None
        self.proof = proof
        self.proof_valid = None if proof else False
        return self.value

    def addActivity(self, activity_type, value, unit=None, exercise_type=None, proof=False):
        self.activity_type = activity_type
        self.value = value
        self.unit = unit
        self.exercise_type = exercise_type
        self.proof = proof
        self.proof_valid = None if proof else False
        return {
            "activity": self.activity_type,
            "exercise_type": self.exercise_type,
            "value": self.value,
            "unit": self.unit,
            "proof": self.proof
        }

    def addSleep(self, hours, proof=False):
        self.activity_type = 'sleep'
        self.value = hours
        self.unit = 'hours'
        self.exercise_type = None
        self.proof = proof
        self.proof_valid = None if proof else False
        return self.value

