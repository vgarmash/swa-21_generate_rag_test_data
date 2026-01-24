# apps/world2/fictional_document_generator.py
import json
import random
from datetime import datetime, timedelta
import os
from typing import List, Dict, Any
import hashlib
import re  # Добавляем для работы с регулярными выражениями

try:
    from .fictional_world_bible import FictionalWorldBuilder
except ImportError:
    from fictional_world_bible import FictionalWorldBuilder

class ContentGenerator:
    """Генератор уникального контента"""

    def __init__(self, world_data, terms_map):
        self.world_data = world_data
        self.terms_map = terms_map
        self.generated_hashes = set()
        self.fictional_terms_cache = self._load_fictional_terms()  # Кэшируем термины

    def _load_fictional_terms(self):
        """Загружает все вымышленные термины для использования"""
        all_terms = []

        # Собираем термины из всех категорий
        if 'characters' in self.terms_map:
            all_terms.extend(list(self.terms_map['characters'].values()))

        if 'items' in self.terms_map:
            all_terms.extend(list(self.terms_map['items'].values()))

        if 'terms' in self.terms_map:
            all_terms.extend(list(self.terms_map['terms'].values()))

        # Добавляем регионы и фракции
        if 'regions' in self.terms_map:
            all_terms.extend(list(self.terms_map['regions'].values()))

        if 'factions' in self.terms_map:
            all_terms.extend(list(self.terms_map['factions'].values()))

        return all_terms

    def enrich_with_terms(self, text):
        """
        Обогащает текст вымышленными терминами
        Пример: "the hero" -> "Veridix (the clever hero)"
        """
        if not self.fictional_terms_cache or len(text) < 50:
            return text

        # Список для замены общих понятий на конкретные термины
        replacements = {
            'the hero': ['Veridix', 'our clever hero Veridix', 'the warrior Veridix'],
            'strong hero': ['Megalix', 'the mighty Megalix', 'Megalix the stone-carrier'],
            'alchemist': ['Alchemix', 'the wise Alchemix', 'Lorekeeper Alchemix'],
            'chief': ['Chief Stentorix', 'the village leader Stentorix'],
            'magic potion': ['Sunstone Elixir', 'the mystical Sunstone Elixir'],
            'village': ['Oakhaven', 'the settlement of Oakhaven'],
            'forest': ['Whispering Woods', 'the ancient groves'],
            'stone': ['standing stone', 'sacred monolith'],
            'empire': ['the Iron Empire', 'Imperial forces'],
            'soldier': ['Imperial legionnaire', 'Iron Empire guard'],
            'camp': ['Imperial outpost', 'fortified garrison'],
            'feast': ['grand gathering', 'communal banquet'],
            'boar': ['forest stag', 'mountain tusker'],
            'druid': ['Lorekeeper', 'star-seer', 'moon-sage'],
            'bard': ['skald', 'lore-singer'],
            'centurion': ['shield-captain', 'blade-commander']
        }

        # Применяем замены
        for generic, options in replacements.items():
            if generic in text.lower():
                replacement = random.choice(options)
                # Заменяем с учётом регистра
                text = re.sub(r'\b' + re.escape(generic) + r'\b', replacement, text, flags=re.IGNORECASE)

        # Добавляем случайные термины в текст (30% вероятность для каждого предложения)
        sentences = [s.strip() for s in text.split('. ') if s.strip()]

        if len(sentences) > 2 and self.fictional_terms_cache:
            for i in range(len(sentences)):
                if random.random() < 0.3:  # 30% chance to enrich this sentence
                    term = random.choice(self.fictional_terms_cache)

                    # Разные способы вставки термина
                    insertions = [
                        f" This relates to {term}.",
                        f" Important consideration: {term}.",
                        f" As demonstrated by {term},",
                        f" Similar to {term}, this shows",
                        f" In the context of {term},",
                        f" {term} exemplifies this principle."
                    ]

                    sentences[i] = sentences[i] + random.choice(insertions)

            text = '. '.join(sentences)

        return text

    def get_unique_content(self, template_func, *args, **kwargs):
        """Генерирует уникальный контент"""
        attempts = 0
        while attempts < 5:
            content = template_func(*args, **kwargs)

            # Обогащаем терминами
            content = self.enrich_with_terms(content)

            content_hash = hashlib.md5(content.encode()).hexdigest()

            if content_hash not in self.generated_hashes:
                self.generated_hashes.add(content_hash)
                return content

            attempts += 1

        # Если не удалось создать уникальный, добавляем идентификатор
        base_content = template_func(*args, **kwargs)
        enriched = self.enrich_with_terms(base_content)
        return enriched + f"\n\n[Document variant {random.randint(1000, 9999)}]"

    def get_character(self, role, get_details=False):
        """Получает вымышленного персонажа по роли"""
        for char in self.world_data.get("characters", []):
            if char.get("type") == role:
                if get_details:
                    return char
                return char.get("fictional_name", role)
        return role

    def get_fictional(self, original_term, category=None):
        """Возвращает вымышленный термин"""
        if category and category in self.terms_map:
            return self.terms_map[category].get(original_term, original_term)

        for cat in self.terms_map.values():
            if isinstance(cat, dict) and original_term in cat:
                return cat[original_term]

        return original_term

    def format_metadata(self, metadata):
        """Форматирует метаданные без yaml"""
        lines = []
        for key, value in metadata.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

    def generate_elixir_article(self):
        """Генерирует уникальную статью об эликсире"""
        alchemist = self.get_character("alchemist")
        strong_hero = self.get_character("strong_hero")
        hero = self.get_character("hero")

        elixir_names = [
            "Sunstone Elixir", "Moonfall Draught", "Starlight Tonic",
            "Dreamweaver Brew", "Crystal Essence", "Elderwood Extract"
        ]
        elixir_name = random.choice(elixir_names)

        ingredients = [
            "moonleaf harvested during the twin moon convergence",
            "star-moss collected from ancient monoliths",
            "petrified sunlight fragments found in crystal caves",
            "whispering willow bark from the Elder Grove",
            "crystalized dew from dream-fed plants"
        ]

        effects = [
            "temporary enhanced vitality and endurance",
            "accelerated reflexes and perception",
            "short-term invulnerability to physical harm",
            "momentary bursts of supernatural strength",
            "enhanced cognitive processing and memory"
        ]

        lore_elements = [
            f"According to {alchemist}'s research, the formula varies by season.",
            f"Ancient texts mention a lost variant used during {random.choice(['The Crystal War', 'The Great Schism', 'The Moonfall'])}.",
            f"The {random.choice(['Lorekeepers', 'Star Seers', 'Moon Sages'])} guild regulates its production.",
            f"Counterfeit versions often contain {random.choice(['ground crystal', 'moon-dust', 'star-shards'])} instead of proper ingredients."
        ]

        template = f"""# Properties of {elixir_name}

The {elixir_name} is a legendary concoction prepared exclusively by the Lorekeeper {alchemist}. 
Its primary ingredient is {random.choice(ingredients)}, gathered using a {random.choice(['silver crescent', 'crystal blade', 'obsidian sickle'])}.

## Effects and Properties

Primary effects include {random.choice(effects)}. Secondary benefits may involve {random.choice(['enhanced healing', 'temporary levitation', 'elemental resistance'])} depending on the brew.

Chronic exposure, as documented in the case of {strong_hero}, leads to permanent physical enhancement but requires frequent nourishment.

## Historical Significance

The formula originated during {random.choice(['the Age of Discovery', 'the Crystal Accord', 'the First Moonfall'])} and has been refined over {random.randint(10, 50)} generations. {random.choice(lore_elements)}

## Modern Usage

{hero} employs it strategically during encounters with Imperial forces. Proper dosage is critical - {random.randint(5, 15)} drops for basic enhancement, up to a full vial for combat situations.

Storage requires {random.choice(['obsidian containers', 'crystal vials', 'silver-lined flasks'])} to maintain potency beyond {random.randint(30, 90)} days."""

        return template

    def generate_settlement_article(self):
        """Генерирует статью о поселении"""
        chief = self.get_character("chief")
        blacksmith = self.get_character("blacksmith")
        fisher = self.get_character("fisher")
        bard = self.get_character("bard")

        settlement_names = ["Oakhaven", "Stonewatch", "Crystalbrook", "Moonhaven", "Starfall Enclave"]
        settlement_name = random.choice(settlement_names)

        regions = self.world_data.get("regions", [])
        region = random.choice(regions) if regions else {"name": "Emerald Valley", "climate": "temperate"}

        structures = [
            "central plaza with the Chief's longhouse",
            "alchemist's tower and laboratory",
            "communal gathering hall",
            "defensive watchtowers",
            "artisan district with workshops",
            "market square for trade"
        ]

        defenses = [
            "natural valley topography providing choke points",
            "strategically placed monoliths with protective enchantments",
            "a militia trained in guerrilla tactics",
            "hidden escape tunnels and safe houses",
            "early warning systems using crystal resonators"
        ]

        economy = [
            "standing stone quarrying and delivery",
            "herbal remedies and alchemical supplies",
            "artisan crafts including metalwork and weaving",
            "fishing and aquatic harvesting",
            "guidance services for travelers"
        ]

        template = f"""# Settlement Structure: {settlement_name}

## Overview

{settlement_name} is a {region.get('type', 'village')} settlement located in the {region.get('name', 'Emerald Valley')}, known for its {region.get('climate', 'temperate')} climate and remarkable resistance to Imperial occupation.

## Physical Layout

The settlement is structured around a {random.choice(structures)} at the highest elevation. Key infrastructure includes:

1. **Central District**: Housing for {random.randint(50, 200)} families, centered around the plaza
2. **Defensive Perimeter**: {random.choice(['Wooden palisade', 'Stone wall', 'Natural rock formation'])}, enhanced with {random.choice(defenses)}
3. **Production Areas**: {random.choice(['Quarry', 'Forge', 'Fishery', 'Workshop'])} districts for essential goods
4. **Cultural Sites**: {random.choice(['Story circle', 'Memory stones', 'Festival grounds', 'Archive'])} for community events

## Social Structure

The social hierarchy places Chief {chief} at the apex, followed by:
- **Defenders**: {random.randint(10, 30)} trained combatants led by {self.get_character('hero')}
- **Artisans**: Specialists including {blacksmith} (metalwork) and {fisher} (aquatic resources)
- **Scholars**: Lorekeepers and healers maintaining traditional knowledge
- **Entertainers**: Including {bard}, whose performances are {random.choice(['celebrated', 'tolerated', 'occasionally restrained'])} during gatherings

## Economy and Trade

Primary economic activities include {random.choice(economy)}. The settlement trades with {random.choice(['Silverport', 'Crystal City', 'Starfall Market'])} for essential imports like {random.choice(['olive oil', 'spices', 'tools', 'fabrics'])}.

## Notable Features

What makes {settlement_name} unique is its {random.choice([
            'integration with natural crystal formations',
            'ancient protective enchantments',
            'communal decision-making process',
            'seasonal migration patterns'
        ])}. Recent developments include {random.choice([
            'expansion of the northern quarry',
            'construction of a new watchtower',
            'establishment of a Lorekeeper academy',
            'negotiations with nearby settlements'
        ])}."""

        return template

    def generate_journal_entry(self, author_role="hero"):
        """Генерирует запись в журнале"""
        author = self.get_character(author_role)

        dates = [
            f"{random.choice(['First', 'Second', 'Third'])} Moon of {random.choice(['Sunfire', 'Starfrost', 'Rain'])}",
            f"Day {random.randint(1, 30)} of the {random.choice(['Harvest', 'Planting', 'Hunting'])} Season",
            f"{random.choice(['Dawn', 'Dusk', 'Midday'])} on the {random.randint(1, 5)}th of {random.choice(['Crystal', 'Iron', 'Silver'])}month"
        ]

        locations = [
            "near the Whispering Falls",
            "at the base of Elder Mountain",
            "within the Sunken Ruins",
            "along the Starlight River",
            "in the Crystalwood Grove"
        ]

        entry = f"""## Journal Entry #{random.randint(1, 100)}

*Date: {random.choice(dates)}*
*Location: {random.choice(locations)}*
*Weather: {random.choice(['Sunny', 'Misty', 'Rainy', 'Clear'])}*
*Mood: {random.choice(['contemplative', 'excited', 'weary', 'hopeful'])}*

Today was eventful. {random.choice([
            f'I discovered {random.choice(["ancient runes", "a hidden cave", "unusual crystals"])} while exploring.',
            f'We had a skirmish with Imperial scouts near the border.',
            f'{self.get_character("alchemist")} showed me a new herbal preparation.',
            f'The community gathered for the monthly festival.'
        ])}

**Observation:** {random.choice([
            'The seasons are changing earlier than expected.',
            'Imperial patrols seem more frequent lately.',
            'The crystal formations hum differently at night.',
            'Our food stores are adequate for the coming winter.'
        ])}

**Personal note:** {self._generate_personal_note()}"""

        return entry

    def _generate_personal_note(self):
        return random.choice([
            "Must remember to check the northern watchtower tomorrow.",
            "The new batch of moonleaf seems particularly potent.",
            f"{self.get_character('strong_hero')} broke another tool today - need to speak with {self.get_character('blacksmith')}.",
            "The dreams have been more vivid since visiting the crystal cave."
        ])

    def generate_report(self):
        """Генерирует отчёт"""
        report_types = [
            "Military Intelligence",
            "Economic Assessment",
            "Cultural Analysis",
            "Resource Survey",
            "Strategic Evaluation"
        ]

        report_type = random.choice(report_types)

        template = f"""# {report_type} Report

## Executive Summary

This report details findings from recent {report_type.lower()} activities in the region. Key observations indicate {random.choice([
            'increased Imperial activity along northern borders',
            'stable economic conditions with minor fluctuations',
            'cultural shifts among younger population segments',
            'depletion of certain natural resources',
            'emergence of new trade patterns'
        ])}.

## Methodology

Data collected through {random.choice([
            'direct observation and reconnaissance',
            'interviews with local informants',
            'analysis of trade records and ledgers',
            'examination of material culture artifacts',
            'long-term monitoring of key indicators'
        ])} over a period of {random.randint(7, 90)} days.

## Findings

1. **Primary Trend**: {random.choice([
            'Imperial forces are consolidating positions',
            'Local economy shows resilience despite pressures',
            'Traditional practices maintain strong adherence',
            'Resource extraction exceeds sustainable levels',
            'New alliances are forming among settlements'
        ])}

2. **Secondary Observations**: {random.choice([
            'Supply lines remain vulnerable in certain sectors',
            'Cultural exchange increasing with neighboring regions',
            'Environmental changes affecting traditional patterns',
            'Technological adaptation proceeding slowly',
            'Social cohesion remains strong under pressure'
        ])}

3. **Anomalies Noted**: {random.choice([
            'Unexpected activity near abandoned ruins',
            'Unusual weather patterns affecting harvests',
            'Discrepancies in reported versus observed data',
            'Emergence of previously undocumented practices',
            'Signs of external influence beyond expected parameters'
        ])}

## Recommendations

Based on these findings, we recommend:
1. {random.choice(['Increase surveillance in identified areas', 'Adjust resource allocation priorities', 'Initiate cultural preservation programs', 'Implement sustainable harvesting protocols', 'Strengthen diplomatic outreach'])}
2. {random.choice(['Prepare contingency plans for potential escalation', 'Diversify economic activities to reduce vulnerability', 'Document traditional knowledge before it is lost', 'Establish monitoring systems for environmental changes', 'Facilitate inter-settlement communication networks'])}
3. {random.choice(['Conduct follow-up investigation in three months', 'Allocate additional resources for implementation', 'Coordinate with allied factions for joint action', 'Review and update existing protocols', 'Educate population about findings and implications'])}

## Conclusion

The situation requires {random.choice(['continued monitoring', 'immediate action', 'strategic patience', 'diplomatic engagement', 'resource investment'])}. Further developments will be reported as they occur."""

        return template

    def generate_decree(self):
        """Генерирует указ"""
        authorities = [
            "Chief", "Council of Elders", "High Commander",
            "Lorekeeper Assembly", "Trade Guild Master"
        ]

        authority = random.choice(authorities)

        decree_types = [
            "Resource Management",
            "Defensive Measures",
            "Cultural Preservation",
            "Economic Regulation",
            "Social Conduct"
        ]

        decree_type = random.choice(decree_types)

        template = f"""# Decree of {authority}

## Preamble

In accordance with traditional authority and for the welfare of the community, this decree is issued regarding matters of {decree_type.lower()}.

## Articles

### Article 1: General Provisions

All members of the community shall adhere to the following regulations effective immediately.

### Article 2: Specific Regulations

1. {random.choice([
            'The harvesting of moonleaf shall be limited to designated areas during specific lunar phases.',
            'All able-bodied individuals shall participate in defensive drills twice per moon cycle.',
            'Traditional festivals shall be observed according to ancestral calendars.',
            'Trade with external parties requires approval from designated authorities.',
            'Public gatherings exceeding twenty individuals require advance notification.'
        ])}

2. {random.choice([
            'Use of standing stones for construction requires quarrymaster approval.',
            'Reporting of Imperial movements to local defenders is mandatory.',
            'Preservation of historical sites takes precedence over development.',
            'Price controls on essential goods shall be maintained.',
            'Resolution of disputes shall follow established mediation procedures.'
        ])}

3. {random.choice([
            'Waste disposal shall conform to environmental protection standards.',
            'Training in basic self-defense is required for all adults.',
            'Passing down of oral histories to younger generations is encouraged.',
            'Quality standards for exported goods shall be enforced.',
            'Community service obligations apply to all resident families.'
        ])}

### Article 3: Enforcement

Violations shall be subject to {random.choice([
            'corrective labor assignments',
            'temporary restrictions on privileges',
            'mandatory education sessions',
            'community service requirements',
            'restitution payments'
        ])} as determined by appropriate authorities.

### Article 4: Duration

This decree remains in effect until {random.choice([
            'the next seasonal council convenes',
            'specific conditions are met as outlined in supplementary documents',
            'amended or revoked by subsequent decree',
            'one full cycle of seasons has passed',
            'emergency conditions have been resolved'
        ])}.

## Authorization

Issued under the seal and authority of {authority} on this {random.randint(1, 30)}th day of {random.choice(['Sunfire', 'Starfrost', 'Rain', 'Bloom'])}month."""

        return template

    def generate_myth(self):
        """Генерирует миф"""
        myth_themes = [
            "Origin of the First Settlement",
            "Why the Mountains Hold Memory",
            "The Gift of the Twin Moons",
            "The Great Beast of the Depths",
            "How Laughter Saved the World"
        ]

        theme = random.choice(myth_themes)

        characters = [
            self.get_character("hero"),
            self.get_character("alchemist"),
            self.get_character("chief"),
            "The First Walker",
            "The Stone Speaker",
            "The Dream Weaver"
        ]

        character = random.choice(characters)

        template = f"""# The Legend of {theme}

## As told by the Elders

In the time before counting, when the world was still learning its shape, there occurred the events that explain {theme.lower()}.

It began when {character} {random.choice([
            'discovered a cave that whispered secrets',
            'followed a path of falling stars',
            'sought answers from the sleeping earth',
            'challenged the boundaries of the known world',
            'listened to the dreams of stones'
        ])}.

## The Journey

{character} traveled through {random.choice([
            'forests that remembered every footstep',
            'mountains that tested resolve with each ascent',
            'rivers that carried memories instead of water',
            'valleys where time flowed differently',
            'plains where the wind told forgotten stories'
        ])}, facing trials that included {random.choice([
            'riddles posed by ancient guardians',
            'temptations of false promises',
            'illusions that mirrored deepest fears',
            'silence that threatened to become permanent',
            'choices with consequences beyond understanding'
        ])}.

## The Revelation

At the moment of greatest challenge, {character} realized that {random.choice([
            'true strength comes from community, not isolation',
            'the land remembers those who listen',
            'balance requires both giving and receiving',
            'some truths can only be carried, not owned',
            'the smallest actions create the largest echoes'
        ])}.

## The Outcome

From this revelation came {random.choice([
            'the founding principles of our settlement',
            'the understanding that guides our relationship with nature',
            'the traditions that bind our community',
            'the wisdom that protects us from folly',
            'the hope that sustains us in difficult times'
        ])}.

## The Moral

This story teaches us that {random.choice([
            'every ending contains a new beginning',
            'the greatest treasures are often overlooked',
            'true power lies in understanding, not controlling',
            'our choices shape the world for generations',
            'the simplest truths are the most enduring'
        ])}.

## Transmission

Remember this tale when {random.choice([
            'facing decisions that affect the community',
            'the seasons change and the world renews itself',
            'teaching the young about their heritage',
            'seeking guidance in times of uncertainty',
            'celebrating the bonds that connect us all'
        ])}."""

        return template

    def generate_letter(self):
        """Генерирует письмо"""
        senders = [
            self.get_character("hero"),
            self.get_character("alchemist"),
            self.get_character("chief"),
            "A Distant Relative",
            "A Traveling Merchant",
            "An Anonymous Informant"
        ]

        receivers = [
            "Trusted Friend",
            "Family Member",
            "Council Representative",
            "Business Associate",
            "Fellow Scholar"
        ]

        sender = random.choice(senders)
        receiver = random.choice(receivers)

        template = f"""To {receiver},

I hope this message finds you in good health and spirits. The seasons turn as always, though not without their peculiarities.

Since we last corresponded, {random.choice([
            'much has changed in our corner of the world',
            'matters have proceeded with expected regularity',
            'unexpected developments have required attention',
            'tranquility has settled over our daily routines',
            'challenges have tested our resilience once more'
        ])}.

Specifically, {random.choice([
            f'work on the {random.choice(["northern watchtower", "communal granary", "healing springs"])} progresses steadily',
            f'relations with the {random.choice(["neighboring settlement", "traveling merchants", "mountain clans"])} remain cordial',
            f'harvest of {random.choice(["moonleaf", "crystal shards", "medicinal herbs"])} has been particularly bountiful',
            f'concerns about {random.choice(["Imperial movements", "resource depletion", "strange occurrences"])} have arisen',
            f'preparations for the {random.choice(["annual festival", "coming winter", "leadership transition"])} are underway'
        ])}.

I must share that {random.choice([
            'a discovery of some significance has come to light',
            'certain observations have given me cause for reflection',
            'traditional methods have proven their worth once again',
            'new approaches are showing promising results',
            'unanswered questions continue to occupy my thoughts'
        ])}. This relates to {random.choice([
            'ancient practices that may have modern applications',
            'patterns that suggest deeper connections',
            'resources whose full potential remains untapped',
            'relationships that shape our collective future',
            'knowledge that bridges generations'
        ])}.

On a more personal note, {random.choice([
            'the quiet moments continue to bring clarity',
            'each day reaffirms the value of community',
            'the balance between tradition and adaptation requires constant attention',
            'small victories accumulate into meaningful progress',
            'the landscape itself seems to hold lessons for those who observe closely'
        ])}.

I would value your perspective on these matters when opportunity permits. Please convey my regards to {random.choice(['mutual acquaintances', 'your family', 'the community elders', 'fellow seekers of knowledge'])}.

With sincerity and anticipation of your reply,

{sender}

P.S. {random.choice([
            'Do not trouble yourself with immediate response - these matters can wait.',
            'I include a small token that may be of interest to your studies.',
            'Burn this after reading, as precautions remain necessary.',
            'The next caravan should reach your area within two moon cycles.',
            'Remember what we discussed under the twin moons last season.'
        ])}"""

        return template

