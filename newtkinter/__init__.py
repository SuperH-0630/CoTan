import tkinter as tk
from tkinter import filedialog


class DragWindow(tk.Tk):
    root_x, root_y, abs_x, abs_y = 0, 0, 0, 0
    width, height = None, None

    def __init__(self, alpha=0.97, width=None, height=None):
        super().__init__()
        self.width, self.height = width, height
        self.wm_attributes("-alpha", alpha)  # 透明度
        self.bind("<B1-Motion>", self._on_move)
        self.bind("<ButtonPress-1>", self._on_tap)

    def set_display_postion(self, offset_x, offset_y):
        self.geometry("+%s+%s" % (offset_x, offset_y))

    def set_window_size(self, w, h):
        self.width, self.height = w, h
        self.geometry("%sx%s" % (w, h))

    def _on_move(self, event):
        offset_x = event.x_root - self.root_x
        offset_y = event.y_root - self.root_y

        if self.width and self.height:
            geo_str = "%sx%s+%s+%s" % (
                self.width,
                self.height,
                self.abs_x + offset_x,
                self.abs_y + offset_y,
            )
        else:
            geo_str = "+%s+%s" % (self.abs_x + offset_x, self.abs_y + offset_y)
        self.geometry(geo_str)

    def _on_tap(self, event):
        self.root_x, self.root_y = event.x_root, event.y_root
        self.abs_x, self.abs_y = self.winfo_x(), self.winfo_y()

# 重建文件读取类 askdirectory,askopenfilename,askopenfilenames,asksaveasfilename


askopenfilenames = filedialog.askopenfilenames


def askopenfilename(title, must=False, **parameters):
    while True:
        name = filedialog.askopenfilename(title=title, **parameters)
        if name == '':
            if not must:
                raise NameError
            continue
        break
    return name


def asksaveasfilename(title, **parameters):
    name: str = filedialog.asksaveasfilename(title=title, **parameters)
    if name == '':
        raise NameError
    end = parameters.get('filetypes', [('', '')])[0][0]
    if name.endswith(end):
        return name
    return name + end


def askdirectory(title, must=False, **parameters):
    while True:
        name: str = filedialog.askdirectory(title=title, **parameters)
        if name == '':
            if not must:
                raise NameError
            continue
        break
    return name
