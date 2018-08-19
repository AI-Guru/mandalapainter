import tkinter as tk

class ToolsWindow:

    def __init__(self, master_window):

        self.master_window = master_window

        self.toplevel = tk.Toplevel(master_window)
        self.toplevel.wm_title("Tools")
        self.toplevel.geometry("75x150+800+0")
        self.toplevel.update()

        row = 0

        self.draw_button = tk.Button(self.toplevel, text="Draw", command=self.click_draw_button)
        self.draw_button.grid(row=row, column=0)
        row += 1

        self.brush_button = tk.Button(self.toplevel, text="Brush", command=self.click_brush_button)
        self.brush_button.grid(row=row, column=0)
        row += 1

        self.fill_button = tk.Button(self.toplevel, text="Fill", command=self.click_fill_button)
        self.fill_button.grid(row=row, column=0)
        row += 1

        # Activate a tool.
        self.active_button = None
        self.click_draw_button()
        #self.click_brush_button()


    def click_draw_button(self):
        if self.active_button == self.draw_button:
            return
        self.activate_button(self.draw_button)
        self.master_window.notify_tool_change("draw")


    def click_brush_button(self):
        if self.active_button == self.brush_button:
            return
        self.activate_button(self.brush_button)
        self.master_window.notify_tool_change("brush")


    def click_fill_button(self):
        if self.active_button == self.fill_button:
            return
        self.activate_button(self.fill_button)
        self.master_window.notify_tool_change("fill")


    def activate_button(self, button):
        if self.active_button != None:
            self.active_button.config(relief=tk.RAISED)
        button.config(relief=tk.SUNKEN)
        self.active_button = button
