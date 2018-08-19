import tkinter as tk
from PIL import ImageDraw

from core import AbstractToolProcessor
from core import AbstractToolModelview

class DrawProcessor(AbstractToolProcessor):

    def move(self, x, y):
        super(DrawProcessor, self).move(x, y)

        self.draw_line(self.old_x, self.old_y, x, y)
        self.main_window.refresh()

        self.old_x = x
        self.old_y = y

    def draw_line(self, x1, y1, x2, y2):

        #if self.blur != 0:
        #    blurredImage = self.pilImage.filter(ImageFilter.BLUR)
        #    self.pilImage = Image.blend(self.pilImage, blurredImage, alpha=self.blur / 10.0)

        # Compute and draw the lines.
        draw = ImageDraw.Draw(self.main_window.pil_image)
        start_points = self.get_mandala_points(x1, y1)
        end_points = self.get_mandala_points(x2, y2)
        for (x1, y1), (x2, y2) in zip(start_points, end_points):
            draw.line((x1, y1, x2, y2), fill=self.modelview.color, width=self.modelview.size)
        del draw


class DrawModelview(AbstractToolModelview):

    def __init__(self, main_window):
        super(DrawModelview, self).__init__(main_window)

        self.enable_color()
        self.enable_size()

        self.toplevel.overrideredirect(True)
        self.toplevel.wm_title("Draw")
        self.toplevel.geometry("75x150+800+200")
        self.toplevel.resizable(width=False, height=False)
        self.toplevel.update()
