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
