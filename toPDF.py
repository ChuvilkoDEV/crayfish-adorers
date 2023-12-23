import os
from docx2pdf import convert

def convert_docx_to_pdf(file_path):
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