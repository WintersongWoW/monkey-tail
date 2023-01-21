class Boss:
    def __init__(self, id, name, location, zone_id):
        self.id = id
        self.name = name
        self.location = location
        self.zone_id = zone_id
        self.encounter_start_found = False
        self.encounter_end_found = False
