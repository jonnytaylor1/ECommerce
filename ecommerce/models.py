from ecommerce import db, login_manager
from flask_login import UserMixin


# T-shirt Model
class TShirt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tshirt_details = db.Column(db.JSON, nullable=False)

    def __init__(self, tshirt_details):
        self.tshirt_details = tshirt_details

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    firstName = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


    def __init__(self, firstName, surname, email, password):
        self.firstName = firstName
        self.surname = surname
        self.email = email
        self.password = password


 #Gets the user Id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
