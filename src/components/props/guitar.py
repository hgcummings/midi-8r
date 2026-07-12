class Guitar:
    """
    Parameter for selecting the guitar (and pickup) used with this patch

    Raises an alert on load if the guitar or pickup has changed:
    - If the guitar changed, shows the guitar name first (footswitch to acknowledge),
      then the pickup selection (footswitch to clear), unless there is only one pickup
    - If only the pickup changed, shows the pickup selection directly (footswitch to clear)

    Two-step editing via advance(): first selects the guitar, then the pickup.
    """
    format = "BB"

    def __init__(self, guitars):
        self.guitars = guitars
        self.default = (1, guitars[1]["default"])
        self.last_acknowledged = self.default
        self.alert = False
        self._guitar_alert = False
        self.pickup_image = Guitar.PickupImage(guitars)

    def load(self, data):
        self.guitar = data[0]
        if self.guitar == 0:
            (self.guitar, self.pickup) = self.default
        else:
            self.pickup = data[1]
        self.saved = (self.guitar, self.pickup)
        self.edit_pickup = False
        if (self.saved != self.last_acknowledged):
            self._set_alert()
        elif (self.alert):
            self.clear_alert()

    def _set_alert(self):
        self.alert = True
        self._guitar_alert = self.last_acknowledged[0] != self.guitar

    def clear_alert(self):
        if self._guitar_alert:
            self._guitar_alert = False
            if len(self.__pickups()) > 1:
                return  # stay in alert mode to show pickup next
        self.alert = False
        self.last_acknowledged = (self.guitar, self.pickup)

    def value_range(self):
        if self.edit_pickup:
            return (0, self.pickup, len(self.__pickups()) - 1)
        else:
            return (1, self.guitar, len(self.guitars) - 1)

    def update_value(self, value):
        if self.edit_pickup:
            self.pickup = value
        else:
            self.guitar = value
            self.pickup = self.guitars[self.guitar]["default"]

    def switch(self):
        pass

    def advance(self):
        if self.edit_pickup or len(self.__pickups()) == 1:
            self.edit_pickup = False
            return False
        else:
            self.edit_pickup = True
            return True

    def has_changed(self):
        return self.saved != (self.guitar, self.pickup)

    def render(self, display, colour=(255,255,255)):
        if self.alert and self._guitar_alert:
            display.show_text(self.guitars[self.guitar]["name"])
        elif self.alert:
            self.__show_pickup(display)
        elif self.edit_pickup:
            self.__show_pickup(display, colour=colour)
        else:
            display.show_text(self.guitars[self.guitar]["name"], colour=colour)

    def save(self):
        self.saved = (self.guitar, self.pickup)
        self.last_acknowledged = self.saved
        return self.saved

    def __guitar(self):
        return self.guitars[self.guitar]

    def __pickups(self):
        return self.__guitar()["pickups"]

    def __show_pickup(self, display, colour=(255,255,255)):
        self.pickup_image.set(self.guitar, self.pickup, colour)
        display.show_image(
            self.pickup_image.width(),
            self.pickup_image.height(),
            self.pickup_image)

    class PickupImage:
        _bg_col = (0,0,0)

        def __init__(self, guitars):
            self._row_buf = [self._bg_col] * (max(map(self._guitar_width, guitars[1:])) + 1)
            self._guitars = guitars
            self._guitar = 0
            self._pickup = 0

        def _guitar_width(self, guitar):
            return guitar["pickups"][-1][-1] + 1

        def width(self):
            return self._guitar_width(self._guitar)

        def height(self):
            return self._guitar["strings"]

        def set(self, guitar_index, pickup_index, colour):
            self._guitar = self._guitars[guitar_index]
            self._pickup = self._guitar["pickups"][pickup_index]

            unselected_colour = (colour[0] // 4, colour[1] // 4, colour[2] // 8)

            for x in range(self.width()):
                self._row_buf[x] = self._bg_col

            for pu in self._guitar["pickups"]:
                for x in pu:
                    self._row_buf[x] = colour if x in self._pickup else unselected_colour

        def __getitem__(self, _):
            return self._row_buf
