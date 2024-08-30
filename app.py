from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from os import urandom

app = Flask(__name__)

app.secret_key = urandom(24)

# Configuration for the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://joelmunoz:mypassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


# Define a model to represent the data
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)


# Create the database tables
with app.app_context():
    db.create_all()


# Define the route for the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Check if the email already exists
        existing_user = Users.query.filter_by(email=email).first()

        if existing_user:
            # Handle the case where the user already exists
            flash(f'User with email {email} already exists!', 'error')
            return redirect('/')

        new_user = Users(name=name, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while adding the user.', 'error')
            return redirect('/')

        flash('User added successfully!', 'success')
        return redirect('/')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
