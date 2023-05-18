import pygame


def type_check(name, correct_type):
    """
    1. call type_check first，return prop setter，and convert name to private attribute. Store private_name  & correct_type information.
    2. class initializing attribute
    3. When initailize name attribute，it'll call prop and check type of input. If type is wrong, raise error; or set attribute by setattr function.
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
    _left: ліва межа кнопки (ціле число)
    _top: верхня межа кнопки (ціле число)
    _width: ширина кнопки (ціле число)
    _height: висота кнопки (ціле число)
    _text: текст кнопки (рядок)
    _textcolor: колір тексту (кортеж, наприклад: (0, 0, 0))
    _rectcolor: колір кнопки (кортеж, наприклад: (255, 255, 255))
    _screen: об'єкт pygame "pygame.display.set_mode()"
    _font: шрифт тексту
    """

    # Зайвих атрибутів не повинно бути
    __slots__ = ["_left", "_top", "_width", "_height","_text", "_textcolor", "_rectcolor","_screen", "_font", "rect"]

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


class ShowText:
    """
    _center: центр позиціонування тексту (кортеж)
    _text: список текстів для відображення (список)
    _textcolor: колір тексту (кортеж)
    _screen: об'єкт pygame "pygame.display.set_mode()"
    _font: шрифт тексту
    """

    # Додаткові атрибути не дозволені
    __slots__ = ["_center", "_text", "_textcolor","_screen", "_font"]

    text = type_check("text", list)
    center = type_check("center", tuple)
    textcolor = type_check("textcolor", tuple)

    def __init__(self, center: tuple, text: list, textcolor: tuple, screen: pygame, font: pygame):
        self._screen = screen
        self._font = font
        self.center = center
        self.text = text
        self.textcolor = textcolor

    def __call__(self):
        for text in self._text:
            showtext = self._font.render(text, True, self._textcolor)
            textrect = showtext.get_rect()
            textrect.center = self._center
            self._screen.blit(showtext, textrect)