from flask import Flask, request, render_template, redirect, url_for, session, flash
import hashlib, os, uuid
from extensions import db
from schema import User
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'b11_secret_key'

# Setup SQLAlchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yinyi:1234@localhost/wellnessconnect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup for uploading profile pictures
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'profile_pics')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # limit file size to 2MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_filetype(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)

@app.route('/')
def start_app():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return render_template('index.html', error="Missing email or password.")

    hashed_password = hashlib.md5(password.encode()).hexdigest()

    user = User.query.filter_by(email=email, password=hashed_password).first()

    if user:
        session['email'] = email
        session['role'] = user.role

        if user.role == 'SystemAdmin':
            return render_template('admin_homepage.html', user=user)
        elif user.role == 'CompanyAdmin':
            return render_template('companyAdmin_homepage.html', user=user)
        else:
            return render_template('homepage.html', user=user)
    else:
        return render_template('index.html', error=True)  # Invalid login

@app.route('/user_register')
def user_register():
    return render_template('user_register.html')

@app.route('/userRegisterAuth', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    phone = request.form['primary_phone_number']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = datetime.strptime(request.form['date_of_birth'], "%Y-%m-%d")

    existing_user = User.query.filter(func.lower(User.email) == email.lower()).first()
    if existing_user:
        flash('An account with that email already exists.')
        return redirect(url_for('user_register'))

    new_user = User(
        email=email,
        password=hashed_password,
        primary_phone_number=phone,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=dob
    )

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('start_app'))


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/account_dashboard')
def account_dashboard():
    if 'email' not in session:
        return redirect(url_for('start_app'))

    user = User.query.filter_by(email=session['email']).first()
    return render_template("account.html", user=user)

@app.route('/admin_homepage')
def admin_homepage():
    if 'email' not in session:
        return redirect(url_for('start_app'))

    user = User.query.filter_by(email=session['email']).first()
    return render_template("admin_homepage.html", user=user)

@app.route('/admin_account')
def admin_account():
    if 'email' not in session:
        return redirect(url_for('start_app'))

    user = User.query.filter_by(email=session['email']).first()
    return render_template("admin_account.html", user=user)

@app.route('/companyAdmin_homepage')
def companyAdmin_homepage():
    if 'email' not in session:
        return redirect(url_for('start_app'))

    user = User.query.filter_by(email=session['email']).first()
    return render_template("companyAdmin_homepage.html", user=user)

@app.route('/companyAdmin_account')
def companyAdmin_account():
    if 'email' not in session:
        return redirect(url_for('start_app'))

    user = User.query.filter_by(email=session['email']).first()
    return render_template("companyAdmin_account.html", user=user)

@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'email' not in session:
        return redirect(url_for('start_app'))

    file = request.files.get('profile_pic')
    if not file or file.filename == '':
        flash('No file selected')
        return redirect(url_for('account_dashboard'))

    if not allowed_filetype(file.filename):
        flash('Invalid file type')
        return redirect(url_for('account_dashboard'))

    filename = secure_filename(file.filename)
    unique_name = "{}_{}".format(uuid.uuid4().hex, filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)

    file.save(save_path)

    user = User.query.filter_by(email=session['email']).first()
    user.profile_picture = "profile_pics/{}".format(unique_name)
    db.session.commit()

    return redirect(url_for('account_dashboard'))

@app.route('/remove_profile_pic', methods=['POST'])
def remove_profile_pic():
    if 'email' not in session:
        return redirect(url_for('start_app'))

    user = User.query.filter_by(email=session['email']).first()
    if user.profile_picture:
        pic_path = os.path.join(app.static_folder, user.profile_picture)
        if os.path.exists(pic_path):
            os.remove(pic_path)

        user.profile_picture = None
        db.session.commit()
    return redirect(url_for('account_dashboard'))

from werkzeug.exceptions import RequestEntityTooLarge

@app.errorhandler(RequestEntityTooLarge)
def large_file_handler(error):
    flash("File too large. Please upload a file smaller than 2MB")
    return redirect(url_for('account_dashboard'))

@app.route('/activity_tracker')
def activity_tracker():
    return render_template('activity.html')

@app.route('/vouchers')
def vouchers():
    return render_template('vouchers.html')

@app.route('/reminders')
def reminders():
    return render_template('reminders.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
