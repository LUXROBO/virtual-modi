
from virtual_modi.virtual_module.virtual_module import VirtualModule


class VirtualButton(VirtualModule):

    CLICKED = 2
    DOUBLE_CLICKED = 3
    PRESSED = 4
    TOGGLED = 5

    def __init__(self):
        self.is_toggled = False

    def click(self):
        self.is_toggled = not self.is_toggled
        self.send_property_message(self.CLICKED, 100)

    def double_click(self):
        self.send_property_message(self.DOUBLE_CLICKED, 100)

    def press(self):
        self.send_property_message(self.PRESSED, 100)

    def run(self):
        # Health Information
        self.send_health_message()

        # Property Information
        self.send_property_message(self.CLICKED, 0)
        self.send_property_message(self.DOUBLE_CLICKED, 0)
        self.send_property_message(self.PRESSED, 0)
        toggled_value = 100 if self.is_toggled else 0
        self.send_property_message(self.TOGGLED, toggled_value)

