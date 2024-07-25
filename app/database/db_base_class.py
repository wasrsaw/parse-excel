"""
Здесь базовый класс БД
"""
from typing import Any, Dict, overload
from abc import ABC, abstractmethod

class BaseDatabase():
    def __init__(self) -> None:
        """
        Инициализируем глобальные параметры
        """
        self.DB_NAME = None
        self.DB_USER = None
        self.DB_PASSWORD = None
        self.DB_HOST = None
        self.DB_PORT = None

    @abstractmethod
    def set_conn(self):
        """
        Устанавливаем соединение с БД
        """
        pass

    @abstractmethod
    def set_data(self, query: str, *args):
        """
        Устанавливаем данные БД
        """
        pass

    @abstractmethod
    def get_data(self, query: str, *args):
        """
        Получаем данные БД
        """
        pass
