from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image, ImageDraw
import io
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    lesson_1 = db.Column(db.Boolean, default=False)
    lesson_2 = db.Column(db.Boolean, default=False)
    lesson_3 = db.Column(db.Boolean, default=False)
    lesson_4 = db.Column(db.Boolean, default=False)
    lesson_5 = db.Column(db.Boolean, default=False)
    lesson_6 = db.Column(db.Boolean, default=False)
    lesson_7 = db.Column(db.Boolean, default=False)
    lesson_8 = db.Column(db.Boolean, default=False)
    lesson_9 = db.Column(db.Boolean, default=False)
    lesson_10 = db.Column(db.Boolean, default=False)
    lesson_11 = db.Column(db.Boolean, default=False)
    lesson_12 = db.Column(db.Boolean, default=False)
    lesson_13 = db.Column(db.Boolean, default=False)
    lesson_14 = db.Column(db.Boolean, default=False)
    lesson_15 = db.Column(db.Boolean, default=False)
    lesson_16 = db.Column(db.Boolean, default=False)
    lesson_17 = db.Column(db.Boolean, default=False)
    lesson_18 = db.Column(db.Boolean, default=False)
    lesson_19 = db.Column(db.Boolean, default=False)
    lesson_20 = db.Column(db.Boolean, default=False)
    lesson_21 = db.Column(db.Boolean, default=False)
    lesson_22 = db.Column(db.Boolean, default=False)
    lesson_23 = db.Column(db.Boolean, default=False)
    lesson_24 = db.Column(db.Boolean, default=False)
    lesson_25 = db.Column(db.Boolean, default=False)
    lesson_26 = db.Column(db.Boolean, default=False)
    lesson_27 = db.Column(db.Boolean, default=False)
    lesson_28 = db.Column(db.Boolean, default=False)
    lesson_29 = db.Column(db.Boolean, default=False)
    lesson_30 = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def home():
    return "Welcome to the Tracking App!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    lessons = Lesson.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', lessons=lessons)

@app.route('/add_lesson', methods=['GET', 'POST'])
@login_required
def add_lesson():
    if request.method == 'POST':
        date = request.form.get('date')
        lesson_data = {}
        for i in range(1, 31):
            lesson_key = f'lesson_{i}'
            lesson_data[lesson_key] = lesson_key in request.form

        try:
            new_lesson = Lesson(user_id=current_user.id, date=date, **lesson_data)
            db.session.add(new_lesson)
            db.session.commit()
            flash('Lesson added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding lesson: {e}', 'danger')
            return redirect(url_for('add_lesson'))
        
        return redirect(url_for('dashboard'))
    return render_template('add_lesson.html')



@app.route('/view_report')
@login_required
def view_report():
    lessons = Lesson.query.filter_by(user_id=current_user.id).all()

    checks = {f'lesson_{i}': any(getattr(lesson, f'lesson_{i}') for lesson in lessons) for i in range(1, 31)}
    
    input_image_path = os.path.join(app.root_path, 'trackingImage.png')
    output_image_path = os.path.join(app.root_path, 'marked_trackingImage.png')
    mark_checkbox(input_image_path, output_image_path, checks)

    return send_file(output_image_path, mimetype='image/png')

@app.route('/download_report')
@login_required
def download_report():
    lessons = Lesson.query.filter_by(user_id=current_user.id).all()

    checks = {f'lesson_{i}': any(getattr(lesson, f'lesson_{i}') for lesson in lessons) for i in range(1, 31)}
    
    input_image_path = os.path.join(app.root_path, 'trackingImage.png')
    output_image_path = os.path.join(app.root_path, 'marked_trackingImage.png')
    mark_checkbox(input_image_path, output_image_path, checks)

    return send_file(output_image_path, mimetype='image/png', download_name='report.png')

def mark_checkbox(image_path, output_path, checks):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    coordinates = {
        'lesson_1': [(63, 225), (84, 245)],
        'lesson_2': [(63, 285), (84, 305)],
        # Diğer dersler için koordinatları ekleyin
        'lesson_30': [(63, 1425), (84, 1445)],
    }

    for key, coord in coordinates.items():
        if checks.get(key, False):
            x1, y1 = coord[0]
            x2, y2 = coord[1]
            draw.rectangle([x1, y1, x2, y2], fill="black")

    image.save(output_path)

if __name__ == '__main__':
    app.run(debug=True)
