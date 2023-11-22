class Boss:
    def __init__(self, id, name, location, location_short, zone_id, difficulty, group_size, alternative_trigger):
        self.id = id
        self.name = name
        self.location = location
        self.location_short = location_short
        self.zone_id = zone_id
        self.difficulty = difficulty
        self.group_size = group_size
        self.alternative_trigger = alternative_trigger
        self.encounter_start_found = False
        self.encounter_end_found = False


# Boss data
boss_data = [
    # Black Wing Lair
    Boss(610, "Razorgore the Untamed", "Black Wing Lair", "bwl", 469, 9, 40, []),
    Boss(611, "Vaelastrasz the Corrupt", "Black Wing Lair", "bwl", 469, 9, 40, []),
    Boss(612, "Broodlord Lashlayer", "Black Wing Lair", "bwl", 469, 9, 40, []),
    Boss(613, "Firemaw", "Black Wing Lair", "bwl", 469, 9, 40, []),
    Boss(614, "Ebonroc", "Black Wing Lair", "bwl", 469, 9, 40, []),
    Boss(615, "Flamegor", "Black Wing Lair", "bwl", 469, 9, 40, []),
    Boss(616, "Chromaggus", "Black Wing Lair", "bwl", 469, 9, 40, []),
    Boss(617, "Nefarian", "Black Wing Lair", "bwl", 469, 9, 40, []),

    # Molten Core
    Boss(663, "Lucifron", "Molten Core", "mc", 409, 9, 40, []),
    Boss(664, "Magmadar", "Molten Core", "mc", 409, 9, 40, []),
    Boss(665, "Gehennas", "Molten Core", "mc", 409, 9, 40, []),
    Boss(666, "Garr", "Molten Core", "mc", 409, 9, 40, []),
    Boss(667, "Shazzrah", "Molten Core", "mc", 409, 9, 40, []),
    Boss(668, "Baron Geddon", "Molten Core", "mc", 409, 9, 40, []),
    Boss(669, "Sulfuron Harbinger", "Molten Core", "mc", 409, 9, 40, []),
    Boss(670, "Golemagg the Incinerator", "Molten Core", "mc", 409, 9, 40, []),
    Boss(671, "Majordomo Executus", "Molten Core", "mc", 409, 9, 40, []),
    Boss(672, "Ragnaros", "Molten Core", "mc", 409, 9, 40, []),

    # Temple of Ahn'Qiraj
    Boss(709, "The Prophet Skeram", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, []),
    Boss(710, "Silithid Royalty", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, ["Lord Kri", "Princess Yauj", "Vem"]),
    Boss(711, "Battleguard Sartura", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, []),
    Boss(712, "Fankriss the Unyielding", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, []),
    Boss(713, "Viscidus", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, []),
    Boss(714, "Princess Huhuran", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, []),
    Boss(715, "Twin Emperors", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, ["Emperor Vek'lor", "Emperor Vek'nilash"]),
    Boss(716, "Ouro", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, []),
    Boss(717, "C'thun", "Temple of Ahn'Qiraj", "aq40", 531, 9, 40, ["Eye of C'Thun"]),

    # Ruins of Ahn'Qiraj
    Boss(718, "Kurinnaxx", "Ruins of Ahn'Qiraj", "aq20", 509, 148, 20, []),
    Boss(719, "General Rajaxx", "Ruins of Ahn'Qiraj", "aq20", 509, 148, 20, []),
    Boss(720, "Moam", "Ruins of Ahn'Qiraj", "aq20", 509, 148, 20, []),
    Boss(721, "Buru the Gorger", "Ruins of Ahn'Qiraj", "aq20", 509, 148, 20, []),
    Boss(722, "Ayamiss the Hunter", "Ruins of Ahn'Qiraj", "aq20", 509, 148, 20, []),
    Boss(723, "Ossirian the Unscarred", "Ruins of Ahn'Qiraj", "aq20", 509, 148, 20, []),

    # Zul'Gurub
    Boss(784, "High Priest Venoxis", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(785, "High Priestess Jeklik", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(786, "High Priestess Mar'li", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(787, "Bloodlord Mandokir", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(788, "Edge of Madness", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(789, "High Priest Thekal", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(790, "Gahz'ranka", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(791, "High Priestess Arlokk", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(792, "Jin'do the Hexxer", "Zul'Gurub", "zg", 309, 148, 20, []),
    Boss(793, "Hakkar", "Zul'Gurub", "zg", 309, 148, 20, []),

    # Onyxia"s Lair
    Boss(1084, "Onyxia", "Onyxia's Lair", "ony", 249, 9, 40, []),

    # Naxxramas
    # The Arachnid Quarter
    Boss(1107, "Anub'Rekhan", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1110, "Grand Widow Faerlina", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1116, "Maexxna", "Naxxramas", "naxx", 533, 9, 40, []),
    # The Plague Quarter
    Boss(1117, "Noth the Plaguebringer", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1112, "Heigan the Unclean", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1115, "Loatheb", "Naxxramas", "naxx", 533, 9, 40, []),
    # The Military Quarter
    Boss(1113, "Instructor Razuvious", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1109, "Gothik the Harvester", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1121, "The Four Horsemen", "Naxxramas", "naxx", 533, 9, 40, ["Thane Korth'azz", "Lady Blaumeux", "Sir Zeliek", "Highlord Mograine"]),
    # The Construct Quarter
    Boss(1118, "Patchwerk", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1111, "Grobbulus", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1108, "Gluth", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1120, "Thaddius", "Naxxramas", "naxx", 533, 9, 40, []),
    # Frostwyrm Lair
    Boss(1119, "Sapphiron", "Naxxramas", "naxx", 533, 9, 40, []),
    Boss(1114, "Kel'Thuzad", "Naxxramas", "naxx", 533, 9, 40, [])
]
