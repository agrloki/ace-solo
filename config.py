import configparser
import os
from pathlib import Path


class Config:
    def __init__(self, config_file=None):
        self.config = configparser.ConfigParser()
        
        if config_file is None:
            # Default to config.ini in the same directory as this module
            config_file = 'config.ini'
        
        self.config_path = config_file
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        self.config.read(config_file)

    def get_serial_port(self) -> str:
        """Получить порт для последовательного соединения"""
        try:
            return self.config.get('serial', 'port')
        except (configparser.NoSectionError, configparser.NoOptionError):
            # Возвращаем значение по умолчанию, если секция или опция отсутствует
            return '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0'

    def get_serial_baud(self) -> int:
        """Получить скорость порта для последовательного соединения"""
        try:
            return self.config.getint('serial', 'baud')
        except (configparser.NoSectionError, configparser.NoOptionError):
            # Возвращаем значение по умолчанию, если секция или опция отсутствует
            return 115200

    def get_default_feed_speed(self) -> int:
        """Получить скорость подачи по умолчанию"""
        try:
            return self.config.getint('defaults', 'feed_speed')
        except (configparser.NoSectionError, configparser.NoOptionError):
            # Возвращаем значение по умолчанию, если секция или опция отсутствует
            return 20

    def get_default_retract_speed(self) -> int:
        """Получить скорость втягивания по умолчанию"""
        try:
            return self.config.getint('defaults', 'retract_speed')
        except (configparser.NoSectionError, configparser.NoOptionError):
            # Возвращаем значение по умолчанию, если секция или опция отсутствует
            return 30

    def get_default_park_hit_count(self) -> int:
        """Получить количество ударов парковки по умолчанию"""
        try:
            return self.config.getint('defaults', 'park_hit_count')
        except (configparser.NoSectionError, configparser.NoOptionError):
            # Возвращаем значение по умолчанию, если секция или опция отсутствует
            return 2

    def get_default_max_dryer_temperature(self) -> int:
        """Получить максимальную температуру сушки по умолчанию"""
        try:
            return self.config.getint('defaults', 'max_dryer_temperature')
        except (configparser.NoSectionError, configparser.NoOptionError):
            # Возвращаем значение по умолчанию, если секция или опция отсутствует
            return 55


# Глобальный экземпляр конфига для импорта в других модулях
config = Config()