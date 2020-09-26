class Step(object):
    def __init__(self, mode, delay, *index):
        self.mode = mode
        self.delay = delay
        self.params = index
