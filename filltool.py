from PIL import ImageDraw, ImageColor
from core import AbstractToolProcessor
from core import AbstractToolModelview


class FillProcessor(AbstractToolProcessor):

    def stop(self, x, y):
        super(FillProcessor, self).stop(x, y)
        ImageDraw.floodfill(self.main_window.pil_image, xy=(x, y), value=ImageColor.getrgb(self.modelview.color))
        self.main_window.refresh()


class FillModelview(AbstractToolModelview):

    def __init__(self, main_window):
        super(FillModelview, self).__init__(main_window)

        # Color.
        self.enable_color()

        # Setup.
        self.toplevel.overrideredirect(True)
        self.toplevel.wm_title("Fill")
        self.toplevel.geometry("150x200+800+200")
        self.toplevel.resizable(width=False, height=False)
        self.toplevel.update()
