#!/usr/bin/env python3
# run_world1.py
import os
import sys

# Добавляем путь к world1
world1_path = os.path.join(os.path.dirname(__file__), "apps", "world1")
sys.path.insert(0, world1_path)

# Меняем рабочую директорию на world1
os.chdir(world1_path)

print(f"Working directory: {os.getcwd()}")
print(f"Python path includes: {world1_path}")

# Запускаем основной скрипт world1
from run_generation import main

if __name__ == "__main__":
    main()