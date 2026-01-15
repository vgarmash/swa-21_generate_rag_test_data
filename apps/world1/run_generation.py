#!/usr/bin/env python3
# apps/world1/run_generation.py
import sys
import os
import time

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_python_script(script_name):
    """Запускает Python скрипт напрямую, без subprocess"""
    try:
        print(f"  Executing: {script_name}")

        if script_name == "document_generator.py":
            from document_generator import main as script_main
            script_main()
        elif script_name == "analyze_corpus.py":
            from analyze_corpus import main as script_main
            script_main()
        else:
            print(f"  ❌ Unknown script: {script_name}")
            return False

        return True
    except Exception as e:
        print(f"  ❌ Error executing {script_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Asterix Universe Document Generator")
    print("=" * 50)

    # Создаём папки
    output_dir = "documents"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    steps = [
        ("Creating documents...", "document_generator.py"),
        ("Analyzing corpus...", "analyze_corpus.py")
    ]

    for description, script in steps:
        print(f"\n📝 {description}")
        success = run_python_script(script)
        if success:
            print("  ✅ Done")
        else:
            print("  ⚠️  Warning: Script had issues")
        time.sleep(0.5)

    print("\n" + "=" * 50)
    print("🎉 Generation complete!")

    # Проверяем созданные файлы
    generated_files = []
    for filename in ["document_index.json", "qa_pairs.jsonl", "corpus_network.json"]:
        if os.path.exists(filename):
            generated_files.append(filename)

    print(f"\n📁 Output structure:")
    for file in generated_files:
        print(f"  {file}")

    if os.path.exists(output_dir):
        doc_count = len([f for f in os.listdir(output_dir) if f.endswith('.txt')])
        print(f"  {output_dir}/ - {doc_count} document files")

if __name__ == "__main__":
    main()