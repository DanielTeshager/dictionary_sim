class Dictionary:
    DK_INDICES = 7

    def __init__(self, dict_string=None) -> None:
        self.dict_string = dict_string
        self.keys = [None] * Dictionary.DK_INDICES
        self.values = [None] * Dictionary.DK_INDICES
        self.collisions = []

    def reset(self):
        self.keys = [None] * Dictionary.DK_INDICES
        self.values = [None] * Dictionary.DK_INDICES
        self.collisions = []

    def split_string(self):
        if self.dict_string:
            key_value_pairs = self.dict_string.split(",")
            for pair in key_value_pairs:
                key, value = pair.split(":")
                self.set_value(key.strip(), value.strip())

    def calculate_hash(self, key):
        return hash(key) % Dictionary.DK_INDICES

    def quadratic_probing(self, index, i):
        return (index + i * i) % Dictionary.DK_INDICES

    def find_slot(self, key):
        index = self.calculate_hash(key)
        i = 0
        while True:
            slot = self.quadratic_probing(index, i)
            if self.keys[slot] is None or self.keys[slot] == key:
                if i > 0:
                    self.collisions.append({'slot': index, 'newSlot': slot})
                return slot
            i += 1

    def get_value(self, key):
        slot = self.find_slot(key)
        if self.keys[slot] == key:
            return self.values[slot]
        return None

    def set_value(self, key, value):
        slot = self.find_slot(key)
        self.keys[slot] = key
        self.values[slot] = value

    def delete_value(self, key):
        try:
            slot = self.keys.index(key)
        except:
            return False
        self.keys[slot] = None
        self.values[slot] = None
        return True
