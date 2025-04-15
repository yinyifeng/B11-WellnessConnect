from extensions import db
from datetime import datetime

from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
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


class HealthTracking(db.Model):
    __tablename__ = 'health_tracking'

    id = db.Column(db.Integer, primary_key=True)
    
    ounces_water = db.Column(db.Float)      
    num_steps = db.Column(db.Integer)    
    activity_type = db.Column(db.String(100)) 
    hours_sleep = db.Column(db.Float)
    proof = db.Column(db.Boolean, default=False)
    proof_valid = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def addWater(self, ounces_water, proof=False):
        self.gallons_water = (self.gallons_water or 0) + ounces_water
        self.proof = proof
        return self.ounces_water

    def addSteps(self, num_steps, proof=False):
        self.num_steps = (self.num_steps or 0) + num_steps
        self.proof = proof
        return self.num_steps

    def addActivity(self, activity_type, proof=False):
        self.activity_type = activity_type
        self.proof = proof
        return {"activity": self.activity_type, "proof": self.proof}

    def addSleep(self, hours, proof=False):
        self.hours_sleep = (self.hours_sleep or 0) + hours
        self.proof = proof
        return self.hours_sleep
