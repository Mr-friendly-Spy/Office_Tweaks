import argparse
import sys
from pathlib import Path


class CLIParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Office Tweaks - Утилита для работы с документами и изображениями',
            epilog='Примеры использования:\n'
                   '  office_tweaks.py -i                     # Интерактивный режим\n'
                   '  office_tweaks.py --pdf2docx file.pdf    # Конвертация PDF в DOCX\n'
                   '  office_tweaks.py --docx2pdf all --workdir ./docs\n'
                   '  office_tweaks.py --compress-images photo.jpg --quality 75',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self._setup_arguments()

    def _setup_arguments(self):
        """Настройка аргументов командной строки"""
        # Основные операции
        operations_group = self.parser.add_argument_group('Операции')

        operations_group.add_argument(
            '--pdf2docx',
            metavar='FILE|all',
            help='Конвертировать PDF в DOCX. Укажите путь к файлу или "all" для всех файлов'
        )

        operations_group.add_argument(
            '--docx2pdf',
            metavar='FILE|all',
            help='Конвертировать DOCX в PDF. Укажите путь к файлу или "all" для всех файлов'
        )

        operations_group.add_argument(
            '--compress-images',
            metavar='FILE|all',
            help='Сжать изображения. Укажите путь к файлу или "all" для всех файлов'
        )

        operations_group.add_argument(
            '--delete',
            action='store_true',
            help='Удалить файлы по критерию'
        )

        # Параметры операций
        params_group = self.parser.add_argument_group('Параметры операций')

        params_group.add_argument(
            '--workdir',
            metavar='DIR',
            help='Рабочий каталог (по умолчанию - текущий)'
        )

        params_group.add_argument(
            '--delete-dir',
            metavar='DIR',
            help='Каталог для удаления файлов (по умолчанию --workdir)'
        )

        params_group.add_argument(
            '--delete-mode',
            choices=['startswith', 'endswith', 'contains', 'extension'],
            help='Режим удаления файлов: startswith, endswith, contains, extension'
        )

        params_group.add_argument(
            '--delete-pattern',
            metavar='PATTERN',
            help='Шаблон для удаления файлов'
        )

        params_group.add_argument(
            '--quality',
            type=int,
            choices=range(1, 101),
            metavar='1-100',
            default=85,
            help='Качество сжатия изображений (1-100, по умолчанию: 85)'
        )

        params_group.add_argument(
            '--output',
            metavar='FILE',
            help='Выходной файл (для одиночных операций)'
        )

        # Режимы работы
        mode_group = self.parser.add_argument_group('Режимы работы')

        mode_group.add_argument(
            '-i', '--interactive',
            action='store_true',
            help='Запустить интерактивный режим'
        )

        mode_group.add_argument(
            '-v', '--version',
            action='version',
            version='Office Tweaks v2.0',
            help='Показать версию программы'
        )

    def parse_args(self):
        """Парсинг аргументов"""
        args = self.parser.parse_args()

        # Валидация аргументов
        self._validate_args(args)

        return args

    def _validate_args(self, args):
        """Валидация аргументов"""
        # Проверка обязательных параметров для удаления
        if args.delete:
            if not args.delete_mode:
                self.parser.error("Для операции удаления требуется --delete-mode")
            if not args.delete_pattern:
                self.parser.error("Для операции удаления требуется --delete-pattern")

        # Проверка конфликтующих операций
        operations = []
        if args.pdf2docx:
            operations.append('pdf2docx')
        if args.docx2pdf:
            operations.append('docx2pdf')
        if args.compress_images:
            operations.append('compress_images')
        if args.delete:
            operations.append('delete')

        if len(operations) > 1:
            self.parser.error(f"Нельзя выполнять несколько операций одновременно: {', '.join(operations)}")

        # Проверка качества сжатия
        if args.quality and (args.quality < 1 or args.quality > 100):
            self.parser.error("Качество сжатия должно быть в диапазоне 1-100")

        # Проверка путей
        if args.workdir:
            if not Path(args.workdir).exists():
                self.parser.error(f"Каталог не существует: {args.workdir}")

        if args.delete_dir:
            if not Path(args.delete_dir).exists():
                self.parser.error(f"Каталог для удаления не существует: {args.delete_dir}")

    def get_operation_mode(self, args):
        """Определить режим работы"""
        if args.interactive or not any([args.pdf2docx, args.docx2pdf, args.compress_images, args.delete]):
            return 'interactive'
        else:
            return 'batch'