class FictionalDocumentGenerator:
    def __init__(self):
        builder = FictionalWorldBuilder()
        self.world_data, _ = builder.build_world()
        self.terms_map = builder.categories
        self.content_gen = ContentGenerator(self.world_data, self.terms_map)

        self.documents = []
        self.doc_ids = []

    def generate_document_set(self, num_docs=50):
        """Генерирует полный набор уникальных документов"""

        doc_distribution = {
            'encyclopedia': 15,
            'journal': 12,
            'report': 10,
            'decree': 5,
            'myth': 5,
            'letter': 3
        }

        print("Generating unique documents...")

        for doc_type, count in doc_distribution.items():
            print(f"  Creating {count} {doc_type} documents...")
            for i in range(count):
                doc = self._generate_document(doc_type, i+1)
                self.documents.append(doc)
                self.doc_ids.append(doc['id'])

        self._add_cross_references()
        self._add_explicit_references()  # Добавляем явные ссылки
        return self.documents

    def _generate_document(self, doc_type, index):
        """Генерирует один уникальный документ"""

        doc_id = f"{doc_type.upper()[:4]}_{index:03d}"

        # Словарь методов генерации
        template_methods = {
            'encyclopedia': self._encyclopedia_template,
            'journal': self._journal_template,
            'report': self._report_template,
            'decree': self._decree_template,
            'myth': self._myth_template,
            'letter': self._letter_template
        }

        content, metadata = template_methods[doc_type](doc_id)

        metadata.update({
            'doc_id': doc_id,
            'doc_type': doc_type,
            'universe': self.world_data['fictional_universe'],
            'generated_date': datetime.now().strftime("%Y-%m-%d"),
            'contains_fictional_terms': True,
            'content_hash': hashlib.md5(content.encode()).hexdigest()[:8]
        })

        full_doc = f"---\n{self.content_gen.format_metadata(metadata)}\n---\n\n{content}"

        return {
            'id': doc_id,
            'type': doc_type,
            'content': full_doc,
            'metadata': metadata,
            'raw_content': content
        }

    def _encyclopedia_template(self, doc_id):
        """Шаблон для энциклопедической статьи"""

        topics = [
            ("Properties of ", "elixir"),
            ("Structure of ", "settlement"),
            ("Imperial ", "military"),
            ("Lorekeeper ", "practices"),
            ("Types of ", "stones"),
            ("History of ", "region"),
            ("Economic ", "systems"),
            ("Cultural ", "traditions"),
            ("Ecological ", "features"),
            ("Architectural ", "styles")
        ]

        prefix, topic_type = random.choice(topics)

        # Генерируем уникальное название
        if topic_type == "elixir":
            elixirs = ["Sunstone Elixir", "Moonfall Draught", "Starlight Tonic", "Dreamweaver Brew"]
            topic_name = random.choice(elixirs)
        elif topic_type == "settlement":
            settlements = ["Oakhaven", "Stonewatch", "Crystalbrook", "Moonhaven"]
            topic_name = random.choice(settlements) + " Settlement"
        else:
            topic_name = prefix + random.choice([
                "Military Organization", "Herbal Practices", "Stone Classifications",
                "Trade Routes", "Festival Calendar", "Defensive Strategies"
            ])

        full_topic = prefix + topic_name if not topic_name.startswith(prefix) else topic_name

        metadata = {
            'title': f"Encyclopedia: {full_topic}",
            'author': random.choice(["Emerald Valley Scholars", "Lorekeeper Archives", "Imperial Geographers", "Traveler's Compendium"]),
            'publication_date': f"{random.randint(45, 50)} {self.world_data.get('era_suffix', 'AM')}",
            'keywords': [self.world_data.get('country_name', 'Veridia'), "fictional", topic_type]
        }

        # Генерируем уникальный контент
        if topic_type == "elixir":
            content = self.content_gen.generate_elixir_article()
        elif topic_type == "settlement":
            content = self.content_gen.generate_settlement_article()
        else:
            content = self.content_gen.get_unique_content(
                self._generate_general_article, full_topic, topic_type
            )

        # Добавляем БОЛЬШЕ ссылок
        content += "\n\n## Related Documents\n"
        if len(self.doc_ids) > 5:
            related = random.sample([d for d in self.doc_ids if d != doc_id], min(5, len(self.doc_ids) - 1))
            for doc in related:
                content += f"- {doc}\n"
                # Добавляем краткое описание
                content += f"  *Covers related aspects of {full_topic.lower()}*\n"
        else:
            content += "- No related documents yet\n"

        return content, metadata

    def _generate_general_article(self, topic, topic_type):
        """Генерирует общую статью"""
        return f"""# {topic}

## Overview

This article covers the {topic_type} aspects of {topic} within the context of {self.world_data.get('fictional_universe', 'Chronicles of Veridia')}.

## Key Features

1. **Primary Characteristics**: {random.choice(['Unique properties distinct from other regions', 'Standard features common across similar entities', 'Evolving nature adapting to environmental factors'])}
2. **Historical Development**: Evolved over {random.randint(5, 50)} generations since {random.choice(['the Great Accord', 'the Moonfall', 'the Crystal War'])}
3. **Current Status**: {random.choice(['Stable and well-documented', 'Undergoing significant changes', 'Subject to ongoing research and debate'])}
4. **Future Prospects**: {random.choice(['Expected to remain consistent', 'Likely to evolve with new discoveries', 'Facing challenges from external factors'])}

## Significance

The study of {topic} provides insights into {random.choice([
            'broader cultural patterns',
            'technological advancements',
            'environmental adaptations',
            'sociopolitical structures'
        ])}.

## Research Notes

Recent investigations by {random.choice(['Lorekeeper expeditions', 'Imperial survey teams', 'Independent scholars'])} have revealed {random.choice([
            'previously undocumented variations',
            'connections to ancient practices',
            'practical applications for daily life',
            'potential risks requiring mitigation'
        ])}.

**Further reading**: Consult related documents on {random.choice(['regional histories', 'technical manuals', 'cultural studies', 'economic analyses'])} for comprehensive understanding."""

    def _journal_template(self, doc_id):
        """Шаблон для журнальной записи"""
        author_roles = ['hero', 'alchemist', 'chief', 'strong_hero']
        author_role = random.choice(author_roles)

        metadata = {
            'title': f"Personal Journal of {self.content_gen.get_character(author_role)}",
            'author': self.content_gen.get_character(author_role),
            'journal_type': random.choice(['Field Notes', 'Personal Reflections', 'Daily Log', 'Observational Record']),
            'period': random.choice(['Current Cycle', 'Recent Months', 'Seasonal Record', 'Ongoing Documentation'])
        }

        content = self.content_gen.generate_journal_entry(author_role)

        # Добавляем БОЛЬШЕ ссылок
        if len(self.doc_ids) > 3:
            related = random.sample([d for d in self.doc_ids if d != doc_id], min(3, len(self.doc_ids) - 1))
            content += f"\n\n**Related entries:** {', '.join(related)}"
            # Добавляем явные ссылки
            for ref_doc in related[:2]:
                content += f"\n- See {ref_doc} for additional context on today's events"

        return content, metadata

    def _report_template(self, doc_id):
        """Шаблон для отчёта"""
        metadata = {
            'title': "Field Report",
            'author': random.choice(["Imperial Scout", "Lorekeeper Observer", "Trade Guild Agent", "Independent Researcher"]),
            'classification': random.choice(["CONFIDENTIAL", "INTERNAL USE", "PUBLIC DOMAIN", "RESTRICTED ACCESS"]),
            'subject_area': random.choice(["Military", "Economics", "Culture", "Resources", "Infrastructure"])
        }

        content = self.content_gen.generate_report()

        # Добавляем БОЛЬШЕ ссылок
        if len(self.doc_ids) > 3:
            related = random.sample([d for d in self.doc_ids if d != doc_id and ('REP' in d or 'ENCY' in d or 'JOUR' in d)],
                                    min(3, len(self.doc_ids) - 1))
            if related:
                content += f"\n\n**Reference documents:** {', '.join(related)}"
                # Добавляем пояснения
                content += "\n\n**Cross-references:**"
                for ref_doc in related:
                    content += f"\n- {ref_doc}: Provides supporting data for findings"

        return content, metadata

    def _decree_template(self, doc_id):
        """Шаблон для указа"""
        metadata = {
            'title': "Official Decree",
            'authority': random.choice(["Chief's Council", "Lorekeeper Assembly", "Defense Command", "Trade Directorate"]),
            'jurisdiction': random.choice(["Oakhaven Settlement", "Emerald Valley Region", "Allied Territories", "Trade Network"]),
            'effective_date': f"{random.choice(['Immediately', 'Next Moon Cycle', 'Beginning of Season'])}"
        }

        content = self.content_gen.generate_decree()

        # Добавляем БОЛЬШЕ ссылок
        if len(self.doc_ids) > 2:
            related = [d for d in self.doc_ids if d != doc_id and ('DECR' in d or 'ENCY' in d)]
            if related:
                content += f"\n\n**Related decrees and laws:** {', '.join(related[:3])}"
                content += f"\n**See also:** Legal precedents and historical regulations"

        return content, metadata

    def _myth_template(self, doc_id):
        """Шаблон для мифа"""
        metadata = {
            'title': "Ancient Legend",
            'storyteller': random.choice(["Elder Chronicler", "Memory Keeper", "Dream Interpreter", "Star Reader"]),
            'origin_culture': random.choice(["Valley Folk", "Mountain Tribes", "River People", "Forest Dwellers"]),
            'estimated_age': f"{random.randint(100, 1000)} years"
        }

        content = self.content_gen.generate_myth()

        # Добавляем БОЛЬШЕ ссылок
        if len(self.doc_ids) > 2:
            related = [d for d in self.doc_ids if d != doc_id and ('MYTH' in d or 'ENCY' in d)]
            if related:
                content += f"\n\n**Related legends and lore:** {', '.join(related[:3])}"
                content += f"\n**Cultural context:** Additional myths provide complementary perspectives"

        return content, metadata

    def _letter_template(self, doc_id):
        """Шаблон для письма"""
        metadata = {
            'title': "Personal Correspondence",
            'correspondence_type': random.choice(["Private Letter", "Official Communication", "Informal Note", "Diplomatic Message"]),
            'delivery_method': random.choice(["Carrier Bird", "Trusted Messenger", "Trade Caravan", "Hidden Compartment"]),
            'security_level': random.choice(["Unsecured", "Coded", "Encrypted", "Self-destructing"])
        }

        content = self.content_gen.generate_letter()

        return content, metadata

    def _add_cross_references(self):
        """Добавляет перекрёстные ссылки - УВЕЛИЧИВАЕМ количество"""
        reference_phrases = [
            " (see document: {DOC} for details)",
            " (comprehensive analysis in {DOC})",
            " (contrasting viewpoint in {DOC})",
            " (historical context in {DOC})",
            " (practical applications documented in {DOC})",
            " (additional information available in {DOC})",
            " (related discussion in {DOC})",
            " (supporting evidence in {DOC})",
            " (as referenced in {DOC})",
            " (for more details, consult {DOC})"
        ]

        for doc in self.documents:
            content = doc['raw_content']
            sentences = [s.strip() for s in content.split('. ') if s.strip()]

            if len(sentences) > 3 and len(self.doc_ids) > 3:
                # УВЕЛИЧИВАЕМ: было 1-2, теперь 3-6 ссылок
                refs_to_add = random.randint(3, 6)
                available_refs = [d for d in self.doc_ids if d != doc['id']]

                if available_refs:
                    selected_refs = random.sample(
                        available_refs,
                        min(refs_to_add, len(available_refs))
                    )

                    added_refs = 0
                    for ref_doc in selected_refs:
                        if len(sentences) > 4 and added_refs < 4:  # Максимум 4 ссылки на документ
                            insert_idx = random.randint(1, len(sentences) - 2)
                            phrase = random.choice(reference_phrases).replace("{DOC}", ref_doc)
                            sentences[insert_idx] = sentences[insert_idx] + phrase
                            added_refs += 1

                    doc['raw_content'] = '. '.join(sentences)

                    # Обновляем контент
                    metadata_str = self.content_gen.format_metadata(doc['metadata'])
                    doc['content'] = f"---\n{metadata_str}\n---\n\n{doc['raw_content']}"

    def _add_explicit_references(self):
        """Добавляет явные ссылки между тематически связанными документами"""
        print("  Adding explicit cross-references...")

        # Группируем документы по темам
        topic_groups = {}

        for doc in self.documents:
            content_lower = doc['content'].lower()

            # Определяем темы
            topics = []
            if any(word in content_lower for word in ['elixir', 'potion', 'brew']):
                topics.append('magic')
            if any(word in content_lower for word in ['oakhaven', 'settlement', 'village']):
                topics.append('settlement')
            if any(word in content_lower for word in ['imperial', 'defense', 'military']):
                topics.append('military')
            if any(word in content_lower for word in ['trade', 'economy', 'market']):
                topics.append('economy')
            if any(word in content_lower for word in ['lorekeeper', 'alchemist', 'scholar']):
                topics.append('lore')
            if any(word in content_lower for word in ['stone', 'monolith', 'menhir']):
                topics.append('stones')

            for topic in topics:
                if topic not in topic_groups:
                    topic_groups[topic] = []
                topic_groups[topic].append(doc)

        # Добавляем ссылки внутри групп
        references_added = 0
        for topic, docs in topic_groups.items():
            if len(docs) > 1:
                for doc in docs:
                    other_docs = [d for d in docs if d['id'] != doc['id']]
                    if other_docs:
                        # Выбираем 1-2 документа для ссылки
                        ref_docs = random.sample(other_docs, min(2, len(other_docs)))

                        for ref_doc in ref_docs:
                            ref_text = f"\n\n**Related to {topic}:** See {ref_doc['id']} for complementary information."
                            doc['raw_content'] += ref_text
                            references_added += 1

                            # Обновляем полный контент
                            metadata_str = self.content_gen.format_metadata(doc['metadata'])
                            doc['content'] = f"---\n{metadata_str}\n---\n\n{doc['raw_content']}"

        print(f"  Added {references_added} explicit cross-references")

    def save_documents(self, knowledge_base_folder="knowledge_base", generated_folder="generated"):
        """Сохраняет документы в новые папки"""

        # Создаём папки
        os.makedirs(knowledge_base_folder, exist_ok=True)
        os.makedirs(generated_folder, exist_ok=True)

        # Сохраняем документы базы знаний
        for doc in self.documents:
            filename = f"{knowledge_base_folder}/{doc['id']}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(doc['content'])

        # Сохраняем индекс базы знаний
        index = []
        for doc in self.documents:
            index.append({
                'id': doc['id'],
                'type': doc['type'],
                'title': doc['metadata'].get('title', 'Untitled'),
                'author': doc['metadata'].get('author', 'Unknown'),
                'word_count': len(doc['raw_content'].split())
            })

        index_path = f"{generated_folder}/knowledge_base_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        print(f"✓ Saved {len(self.documents)} documents to {knowledge_base_folder}/")
        print(f"✓ Saved index to {index_path}")

        return len(self.documents)

