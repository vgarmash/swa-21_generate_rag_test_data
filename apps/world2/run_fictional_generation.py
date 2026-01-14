#!/usr/bin/env python3
# run_fictional_generation.py
import subprocess
import time
import os

def run_step(description, command):
    print(f"\n📝 {description}")
    print("-" * 40)
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ⚠️  Warning: Exit code {result.returncode}")
            if result.stderr:
                print(f"  Stderr: {result.stderr[:200]}")
        else:
            print("  ✅ Success")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    time.sleep(0.5)

def main():
    print("🎭 Fictional Universe Document Generator")
    print("=" * 60)
    print("Creating a completely fictional world for RAG testing")
    print("Based on Asterix structure but with original terms")

    # Создаём папки
    os.makedirs("fictional_documents", exist_ok=True)

    # Шаги генерации
    steps = [
        ("Building fictional world and term mapping", "python fictional_world_bible.py"),
        ("Generating 50 interconnected documents", "python fictional_document_generator.py"),
        ("Validating corpus quality", "python validate_fictional_corpus.py")
    ]

    for desc, cmd in steps:
        run_step(desc, cmd)

    # Итоговая информация
    print("\n" + "=" * 60)
    print("🎉 GENERATION COMPLETE!")
    print("=" * 60)

    print("\n📁 Generated Files:")
    print("  fictional_world.json    - Complete world data")
    print("  terms_map.json          - Mapping from Asterix to fictional terms")
    print("  fictional_documents/    - 50 generated text files")
    print("  fictional_index.json    - Document index")
    print("  generation_stats.json   - Generation statistics")
    print("  validation_report.json  - Quality assessment")

    print("\n🔍 Key Features:")
    print("  • All terms are fictional (no Asterix/Roman names)")
    print("  • Documents have cross-references")
    print("  • Multiple document types (encyclopedia, journal, etc.)")
    print("  • Consistent internal logic")

    print("\n🎯 Perfect for RAG testing because:")
    print("  • Models have no prior knowledge of this universe")
    print("  • Can test true understanding vs. memorization")
    print("  • Cross-document relationships test reasoning")

    print("\n📊 To use with RAG:")
    print("  1. Load documents from fictional_documents/")
    print("  2. Use terms_map.json to understand mappings")
    print("  3. Test with questions about Veridonia universe")

if __name__ == "__main__":
    main()