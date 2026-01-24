# apps/world2/validate_fictional_corpus.py
import json
import os
import re
from collections import Counter

class FictionalCorpusValidator:
    def __init__(self, knowledge_base_folder="knowledge_base", generated_folder="generated"):
        self.knowledge_base_folder = knowledge_base_folder
        self.generated_folder = generated_folder
        self.documents = []
        self.load_documents()

        # Загружаем маппинг из generated папки
        terms_map_path = os.path.join(generated_folder, "terms_map.json")
        if os.path.exists(terms_map_path):
            with open(terms_map_path, 'r', encoding='utf-8') as f:
                self.terms_map = json.load(f)
        else:
            self.terms_map = {"term_mappings": {}}

    def load_documents(self):
        """Загружает документы из knowledge_base папки"""
        if not os.path.exists(self.knowledge_base_folder):
            print(f"⚠️  Directory '{self.knowledge_base_folder}' not found")
            return

        for filename in os.listdir(self.knowledge_base_folder):
            if filename.endswith('.txt'):
                with open(os.path.join(self.knowledge_base_folder, filename), 'r', encoding='utf-8') as f:
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
        # Получаем термины из terms_map.json
        all_fictional_terms = []

        # Получаем все вымышленные термины из mapping
        if 'categories' in self.terms_map:
            for category, terms_dict in self.terms_map['categories'].items():
                if isinstance(terms_dict, dict):
                    all_fictional_terms.extend(terms_dict.values())

        # Также проверяем term_mappings
        if 'term_mappings' in self.terms_map:
            term_mappings = self.terms_map['term_mappings']
            if isinstance(term_mappings, dict):
                for value in term_mappings.values():
                    if isinstance(value, str):
                        all_fictional_terms.append(value)

        term_usage = Counter()

        for doc in self.documents:
            content_lower = doc['content'].lower()
            for term in all_fictional_terms:
                if isinstance(term, str) and term.lower() in content_lower:
                    term_usage[term] += 1

        print(f"\nFound {len(term_usage)} unique fictional terms used")
        if term_usage:
            print("Top 10 most used fictional terms:")
            print("-" * 40)
            for term, count in term_usage.most_common(10):
                print(f"  {term:25}: {count:3} occurrences")
        else:
            print("⚠️  No fictional terms detected in documents")
            # Показываем примеры терминов, которые должны быть
            print("Example terms that should be present:")
            if 'categories' in self.terms_map:
                for category in ['characters', 'items']:
                    if category in self.terms_map['categories']:
                        terms = list(self.terms_map['categories'][category].values())[:3]
                        print(f"  {category}: {', '.join(terms)}")

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

    def check_document_uniqueness(self):
        """Проверяет уникальность документов"""
        content_hashes = set()
        duplicate_count = 0

        for doc in self.documents:
            # Используем хэш для проверки уникальности
            content_hash = hash(doc['content'][:1000])  # Первые 1000 символов
            if content_hash in content_hashes:
                duplicate_count += 1
                print(f"  ⚠️  Possible duplicate: {doc['id']}")
            content_hashes.add(content_hash)

        if duplicate_count == 0:
            print("✓ All documents appear to be unique")
            return True
        else:
            print(f"⚠️  Found {duplicate_count} possible duplicate documents")
            return False

    def analyze_document_statistics(self):
        """Анализирует статистику документов"""
        print("\nDocument Statistics:")
        print("-" * 40)

        # Типы документов
        doc_types = Counter(doc['type'] for doc in self.documents)
        for doc_type, count in doc_types.items():
            percentage = (count / len(self.documents)) * 100
            print(f"  {doc_type:15}: {count:2} documents ({percentage:.1f}%)")

        # Количество слов
        total_words = sum(len(doc['content'].split()) for doc in self.documents)
        avg_words = total_words / len(self.documents) if self.documents else 0

        print(f"\n  Total documents: {len(self.documents)}")
        print(f"  Total words: {total_words:,}")
        print(f"  Average words per document: {avg_words:.0f}")

        # Проверяем ссылки
        total_refs = sum(len(re.findall(r'\(see document:|\(refer to:|\(detailed in:|\(cf\.', doc['content'])) for doc in self.documents)
        avg_refs = total_refs / len(self.documents) if self.documents else 0

        print(f"  Total cross-references: {total_refs}")
        print(f"  Average references per document: {avg_refs:.2f}")

        return {
            'total_documents': len(self.documents),
            'total_words': total_words,
            'avg_words': avg_words,
            'total_refs': total_refs,
            'avg_refs': avg_refs
        }

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

        # 2. Проверка уникальности
        uniqueness = self.check_document_uniqueness()

        # 3. Анализ использования терминов
        term_usage = self.analyze_term_usage()

        # 4. Проверка ссылок
        broken_refs = self.check_cross_references()

        # 5. Статистика
        stats = self.analyze_document_statistics()

        # 6. Оценка качества
        print("\n" + "=" * 60)
        print("QUALITY ASSESSMENT")
        print("-" * 60)

        score = 0
        if original_free:
            score += 2
            print("✓ Original terms: PASS (2/2)")
        else:
            print("✗ Original terms: FAIL (0/2)")

        if uniqueness:
            score += 2
            print("✓ Document uniqueness: PASS (2/2)")
        else:
            print(f"✗ Document uniqueness: PARTIAL (1/2)")
            score += 1

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

        if stats['avg_refs'] >= 1.0:
            score += 2
            print("✓ Interconnectivity: PASS (2/2)")
        else:
            partial_score = min(2, stats['avg_refs'])
            score += partial_score
            print(f"✗ Interconnectivity: PARTIAL ({partial_score:.1f}/2)")

        print(f"\n  FINAL SCORE: {score}/10 ({score/10*100:.1f}%)")

        report = {
            'original_free': original_free,
            'uniqueness': uniqueness,
            'broken_refs': len(broken_refs),
            'unique_terms': len(term_usage),
            'total_documents': stats['total_documents'],
            'avg_references': stats['avg_refs'],
            'quality_score': score,
            'quality_percentage': score/10*100
        }

        # Сохраняем отчёт в generated папке
        report_path = os.path.join(self.generated_folder, "validation_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Validation report saved to {report_path}")

        return report

def main():
    """Основная функция валидации"""
    print("🔍 Validating Fictional Corpus")
    print("=" * 60)

    validator = FictionalCorpusValidator("knowledge_base", "generated")
    report = validator.generate_coherence_report()

    # Выводим рекомендации
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)

    if report.get('quality_percentage', 0) >= 80:
        print("✅ Corpus quality is EXCELLENT for RAG testing!")
        print("   - Documents are unique and fictional")
        print("   - Good cross-references between documents")
        print("   - No contamination with original terms")
    elif report.get('quality_percentage', 0) >= 60:
        print("⚠️  Corpus quality is ACCEPTABLE for RAG testing")
        print("   - Some minor issues detected")
        print("   - Still usable for testing purposes")
    else:
        print("❌ Corpus quality needs IMPROVEMENT")
        print("   - Significant issues detected")
        print("   - Consider regenerating the corpus")

    print(f"\n📊 Final assessment: {report.get('quality_percentage', 0):.1f}%")

if __name__ == "__main__":
    main()