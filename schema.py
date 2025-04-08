from extensions import db

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

    def __repr__(self):
        return "<User {}>".format(self.email)
