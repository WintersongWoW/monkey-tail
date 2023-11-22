import os
import re
from boss import boss_data

guidToAvailableHeal = {}

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


def process_dmg(log_entry):
    time_split = log_entry.split("  ")
    timestamp = time_split[0]
    rest = time_split[1].split(",")
    targetGUID = rest[5]

    if targetGUID.startswith("Creature"):
        return

    dmg1 = rest[28]
    dmg2 = rest[29]

    if rest[0] == "SWING_DAMAGE":
        dmg1 = rest[25]
        dmg2 = rest[26]

    dmg = int(dmg1)

    if dmg1 != dmg2:
        print("DEBUG: DMG DIFF", dmg1, dmg2, log_entry)

    guidToAvailableHeal[targetGUID] = guidToAvailableHeal.get(targetGUID, 0) + dmg

def process_heal(log_entry, writer):
    time_split = log_entry.split("  ")
    timestamp = time_split[0]
    rest = time_split[1].split(",")
    targetGUID = rest[5]

    if targetGUID.startswith("Creature"):
        return

    heal1 = rest[28]
    heal2 = rest[29]
    heal = int(heal1)

    if heal1 != heal2:
        print("DEBUG: HEAL DIFF", heal1, heal2, log_entry)

    available = guidToAvailableHeal.get(targetGUID, 0)
    guidToAvailableHeal[targetGUID] = max(0, available - heal)
    overheal = heal - available

    if overheal > 0:
        rest[30] = str(overheal)
        writer.write(time_split[0] + "  " + ",".join(rest))
    else:
        writer.write(log_entry)

def process_line(log_entry, writer):
    log_entry = fix_zone(log_entry)
    log_entry = update_realm(log_entry, "Everlook")

    fix_segmenting_start(log_entry, writer)

    if "SWING_DAMAGE" in log_entry or "SPELL_DAMAGE" in log_entry or "SPELL_PERIODIC_DAMAGE" in log_entry:
        process_dmg(log_entry)

    if "SPELL_HEAL" in log_entry or "SPELL_PERIODIC_HEAL" in log_entry:
        process_heal(log_entry, writer)
    else:
        writer.write(log_entry)

    fix_segmenting_end(log_entry, writer)


def fix_zone(log_entry):
    if "ZONE_CHANGE" in log_entry:
        log_entry = log_entry.replace(",9", ",1")
    return log_entry


def update_realm(log_entry, realmname):
    return log_entry.replace("-\"", "-" + realmname + "\"")


def write_segment_start(log_entry, boss, writer):
    # ENCOUNTER_START: encounterID, encounterName, difficultyID, groupSize
    #
    # encounterID: 672 (Boss id)
    # encounterName: Ragnaros (Boss name)
    # difficultyID: 9 (40 man raid), 148 (ZG, AQ20)
    # groupSize: 40 (raid size)
    writer.write(extract_timestamp(log_entry) + "  ENCOUNTER_START,"+str(boss.id)+",\"" + boss.name + "\","+str(boss.difficulty)+","+str(boss.group_size)+"\n")


def write_segment_end(log_entry, boss, writer):
    # ENCOUNTER_END: encounterID, encounterName, difficultyID, groupSize, success
    #
    # encounterID: 672 (Boss id)
    # encounterName: Ragnaros (Boss name)
    # difficultyID: 9 (40 man raid), 148 (ZG, AQ20)
    # groupSize: 40 (raid size)
    # success: 1 (kill), 0 (wipe)
    writer.write(extract_timestamp(log_entry) + "  ENCOUNTER_END,"+str(boss.id)+",\"" + boss.name + "\","+str(boss.difficulty)+","+str(boss.group_size)+",1\n")


def fix_segmenting_start(log_entry, writer):
    for boss in boss_data:
        triggers = boss.alternative_trigger.copy()
        triggers.append(boss.name)
        for trigger in triggers:
            if not boss.encounter_start_found and "\""+trigger+"\"" in log_entry:
                write_segment_start(log_entry, boss, writer)
                boss.encounter_start_found = True


def fix_segmenting_end(log_entry, writer):
    # 0xa18 — specific UnitFlag for Majordomo Executus's ends of encounter, the 1 indicates Majordomo turning friendly - see https://wowpedia.fandom.com/wiki/UnitFlag.
    for boss in boss_data:
        if not boss.encounter_end_found and ("UNIT_DIED" in log_entry or (boss.name == "Majordomo Executus" and "0xa18" in log_entry)) and "\""+boss.name+"\"" in log_entry:
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
input("Press enter to exit...")
exit()
