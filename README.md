# ACE-Solo

[English](#english) | [Русский](#русский)

---

<a name="русский"></a>
# ACE-Solo

Автономное Python-приложение для управления устройством ValgACE без использования Klipper. Позволяет управлять подачей филамента, парковкой, сушкой и мониторингом состояния устройства через удобный командный интерфейс.

## 🚀 Возможности

- ✅ Управление подачей и втягиванием филамента
- ✅ Парковка филамента к печатающей головке
- ✅ Мониторинг статуса устройства и информации о филаменте
- ✅ Управление сушкой филамента
- ✅ Настройка скоростей подачи и втягивания
- ✅ Вспомогательная подача (feed assist)
- ✅ Простой и понятный CLI интерфейс
- ✅ Конфигурируемые параметры через INI-файл

## 📋 Требования

- Python 3.6 или выше
- pyserial >= 3.5
- click >= 8.0
- Устройство ValgACE, подключенное через USB

## 🔧 Установка

### Автоматическая установка

```bash
./install-solo.sh
```

### Ручная установка

```bash
pip install -r requirements.txt
```

## ⚙️ Конфигурация

Перед использованием настройте файл `config.ini`:

```ini
[serial]
port = /dev/serial/by-id/usb-ANYCUBIC_ACE_1-if00
baud = 115200

[defaults]
feed_speed = 20
retract_speed = 30
park_hit_count = 2
max_dryer_temperature = 55
```

### Параметры конфигурации

- **`port`**: Путь к последовательному порту устройства
- **`baud`**: Скорость передачи данных (обычно 115200)
- **`feed_speed`**: Скорость подачи филамента по умолчанию (мм/с)
- **`retract_speed`**: Скорость втягивания филамента по умолчанию (мм/с)
- **`park_hit_count`**: Количество ударов при парковке
- **`max_dryer_temperature`**: Максимальная температура сушки (°C)

## 📖 Использование

### Основные команды

#### Получение информации

```bash
# Статус устройства
python main.py status

# Информация о филаменте в слоте
python main.py filament_info 0
```

#### Управление филаментом

```bash
# Парковка к печатающей головке
python main.py park_to_toolhead 0

# Подача филамента (слот, длина в мм, скорость в мм/с)
python main.py feed 0 100.0 20

# Втягивание филамента
python main.py retract 0 50.0 30

# Остановка подачи/втягивания
python main.py stop_feed 0
python main.py stop_retract 0
```

#### Настройка скоростей

```bash
# Обновление скорости подачи
python main.py update_feed_speed 0 25

# Обновление скорости втягивания
python main.py update_retract_speed 0 35
```

#### Вспомогательная подача

```bash
# Включить/выключить feed assist
python main.py enable_feed_assist 0
python main.py disable_feed_assist 0
```

#### Сушка филамента

```bash
# Запуск сушки (температура, продолжительность в минутах)
python main.py start_drying 55 120

# Остановка сушки
python main.py stop_drying
```

#### Отладка

```bash
# Отправка сырой команды для отладки
python main.py debug_send "get_status"
```

### Справка

Для просмотра всех доступных команд:

```bash
python main.py --help
```

Для получения справки по конкретной команде:

```bash
python main.py <команда> --help
```

## 📁 Структура проекта

```
ace-solo/
├── main.py              # Точка входа приложения
├── cli.py               # Командный интерфейс (CLI)
├── ace_driver.py        # Драйвер для работы с устройством
├── ace_protocol.py      # Протокол обмена данными
├── config.py            # Модуль конфигурации
├── config.ini           # Файл конфигурации
├── requirements.txt     # Зависимости Python
├── install-solo.sh      # Скрипт установки
├── README.md            # Документация (этот файл)
└── docs/
    └── USAGE.md         # Подробное руководство по использованию
```

## 🏗️ Архитектура

Проект построен по модульной архитектуре:

1. **`main.py`** - точка входа, инициализирует CLI
2. **`cli.py`** - обработка команд пользователя
3. **`ace_driver.py`** - управление serial-соединением и высокоуровневый API
4. **`ace_protocol.py`** - низкоуровневый протокол (пакеты, CRC16)
5. **`config.py`** - загрузка и управление конфигурацией

### Схема взаимодействия компонентов

```
Пользователь → main.py → cli.py → ace_driver.py → ace_protocol.py → Устройство ACE
                                    ↓
                                 config.py → config.ini
```

## 🔌 Протокол связи

Приложение использует собственный протокол обмена данными с устройством:

- **Формат пакета**: `[0xFF 0xAA] [длина] [JSON payload] [CRC16] [0xFE]`
- **Контрольная сумма**: CRC16-CCITT-FALSE
- **Формат данных**: JSON для команд и ответов
- **Порядок байтов**: Little-endian

## ⚠️ Устранение неполадок

### Устройство не найдено

Убедитесь, что:
- Устройство подключено через USB
- Правильно указан путь к порту в `config.ini`
- У вас есть права доступа к serial-порту (может потребоваться добавить пользователя в группу `dialout`)

```bash
# Проверка доступных портов
ls -l /dev/serial/by-id/

# Добавление пользователя в группу dialout
sudo usermod -a -G dialout $USER
```

### Ошибки связи

- Проверьте скорость передачи данных (baud rate) в `config.ini`
- Убедитесь, что устройство не используется другим приложением
- Попробуйте переподключить USB-кабель

## 📝 Лицензия

Этот проект распространяется без лицензии или с лицензией, указанной в репозитории.

## 🤝 Вклад в проект

Предложения по улучшению и исправления ошибок приветствуются! Пожалуйста, создавайте issues и pull requests.

## 📚 Дополнительная документация

Подробное руководство по использованию доступно в файле [docs/USAGE.md](docs/USAGE.md).

---

<a name="english"></a>
# ACE-Solo

Standalone Python application for controlling the ValgACE device without Klipper. Allows you to manage filament feeding, parking, drying, and device status monitoring through a convenient command-line interface.

## 🚀 Features

- ✅ Filament feed and retract control
- ✅ Filament parking to print head
- ✅ Device status and filament information monitoring
- ✅ Filament drying control
- ✅ Feed and retract speed configuration
- ✅ Feed assist functionality
- ✅ Simple and intuitive CLI interface
- ✅ Configurable parameters via INI file

## 📋 Requirements

- Python 3.6 or higher
- pyserial >= 3.5
- click >= 8.0
- ValgACE device connected via USB

## 🔧 Installation

### Automatic Installation

```bash
./install-solo.sh
```

### Manual Installation

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Before using, configure the `config.ini` file:

```ini
[serial]
port = /dev/serial/by-id/usb-ANYCUBIC_ACE_1-if00
baud = 115200

[defaults]
feed_speed = 20
retract_speed = 30
park_hit_count = 2
max_dryer_temperature = 55
```

### Configuration Parameters

- **`port`**: Path to the device serial port
- **`baud`**: Data transmission rate (usually 115200)
- **`feed_speed`**: Default filament feed speed (mm/s)
- **`retract_speed`**: Default filament retract speed (mm/s)
- **`park_hit_count`**: Number of hits during parking
- **`max_dryer_temperature`**: Maximum drying temperature (°C)

## 📖 Usage

### Basic Commands

#### Getting Information

```bash
# Device status
python main.py status

# Filament information for a slot
python main.py filament_info 0
```

#### Filament Control

```bash
# Park to print head
python main.py park_to_toolhead 0

# Feed filament (slot, length in mm, speed in mm/s)
python main.py feed 0 100.0 20

# Retract filament
python main.py retract 0 50.0 30

# Stop feed/retract
python main.py stop_feed 0
python main.py stop_retract 0
```

#### Speed Configuration

```bash
# Update feed speed
python main.py update_feed_speed 0 25

# Update retract speed
python main.py update_retract_speed 0 35
```

#### Feed Assist

```bash
# Enable/disable feed assist
python main.py enable_feed_assist 0
python main.py disable_feed_assist 0
```

#### Filament Drying

```bash
# Start drying (temperature, duration in minutes)
python main.py start_drying 55 120

# Stop drying
python main.py stop_drying
```

#### Debugging

```bash
# Send raw command for debugging
python main.py debug_send "get_status"
```

### Help

To view all available commands:

```bash
python main.py --help
```

To get help for a specific command:

```bash
python main.py <command> --help
```

## 📁 Project Structure

```
ace-solo/
├── main.py              # Application entry point
├── cli.py               # Command-line interface (CLI)
├── ace_driver.py        # Device driver
├── ace_protocol.py      # Communication protocol
├── config.py            # Configuration module
├── config.ini           # Configuration file
├── requirements.txt     # Python dependencies
├── install-solo.sh      # Installation script
├── README.md            # Documentation (this file)
└── docs/
    └── USAGE.md         # Detailed usage guide
```

## 🏗️ Architecture

The project is built using a modular architecture:

1. **`main.py`** - entry point, initializes CLI
2. **`cli.py`** - handles user commands
3. **`ace_driver.py`** - manages serial connection and high-level API
4. **`ace_protocol.py`** - low-level protocol (packets, CRC16)
5. **`config.py`** - loads and manages configuration

### Component Interaction Diagram

```
User → main.py → cli.py → ace_driver.py → ace_protocol.py → ACE Device
                                    ↓
                                 config.py → config.ini
```

## 🔌 Communication Protocol

The application uses a custom communication protocol with the device:

- **Packet format**: `[0xFF 0xAA] [length] [JSON payload] [CRC16] [0xFE]`
- **Checksum**: CRC16-CCITT-FALSE
- **Data format**: JSON for commands and responses
- **Byte order**: Little-endian

## ⚠️ Troubleshooting

### Device Not Found

Make sure:
- Device is connected via USB
- Port path is correctly specified in `config.ini`
- You have access rights to the serial port (may need to add user to `dialout` group)

```bash
# Check available ports
ls -l /dev/serial/by-id/

# Add user to dialout group
sudo usermod -a -G dialout $USER
```

### Communication Errors

- Check the baud rate in `config.ini`
- Ensure the device is not being used by another application
- Try reconnecting the USB cable

## 📝 License

This project is distributed without a license or with the license specified in the repository.

## 🤝 Contributing

Suggestions for improvements and bug fixes are welcome! Please create issues and pull requests.

## 📚 Additional Documentation

A detailed usage guide is available in [docs/USAGE.md](docs/USAGE.md).
