import tkinter as tk
from PIL import Image, ImageChops

from core import AbstractToolProcessor
from core import AbstractToolModelview
import glob
import os
from matplotlib import cm


class BrushProcessor(AbstractToolProcessor):

    def __init__(self, main_window):
        super(BrushProcessor, self).__init__(main_window)

        self.colormap_lookup = {}
        self.colormap_lookup["Plasma"] = cm.plasma
        self.colormap_lookup["Plasma R"] = cm.plasma_r
        self.colormap_lookup["Inferno"] = cm.inferno
        self.colormap_lookup["Inferno R"] = cm.inferno_r
        self.colormap_lookup["Magma"] = cm.magma
        self.colormap_lookup["Magma R"] = cm.magma_r
        self.colormap_lookup["Viridis"] = cm.viridis
        self.colormap_lookup["Viridis R"] = cm.viridis_r


    def move(self, x, y):
        super(BrushProcessor, self).move(x, y)

        self.old_x = x
        self.old_y = y

        width = self.modelview.size
        color = self.modelview.color

        # Handle shrinking.
        factor = 1.0
        if self.modelview.shrink == True:

            shrink_min = 25.0
            shrink_max = 200.0
            shrink_length = shrink_min * self.modelview.shrink_ratio + shrink_max * (1.0 - self.modelview.shrink_ratio)
            factor = 1.0 - min(1.0, self.overall_moved_distance / shrink_length)
            width = int(max(0.0, factor * width))

        # Handle gradients.
        if self.modelview.current_mode != "Color":
            color_index = 255 - int(factor * 255)
            colormap = self.colormap_lookup[self.modelview.current_mode]
            color = colormap(color_index)
            color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

        # Nothing to do.
        if width == 0:
            return

        # Render brush.
        color_image = Image.new("RGBA", size=(2 * width, 2 * width), color=color)
        image = self.modelview.current_brush_image.resize((2 * width, 2 * width), Image.ANTIALIAS)
        image = ImageChops.multiply(image, color_image)

        overall_image = Image.new("RGBA", size=(self.main_window.width, self.main_window.height), color="black")
        points = self.get_mandala_points(x, y)
        for (x, y) in points:
            x = int(x)
            y = int(y)
            self.main_window.pil_image.paste(image, (x - width, y - width), image)

        self.main_window.refresh()



class BrushModelview(AbstractToolModelview):

    def __init__(self, main_window):
        super(BrushModelview, self).__init__(main_window)

        # Color.
        self.enable_color()

        # Size.
        self.enable_size()
        self.set_size(10)

        # Setup.
        self.toplevel.overrideredirect(True)
        self.toplevel.wm_title("Draw")
        self.toplevel.geometry("150x200+800+200")
        self.toplevel.resizable(width=False, height=False)
        self.toplevel.update()

        # Color modes.
        modes = ["Color", "Plasma", "Plasma R", "Inferno", "Inferno R", "Magma", "Magma R", "Viridis", "Viridis R"]
        modes_variable = tk.StringVar(self.toplevel)
        modes_variable.set(modes[0])
        self.mode_option_menu = tk.OptionMenu(self.toplevel, modes_variable, *modes, command=self.mode_option_menu_changed)
        self.mode_option_menu.grid(row=self.row, column=0)
        self.mode_option_menu_changed(modes[0])
        self.row += 1

        # Brushes.
        brush_paths = glob.glob(os.path.join("resources", "brushes", "*.png"))
        brush_names = [os.path.basename(brush_path).replace(".png", "") for brush_path in brush_paths]
        self.brush_dictionary = {}
        for (brush_name, brush_path) in zip(brush_names, brush_paths):
            self.brush_dictionary[brush_name] = Image.open(brush_path, "r")
        brushes_variable = tk.StringVar(self.toplevel)
        brushes_variable.set(brush_names[0])
        self.brush_option_menu = tk.OptionMenu(self.toplevel, brushes_variable, *brush_names, command=self.brush_option_menu_changed)
        self.brush_option_menu.grid(row=self.row, column=0)
        self.brush_option_menu_changed(brush_names[0])
        self.row += 1

        # Mirror button.
        self.shrink_checkbutton_var = tk.IntVar()
        self.shrink_checkbutton_var.set(0)
        self.shrink_checkbutton = tk.Checkbutton(self.toplevel, text="Shrink", variable=self.shrink_checkbutton_var, command=self.shrink_checkbutton_changed)
        self.shrink_checkbutton.grid(row=self.row, column=0)
        self.row += 1

        # Shrink spinbox.
        self.shrink_spinbox = tk.Spinbox(self.toplevel, width=3, from_=1, to=100, command=self.shrink_spinbox_changed)
        self.shrink_spinbox.delete(0,"end")
        self.shrink_spinbox.insert(0, 100)
        self.shrink_spinbox.grid(row=self.row, column=0)
        self.row += 1

        self.shrink_spinbox_changed()
        self.shrink_checkbutton_changed()


    def mode_option_menu_changed(self, value):
        self.current_mode = value


    def brush_option_menu_changed(self, value):
        self.current_brush_image = self.brush_dictionary[value]


    def shrink_checkbutton_changed(self):
        self.shrink = self.shrink_checkbutton_var.get() == 1

    def shrink_spinbox_changed(self):
        self.shrink_ratio = int(self.shrink_spinbox.get()) / 100.0
