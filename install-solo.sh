#!/bin/bash

echo "Начало установки ace-solo..."

# Находим директорию скрипта, чтобы корректно найти requirements.txt
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Установка зависимостей Python из requirements.txt..."
if python3 -m pip install -r "$SCRIPT_DIR/requirements.txt"; then
    echo "Зависимости успешно установлены."
else
    echo "Ошибка при установке зависимостей. Убедитесь, что pip установлен."
    exit 1
fi

echo ""
echo "Установка ace-solo завершена!"
echo "Для начала работы, настройте ace-solo/config.ini"
echo "Затем используйте 'python3 ace-solo/main.py --help' для просмотра доступных команд."