import os
from pathlib import Path
from utils import print_success, print_error, print_info, get_file_size, show_progress


class DocumentConverter:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def pdf_to_docx(self, pdf_path, docx_path=None):
        """Конвертация PDF в DOCX"""
        try:
            from pdf2docx import Converter

            if docx_path is None:
                docx_path = pdf_path.with_suffix('.docx')

            # Проверка существования выходного файла
            if docx_path.exists():
                docx_path = self.file_manager.get_unique_filename(docx_path)

            print_info(f"Конвертация: {pdf_path.name} -> {docx_path.name}")

            # Конвертация
            cv = Converter(str(pdf_path))
            cv.convert(str(docx_path))
            cv.close()

            original_size = get_file_size(pdf_path)
            new_size = get_file_size(docx_path)
            print_success(f"Конвертация завершена: {original_size} -> {new_size}")
            return True

        except ImportError:
            print_error("Библиотека pdf2docx не установлена")
            return False
        except Exception as e:
            print_error(f"Ошибка конвертации PDF в DOCX: {str(e)}")
            return False

    def docx_to_pdf(self, docx_path, pdf_path=None):
        """Конвертация DOCX в PDF"""
        try:
            from docx2pdf import convert

            if pdf_path is None:
                pdf_path = docx_path.with_suffix('.pdf')

            # Проверка существования выходного файла
            if pdf_path.exists():
                pdf_path = self.file_manager.get_unique_filename(pdf_path)

            print_info(f"Конвертация: {docx_path.name} -> {pdf_path.name}")

            # Конвертация
            convert(str(docx_path), str(pdf_path))

            original_size = get_file_size(docx_path)
            new_size = get_file_size(pdf_path)
            print_success(f"Конвертация завершена: {original_size} -> {new_size}")
            return True

        except ImportError:
            print_error("Библиотека docx2pdf не установлена")
            return False
        except Exception as e:
            print_error(f"Ошибка конвертации DOCX в PDF: {str(e)}")
            print_error("Убедитесь, что Microsoft Word установлен и доступен")
            return False

    def convert_all_pdf_to_docx(self):
        """Конвертация всех PDF файлов в DOCX"""
        pdf_files = self.file_manager.list_pdf_files()
        if not pdf_files:
            print_info("PDF файлы не найдены в текущем каталоге")
            return

        print_info(f"Найдено PDF файлов: {len(pdf_files)}")
        success_count = 0

        for i, pdf_file in enumerate(pdf_files, 1):
            show_progress(i, len(pdf_files), "Конвертация PDF -> DOCX")
            if self.pdf_to_docx(pdf_file):
                success_count += 1

        print_success(f"Успешно сконвертировано: {success_count}/{len(pdf_files)}")

    def convert_all_docx_to_pdf(self):
        """Конвертация всех DOCX файлов в PDF"""
        docx_files = self.file_manager.list_docx_files()
        if not docx_files:
            print_info("DOCX файлы не найдены в текущем каталоге")
            return

        print_info(f"Найдено DOCX файлов: {len(docx_files)}")
        success_count = 0

        for i, docx_file in enumerate(docx_files, 1):
            show_progress(i, len(docx_files), "Конвертация DOCX -> PDF")
            if self.docx_to_pdf(docx_file):
                success_count += 1

        print_success(f"Успешно сконвертировано: {success_count}/{len(docx_files)}")