import tkinter.messagebox
import math
from CGB import TK_DoneHS

def HS_1():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制1次函数(点击取消可撤销未执行的函数)'):
        HS_List[1] = lambda x:x
    else:
        HS_List[1] = None

def HS_2():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制2次函数(点击取消可撤销未执行的函数)'):
        HS_List[2] = lambda x:x**2
    else:
        HS_List[2] = None

def HS_3():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制3次函数(点击取消可撤销未执行的函数)'):
        HS_List[4] = lambda x:x**3
    else:
        HS_List[4] = None

def HS_D1():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制-1次函数(点击取消可撤销未执行的函数)'):
        HS_List[3] = lambda x:1/x
    else:
        HS_List[3] = None

def HS_GH():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制根号函数(点击取消可撤销未执行的函数)'):
        HS_List[5] = lambda x:x**(1/2)
    else:
        HS_List[5] = None

def HS_ZS():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制指数函数(点击取消可撤销未执行的函数)'):
        HS_List[6] = lambda x:10**x
    else:
        HS_List[6] = None

def HS_DS():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制对数函数(点击取消可撤销未执行的函数)'):
        HS_List[7] = lambda x:math.log(x,2)
    else:
        HS_List[7] = None

def HS_DS2():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制对数函数2(点击取消可撤销未执行的函数)'):
        HS_List[8] = lambda x:math.log(2,x)
    else:
        HS_List[8] = None

def HS_sin():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制正弦函数(点击取消可撤销未执行的函数)'):
        HS_List[9] = lambda x:math.sin(x)
    else:
        HS_List[9] = None

def HS_cos():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制余弦函数(点击取消可撤销未执行的函数)'):
        HS_List[10] = lambda x:math.cos(x)
    else:
        HS_List[10] = None

def HS_tan():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制正切函数(点击取消可撤销未执行的函数)'):
        HS_List[11] = lambda x:math.tan(x)
    else:
        HS_List[11] = None

def HS_cot():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制余切函数(点击取消可撤销未执行的函数)'):
        HS_List[12] = lambda x:1/math.tan(x)
    else:
        HS_List[12] = None

def HS_sec():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制正割函数(点击取消可撤销未执行的函数)'):
        HS_List[13] = lambda x:1/math.cos(x)
    else:
        HS_List[13] = None

def HS_csc():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制余割函数(点击取消可撤销未执行的函数)'):
        HS_List[11] = lambda x:1/math.sin(x)
    else:
        HS_List[11] = None

def HS_arcsin():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制反正弦函数(点击取消可撤销未执行的函数)'):
        HS_List[12] = lambda x:math.asin(x)
    else:
        HS_List[12] = None

def HS_arccos():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制反余弦函数(点击取消可撤销未执行的函数)'):
        HS_List[13] = lambda x:math.acos(x)
    else:
        HS_List[13] = None

def HS_arctan():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制反正切函数(点击取消可撤销未执行的函数)'):
        HS_List[14] = lambda x:math.atan(x)
    else:
        HS_List[14] = None

def HS_arccot():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制反余切函数(点击取消可撤销未执行的函数)'):
        HS_List[15] = lambda x:1/math.atan(x)
    else:
        HS_List[15] = None

def HS_arcsec():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制反正割函数(点击取消可撤销未执行的函数)'):
        HS_List[16] = lambda x:1/math.acos(x)
    else:
        HS_List[16] = None

def HS_arccsc():
    global HS_List
    if tkinter.messagebox.askokcancel('提示', '是否绘制反余割函数(点击取消可撤销未执行的函数)'):
        HS_List[17] = lambda x:1/math.asin(x)
    else:
        HS_List[17] = None

def HS_ZDY():
    global HS_List,Num
    get = TK_DoneHS.Done_HS()
    if get != None:
        HS_List[Num] = get
        Num += 1

def close():
    global top
    try:TK_DoneHS.top.destroy()
    except:pass
    top.destroy()

def CHS():
    global HS_List#绘制函数列表
    global Num,top
    Num = 18#字定义函数的序号
    HS_List = {}
    w_b=20

    top = tkinter.Tk()  # 设置屏幕
    top.title('')
    top.resizable(width=False, height=False)
    top.geometry(f'+180+10')
    tkinter.Button(top, text="1次函数", command=HS_1, width=w_b, height=1).pack()
    tkinter.Button(top, text="2次函数", command=HS_2, width=w_b, height=1).pack()
    tkinter.Button(top, text="-1次函数", command=HS_D1, width=w_b, height=1).pack()
    tkinter.Button(top, text="3次函数", command=HS_3, width=w_b, height=1).pack()
    tkinter.Button(top, text="根号函数", command=HS_GH, width=w_b, height=1).pack()
    tkinter.Button(top, text="对数函数", command=HS_DS, width=w_b, height=1).pack()
    tkinter.Button(top, text="指数函数", command=HS_ZS, width=w_b, height=1).pack()
    tkinter.Button(top, text="对数底函数", command=HS_DS2, width=w_b, height=1).pack()
    tkinter.Button(top, text="sin函数", command=HS_sin, width=w_b, height=1).pack()
    tkinter.Button(top, text="cos函数", command=HS_cos, width=w_b, height=1).pack()
    tkinter.Button(top, text="tan函数", command=HS_tan, width=w_b, height=1).pack()
    tkinter.Button(top, text="cot函数", command=HS_tan, width=w_b, height=1).pack()
    tkinter.Button(top, text="csc函数", command=HS_csc, width=w_b, height=1).pack()
    tkinter.Button(top, text="sec函数", command=HS_sec, width=w_b, height=1).pack()
    tkinter.Button(top, text="arcsin函数", command=HS_arcsin, width=w_b, height=1).pack()
    tkinter.Button(top, text="arccos函数", command=HS_arccos, width=w_b, height=1).pack()
    tkinter.Button(top, text="arctan函数", command=HS_arctan, width=w_b, height=1).pack()
    tkinter.Button(top, text="arccot函数", command=HS_arctan, width=w_b, height=1).pack()
    tkinter.Button(top, text="arccsc函数", command=HS_arccsc, width=w_b, height=1).pack()
    tkinter.Button(top, text="arcsec函数", command=HS_arcsec, width=w_b, height=1).pack()
    tkinter.Button(top, text="自定义函数", command=HS_ZDY, width=w_b, height=3).pack()
    top.protocol('WM_DELETE_WINDOW', close)
    top.mainloop()
    return HS_List