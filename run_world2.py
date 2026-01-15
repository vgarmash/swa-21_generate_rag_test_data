#!/usr/bin/env python3
# run_world2.py
import os
import sys

# Добавляем путь к world2
world2_path = os.path.join(os.path.dirname(__file__), "apps", "world2")
sys.path.insert(0, world2_path)

# Меняем рабочую директорию на world2
os.chdir(world2_path)

print(f"Working directory: {os.getcwd()}")
print(f"Python path includes: {world2_path}")

# Запускаем основной скрипт world2
from run_fictional_generation import main

if __name__ == "__main__":
    main()