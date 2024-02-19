from flask import Flask, render_template, request, send_from_directory, send_file, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from docx import Document
from pptx import Presentation
from PIL import Image
from io import BytesIO
import base64
import fitz
import yadisk

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'your_secret_key_here'

# Класс для хранения информации о пользователе
class User(UserMixin):
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

# Функция для загрузки информации о пользователях из текстовых файлов
def load_users():
    users_file = 'users.txt'
    users = {}
    with open(users_file, 'r') as f:
        for line in f:
            # Игнорировать пустые строки
            if not line.strip():
                continue
            # Попытка разделить строку на две части
            parts = line.strip().split(':')
            # Проверка наличия двух частей
            if len(parts) != 2:
                continue
            key, value = parts
            users[key.strip()] = value.strip()
    return users


# Функция для сохранения информации о пользователе на Яндекс.Диск
def save_user_to_yadisk(user):
    with yadisk.YaDisk(token="your_yadisk_token") as y:
        with y.upload(user.username + ".txt", overwrite=True) as f:
            f.write(f"username:{user.username}\npassword:{user.password}\nrole:{user.role}")

# Функция для загрузки информации о пользователе с Яндекс.Диска
def load_user_from_yadisk(username):
    with yadisk.YaDisk(token="your_yadisk_token") as y:
        with y.download(username + ".txt") as f:
            user_info = {}
            for line in f:
                key, value = line.strip().split(':')
                user_info[key] = value
            return User(user_info['username'], user_info['password'], user_info['role'])

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user.password == password:
            login_user(user)
            if user.role == 'teacher':
                return redirect(url_for('teacher_index'))
            elif user.role == 'student':
                return redirect(url_for('student_index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/teacher')
@login_required
def teacher_index():
    return render_template('teacher_index.html')

@app.route('/student')
@login_required
def student_index():
    return render_template('student_index.html')

if __name__ == '__main__':
    app.run()
