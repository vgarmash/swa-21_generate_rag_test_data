#!/usr/bin/env python3
# apps/world2/run_fictional_generation.py
import sys
import os
import time

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_python_script(script_name):
    """Запускает Python скрипт напрямую, без subprocess"""
    try:
        print(f"  Executing: {script_name}")

        # Динамический импорт и вызов main
        if script_name == "fictional_world_bible.py":
            import fictional_world_bible
            if hasattr(fictional_world_bible, 'main'):
                fictional_world_bible.main()
            else:
                print(f"  ❌ Script {script_name} has no main() function")
                return False

        elif script_name == "fictional_document_generator.py":
            import fictional_document_generator
            if hasattr(fictional_document_generator, 'main'):
                fictional_document_generator.main()
            else:
                print(f"  ❌ Script {script_name} has no main() function")
                return False

        elif script_name == "validate_fictional_corpus.py":
            import validate_fictional_corpus
            if hasattr(validate_fictional_corpus, 'main'):
                validate_fictional_corpus.main()
            else:
                print(f"  ❌ Script {script_name} has no main() function")
                return False
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
    print("🎭 Fictional Universe Document Generator")
    print("=" * 60)
    print("Creating a completely fictional world for RAG testing")
    print("Based on Asterix structure but with original terms")

    # Создаём папки
    output_dir = "fictional_documents"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Шаги генерации
    steps = [
        ("Building fictional world and term mapping", "fictional_world_bible.py"),
        ("Generating 50 interconnected documents", "fictional_document_generator.py"),
        ("Validating corpus quality", "validate_fictional_corpus.py")
    ]

    for desc, script in steps:
        print(f"\n📝 {desc}")
        print("-" * 40)
        success = run_python_script(script)
        if success:
            print("  ✅ Success")
        else:
            print("  ⚠️  Warning: Script had issues")
        time.sleep(0.5)

    # Итоговая информация
    print("\n" + "=" * 60)
    print("🎉 GENERATION COMPLETE!")
    print("=" * 60)

    # Проверяем созданные файлы
    generated_files = []
    for filename in ["fictional_world.json", "terms_map.json", "fictional_index.json",
                     "generation_stats.json", "validation_report.json"]:
        if os.path.exists(filename):
            generated_files.append(filename)

    print(f"\n📁 Generated {len(generated_files)} files:")
    for file in generated_files:
        print(f"  {file}")

    if os.path.exists(output_dir):
        doc_count = len([f for f in os.listdir(output_dir) if f.endswith('.txt')])
        print(f"  {output_dir}/ - {doc_count} document files")

    print("\n🔍 Key Features:")
    print("  • All terms are fictional (no Asterix/Roman names)")
    print("  • Documents have cross-references")
    print("  • Multiple document types (encyclopedia, journal, etc.)")
    print("  • Consistent internal logic")

    print("\n🎯 Perfect for RAG testing because:")
    print("  • Models have no prior knowledge of this universe")
    print("  • Can test true understanding vs. memorization")
    print("  • Cross-document relationships test reasoning")

if __name__ == "__main__":
    main()