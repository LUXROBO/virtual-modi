
class VirtualNetwork:

    def __init__(self):
        # network virtual_module cannot have left neighbor
        self.neighbors.pop("l")
