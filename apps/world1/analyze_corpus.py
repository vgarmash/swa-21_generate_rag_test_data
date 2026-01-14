# analyze_corpus.py - Анализ сгенерированного корпуса
import json
import os
import re
from collections import Counter, defaultdict

class CorpusAnalyzer:
    def __init__(self, docs_folder="documents"):
        self.docs_folder = docs_folder
        self.documents = []
        self.load_documents()

    def load_documents(self):
        """Загружает все документы из папки"""
        for filename in os.listdir(self.docs_folder):
            if filename.endswith('.txt'):
                with open(os.path.join(self.docs_folder, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    doc_id = filename.replace('.txt', '')
                    self.documents.append({
                        'id': doc_id,
                        'content': content,
                        'type': doc_id.split('_')[0]
                    })

    def analyze_references(self):
        """Анализирует ссылки между документами"""
        reference_pattern = r'\(see:\s*([A-Z]+_\d+)\)'
        references = defaultdict(list)

        for doc in self.documents:
            matches = re.findall(reference_pattern, doc['content'])
            references[doc['id']] = matches

        # Статистика
        total_refs = sum(len(refs) for refs in references.values())
        avg_refs = total_refs / len(self.documents) if self.documents else 0

        print(f"Total documents: {len(self.documents)}")
        print(f"Total references: {total_refs}")
        print(f"Average references per document: {avg_refs:.2f}")

        # Документы с наибольшим количеством ссылок
        print("\nTop 5 documents with most references:")
        sorted_docs = sorted(references.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        for doc_id, refs in sorted_docs:
            print(f"  {doc_id}: {len(refs)} references")

        return references

    def analyze_document_types(self):
        """Анализирует распределение по типам документов"""
        type_counter = Counter(doc['type'] for doc in self.documents)

        print("\nDocument type distribution:")
        for doc_type, count in type_counter.items():
            percentage = (count / len(self.documents)) * 100
            print(f"  {doc_type}: {count} documents ({percentage:.1f}%)")

        return dict(type_counter)

    def find_broken_links(self):
        """Находит битые ссылки (ссылки на несуществующие документы)"""
        all_doc_ids = set(doc['id'] for doc in self.documents)
        reference_pattern = r'\(see:\s*([A-Z]+_\d+)\)'
        broken_links = []

        for doc in self.documents:
            matches = re.findall(reference_pattern, doc['content'])
            for ref in matches:
                if ref not in all_doc_ids:
                    broken_links.append((doc['id'], ref))

        if broken_links:
            print(f"\nFound {len(broken_links)} broken links:")
            for source, target in broken_links[:10]:  # Показываем первые 10
                print(f"  {source} -> {target} (missing)")
        else:
            print("\nNo broken links found!")

        return broken_links

    def generate_network_graph(self):
        """Генерирует данные для графа связей"""
        references = self.analyze_references()

        nodes = []
        links = []

        for doc in self.documents:
            nodes.append({
                'id': doc['id'],
                'type': doc['type'],
                'group': 1 if 'ENCY' in doc['id'] else 2 if 'JOURN' in doc['id'] else 3
            })

        for source, targets in references.items():
            for target in targets:
                links.append({
                    'source': source,
                    'target': target,
                    'value': 1
                })

        graph_data = {
            'nodes': nodes,
            'links': links
        }

        with open('corpus_network.json', 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2)

        print("\nNetwork graph saved to 'corpus_network.json'")
        return graph_data

    def run_full_analysis(self):
        """Запускает полный анализ корпуса"""
        print("=" * 60)
        print("CORPUS ANALYSIS REPORT")
        print("=" * 60)

        self.analyze_document_types()
        print("-" * 60)
        self.analyze_references()
        print("-" * 60)
        self.find_broken_links()
        print("-" * 60)
        self.generate_network_graph()

if __name__ == "__main__":
    analyzer = CorpusAnalyzer()
    analyzer.run_full_analysis()