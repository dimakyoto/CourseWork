import pygame

def type_check(name, correct_type):
    """
    1. call type_check first，return prop setter，and convert name to private attribute. Store private_name
    & correct_type information.
    2. class initializing attribute
    3. When initialize name attribute，it'll call prop and check type of input. If type is wrong, raise error;
    or set attribute by setattr function.
    """
    private_name = '_' + name

    @property
    def prop(self):
        return getattr(self, private_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, correct_type):
            raise ValueError("{} must be a {}".format(private_name, correct_type))
        setattr(self, private_name, value)

    return prop

class RectButton:

    """
    _left: left boundary of the button (integer)
    _top: top boundary of the button (integer)
    _width: width of the button (integer)
    _height: height of the button (integer)
    _text: button text (string)
    _textcolor: text color (tuple, e.g., (0, 0, 0))
    _rect_color: button color (tuple, e.g., (255, 255, 255))
    _screen: pygame screen object "pygame.display.set_mode()"
    _font: text font
    """

    textcolor = type_check("textcolor", tuple)
    rectcolor = type_check("rectcolor", tuple)

    def __init__(self, left: int, top: int, width: int, height: int,
                 text: str, textcolor: tuple, rectcolor: tuple,
                 screen: pygame, font: pygame):
        self._left = left
        self._top = top
        self._width = width
        self._height = height
        self._text = text
        self._screen = screen
        self._font = font
        self.rect = pygame.Rect(self._left, self._top, self._width, self._height)
        self.textcolor = textcolor
        self.rectcolor = rectcolor


    def __call__(self):
        button_text = self._font.render(self._text, True, self._textcolor)
        button_rect = button_text.get_rect()
        button_rect.center = self.rect.center
        pygame.draw.rect(self._screen, self._rectcolor, self.rect)
        self._screen.blit(button_text, button_rect)

    def color_change(self, color: tuple):
        self.rectcolor = color

class TextField:

    text = type_check("text", str)
    x = type_check("x", int)
    y = type_check("y", int)
    width = type_check("width", int)
    height = type_check("height", int)
    font_size = type_check("font_size", int)
    font_color = type_check("font_color", tuple)
    background_color = type_check("background_color", tuple)

    def __init__(self, x, y, width, height, font_size=24, font_color=(0, 0, 0), background_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font_color = font_color
        self.background_color = background_color
        self.text = ""
        self.active = False

    def get_info(self):
        return {
            'text': self.text,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'font_size': self.font_size,
            'font_color': self.font_color,
            'background_color': self.background_color
        }

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.font_color)
        screen.blit(text_surface, (self.x, self.y))

    def set_text(self, text):
        self.text = text
