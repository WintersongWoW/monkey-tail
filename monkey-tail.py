import os
from boss import Boss
import re


def extract_timestamp(log_entry):
    """
    Use regular expression to search for timestamp in the format of "MM/DD HH:MM:SS.sss"
    """
    match = re.search(r'^(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})', log_entry)
    if match:
        return match.group(1)
    return None


def print_progress(input_filename, output_filename):
    """
    This function prints the percentage of completion of the processing of the input file based on the output file size
    Currently goes over 100% done as new file size is bigger. Whajooo.
    """
    monkey_print(f'{os.path.getsize(output_filename) / os.path.getsize(input_filename) * 100 :.2f}% complete')


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


def write_segment_start(log_entry, boss, writer):
    writer.write(extract_timestamp(log_entry) + "  ENCOUNTER_START,"+str(boss.id)+",\"" + boss.name + "\",9,40,409\n")


def write_segment_end(log_entry, boss, writer):
    writer.write(extract_timestamp(log_entry) + "  ENCOUNTER_END,"+str(boss.id)+",\"" + boss.name + "\",9,40,1\n")


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
    txt_files = [f for f in os.listdir() if (f.endswith('.txt') and not f.endswith('.monkey-tail.txt'))]

    # Print the list of .txt files and ask the user to select one
    monkey_print('Found the following logs')
    for i, txt_file in enumerate(txt_files):
        print(f'{i+1}. {txt_file}')

    selected_file = input('Please select a file by entering its number: ')

    # Get and return the selected file name
    return txt_files[int(selected_file) - 1]


def monkey_print(string):
    print('(^.^)@ |', string)


# Molten Core boss data
boss_data = [
    # Lucifron
    Boss(663, 'Lucifron', 'Molten Core', 9),
    # Magmadar
    Boss(664, 'Magmadar', 'Molten Core', 9),
    # Gehennas
    Boss(665, 'Gehennas', 'Molten Core', 9),
    # Garr
    Boss(666, 'Garr', 'Molten Core', 9),
    # Shazzrah
    Boss(667, 'Shazzrah', 'Molten Core', 9),
    # Baron Geddon
    Boss(668, 'Baron Geddon', 'Molten Core', 9),
    # Sulfuron Harbinger
    Boss(669, 'Sulfuron Harbinger', 'Molten Core', 9),
    # Golemagg the Incinerator
    Boss(670, 'Golemagg the Incinerator', 'Molten Core', 9),
    # Majordomo Executus
    Boss(671, 'Majordomo Executus', 'Molten Core', 9),
    # Ragnaros
    Boss(672, 'Ragnaros', 'Molten Core', 9)
]

input_filename = select_inputfile()
output_filename = input_filename.replace('.txt', '.monkey-tail.txt')

with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
    for i, line in enumerate(input_file, 1):
        # process the line
        process_line(line, output_file)
        # Print progress every 1000 lines
        if i % 50000 == 0:
            print_progress(input_filename, output_filename)
monkey_print('Processing complete, wrote new logfile to ' + output_filename)
monkey_print('Now upload it so the other monkeys can look at them.')
input('Press any key to exit...')
