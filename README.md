# Активируйте виртуальное окружение если нужно
- ```.venv\Scripts\activate  # Windows```
- ```source .venv/bin/activate  # Linux/Mac```

# Установите зависимости
`pip install -r requirements.txt`

# Запустите world1 (оригинальный Asterix мир)
`python run_world1.py`

# Запустите world2 (вымышленный мир)
## Из корня проекта запустите тест:
`python test_all.py`

## Если тест проходит, запустите генерацию:
`python run_world2.py`