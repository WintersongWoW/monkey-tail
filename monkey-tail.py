import os
from boss import Boss
import re


def extract_timestamp(log_entry):
    """
    Use regular expression to search for timestamp in the format of "MM/DD HH:MM:SS.sss"
    """
    match = re.search(r"^(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})", log_entry)
    if match:
        return match.group(1)
    return None


def print_progress(input_filename, output_filename):
    """
    This function prints the percentage of completion of the processing of the input file based on the output file size
    Currently goes over 100% done as new file size is bigger. Whajooo.
    """
    monkey_print(f"{os.path.getsize(output_filename) / os.path.getsize(input_filename) * 100 :.2f}% complete")


def process_line(log_entry, writer):
    log_entry = fix_zone(log_entry)
    log_entry = update_realm(log_entry, "Everlook")

    fix_segmenting_start(log_entry, writer)
    writer.write(log_entry)
    fix_segmenting_end(log_entry, writer)


def fix_zone(log_entry):
    if "ZONE_CHANGE" in log_entry:
        log_entry = log_entry.replace(",9", ",1")
    return log_entry


def update_realm(log_entry, realmname):
    return log_entry.replace("-\"", "-" + realmname + "\"")


# ENCOUNTER_START: encounterID, encounterName, difficultyID, groupSize
#
# encounterID: 672 (Boss id)
# encounterName: Ragnaros (Boss name)
# difficultyID: 9 (40 man raid), 148 (ZG, AQ20)
# groupSize: 40 (raid size)

def write_segment_start(log_entry, boss, writer):
    writer.write(extract_timestamp(log_entry) + "  ENCOUNTER_START,"+str(boss.id)+",\"" + boss.name + "\","+str(boss.difficulty)+","+str(boss.group_size)+"\n")


# ENCOUNTER_END: encounterID, encounterName, difficultyID, groupSize, success
#
# encounterID: 672 (Boss id)
# encounterName: Ragnaros (Boss name)
# difficultyID: 9 (40 man raid), 148 (ZG, AQ20)
# groupSize: 40 (raid size)
# success: 1 (kill), 0 (wipe)

def write_segment_end(log_entry, boss, writer):
    writer.write(extract_timestamp(log_entry) + "  ENCOUNTER_END,"+str(boss.id)+",\"" + boss.name + "\","+str(boss.difficulty)+","+str(boss.group_size)+",1\n")


def fix_segmenting_start(log_entry, writer):
    for boss in boss_data:
        if not boss.encounter_start_found and "\""+boss.name+"\"" in log_entry:
            write_segment_start(log_entry, boss, writer)
            boss.encounter_start_found = True


def fix_segmenting_end(log_entry, writer):
    for boss in boss_data:
        if not boss.encounter_end_found and "UNIT_DIED" in log_entry and "\""+boss.name+"\"" in log_entry:
            write_segment_end(log_entry, boss, writer)
            boss.encounter_end_found = True


def select_inputfile():
    # Get a list of all .txt files in the current directory that have not been processed yet
    txt_files = [f for f in os.listdir() if (f.endswith(".txt") and not f.endswith(".monkey-tail.txt"))]

    # Print the list of .txt files and ask the user to select one
    monkey_print("Found the following logs")
    for i, txt_file in enumerate(txt_files):
        print(f"{i+1}. {txt_file}")

    selected_file = input("Please select a file by entering its number: ")

    # Get and return the selected file name
    return txt_files[int(selected_file) - 1]


def monkey_print(string):
    print("(^.^)@ |", string)


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


input_filename = select_inputfile()
output_filename = input_filename.replace(".txt", ".monkey-tail.txt")

with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
    for i, line in enumerate(input_file, 1):
        # process the line
        process_line(line, output_file)
        # Print progress every 1000 lines
        if i % 50000 == 0:
            print_progress(input_filename, output_filename)
monkey_print("Processing complete, wrote new logfile to " + output_filename)
monkey_print("Now upload it so the other monkeys can look at them.")
input("Press any key to exit...")
