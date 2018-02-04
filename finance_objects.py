class Quote:
    def __init__(self):
        self.cross = ""
        self.date_time = 0
        self.bid = 0
        self.ask = 0

    def spread(self):
        return self.ask - self.bid

    def pip_value(self):
        pass


class PriceTimeBlock:
    def __init__(self):
        self.cross = ""
        self.price_high = 0
        self.price_low = 0
        self.price_open = 0
        self.price_close = 0
        self.time_frame = 0
        self.date_time = 0

    def update(self, q: Quote):
        pass
