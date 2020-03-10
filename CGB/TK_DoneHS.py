import tkinter
import tkinter.messagebox
import math
help_doc = '''
请在第一个输入框输入你的函数方程，不需要输入f(x)=和y=,唯一变量是x(x为自变量)
圆周率-Pi，自然无理数-e
指数的表示符号：**，比如x**2表示x的二次方
对数的表示符号：log(a,b)，其中a是真书，b是底数(没有lg和ln)
三角函数sin(),cos(),tan(),cot(),csc(),sec()
反三角函数arcsin(),arccos(),arctan()
双曲函数：sinh(),cosh(),tanh()
注意：三角函数必须带括号使用
不支持定义域选择，不支持分段函数
'''


class FunctionExpression:
    def __init__(self, func):
        self.FUNC = func
        self.NAME = {
            'x': 0,
            'Pi': math.pi,
            'e': math.e,
            'log': math.log,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'cot': lambda x: 1 / math.tan(x),
            'csc': lambda x: 1 / math.sin(x),
            'sec': lambda x: 1 / math.cos(x),
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan}

    def __call__(self, x):
        self.NAME['x'] = x
        return eval(self.FUNC, self.NAME)


def determine():
    global HS_Input, HS, help_doc
    Input = HS_Input.get().replace(' ', '')
    if Input:
        if tkinter.messagebox.askokcancel(
                '提示', f'是否确认生成自定义函数:\n{HS_Input.get()}\n(点击取消可撤销未执行的制造函数)'):
            HS = FunctionExpression(HS_Input.get())
        else:
            HS = None
    else:
        if tkinter.messagebox.askokcancel('提示', f'点击确定撤销为执行的制造函数'):
            HS = None


def get_help():
    tkinter.messagebox.showinfo(title='帮助', message=help_doc)


def make_func():
    global HS_Input, HS, top
    HS = None
    top = tkinter.Tk()  # 设置屏幕
    top.title('')
    top.resizable(width=False, height=False)
    top.geometry(f'+350+10')
    button = tkinter.Button(
        top,
        text="制造函数",
        command=determine,
        width=28,
        height=1)  # 收到消息执行这个函数
    help = tkinter.Button(
        top,
        text="帮助",
        command=get_help,
        width=28,
        height=1)  # 帮助菜单
    HS_Input = tkinter.Entry(top)
    HS_Input.pack(fill=tkinter.BOTH)
    button.pack()
    help.pack()
    top.mainloop()
    return HS
