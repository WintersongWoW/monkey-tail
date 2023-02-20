class Boss:
    def __init__(self, id, name, location, zone_id, difficulty, group_size):
        self.id = id
        self.name = name
        self.location = location
        self.zone_id = zone_id
        self.difficulty = difficulty
        self.group_size = group_size
        self.encounter_start_found = False
        self.encounter_end_found = False

# Boss data
boss_data = [
    # Black Wing Lair
    Boss(610, "Razorgore the Untamed", "Black Wing Lair", 469, 9, 40),
    Boss(611, "Vaelastrasz the Corrupt", "Black Wing Lair", 469, 9, 40),
    Boss(612, "Broodlord Lashlayer", "Black Wing Lair", 469, 9, 40),
    Boss(613, "Firemaw", "Black Wing Lair", 469, 9, 40),
    Boss(614, "Ebonroc", "Black Wing Lair", 469, 9, 40),
    Boss(615, "Flamegor", "Black Wing Lair", 469, 9, 40),
    Boss(616, "Chromaggus", "Black Wing Lair", 469, 9, 40),
    Boss(617, "Nefarian", "Black Wing Lair", 469, 9, 40),

    # Molten Core
    Boss(663, "Lucifron", "Molten Core", 409, 9, 40),
    Boss(664, "Magmadar", "Molten Core", 409, 9, 40),
    Boss(665, "Gehennas", "Molten Core", 409, 9, 40),
    Boss(666, "Garr", "Molten Core", 409, 9, 40),
    Boss(667, "Shazzrah", "Molten Core", 409, 9, 40),
    Boss(668, "Baron Geddon", "Molten Core", 409, 9, 40),
    Boss(669, "Sulfuron Harbinger", "Molten Core", 409, 9, 40),
    Boss(670, "Golemagg the Incinerator", "Molten Core", 409, 9, 40),
    Boss(671, "Majordomo Executus", "Molten Core", 409, 9, 40),
    Boss(672, "Ragnaros", "Molten Core", 409, 9, 40),

    # Temple of Ahn'Qiraj
    Boss(709, "The Prophet Skeram", "Temple of Ahn'Qiraj", 531, 9, 40),
    Boss(710, "Silithid Royalty", "Temple of Ahn'Qiraj", 531, 9, 40),
    Boss(711, "Battleguard Sartura", "Temple of Ahn'Qiraj", 531, 9, 40),
    Boss(712, "Fankriss the Unyielding", "Temple of Ahn'Qiraj", 531, 9, 40),
    Boss(713, "Viscidus", "Temple of Ahn'Qiraj", 531, 9, 40),
    Boss(714, "Princess Huhuran", "Temple of Ahn'Qiraj", 531, 9, 40),
    Boss(715, "Twin Emperors", "Temple of Ahn'Qiraj", 531, 9, 40),
    Boss(716, "Ouro", "Temple of Ahn'Qiraj", 531, 9, 40),
    Boss(717, "C'thun", "Temple of Ahn'Qiraj", 531, 9, 40),

    # Ruins of Ahn'Qiraj
    Boss(718, "Kurinnaxx", "Ruins of Ahn'Qiraj", 509, 148, 20),
    Boss(719, "General Rajaxx", "Ruins of Ahn'Qiraj", 509, 148, 20),
    Boss(720, "Moam", "Ruins of Ahn'Qiraj", 509, 148, 20),
    Boss(721, "Buru the Gorger", "Ruins of Ahn'Qiraj", 509, 148, 20),
    Boss(722, "Ayamiss the Hunter", "Ruins of Ahn'Qiraj", 509, 148, 20),
    Boss(723, "Ossirian the Unscarred", "Ruins of Ahn'Qiraj", 509, 148, 20),

    # Zul'Gurub
    Boss(784, "High Priest Venoxis", "Zul'Gurub", 309, 148, 20),
    Boss(785, "High Priestess Jeklik", "Zul'Gurub", 309, 148, 20),
    Boss(786, "High Priestess Mar'li", "Zul'Gurub", 309, 148, 20),
    Boss(787, "Bloodlord Mandokir", "Zul'Gurub", 309, 148, 20),
    Boss(788, "Edge of Madness", "Zul'Gurub", 309, 148, 20),
    Boss(789, "High Priest Thekal", "Zul'Gurub", 309, 148, 20),
    Boss(790, "Gahz'ranka", "Zul'Gurub", 309, 148, 20),
    Boss(791, "High Priestess Arlokk", "Zul'Gurub", 309, 148, 20),
    Boss(792, "Jin'do the Hexxer", "Zul'Gurub", 309, 148, 20),
    Boss(793, "Hakkar", "Zul'Gurub", 309, 148, 20),

    # Onyxia"s Lair
    Boss(1084, "Onyxia", "Onyxia's Lair", 249, 9, 40),

    # Naxxramas
    # The Arachnid Quarter
    Boss(1107, "Anub'Rekhan", "Naxxramas", 533, 9, 40),
    Boss(1110, "Grand Widow Faerlina", "Naxxramas", 533, 9, 40),
    Boss(1116, "Maexxna", "Naxxramas", 533, 9, 40),
    # The Plague Quarter
    Boss(1117, "Noth the Plaguebringer", "Naxxramas", 533, 9, 40),
    Boss(1112, "Heigan the Unclean", "Naxxramas", 533, 9, 40),
    Boss(1115, "Loatheb", "Naxxramas", 533, 9, 40),
    # The Military Quarter
    Boss(1113, "Instructor Razuvious", "Naxxramas", 533, 9, 40),
    Boss(1109, "Gothik the Harvester", "Naxxramas", 533, 9, 40),
    Boss(1121, "The Four Horsemen", "Naxxramas", 533, 9, 40),
    # The Construct Quarter
    Boss(1118, "Patchwerk", "Naxxramas", 533, 9, 40),
    Boss(1111, "Grobbulus", "Naxxramas", 533, 9, 40),
    Boss(1108, "Gluth", "Naxxramas", 533, 9, 40),
    Boss(1120, "Thaddius", "Naxxramas", 533, 9, 40),
    # Frostwyrm Lair
    Boss(1119, "Sapphiron", "Naxxramas", 533, 9, 40),
    Boss(1114, "Kel'Thuzad", "Naxxramas", 533, 9, 40)
]