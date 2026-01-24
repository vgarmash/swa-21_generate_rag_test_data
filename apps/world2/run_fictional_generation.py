#!/usr/bin/env python3
# apps/world2/run_fictional_generation.py
import sys
import os
import time
import shutil

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def cleanup_old_folders():
    """Очищает старые папки перед генерацией"""
    folders_to_clean = ["knowledge_base", "generated", "fictional_documents"]

    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"  Cleaned up: {folder}/")
            except Exception as e:
                print(f"  Warning: Could not clean {folder}: {e}")

def run_script(script_name):
    """Запускает Python скрипт"""
    try:
        print(f"  Running: {script_name}")

        if script_name == "fictional_world_bible.py":
            import fictional_world_bible
            if hasattr(fictional_world_bible, 'main'):
                fictional_world_bible.main()
            else:
                print(f"  ❌ No main() in {script_name}")
                return False

        elif script_name == "fictional_document_generator.py":
            import fictional_document_generator
            if hasattr(fictional_document_generator, 'main'):
                fictional_document_generator.main()
            else:
                print(f"  ❌ No main() in {script_name}")
                return False

        else:
            print(f"  ❌ Unknown script: {script_name}")
            return False

        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🎭 Fictional Universe Generator v2.0")
    print("=" * 60)
    print("Creating unique documents with new folder structure")

    # Очищаем старые папки
    print("\n🧹 Cleaning up old folders...")
    cleanup_old_folders()

    # Шаги генерации
    steps = [
        ("Building fictional world with unique terms", "fictional_world_bible.py"),
        ("Generating 50 documents with new structure", "fictional_document_generator.py")
    ]

    for desc, script in steps:
        print(f"\n📝 {desc}")
        print("-" * 40)
        success = run_script(script)
        if success:
            print("  ✅ Success")
        else:
            print("  ⚠️  Issues encountered")
        time.sleep(0.5)

    # Проверяем результаты
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)

    # Проверяем папки
    folders_to_check = [
        ("knowledge_base", "Knowledge base documents"),
        ("generated", "Generated metadata and QA pairs")
    ]

    print("\n📁 Generated folders:")
    for folder, description in folders_to_check:
        if os.path.exists(folder):
            if folder == "knowledge_base":
                files = [f for f in os.listdir(folder) if f.endswith('.txt')]
                print(f"  ✓ {folder}/ - {len(files)} {description}")
            elif folder == "generated":
                files = os.listdir(folder)
                print(f"  ✓ {folder}/ - {len(files)} files ({description})")
        else:
            print(f"  ✗ {folder}/ - MISSING")

    # Показываем содержимое generated
    if os.path.exists("generated"):
        print(f"\n📄 Files in generated/:")
        for file in sorted(os.listdir("generated")):
            filepath = os.path.join("generated", file)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                print(f"  - {file} ({size:,} bytes)")

    # Проверяем уникальность документов
    if os.path.exists("knowledge_base"):
        files = [f for f in os.listdir("knowledge_base") if f.endswith('.txt')]
        if files:
            # Читаем первые 200 символов из первых 5 файлов
            contents = []
            for f in files[:5]:
                with open(os.path.join("knowledge_base", f), 'r', encoding='utf-8') as file:
                    contents.append(file.read()[:200])

            unique_contents = set(contents)
            if len(unique_contents) == len(contents):
                print(f"\n✓ Sample documents are unique")
            else:
                print(f"\n⚠️  Some sample documents show repetition")

            print(f"\n📊 Document types in knowledge_base/:")
            doc_types = {}
            for f in files:
                doc_type = f.split('_')[0]
                doc_types[doc_type] = doc_types.get(doc_type, 0) + 1

            for doc_type, count in doc_types.items():
                print(f"  {doc_type}: {count} documents")

    print("\n🔍 New folder structure:")
    print("  knowledge_base/ - 50 documents for RAG testing")
    print("  generated/ - All metadata, indices, and QA pairs")

    print("\n🎯 QA Pair types available:")
    if os.path.exists("generated"):
        qa_files = [f for f in os.listdir("generated") if 'qa' in f.lower()]
        for qa_file in qa_files:
            print(f"  - {qa_file}")

if __name__ == "__main__":
    main()