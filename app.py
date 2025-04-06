from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2
import hashlib

app = Flask(__name__)
app.secret_key = 'b11_secret_key'

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="wellnessconnect",
    user="yinyi",
    password="1234"
)
cur = conn.cursor()

@app.route('/')
def start_app():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, hashed_password))
    user = cur.fetchone()

    if user:
        session['email'] = email
        return render_template('homepage.html')
    else:
        return render_template('index.html', error=True)

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
    dob = request.form['date_of_birth']

    cur.execute("""
        INSERT INTO users (email, password, primary_phone_number, first_name, last_name, date_of_birth)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (email, hashed_password, phone, first_name, last_name, dob))

    conn.commit()
    return redirect(url_for('start_app'))


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/account_dashboard')
def account_dashboard():
    if 'email' not in session:
        return redirect(url_for('start_app'))

    cur.execute("SELECT first_name, last_name, primary_phone_number FROM users WHERE email=%s", (session['email'],))
    user = cur.fetchone()

    return render_template("account.html", 
                           first_name=user[0], 
                           last_name=user[1],
                           phone=user[2],
                           email=session['email'])

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

if __name__ == '__main__':
    app.run(debug=True)
