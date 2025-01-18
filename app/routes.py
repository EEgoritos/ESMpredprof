from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from .models import User, Sheet
from .utils import recognize_notes, create_midi, convert_to_audio
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import login_manager

main = Blueprint('main', __name__)


# Регистрация user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/')
def home():
    return render_template('index.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))


@main.route('/dashboard')
@login_required
def dashboard():
    sheets = Sheet.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', sheets=sheets)


@main.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('main.dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('main.dashboard'))
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        notes = recognize_notes(filepath)
        midi_path = os.path.join(current_app.config['AUDIO_FOLDER'], f"{filename}.mid")
        audio_path = os.path.join(current_app.config['AUDIO_FOLDER'], f"{filename}.wav")
        create_midi(notes, midi_path)
        convert_to_audio(midi_path, audio_path)

        sheet = Sheet(filename=filename, audio_filename=f"{filename}.wav", user_id=current_user.id)
        db.session.add(sheet)
        db.session.commit()
        flash('File uploaded and processed successfully!', 'success')
    return redirect(url_for('main.dashboard'))


@main.route('/audio/<filename>')
@login_required
def download_audio(filename):
    return send_from_directory(current_app.config['AUDIO_FOLDER'], filename)


@main.route('/profile')
@login_required
def profile():
    sheets = Sheet.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', sheets=sheets)
