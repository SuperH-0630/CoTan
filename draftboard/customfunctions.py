import math

import tkinter
import tkinter.messagebox

SCREEN = None  # 设置屏幕
func_input = None
help = None
button = None
logger = None
bg_color = "#FFFAFA"  # 主颜色
botton_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
help_doc = """
请在第一个输入框输入你的函数方程，不需要输入f(x)=和y=,唯一变量是x(x为自变量)
圆周率-Pi，自然无理数-e
指数的表示符号：**，比如x**2表示x的二次方
对数的表示符号：log(a,b)，其中a是真书，b是底数(没有lg和ln)
三角函数sin(),cos(),tan(),cot(),csc(),sec()
反三角函数arcsin(),arccos(),arctan()
双曲函数：sinh(),cosh(),tanh()
注意：三角函数必须带括号使用
不支持定义域选择，不支持分段函数
"""


class CustomFuncLogger:
    def __init__(self):
        self.func = None

    def set(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func


class FunctionExpression:
    def __init__(self, func):
        self.func = func
        self.named_domain = {
            "x": 0,
            "Pi": math.pi,
            "e": math.e,
            "log": math.log,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "cot": lambda x: 1 / math.tan(x),
            "csc": lambda x: 1 / math.sin(x),
            "sec": lambda x: 1 / math.cos(x),
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
        }

    def __call__(self, x):
        self.named_domain["x"] = x
        return eval(self.func, self.named_domain)


def custom():
    global func_input, help_doc, logger
    func_str = func_input.get().replace(" ", "")
    if func_str:
        if tkinter.messagebox.askokcancel(
            "提示", f"是否确认生成自定义函数:\n{func_input.get()}\n(点击取消可撤销未执行的制造函数)"
        ):
            logger.set(FunctionExpression(func_input.get()))
        else:
            logger.set(None)
    else:
        if tkinter.messagebox.askokcancel("提示", f"点击确定撤销为执行的制造函数"):
            logger.set(None)


def get_help():
    tkinter.messagebox.showinfo(title="帮助", message=help_doc)


def make_func():
    global SCREEN, func_input, help, button, logger
    SCREEN = tkinter.Toplevel(bg=bg_color)
    SCREEN.title("")
    SCREEN.resizable(width=False, height=False)
    SCREEN.geometry(f"+350+10")
    button = tkinter.Button(
        SCREEN,
        text="制造函数",
        command=custom,
        width=28,
        height=1,
        bg=bg_color,
        fg=word_color,
    )
    help = tkinter.Button(
        SCREEN,
        text="帮助",
        command=get_help,
        width=28,
        height=1,
        bg=bg_color,
        fg=word_color,
    )
    func_input = tkinter.Entry(SCREEN)
    func_input.pack(fill=tkinter.BOTH)
    button.pack()
    help.pack()
    logger = CustomFuncLogger()
    return logger
