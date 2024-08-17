class GameSettings:
    _window_size = [600, 800]
    _field_size = [400, 600]
    _cell_size = 20
    _border_width = 20
    _fps = 5
    _name = 'Snake'

    @property
    def window_size(self):
        return self._window_size

    @property
    def name(self):
        return self._name

    @property
    def field_size(self):
        return self._field_size

    @property
    def cell_size(self):
        return self._cell_size

    @property
    def border_width(self):
        return self._border_width

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):
        if value > 0:
            self._fps = value
        else:
            raise ValueError("FPS must be a positive integer.")


class Colors:
    _frame_color = (0, 255, 204)
    _field_color = (0, 0, 0)
    _border_color = (255, 255, 255)
    _text_color = (255, 0, 0)

    @property
    def frame_color(self):
        return self._frame_color

    @property
    def text_color(self):
        return self._text_color

    @property
    def field_color(self):
        return self._field_color

    @property
    def border_color(self):
        return self._border_color