def generate_qa_pairs(documents, world_data, terms_map, generated_folder="generated"):
    """Генерирует QA пары двух типов: Few-Shot и Chain-of-Thought"""

    print("\nGenerating QA pairs...")

    # Собираем информацию из документов
    doc_by_type = {}
    for doc in documents:
        doc_type = doc['type']
        if doc_type not in doc_by_type:
            doc_by_type[doc_type] = []
        doc_by_type[doc_type].append(doc['id'])

    # Получаем вымышленные термины
    hero = terms_map.get("characters", {}).get("Hero", "Veridix")
    strong_hero = terms_map.get("characters", {}).get("Strong Hero", "Megalix")
    alchemist = terms_map.get("characters", {}).get("Alchemist", "Alchemix")
    chief = terms_map.get("characters", {}).get("Chief", "Stentorix")
    bard = terms_map.get("characters", {}).get("Bard", "Melodix")

    magic_potion = terms_map.get("items", {}).get("Magic Potion", "Sunstone Elixir")
    village = terms_map.get("terms", {}).get("village", "Oakhaven")

    # Генерируем QA пары
    qa_pairs = []

    # 1. Few-Shot Template QA pairs
    few_shot_qa = [
        {
            "template_type": "few_shot",
            "question": f"What are the main ingredients of {magic_potion}?",
            "answer": f"The primary ingredient of {magic_potion} is moonleaf harvested during specific celestial alignments, along with secondary components like star-moss and crystalized dew.",
            "source_docs": doc_by_type.get('encyclopedia', ['ENCY_001', 'ENCY_010'])[:2],
            "difficulty": "easy",
            "category": "magic_items",
            "context_required": True,
            "reasoning_steps": []
        },
        {
            "template_type": "few_shot",
            "question": f"Why is {strong_hero} permanently strong?",
            "answer": f"{strong_hero} gained permanent strength from accidental exposure to {magic_potion} as an infant, unlike others who need to consume it regularly for temporary effects.",
            "source_docs": doc_by_type.get('myth', ['MYTH_001']) + doc_by_type.get('encyclopedia', ['ENCY_005'])[:1],
            "difficulty": "medium",
            "category": "characters",
            "context_required": True,
            "reasoning_steps": []
        },
        {
            "template_type": "few_shot",
            "question": f"What are the defenses of {village}?",
            "answer": f"{village} uses natural terrain advantages, strategic monolith placements, trained militia, and early warning systems for defense against Imperial forces.",
            "source_docs": doc_by_type.get('encyclopedia', ['ENCY_002'])[:1] + doc_by_type.get('report', ['REP_005'])[:1],
            "difficulty": "medium",
            "category": "defense",
            "context_required": True,
            "reasoning_steps": []
        },
        {
            "template_type": "few_shot",
            "question": f"What is {alchemist}'s primary responsibility?",
            "answer": f"{alchemist} is responsible for brewing the {magic_potion}, studying medicinal herbs, preserving ancient knowledge, and serving as a healer for the community.",
            "source_docs": doc_by_type.get('encyclopedia', ['ENCY_004'])[:1] + doc_by_type.get('journal', ['JOURN_003'])[:1],
            "difficulty": "easy",
            "category": "roles",
            "context_required": True,
            "reasoning_steps": []
        },
        {
            "template_type": "few_shot",
            "question": "How are standing stones classified?",
            "answer": "Standing stones are classified into three sizes: Standard (2 meters), Grande (3 meters), and Colossal (4+ meters), each with different uses and significance.",
            "source_docs": doc_by_type.get('encyclopedia', ['ENCY_005'])[:1] + doc_by_type.get('report', ['REP_007'])[:1],
            "difficulty": "easy",
            "category": "artifacts",
            "context_required": True,
            "reasoning_steps": []
        }
    ]

    # 2. Chain-of-Thought QA pairs
    chain_of_thought_qa = [
        {
            "template_type": "chain_of_thought",
            "question": f"Based on the documents, explain how {hero} typically approaches conflicts with Imperial forces and why this strategy is effective.",
            "answer": f"""{hero}'s strategy involves three key elements: 1) Strategic use of {magic_potion} for enhanced capabilities during critical moments, 2) Utilization of terrain knowledge to control engagement locations, and 3) Coordinated actions with {strong_hero} and other defenders. This approach is effective because it maximizes limited resources, exploits Imperial reliance on conventional tactics, and leverages local knowledge advantages.""",
            "source_docs": doc_by_type.get('journal', ['JOURN_001', 'JOURN_003'])[:2] + doc_by_type.get('report', ['REP_002'])[:1],
            "difficulty": "hard",
            "category": "strategy",
            "context_required": True,
            "reasoning_steps": [
                "First, identify {hero}'s resources and limitations from settlement documents",
                "Second, analyze Imperial tactical patterns from military reports",
                "Third, examine specific conflict accounts in journal entries",
                "Fourth, synthesize how {hero}'s approach counters Imperial weaknesses",
                "Finally, evaluate effectiveness based on documented outcomes"
            ]
        },
        {
            "template_type": "chain_of_thought",
            "question": f"Trace the economic relationship between {village} and nearby settlements, explaining both dependencies and points of friction.",
            "answer": f"""The economic relationship involves: 1) {village} exports standing stones and herbal remedies, 2) Imports essential goods like olive oil and tools from trading ports, 3) Experiences friction over trade route control and resource access rights, 4) Maintains delicate balance between self-sufficiency and interdependence. Key friction points include disputes over quarrying rights and competition for limited trading partnerships.""",
            "source_docs": doc_by_type.get('encyclopedia', ['ENCY_005'])[:1] + doc_by_type.get('report', ['REP_003', 'REP_007'])[:2] + doc_by_type.get('letter', ['LETTER_001'])[:1],
            "difficulty": "hard",
            "category": "economics",
            "context_required": True,
            "reasoning_steps": [
                "Identify {village}'s primary exports from economic documents",
                "List imported goods and their sources from trade records",
                "Analyze conflict documentation for friction points",
                "Examine negotiation records for relationship dynamics",
                "Synthesize into comprehensive economic relationship analysis"
            ]
        },
        {
            "template_type": "chain_of_thought",
            "question": f"Compare and contrast the leadership styles of {chief} and the Imperial commander, analyzing their effectiveness in their respective contexts.",
            "answer": f"""{chief} employs consensual, tradition-based leadership emphasizing community cohesion and adaptive defense. The Imperial commander uses hierarchical, discipline-focused command prioritizing expansion and control. {chief}'s style excels in maintaining morale and leveraging local knowledge but struggles with rapid large-scale coordination. The Imperial approach enables efficient large-force management but fails against unconventional resistance and alienates local populations. Effectiveness depends entirely on context: Imperial methods work for territorial control, while {chief}'s approach succeeds in community defense.""",
            "source_docs": doc_by_type.get('encyclopedia', ['ENCY_002'])[:1] + doc_by_type.get('report', ['REP_001', 'REP_004'])[:2] + doc_by_type.get('journal', ['JOURN_005'])[:1],
            "difficulty": "hard",
            "category": "leadership",
            "context_required": True,
            "reasoning_steps": [
                "Extract leadership principles from {chief}'s documented decisions",
                "Analyze Imperial command structure from military documents",
                "Compare outcomes in specific documented conflicts",
                "Evaluate adaptability to different situations",
                "Assess long-term effectiveness in respective goals"
            ]
        },
        {
            "template_type": "chain_of_thought",
            "question": f"Analyze the role of {bard} in the community, explaining both the cultural significance and the practical challenges this role presents.",
            "answer": f"""{bard} serves as cultural preserver, entertainer, and historical chronicler. Cultural significance includes: 1) Transmission of oral history and traditions, 2) Reinforcement of community identity through performance, 3) Mediation of social tensions through satire. Practical challenges include: 1) Balancing artistic expression with community standards, 2) Economic dependence on community support, 3) Preservation of accuracy in historical accounts, 4) Navigation of political sensitivities in content.""",
            "source_docs": doc_by_type.get('encyclopedia', ['ENCY_006'])[:1] + doc_by_type.get('journal', ['JOURN_004', 'JOURN_007'])[:2] + doc_by_type.get('decree', ['DECR_002'])[:1],
            "difficulty": "medium",
            "category": "culture",
            "context_required": True,
            "reasoning_steps": [
                "Identify documented performances and their reception",
                "Analyze community regulations affecting {bard}'s role",
                "Examine historical accounts preserved by {bard}",
                "Evaluate economic and social support systems",
                "Synthesize into comprehensive role analysis"
            ]
        },
        {
            "template_type": "chain_of_thought",
            "question": "Explain the ecological adaptation strategies of the settlement and how they reflect the community's relationship with the environment.",
            "answer": """Ecological adaptation strategies include: 1) Seasonal migration patterns following resource availability, 2) Sustainable harvesting techniques preserving regeneration capacity, 3) Integration of settlement design with natural topography, 4) Use of native materials in construction. These strategies reflect a symbiotic relationship where the community views itself as part of the ecosystem rather than separate from it, prioritizing long-term sustainability over short-term exploitation.""",
            "source_docs": doc_by_type.get('encyclopedia', ['ENCY_007', 'ENCY_009'])[:2] + doc_by_type.get('report', ['REP_006'])[:1] + doc_by_type.get('journal', ['JOURN_008'])[:1],
            "difficulty": "hard",
            "category": "ecology",
            "context_required": True,
            "reasoning_steps": [
                "Document resource management practices",
                "Analyze settlement design in relation to environment",
                "Examine seasonal patterns and adaptations",
                "Identify philosophical principles in community documents",
                "Synthesize into ecological relationship analysis"
            ]
        }
    ]

    # Объединяем оба типа
    qa_pairs = few_shot_qa + chain_of_thought_qa

    # Сохраняем в два отдельных файла в generated папке
    few_shot_path = f"{generated_folder}/few_shot_qa_pairs.jsonl"
    with open(few_shot_path, 'w', encoding='utf-8') as f:
        for qa in few_shot_qa:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    chain_of_thought_path = f"{generated_folder}/chain_of_thought_qa_pairs.jsonl"
    with open(chain_of_thought_path, 'w', encoding='utf-8') as f:
        for qa in chain_of_thought_qa:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    # И общий файл
    output_file = f"{generated_folder}/qa_pairs.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for qa in qa_pairs:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')

    print(f"✓ Generated {len(few_shot_qa)} Few-Shot QA pairs")
    print(f"✓ Generated {len(chain_of_thought_qa)} Chain-of-Thought QA pairs")
    print(f"✓ QA pairs saved to {generated_folder}/")

    return qa_pairs

