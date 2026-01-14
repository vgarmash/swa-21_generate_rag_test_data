# document_generator.py
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import yaml
from world_bible import WORLD_DATA

class DocumentGenerator:
    def __init__(self):
        self.world = WORLD_DATA
        self.documents = []
        self.doc_ids = []

    def generate_document_set(self, num_docs=50):
        """Генерирует полный набор документов"""

        # Распределение по типам документов
        doc_distribution = {
            'encyclopedia': 15,
            'journal': 10,
            'report': 10,
            'decree': 5,
            'myth': 5,
            'letter': 5
        }

        # Генерация документов каждого типа
        for doc_type, count in doc_distribution.items():
            for i in range(count):
                doc = self._generate_document(doc_type, i+1)
                self.documents.append(doc)
                self.doc_ids.append(doc['id'])

        # Добавляем перекрестные ссылки
        self._add_cross_references()

        return self.documents

    def _generate_document(self, doc_type: str, index: int):
        """Генерирует один документ заданного типа"""

        doc_id = f"{doc_type.upper()[:4]}_{self._generate_doc_id(doc_type, index)}"

        templates = {
            'encyclopedia': self._encyclopedia_template,
            'journal': self._journal_template,
            'report': self._report_template,
            'decree': self._decree_template,
            'myth': self._myth_template,
            'letter': self._letter_template
        }

        content, metadata = templates[doc_type](doc_id)

        # Добавляем метаданные
        metadata.update({
            'doc_id': doc_id,
            'doc_type': doc_type,
            'generated_date': datetime.now().strftime("%Y-%m-%d")
        })

        # Формируем полный документ
        full_doc = f"---\n{yaml.dump(metadata, default_flow_style=False)}---\n\n{content}"

        return {
            'id': doc_id,
            'type': doc_type,
            'content': full_doc,
            'metadata': metadata,
            'raw_content': content
        }

    def _encyclopedia_template(self, doc_id: str):
        """Шаблон для энциклопедической статьи"""

        topics = [
            ("Magic Potion Properties", "magic_potion"),
            ("Gallic Village Structure", "regions"),
            ("Roman Military Tactics", "organizations"),
            ("Druidic Practices", "characters"),
            ("Menhir Types and Uses", "magic_items")
        ]

        topic, topic_type = random.choice(topics)

        metadata = {
            'title': f"Encyclopedia: {topic}",
            'author': "Gallic Scholars Collective",
            'publication_date': f"{random.randint(45, 50)} BC",
            'keywords': self._get_keywords(topic_type)
        }

        # Генерация содержания
        content = f"# {topic}\n\n"

        if "Magic Potion" in topic:
            content += self._generate_potion_article()
        elif "Gallic Village" in topic:
            content += self._generate_village_article()
        elif "Roman" in topic:
            content += self._generate_roman_article()
        elif "Druidic" in topic:
            content += self._generate_druid_article()
        else:
            content += self._generate_menhir_article()

        # Добавляем раздел "See Also"
        content += "\n\n## See Also\n"
        see_also = random.sample([d for d in self.doc_ids if d != doc_id], min(3, len(self.doc_ids)))
        for doc in see_also:
            content += f"- {doc}\n"

        return content, metadata

    def _journal_template(self, doc_id: str):
        """Шаблон для дневниковой записи"""

        authors = ["Asterix", "Obelix", "Getafix", "Roman_Spy", "Village_Elder"]
        author = random.choice(authors)

        date = datetime(50, 1, 1) + timedelta(days=random.randint(1, 365))

        metadata = {
            'title': f"Journal of {author}",
            'author': author,
            'date': date.strftime("%B %d, %Y BC"),
            'mood': random.choice(["Excited", "Worried", "Happy", "Angry", "Thoughtful"])
        }

        # Генерация дневниковой записи
        content = f"## Entry #{random.randint(1, 50)}\n\n"
        content += f"*Date: {metadata['date']}*\n*Location: {random.choice(['Armorican Village', 'Roman Camp', 'Forest', 'Lutetia'])}*\n\n"

        journal_templates = [
            f"Today we had another encounter with the Romans. {self._get_random_character('roman')} tried to attack our village, but as usual, {self._get_reference('encyclopedia', 'Magic Potion')} made short work of them.",
            f"{self._get_random_character('hero')} and I went menhir hunting today. Found a particularly fine specimen near {self._get_random_location()}. Must remember to avoid the wild boar traps!",
            f"Another feast tonight. As expected, {self._get_random_character('bard')} started singing and had to be restrained. The fish from {self._get_random_character('fishmonger')} was particularly salty today.",
            f"Discussed potion ingredients with {self._get_random_character('druid')}. The mistletoe is particularly potent this season. Note: avoid using oak from the northern grove."
        ]

        content += random.choice(journal_templates)
        content += "\n\n" + self._add_random_observation()

        return content, metadata

    def _report_template(self, doc_id: str):
        """Шаблон для официального отчета"""

        reporters = ["Roman Centurion", "Gallic Scout", "Druid Observer", "Merchant Informant"]
        reporter = random.choice(reporters)

        metadata = {
            'title': f"Military/Scientific Report",
            'author': reporter,
            'classification': random.choice(["CONFIDENTIAL", "INTERNAL", "PUBLIC"]),
            'subject': random.choice(["Magic Potion Analysis", "Village Defenses", "Roman Camp Status"])
        }

        content = f"# REPORT: {metadata['subject']}\n"
        content += f"**Classification:** {metadata['classification']}\n"
        content += f"**Reporter:** {reporter}\n"
        content += f"**Date:** {random.randint(45, 50)} BC\n\n"

        content += "## Executive Summary\n"
        content += self._generate_report_summary()

        content += "\n## Findings\n"
        content += self._generate_report_findings()

        content += "\n## Recommendations\n"
        content += self._generate_report_recommendations()

        content += f"\n\n**References:** {self._get_random_references(2)}"

        return content, metadata

    def _decree_template(self, doc_id: str):
        """Шаблон для указа или закона"""

        authorities = ["Chief Vitalstatistix", "Julius Caesar", "Village Council", "Druid Circle"]
        authority = random.choice(authorities)

        metadata = {
            'title': "Official Decree",
            'authority': authority,
            'effective_date': f"{random.randint(48, 50)} BC",
            'jurisdiction': random.choice(["Armorican Village", "Roman Empire", "All Gaul"])
        }

        decrees = [
            f"By order of {authority}, the consumption of magic potion is restricted to defensive purposes only. Violators will face boar-cleaning duties.",
            f"All menhirs must be properly labeled with delivery information. Unlabeled menhirs will be considered property of {self._get_random_character('chief')}.",
            f"The singing of {self._get_random_character('bard')} is hereby prohibited during feast hours. First offense: warning. Second offense: being tied to a tree.",
            f"Roman soldiers are banned from entering the village without prior permission. Exception: delivery of olive oil and wine."
        ]

        content = f"# DECREE OF {authority.upper()}\n\n"
        content += random.choice(decrees)
        content += f"\n\n**Signed,**\n{authority}"
        content += f"\n\n**Witnessed by:** {self._get_random_witness()}"

        return content, metadata

    def _myth_template(self, doc_id: str):
        """Шаблон для мифа или легенды"""

        myths = [
            ("Origin of Magic Potion", "How Getafix discovered the potion recipe"),
            ("First Menhir", "How the first menhir was created by giants"),
            ("Why Romans Can't Win", "Legend of the village's eternal protection"),
            ("The Singing Bard", "Why Cacofonix was cursed with terrible voice")
        ]

        myth_name, description = random.choice(myths)

        metadata = {
            'title': f"Myth: {myth_name}",
            'storyteller': random.choice(["Village Elder", "Druid Storyteller", "Traveling Bard"]),
            'estimated_age': f"{random.randint(100, 500)} years",
            'region': "Armorica"
        }

        content = f"# The Legend of {myth_name}\n\n"
        content += f"*As told by {metadata['storyteller']}*\n\n"

        myth_stories = {
            "Origin of Magic Potion": "Long before the Romans came, the druid Getafix was studying mistletoe when a lightning bolt struck his cauldron...",
            "First Menhir": "In ancient times, giants roamed the land. When they slept, their fingers turned to stone, creating the first menhirs...",
            "Why Romans Can't Win": "The goddess Toutatis made a pact with the first village chief that as long as they eat wild boar weekly...",
            "The Singing Bard": "Cacofonix was once a great singer, but he insulted the god of music, who cursed him to sing off-key forever..."
        }

        content += myth_stories.get(myth_name, "This is an ancient tale passed down through generations...")
        content += "\n\n**Moral:** " + random.choice([
            "Strength comes from unity, not just potion.",
            "Even giants need to rest sometimes.",
            "Never underestimate a Gaul with a full stomach.",
            "Some curses are blessings in disguise."
        ])

        return content, metadata

    def _letter_template(self, doc_id: str):
        """Шаблон для письма"""

        senders = ["Asterix", "Obelix", "Getafix", "Roman_Soldier", "Village_Merchant"]
        receivers = ["Friend_in_Lutetia", "Roman_Command", "Druid_Circle", "Family"]

        sender = random.choice(senders)
        receiver = random.choice(receivers)

        metadata = {
            'title': f"Personal Letter",
            'from': sender,
            'to': receiver,
            'delivery_method': random.choice(["Messenger pigeon", "Traveling merchant", "Secret agent"]),
            'urgency': random.choice(["Normal", "Urgent", "Secret"])
        }

        content = f"Dear {receiver.replace('_', ' ')},\n\n"

        letters = [
            f"I hope this letter finds you well. Things here in the village are as chaotic as ever. {self._get_random_character('blacksmith')} and {self._get_random_character('fishmonger')} had another fight today.",
            f"Important news! The Romans from {self._get_random_location('roman')} are planning something. Saw them drilling near the forest.",
            f"Need more mistletoe for potion brewing. The harvest from {random.choice(['oak grove', 'sacred forest', 'druid circle'])} was poor this year.",
            f"Obelix delivered another batch of menhirs today. One was so large it broke the village gate! Chief {self._get_random_character('chief')} was not amused."
        ]

        content += random.choice(letters)
        content += f"\n\nRemember what we discussed about {random.choice(['the potion formula', 'Roman movements', 'the next feast'])}."
        content += f"\n\nYours sincerely,\n{sender}"
        content += f"\n\nP.S. {self._add_postscript()}"

        return content, metadata

    def _add_cross_references(self):
        """Добавляет перекрестные ссылки между документами"""
        for i, doc in enumerate(self.documents):
            # Находим подходящие места для ссылок
            content = doc['raw_content']

            # Добавляем 1-3 ссылки на другие документы
            for _ in range(random.randint(1, 3)):
                # Выбираем случайный документ для ссылки (не текущий)
                other_docs = [d for d in self.doc_ids if d != doc['id']]
                if other_docs:
                    ref_doc = random.choice(other_docs)
                    # Находим подходящее место для вставки ссылки
                    sentences = content.split('. ')
                    if len(sentences) > 2:
                        insert_pos = random.randint(1, len(sentences) - 1)
                        ref_text = f" (see: {ref_doc})"
                        sentences[insert_pos] = sentences[insert_pos] + ref_text
                        content = '. '.join(sentences)

            # Обновляем документ
            doc['raw_content'] = content

            # Обновляем полный контент
            metadata_yaml = yaml.dump(doc['metadata'], default_flow_style=False)
            doc['content'] = f"---\n{metadata_yaml}---\n\n{content}"

    # Вспомогательные методы для генерации контента
    def _generate_doc_id(self, doc_type: str, index: int) -> str:
        """Генерирует ID документа"""
        prefixes = {
            'encyclopedia': 'ENCY',
            'journal': 'JOURN',
            'report': 'REP',
            'decree': 'DECR',
            'myth': 'MYTH',
            'letter': 'LETTER'
        }
        return f"{prefixes.get(doc_type, 'DOC')}_{index:03d}"

    def _get_random_character(self, char_type: str = None) -> str:
        """Возвращает случайного персонажа"""
        if char_type:
            chars = [c['name'] for c in self.world['characters'] if char_type in c['type']]
        else:
            chars = [c['name'] for c in self.world['characters']]
        return random.choice(chars) if chars else "Unknown"

    def _get_random_location(self, loc_type: str = None) -> str:
        """Возвращает случайное место"""
        if loc_type == 'roman':
            return random.choice(["Camp Babaorum", "Camp Laudanum", "Rome"])
        return random.choice(["Forest", "Village Square", "Getafix's Hut", "Menhir Quarry"])

    def _get_reference(self, doc_type: str, keyword: str) -> str:
        """Создает ссылку на документ"""
        possible_refs = [doc_id for doc_id in self.doc_ids if doc_type.upper() in doc_id and keyword.lower() in doc_id.lower()]
        if possible_refs:
            return f"(Refer to {random.choice(possible_refs)})"
        return f"(See related documents on {keyword})"

    def _get_random_references(self, count: int) -> str:
        """Возвращает случайные ссылки"""
        if len(self.doc_ids) < count:
            return "No references available"
        refs = random.sample(self.doc_ids, count)
        return ', '.join(refs)

    def _get_keywords(self, topic_type: str) -> list:
        """Генерирует ключевые слова"""
        base_keywords = ["Gaul", "Roman", "Village", "Magic"]
        type_keywords = {
            'magic_potion': ['potion', 'strength', 'mistletoe', 'Getafix'],
            'regions': ['geography', 'location', 'territory'],
            'organizations': ['army', 'government', 'society'],
            'characters': ['people', 'personality', 'biography'],
            'magic_items': ['artifact', 'tool', 'equipment']
        }
        return base_keywords + type_keywords.get(topic_type, [])

    def _get_random_witness(self) -> str:
        """Возвращает случайного свидетеля"""
        witnesses = ["Two village elders", "Roman centurion", "Druid apprentice", "Merchant guild representative"]
        return random.choice(witnesses)

    def _add_random_observation(self) -> str:
        """Добавляет случайное наблюдение"""
        observations = [
            "The wild boar seems particularly plentiful this season.",
            "Noticed Roman scouts near the northern border.",
            "The fish from Unhygienix smells worse than usual.",
            "Cacofonix is practicing a new song. May the gods help us all."
        ]
        return f"*Observation:* {random.choice(observations)}"

    def _add_postscript(self) -> str:
        """Добавляет постскриптум к письму"""
        ps_options = [
            "Don't forget the boar for the feast!",
            "Bring more olive oil next time.",
            "Keep this message secret from Romans.",
            "Obelix says hello (and wants more menhirs)."
        ]
        return random.choice(ps_options)

    # Методы для генерации статей
    def _generate_potion_article(self) -> str:
        return """The Magic Potion is a legendary concoction brewed exclusively by the druid Getafix. 
Its primary ingredient is mistletoe harvested with a golden sickle during the full moon.
Effects include temporary superhuman strength, increased speed, and invulnerability.
Note: Permanent exposure (as in Obelix's case) leads to chronic strength but no other known side effects.
The recipe is a closely guarded secret of the druidic circle."""

    def _generate_village_article(self) -> str:
        return """The Armorican Village is structured around a central square with Chief Vitalstatistix's hut at the highest point.
Key infrastructure includes Getafix's potion laboratory, the menhir quarry, and the fishmonger's stall.
Defense relies on natural forest barriers and the strategic use of magic potion.
Social hierarchy places the chief at the top, followed by warriors, then craftsmen, with the bard (Cacofonix) nominally respected but often restrained."""

    def _generate_roman_article(self) -> str:
        return """Roman military tactics in Gaul involve the construction of fortified camps (Babaorum, Laudanum, etc.) surrounding resistant villages.
Standard procedure includes attempted diplomacy, followed by siege tactics, though neither has succeeded against the Armorican village.
Caesar's forces are known for their discipline, engineering prowess, and persistence despite repeated defeats.
Intelligence gathering remains a challenge due to Gaulish loyalty and the language barrier."""

    def _generate_druid_article(self) -> str:
        return """Druidic practices include herbalism, astronomy, and the preservation of oral history.
The annual gathering at the Forest of the Carnutes is mandatory for all druids.
Getafix is considered among the most skilled, particularly for his mastery of potion brewing.
Druids serve as judges, teachers, and healers in Gallic society, commanding great respect."""

    def _generate_menhir_article(self) -> str:
        return """Menhirs are large, shaped standing stones used for ceremonial purposes and as Obelix's primary trade.
Classification includes: Standard (2m), Grande (3m), and Colossal (4m+).
Quarrying techniques involve careful splitting along natural stone lines.
Delivery logistics remain a mystery, as Obelix transports them single-handedly without visible strain."""

    def _generate_report_summary(self) -> str:
        summaries = [
            "The Gaulish village remains impregnable due to magic potion. Alternative strategies required.",
            "Potion ingredient supply lines identified. Disruption possible but risky.",
            "Internal village conflicts observed between blacksmith and fishmonger. Could be exploitable.",
            "Menhir production continues at unprecedented rates. Economic implications unclear."
        ]
        return random.choice(summaries)

    def _generate_report_findings(self) -> str:
        findings = [
            "1. Magic potion effects last approximately 10 minutes per dose.\n2. Village defenses weakest during feast preparations.\n3. Roman spies have been detected but captured.",
            "1. Obelix's strength appears permanent and non-diminishing.\n2. Getafix obtains mistletoe from three secret locations.\n3. Village morale remains high despite Roman pressure.",
            "1. Fish supply chain vulnerable to interception.\n2. Bard's singing causes measurable discomfort.\n3. Wild boar population stable and abundant."
        ]
        return random.choice(findings)

    def _generate_report_recommendations(self) -> str:
        recommendations = [
            "1. Attempt diplomacy with offers of Roman citizenship.\n2. Research counter-potion with Egyptian alchemists.\n3. Increase surveillance on mistletoe harvests.",
            "1. Exploit internal village conflicts.\n2. Intercept menhir deliveries for intelligence.\n3. Propose cultural exchange including olive oil.",
            "1. Wait for natural generational change in leadership.\n2. Study potion's long-term effects on Obelix.\n3. Establish trade relations to build dependency."
        ]
        return random.choice(recommendations)

