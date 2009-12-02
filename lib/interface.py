import pygame
from data import *
from config import *
from constants import *

class Text(pygame.sprite.DirtySprite):
    """A sprite for text loaded from a font."""

    def __init__(self, font_name, font_size, font_color, font_text):
        pygame.sprite.DirtySprite.__init__(self)
        self.font = load_font(font_name, font_size)
        self.image = self.font.render(font_text, True, font_color)
        self.rect = self.image.get_rect()

    def update(self, rects):
        pygame.display.update(rects)

class TextBox(pygame.sprite.DirtySprite):
    """The moving text in the dialog window."""

    def __init__(self, dialog):
        pygame.sprite.DirtySprite.__init__(self)
        self.dialog = dialog
        self.text = Text("menu", 16, (224,224,224), None)
        self.font = self.text.font
        self.scroll_pos = 0
        self.image = pygame.Surface((DIALOG_SIZE[0], 50000), SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = [ WINDOW_SIZE[0]/2, 100 ]
        self.rect.top = WINDOW_SIZE[1] - DIALOG_SIZE[1] - 32
        self.draw()

    def draw(self):
        """Draw the dialog text."""

        text_all="b obgfiy yb jb j bjl bjl b jlb jl bjl bjlbjl bljbjl bljbljbjl bjlbjlbjlbj bjbkhlvkhgyi gfiyfg  bkh bkh bhk bhk bhk bhb hkb hk bhkbkb lkbl bljblj blj bjbljb jlbjlb jlb bj bj bj bjb jlb jbuobu bu bj bj bjl bj jlbjl bjl bj bjk b jkbkjbkj bkjbuobuobu obuobou buo uouob uo uboub uob ouboubou bouueefjnnb nbkb kh bb"
        words = text_all.rstrip().split(" ")
        line = ""
        num_lines = 0
        lines = []
        color = (224,224,224)
        for word in words:
            line = line + " " + word
            if line[0] == " ":
                line = line[1:]
            if self.font.size(line)[0] > DIALOG_MAX[0] - 8:
                line = line.rstrip(word)
                lines.append(self.font.render(line, 1, color))
                line = word
                num_lines = num_lines + 1
        if line != "":
            lines.append(self.font.render(line, 1, color))
            line = ""
            num_lines = num_lines + 1
        for num in range(num_lines):
            self.image.blit(lines[num],
                (20, num * self.font.get_height() + 10))


class Dialog(pygame.sprite.DirtySprite):
    """The dialog window used for story and character dialog."""

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(DIALOG_SIZE, SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = [ WINDOW_SIZE[0] / 2, 0 ]
        self.rect.bottom = WINDOW_SIZE[1] - 32
        self.toggle = False
        self.text = TextBox(self.image)
        self.images = [
            load_tile("interface", "window_n"),
            load_tile("interface", "window_ne"),
            load_tile("interface", "window_e"),
            load_tile("interface", "window_se"),
            load_tile("interface", "window_s"),
            load_tile("interface", "window_sw"),
            load_tile("interface", "window_w"),
            load_tile("interface", "window_nw"),
            load_tile("interface", "window_bg") ]
        self.draw_background()
        self.draw_frame()

    def draw_background(self):
        """ Draw the dialog window background."""

        for row in range(0, DIALOG_TILES[1] - 1):
            for tile in range(0, DIALOG_TILES[0]):
                offset = (tile * 16 + 8, row * 16 + 8)
                self.image.blit(self.images[8], offset)

    def draw_frame(self):
        """Draw a frame around the dialog window."""

        for row in (range(0, DIALOG_TILES[1] / 2 - 1)):
            for tile in range(0, DIALOG_TILES[0] / 2):
                offset = (tile * 32 + 16, row * 32 + 16)
                self.image.blit(self.images[0], (offset[0], 0))
                self.image.blit(self.images[4], (offset[0], DIALOG_MAX[1]))
                self.image.blit(self.images[2], (DIALOG_MAX[0], offset[1]))
                self.image.blit(self.images[6], (0, offset[1]))
        self.image.blit(self.images[1], (DIALOG_MAX[0], 0))
        self.image.blit(self.images[3], (DIALOG_MAX[0], DIALOG_MAX[1]))
        self.image.blit(self.images[5], (0, DIALOG_MAX[1]))
        self.image.blit(self.images[7], (0, 0))

    def scroll(self, dir):
        """Scroll the dialog text."""

        self.dirty = 1
        height = self.text.font.get_height()
        if dir == "up":
            self.text.rect.move_ip([0, height])
        elif dir =="down":
            self.text.rect.move_ip([0, -height])
