import tkinter as tk
from tkinter import filedialog


def center_windows(screen, w, h):
    ws = screen.winfo_screenwidth()
    hs = screen.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws/2) - (w/2) + 1
    y = (hs/2) - (h/2) + 1
    screen.geometry('%dx%d+%d+%d' % (w, h, x, y))


class DragWindow(tk.Tk):
    root_x, root_y, abs_x, abs_y = 0, 0, 0, 0
    width, height = None, None

    def __init__(self, alpha=1, width=None, height=None, drag=False):
        super().__init__()
        self.width, self.height = width, height
        self.wm_attributes("-alpha", alpha)  # 透明度
        if drag:
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
