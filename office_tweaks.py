#!/usr/bin/env python3
"""
Office_Tweaks - Утилита для работы с документами и изображениями
"""

import os
import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from file_manager import FileManager
from converter import DocumentConverter
from image_processor import ImageProcessor
from utils import (
    setup_logging, print_success, print_error, print_info,
    print_warning, validate_number_input, confirm_action
)
import logging


class OfficeTweaks:
    def __init__(self):
        setup_logging()
        self.file_manager = FileManager()
        self.converter = DocumentConverter(self.file_manager)
        self.image_processor = ImageProcessor(self.file_manager)
        self.version = "1.0"

        logging.info(f"Office_Tweaks v{self.version} запущен")
        logging.info(f"Текущий каталог: {self.file_manager.get_current_directory()}")

    def display_menu(self):
        """Отображение главного меню"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{'=' * 50}")
        print(f"=== Office Tweaks v{self.version} ===")
        print(f"{'=' * 50}")
        print(f"Текущий каталог: {self.file_manager.get_current_directory()}")
        print(f"{'=' * 50}")
        print("Выберите действие:")
        print("0. Сменить рабочий каталог")
        print("1. Преобразовать PDF в Docx")
        print("2. Преобразовать Docx в PDF")
        print("3. Произвести сжатие изображений")
        print("4. Удалить группу файлов")
        print("5. Выход")
        print(f"{'=' * 50}")

    def change_directory_menu(self):
        """Меню смены рабочего каталога"""
        print_info(f"Текущий каталог: {self.file_manager.get_current_directory()}")
        new_path = input("Введите новый путь к каталогу (или Enter для отмены): ").strip()

        if new_path:
            self.file_manager.change_directory(new_path)
        else:
            print_info("Операция отменена")

        input("\nНажмите Enter для продолжения...")

    def pdf_to_docx_menu(self):
        """Меню конвертации PDF в DOCX"""
        pdf_files = self.file_manager.list_pdf_files()

        if not pdf_files:
            print_info("PDF файлы не найдены в текущем каталоге")
            input("\nНажмите Enter для продолжения...")
            return

        print_info("Список PDF файлов:")
        for i, pdf_file in enumerate(pdf_files, 1):
            size = self.file_manager.get_file_size(pdf_file)
            print(f"  {i}. {pdf_file.name} ({size})")

        print("\nВведите:")
        print("  0 - конвертировать все файлы")
        print("  -1 - отмена")
        print("  номер файла - конвертировать выбранный файл")

        while True:
            choice = input("\nВаш выбор: ").strip()
            valid, result = validate_number_input(choice, -1, len(pdf_files))

            if valid:
                if result == -1:
                    print_info("Операция отменена")
                    break
                elif result == 0:
                    self.converter.convert_all_pdf_to_docx()
                    break
                else:
                    selected_file = pdf_files[result - 1]
                    self.converter.pdf_to_docx(selected_file)
                    break
            else:
                print_error(result)

        input("\nНажмите Enter для продолжения...")

    def docx_to_pdf_menu(self):
        """Меню конвертации DOCX в PDF"""
        docx_files = self.file_manager.list_docx_files()

        if not docx_files:
            print_info("DOCX файлы не найдены в текущем каталоге")
            input("\nНажмите Enter для продолжения...")
            return

        print_info("Список DOCX файлов:")
        for i, docx_file in enumerate(docx_files, 1):
            size = self.file_manager.get_file_size(docx_file)
            print(f"  {i}. {docx_file.name} ({size})")

        print("\nВведите:")
        print("  0 - конвертировать все файлы")
        print("  -1 - отмена")
        print("  номер файла - конвертировать выбранный файл")

        while True:
            choice = input("\nВаш выбор: ").strip()
            valid, result = validate_number_input(choice, -1, len(docx_files))

            if valid:
                if result == -1:
                    print_info("Операция отменена")
                    break
                elif result == 0:
                    self.converter.convert_all_docx_to_pdf()
                    break
                else:
                    selected_file = docx_files[result - 1]
                    self.converter.docx_to_pdf(selected_file)
                    break
            else:
                print_error(result)

        input("\nНажмите Enter для продолжения...")

    def compress_images_menu(self):
        """Меню сжатия изображений"""
        image_files = self.file_manager.list_image_files()

        if not image_files:
            print_info("Изображения не найдены в текущем каталоге")
            input("\nНажмите Enter для продолжения...")
            return

        print_info("Список изображений:")
        for i, image_file in enumerate(image_files, 1):
            size = self.file_manager.get_file_size(image_file)
            print(f"  {i}. {image_file.name} ({size})")

        print("\nВведите:")
        print("  0 - обработать все файлы")
        print("  -1 - отмена")
        print("  номер файла - обработать выбранный файл")

        while True:
            choice = input("\nВаш выбор: ").strip()
            valid, result = validate_number_input(choice, -1, len(image_files))

            if valid:
                if result == -1:
                    print_info("Операция отменена")
                    break
                else:
                    quality = self.image_processor.get_compression_quality()
                    if result == 0:
                        self.image_processor.compress_all_images(quality)
                    else:
                        selected_file = image_files[result - 1]
                        self.image_processor.compress_image(selected_file, quality)
                    break
            else:
                print_error(result)

        input("\nНажмите Enter для продолжения...")

    def delete_files_menu(self):
        """Меню удаления файлов"""
        print("Выберите критерий удаления:")
        print("1. Удалить файлы, начинающиеся на...")
        print("2. Удалить файлы, заканчивающиеся на...")
        print("3. Удалить файлы, содержащие...")
        print("4. Удалить файлы по расширению")
        print("5. Отмена")

        while True:
            choice = input("\nВаш выбор: ").strip()
            valid, result = validate_number_input(choice, 1, 5)

            if valid:
                if result == 5:
                    print_info("Операция отменена")
                    break
                else:
                    pattern = input("Введите шаблон для поиска: ").strip()
                    if not pattern:
                        print_error("Шаблон не может быть пустым")
                        continue

                    pattern_types = {
                        1: 'startswith',
                        2: 'endswith',
                        3: 'contains',
                        4: 'extension'
                    }

                    self.file_manager.delete_files_by_pattern(pattern_types[result], pattern)
                    break
            else:
                print_error(result)

        input("\nНажмите Enter для продолжения...")

    def run(self):
        """Главный цикл программы"""
        try:
            while True:
                self.display_menu()
                choice = input("Ваш выбор: ").strip()

                valid, result = validate_number_input(choice, 0, 5)

                if valid:
                    if result == 0:
                        self.change_directory_menu()
                    elif result == 1:
                        self.pdf_to_docx_menu()
                    elif result == 2:
                        self.docx_to_pdf_menu()
                    elif result == 3:
                        self.compress_images_menu()
                    elif result == 4:
                        self.delete_files_menu()
                    elif result == 5:
                        print_success("До свидания!")
                        logging.info("Office_Tweaks завершил работу")
                        break
                else:
                    print_error(result)
                    input("\nНажмите Enter для продолжения...")

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
            logging.info("Программа прервана пользователем (Ctrl+C)")
        except Exception as e:
            print_error(f"Критическая ошибка: {str(e)}")
            logging.error(f"Критическая ошибка: {str(e)}")
            input("\nНажмите Enter для выхода...")


def main():
    """Точка входа в программу"""
    app = OfficeTweaks()
    app.run()


if __name__ == "__main__":
    main()