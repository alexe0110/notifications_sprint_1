import csv
import os
from typing import Any, Callable


class CSVHandler:
    def __init__(self, columns: list[str], file_path: str):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            self.columns = columns
            self._create_file()
        else:
            self.columns = self._get_columns()

    def _get_columns(self) -> list[str]:
        """Возвращает названия колонок первого ряда файла."""
        with open(self.file_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return next(reader)  # Получаем первую строку как заголовки

    def _create_file(self) -> None:
        """Создает новый CSV файл с заголовками."""
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.columns)  # Записываем заголовки в файл

    def count_rows(self) -> int:
        """Возвращает количество строк в файле (без учета заголовков)."""
        with open(self.file_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return sum(1 for _ in reader) - 1  # Вычитаем 1 для заголовка

    def write_row(self, data: dict[str, Any]) -> None:
        """
        Записывает новую строку в файл с данными по колонкам.
        :param data: Словарь с данными для записи.
        :raises ValueError: Если ключи не соответствуют колонкам.
        """
        if set(data.keys()) != set(self.columns):
            not_known_columns = set(self.columns) - set(data.keys())
            raise ValueError(f'Не хватает ключей: {not_known_columns}, пришли: {data.keys()}')

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.columns)
            writer.writerow(data)

    def clear_file(self) -> None:
        """Очищает все строки, кроме заголовков."""
        with open(self.file_path, 'r+', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Читаем заголовки
            # Очищаем содержимое файла
            file.seek(0)
            file.truncate()
            # Записываем заголовки обратно
            writer = csv.writer(file)
            writer.writerow(header)

    def read_all_rows(self) -> list[dict[str, Any]]:
        """Возвращает все строки файла в виде списка словарей."""
        with open(self.file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def delete_rows(self, condition: Callable[[dict[str, Any]], bool]) -> None:
        """
        Удаляет строки из файла по заданному условию.
        :param condition: Функция условия, которая принимает строку (словарь) и возвращает True, если строка должна быть удалена.
        """
        rows = self.read_all_rows()  # Читаем все строки
        rows_to_keep = [
            row for row in rows if not condition(row)
        ]  # Оставляем те строки, которые не соответствуют условию

        # Перезаписываем файл новыми данными
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.columns)
            writer.writeheader()  # Записываем заголовки
            writer.writerows(rows_to_keep)  # Записываем оставшиеся строки
