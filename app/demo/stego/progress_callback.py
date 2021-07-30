from math import floor


class ProgressCallback:

    def __init__(self):
        self.progress = 0
        self.max_value = 0
        self.current_value = 0

    def add_max_value(self, value):
        self.max_value += value
        self.update_progress()

    def add_current_value(self, value):
        self.current_value += value
        self.update_progress()

    def update_progress(self):
        try:
            self.progress = floor(self.current_value * 100 / self.max_value)
        except ZeroDivisionError:
            self.progress = 0

    def reset(self):
        self.progress = 0
        self.max_value = 0
        self.current_value = 0
