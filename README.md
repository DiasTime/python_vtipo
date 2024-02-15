ЧТОБЫ ОЧИСТИТЬ ВСЕ ДАННЫЕ ТО-ЕСТЬ УДОЛИТЬ ВСЕ ФАЙЛЫ
ВВЕДИТЕ КОМАНДУ curl http://127.0.0.1:5000/clear_data?key=clear_all_data
ВНИМАНИЕ ПОСЛЕ УДАЛЕНИЯ ФАЙЛЫ НЕЛЬЗЯ БУДЕТ ВОСТОНАВИТЬ!!!!!!!!!!!!!!!





README (Russian):

# Описание проекта

Этот проект представляет собой веб-приложение на Python с использованием Flask, которое позволяет загружать файлы .docx, .pdf и .pptx для их обработки и отображения результатов в браузере.

## Установка

1. Установите необходимые зависимости, выполнив следующую команду:
   ```
   pip install flask python-docx python-pptx pillow wand
   ```

2. Клонируйте репозиторий:
   ```
   git clone https://github.com/your_username/your_project.git
   ```

3. Перейдите в каталог проекта:
   ```
   cd your_project
   ```

4. Запустите приложение:
   ```
   python app.py
   ```

## ВСЕ PIP INSTALLЫ

pip install Flask
pip install python-docx
pip install python-pptx
pip install Pillow
pip install PyMuPDF
pip install Wand










## Использование

1. Запустите приложение и откройте браузер.
2. Перейдите по адресу http://127.0.0.1:5000/.
3. Загрузите файл, нажав на соответствующую кнопку.
4. Результаты обработки файла будут отображены на странице.

## Дополнительные сведения

- Это приложение поддерживает обработку файлов форматов .docx, .pdf и .pptx.
- Результаты обработки файлов .docx отображаются в HTML-шаблоне.
- Результаты обработки файлов .pdf отображаются в виде изображений на странице.
- Результаты обработки файлов .pptx отображаются в виде слайдов на странице.

---

README (English):

# Project Description

This project is a Python web application using Flask that allows uploading .docx, .pdf, and .pptx files for processing and displaying the results in the browser.

## Installation

1. Install the required dependencies by executing the following command:
   ```
   pip install flask python-docx python-pptx pillow wand
   ```

2. Clone the repository:
   ```
   git clone https://github.com/your_username/your_project.git
   ```

3. Navigate to the project directory:
   ```
   cd your_project
   ```

4. Run the application:
   ```
   python app.py
   ```

## Usage

1. Run the application and open a web browser.
2. Go to http://127.0.0.1:5000/.
3. Upload a file by clicking on the corresponding button.
4. The processing results of the file will be displayed on the page.

## Additional Information

- This application supports processing of .docx, .pdf, and .pptx files.
- The processing results of .docx files are displayed in an HTML template.
- The processing results of .pdf files are displayed as images on the page.
- The processing results of .pptx files are displayed as slides on the page.
