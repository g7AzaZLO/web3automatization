import json
import os
from typing import Optional, Union


def read_json(path: str, encoding: Optional[str] = None) -> Union[list, dict]:
    """
    Читает содержимое файла и возвращает его в виде словаря или списка.

    :param path: путь к файлу для чтения
    :param encoding: тип расшифровки
    :return:
    """
    return json.load(open(path, encoding=encoding))


def read_file(path: str) -> list:
    """
    Читает содержимое файла и возвращает его в виде списка строк.

    :param path: Путь к файлу, который нужно прочитать.
    :return: Список строк из файла.
    :raises FileNotFoundError: Если файл не найден.
    """
    if os.path.exists(path):
        with open(path, "r") as file:
            return file.read().splitlines()
    else:
        raise FileNotFoundError(f"The file '{path}' does not exist.")
