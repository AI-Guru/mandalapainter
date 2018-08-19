from PIL import ImageDraw
from core import AbstractToolProcessor
from core import AbstractToolModel

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
            draw.line((x1, y1, x2, y2), fill=self.main_window.color, width=self.main_window.line_width)
        del draw
