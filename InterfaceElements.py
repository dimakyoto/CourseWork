import pygame


class Button:
    def __init__(self, horizontal: float, vertical: float, width: float, height: float,
                 text: str, textcolor: tuple, button_color: tuple,
                 screen: pygame, font: pygame):
        self.__horizontal = horizontal
        self.__vertical = vertical
        self.__width = width
        self.__height = height
        self.__text = text
        self.__screen = screen
        self.__font = font
        self.__textcolor = textcolor
        self.__button_color = button_color

        self.rect = pygame.Rect(self.__horizontal, self.__vertical, self.__width, self.__height)

    def __call__(self):
        button_text = self.__font.render(self.__text, True, self.__textcolor)
        button_rect = button_text.get_rect()
        button_rect.center = self.rect.center
        pygame.draw.rect(self.__screen, self.__button_color, self.rect)
        self.__screen.blit(button_text, button_rect)

    def color_change(self, color: tuple):
        self.__button_color = color


class TextField:
    def __init__(self, x: int, y: int, width: int, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = ""

        self.__font_size = 18
        self.__font_color = (0, 0, 0)
        self.__background_color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.__background_color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("timesnewroman", self.__font_size)
        text_surface = font.render(self.text, True, self.__font_color)
        screen.blit(text_surface, (self.x, self.y))

    def set_text(self, text):
        self.text = text
