# apps/world2/fictional_world_bible.py
import json
import random

class FictionalWorldBuilder:
    """Создатель вымышленного мира с сохранением маппинга"""

    def __init__(self):
        self.terms_map = {}  # original_fictional -> fictional_term
        self.categories = {}

    def build_world(self):
        """Создаёт полностью вымышленный мир"""

        # Генераторы названий
        def gen_gallic_name():
            prefixes = ['Ver', 'Mor', 'Tara', 'Carno', 'Belo', 'Lugo']
            suffixes = ['rix', 'os', 'ax', 'ix', 'us', 'ac']
            return random.choice(prefixes) + random.choice(suffixes)

        def gen_roman_name():
            names = ['Marcus', 'Lucius', 'Gaius', 'Titus', 'Septimus']
            family = ['Aurelius', 'Claudius', 'Flavius', 'Julius', 'Valerius']
            return f"{random.choice(names)} {random.choice(family)}"

        def gen_place_name():
            elements = ['Sil', 'Vor', 'Glen', 'Stone', 'Oak', 'River', 'Moon']
            types = ['burg', 'haven', 'ford', 'wood', 'hill', 'dale']
            return random.choice(elements) + random.choice(types)

        def gen_item_name():
            adjectives = ['Sun', 'Moon', 'Star', 'Crystal', 'Golden', 'Silver']
            nouns = ['Blade', 'Chalice', 'Amulet', 'Orb', 'Stone', 'Crown']
            return f"{random.choice(adjectives)} {random.choice(nouns)}"

        # Создаём вымышленный мир
        world = {
            "original_universe": "Asterix and Obelix",
            "fictional_universe": "The Chronicles of Veridonia",
            "description": "A fictional universe inspired by Asterix structure but with completely original names and terms",

            "country_name": "Veridonia",
            "time_period": "Age of the Twin Suns",

            "regions": [
                {
                    "original": "Armorican Village",
                    "fictional": "Oakhaven",
                    "description": "A small village in the Emerald Valley that miraculously resists Imperial occupation.",
                    "key_locations": ["Town square", "Alchemist's tower", "Fishery", "Stone quarry"],
                    "climate": "Temperate, with misty mornings"
                },
                {
                    "original": "Roman Camps",
                    "fictional": "Imperial Outposts",
                    "description": "Military camps surrounding the valley, constantly being rebuilt after attacks.",
                    "key_locations": ["Fort Argentum", "Fort Ferrum", "Fort Aurum", "Fort Plumbum"],
                    "climate": "Arid, dusty"
                },
                {
                    "original": "Lutetia",
                    "fictional": "Silverport",
                    "description": "Bustling trading town with markets and Imperial influence.",
                    "key_locations": ["Grand Bazaar", "Sailor's Rest Inn", "Imperial garrison"],
                    "climate": "Coastal, humid"
                }
            ],

            "factions": [
                {
                    "original": "Gauls",
                    "fictional": "Valefolk",
                    "description": "Proud inhabitants of the Emerald Valley, known for resilience.",
                    "symbol": "Oak tree with twin suns",
                    "colors": ["Green", "Brown"]
                },
                {
                    "original": "Romans",
                    "fictional": "Imperials",
                    "description": "Expansionist empire trying to conquer the valley.",
                    "symbol": "Iron eagle",
                    "colors": ["Red", "Gold"]
                },
                {
                    "original": "Druids",
                    "fictional": "Lorekeepers",
                    "description": "Wise scholars and alchemists preserving ancient knowledge.",
                    "symbol": "Crystal orb",
                    "colors": ["Blue", "White"]
                }
            ],

            "characters": [],

            "magic_items": [],

            "historical_events": [],

            "unique_terms": []
        }

        # Генерация персонажей
        characters_data = [
            {"role": "hero", "traits": ["clever", "small", "strategic"]},
            {"role": "strong_hero", "traits": ["strong", "friendly", "loves food"]},
            {"role": "alchemist", "traits": ["wise", "old", "knowledgeable"]},
            {"role": "chief", "traits": ["proud", "loud", "respected"]},
            {"role": "bard", "traits": ["musical", "unskilled", "optimistic"]},
            {"role": "emperor", "traits": ["ambitious", "strategic", "proud"]},
            {"role": "blacksmith", "traits": ["strong", "hot-tempered", "skilled"]},
            {"role": "fisher", "traits": ["stubborn", "proud", "traditional"]}
        ]

        for char_data in characters_data:
            original_name = char_data["role"].replace("_", " ").title()
            fictional_name = gen_gallic_name() if char_data["role"] != "emperor" else gen_roman_name()

            character = {
                "id": char_data["role"],
                "original_name": original_name,
                "fictional_name": fictional_name,
                "type": char_data["role"],
                "description": f"A {char_data['traits'][0]} {char_data['role'].replace('_', ' ')} from the stories.",
                "traits": char_data["traits"]
            }
            world["characters"].append(character)
            self.terms_map[original_name] = fictional_name

        # Генерация магических предметов
        items_data = [
            {"original": "Magic Potion", "type": "potion", "effect": "temporary superhuman strength"},
            {"original": "Golden Sickle", "type": "tool", "effect": "harvests special herbs"},
            {"original": "Menhir", "type": "artifact", "effect": "standing stone with mysterious properties"},
            {"original": "Roman Standard", "type": "symbol", "effect": "military banner"},
            {"original": "Wild Boar", "type": "food", "effect": "favorite feast dish"}
        ]

        for item in items_data:
            fictional_name = gen_item_name()
            world["magic_items"].append({
                "original": item["original"],
                "fictional": fictional_name,
                "type": item["type"],
                "effect": item["effect"]
            })
            self.terms_map[item["original"]] = fictional_name

        # Генерация исторических событий
        events_data = [
            {"original": "Potion Accident", "impact": "high", "year": "50 years ago"},
            {"original": "Battle of Babaorum", "impact": "medium", "year": "10 years ago"},
            {"original": "Caesar's Invasion", "impact": "high", "year": "20 years ago"},
            {"original": "First Resistance", "impact": "high", "year": "30 years ago"}
        ]

        for event in events_data:
            event_name = f"The {random.choice(['Great', 'Silent', 'Emerald', 'Crystal'])} {random.choice(['Accord', 'War', 'Pact', 'Rebellion'])}"
            world["historical_events"].append({
                "original": event["original"],
                "fictional": event_name,
                "impact": event["impact"],
                "year": event["year"]
            })
            self.terms_map[event["original"]] = event_name

        # Генерация уникальных терминов
        terms_to_replace = [
            "Gaul", "Rome", "mistletoe", "Getafix's hut",
            "boar", "feast", "centurion", "legion",
            "druid", "bard", "village", "camp"
        ]

        for term in terms_to_replace:
            fictional_term = random.choice([
                f"{random.choice(['Sun', 'Moon', 'Star'])}{random.choice(['stone', 'wood', 'leaf'])}",
                f"{random.choice(['Crystal', 'Iron', 'Oak'])} {random.choice(['rite', 'way', 'path'])}",
                gen_place_name().lower()
            ])
            world["unique_terms"].append({
                "original": term,
                "fictional": fictional_term
            })
            self.terms_map[term] = fictional_term

        # Сохраняем категории для быстрого доступа
        self.categories = {
            "characters": {c["original_name"]: c["fictional_name"] for c in world["characters"]},
            "items": {i["original"]: i["fictional"] for i in world["magic_items"]},
            "events": {e["original"]: e["fictional"] for e in world["historical_events"]},
            "terms": {t["original"]: t["fictional"] for t in world["unique_terms"]}
        }

        return world, self.terms_map

    def save_mapping(self, filename="terms_map.json"):
        """Сохраняет маппинг терминов"""
        mapping_info = {
            "metadata": {
                "original_universe": "Asterix and Obelix (French comic series)",
                "fictional_universe": "The Chronicles of Veridonia",
                "creation_date": "2024",
                "purpose": "RAG testing - avoid model memory contamination",
                "description": "All recognizable names and terms from Asterix have been replaced with fictional ones while preserving narrative structure and relationships."
            },
            "mapping_strategy": {
                "character_names": "Generated using Celtic/Latin-inspired prefixes and suffixes",
                "place_names": "Descriptive English compounds (Oakhaven, Silverport)",
                "magic_items": "Adjective+Noun patterns (Sun Blade, Crystal Orb)",
                "events": "Thematic titles (Great Accord, Emerald Rebellion)"
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
    builder = FictionalWorldBuilder()
    world_data, mapping = builder.build_world()

    # Сохраняем данные мира
    with open("fictional_world.json", "w", encoding="utf-8") as f:
        json.dump(world_data, f, indent=2, ensure_ascii=False)

    # Сохраняем маппинг
    builder.save_mapping()

    print("=" * 60)
    print("Fictional World Created Successfully!")
    print(f"Universe: {world_data['fictional_universe']}")
    print(f"Total terms mapped: {len(mapping)}")
    print("=" * 60)

    # Показываем несколько примеров
    print("\nExample mappings:")
    examples = list(mapping.items())[:10]
    for orig, fict in examples:
        print(f"  {orig:20} → {fict}")

    return world_data, mapping

# Создаём мир и сохраняем его
if __name__ == "__main__":
    main()