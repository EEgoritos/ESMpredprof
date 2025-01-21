from flask import Flask, render_template, redirect, url_for, flash, session as flask_session, request
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from database import global_init, create_session
from models.user import User
import os
db_path = os.path.join(os.path.dirname(__file__), 'site.db')
global_init(db_path)

app = Flask(__name__)
app.secret_key = "your_secret_key"




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Работа с базой данных
        session = create_session()
        if session.query(User).filter((User.username == username) | (User.email == email)).first():
            flash('Пользователь с таким именем или email уже существует.')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=hashed_password)
        session.add(new_user)
        session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        session = create_session()
        user = session.query(User).filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flask_session['user_id'] = user.id
            flash('Вы успешно вошли в систему!')
            return redirect(url_for('dashboard'))

        flash('Неверный email или пароль.')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in flask_session:
        flash('Сначала войдите в систему.')
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    flask_session.pop('user_id', None)
    flash('Вы вышли из системы.')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)