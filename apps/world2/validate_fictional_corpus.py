# apps/world2/validate_fictional_corpus.py
import json
import os
import re
from collections import Counter

class FictionalCorpusValidator:
    def __init__(self, docs_folder="fictional_documents"):
        self.docs_folder = docs_folder
        self.documents = []
        self.load_documents()

        # Загружаем маппинг
        if os.path.exists('terms_map.json'):
            with open('terms_map.json', 'r', encoding='utf-8') as f:
                self.terms_map = json.load(f)
        else:
            self.terms_map = {"term_mappings": {}}

    def load_documents(self):
        """Загружает документы"""
        if not os.path.exists(self.docs_folder):
            print(f"⚠️  Directory '{self.docs_folder}' not found")
            return

        for filename in os.listdir(self.docs_folder):
            if filename.endswith('.txt'):
                with open(os.path.join(self.docs_folder, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.documents.append({
                        'id': filename.replace('.txt', ''),
                        'content': content,
                        'type': filename.split('_')[0]
                    })

    def check_for_original_terms(self):
        """Проверяет, не остались ли оригинальные термины Астерикса"""
        original_terms = [
            'Asterix', 'Obelix', 'Getafix', 'Vitalstatistix', 'Cacofonix',
            'Gaul', 'Rome', 'Roman', 'mistletoe', 'boar', 'druid',
            'Babaorum', 'Laudanum', 'Aquarium', 'Petibonum'
        ]

        found_terms = {}

        for doc in self.documents:
            content_lower = doc['content'].lower()
            for term in original_terms:
                if term.lower() in content_lower:
                    found_terms.setdefault(term, []).append(doc['id'])

        if found_terms:
            print("⚠️  Found original Asterix terms:")
            for term, docs in found_terms.items():
                print(f"  '{term}' in documents: {', '.join(docs[:3])}{'...' if len(docs) > 3 else ''}")
            return False
        else:
            print("✓ No original Asterix terms found")
            return True

    def analyze_term_usage(self):
        """Анализирует использование вымышленных терминов"""
        term_mappings = self.terms_map.get('term_mappings', {})
        all_fictional_terms = []

        # Собираем все вымышленные термины
        for value in term_mappings.values():
            if isinstance(value, dict):
                all_fictional_terms.extend(value.values())
            elif isinstance(value, str):
                all_fictional_terms.append(value)

        term_usage = Counter()

        for doc in self.documents:
            for term in all_fictional_terms:
                if term in doc['content']:
                    term_usage[term] += 1

        print("\nTop 10 most used fictional terms:")
        print("-" * 40)
        for term, count in term_usage.most_common(10):
            print(f"  {term:25}: {count:3} occurrences")

        return term_usage

    def check_cross_references(self):
        """Проверяет перекрёстные ссылки"""
        ref_pattern = r'\(see document: ([A-Z]+_\d+)\)|\(refer to: ([A-Z]+_\d+)\)|\(detailed in: ([A-Z]+_\d+)\)|\(cf\. ([A-Z]+_\d+)\)'

        all_doc_ids = {doc['id'] for doc in self.documents}
        broken_refs = []

        for doc in self.documents:
            matches = re.findall(ref_pattern, doc['content'])
            for match in matches:
                ref_id = next((m for m in match if m), None)
                if ref_id and ref_id not in all_doc_ids:
                    broken_refs.append((doc['id'], ref_id))

        if broken_refs:
            print(f"\n⚠️  Found {len(broken_refs)} broken references:")
            for source, target in broken_refs[:5]:
                print(f"  {source} -> {target} (missing)")
        else:
            print("\n✓ All cross-references are valid")

        return broken_refs

    def generate_coherence_report(self):
        """Генерирует отчёт о связности корпуса"""
        print("=" * 60)
        print("FICTION CORPUS VALIDATION REPORT")
        print("=" * 60)

        if not self.documents:
            print("⚠️  No documents found. Please generate documents first.")
            return {"error": "No documents found"}

        # 1. Проверка на оригинальные термины
        original_free = self.check_for_original_terms()

        # 2. Анализ использования терминов
        term_usage = self.analyze_term_usage()

        # 3. Проверка ссылок
        broken_refs = self.check_cross_references()

        # 4. Общая статистика
        print("\n" + "=" * 60)
        print("CORPUS STATISTICS")
        print("-" * 60)

        doc_types = Counter(doc['type'] for doc in self.documents)
        for doc_type, count in doc_types.items():
            percentage = (count / len(self.documents)) * 100
            print(f"  {doc_type:15}: {count:2} documents ({percentage:.1f}%)")

        total_refs = sum(len(re.findall(r'\(see document:|\(refer to:|\(detailed in:|\(cf\.', doc['content'])) for doc in self.documents)
        avg_refs = total_refs / len(self.documents) if self.documents else 0

        print(f"\n  Total documents: {len(self.documents)}")
        print(f"  Total references: {total_refs}")
        print(f"  Avg references/doc: {avg_refs:.2f}")
        print(f"  Unique fictional terms: {len(term_usage)}")

        # 5. Оценка качества
        print("\n" + "=" * 60)
        print("QUALITY ASSESSMENT")
        print("-" * 60)

        score = 0
        if original_free:
            score += 2
            print("✓ Original terms: PASS (2/2)")
        else:
            print("✗ Original terms: FAIL (0/2)")

        if not broken_refs:
            score += 2
            print("✓ Cross-references: PASS (2/2)")
        else:
            deduction = min(2, len(broken_refs) / 10)
            score += (2 - deduction)
            print(f"✗ Cross-references: PARTIAL ({2 - deduction:.1f}/2)")

        if len(term_usage) >= 20:
            score += 2
            print("✓ Term diversity: PASS (2/2)")
        else:
            partial_score = min(2, len(term_usage) / 10)
            score += partial_score
            print(f"✗ Term diversity: PARTIAL ({partial_score:.1f}/2)")

        if avg_refs >= 1.0:
            score += 2
            print("✓ Interconnectivity: PASS (2/2)")
        else:
            partial_score = min(2, avg_refs)
            score += partial_score
            print(f"✗ Interconnectivity: PARTIAL ({partial_score:.1f}/2)")

        print(f"\n  FINAL SCORE: {score}/8 ({score/8*100:.1f}%)")

        return {
            'original_free': original_free,
            'broken_refs': len(broken_refs),
            'unique_terms': len(term_usage),
            'avg_references': avg_refs,
            'quality_score': score
        }

def main():
    """Основная функция валидации"""
    print("🔍 Validating Fictional Corpus")
    print("=" * 60)

    validator = FictionalCorpusValidator()
    report = validator.generate_coherence_report()

    # Сохраняем отчёт
    with open('validation_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n✓ Validation report saved to 'validation_report.json'")

if __name__ == "__main__":
    main()