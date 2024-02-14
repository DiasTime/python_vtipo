from flask import Flask, render_template, request, send_from_directory,send_file
import os
from docx import Document
from pptx import Presentation
from PIL import Image
from io import BytesIO
import base64
import fitz
import PyPDF2
from wand.image import Image as WandImage
import yadisk
import mysql.connector
import tempfile
from flask import Flask, render_template, request, send_from_directory, url_for



app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Подключение к MySQL базе данных
db = mysql.connector.connect(
    host="127.0.0.1",
    user="dias",
    password="3418",
    database="files"
)
cursor = db.cursor()

# Токен для доступа к Яндекс.Диску
y = yadisk.YaDisk(token="y0_AgAAAAAl5jRpAAtKfAAAAAD6_t3BAABRqHACUIJMrJ4PRAckXHu7iVOojw")

def list_files_on_yadisk(folder_path):
    files = y.listdir(folder_path)
    # Преобразуем генератор в список кортежей
    files_list = [(file.name, file.path) for file in files]
    return files_list


# Получение списка файлов из базы данных
def list_files_from_database():
    cursor.execute("SELECT * from files")
    files = cursor.fetchall()
    return files

# Функция для сохранения файла на Яндекс.Диск
def save_to_yadisk(file_path):
    # Проверяем, начинается ли имя файла с префикса temp_
    if not os.path.basename(file_path).startswith('temp_'):
        # Если имя файла не начинается с префикса temp_, загружаем его на Яндекс.Диск
        y.upload(file_path, f'/uploads/{os.path.basename(file_path)}')


@app.route('/', methods=['GET', 'POST'])
def index():
    yadisk_files = list_files_on_yadisk('/uploads')
    db_files = list_files_from_database()

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename

            # Проверяем, есть ли файл уже на Яндекс.Диске
            existing_file = next((f for f in yadisk_files if f[1] == filename), None)
            if existing_file:
                # Если файл уже есть на Яндекс.Диске, создаем ссылку на него
                file_url = url_for('open_from_yadisk', file_path=existing_file[1])
            else:
                # Если файла нет на Яндекс.Диске, сохраняем его туда
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                # Проверяем, начинается ли имя файла с префикса temp_
                if not filename.startswith('temp_'):
                    # Если нет, добавляем информацию о файле в базу данных
                    save_to_yadisk(file_path)
                    cursor.execute("INSERT INTO files (filename, file_path) VALUES (%s, %s)", (filename, file_path))
                    db.commit()

                    file_url = url_for('open_from_yadisk', file_path=f'/uploads/{filename}')
                else:
                    # Если имя файла начинается с префикса temp_, не добавляем его в базу данных
                    file_url = None

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
            
    return render_template('index.html', yadisk_files=yadisk_files, db_files=db_files)





@app.route('/open_from_yadisk/<path:file_path>')
def open_from_yadisk(file_path):
    temp_file = f"temp_{os.path.basename(file_path)}"
    with open(temp_file, "wb") as f:
        y.download(file_path, f)

    return send_file(temp_file, as_attachment=True)

@app.route('/open_from_db/<path:file_path>')
def open_from_db(file_path):
    encodings = ['utf-8', 'latin-1']  # список возможных кодировок
    for encoding in encodings:
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read().decode(encoding)
            return file_data
        except UnicodeDecodeError:
            continue
    return "Failed to decode file"

@app.route('/files', methods=['GET'])
def list_files():
    cursor.execute("SELECT id, filename, file_path FROM files")
    files = cursor.fetchall()
    return render_template('files.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/apply_style', methods=['GET'])
def apply_style():
    style = request.args.get('style')
    text = request.args.get('text')
    return render_template('result.html', text=text, css_file=style)

def process_word(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

def process_pdf(file_path):
    images = []
    filename = os.path.basename(file_path)  # Получаем имя файла из пути
    with fitz.open(file_path) as pdf:
        for page in pdf:
            # Получаем изображение страницы PDF в формате RGBA
            pixmap = page.get_pixmap(alpha=True)
            # Создаем объект Image из библиотеки PIL на основе pixmap
            img = Image.frombytes("RGBA", [pixmap.width, pixmap.height], pixmap.samples)
            # Создаем объект BytesIO для записи изображения
            image_stream = BytesIO()
            # Сохраняем изображение в формате PNG в объект BytesIO
            img.save(image_stream, format="PNG")
            # Получаем данные изображения в виде байтовой строки
            image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')
            # Добавляем закодированное изображение в список
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
            elif shape.shape_type == 13:  # Код 13 означает изображение
                image_stream = BytesIO()
                img = shape.image
                img_bytes = img.blob
                image_stream.write(img_bytes)
                image_data = base64.b64encode(image_stream.getvalue()).decode('utf-8')
                slide_data["images"].append(image_data)
        slides_data.append(slide_data)
    return slides_data

if __name__ == '__main__':
    app.run(debug=True)
