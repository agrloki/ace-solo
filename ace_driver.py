# File: ace-solo/ace_driver.py
# Драйвер для взаимодействия с устройством ValgACE

import time
import serial
import threading
import ace_protocol
from config import config


class ACEDriver:
    def __init__(self):
        self.port = config.get_serial_port()
        self.baudrate = config.get_serial_baud()
        self.timeout = 5  # 5 seconds timeout for read operations
        self.write_timeout = 2  # 2 seconds timeout for write operations
        self.serial_conn = None
        self.lock = threading.Lock()
    
    def connect(self):
        """Открытие соединения с serial-портом"""
        if self.serial_conn is not None and self.serial_conn.is_open:
            return True  # Already connected
        
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                write_timeout=self.write_timeout
            )
            return True
        except serial.SerialException as e:
            print(f"Failed to connect to serial port {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Закрытие соединения с serial-портом"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            self.serial_conn = None
    
    def _read_response(self):
        """Приватный метод для чтения ответа от устройства"""
        if not self.serial_conn or not self.serial_conn.is_open:
            raise serial.SerialException("Serial connection is not open")
        
        # Read header (0xFF 0xAA)
        header = self.serial_conn.read(2)
        if len(header) < 2:
            raise ValueError("Failed to read packet header")
        
        if header != bytes([0xFF, 0xAA]):
            raise ValueError("Invalid packet header")
        
        # Read payload length (2 bytes, little endian)
        length_bytes = self.serial_conn.read(2)
        if len(length_bytes) < 2:
            raise ValueError("Failed to read packet length")
        
        payload_len = int.from_bytes(length_bytes, byteorder='little')
        
        # Read payload
        payload = self.serial_conn.read(payload_len)
        if len(payload) < payload_len:
            raise ValueError("Failed to read full payload")
        
        # Read CRC (2 bytes, little endian)
        crc_bytes = self.serial_conn.read(2)
        if len(crc_bytes) < 2:
            raise ValueError("Failed to read CRC")
        
        # Read end marker (0xFE)
        end_marker = self.serial_conn.read(1)
        if len(end_marker) < 1 or end_marker[0] != 0xFE:
            raise ValueError("Invalid packet end")
        
        # Combine all parts to form the complete packet
        packet = header + length_bytes + payload + crc_bytes + end_marker
        
        return packet
    
    def _send_command(self, command, params=None, retries=3, delay=2):
        """Приватный метод для отправки команды и получения ответа с повторными попытками"""
        if not self.serial_conn or not self.serial_conn.is_open:
            raise serial.SerialException("Serial connection is not open")

        packet = ace_protocol.build_packet(command, params)
        
        last_exception = None
        
        with self.lock:
            for attempt in range(retries):
                try:
                    self.serial_conn.write(packet)
                    response_packet = self._read_response()
                    response = ace_protocol.parse_response(response_packet)
                    return response
                except serial.SerialException as e:
                    print(f"Attempt {attempt + 1}/{retries} failed with serial error: {e}")
                    last_exception = e
                    time.sleep(delay)
                except ValueError as e:
                    print(f"Error parsing response: {e}")
                    # Не повторяем при ошибках парсинга, так как это, скорее всего, не временная проблема
                    raise
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    last_exception = e
                    # Можно добавить повтор для других неожиданных ошибок, если это имеет смысл
                    time.sleep(delay)
            
            # Если все попытки не увенчались успехом
            if last_exception:
                print("All retry attempts failed.")
                raise last_exception
        
        # Этот код не должен быть достижим, но для безопасности:
        return None
    
    def get_status(self):
        """Получить статус устройства"""
        return self._send_command("get_status", {})
    
    def get_filament_info(self, slot):
        """Получить информацию о филаменте в указанном слоте"""
        return self._send_command("get_filament_info", {"slot": slot})
    
    def park_to_toolhead(self, slot):
        """Парковка к головке"""
        return self._send_command("start_feed_assist", {"slot": slot})
    
    def feed(self, slot, length, speed):
        """Подача филамента"""
        return self._send_command("feed_filament", {"slot": slot, "length": length, "speed": speed})
    
    def retract(self, slot, length, speed):
        """Втягивание филамента"""
        return self._send_command("unwind_filament", {"slot": slot, "length": length, "speed": speed})
    
    def stop_feed(self, slot):
        """Остановить подачу филамента"""
        return self._send_command("stop_feed_filament", {"slot": slot})
    
    def stop_retract(self, slot):
        """Остановить втягивание филамента"""
        return self._send_command("stop_unwind_filament", {"slot": slot})
    
    def update_feed_speed(self, slot, speed):
        """Обновить скорость подачи филамента"""
        return self._send_command("update_feeding_speed", {"slot": slot, "speed": speed})
    
    def update_retract_speed(self, slot, speed):
        """Обновить скорость втягивания филамента"""
        return self._send_command("update_unwinding_speed", {"slot": slot, "speed": speed})
    
    def enable_feed_assist(self, slot):
        """Включить вспомогательную подачу"""
        return self._send_command("start_feed_assist", {"slot": slot})
    
    def disable_feed_assist(self, slot):
        """Выключить вспомогательную подачу"""
        return self._send_command("stop_feed_assist", {"slot": slot})
    
    def start_drying(self, temp, duration):
        """Начать сушку филамента"""
        return self._send_command("drying", {"temp": temp, "duration": duration, "fan_speed": 7000})
    
    def stop_drying(self):
        """Остановить сушку филамента"""
        return self._send_command('drying_stop', {})
    
    def debug_send(self, command_string):
        """Отправить команду для отладки"""
        # This method allows sending raw command strings for debugging purposes
        # It's useful for testing new commands or troubleshooting
        return self._send_command(command_string)