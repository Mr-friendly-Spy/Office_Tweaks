import os
from pathlib import Path
from utils import print_success, print_error, print_info, get_file_size, validate_number_input, show_progress


class ImageProcessor:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def compress_image(self, image_path, quality=85, output_dir=None):
        """Сжатие изображения"""
        try:
            from PIL import Image

            if output_dir is None:
                output_dir = self.file_manager.current_directory

            output_path = output_dir / f"compressed_{image_path.name}"

            # Проверка существования выходного файла
            if output_path.exists():
                output_path = self.file_manager.get_unique_filename(output_path)

            # Открытие и обработка изображения
            with Image.open(image_path) as img:
                original_format = img.format
                original_size = os.path.getsize(image_path)

                # Сохранение с указанным качеством
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                save_kwargs = {'quality': quality, 'optimize': True}
                if original_format == 'PNG':
                    save_kwargs = {'optimize': True}

                img.save(output_path, **save_kwargs)
                new_size = os.path.getsize(output_path)

                # Расчет экономии
                savings = original_size - new_size
                savings_percent = (savings / original_size) * 100 if original_size > 0 else 0

                return True, savings, savings_percent

        except ImportError:
            print_error("Библиотека Pillow не установлена")
            return False, 0, 0
        except Exception as e:
            print_error(f"Ошибка сжатия изображения {image_path.name}: {str(e)}")
            return False, 0, 0

    def compress_all_images(self, quality=85):
        """Сжатие всех изображений"""
        image_files = self.file_manager.list_image_files()
        if not image_files:
            print_info("Изображения не найдены в текущем каталоге")
            return

        print_info(f"Найдено изображений: {len(image_files)}")
        success_count = 0
        total_savings = 0
        total_original_size = 0

        for i, image_file in enumerate(image_files, 1):
            show_progress(i, len(image_files), "Сжатие изображений")
            success, savings, _ = self.compress_image(image_file, quality)
            if success:
                success_count += 1
                total_savings += savings
                total_original_size += os.path.getsize(image_file)

        # Общая статистика
        if total_original_size > 0:
            total_savings_percent = (total_savings / total_original_size) * 100
            print_success(
                f"Сжато изображений: {success_count}/{len(image_files)}. "
                f"Общая экономия: {total_savings / 1024 / 1024:.2f} MB ({total_savings_percent:.1f}%)"
            )
        else:
            print_success(f"Сжато изображений: {success_count}/{len(image_files)}")

    def get_compression_quality(self):
        """Получить качество сжатия от пользователя"""
        while True:
            try:
                quality_input = input("Введите качество сжатия (1-100, по умолчанию 85): ").strip()
                if not quality_input:
                    return 85

                quality = int(quality_input)
                if 1 <= quality <= 100:
                    return quality
                else:
                    print_error("Качество должно быть в диапазоне от 1 до 100")
            except ValueError:
                print_error("Пожалуйста, введите целое число")