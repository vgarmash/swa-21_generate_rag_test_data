#!/usr/bin/env python3
# run_generation.py - Основной скрипт запуска
import subprocess
import sys
import time

def main():
    print("🚀 Asterix Universe Document Generator")
    print("=" * 50)

    steps = [
        ("Generating world data...", "python world_bible.py"),
        ("Creating documents...", "python document_generator.py"),
        ("Analyzing corpus...", "python analyze_corpus.py")
    ]

    for description, command in steps:
        print(f"\n📝 {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  Warning: Command returned {result.returncode}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:200]}")
            else:
                print("  ✅ Done")
        except Exception as e:
            print(f"  ❌ Failed: {e}")

        time.sleep(0.5)

    print("\n" + "=" * 50)
    print("🎉 Generation complete!")
    print("\n📁 Output structure:")
    print("  documents/        - 50 generated text files")
    print("  document_index.json - Index of all documents")
    print("  qa_pairs.jsonl    - Test QA pairs for RAG")
    print("  corpus_network.json - Visualization data")
    print("\n📊 To visualize the network, use:")
    print("  https://observablehq.com/@d3/force-directed-graph")
    print("  and load corpus_network.json")

if __name__ == "__main__":
    main()