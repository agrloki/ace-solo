# File: ace-solo/ace_protocol.py
# Протокол обмена данными с устройством ValgACE

import json
import struct
import binascii


def crc16(data: bytes) -> int:
    """
    Вычисление CRC16-CCITT-FALSE (0xFFFF начальное значение, 0x1021 полином)
    """
    crc = 0xffff
    for byte in data:
        data = byte ^ (crc & 0xff)
        data ^= (data & 0x0f) << 4
        crc = (((data << 8) | (crc >> 8)) ^ (data >> 4) ^ (data << 3)) & 0xffff
    return crc & 0xffff


def build_packet(command: str, params: dict) -> bytes:
    """
    Функция, которая принимает имя команды и словарь параметров,
    преобразует их в JSON и упаковывает в бинарный пакет с заголовком,
    длиной, данными и CRC16.
    """
    # Создаем JSON-объект команды
    request = {"method": command}
    if params:
        request["params"] = params
    
    # Преобразуем в байты
    payload = json.dumps(request).encode('utf-8')
    
    # Вычисляем CRC
    crc = crc16(payload)
    
    # Формируем пакет: заголовок (0xFF 0xAA) + длина (2 байта, little endian) + payload + CRC (2 байта, little endian) + конец (0xFE)
    packet = (
        bytes([0xFF, 0xAA]) +
        struct.pack('<H', len(payload)) +
        payload +
        struct.pack('<H', crc) +
        bytes([0xFE])
    )
    
    return packet


def parse_response(data: bytes) -> dict:
    """
    Функция, которая принимает бинарный ответ от устройства,
    проверяет заголовок, длину, CRC16 и возвращает JSON-содержимое в виде словаря.
    Вызывает исключение (ValueError) в случае ошибки формата или CRC.
    """
    # Проверяем минимальную длину пакета: заголовок (2) + длина (2) + CRC (2) + конец (1) = 7
    if len(data) < 7:
        raise ValueError("Packet too short")
    
    # Проверяем заголовок
    if data[0:2] != bytes([0xFF, 0xAA]):
        raise ValueError("Invalid packet header")
    
    # Проверяем конец пакета
    if data[-1] != 0xFE:
        raise ValueError("Invalid packet end")
    
    # Читаем длину полезной нагрузки
    payload_len = struct.unpack('<H', data[2:4])[0]
    
    # Проверяем, что длина соответствует ожидаемой длине пакета
    expected_length = 4 + payload_len + 3  # 4 байта заголовок+длина + payload_len + 2 байта CRC + 1 байт конец
    if len(data) != expected_length:
        raise ValueError(f"Invalid packet length: expected {expected_length}, got {len(data)}")
    
    # Извлекаем полезную нагрузку
    payload = data[4:4+payload_len]
    
    # Извлекаем CRC из пакета
    packet_crc = struct.unpack('<H', data[4+payload_len:4+payload_len+2])[0]
    
    # Проверяем CRC
    calculated_crc = crc16(payload)
    if calculated_crc != packet_crc:
        raise ValueError(f"CRC mismatch: expected {calculated_crc}, got {packet_crc}")
    
    # Декодируем JSON
    try:
        response = json.loads(payload.decode('utf-8'))
        return response
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in payload: {e}")
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid UTF-8 in payload: {e}")