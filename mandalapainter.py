from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageChops, ImageEnhance
from tkinter.colorchooser import askcolor
import math
import numpy as np


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()
        self.root.tk.call('tk', 'scaling', 1.0)

        column = 0

        # Adds a button for mirroring.
        self.mirror_button = Button(self.root, text='Mirror', command=self.toggle_mirror)
        self.mirror_button.grid(row=0, column=column)

        self.color_button = Button(self.root, text='Color', command=self.choose_color)
        self.color_button.grid(row=1, column=column)
        column += 1

        self.segments_button = Button(self.root, text='Segments', command=self.draw_segments)
        self.segments_button.grid(row=0, column=column)
        column += 1

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL, label="Pen Size")
        self.choose_size_button.grid(row=0, column=column)
        column += 1

        self.choose_segments = Scale(self.root, from_=4, to=40, orient=HORIZONTAL, label="Segments")
        self.choose_segments.set(16)
        self.choose_segments.grid(row=0, column=column)
        column += 1

        self.choose_blur = Scale(self.root, from_=0, to=10, orient=HORIZONTAL, label="Blur degree")
        self.choose_blur.grid(row=0, column=column)
        column += 1

        self.save_button = Button(self.root, text='save', command=self.save_image)
        self.save_button.grid(row=0, column=column)
        column += 1

        self.size = (600, 600)
        self.center = (300, 300)
        self.segments = 40
        self.clicked_segment = None
        self.segment_vectors = []

        self.mirror = False

        self.c = Canvas(self.root, bg='red', width=self.size[0], height=self.size[0])
        self.c.grid(row=2, columnspan=column)

        # Create a PIL image.
        self.pilImage = Image.new('RGB', self.size)
        self.image = ImageTk.PhotoImage(self.pilImage)
        self.imagesprite = self.c.create_image(self.center[0], self.center[1], image=self.image)

        self.setup()

        self.root.mainloop()


    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = "white"
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

        self.c.create_oval(self.center[0] - 5, self.center[1] - 5, self.center[0] + 5, self.center[1] + 5, fill="white")


    def toggle_mirror(self):
        self.mirror = not self.mirror

    def draw_segments(self):
        for segment in range(self.segments):
            pass


    def save_image(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if file is None:
            return
        self.pilImage.save(file.name)


    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):

        if self.clicked_segment == None:
            vec_x = event.x - self.center[0]
            vec_y = event.y - self.center[1]
            angle = math.atan2(vec_y, vec_x)
            if angle < 0.0:
                angle += 2.0 * math.pi
            self.clicked_segment = int(angle * self.segments / (2.0 * math.pi))

            # For debugging.
            #self.render_segments(self.clicked_segment)

        self.line_width = self.choose_size_button.get()
        self.segments = self.choose_segments.get()
        self.blur_degree = self.choose_blur.get() / 10.0

        brush_offsets = [(-5, 2), (2, 12), (-20, 2), (8, -4), (-4, -6)]

        if self.old_x and self.old_y:
            distance = get_distance(self.old_x, self.old_y, event.x, event.y)
            if distance > 1.0:
                self.draw_line(self.old_x, self.old_y, event.x, event.y)

                #for (x, y) in brush_offsets:
                #    self.draw_line(x + self.old_x, y + self.old_y, x + event.x, y + event.y)

                self.old_x = event.x
                self.old_y = event.y
        else:
            self.old_x = event.x
            self.old_y = event.y


    def render_segments(self, clicked_segment):
        for segment in range(self.segments):
            points = np.zeros(3 * 2)

            points[0] = self.center[0]
            points[1] = self.center[1]

            angle = segment * 2.0 * math.pi / self.segments
            points[2] = self.center[0] + 100.0 * math.sin(angle)
            points[3] = self.center[1] + 100.0 * math.cos(angle)

            angle = (segment + 1) * 2.0 * math.pi / self.segments
            points[4] = self.center[0] + 100.0 * math.sin(angle)
            points[5] = self.center[1] + 100.0 * math.cos(angle)

            points = points.astype("int16")[::-1]

            if segment == clicked_segment:
                fill = "red"
            else:
                fill = "gray"
            self.c.create_polygon(*points, fill=fill)


    def draw_line(self, x1, y1, x2, y2):

        del self.imagesprite
        del self.image

        if self.blur_degree != 0:
            blurredImage = self.pilImage.filter(ImageFilter.BLUR)
            self.pilImage = Image.blend(self.pilImage, blurredImage, alpha=self.blur_degree / 10.0)
            #self.pilImage = ImageChops.add(self.pilImage, blurredImage)
            #self.pilImage = ImageEnhance.Brightness(self.pilImage).enhance(0.9995)

        draw = ImageDraw.Draw(self.pilImage)

        # Center the vectors.
        x1 -= self.center[0]
        y1 -= self.center[1]
        x2 -= self.center[0]
        y2 -= self.center[1]

        # Compute polar coordinates of vectors.
        angle1, length1 = polar_coordinates(x1, y1)
        angle2, length2 = polar_coordinates(x2, y2)

        # BLA
        clicked_segment_angle = 2.0 * math.pi * self.clicked_segment / self.segments

        angle1 -= clicked_segment_angle
        angle2 -= clicked_segment_angle
        for segment in range(self.segments):

            if self.mirror == True and segment % 2 != self.clicked_segment % 2:
                segment_angle = 2.0 * math.pi * (segment + 1) / self.segments
                x1, y1 = vector_from_angle_and_length(segment_angle - angle1, length1)
                x2, y2 = vector_from_angle_and_length(segment_angle - angle2, length2)

            else:
                segment_angle = 2.0 * math.pi * segment / self.segments
                x1, y1 = vector_from_angle_and_length(segment_angle + angle1, length1)
                x2, y2 = vector_from_angle_and_length(segment_angle + angle2, length2)

            # Back with center and draw.
            x1 += self.center[0]
            y1 += self.center[1]
            x2 += self.center[0]
            y2 += self.center[1]
            draw.line((x1, y1, x2, y2), fill=self.color, width=self.line_width)

            # Draw a line.
            cap_size = self.line_width // 2
            draw.ellipse ((x1 - cap_size, y1 - cap_size, x1 + cap_size, y1 + cap_size), fill=self.color)
            draw.ellipse ((x2 - cap_size, y2 - cap_size, x2 + cap_size, y2 + cap_size), fill=self.color)

        del draw

        self.image = ImageTk.PhotoImage(self.pilImage)
        self.imagesprite = self.c.create_image(self.center[0], self.center[1], image=self.image)


    def reset(self, event):
        self.old_x, self.old_y = None, None
        self.clicked_segment = None


def vector_from_angle_and_length(angle, length):
    vector = (length * math.sin(angle), length * math.cos(angle))
    vector = np.array(vector)
    return vector


def polar_coordinates(x, y):
    angle = math.atan2(x, y)
    if angle < 0.0:
        angle += 2.0 * math.pi
    length = math.sqrt(x**2 + y**2)
    return angle, length


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    Paint()
