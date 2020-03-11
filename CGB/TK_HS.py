import tkinter.messagebox
import math
from CGB import TK_DoneHS


def linear_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制1次函数(点击取消可撤销未执行的函数)'):
        func_dict[1] = lambda x: x
    else:
        func_dict[1] = None


def quadratic_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制2次函数(点击取消可撤销未执行的函数)'):
        func_dict[2] = lambda x: x ** 2
    else:
        func_dict[2] = None


def cubic_function():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制3次函数(点击取消可撤销未执行的函数)'):
        func_dict[4] = lambda x: x ** 3
    else:
        func_dict[4] = None


def inverse_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制-1次函数(点击取消可撤销未执行的函数)'):
        func_dict[3] = lambda x: 1 / x
    else:
        func_dict[3] = None


def radical_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制根号函数(点击取消可撤销未执行的函数)'):
        func_dict[5] = lambda x: x ** (1 / 2)
    else:
        func_dict[5] = None


def exp_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制指数函数(点击取消可撤销未执行的函数)'):
        func_dict[6] = lambda x: 10 ** x
    else:
        func_dict[6] = None


def log_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制对数函数(点击取消可撤销未执行的函数)'):
        func_dict[7] = lambda x: math.log(x, 2)
    else:
        func_dict[7] = None


def log2_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制对数函数2(点击取消可撤销未执行的函数)'):
        func_dict[8] = lambda x: math.log(2, x)
    else:
        func_dict[8] = None


def sin_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制正弦函数(点击取消可撤销未执行的函数)'):
        func_dict[9] = lambda x: math.sin(x)
    else:
        func_dict[9] = None


def cos_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制余弦函数(点击取消可撤销未执行的函数)'):
        func_dict[10] = lambda x: math.cos(x)
    else:
        func_dict[10] = None


def tan_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制正切函数(点击取消可撤销未执行的函数)'):
        func_dict[11] = lambda x: math.tan(x)
    else:
        func_dict[11] = None


def cot_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制余切函数(点击取消可撤销未执行的函数)'):
        func_dict[12] = lambda x: 1 / math.tan(x)
    else:
        func_dict[12] = None


def sec_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制正割函数(点击取消可撤销未执行的函数)'):
        func_dict[13] = lambda x: 1 / math.cos(x)
    else:
        func_dict[13] = None


def csc_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制余割函数(点击取消可撤销未执行的函数)'):
        func_dict[11] = lambda x: 1 / math.sin(x)
    else:
        func_dict[11] = None


def arcsin_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制反正弦函数(点击取消可撤销未执行的函数)'):
        func_dict[12] = lambda x: math.asin(x)
    else:
        func_dict[12] = None


def arccos_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制反余弦函数(点击取消可撤销未执行的函数)'):
        func_dict[13] = lambda x: math.acos(x)
    else:
        func_dict[13] = None


def arctan_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制反正切函数(点击取消可撤销未执行的函数)'):
        func_dict[14] = lambda x: math.atan(x)
    else:
        func_dict[14] = None


def arccot_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制反余切函数(点击取消可撤销未执行的函数)'):
        func_dict[15] = lambda x: 1 / math.atan(x)
    else:
        func_dict[15] = None


def arcsec_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制反正割函数(点击取消可撤销未执行的函数)'):
        func_dict[16] = lambda x: 1 / math.acos(x)
    else:
        func_dict[16] = None


def arccsc_func():
    global func_dict
    if tkinter.messagebox.askokcancel('提示', '是否绘制反余割函数(点击取消可撤销未执行的函数)'):
        func_dict[17] = lambda x: 1 / math.asin(x)
    else:
        func_dict[17] = None


def custom_func():
    global func_dict, custom_function_index
    get = TK_DoneHS.make_func()
    if get is not None:
        func_dict[custom_function_index] = get
        custom_function_index += 1


def close():
    global SCREEN
    try:
        TK_DoneHS.top.destroy()
    except BaseException:
        pass
    SCREEN.destroy()


def func_box():
    global func_dict  # 绘制函数列表
    global custom_function_index, SCREEN
    custom_function_index = 18  # 字定义函数的序号
    func_dict = {}
    width = 20

    SCREEN = tkinter.Tk()  # 设置屏幕
    SCREEN.title('')
    SCREEN.resizable(width=False, height=False)
    SCREEN.geometry(f'+180+10')
    tkinter.Button(
        SCREEN,
        text="1次函数",
        command=linear_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="2次函数",
        command=quadratic_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="-1次函数",
        command=inverse_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="3次函数",
        command=cubic_function,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="根号函数",
        command=radical_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="对数函数",
        command=log_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="指数函数",
        command=exp_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="对数底函数",
        command=log2_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="sin函数",
        command=sin_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="cos函数",
        command=cos_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="tan函数",
        command=tan_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="cot函数",
        command=tan_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="csc函数",
        command=csc_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="sec函数",
        command=sec_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="arcsin函数",
        command=arcsin_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="arccos函数",
        command=arccos_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="arctan函数",
        command=arctan_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="arccot函数",
        command=arccot_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="arccsc函数",
        command=arccsc_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="arcsec函数",
        command=arcsec_func,
        width=width,
        height=1).pack()
    tkinter.Button(
        SCREEN,
        text="自定义函数",
        command=custom_func,
        width=width,
        height=3).pack()
    SCREEN.protocol('WM_DELETE_WINDOW', close)
    SCREEN.mainloop()
    return func_dict
