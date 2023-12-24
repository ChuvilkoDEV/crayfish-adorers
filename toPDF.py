import os
import io
from docx2pdf import convert
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from docx import Document
from typing import Dict, Any, List


def convert_docx_to_pdf(file_path: str):
    """
    Конвертирует один файл формата DOCX в PDF.

    :param file_path: Путь к файлу DOCX, который необходимо конвертировать.
    """
    try:
        # Извлекаем имя файла без расширения
        file_name = os.path.splitext(file_path)[0]
        # Конвертируем файл в PDF
        convert(file_path, f"{file_name}.pdf")
        print(f"Конвертация успешно завершена для файла: {file_path}")
    except Exception as e:
        print(f"Ошибка при конвертации файла {file_path}: {str(e)}")


def add_text_to_pdf(input_file_path: str, output_file_path: str, text_data: List[Dict[str, Any]]) -> None:
    """
    Добавляет текст в указанное место PDF-документа.

    :param input_file_path: Путь к исходному PDF-файлу.
    :param output_file_path: Путь к результирующему PDF-файлу.
    :param text_data: Список словарей, хранящих информацию о блоках текста.
                      Каждый словарь содержит информацию о тексте, x и y координатах.
                      Пример: [{'text': 'Текст блока 1', 'x': 100, 'y': 200}, ...]
    """
    # Регистрация кириллического шрифта Arial
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

    pdf_reader = PdfReader(input_file_path)
    pdf_writer = PdfWriter()

    # Создание буфера для временного хранения созданного canvas
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Установка кириллического шрифта
    can.setFont('Arial', 12)

    for block_info in text_data:
        # Добавление текста на canvas в указанные координаты
        can.drawString(block_info['x'], block_info['y'], block_info['text'])

    can.save()  # Сохранение canvas в буфере

    packet.seek(0)  # Перемещение указателя в начало буфера
    overlay = PdfReader(packet)  # Создание PdfReader из буфера

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page.merge_page(overlay.pages[0])  # Объединение страницы исходного PDF и созданного canvas
        pdf_writer.add_page(page)  # Добавление объединенной страницы в PdfWriter

    with open(output_file_path, 'wb') as output_file:  # Сохранение результата в новом PDF
        pdf_writer.write(output_file)


def print_docx_content(file_path):
    """
    Функция принимает путь к DOCX файлу и выводит его содержимое в консоль.

    :param file_path: Путь к DOCX файлу.
    """
    # Создание объекта Document из файла
    doc = Document(file_path)

    # Переменная для отслеживания номера строки
    row_number = 0

    # Перебор всех элементов в документе (параграфы и таблицы)
    for element in doc.paragraphs:
        row_number += 1
        print(row_number, element.text)


def create_certificate(name: str, certificate_number: str, date_of_entry: str, date_of_issue: str):
    # Пример данных для блоков текста
    text_data_list = [
        {'text': name, 'x': 400, 'y': 250},
        {'text': certificate_number, 'x': 250, 'y': 174},
        {'text': date_of_entry, 'x': 210, 'y': 127},
        {'text': date_of_issue, 'x': 510, 'y': 127}
    ]

    # Пример использования функции
    input_pdf_path = 'Documents\Serifikat.pdf'
    output_pdf_path = f'Documents\Serifikat{certificate_number}.pdf'

    add_text_to_pdf(input_pdf_path, output_pdf_path, text_data_list)