# Основной скрипт для генерации
def main():
    print("Generating Asterix universe documents...")

    generator = DocumentGenerator()
    documents = generator.generate_document_set(50)

    # Сохраняем документы в файлы
    for doc in documents:
        filename = f"documents/{doc['id']}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(doc['content'])

    # Сохраняем индекс
    index = []
    for doc in documents:
        index.append({
            'id': doc['id'],
            'type': doc['type'],
            'title': doc['metadata'].get('title', 'Untitled'),
            'author': doc['metadata'].get('author', 'Unknown')
        })

    with open('document_index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    # Генерируем тестовые QA пары
    generate_qa_pairs(documents)

    print(f"Generated {len(documents)} documents in 'documents/' folder")
    print("Index saved to 'document_index.json'")
    print("QA pairs saved to 'qa_pairs.jsonl'")

def generate_qa_pairs(documents):
    """Генерирует тестовые QA пары для RAG"""
    qa_pairs = [
        {
            "question": "What are the main ingredients of Getafix's magic potion?",
            "answer": "The primary ingredient is mistletoe harvested with a golden sickle during the full moon. The full recipe is a druidic secret.",
            "source_docs": ["ENCY_001", "ENCY_010", "REP_005"],
            "difficulty": "easy"
        },
        {
            "question": "Why is Obelix permanently strong?",
            "answer": "Obelix fell into a cauldron of magic potion as a baby, giving him permanent superhuman strength without needing to drink the potion like others.",
            "source_docs": ["ENCY_001", "MYTH_001", "JOURN_003"],
            "difficulty": "medium"
        },
        {
            "question": "What are the names of the Roman camps surrounding the Gaulish village?",
            "answer": "The main Roman camps are Camp Babaorum, Camp Laudanum, Camp Aquarium, and Camp Petibonum.",
            "source_docs": ["ENCY_002", "REP_008", "LETTER_002"],
            "difficulty": "easy"
        },
        {
            "question": "How does the village deal with Cacofonix's singing during feasts?",
            "answer": "Cacofonix is usually tied to a tree or otherwise restrained during feasts to prevent him from singing, as his music is considered terrible.",
            "source_docs": ["DECR_003", "JOURN_005", "LETTER_004"],
            "difficulty": "medium"
        },
        {
            "question": "What is the relationship between Fulliautomatix and Unhygienix?",
            "answer": "They frequently argue and fight, representing the ongoing conflict between the blacksmith and fishmonger trades in the village.",
            "source_docs": ["JOURN_002", "REP_006", "LETTER_001"],
            "difficulty": "hard"
        }
    ]

    with open('qa_pairs.jsonl', 'w', encoding='utf-8') as f:
        for qa in qa_pairs:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    import os
    os.makedirs("documents", exist_ok=True)
    main()