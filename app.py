from flask import Flask, render_template, request, send_from_directory
import os
from docx import Document
from pptx import Presentation
from PIL import Image
from io import BytesIO
import base64
import fitz
import PyPDF2
from wand.image import Image as WandImage

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
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






if __name__ == '__main__':
    app.run(debug=True)
