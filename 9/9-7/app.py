# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему для доступа к этой странице.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Функция для получения пользователя по ID
def get_user_by_id(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user


# Главная страница
@app.route('/')
def index():
    if 'user_id' in session:
        user = get_user_by_id(session['user_id'])
        return render_template('dashboard.html', user=user)
    return render_template('index.html')


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Валидация
        if not username or not email or not password:
            flash('Все поля обязательны для заполнения', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов', 'error')
            return render_template('register.html')

        # Проверка уникальности
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if c.fetchone():
            flash('Пользователь с таким именем или email уже существует', 'error')
            conn.close()
            return render_template('register.html')

        # Создание пользователя
        password_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                  (username, email, password_hash))
        conn.commit()
        conn.close()

        flash('Регистрация прошла успешно! Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash(f'Добро пожаловать, {user[1]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')

    return render_template('login.html')


# Выход
@app.route('/logout')
def logout():
    session.clear()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('index'))


# Профиль пользователя
@app.route('/profile')
@login_required
def profile():
    user = get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)


# Редактирование профиля
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Валидация
        if not username or not email:
            flash('Имя пользователя и email обязательны', 'error')
            return redirect(url_for('edit_profile'))

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Проверка уникальности имени и email (исключая текущего пользователя)
        c.execute('SELECT id FROM users WHERE (username = ? OR email = ?) AND id != ?',
                  (username, email, session['user_id']))
        if c.fetchone():
            flash('Пользователь с таким именем или email уже существует', 'error')
            conn.close()
            return redirect(url_for('edit_profile'))

        # Если пользователь хочет изменить пароль
        if new_password:
            if len(new_password) < 6:
                flash('Новый пароль должен содержать минимум 6 символов', 'error')
                conn.close()
                return redirect(url_for('edit_profile'))

            if new_password != confirm_password:
                flash('Новые пароли не совпадают', 'error')
                conn.close()
                return redirect(url_for('edit_profile'))

            # Проверка текущего пароля
            c.execute('SELECT password_hash FROM users WHERE id = ?', (session['user_id'],))
            current_hash = c.fetchone()[0]

            if not check_password_hash(current_hash, current_password):
                flash('Неверный текущий пароль', 'error')
                conn.close()
                return redirect(url_for('edit_profile'))

            # Обновление с новым паролем
            new_password_hash = generate_password_hash(new_password)
            c.execute('UPDATE users SET username = ?, email = ?, password_hash = ? WHERE id = ?',
                      (username, email, new_password_hash, session['user_id']))
            flash('Профиль и пароль успешно обновлены!', 'success')
        else:
            # Обновление без изменения пароля
            c.execute('UPDATE users SET username = ?, email = ? WHERE id = ?',
                      (username, email, session['user_id']))
            flash('Профиль успешно обновлен!', 'success')

        # Обновление сессии
        session['username'] = username

        conn.commit()
        conn.close()

        return redirect(url_for('profile'))

    user = get_user_by_id(session['user_id'])
    return render_template('edit_profile.html', user=user)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)