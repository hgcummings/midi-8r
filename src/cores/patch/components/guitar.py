import json

with open(__file__.replace("guitar.py", "guitars.json"), encoding="utf8") as f:
    guitars = json.load(f)

class Guitar:
    format = "BB"
    default = (1, guitars[1]["default"])

    def __init__(self, *_):
        self.last_acknowledged = self.default
        self.alert = False
        self.pickup_image = PickupImage(guitars)

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

    def save(self):
        return (self.index,)

    def show_view(self, display):
        if (len(self.__pickups()) == 1 or (self.alert and self.last_acknowledged[0] != self.guitar)):
            display.show_text(guitars[self.guitar]["name"])
        else:
            self.__show_pickup(display)

    def __guitar(self):
        return guitars[self.guitar]

    def __pickups(self):
        return self.__guitar()["pickups"]

    def _set_alert(self):
        self.alert = True

    def clear_alert(self):
        self.alert = False
        self.last_acknowledged = (self.guitar, self.pickup)

    def edit(self, display):
        self.__show_edit(display)
        return (0, self.pickup, len(self.__pickups()) - 1) if self.edit_pickup else (1, self.guitar, len(guitars) - 1)

    def update_value(self, value, display):
        if (self.edit_pickup):
            self.pickup = value
        else:
            self.guitar = value
            self.pickup = guitars[self.guitar]["default"]
        self.__show_edit(display)

    def switch(self, *_):
        pass

    def next(self):
        if self.edit_pickup or len(self.__pickups()) == 1:
            return None
        else:
            self.edit_pickup = True
            return self

    def save(self):
        self.saved = (self.guitar, self.pickup)
        self.last_acknowledged = self.saved
        return self.saved

    def __show_edit(self, display):
        colour = (32,255,32) if self.saved == (self.guitar, self.pickup) else (127,0,0)
        if self.edit_pickup:
            self.__show_pickup(display, colour=colour)
        else:
            display.show_text(guitars[self.guitar]["name"],colour=colour)

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
