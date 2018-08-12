from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from tkinter.colorchooser import askcolor
import math
import numpy as np


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.mirror_button = Button(self.root, text='mirror', command=self.toggle_mirror)
        self.mirror_button.grid(row=0, column=0)

        self.blur_button = Button(self.root, text='blur', command=self.toggle_blur)
        self.blur_button.grid(row=0, column=1)

        #self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        #self.pen_button.grid(row=0, column=0)

        #self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        #self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        #self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        #self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.size = (600, 600)
        self.center = (300, 300)
        self.segments = 10
        self.clicked_segment = None
        self.segment_vectors = []

        self.mirror = False
        self.blur = False

        # Compute the vectors for the segments.
        #for segment in range(self.segments):

        #    angle1 = segment * 2.0 * math.pi / self.segments
        #    vector1 = (math.sin(angle1), math.cos(angle1))
        #    vector1 = np.array(vector1)

        #    angle2 = (segment + 1) * 2.0 * math.pi / self.segments
        #    vector2 = (math.sin(angle2), math.cos(angle2))
        #    vector2 = np.array(vector2)

        #    vector2 = vector_from_angle_and_size()

            #print(vector1, vector2)
            #self.segment_vectors.append((vector1, vector2))

        self.c = Canvas(self.root, bg='red', width=self.size[0], height=self.size[0])
        self.c.grid(row=1, columnspan=5)

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
        self.eraser_on = False
        #self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

        self.c.create_oval(self.center[0] - 5, self.center[1] - 5, self.center[0] + 5, self.center[1] + 5, fill="white")


    #def use_pen(self):
    #    self.activate_button(self.pen_button)

    #def use_brush(self):
    #    self.activate_button(self.brush_button)

    def toggle_mirror(self):
        self.mirror = not self.mirror

    def toggle_blur(self):
        self.blur = not self.blur

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
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.draw_line(self.old_x, self.old_y, event.x, event.y)

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

        if self.blur == True:
            blurredImage = self.pilImage.filter(ImageFilter.BLUR)
            self.pilImage = Image.blend(self.pilImage, blurredImage, alpha=.2)

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

            # Back with center.
            x1 += self.center[0]
            y1 += self.center[1]
            x2 += self.center[0]
            y2 += self.center[1]

            draw.line((x1, y1, x2, y2), fill=self.color, width=self.line_width)

            ## Draw.
            #self.c.create_line(
            #    x1, y1, x2, y2,
            #    width=self.line_width, fill=self.color,
            #                   capstyle=ROUND, smooth=TRUE, splinesteps=36)

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


if __name__ == '__main__':
    Paint()
