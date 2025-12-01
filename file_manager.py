import os
import shutil
from pathlib import Path
from utils import print_success, print_error, print_warning, print_info, confirm_action


class FileManager:
    def __init__(self):
        self.current_directory = Path.cwd()

    def get_current_directory(self):
        """Получить текущий рабочий каталог"""
        return self.current_directory

    def change_directory(self, new_path):
        """Сменить рабочий каталог"""
        try:
            if not new_path:
                print_error("Путь не может быть пустым")
                return False

            path = Path(new_path)
            if not path.exists():
                print_error(f"Каталог '{new_path}' не существует")
                return False

            if not path.is_dir():
                print_error(f"'{new_path}' не является каталогом")
                return False

            # Проверка прав доступа
            if not os.access(path, os.R_OK | os.W_OK):
                print_error("Недостаточно прав для доступа к каталогу")
                return False

            self.current_directory = path.resolve()
            print_success(f"Рабочий каталог изменен на: {self.current_directory}")
            return True

        except Exception as e:
            print_error(f"Ошибка при смене каталога: {str(e)}")
            return False

    def list_files_by_extension(self, extensions):
        """Получить список файлов по расширениям"""
        files = []
        for ext in extensions:
            pattern = f"*.{ext.lstrip('.')}"
            files.extend(self.current_directory.glob(pattern))

        # Убираем дубликаты и сортируем
        files = sorted(set(files), key=lambda x: x.name.lower())
        return [f for f in files if f.is_file()]

    def list_pdf_files(self):
        """Список PDF файлов"""
        return self.list_files_by_extension(['pdf'])

    def list_docx_files(self):
        """Список DOCX файлов"""
        return self.list_files_by_extension(['docx'])

    def list_image_files(self):
        """Список изображений"""
        return self.list_files_by_extension(['jpg', 'jpeg', 'png', 'gif'])

    def get_file_size(self, file_path):
        """Получение размера файла в читаемом формате"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} TB"
        except:
            return "unknown size"

    def get_file_size_from_bytes(self, size_bytes):
        """Получение читаемого формата размера из байтов"""
        try:
            size = size_bytes
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} TB"
        except:
            return "unknown size"
    def delete_files_by_pattern(self, pattern_type, pattern):
        """Удаление файлов по шаблону"""
        try:
            files_to_delete = []

            for file_path in self.current_directory.iterdir():
                if not file_path.is_file():
                    continue

                filename = file_path.name.lower()
                pattern_lower = pattern.lower()

                if pattern_type == 'startswith' and filename.startswith(pattern_lower):
                    files_to_delete.append(file_path)
                elif pattern_type == 'endswith' and filename.endswith(pattern_lower):
                    files_to_delete.append(file_path)
                elif pattern_type == 'contains' and pattern_lower in filename:
                    files_to_delete.append(file_path)
                elif pattern_type == 'extension' and filename.endswith('.' + pattern_lower.lstrip('.')):
                    files_to_delete.append(file_path)

            if not files_to_delete:
                print_info("Файлы, соответствующие критерию, не найдены")
                return False

            # Показать файлы для удаления
            print_info(f"Найдено файлов для удаления: {len(files_to_delete)}")
            for i, file_path in enumerate(files_to_delete, 1):
                size = self.get_file_size(file_path)
                print(f"  {i}. {file_path.name} ({size})")

            # Подтверждение
            if confirm_action("Вы уверены, что хотите удалить эти файлы?"):
                deleted_count = 0
                for file_path in files_to_delete:
                    try:
                        file_path.unlink()
                        print_success(f"Удален: {file_path.name}")
                        deleted_count += 1
                    except Exception as e:
                        print_error(f"Ошибка при удалении {file_path.name}: {str(e)}")

                print_success(f"Удалено файлов: {deleted_count}/{len(files_to_delete)}")
                return True
            else:
                print_info("Удаление отменено")
                return False

        except Exception as e:
            print_error(f"Ошибка при удалении файлов: {str(e)}")
            return False

    def get_unique_filename(self, original_path):
        """Получить уникальное имя файла"""
        path = Path(original_path)
        if not path.exists():
            return path

        counter = 1
        while True:
            new_name = f"{path.stem}_{counter}{path.suffix}"
            new_path = path.parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1