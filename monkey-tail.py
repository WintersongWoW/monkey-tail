import os
import re
from boss import boss_data
from tkinter import Tk 
from tkinter.filedialog import askopenfilename

guidToAvailableHeal = {}
trigger_count = 0
triggered_triggers = set()  # Keep track of triggered triggers for the current boss to check for wipes on encounters with multiple bosses.

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
    global trigger_count
    global triggered_triggers
    for boss in boss_data:
        triggers = boss.alternative_trigger.copy()
        if not boss.name in ['Silithid Royalty', 'Twin Emperors', 'The Four Horsemen']:
            triggers.append(boss.name)

        if boss.name in ['Silithid Royalty', 'Twin Emperors', 'The Four Horsemen']:
            for trigger in triggers:
                if not boss.encounter_end_found and ("UNIT_DIED" in log_entry) and "\""+trigger+"\"" in log_entry:
                    if trigger in triggered_triggers:
                        trigger_count = 0  # Reset trigger_count if the trigger has already been triggered
                        triggered_triggers = set()
                        triggered_triggers.add(trigger)
                        trigger_count += 1
                    else:
                        triggered_triggers.add(trigger)
                        trigger_count += 1

                    if trigger_count == len(triggers):
                        if not boss.encounter_end_found and "UNIT_DIED" in log_entry:
                            write_segment_end(log_entry, boss, writer)
                            boss.encounter_end_found = True
                            trigger_count = 0
        else:
            # 0xa18 — specific UnitFlag for Majordomo Executus's ends of encounter, the 1 indicates Majordomo turning friendly - see https://wowpedia.fandom.com/wiki/UnitFlag.
            for trigger in triggers:
                if not boss.encounter_end_found and ("UNIT_DIED" in log_entry or (boss.name == "Majordomo Executus" and "0xa18" in log_entry)) and "\""+trigger+"\"" in log_entry:
                    if not trigger == "Eye of C'Thun":
                        write_segment_end(log_entry, boss, writer)
                        boss.encounter_end_found = True


def monkey_print(string):
    print("(^.^)@ |", string)

Tk().withdraw()
input_filename = askopenfilename(filetypes=[('Text files', '.txt')], title='Select the log file')
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