def save_world_data(world_data, terms_map, generated_folder="generated"):
    """Сохраняет данные мира в generated папке"""

    # Сохраняем данные мира
    world_data_path = f"{generated_folder}/fictional_world.json"
    with open(world_data_path, 'w', encoding='utf-8') as f:
        json.dump(world_data, f, indent=2, ensure_ascii=False)

    # Сохраняем маппинг терминов
    terms_map_path = f"{generated_folder}/terms_map.json"
    with open(terms_map_path, 'w', encoding='utf-8') as f:
        json.dump(terms_map, f, indent=2, ensure_ascii=False)

    print(f"✓ World data saved to {generated_folder}/")
    return world_data_path, terms_map_path

def save_generation_stats(documents, world_data, generated_folder="generated"):
    """Сохраняет статистику генерации"""

    stats = {
        'generation_date': datetime.now().isoformat(),
        'universe': world_data.get('fictional_universe', 'Unknown'),
        'total_documents': len(documents),
        'document_types': {},
        'word_counts': {},
        'characters_created': len(world_data.get('characters', [])),
        'regions_created': len(world_data.get('regions', [])),
        'magic_items_created': len(world_data.get('magic_items', [])),
        'historical_events_created': len(world_data.get('historical_events', []))
    }

    # Статистика по типам документов
    for doc in documents:
        doc_type = doc['type']
        stats['document_types'][doc_type] = stats['document_types'].get(doc_type, 0) + 1

        word_count = len(doc['raw_content'].split())
        if doc_type not in stats['word_counts']:
            stats['word_counts'][doc_type] = {'total': 0, 'count': 0, 'average': 0}

        stats['word_counts'][doc_type]['total'] += word_count
        stats['word_counts'][doc_type]['count'] += 1

    # Рассчитываем среднее
    for doc_type in stats['word_counts']:
        if stats['word_counts'][doc_type]['count'] > 0:
            stats['word_counts'][doc_type]['average'] = (
                    stats['word_counts'][doc_type]['total'] /
                    stats['word_counts'][doc_type]['count']
            )

    stats_path = f"{generated_folder}/generation_stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"✓ Generation stats saved to {stats_path}")
    return stats

