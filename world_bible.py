# world_bible.py - Основные данные о мире
WORLD_DATA = {
    "country_name": "Gaul",
    "time_period": "50 BC",

    "regions": [
        {
            "name": "Armorican Village",
            "description": "The small coastal village in northwest Gaul that miraculously resists Roman occupation.",
            "key_locations": ["Village square", "Getafix's hut", "Fishmonger's shop", "Menhir quarry"],
            "key_people": ["Asterix", "Obelix", "Chief Vitalstatistix", "Getafix", "Cacofonix"]
        },
        {
            "name": "Roman Camps",
            "description": "Various Roman camps surrounding the village, constantly being rebuilt.",
            "key_locations": ["Camp of Babaorum", "Camp of Laudanum", "Camp of Aquarium", "Camp of Petibonum"],
            "key_people": ["Julius Caesar", "Centurions", "Roman soldiers"]
        },
        {
            "name": "Lutetia",
            "description": "Busy Gallic town with markets, inns, and Roman influence.",
            "key_locations": ["Marketplace", "Inn of the Boar", "Roman garrison"],
            "key_people": ["Tournedix", "Various merchants"]
        }
    ],

    "characters": [
        {"id": "asterix", "name": "Asterix", "type": "hero", "description": "Small but clever Gaulish warrior, uses magic potion for strength."},
        {"id": "obelix", "name": "Obelix", "type": "hero", "description": "Menhir deliveryman, permanently strong from falling into potion as baby."},
        {"id": "getafix", "name": "Getafix", "type": "druid", "description": "Village druid, brewers of magic potion and other remedies."},
        {"id": "vitalstatistix", "name": "Chief Vitalstatistix", "type": "chief", "description": "Village chief, carried on shield by his men."},
        {"id": "cacofonix", "name": "Cacofonix", "type": "bard", "description": "Terrible bard who is often tied up during feasts."},
        {"id": "julius_caesar", "name": "Julius Caesar", "type": "roman", "description": "Roman Emperor, determined to conquer Gaul."},
        {"id": "fulliautomatix", "name": "Fulliautomatix", "type": "blacksmith", "description": "Village blacksmith, quick to fight with Unhygienix."},
        {"id": "unhygienix", "name": "Unhygienix", "type": "fishmonger", "description": "Fishmonger, often fights with Fulliautomatix."}
    ],

    "magic_items": [
        {"id": "magic_potion", "name": "Magic Potion", "description": "Gives superhuman strength, brewed by Getafix from mistletoe."},
        {"id": "golden_sickle", "name": "Golden Sickle", "description": "Used by druids to cut mistletoe for potions."},
        {"id": "menhir", "name": "Menhir", "description": "Large standing stones delivered by Obelix."},
        {"id": "roman_standard", "name": "Roman Standard", "description": "Symbol of Roman authority, often stolen by Gauls."}
    ],

    "organizations": [
        {"id": "village_council", "name": "Village Council", "description": "Governing body of the Armorican village."},
        {"id": "roman_legion", "name": "Roman Legion", "description": "Military organization of Rome."},
        {"id": "druid_circle", "name": "Druid Circle", "description": "Society of Gallic druids."},
        {"id": "fishmongers_guild", "name": "Fishmongers Guild", "description": "Organization of fish traders."}
    ],

    "historical_events": [
        {"id": "potion_accident", "name": "Potion Accident", "year": "50 BC", "description": "Obelix falls into cauldron of magic potion as baby."},
        {"id": "battle_babaorum", "name": "Battle of Babaorum", "year": "50 BC", "description": "Gauls defeat Romans at Camp Babaorum."},
        {"id": "caesar_invasion", "name": "Caesar's Invasion", "year": "58 BC", "description": "Julius Caesar begins conquest of Gaul."}
    ],

    "document_types": {
        "encyclopedia": "Factual articles about people, places, and items.",
        "decree": "Official laws and proclamations.",
        "journal": "Personal diaries and logs.",
        "report": "Military or scientific reports.",
        "myth": "Legends and folk stories.",
        "letter": "Personal correspondence.",
        "recipe": "Cooking or potion recipes."
    }
}