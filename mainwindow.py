import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageChops, ImageEnhance, ImageColor, ImageOps

from toolswindow import *
from drawtool import *
from brushtool import *
from filltool import *


class MainWindow(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # TODO set title

        column = 0

        # Save button.
        self.save_button = tk.Button(self, text="Save", command=self.save_button_clicked)
        self.save_button.grid(row=0, column=column)
        column += 1

        # Undo button.
        self.undo_button = tk.Button(self, text="Undo", command=self.undo_button_clicked)
        self.undo_button.grid(row=0, column=column)
        column += 1

        # Selecting the number of segments.
        self.label = tk.Label(self, text="Segments:")
        self.label.grid(row=0, column=column)
        column += 1
        self.segments_spinbox = tk.Spinbox(self, width=3, from_=4, to=100, command=self.segments_spinbox_changed)
        self.segments_spinbox.grid(row=0, column=column)
        self.segments_spinbox.delete(0,"end")
        self.segments_spinbox.insert(0, 32)
        column += 1

        # Mirror button.
        self.mirror_checkbutton_var = tk.IntVar()
        self.mirror_checkbutton = tk.Checkbutton(self, text="Mirror", variable=self.mirror_checkbutton_var, command=self.mirror_checkbutton_changed)
        self.mirror_checkbutton.grid(row=0, column=column)

        # Some parameters.
        self.width = 700
        self.height = 700
        self.center_x = self.width // 2
        self.center_y = self.height // 2

        # For undo/redo.
        self.undo_cache = []

        # Create the canvas.
        self.canvas = tk.Canvas(self, bg="black", width=self.width, height=self.height)
        self.canvas.grid(row=1, columnspan=column)
        self.canvas.bind("<Button-1>", self.start_tool)
        self.canvas.bind("<B1-Motion>", self.move_tool)
        self.canvas.bind("<ButtonRelease-1>", self.stop_tool)

        # Create a PIL image.
        self.pil_image = Image.new("RGB", (self.width, self.height))
        self.photo_image = None
        self.image_sprite = None
        self.refresh()

        self.current_tool = None
        self.current_tool_processor = None
        self.current_tool_modelview = None

        # Set up modelviews for tools.
        self.tool_modelviews = {}
        self.tool_modelviews["draw"] = DrawModelview(self)
        self.tool_modelviews["brush"] = BrushModelview(self)
        self.tool_modelviews["fill"] = FillModelview(self)

        # Set up processors for tools.
        self.tool_processors = {}
        self.tool_processors["draw"] = DrawProcessor(self)
        self.tool_processors["brush"] = BrushProcessor(self)
        self.tool_processors["fill"] = FillProcessor(self)

        # Connect.
        for key in self.tool_modelviews.keys():
            self.tool_processors[key].modelview = self.tool_modelviews[key]
            self.tool_modelviews[key].hide()

        # Create tools-window.
        self.tools_window = ToolsWindow(self)

        # Update UI.
        self.segments_spinbox_changed()
        self.mirror_checkbutton_changed()


    def save_button_clicked(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if file is None:
            return
        self.pil_image.save(file.name)


    def undo_button_clicked(self):
        self.undo()


    def segments_spinbox_changed(self):
        self.segments = int(self.segments_spinbox.get())


    def mirror_checkbutton_changed(self):
        self.mirror = self.mirror_checkbutton_var.get() == 1


    def notify_tool_change(self, new_tool):

        if self.current_tool_modelview:
            self.current_tool_modelview.hide()

        self.current_tool = new_tool
        self.current_tool_processor = self.tool_processors[new_tool]
        self.current_tool_modelview = self.tool_modelviews[new_tool]
        self.current_tool_modelview.show()


    def start_tool(self, event):
        self.cache_undo()
        self.current_tool_processor.start(event.x, event.y)


    def move_tool(self, event):
        self.current_tool_processor.move(event.x, event.y)


    def stop_tool(self, event):
        self.current_tool_processor.stop(event.x, event.y)


    def cache_undo(self):
        self.undo_cache.append(self.pil_image.copy())
        if len(self.undo_cache) > 64:
            self.undo_cache.pop(0)


    def undo(self):
        if len(self.undo_cache) != 0:
            cached_pil_image = self.undo_cache.pop()
            self.pil_image = cached_pil_image
            self.refresh()


    def redo(self):
        pass


    def refresh(self):
        if self.image_sprite != None:
            del self.image_sprite
        if self.photo_image != None:
            del self.photo_image
        self.photo_image = ImageTk.PhotoImage(self.pil_image)
        self.image_sprite = self.canvas.create_image(self.center_x + 3, self.center_y + 3, image=self.photo_image)


if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
