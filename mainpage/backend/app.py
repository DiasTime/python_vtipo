from flask import Flask, render_template, request
import os
from docx import Document

app = Flask(__name__)

# Путь к папке, где будут сохраняться документы
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Страница добавления курсов
@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        # Получаем загруженный файл
        file = request.files['file']
        if file:
            # Сохраняем файл
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Парсим документ и извлекаем лекции
            lectures = parse_document(filepath)
            return render_template('show_lectures.html', lectures=lectures)
    return render_template('add_course.html')

# Функция для парсинга документа Word
def parse_document(filepath):
    doc = Document(filepath)
    lectures = []
    lecture = {'title': '', 'content': ''}
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith('<TITLE>'):
            lecture['title'] = paragraph.text.replace('<TITLE>', '').replace('</TITLE>', '')
        elif paragraph.text.startswith('<LECTURE>'):
            lecture['content'] = paragraph.text.replace('<LECTURE>', '').replace('</LECTURE>', '')
            lectures.append(lecture.copy())
            lecture = {'title': '', 'content': ''}
    return lectures

if __name__ == '__main__':
    app.run(debug=True)
