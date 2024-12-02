#!/bin/bash

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен. Пропишите sudo apt install python3"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Создаю виртуальное окружение..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Устанавливаю зависимости..."
pip install -r requirements.txt

echo "Запускаю основной скрипт..."
python3 core/main.py
