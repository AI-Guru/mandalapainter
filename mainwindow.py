import tkinter as tk
from toolswindow import *
from toolprocessors import *
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageChops, ImageEnhance, ImageColor, ImageOps

class MainWindow(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # TODO set title

        column = 0

        # Adds a button for mirroring.
        self.mirror_button = tk.Button(self, text="Mirror", command=self.click)
        self.mirror_button.grid(row=0, column=column)
        column += 1

        # Save button.
        self.save_button = tk.Button(self, text="Save", command=self.click)
        self.save_button.grid(row=0, column=column)
        column += 1

        # Undo button.
        self.undo_button = tk.Button(self, text="Undo", command=self.click)
        self.undo_button.grid(row=0, column=column)
        column += 1

        self.width = 800
        self.height = 800
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.segments = 32
        self.mirror = True
        self.color = "white"
        self.line_width = 2

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


    def click(self):
        pass


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
