#!/usr/bin/env python3
# test_all.py - тестирует оба мира
import sys
import os

def test_world1():
    """Тестирует world1"""
    print("\n" + "="*60)
    print("TESTING WORLD 1 (Original Asterix World)")
    print("="*60)

    world1_path = os.path.join(os.path.dirname(__file__), "apps", "world1")
    sys.path.insert(0, world1_path)

    try:
        # Тестируем импорты
        from world_bible import WORLD_DATA
        print("✓ world_bible.py imports successfully")

        from document_generator import DocumentGenerator
        print("✓ document_generator.py imports successfully")

        from analyze_corpus import CorpusAnalyzer
        print("✓ analyze_corpus.py imports successfully")

        print("\n✓ World 1: All imports OK!")
        return True

    except Exception as e:
        print(f"✗ World 1 import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_world2():
    """Тестирует world2"""
    print("\n" + "="*60)
    print("TESTING WORLD 2 (Fictional World)")
    print("="*60)

    world2_path = os.path.join(os.path.dirname(__file__), "apps", "world2")
    sys.path.insert(0, world2_path)

    try:
        # Тестируем импорты
        from fictional_world_bible import FictionalWorldBuilder, main as world_main
        print("✓ fictional_world_bible.py imports successfully")

        from fictional_document_generator import FictionalDocumentGenerator, main as doc_main
        print("✓ fictional_document_generator.py imports successfully")

        from validate_fictional_corpus import FictionalCorpusValidator, main as validate_main
        print("✓ validate_fictional_corpus.py imports successfully")

        # Проверяем, что есть main функции
        print("\n✓ World 2: All imports OK!")
        return True

    except Exception as e:
        print(f"✗ World 2 import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Testing both RAG test data generators...")

    success1 = test_world1()
    success2 = test_world2()

    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)

    if success1 and success2:
        print("✓ BOTH WORLDS ARE READY!")
        print("\nTo generate World 1 (Asterix):")
        print("  python run_world1.py")
        print("\nTo generate World 2 (Fictional):")
        print("  python run_world2.py")
    else:
        print("✗ SOME TESTS FAILED")

    return success1 and success2

if __name__ == "__main__":
    sys.exit(0 if main() else 1)