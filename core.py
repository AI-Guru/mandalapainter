import tkinter as tk
from tkinter.colorchooser import askcolor
import math
import numpy as np


class AbstractToolProcessor:

    def __init__(self, main_window):

        self.main_window = main_window

        pass

    def start(self, x, y):

        # Store the old coordinates.
        self.old_x = x
        self.old_y = y

        # Compute clicked_segment.
        vec_x = x - self.main_window.center_x
        vec_y = y - self.main_window.center_x
        angle = math.atan2(vec_y, vec_x)
        if angle < 0.0:
            angle += 2.0 * math.pi
        self.clicked_segment = int(angle * self.main_window.segments / (2.0 * math.pi))

        # Moved distance.
        self.moved_distance_in_step = 0
        self.overall_moved_distance = 0


    def move(self, x, y):
        self.moved_distance_in_step = get_distance(self.old_x, self.old_y, x, y)
        self.overall_moved_distance += self.moved_distance_in_step


    def stop(self, x, y):
        self.old_x = None
        self.old_y = None
        self.clicked_segment = None
        self.moved_distance_in_step = None
        self.overall_moved_distance = None


    def get_mandala_points(self, x, y):
        x, y = self.center_point(x, y)
        angle, length = polar_coordinates(x, y)

        clicked_segment_angle = 2.0 * math.pi * self.clicked_segment / self.main_window.segments

        angle -= clicked_segment_angle

        points = []
        for segment in range(self.main_window.segments):

            if self.main_window.mirror == True and segment % 2 != self.clicked_segment % 2:
                segment_angle = 2.0 * math.pi * (segment + 1) / self.main_window.segments
                x, y = vector_from_angle_and_length(segment_angle - angle, length)

            else:
                segment_angle = 2.0 * math.pi * segment / self.main_window.segments
                x, y = vector_from_angle_and_length(segment_angle + angle, length)

            x, y = self.recenter_point(x, y)
            points.append((x, y))

        return points


    def center_point(self, x, y):
        return x - self.main_window.center_x, y - self.main_window.center_y


    def recenter_point(self, x, y):
        return x + self.main_window.center_x, y + self.main_window.center_y



class AbstractToolModelview:

    def __init__(self, main_window):

        self.main_window = main_window
        self.toplevel = tk.Toplevel(self.main_window)

        self.row = 0

    def enable_color(self):

        self.color_button = tk.Button(self.toplevel, text='Color', command=self.color_button_clicked)
        self.color_button.grid(row=self.row, column=0)
        self.row += 1
        self.color = "white"


    def enable_size(self):

        size_start_value = 1
        size_end_value = 100

        def size_var_changed(*args):
            value = self.size_var.get()
            if value >= size_start_value and value <= size_end_value:
                self.size = int(value)
            else:
                self.size_var.set(10)

        self.size_var = tk.IntVar()
        self.size_var.set(10)
        self.size_var.trace("w", size_var_changed)
        self.size_spinbox = tk.Spinbox(self.toplevel, width=3, textvariable=self.size_var, from_=size_start_value, to=size_end_value)
        self.size_spinbox.grid(row=self.row, column=0)
        self.row += 1


    def set_size(self, size):
        self.size_var.set(10)


    def color_button_clicked(self):
        self.color = askcolor(color=self.color)[1]


    def show(self):
        self.toplevel.deiconify()


    def hide(self):
        self.toplevel.withdraw()



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
