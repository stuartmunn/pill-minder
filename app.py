import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dosage = db.Column(db.String(100))
    time = db.Column(db.String(100))
    taken = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    medications = Medication.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', medications=medications)

@app.route('/add_medication', methods=['POST'])
@login_required
def add_medication():
    name = request.form['name']
    dosage = request.form['dosage']
    time = request.form['time']
    new_medication = Medication(name=name, dosage=dosage, time=time, user_id=current_user.id)
    db.session.add(new_medication)
    db.session.commit()
    schedule_medication(new_medication)
    return redirect(url_for('index'))

@app.route('/update_medication/<int:medication_id>', methods=['POST'])
@login_required
def update_medication(medication_id):
    medication = Medication.query.get(medication_id)
    medication.taken = not medication.taken
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/delete_medication/<int:medication_id>')
@login_required
def delete_medication(medication_id):
    medication = Medication.query.get(medication_id)
    db.session.delete(medication)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'change_username':
            new_username = request.form['username']
            current_user.username = new_username
            db.session.commit()
            flash('Username changed successfully')
        elif action == 'change_password':
            new_password = request.form['password']
            confirm_password = request.form['confirm_password']
            if new_password == confirm_password:
                current_user.password = new_password
                db.session.commit()
                flash('Password changed successfully')
            else:
                flash('Passwords do not match')
        return redirect(url_for('settings'))
    return render_template('settings.html')

@app.route('/bnf_lookup')
@login_required
def bnf_lookup():
    query = request.args.get('query')
    url = f"https://bnf.nice.org.uk/search/?q={query}"
    # This is a simplified example. A real implementation would need to parse the HTML response.
    # For now, we'll just return a link.
    return jsonify({'url': url})

def schedule_medication(med):
    print(f"Scheduling notification for medication {med.name} at {med.time}")
    # This is a simplified scheduler. A real implementation would parse the time properly.
    # scheduler.add_job(send_telegram_notification, 'cron', hour=med.time.split(":")[0], minute=med.time.split(":")[1], args=[med.user_id, med.id, med.name])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.start()

    app.run(host='0.0.0.0', port=5000)