import tkinter as tk
from tkinter.colorchooser import askcolor
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
        self.save_button = tk.Button(self, text="Save", command=self.click)
        self.save_button.grid(row=0, column=column)
        column += 1

        # Undo button.
        self.undo_button = tk.Button(self, text="Undo", command=self.click)
        self.undo_button.grid(row=0, column=column)
        column += 1

        # Color.
        self.color_button = tk.Button(self, text='Color', command=self.color_button_clicked)
        self.color_button.grid(row=0, column=column)
        column += 1

        # Selecting the number of segments.
        self.label = tk.Label(self, text="Segments:")
        self.label.grid(row=0, column=column)
        column += 1
        self.segments_spinbox = tk.Spinbox(self, width=3, from_=4, to=100, command=self.segments_spinbox_changed)
        self.segments_spinbox.grid(row=0, column=column)
        self.segments_spinbox.delete(0,"end")
        self.segments_spinbox.insert(0 ,32)
        column += 1

        # Mirror button.
        self.mirror_checkbutton_var = tk.IntVar()
        self.mirror_checkbutton = tk.Checkbutton(self, text="Mirror", variable=self.mirror_checkbutton_var, command=self.mirror_checkbutton_changed)
        self.mirror_checkbutton.grid(row=0, column=column)

        self.width = 800
        self.height = 800
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        #self.segments = 32
        #self.mirror = True
        self.color = "white"
        self.line_width = 20

        # Create the canvas.
        self.canvas = tk.Canvas(self, bg="red", width=self.width, height=self.height)
        self.canvas.grid(row=1, columnspan=column)
        self.canvas.bind("<Button-1>", self.start_tool)
        self.canvas.bind("<B1-Motion>", self.move_tool)
        self.canvas.bind("<ButtonRelease-1>", self.stop_tool)

        # Create a PIL image.
        self.pil_image = Image.new("RGB", (self.width, self.height))
        self.photo_image = ImageTk.PhotoImage(self.pil_image)
        self.image_sprite = self.canvas.create_image(self.center_y, self.center_x, image=self.photo_image)

        # Set up tools.
        self.tool_processors = {}
        self.tool_processors["draw"] = DrawProcessor(self)
        self.tool_processors["brush"] = BrushProcessor(self)
        self.tool_processors["fill"] = FillProcessor(self)

        # Create tools-window.
        self.tools_window = ToolsWindow(self)

        self.segments_spinbox_changed()
        self.mirror_checkbutton_changed()


    def click(self):
        pass


    def color_button_clicked(self):
        self.color = askcolor(color=self.color)[1]


    def segments_spinbox_changed(self):
        self.segments = int(self.segments_spinbox.get())


    def mirror_checkbutton_changed(self):
        self.mirror = self.mirror_checkbutton_var.get() == 1


    def notify_tool_change(self, new_tool):
        self.current_tool_processor = self.tool_processors[new_tool]


    def start_tool(self, event):
        self.current_tool_processor.start(event.x, event.y)


    def move_tool(self, event):
        self.current_tool_processor.move(event.x, event.y)


    def stop_tool(self, event):
        self.current_tool_processor.stop(event.x, event.y)


    def refresh(self):
        del self.image_sprite
        del self.photo_image
        self.photo_image = ImageTk.PhotoImage(self.pil_image)
        self.image_sprite = self.canvas.create_image(self.center_x, self.center_y, image=self.photo_image)


if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
