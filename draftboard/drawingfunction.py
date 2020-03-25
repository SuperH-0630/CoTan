import math

import tkinter.messagebox

from draftboard import customfunctions

width = 20
SCREEN = None  # 设置屏幕
bg_color = "#FFFAFA"  # 主颜色
botton_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色


class Logger:
    def __init__(self):
        self.func_dict = {}
        self.custom_loger = {}
        self.custom_function_index = 18
    
    def __call__(self, *args, **kwargs):
        for i in self.custom_loger:
            self.func_dict[i] = self.custom_loger[i]()
        return self.func_dict


loger = Logger()


class UIAPI:
    @staticmethod
    def askok_gui(message):
        return tkinter.messagebox.askokcancel('提示', message)


class API:
    @staticmethod
    def linear_func():
        if UIAPI.askok_gui("是否绘制1次函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[1] = lambda x: x
        else:
            loger.func_dict[1] = None

    @staticmethod
    def quadratic_func():
        if UIAPI.askok_gui("是否绘制2次函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[2] = lambda x: x ** 2
        else:
            loger.func_dict[2] = None

    @staticmethod
    def cubic_function():
        if UIAPI.askok_gui("是否绘制3次函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[4] = lambda x: x ** 3
        else:
            loger.func_dict[4] = None

    @staticmethod
    def inverse_func():
        if UIAPI.askok_gui("是否绘制-1次函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[3] = lambda x: 1 / x
        else:
            loger.func_dict[3] = None

    @staticmethod
    def radical_func():
        if UIAPI.askok_gui("是否绘制根号函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[5] = lambda x: x ** (1 / 2)
        else:
            loger.func_dict[5] = None

    @staticmethod
    def exp_func():
        if UIAPI.askok_gui("是否绘制指数函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[6] = lambda x: 10 ** x
        else:
            loger.func_dict[6] = None

    @staticmethod
    def log_func():
        if UIAPI.askok_gui("是否绘制对数函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[7] = lambda x: math.log(x, 2)
        else:
            loger.func_dict[7] = None

    @staticmethod
    def log2_func():
        if UIAPI.askok_gui("是否绘制对数函数2(点击取消可撤销未执行的函数)"):
            loger.func_dict[8] = lambda x: math.log(2, x)
        else:
            loger.func_dict[8] = None

    @staticmethod
    def sin_func():
        if UIAPI.askok_gui("是否绘制正弦函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[9] = lambda x: math.sin(x)
        else:
            loger.func_dict[9] = None

    @staticmethod
    def cos_func():
        if UIAPI.askok_gui("是否绘制余弦函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[10] = lambda x: math.cos(x)
        else:
            loger.func_dict[10] = None

    @staticmethod
    def tan_func():
        if UIAPI.askok_gui("是否绘制正切函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[11] = lambda x: math.tan(x)
        else:
            loger.func_dict[11] = None

    @staticmethod
    def cot_func():
        if UIAPI.askok_gui("是否绘制余切函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[12] = lambda x: 1 / math.tan(x)
        else:
            loger.func_dict[12] = None

    @staticmethod
    def sec_func():
        if UIAPI.askok_gui("是否绘制正割函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[13] = lambda x: 1 / math.cos(x)
        else:
            loger.func_dict[13] = None

    @staticmethod
    def csc_func():
        if UIAPI.askok_gui("是否绘制余割函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[11] = lambda x: 1 / math.sin(x)
        else:
            loger.func_dict[11] = None

    @staticmethod
    def arcsin_func():
        if UIAPI.askok_gui("是否绘制反正弦函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[12] = lambda x: math.asin(x)
        else:
            loger.func_dict[12] = None

    @staticmethod
    def arccos_func():
        if UIAPI.askok_gui("是否绘制反余弦函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[13] = lambda x: math.acos(x)
        else:
            loger.func_dict[13] = None

    @staticmethod
    def arctan_func():
        if UIAPI.askok_gui("是否绘制反正切函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[14] = lambda x: math.atan(x)
        else:
            loger.func_dict[14] = None

    @staticmethod
    def arccot_func():
        if UIAPI.askok_gui("是否绘制反余切函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[15] = lambda x: 1 / math.atan(x)
        else:
            loger.func_dict[15] = None

    @staticmethod
    def arcsec_func():
        if UIAPI.askok_gui("是否绘制反正割函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[16] = lambda x: 1 / math.acos(x)
        else:
            loger.func_dict[16] = None

    @staticmethod
    def arccsc_func():
        if UIAPI.askok_gui("是否绘制反余割函数(点击取消可撤销未执行的函数)"):
            loger.func_dict[17] = lambda x: 1 / math.asin(x)
        else:
            loger.func_dict[17] = None

    @staticmethod
    def custom_func():
        loger.custom_loger[loger.custom_function_index] = customfunctions.make_func()


def func_box():
    global SCREEN, loger
    loger = Logger()
    SCREEN = tkinter.Toplevel(bg=bg_color)  # 设置屏幕
    SCREEN.title("")
    SCREEN.resizable(width=False, height=False)
    SCREEN.geometry(f"+180+10")
    tkinter.Button(
        SCREEN,
        text="1次函数",
        bg=bg_color,
        fg=word_color,
        command=API.linear_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="2次函数",
        bg=bg_color,
        fg=word_color,
        command=API.quadratic_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="-1次函数",
        bg=bg_color,
        fg=word_color,
        command=API.inverse_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="3次函数",
        bg=bg_color,
        fg=word_color,
        command=API.cubic_function,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="根号函数",
        bg=bg_color,
        fg=word_color,
        command=API.radical_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="对数函数",
        bg=bg_color,
        fg=word_color,
        command=API.log_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="指数函数",
        bg=bg_color,
        fg=word_color,
        command=API.exp_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="对数底函数",
        bg=bg_color,
        fg=word_color,
        command=API.log2_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="sin函数",
        bg=bg_color,
        fg=word_color,
        command=API.sin_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="cos函数",
        bg=bg_color,
        fg=word_color,
        command=API.cos_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="tan函数",
        bg=bg_color,
        fg=word_color,
        command=API.tan_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="cot函数",
        bg=bg_color,
        fg=word_color,
        command=API.tan_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="csc函数",
        bg=bg_color,
        fg=word_color,
        command=API.csc_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="sec函数",
        bg=bg_color,
        fg=word_color,
        command=API.sec_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="arcsin函数",
        bg=bg_color,
        fg=word_color,
        command=API.arcsin_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="arccos函数",
        bg=bg_color,
        fg=word_color,
        command=API.arccos_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="arctan函数",
        bg=bg_color,
        fg=word_color,
        command=API.arctan_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="arccot函数",
        bg=bg_color,
        fg=word_color,
        command=API.arccot_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="arccsc函数",
        bg=bg_color,
        fg=word_color,
        command=API.arccsc_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="arcsec函数",
        bg=bg_color,
        fg=word_color,
        command=API.arcsec_func,
        width=width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="自定义函数",
        bg=bg_color,
        fg=word_color,
        command=API.custom_func,
        width=width,
        height=3,
    ).pack()
    return loger
