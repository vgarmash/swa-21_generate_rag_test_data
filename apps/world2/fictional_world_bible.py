# apps/world2/fictional_world_bible.py
import json
import random
import os

class FictionalWorldBuilder:
    """Создатель вымышленного мира с сохранением маппинга"""

    def __init__(self):
        self.terms_map = {}
        self.categories = {}
        self.generated_content = set()

    def build_world(self):
        """Создаёт полностью вымышленный мир"""

        # Генераторы названий с большей вариативностью
        def gen_character_name():
            prefixes = ['Ver', 'Mor', 'Tara', 'Carno', 'Belo', 'Lugo', 'Eri', 'Sylo', 'Quen', 'Neme']
            suffixes = ['rix', 'os', 'ax', 'ix', 'us', 'ac', 'or', 'el', 'ion', 'as']
            return random.choice(prefixes) + random.choice(suffixes)

        def gen_place_name():
            first = ['Sil', 'Vor', 'Glen', 'Stone', 'Oak', 'River', 'Moon', 'Star', 'Crystal', 'Iron']
            second = ['burg', 'haven', 'ford', 'wood', 'hill', 'dale', 'port', 'watch', 'reach', 'spire']
            return random.choice(first) + random.choice(second)

        def gen_item_name():
            adjectives = ['Sun', 'Moon', 'Star', 'Crystal', 'Golden', 'Silver', 'Iron', 'Obsidian', 'Jade', 'Amber']
            nouns = ['Blade', 'Chalice', 'Amulet', 'Orb', 'Stone', 'Crown', 'Shard', 'Talisman', 'Relic', 'Seal']
            return f"{random.choice(adjectives)} {random.choice(nouns)}"

        def gen_event_name():
            first = ['Great', 'Silent', 'Emerald', 'Crystal', 'Iron', 'Golden', 'Bloody', 'Forgotten', 'Ancient']
            second = ['Accord', 'War', 'Pact', 'Rebellion', 'Cataclysm', 'Alliance', 'Schism', 'Exodus', 'Convergence']
            return f"The {random.choice(first)} {random.choice(second)}"

        # Создаём вымышленный мир с большим разнообразием
        world_data = {
            "original_universe": "Asterix and Obelix",
            "fictional_universe": "Chronicles of Veridia",
            "description": "A fully fictional fantasy world inspired by comic adventure structure with original everything",

            "country_name": "Veridia",
            "time_period": "Age of Twin Moons",
            "era_suffix": "AM (After Moonfall)",

            "regions": [],
            "factions": [],
            "characters": [],
            "magic_items": [],
            "historical_events": [],
            "lore_elements": [],
            "unique_terms": []
        }

        # Генерация регионов
        regions_data = [
            {"type": "village", "climate": "temperate", "feature": "miraculously resists Imperial occupation"},
            {"type": "forest", "climate": "misty", "feature": "ancient magical woods"},
            {"type": "mountain", "climate": "alpine", "feature": "crystal-rich peaks"},
            {"type": "coastal", "climate": "humid", "feature": "bustling trade port"},
            {"type": "desert", "climate": "arid", "feature": "hidden oasis settlement"},
            {"type": "swamp", "climate": "damp", "feature": "mysterious bog villages"}
        ]

        for i, region_data in enumerate(regions_data[:4]):
            region_name = gen_place_name()
            world_data["regions"].append({
                "id": f"region_{i}",
                "name": region_name,
                "type": region_data["type"],
                "description": f"A {region_data['type']} in Veridia with {region_data['climate']} climate, known for {region_data['feature']}.",
                "climate": region_data["climate"],
                "key_locations": [
                    f"{random.choice(['Central', 'Old', 'Grand', 'New'])} {random.choice(['Square', 'Market', 'Tower', 'Hall'])}",
                    f"{random.choice(['Ancient', 'Secret', 'Forgotten', 'Sacred'])} {random.choice(['Grove', 'Shrine', 'Cavern', 'Spring'])}"
                ]
            })
            self.terms_map[f"region_{i}"] = region_name

        # Генерация фракций
        factions_data = [
            {"type": "resistance", "traits": ["proud", "resilient", "traditional"]},
            {"type": "empire", "traits": ["expansionist", "disciplined", "technological"]},
            {"type": "scholars", "traits": ["wise", "secretive", "knowledgeable"]},
            {"type": "merchants", "traits": ["wealthy", "connected", "pragmatic"]}
        ]

        for i, faction_data in enumerate(factions_data):
            faction_name = random.choice([
                "Valewardens", "Iron Empire", "Lorekeepers", "Silver Consortium",
                "Free Folk", "Crystal Order", "Star Alliance", "Moon Sect"
            ])
            world_data["factions"].append({
                "id": f"faction_{i}",
                "name": faction_name,
                "type": faction_data["type"],
                "description": f"A {faction_data['type']} faction known for being {', '.join(faction_data['traits'][:2])}.",
                "symbol": f"{random.choice(['Oak', 'Eagle', 'Orb', 'Coin'])} {random.choice(['Tree', 'Standard', 'Sigil', 'Emblem'])}",
                "colors": [random.choice(["Green", "Blue", "Red", "Gold"]), random.choice(["Silver", "White", "Black", "Bronze"])]
            })
            self.terms_map[f"faction_{i}"] = faction_name

        # Генерация персонажей с уникальными чертами
        characters_data = [
            {"role": "hero", "traits": ["clever", "strategic", "agile"], "skills": ["tactics", "stealth", "leadership"]},
            {"role": "strong_hero", "traits": ["strong", "loyal", "hearty"], "skills": ["strength", "endurance", "crafting"]},
            {"role": "alchemist", "traits": ["wise", "patient", "perceptive"], "skills": ["herbalism", "brewing", "lore"]},
            {"role": "chief", "traits": ["proud", "decisive", "charismatic"], "skills": ["diplomacy", "strategy", "oration"]},
            {"role": "bard", "traits": ["creative", "optimistic", "energetic"], "skills": ["music", "storytelling", "entertainment"]},
            {"role": "emperor", "traits": ["ambitious", "calculating", "disciplined"], "skills": ["strategy", "administration", "warfare"]},
            {"role": "blacksmith", "traits": ["strong", "skilled", "temperamental"], "skills": ["forging", "repair", "design"]},
            {"role": "fisher", "traits": ["stubborn", "traditional", "observant"], "skills": ["fishing", "navigation", "weather"]},
            {"role": "scout", "traits": ["stealthy", "observant", "enduring"], "skills": ["tracking", "reconnaissance", "survival"]},
            {"role": "healer", "traits": ["compassionate", "knowledgeable", "calm"], "skills": ["medicine", "herbalism", "healing"]}
        ]

        for char_data in characters_data:
            original_name = char_data["role"].replace("_", " ").title()
            fictional_name = gen_character_name()

            character = {
                "id": char_data["role"],
                "original_name": original_name,
                "fictional_name": fictional_name,
                "type": char_data["role"],
                "description": f"A {char_data['traits'][0]} {char_data['role'].replace('_', ' ')} known for {char_data['skills'][0]}.",
                "traits": char_data["traits"],
                "skills": char_data["skills"],
                "unique_feature": random.choice([
                    f"has a distinctive {random.choice(['scar', 'tattoo', 'accent', 'gesture'])}",
                    f"carries a {random.choice(['unique', 'ancient', 'family'])} {random.choice(['weapon', 'tool', 'amulet'])}",
                    f"is known for exceptional {char_data['skills'][-1]}",
                    f"has a mysterious past involving {random.choice(['the lost city', 'the ancient order', 'the fallen kingdom'])}"
                ])
            }
            world_data["characters"].append(character)
            self.terms_map[original_name] = fictional_name

        # Генерация магических предметов
        items_data = [
            {"original": "Magic Potion", "type": "potion", "effects": ["strength", "speed", "invulnerability"]},
            {"original": "Golden Sickle", "type": "tool", "effects": ["harvesting", "purifying", "focusing"]},
            {"original": "Menhir", "type": "artifact", "effects": ["protection", "energy", "memory"]},
            {"original": "Roman Standard", "type": "symbol", "effects": ["authority", "morale", "command"]},
            {"original": "Wild Boar", "type": "creature", "effects": ["nourishment", "celebration", "tradition"]},
            {"original": "Druid's Staff", "type": "focus", "effects": ["channeling", "amplification", "guidance"]},
            {"original": "Invisibility Potion", "type": "potion", "effects": ["stealth", "evasion", "infiltration"]}
        ]

        for item in items_data:
            fictional_name = gen_item_name()
            world_data["magic_items"].append({
                "original": item["original"],
                "fictional": fictional_name,
                "type": item["type"],
                "effects": item["effects"],
                "description": f"A {item['type']} used for {', '.join(item['effects'][:2])}. Often found in {random.choice(['ancient ruins', 'secret laboratories', 'sacred groves'])}.",
                "rarity": random.choice(["common", "uncommon", "rare", "legendary"])
            })
            self.terms_map[item["original"]] = fictional_name

        # Генерация исторических событий
        for i in range(6):
            event_name = gen_event_name()
            world_data["historical_events"].append({
                "id": f"event_{i}",
                "original": f"Historical Event {i+1}",
                "fictional": event_name,
                "year": f"{random.randint(100, 500)} {world_data['era_suffix'].split()[0]}",
                "description": f"A {random.choice(['major', 'minor', 'forgotten', 'celebrated'])} event that {random.choice(['shaped', 'divided', 'united', 'destroyed'])} the realm.",
                "impact": random.choice(["high", "medium", "low"]),
                "factions_involved": random.sample([f["name"] for f in world_data["factions"]], random.randint(2, 3))
            })
            self.terms_map[f"Historical Event {i+1}"] = event_name

        # Генерация уникальных терминов
        terms_to_replace = [
            "Gaul", "Rome", "mistletoe", "boar", "feast", "centurion",
            "legion", "druid", "bard", "village", "camp", "forest",
            "potion", "sword", "shield", "armor", "gold", "silver",
            "emperor", "chief", "warrior", "magic", "stone", "tree"
        ]

        for term in terms_to_replace:
            fictional_term = self._generate_fictional_term(term)
            world_data["unique_terms"].append({
                "original": term,
                "fictional": fictional_term,
                "category": random.choice(["material", "creature", "concept", "title", "place"])
            })
            self.terms_map[term] = fictional_term

        # Сохраняем категории для быстрого доступа
        self.categories = {
            "characters": {c["original_name"]: c["fictional_name"] for c in world_data["characters"]},
            "items": {i["original"]: i["fictional"] for i in world_data["magic_items"]},
            "events": {e["original"]: e["fictional"] for e in world_data["historical_events"]},
            "terms": {t["original"]: t["fictional"] for t in world_data["unique_terms"]},
            "regions": {r["id"]: r["name"] for r in world_data["regions"]},
            "factions": {f["id"]: f["name"] for f in world_data["factions"]}
        }

        return world_data, self.terms_map

    def _generate_fictional_term(self, original: str) -> str:
        """Генерирует вымышленный термин на основе оригинала"""
        term_map = {
            "Gaul": ["Veridia", "Aetheria", "Mythoria", "Eldoria"],
            "Rome": ["The Imperium", "The Dominion", "The Hegemony", "The Sovereignty"],
            "mistletoe": ["moonleaf", "star-moss", "sun-lichen", "dream-fern"],
            "boar": ["forest stag", "mountain tusker", "iron-hide boar", "crystal-tusk"],
            "feast": ["grand gathering", "moon festival", "sun celebration", "harvest banquet"],
            "centurion": ["legionnaire", "shield-captain", "iron-guard", "blade-commander"],
            "legion": ["iron host", "crystal legion", "star battalion", "moon cohort"],
            "druid": ["lorekeeper", "star-seer", "moon-sage", "earth-warden"],
            "bard": ["skald", "lore-singer", "story-weaver", "verse-smith"],
            "village": ["hamlet", "settlement", "enclave", "haven"],
            "camp": ["outpost", "garrison", "encampment", "fortification"],
            "forest": ["woods", "grove", "copse", "wildwood"],
            "potion": ["elixir", "tonic", "draught", "concoction"],
            "sword": ["blade", "glaive", "falchion", "cutlass"],
            "shield": ["buckler", "pavis", "aegis", "guard"],
            "armor": ["plate", "mail", "harness", "cuirass"],
            "gold": ["aurum", "sun-metal", "gleam-stone", "royal ore"],
            "silver": ["argentum", "moon-metal", "star-dust", "lunar ore"],
            "emperor": ["sovereign", "high ruler", "imperator", "supreme commander"],
            "chief": ["chieftain", "elder", "headman", "patriarch"],
            "warrior": ["fighter", "combatant", "champion", "defender"],
            "magic": ["arcana", "thaumaturgy", "sorcery", "enchantment"],
            "stone": ["rock", "boulder", "monolith", "menhir"],
            "tree": ["oak", "yew", "ash", "elm"]
        }

        return random.choice(term_map.get(original, [original + "-variant"]))

    def save_mapping(self, filename="generated/terms_map.json"):
        """Сохраняет маппинг терминов в папку generated"""

        # Создаём папку generated если её нет
        os.makedirs("generated", exist_ok=True)

        mapping_info = {
            "metadata": {
                "original_universe": "Asterix and Obelix (French comic series by René Goscinny and Albert Uderzo)",
                "fictional_universe": "Chronicles of Veridia",
                "creation_date": "2024",
                "purpose": "RAG testing - avoid model memory contamination with real-world references",
                "description": "All recognizable names, terms, and concepts from Asterix have been replaced with original fictional ones while preserving narrative structure, character archetypes, and thematic elements.",
                "note": "This dataset is designed to test RAG systems' ability to understand and reason about completely novel information."
            },
            "mapping_strategy": {
                "character_names": "Celtic/Latin-inspired original names preserving role archetypes",
                "place_names": "Descriptive fantasy toponyms reflecting location characteristics",
                "magic_items": "Fantasy adjective-noun combinations with thematic consistency",
                "events": "Dramatic historical-sounding titles with appropriate gravitas",
                "common_terms": "Thematic replacements maintaining semantic function in context"
            },
            "structural_preservation": {
                "hero_sidekick_dynamic": "Preserved (clever hero + strong companion)",
                "wise_elder_archetype": "Preserved (knowledgeable alchemist/scholar)",
                "comic_relief_character": "Preserved (enthusiastic but unskilled performer)",
                "authority_figures": "Preserved (village chief vs imperial ruler)",
                "community_dynamics": "Preserved (internal conflicts, celebrations, traditions)",
                "recurring_themes": "Adapted (resistance vs empire, magic vs technology)"
            },
            "term_mappings": self.terms_map,
            "categories": self.categories
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(mapping_info, f, indent=2, ensure_ascii=False)

        print(f"✓ Mapping saved to {filename}")
        return mapping_info

def main():
    """Основная функция для запуска скрипта"""

    # Создаём папку generated если её нет
    os.makedirs("generated", exist_ok=True)

    builder = FictionalWorldBuilder()
    world_data, mapping = builder.build_world()

    # Сохраняем данные мира в generated папку
    world_data_path = "generated/fictional_world.json"
    with open(world_data_path, "w", encoding="utf-8") as f:
        json.dump(world_data, f, indent=2, ensure_ascii=False)

    # Сохраняем маппинг
    builder.save_mapping()

    print("=" * 60)
    print("Fictional World Created Successfully!")
    print(f"Universe: {world_data['fictional_universe']}")
    print(f"Total unique terms: {len(mapping)}")
    print(f"Characters: {len(world_data['characters'])}")
    print(f"Regions: {len(world_data['regions'])}")
    print(f"Magic items: {len(world_data['magic_items'])}")
    print("=" * 60)

    # Показываем несколько примеров
    print("\nExample mappings (Original → Fictional):")
    print("-" * 40)

    # Показываем по категориям
    categories = [
        ("Hero", "hero"),
        ("Strong Hero", "strong_hero"),
        ("Magic Potion", "Magic Potion"),
        ("Village", "village"),
        ("Forest", "forest")
    ]

    for display_name, term in categories:
        if term in mapping:
            print(f"{display_name:15} → {mapping[term]}")

    return world_data, mapping

if __name__ == "__main__":
    main()