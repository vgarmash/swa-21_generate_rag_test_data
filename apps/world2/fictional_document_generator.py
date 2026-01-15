# apps/world2/fictional_document_generator.py
import json
import random
import yaml
from datetime import datetime, timedelta
import os

# Исправляем импорт
try:
    from .fictional_world_bible import FictionalWorldBuilder
except ImportError:
    from fictional_world_bible import FictionalWorldBuilder

class FictionalDocumentGenerator:
    def __init__(self):
        # Загружаем вымышленный мир
        builder = FictionalWorldBuilder()
        self.world_data, _ = builder.build_world()
        self.terms_map = builder.categories

        self.documents = []
        self.doc_ids = []
        self.fictional_to_original = self._reverse_mapping()

    def _reverse_mapping(self):
        """Создаёт обратный маппинг для отладки"""
        reverse = {}
        for category, mappings in self.terms_map.items():
            for original, fictional in mappings.items():
                reverse[fictional] = original
        return reverse

    def get_fictional(self, original_term, category=None):
        """Возвращает вымышленный термин для оригинального"""
        if category and category in self.terms_map:
            return self.terms_map.get(category, {}).get(original_term, original_term)

        # Ищем во всех категориях
        for cat in self.terms_map.values():
            if isinstance(cat, dict) and original_term in cat:
                return cat[original_term]

        return original_term

    def get_character(self, role):
        """Получает вымышленного персонажа по роли"""
        for char in self.world_data["characters"]:
            if char["type"] == role:
                return char["fictional_name"]
        return role

    def generate_document_set(self, num_docs=50):
        """Генерирует полный набор документов"""

        doc_distribution = {
            'encyclopedia': 15,
            'journal': 10,
            'report': 10,
            'decree': 5,
            'myth': 5,
            'letter': 5
        }

        for doc_type, count in doc_distribution.items():
            for i in range(count):
                doc = self._generate_document(doc_type, i+1)
                self.documents.append(doc)
                self.doc_ids.append(doc['id'])

        self._add_cross_references()
        return self.documents

    def _generate_document(self, doc_type, index):
        """Генерирует один документ с вымышленными терминами"""

        doc_id = f"{doc_type.upper()[:4]}_{index:03d}"

        templates = {
            'encyclopedia': self._encyclopedia_template,
            'journal': self._journal_template,
            'report': self._report_template,
            'decree': self._decree_template,
            'myth': self._myth_template,
            'letter': self._letter_template
        }

        content, metadata = templates[doc_type](doc_id)

        metadata.update({
            'doc_id': doc_id,
            'doc_type': doc_type,
            'universe': self.world_data['fictional_universe'],
            'generated_date': datetime.now().strftime("%Y-%m-%d"),
            'contains_fictional_terms': True
        })

        full_doc = f"---\n{yaml.dump(metadata, default_flow_style=False)}---\n\n{content}"

        return {
            'id': doc_id,
            'type': doc_type,
            'content': full_doc,
            'metadata': metadata,
            'raw_content': content
        }

    def _encyclopedia_template(self, doc_id):
        """Энциклопедическая статья с вымышленными терминами"""

        topics = [
            ("Properties of Sunstone Elixir", "alchemy"),
            ("Structure of Oakhaven Settlement", "geography"),
            ("Imperial Military Organization", "military"),
            ("Lorekeeper Practices and Rituals", "culture"),
            ("Types of Standing Stones", "archeology")
        ]

        topic, topic_type = random.choice(topics)

        metadata = {
            'title': f"Encyclopedia: {topic}",
            'author': "Emerald Valley Scholars",
            'publication_date': f"{random.randint(45, 50)} AS (After Settlement)",
            'keywords': ["Veridonia", "fictional", topic_type]
        }

        content = f"# {topic}\n\n"

        if "Sunstone" in topic:
            content += self._generate_elixir_article()
        elif "Oakhaven" in topic:
            content += self._generate_settlement_article()
        elif "Imperial" in topic:
            content += self._generate_imperial_military_article()  # Исправлено название!
        elif "Lorekeeper" in topic:
            content += self._generate_lorekeeper_article()
        else:
            content += self._generate_stones_article()

        # Добавляем раздел "Related Documents"
        content += "\n\n## Related Documents\n"
        related = random.sample([d for d in self.doc_ids if d != doc_id], min(3, len(self.doc_ids)))
        for doc in related:
            content += f"- {doc}\n"

        return content, metadata

    def _generate_elixir_article(self):
        hero = self.get_character("hero")
        strong_hero = self.get_character("strong_hero")
        alchemist = self.get_character("alchemist")
        elixir = self.get_fictional("Magic Potion", "items")
        herb = self.get_fictional("mistletoe", "terms")

        return f"""The {elixir} is a legendary concoction prepared exclusively by the Lorekeeper {alchemist}. 
Its primary ingredient is {herb} harvested with a silver crescent during the twin suns' alignment.
Effects include temporary enhanced vitality, accelerated movement, and temporary resilience.
Chronic exposure (as in the case of {strong_hero}) leads to permanent strength but requires frequent nourishment.
The formula is a closely guarded secret of the Lorekeeper Circle. {hero} uses it strategically during Imperial encounters."""

    def _generate_settlement_article(self):
        chief = self.get_character("chief")
        blacksmith = self.get_character("blacksmith")
        fisher = self.get_character("fisher")
        bard = self.get_character("bard")

        return f"""Oakhaven is structured around a central plaza with Chief {chief}'s longhouse at the highest elevation.
Key structures include the Alchemist's tower, the stone circle quarry, and the fishery.
Defensive strategy relies on natural valley topography and strategic use of the Sunstone Elixir.
Social structure places the chief atop, followed by defenders, then artisans, with the minstrel {bard} enjoying ceremonial status but often being restrained during gatherings.
Notable conflicts frequently occur between {blacksmith} and {fisher} over trade disputes."""

    def _generate_imperial_military_article(self):  # Исправленное название метода
        """Статья об имперской армии"""
        return f"""Imperial military tactics involve constructing fortified outposts (Argentum, Ferrum, etc.) around resistant settlements.
Standard procedure includes diplomatic overtures followed by siege tactics, though neither has succeeded against Oakhaven.
Imperial forces are noted for discipline, engineering capabilities, and persistence despite repeated setbacks.
Intelligence collection remains challenging due to Valefolk loyalty and dialect barriers."""

    def _generate_lorekeeper_article(self):
        alchemist = self.get_character("alchemist")
        return f"""Lorekeeper practices encompass herbalism, celestial observation, and oral tradition preservation.
The annual convocation at the Crystalwood Grove is mandatory for all Lorekeepers.
{alchemist} is regarded among the most adept, particularly for elixir mastery.
Lorekeepers serve as arbiters, instructors, and healers in Valefolk society, commanding significant respect."""

    def _generate_stones_article(self):
        strong_hero = self.get_character("strong_hero")
        return f"""Standing stones are large, shaped monoliths used ceremonially and as {strong_hero}'s primary trade.
Classification includes: Standard (2m), Grande (3m), and Colossal (4m+).
Quarrying techniques involve precise fracturing along natural stone planes.
Transport logistics remain enigmatic, as {strong_hero} conveys them single-handedly without apparent exertion."""

    def _journal_template(self, doc_id):
        """Дневниковая запись"""

        authors = [
            self.get_character("hero"),
            self.get_character("strong_hero"),
            self.get_character("alchemist"),
            "Imperial Observer",
            "Valley Elder"
        ]
        author = random.choice(authors)

        date = f"{random.choice(['First', 'Second', 'Third'])} Moon, {random.randint(1, 300)} AS"

        metadata = {
            'title': f"Personal Journal of {author}",
            'author': author,
            'date': date,
            'location': random.choice(["Oakhaven", "Fort Argentum", "Whispering Woods", "Silverport"]),
            'weather': random.choice(["Sunny", "Misty", "Rainy", "Clear night"])
        }

        content = f"## Entry #{random.randint(1, 50)}\n\n"
        content += f"*Date: {metadata['date']}*\n"
        content += f"*Location: {metadata['location']}*\n"
        content += f"*Weather: {metadata['weather']}*\n\n"

        # Шаблоны записей с вымышленными терминами
        entry_templates = [
            f"Today brought another Imperial patrol near the valley rim. Legate Valerius attempted to approach, but as usual, the {self.get_fictional('Magic Potion', 'items')} made our defense effortless. The Imperials retreated to Fort Argentum.",
            f"{self.get_character('hero')} and I went to gather standing stones today. Found a remarkable monolith near the Whispering Woods. Must remember the locations of crystal-fox dens!",
            f"Community gathering tonight. Predictably, {self.get_character('bard')} began his ballad and had to be escorted out. The catch from {self.get_character('fisher')} was unusually brine-heavy today.",
            f"Discussed herb cultivation with {self.get_character('alchemist')}. The {self.get_fictional('mistletoe', 'terms')} is particularly potent this season. Note: avoid specimens from the northern grove—they induce drowsiness."
        ]

        content += random.choice(entry_templates)
        content += f"\n\n**Personal note:** {self._add_personal_reflection()}"

        return content, metadata

    def _add_personal_reflection(self):
        reflections = [
            f"The {self.get_fictional('Wild Boar', 'items')} roast was exceptionally flavorful tonight.",
            f"Noticed Imperial scouts mapping the eastern pass.",
            f"The forge-smoke from {self.get_character('blacksmith')}'s workshop carries a distinctive metallic scent lately.",
            f"{self.get_character('bard')} is composing a new epic. May the twin suns grant us patience."
        ]
        return random.choice(reflections)

    def _report_template(self, doc_id):
        """Официальный отчёт"""

        reporters = ["Imperial Legate", "Valley Scout", "Lorekeeper Scribe", "Merchant Informant"]
        reporter = random.choice(reporters)

        subjects = [
            f"Analysis of {self.get_fictional('Magic Potion', 'items')}",
            "Oakhaven Defensive Capabilities",
            "Status of Imperial Outposts",
            f"Effects of {self.get_fictional('The Great Accord', 'events')}"
        ]

        metadata = {
            'title': "Official Field Report",
            'author': reporter,
            'classification': random.choice(["RESTRICTED", "EYES ONLY", "CIRCULATION LIMITED"]),
            'subject': random.choice(subjects),
            'report_id': f"RPT-{random.randint(1000, 9999)}"
        }

        content = f"# FIELD REPORT: {metadata['subject']}\n"
        content += f"**Classification:** {metadata['classification']}\n"
        content += f"**Author:** {reporter}\n"
        content += f"**Report ID:** {metadata['report_id']}\n"
        content += f"**Date:** {random.randint(1, 30)} of Harvest Moon, {random.randint(290, 300)} AS\n\n"

        content += "## Executive Assessment\n"
        content += self._generate_report_assessment()

        content += "\n## Detailed Observations\n"
        content += self._generate_observations()

        content += "\n## Strategic Recommendations\n"
        content += self._generate_recommendations()

        # Добавляем случайные ссылки
        if self.doc_ids:
            refs = random.sample(self.doc_ids, min(2, len(self.doc_ids)))
            content += f"\n\n**Cross-references:** {', '.join(refs)}"

        return content, metadata

    def _generate_report_assessment(self):
        assessments = [
            f"The settlement remains resilient primarily due to {self.get_fictional('Magic Potion', 'items')}. Alternative approaches under review.",
            f"Supply routes for {self.get_fictional('mistletoe', 'terms')} identified. Disruption feasible but carries diplomatic risk.",
            f"Internal tensions observed between {self.get_character('blacksmith')} and {self.get_character('fisher')}. Potential leverage point.",
            f"Production of standing stones continues at notable volume. Economic implications require further study."
        ]
        return random.choice(assessments)

    def _generate_observations(self):
        findings = [
            "1. Elixir effects last approximately 10 minutes per dose.\n2. Settlement defenses weakest during gathering preparations.\n3. Imperial agents have been detected but captured.",
            "1. Megalix's strength appears permanent and non-diminishing.\n2. Alchemix obtains moonleaf from three secret locations.\n3. Settlement morale remains high despite Imperial pressure.",
            "1. Fish supply chain vulnerable to interception.\n2. Minstrel's singing causes measurable discomfort.\n3. Forest stag population stable and abundant."
        ]
        return random.choice(findings)

    def _generate_recommendations(self):
        recommendations = [
            "1. Attempt diplomacy with offers of Imperial citizenship.\n2. Research counter-elixir with alchemists.\n3. Increase surveillance on moonleaf harvests.",
            "1. Exploit internal settlement conflicts.\n2. Intercept stone deliveries for intelligence.\n3. Propose cultural exchange including olive oil.",
            "1. Wait for natural generational change in leadership.\n2. Study elixir's long-term effects on Megalix.\n3. Establish trade relations to build dependency."
        ]
        return random.choice(recommendations)

    def _decree_template(self, doc_id):
        """Официальный указ"""

        authorities = [
            self.get_character("chief"),
            "Imperial Proconsul",
            "Council of Elders",
            "Lorekeeper Assembly"
        ]
        authority = random.choice(authorities)

        metadata = {
            'title': "Proclamation of Authority",
            'authority': authority,
            'effective_date': f"{random.choice(['Immediately', 'Next moon cycle', 'At dawn'])}",
            'jurisdiction': random.choice(["Emerald Valley", "Imperial Territories", "Allied Settlements"]),
            'seal': random.choice(["Oak Tree Seal", "Iron Eagle Seal", "Twin Suns Seal"])
        }

        decrees = [
            f"By the authority of {authority}, consumption of the Sunstone Elixir is restricted to defensive actions only. Violators shall perform quarry-clearing duties.",
            f"All standing stones must bear quarry-marks and delivery records. Unmarked stones revert to ownership of Chief {self.get_character('chief')}.",
            f"The musical performances of {self.get_character('bard')} are prohibited during formal gatherings. First offense: warning. Second offense: temporary tree-binding.",
            f"Imperial personnel are forbidden from entering Oakhaven without advance permission. Exception: delivery of olive oil and amphorae."
        ]

        content = f"# PROCLAMATION\n\n"
        content += f"**Seal:** {metadata['seal']}\n"
        content += f"**Authority:** {authority}\n"
        content += f"**Effective:** {metadata['effective_date']}\n\n"
        content += random.choice(decrees)
        content += f"\n\n**Attested by:** {self._get_witness()}\n"
        content += f"**Date recorded:** {random.randint(1,30)} / {random.randint(290,300)} AS"

        return content, metadata

    def _get_witness(self):
        witnesses = [
            "Two elders of the valley",
            "Imperial quartermaster",
            "Lorekeeper apprentice",
            "Guild representative"
        ]
        return random.choice(witnesses)

    def _myth_template(self, doc_id):
        """Миф или легенда"""

        myths = [
            ("Origin of the Sunstone Elixir", "alchemy"),
            ("The First Standing Stone", "archeology"),
            ("Why the Imperials Cannot Conquer", "history"),
            ("The Minstrel's Curse", "folklore")
        ]

        myth_name, myth_type = random.choice(myths)

        metadata = {
            'title': f"Legend: {myth_name}",
            'storyteller': random.choice(["Valley Elder", "Lorekeeper Chronicler", "Traveling Skald"]),
            'estimated_origin': f"{random.randint(500, 1000)} years before settlement",
            'region': "Emerald Valley",
            'myth_type': myth_type
        }

        content = f"# The Tale of {myth_name}\n\n"
        content += f"*As recounted by {metadata['storyteller']}*\n\n"

        myth_stories = {
            "Origin of the Sunstone Elixir": f"Before the Imperials came, the Lorekeeper {self.get_character('alchemist')} was studying {self.get_fictional('mistletoe', 'terms')} when twin sunbeams converged on his alembic...",
            "The First Standing Stone": "In elder times, earth-giants walked the land. Where they paused to rest, their shadows petrified into the first standing stones...",
            "Why the Imperials Cannot Conquer": f"The spirit of the valley made pact with the first chieftain that so long as they honor the {self.get_fictional('Wild Boar', 'items')} feast...",
            "The Minstrel's Curse": f"{self.get_character('bard')} was once the realm's finest singer, but he mocked the Muse of Harmony, who twisted his melodies forever..."
        }

        content += myth_stories.get(myth_name, "This ancient narrative passes through generations...")
        content += f"\n\n**Lesson:** {random.choice([
            'True strength flows from unity, not elixirs.',
            'Even giants must sometimes stand still.',
            'Never underestimate valley-dwellers after a feast.',
            'Some curses conceal unexpected blessings.'
        ])}"

        return content, metadata

    def _letter_template(self, doc_id):
        """Личное письмо"""

        senders = [
            self.get_character("hero"),
            self.get_character("strong_hero"),
            self.get_character("alchemist"),
            "Imperial Despatch",
            "Valley Merchant"
        ]

        receivers = [
            "Friend in Silverport",
            "Imperial Command",
            "Lorekeeper Circle",
            "Kinsfolk"
        ]

        sender = random.choice(senders)
        receiver = random.choice(receivers)

        metadata = {
            'title': "Private Correspondence",
            'from': sender,
            'to': receiver,
            'delivery': random.choice(["Carrier hawk", "Trusted caravan", "Coded message"]),
            'urgency': random.choice(["Routine", "Urgent", "Confidential"])
        }

        content = f"To {receiver},\n\n"

        letters = [
            f"I trust this finds you well. Matters here proceed with usual vigor. {self.get_character('blacksmith')} and {self.get_character('fisher')} had another dispute today over trade rights.",
            f"Critical intelligence: Imperials from Fort Ferrum are preparing an excursion. Observed drilling near the western woods.",
            f"Require additional {self.get_fictional('mistletoe', 'terms')} for elixir preparation. The yield from the {random.choice(['sunlit grove', 'sacred copse', 'elder circle'])} was meager this season.",
            f"{self.get_character('strong_hero')} delivered another load of standing stones today. One monolith was so massive it cracked the gate lintel! Chief {self.get_character('chief')} expressed measured displeasure."
        ]

        content += random.choice(letters)
        content += f"\n\nRecall our discussion regarding {random.choice(['the elixir formula', 'Imperial movements', 'the upcoming gathering'])}."
        content += f"\n\nIn fellowship,\n{sender}"
        content += f"\n\nP.S. {self._add_postscript()}"

        return content, metadata

    def _add_postscript(self):
        ps_options = [
            f"Do not forget the {self.get_fictional('Wild Boar', 'items')} for the gathering!",
            "Bring more olive amphorae next caravan.",
            "Burn this after reading—Imperials intercept messages.",
            f"{self.get_character('strong_hero')} sends greetings (and requests more standing stones)."
        ]
        return random.choice(ps_options)

    def _add_cross_references(self):
        """Добавляет перекрёстные ссылки между документами"""
        reference_phrases = [
            " (see document: {})",
            " (refer to: {})",
            " (detailed in: {})",
            " (cf. {})"
        ]

        for doc in self.documents:
            content = doc['raw_content']
            sentences = [s.strip() for s in content.split('. ') if s.strip()]

            if len(sentences) > 3:
                # Выбираем 1-2 предложения для добавления ссылок
                for _ in range(random.randint(1, 2)):
                    insert_idx = random.randint(1, len(sentences)-2)
                    if self.doc_ids:
                        ref_doc = random.choice([d for d in self.doc_ids if d != doc['id']])
                        phrase = random.choice(reference_phrases).format(ref_doc)
                        sentences[insert_idx] = sentences[insert_idx] + phrase

                doc['raw_content'] = '. '.join(sentences)

                # Обновляем полный контент
                metadata_yaml = yaml.dump(doc['metadata'], default_flow_style=False)
                doc['content'] = f"---\n{metadata_yaml}---\n\n{doc['raw_content']}"

    def save_documents(self, folder="fictional_documents"):
        """Сохраняет документы в файлы"""
        os.makedirs(folder, exist_ok=True)

        for doc in self.documents:
            filename = f"{folder}/{doc['id']}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(doc['content'])

        # Сохраняем индекс
        index = []
        for doc in self.documents:
            index.append({
                'id': doc['id'],
                'type': doc['type'],
                'title': doc['metadata'].get('title', 'Untitled'),
                'author': doc['metadata'].get('author', 'Unknown')
            })

        with open('fictional_index.json', 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        # Сохраняем статистику
        stats = {
            'total_documents': len(self.documents),
            'by_type': {},
            'universe': self.world_data['fictional_universe'],
            'generation_date': datetime.now().isoformat()
        }

        for doc in self.documents:
            doc_type = doc['type']
            stats['by_type'][doc_type] = stats['by_type'].get(doc_type, 0) + 1

        with open('generation_stats.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        return len(self.documents)

def main():
    """Основная функция генерации документов"""
    print("Generating fictional universe documents...")
    print("=" * 60)

    # 1. Создаём генератор
    generator = FictionalDocumentGenerator()

    # 2. Генерируем документы
    documents = generator.generate_document_set(50)

    # 3. Сохраняем
    count = generator.save_documents()

    print(f"✓ Generated {count} documents in 'fictional_documents/'")
    print(f"✓ Universe: {generator.world_data['fictional_universe']}")
    print(f"✓ Index saved to 'fictional_index.json'")
    print(f"✓ Stats saved to 'generation_stats.json'")

    # 4. Показываем примеры замен
    print("\nExample fictional terms:")
    print("-" * 40)

    categories = ['characters', 'items', 'events', 'terms']
    for category in categories:
        if category in generator.terms_map:
            print(f"\n{category.upper()}:")
            items = list(generator.terms_map.get(category, {}).items())[:3]
            for orig, fict in items:
                print(f"  {orig:20} → {fict}")

    print("\n" + "=" * 60)
    print("Documents are ready for RAG testing!")
    print("All terms are fictional to avoid model memory bias.")

# apps/world2/fictional_document_generator.py
# ... предыдущий код остается без изменений до функции main() ...

def generate_qa_pairs(documents, world_data, terms_map):
    """Генерирует тестовые QA пары для RAG"""

    # Используем вымышленные термины из мира
    hero = None
    strong_hero = None
    alchemist = None
    chief = None
    bard = None
    blacksmith = None
    fisher = None

    # Находим вымышленные имена персонажей
    for char in world_data.get("characters", []):
        if char.get("type") == "hero":
            hero = char.get("fictional_name", "Veridix")
        elif char.get("type") == "strong_hero":
            strong_hero = char.get("fictional_name", "Megalix")
        elif char.get("type") == "alchemist":
            alchemist = char.get("fictional_name", "Alchemix")
        elif char.get("type") == "chief":
            chief = char.get("fictional_name", "Stentorix")
        elif char.get("type") == "bard":
            bard = char.get("fictional_name", "Melodix")
        elif char.get("type") == "blacksmith":
            blacksmith = char.get("fictional_name", "Blacksmith")
        elif char.get("type") == "fisher":
            fisher = char.get("fictional_name", "Fisher")

    # Получаем вымышленные названия предметов
    magic_potion = terms_map.get("items", {}).get("Magic Potion", "Sunstone Elixir")
    menhir = terms_map.get("items", {}).get("Menhir", "Standing Stone")
    wild_boar = terms_map.get("items", {}).get("Wild Boar", "Forest Stag")
    mistletoe = terms_map.get("terms", {}).get("mistletoe", "moonleaf")

    # Собираем ID документов по типам для ссылок
    encyclopedia_docs = [doc['id'] for doc in documents if doc['type'] == 'encyclopedia']
    journal_docs = [doc['id'] for doc in documents if doc['type'] == 'journal']
    report_docs = [doc['id'] for doc in documents if doc['type'] == 'report']
    myth_docs = [doc['id'] for doc in documents if doc['type'] == 'myth']

    qa_pairs = [
        {
            "question": f"What are the main ingredients and effects of the {magic_potion}?",
            "answer": f"The primary ingredient is {mistletoe} harvested during the twin suns' alignment. Effects include temporary enhanced vitality, accelerated movement, and temporary resilience. Chronic exposure leads to permanent strength.",
            "source_docs": encyclopedia_docs[:2] if encyclopedia_docs else ["ENCY_001", "ENCY_010"],
            "difficulty": "easy",
            "category": "magic_items"
        },
        {
            "question": f"Why is {strong_hero} permanently strong without drinking the {magic_potion}?",
            "answer": f"{strong_hero} fell into a cauldron of {magic_potion} as a baby, giving him permanent superhuman strength without needing to drink it like others.",
            "source_docs": myth_docs[:1] + encyclopedia_docs[:1] if myth_docs and encyclopedia_docs else ["MYTH_001", "ENCY_005"],
            "difficulty": "medium",
            "category": "characters"
        },
        {
            "question": f"What are the names of the Imperial outposts surrounding Oakhaven?",
            "answer": "The main Imperial outposts are Fort Argentum, Fort Ferrum, Fort Aurum, and Fort Plumbum.",
            "source_docs": encyclopedia_docs[2:3] + report_docs[:1] if len(encyclopedia_docs) > 2 and report_docs else ["ENCY_003", "REP_008"],
            "difficulty": "easy",
            "category": "geography"
        },
        {
            "question": f"How does the village deal with {bard}'s singing during gatherings?",
            "answer": f"{bard} is usually tied to a tree or otherwise restrained during gatherings to prevent him from singing, as his music is considered terrible.",
            "source_docs": journal_docs[:2] if journal_docs else ["JOURN_005", "JOURN_008"],
            "difficulty": "medium",
            "category": "culture"
        },
        {
            "question": f"What is the relationship between {blacksmith} and {fisher} in Oakhaven?",
            "answer": f"They frequently argue and fight, representing the ongoing conflict between the blacksmith and fisher trades in the village.",
            "source_docs": journal_docs[3:4] + report_docs[1:2] if len(journal_docs) > 3 and len(report_docs) > 1 else ["JOURN_002", "REP_006"],
            "difficulty": "hard",
            "category": "social_structure"
        },
        {
            "question": f"What are the three main factions in Veridonia and their symbols?",
            "answer": "1. Valefolk (Oakhaven villagers) - Symbol: Oak tree with twin suns. 2. Imperials (occupying force) - Symbol: Iron eagle. 3. Lorekeepers (scholars/alchemists) - Symbol: Crystal orb.",
            "source_docs": encyclopedia_docs[:3] if len(encyclopedia_docs) > 2 else ["ENCY_001", "ENCY_002", "ENCY_004"],
            "difficulty": "medium",
            "category": "factions"
        },
        {
            "question": f"What is the primary trade of {strong_hero} and what are the sizes of the stones he delivers?",
            "answer": f"{strong_hero} is a standing stone deliveryman. The stones come in three sizes: Standard (2m), Grande (3m), and Colossal (4m+).",
            "source_docs": encyclopedia_docs[4:5] + journal_docs[1:2] if len(encyclopedia_docs) > 4 and len(journal_docs) > 1 else ["ENCY_005", "JOURN_003"],
            "difficulty": "easy",
            "category": "economy"
        },
        {
            "question": "What are the key defensive strategies of Oakhaven against Imperial forces?",
            "answer": "Oakhaven relies on natural valley topography, strategic use of the Sunstone Elixir, and the clever tactics of its defenders. The settlement's location in the Emerald Valley provides natural barriers.",
            "source_docs": report_docs[:2] + encyclopedia_docs[1:2] if report_docs and len(encyclopedia_docs) > 1 else ["REP_002", "REP_005", "ENCY_002"],
            "difficulty": "medium",
            "category": "military"
        },
        {
            "question": f"What happens during the annual gathering at the Crystalwood Grove?",
            "answer": "The annual convocation at the Crystalwood Grove is mandatory for all Lorekeepers. They discuss herbalism, celestial observations, and preserve oral traditions.",
            "source_docs": encyclopedia_docs[3:4] + journal_docs[4:5] if len(encyclopedia_docs) > 3 and len(journal_docs) > 4 else ["ENCY_004", "JOURN_007"],
            "difficulty": "hard",
            "category": "traditions"
        },
        {
            "question": f"Why can't the Imperials successfully conquer Oakhaven according to legends?",
            "answer": "According to legend, the spirit of the valley made a pact with the first chieftain that as long as they honor the Forest Stag feast, the settlement will remain protected.",
            "source_docs": myth_docs[:2] if len(myth_docs) > 1 else ["MYTH_003", "MYTH_004"],
            "difficulty": "medium",
            "category": "mythology"
        },
        {
            "question": f"What are {alchemist}'s main responsibilities in Oakhaven society?",
            "answer": f"{alchemist} is the Lorekeeper responsible for brewing the Sunstone Elixir, studying herbs, serving as a healer, and preserving ancient knowledge.",
            "source_docs": encyclopedia_docs[3:4] + journal_docs[:1] if len(encyclopedia_docs) > 3 and journal_docs else ["ENCY_004", "JOURN_001"],
            "difficulty": "easy",
            "category": "characters"
        },
        {
            "question": "What is the social hierarchy in Oakhaven?",
            "answer": "The social structure places the chief at the top, followed by defenders, then artisans (blacksmith, fisher, etc.), with the minstrel enjoying ceremonial status but often being restrained during gatherings.",
            "source_docs": encyclopedia_docs[1:2] + report_docs[3:4] if len(encyclopedia_docs) > 1 and len(report_docs) > 3 else ["ENCY_002", "REP_004"],
            "difficulty": "hard",
            "category": "social_structure"
        },
        {
            "question": f"What restrictions are placed on the use of {magic_potion} according to village decrees?",
            "answer": f"Consumption of the {magic_potion} is restricted to defensive purposes only. Violators face quarry-cleaning duties.",
            "source_docs": ["DECR_001", "DECR_003"] if any('DECR' in doc['id'] for doc in documents) else [],
            "difficulty": "medium",
            "category": "laws"
        },
        {
            "question": "How do the Valefolk typically celebrate victories or important events?",
            "answer": "They hold gatherings featuring Forest Stag roasts, storytelling, and music (though the minstrel is often restrained). These celebrations reinforce community bonds.",
            "source_docs": journal_docs[2:3] + encyclopedia_docs[4:5] if len(journal_docs) > 2 and len(encyclopedia_docs) > 4 else ["JOURN_004", "ENCY_005"],
            "difficulty": "easy",
            "category": "culture"
        },
        {
            "question": "What are the main exports and trade goods of Oakhaven?",
            "answer": "Oakhaven exports standing stones, herbal remedies, and fish. They import olive oil, amphorae, and other goods from Silverport and Imperial traders.",
            "source_docs": report_docs[2:3] + encyclopedia_docs[4:5] if len(report_docs) > 2 and len(encyclopedia_docs) > 4 else ["REP_003", "ENCY_005"],
            "difficulty": "hard",
            "category": "economy"
        }
    ]

    # Фильтруем пустые source_docs
    for qa in qa_pairs:
        if not qa["source_docs"]:
            # Если не нашли документы, используем общие
            qa["source_docs"] = ["ENCY_001", "ENCY_002", "JOURN_001"]

    return qa_pairs

def save_qa_pairs(qa_pairs, filename="qa_pairs.jsonl"):
    """Сохраняет QA пары в файл"""
    import json

    with open(filename, 'w', encoding='utf-8') as f:
        for qa in qa_pairs:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    print(f"✓ Saved {len(qa_pairs)} QA pairs to {filename}")
    return len(qa_pairs)

def main():
    """Основная функция генерации документов"""
    print("Generating fictional universe documents...")
    print("=" * 60)

    # 1. Создаём генератор
    generator = FictionalDocumentGenerator()

    # 2. Генерируем документы
    documents = generator.generate_document_set(50)

    # 3. Сохраняем документы
    count = generator.save_documents()

    # 4. Генерируем и сохраняем QA пары
    qa_pairs = generate_qa_pairs(documents, generator.world_data, generator.terms_map)
    save_qa_pairs(qa_pairs)

    print(f"\n✓ Generated {count} documents in 'fictional_documents/'")
    print(f"✓ Universe: {generator.world_data['fictional_universe']}")
    print(f"✓ Index saved to 'fictional_index.json'")
    print(f"✓ Stats saved to 'generation_stats.json'")
    print(f"✓ QA pairs saved to 'qa_pairs.jsonl'")

    # 5. Показываем примеры замен
    print("\nExample fictional terms:")
    print("-" * 40)

    categories = ['characters', 'items', 'events', 'terms']
    for category in categories:
        if category in generator.terms_map:
            print(f"\n{category.upper()}:")
            items = list(generator.terms_map.get(category, {}).items())[:3]
            for orig, fict in items:
                print(f"  {orig:20} → {fict}")

    print("\n" + "=" * 60)
    print("Documents are ready for RAG testing!")
    print("All terms are fictional to avoid model memory bias.")
    print("\nExample questions for testing:")
    print("-" * 40)
    for i, qa in enumerate(qa_pairs[:3], 1):
        print(f"{i}. {qa['question']}")
        print(f"   Difficulty: {qa['difficulty']}, Category: {qa['category']}")

if __name__ == "__main__":
    main()