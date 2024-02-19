from flask import Flask, render_template, request, send_from_directory, send_file, url_for, redirect, session
import os
from docx import Document
from pptx import Presentation
from PIL import Image
from io import BytesIO
import base64
import fitz

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'

# Простой список пользователей и их паролей
TEACHER_USERS = {'teacher1': 'password1', 'teacher2': 'password2'}
STUDENT_USERS = {'student1': 'password1', 'student2': 'password2'}

# Функция для аутентификации пользователя
def authenticate(username, password, user_type):
    if user_type == 'teacher':
        users = TEACHER_USERS
    elif user_type == 'student':
        users = STUDENT_USERS
    
    if username in users and users[username] == password:
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if filename.endswith('.docx'):
                text = process_word(file_path)
                return render_template('word_template.html', text=text, filename=filename) 
            
            elif filename.endswith('.pdf'):
                filename, images = process_pdf(file_path)
                return render_template('pdf_template.html', filename=filename, images=images)
            
            elif filename.endswith('.pptx'):
                slides_data = process_pptx(file_path)
                return render_template('pptx_template.html', slides=slides_data, filename=filename)
            
            else:
                text = "Unsupported file format"
                slides_data = [{"text": text, "images": []}]
                return render_template('pptx_template.html', slides=slides_data, filename=filename)
            
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        if authenticate(username, password, user_type):
            session['username'] = username
            session['user_type'] = user_type
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

@app.route('/clear_data', methods=['GET'])
def clear_data():
    if request.args.get('key') == 'clear_all_data':
        y.remove('/uploads')
        return "Data cleared successfully."
    else:
        return "Invalid key."

@app.route('/open_from_yadisk/<path:file_path>')
def open_from_yadisk(file_path):
    temp_file = f"temp_{os.path.basename(file_path)}"
    with open(temp_file, "wb") as f:
        y.download(file_path, f)

    return send_file(temp_file, as_attachment=True)

@app.route('/files', methods=['GET'])
def list_files():
    yadisk_files = list_files_on_yadisk('/uploads')
    return render_template('files.html', files=yadisk_files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def process_word(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

def process_pdf(file_path):
    images = []
    filename = os.path.basename(file_path)
    with fitz.open(file_path) as pdf:
        for page in pdf:
            pixmap = page.get_pixmap(alpha=True)
            img = Image.frombytes("RGBA", [pixmap.width, pixmap.height], pixmap.samples)
            image_stream = BytesIO()
            img.save(image_stream, format="PNG")
            image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
            images.append(image_base64)
    return filename, images

def process_pptx(file_path):
    presentation = Presentation(file_path)
    slides_data = []
    for slide in presentation.slides:
        slide_data = {"text": "", "images": []}
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_data["text"] += shape.text + "\n"
            elif shape.shape_type == 13:
                image_stream = BytesIO()
                img = shape.image
                img_bytes = img.blob
                image_stream.write(img_bytes)
                image_data = base64.b64encode(image_stream.getvalue()).decode('utf-8')
                slide_data["images"].append(image_data)
        slides_data.append(slide_data)
    return slides_data

if __name__ == '__main__':
  app.run()
  
  
  
#  project_folder/ 
# ├── templates/
# │   ├── files.html
# │   ├── index.html
# │   ├── pdf_template.html
# │   ├── pptx_template.html
# │   ├── result.html
# │   ├── word_template.html
# │   └── teacher_index.html
# ├── app.py
# ├── README.md
# └── TODO