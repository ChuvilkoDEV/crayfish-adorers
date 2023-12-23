import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

def add_text_to_pdf(input_file_path, output_file_path, added_text, x, y):
    # Чтение исходного PDF
    pdf_reader = PdfReader(input_file_path)
    pdf_writer = PdfWriter()

    # Создание canvas для добавления текста
    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    can.drawString(x, y, added_text)
    can.save()

    # Объединение созданного canvas с исходным PDF
    packet.seek(0)
    overlay = PdfReader(packet)
    page = pdf_reader.pages[0]
    page.merge_page(overlay.pages[0])
    pdf_writer.add_page(page)

    # Добавление оставшихся страниц
    for page_num in range(1, len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    # Сохранение результата в новом PDF
    with open(output_file_path, 'wb') as output_file:
        pdf_writer.write(output_file)

# Пример использования
input_pdf = 'example.pdf'
output_pdf = 'output_with_text.pdf'
added_text = 'Text Example'
x_coordinate = 100  # X-координата, где нужно разместить текст
y_coordinate = 500  # Y-координата, где нужно разместить текст

add_text_to_pdf(input_pdf, output_pdf, added_text, x_coordinate, y_coordinate)