def main():
    """Основная функция"""
    print("=" * 60)
    print("Generating Fictional Universe Documents")
    print("=" * 60)

    # 1. Создаём генератор
    generator = FictionalDocumentGenerator()

    # 2. Генерируем документы
    documents = generator.generate_document_set(50)

    # 3. Сохраняем документы базы знаний
    knowledge_base_folder = "knowledge_base"
    generated_folder = "generated"

    count = generator.save_documents(knowledge_base_folder, generated_folder)

    # 4. Сохраняем данные мира
    save_world_data(generator.world_data, generator.terms_map, generated_folder)

    # 5. Генерируем QA пары
    qa_pairs = generate_qa_pairs(documents, generator.world_data, generator.terms_map, generated_folder)

    # 6. Сохраняем статистику
    stats = save_generation_stats(documents, generator.world_data, generated_folder)

    print("\n" + "=" * 60)
    print("GENERATION COMPLETE!")
    print("=" * 60)

    print(f"\n📊 Statistics:")
    print(f"  Documents in knowledge base: {count}")
    print(f"  QA pairs generated: {len(qa_pairs)}")
    print(f"  Universe: {generator.world_data['fictional_universe']}")

    print(f"\n📁 Folder Structure:")
    print(f"  {knowledge_base_folder}/ - {count} document files for RAG testing")
    print(f"  {generated_folder}/ - Generated metadata and QA pairs")

    print(f"\n📁 Files in {generated_folder}/:")
    generated_files = [
        "fictional_world.json",
        "terms_map.json",
        "knowledge_base_index.json",
        "generation_stats.json",
        "qa_pairs.jsonl",
        "few_shot_qa_pairs.jsonl",
        "chain_of_thought_qa_pairs.jsonl"
    ]

    for file in generated_files:
        print(f"  - {file}")

    print(f"\n🎯 QA Pair Types:")
    few_shot = sum(1 for qa in qa_pairs if qa['template_type'] == 'few_shot')
    chain_of_thought = sum(1 for qa in qa_pairs if qa['template_type'] == 'chain_of_thought')
    print(f"  Few-Shot Template: {few_shot} pairs")
    print(f"  Chain-of-Thought: {chain_of_thought} pairs")

    print(f"\n✅ Ready for RAG testing!")
    print(f"\nUsage:")
    print(f"  1. Load documents from {knowledge_base_folder}/ into your RAG system")
    print(f"  2. Use QA pairs from {generated_folder}/ for testing")
    print(f"  3. Check terms_map.json for fictional term mappings")

if __name__ == "__main__":
    main()