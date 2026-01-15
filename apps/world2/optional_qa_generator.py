#!/usr/bin/env python3
# apps/world2/optional_qa_generator.py
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fictional_world_bible import FictionalWorldBuilder
from fictional_document_generator import generate_qa_pairs, save_qa_pairs

def load_documents():
    """Загружает существующие документы"""
    documents = []
    docs_folder = "fictional_documents"

    if not os.path.exists(docs_folder):
        print(f"❌ Directory '{docs_folder}' not found. Generate documents first.")
        return []

    for filename in os.listdir(docs_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(docs_folder, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                doc_id = filename.replace('.txt', '')
                doc_type = doc_id.split('_')[0]
                documents.append({
                    'id': doc_id,
                    'type': doc_type.lower() if doc_type.lower() in ['encyclopedia', 'journal', 'report', 'decree', 'myth', 'letter'] else 'unknown',
                    'content': content
                })

    return documents

def load_world_data():
    """Загружает данные о мире"""
    if os.path.exists('fictional_world.json'):
        with open('fictional_world.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_terms_map():
    """Загружает маппинг терминов"""
    if os.path.exists('terms_map.json'):
        with open('terms_map.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('categories', {})
    return {}

def main():
    print("🔍 Generating QA pairs for fictional universe")
    print("=" * 60)

    # Загружаем данные
    documents = load_documents()
    if not documents:
        print("No documents found. Please run the main generator first.")
        return

    world_data = load_world_data()
    terms_map = load_terms_map()

    if not world_data:
        # Создаём мир, если файла нет
        builder = FictionalWorldBuilder()
        world_data, _ = builder.build_world()
        terms_map = builder.categories

    print(f"Loaded {len(documents)} documents")
    print(f"Universe: {world_data.get('fictional_universe', 'Unknown')}")

    # Генерируем QA пары
    qa_pairs = generate_qa_pairs(documents, world_data, terms_map)

    # Сохраняем
    count = save_qa_pairs(qa_pairs)

    # Показываем статистику
    print("\n📊 QA Pairs Statistics:")
    print("-" * 40)

    categories = {}
    difficulties = {}

    for qa in qa_pairs:
        cat = qa.get('category', 'unknown')
        diff = qa.get('difficulty', 'unknown')

        categories[cat] = categories.get(cat, 0) + 1
        difficulties[diff] = difficulties.get(diff, 0) + 1

    print("By category:")
    for cat, cnt in categories.items():
        print(f"  {cat:20}: {cnt:2} pairs")

    print("\nBy difficulty:")
    for diff, cnt in difficulties.items():
        print(f"  {diff:20}: {cnt:2} pairs")

    print(f"\nTotal QA pairs: {count}")

    # Показываем примеры
    print("\n🎯 Example questions for RAG testing:")
    print("=" * 60)
    for i, qa in enumerate(qa_pairs[:5], 1):
        print(f"\n{i}. {qa['question']}")
        print(f"   Answer length: {len(qa['answer'])} characters")
        print(f"   Sources: {', '.join(qa['source_docs'][:3])}")
        print(f"   Category: {qa['category']}, Difficulty: {qa['difficulty']}")

if __name__ == "__main__":
    main()