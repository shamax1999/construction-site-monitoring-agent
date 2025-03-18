import random
from typing import Optional

class Sensor:
    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val

    def read(self) -> Optional[float]:
        if random.random() < 0.05:
            return None
        return random.uniform(self.min_val, self.max_val)