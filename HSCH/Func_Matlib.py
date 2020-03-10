import numpy
import pandas
from matplotlib import pyplot as plt
from matplotlib import rcParams
import tkinter
import tkinter.messagebox
import math
import random
from tkinter.filedialog import asksaveasfile
import tkinter.messagebox
from os import path
from HSCH.HS import HS_lambda, HS_CSV
from HSCH.Func_advanced import Advanced_Control


def Float(IN, si=float, n=True):  # Float筛选系统
    x = []
    for i in IN:
        try:
            if si(i) == si(0) and n:
                continue
            x.append(si(i))
        except ValueError:
            pass
    return x


def Fucn_Draw():
    global HS, X_Input, fig, Xlim_Input, Ylim_Input, YK_Input, XK_Input
    # 画板创造
    addNews('生成绘制取...')
    fig = plt.figure(num='CoTan函数')  # 定义一个图像窗口
    plt.grid(True, ls='--')  # 显示网格(不能放到后面，因为后面调整成为了笛卡尔坐标系)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))  # 设置x轴, y轴在(0, 0)的位置
    ax.spines['left'].set_position(('data', 0))
    # 检测x
    try:
        if XK_Input.get()[0] == 'c':  # 如果输入函数cx#-10#10#1#1
            # 第一部分HS，第二部分S，第三部分E，第四部分KD，第五部分JD
            _HS = XK_Input.get()[1:].split('#')
            P = ['x', -10, 10, 1, 2]  # 保护系统
            try:
                P[0] = _HS[0]
                P[1] = int(_HS[1])
                P[2] = int(_HS[2])
                P[3] = int(_HS[3])
                P[4] = int(_HS[4])
            except BaseException:  # 迭代匹配直到出现错误
                pass
            _HS = P
            x = Float(
                HS_lambda(
                    _HS[0],
                    'x',
                    '',
                    _HS[1],
                    _HS[2],
                    _HS[3],
                    _HS[4]).Cul()[1])  # 取y
            ax.set_xticks(x)
        elif XK_Input.get()[0] == 'y':  # 输入函数y
            x = abs(int(XK_Input.get()[1:]))
            x_major_locator = plt.MultipleLocator(x)
            ax.xaxis.set_major_locator(x_major_locator)
        else:  # 输入纯数字
            x = Float(XK_Input.get().split(','))
            ax.set_xticks(x)
    except BaseException:
        x_major_locator = plt.MultipleLocator(2)
        ax.xaxis.set_major_locator(x_major_locator)
    # 检测y
    try:  # 意外捕捉
        if YK_Input.get()[0] == 'c':  # 如果输入函数cx#-10#10#1#1
            # 第一部分HS，第二部分S，第三部分E，第四部分KD，第五部分JD
            _HS = YK_Input.get()[1:].split('#')
            P = ['x', -10, 10, 1, 2]  # 保护系统
            try:
                P[0] = _HS[0]
                P[1] = int(_HS[1])
                P[2] = int(_HS[2])
                P[3] = int(_HS[3])
                P[4] = int(_HS[4])
            except BaseException:  # 迭代匹配直到出现错误
                pass
            _HS = P
            y = Float(
                HS_lambda(
                    _HS[0],
                    'y',
                    '',
                    _HS[1],
                    _HS[2],
                    _HS[3],
                    _HS[4]).Cul()[1])  # 取y
            ax.set_yticks(y)
        elif YK_Input.get()[0] == 'y':  # 输入函数y
            y = abs(int(YK_Input.get()[1:]))
            y_major_locator = plt.MultipleLocator(y)
            ax.yaxis.set_major_locator(y_major_locator)
        else:
            y = Float(YK_Input.get().split(','))
            ax.set_yticks(y)
    except BaseException:
        y_major_locator = plt.MultipleLocator(2)
        ax.yaxis.set_major_locator(y_major_locator)
    # 极限设计
    try:
        xlim_IN = Float(Xlim_Input.get().split(','), si=int, n=False)
        ylim_IN = Float(Ylim_Input.get().split(','), si=int, n=False)
        try:
            _xlim = [xlim_IN[0], xlim_IN[1]]
        except BaseException:
            _xlim = [-10, 10]
        try:
            _ylim = [ylim_IN[0], ylim_IN[1]]
        except BaseException:
            _ylim = _xlim
    except BaseException:
        _xlim = [-10, 10]
        _ylim = [-10, 10]
    _xlim.sort()
    _ylim.sort()
    plt.xlim(_xlim)
    plt.ylim(_ylim)
    # 函数绘图系统
    addNews('图像绘制中...')
    if not HS:
        return False
    for Fucn in HS:
        get = Fucn.Draw_Cul()
        fx = get[0]
        fy = get[1]
        Func_label = get[2]
        View = get[3]
        First = True
        for i in range(len(fx)):
            x = fx[i]
            y = fy[i]
            if First:
                plt.plot(x, y, View, label=Func_label)  # plot()画出曲线
                First = False
            else:
                plt.plot(x, y, View)
        get = Fucn.getMemory()
        m_x = get[0]
        m_y = get[1]
        max_x, max_y, min_x, min_y = Fucn.Best_value()
        plt.plot(
            m_x,
            m_y,
            View[0] + 'o',
            label=f'Point of {Func_label}')  # 画出一些点
        len_x = sorted(list(set(m_x)))  # 去除list重复项目
        JZD = max_x + min_x

        o_x = None
        for i in range(len(len_x)):
            if i in JZD:
                continue  # 去除极值点
            _x = len_x[i]  # x
            if o_x is None or abs(_x - o_x) >= 1:  # 确保位置
                num = m_x.index(_x)  # y的座位
                _y = m_y[num]
                plt.text(
                    _x, _y, f'({_x},{int(_y)})', fontdict={
                        'size': '10', 'color': 'b'})  # 标出坐标
                o_x = _x

        o_x = None
        n_max = []
        for i in range(len(max_x)):  # 画出最大值
            _x = max_x[i]
            if o_x is None or abs(_x - o_x) >= 1:  # 确保位置
                plt.text(
                    _x - 1,
                    max_y,
                    f'max:({_x},{int(max_y)})',
                    fontdict={
                        'size': '10',
                        'color': 'b'})  # 标出坐标
                n_max.append(_x)
                o_x = _x

        o_x = None
        n_min = []
        for i in range(len(min_x)):  # 画出最小值
            _x = min_x[i]
            if o_x is None or abs(_x - o_x) >= 1:
                n_min.append(_x)
                plt.text(
                    _x - 1,
                    min_y,
                    f'min:({_x},{int(min_y)})',
                    fontdict={
                        'size': '10',
                        'color': 'b'})  # 标出坐标
                o_x = _x
        plt.plot(n_min, [min_y] * len(n_min), View[0] + 'o')  # 画出一些点
        plt.plot(n_max, [max_y] * len(n_max), View[0] + 'o')  # 画出一些点
    addNews('绘制完毕')
    plt.legend()  # 显示图示
    plt.show()  # 显示图像
    return True


def Fucn_Cul_CSV():  # 添加函数

    global HS, HS_str, lb, x_I, Name_Input, View_C, View_Co, View_Input
    File = tkinter.filedialog.askopenfilename(
        title='载入表格', filetypes=[("CSV", ".csv")])
    view = View_Input.get().split('#')
    try:
        if view[0] not in View_Co:
            view[0] = 'b'
        v_2 = View_C.get(view[1], '-')
    except BaseException:
        view = ['', '']
        view[0] = random.choice(View_Co)
        v_2 = '-'
    V = view[0] + v_2
    try:
        addNews('读取CSV')
        read = pandas.read_csv(File)
        name = path.basename(File)[0:-4].replace(' ', '')
        if not name:
            name = random.randint(1, 1000)
        name += '(In CSV)'
        _HS = numpy.array(read).tolist()
        if len(_HS[0]) != len(_HS[1]):
            raise Exception
        HS_str.append(name)
        HS.append(HS_CSV(_HS, name, V))
        lb.delete(0, tkinter.END)
        lb.insert(tkinter.END, *HS)
        addNews('读取完毕')
    except BaseException:
        addNews('读取失败')


def Fucn_Cul():  # 添加函数
    global HS, HS_str, lb, x_I, Name_Input, View_C, View_Co, View_Input
    get = Func_Input.get().replace(' ', '')
    x_I = X_Input.get().split(',')
    name = Name_Input.get().replace(' ', '')
    view = View_Input.get().split('#')
    if not name:
        name = get
    try:
        if view[0] not in View_Co:
            view[0] = 'b'
        v_2 = View_C.get(view[1], '-')
    except BaseException:
        view = ['', '']
        view[0] = random.choice(View_Co)
        v_2 = '-'
    V = view[0] + v_2
    try:
        c = x_I[2]
        if c[0] == 'H':
            Name = {
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
            x_I[2] = eval(c[1:], Name)
    except BaseException:
        pass
    if get and get not in HS_str:
        HS_str.append(get)
        HS.append(HS_lambda(get, name, V, *x_I))
        lb.delete(0, tkinter.END)
        lb.insert(tkinter.END, *HS)
        addNews('函数生成完毕')
    else:
        addNews('函数生成失败')
        pass


def Fucn_Cul_Clear():  # 添加函数
    global HS, HS_str, lb, x_I, Name_Input, View_C, View_Co, View_Input
    if tkinter.messagebox.askokcancel('提示', '是否清空所有函数？)'):
        HS_str = []
        HS = []
        lb.delete(0, tkinter.END)
        addNews('函数清空完毕')


def Fucn_Numpy():  # 显示xy
    global HS, lb, Pr_BOX
    try:
        Fucn = HS[lb.curselection()[0]]
        Pr_BOX.delete(0, tkinter.END)
        Pr_BOX.insert(tkinter.END, *Fucn.returnList())
        addNews('表格创建成功')
    except BaseException:
        addNews('无法创建表格')
        pass


def Cul_Y_Clear():
    global Xcul_Input, lb, HS
    try:
        if tkinter.messagebox.askokcancel(
                '提示', f'确定删除{HS[lb.curselection()[0]]}的记忆吗？'):
            Y_cul.delete(0, tkinter.END)
            Fucn = HS[lb.curselection()[0]]
            Fucn.Clear_Memory()
            addNews('删除完毕')
        else:
            addNews('删除取消')
    except BaseException:
        addNews('删除失败')


def Cul_Y_YC():  # 显示xy
    global HS, Y_cul
    try:
        Fucn = HS[lb.curselection()[0]]
        Y_cul.delete(0, tkinter.END)
        Fucn.YC_On_Off()
        addNews('已清空卡槽')
    except BaseException:
        addNews('隐藏（显示）失败')


def Cul_Y_Check():  # 显示xy
    global HS, Y_cul
    try:
        Fucn = HS[lb.curselection()[0]]
        Y_cul.delete(0, tkinter.END)
        m_x, m_y = Fucn.getMemory()
        answer = []
        for i in range(len(m_x)):
            answer.append(f'x={m_x[i]} -> y={m_y[i]}')
        Y_cul.insert(tkinter.END, *answer)
        addNews('输出完成')
    except BaseException:
        addNews('操作失败')


def Fucn_XZ():
    global HS, lb, XZ_box
    try:
        addNews('预测过程程序可能无响应')
        Fucn = HS[lb.curselection()[0]]
        XZ_box.delete(0, tkinter.END)
        answer = Fucn.Nature(addNews)
        XZ_box.insert(tkinter.END, *answer)
        addNews('性质预测完成')
    except IndexError:
        addNews('性质预测失败')


def Cul_Y():
    global HS, Y_cul, Xcul_Input, lb
    try:
        addNews('计算过程程序可能无响应')
        Fucn = HS[lb.curselection()[0]]
        Y_cul.delete(0, tkinter.END)
        x = Xcul_Input.get().split(',')
        answer = Fucn.Cul_Y(x)
        Y_cul.insert(tkinter.END, *answer)
        addNews('系统计算完毕')
    except IndexError:
        addNews('计算失败')


def Fucn_Save():  # 导出CSV
    global CSV
    if not lb.curselection():
        return False
    try:
        Fucn = HS[lb.curselection()[0]]
        Fucn.Out()
        addNews('CSV导出成功')
    except BaseException:
        addNews('CSV导出失败')


def Fucn_Del():  # 删除函数
    global HS, HS_str, lb
    del_Fucn = lb.curselection()
    for i in del_Fucn:  # 只存在一项
        lb.delete(i)
        del HS[i]
        del HS_str[i]
        addNews('函数删除完毕')


def Find(x, y, in_y):
    m = []
    while True:  # 筛选求出最大值极值点
        try:
            num = y.index(in_y)
            m.append(x[num])
            del x[num]
            del y[num]
        except ValueError:
            break
    return m


def Cul_X():
    global HS, Y_cul, Ycul_Input, E_Input
    try:
        addNews('计算过程程序可能无响应')
        Fucn = HS[lb.curselection()[0]]  # 获取目标函数
        Y_cul.delete(0, tkinter.END)  # 清空
        y = Ycul_Input.get().split(',')  # 拆解输入
        E = E_Input.get().split('#')  # 拆解输入
        answer = []
        addNews('系统运算中')
        for i in y:
            answer += Fucn.Cul_dichotomy(float(i), *E)[0]
        if answer:
            addNews('系统运算完成')
            Y_cul.insert(tkinter.END, *answer)
        else:
            addNews('系统运算无结果')
    except BaseException:
        addNews('系统运算失败')
        Y_cul.delete(0, tkinter.END)


def Cul_X_TD():
    global HS, Y_cul, YTDcul_Input
    try:
        addNews('计算过程程序可能无响应')
        Fucn = HS[lb.curselection()[0]]  # 获取目标函数
        Y_cul.delete(0, tkinter.END)  # 清空
        E = YTDcul_Input.get().split('#')  # 拆解输入
        addNews('系统运算中')
        answer = Fucn.Iterative_method_Of_Huan(*E)
        if answer[1]:
            Y_cul.insert(tkinter.END, answer[0])
            addNews('系统运算完成')
        else:
            addNews('系统运算无结果')
    except BaseException:
        addNews('系统运算失败，请注意参数设置')
        Y_cul.delete(0, tkinter.END)


def addNews(News):
    global News_box, T
    T += 1
    News = str(News)
    News_box.insert(0, News + f'({T})')
    top.update()


def Fucn_DHS():
    global HS, lb, XZ_box, HS_str, x_I, Name_Input, View_C, View_Co, View_Input
    try:
        Fucn = HS[lb.curselection()[0]]
        DHS = Fucn.DHS
        if DHS is not None and str(DHS):
            get = str(DHS)
            HS_str.append(get)
            HS.append(
                HS_lambda(
                    get,
                    '(导)' +
                    Fucn.Func_Name +
                    ' Of ',
                    Fucn.View,
                    Fucn.start,
                    Fucn.end,
                    Fucn.kd,
                    Fucn.JD))
            lb.delete(0, tkinter.END)
            lb.insert(tkinter.END, *HS)
            addNews('函数生成完毕')
        else:
            raise Exception
    except BaseException:
        addNews('导函数创建失败')


def Func_Control():
    global top, FONT, View_C, View_Co, CSV, Func_Input, X_Input, Name_Input, View_Input, XK_Input, YK_Input, Xlim_Input, Ylim_Input
    global lb, Pr_BOX, Xcul_Input, Y_cul, HS, HS_str, Ycul_Input, E_Input, YTDcul_Input, XZ_box, News_box, T
    HS = []
    HS_str = []
    T = 0

    # 控制面板使用Tk实现
    top = tkinter.Tk()  # 设置屏幕
    top.title('CoTan函数测绘')
    top.resizable(width=False, height=False)
    top.geometry(f'+10+10')
    FONT = (r'Font\ZKST.ttf', 11)  # 设置字体
    rcParams['font.family'] = 'simhei'
    rcParams['axes.unicode_minus'] = False

    View_C = {'实线': '-',
              '短横线': '--',
              '点划线': '-,',
              '虚线': ':',
              '点标记': '.',
              '圆标记': 'o',
              '倒三角': 'v',
              '正三角': '^',
              '左三角': '&lt',
              '下箭头': '1',
              '上箭头': '2',
              '左箭头': '3',
              '右箭头': '4',
              '正方形': 's',
              '五边形': 'p',
              '星形': '*',
              '六边形': 'h',
              '六边形2': 'H',
              '+号': '+',
              'X标记': 'x', }  # 函数样式翻译表
    View_Co = ['g', 'r', 'c', 'm', 'y', 'k']
    CSV = []

    width_B = 12  # 标准宽度
    height_B = 1
    # column-水平方向，row-竖直方向
    # 设置解析式
    tkinter.Label(
        top,
        text='输入解析式：',
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=0,
        row=0)  # 设置说明
    Func_Input = tkinter.Entry(top, width=width_B * 2)
    Func_Input.grid(
        column=1,
        row=0,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    # 设置定义域
    tkinter.Label(
        top,
        font=FONT,
        text='定义域：',
        width=width_B,
        height=height_B).grid(
        column=0,
        row=1)  # 设置说明
    X_Input = tkinter.Entry(top, width=width_B * 2)
    X_Input.grid(column=1, row=1, columnspan=2, sticky=tkinter.E + tkinter.W)

    # 设置函数名字
    tkinter.Label(
        top,
        font=FONT,
        text='函数名字：',
        width=width_B,
        height=height_B).grid(
        column=0,
        row=2)  # 设置说明
    Name_Input = tkinter.Entry(top, width=width_B * 2)
    Name_Input.grid(
        column=1,
        row=2,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    # 设置函数图示
    tkinter.Label(
        top,
        font=FONT,
        text='函数样式：',
        width=width_B,
        height=height_B).grid(
        column=0,
        row=3)  # 设置说明
    View_Input = tkinter.Entry(top, width=width_B * 2)
    View_Input.grid(
        column=1,
        row=3,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y = 4  # 按钮统一纵坐标
    tkinter.Button(
        top,
        text='添加新函数',
        command=Fucn_Cul,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=0,
        row=a_y)  # 添加函数
    tkinter.Button(
        top,
        text='删除选中函数',
        command=Fucn_Del,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=1,
        row=a_y)  # 删除函数
    tkinter.Button(
        top,
        text='清除函数',
        command=Fucn_Cul_Clear,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=2,
        row=a_y)  # 绘制函数
    a_y += 1
    # 显示函数
    lb = tkinter.Listbox(top, width=width_B * 3 + 2)  # 暂时不启用多选
    TD_a_y = 10
    lb.grid(
        column=0,
        row=a_y,
        columnspan=3,
        rowspan=TD_a_y,
        sticky=tkinter.S +
        tkinter.N +
        tkinter.E +
        tkinter.W)
    a_y += TD_a_y
    tkinter.Label(
        top,
        font=FONT,
        text='',
        width=width_B,
        height=1).grid(
        column=0,
        row=a_y)

    tkinter.Label(
        top,
        font=FONT,
        text='',
        width=1).grid(
        column=4,
        row=0)  # 占用第四
    a_y = 0
    # 输入x函数求y值
    tkinter.Label(
        top,
        font=FONT,
        text='计算(y):',
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 设置说明
    Xcul_Input = tkinter.Entry(top, width=width_B * 2)
    Xcul_Input.grid(
        column=6,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    # 输入x函数求y值
    tkinter.Label(
        top,
        font=FONT,
        text='二分法计算(y):',
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 设置说明
    Ycul_Input = tkinter.Entry(top, width=width_B * 2)
    Ycul_Input.grid(
        column=6,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        font=FONT,
        text='二分法参数:',
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 设置说明
    E_Input = tkinter.Entry(top, width=width_B * 2)
    E_Input.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    # 输入x函数求y值
    tkinter.Label(
        top,
        font=FONT,
        text='梯度法计算(y):',
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 设置说明
    YTDcul_Input = tkinter.Entry(top, width=width_B * 2)
    YTDcul_Input.grid(
        column=6,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        top,
        text='计算(y)',
        command=Cul_Y,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 设置说明
    tkinter.Button(
        top,
        text='二分法计算(x)',
        command=Cul_X,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=6,
        row=a_y)
    tkinter.Button(
        top,
        text='梯度法计算(x)',
        command=Cul_X_TD,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=7,
        row=a_y)

    a_y += 1
    # 绘制函数坐标表格
    tkinter.Button(
        top,
        text='查看记忆',
        command=Cul_Y_Check,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)
    tkinter.Button(
        top,
        text='隐藏记忆',
        command=Cul_Y_YC,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=6,
        row=a_y)
    tkinter.Button(
        top,
        text='清空记忆',
        command=Cul_Y_Clear,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=7,
        row=a_y)

    a_y += 1
    # 显示函数
    Y_cul = tkinter.Listbox(top, width=width_B * 3 + 2, height=17)  # 暂时不启用多选
    Y_cul.grid(
        column=5,
        row=a_y,
        columnspan=3,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    a_y += 1
    # 设置坐标系刻度
    tkinter.Label(
        top,
        font=FONT,
        text='X轴(函数):',
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y,
        sticky=tkinter.N)  # 设置说明
    XK_Input = tkinter.Entry(top, width=width_B * 2)
    XK_Input.grid(
        column=6,
        row=a_y,
        columnspan=2,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    a_y += 1
    # 设置坐标系刻度
    tkinter.Label(
        top,
        font=FONT,
        text='Y轴(函数):',
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 设置说明
    YK_Input = tkinter.Entry(top, width=width_B * 2)
    YK_Input.grid(
        column=6,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    # 设置坐标系刻度
    tkinter.Label(
        top,
        font=FONT,
        text='X轴极限:',
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 设置说明
    Xlim_Input = tkinter.Entry(top, width=width_B * 2)
    Xlim_Input.grid(
        column=6,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    # 设置坐标系刻度
    tkinter.Label(
        top,
        font=FONT,
        text='Y轴极限:',
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 设置说明
    Ylim_Input = tkinter.Entry(top, width=width_B * 2)
    Ylim_Input.grid(
        column=6,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        top,
        text='绘制函数',
        command=Fucn_Draw,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=5,
        row=a_y)  # 绘制函数
    tkinter.Button(
        top,
        text='计算性质',
        command=Fucn_XZ,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=6,
        row=a_y)  # 绘制函数
    tkinter.Button(
        top,
        text='创建导函数',
        command=Fucn_DHS,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=7,
        row=a_y)  # 绘制函数
    a_y += 1
    XZ_box = tkinter.Listbox(top, width=width_B * 3 + 2, height=10)  # 暂时不启用多选
    XZ_box.grid(
        column=5,
        row=a_y,
        columnspan=3,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    a_y += 1
    News_box = tkinter.Listbox(top, width=width_B * 3 + 2, height=5)  # 暂时不启用多选
    News_box.grid(
        column=5,
        row=a_y,
        columnspan=3,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    tkinter.Label(
        top,
        font=FONT,
        text='',
        width=1).grid(
        column=8,
        row=a_y)  # 占用第四
    a_y = 0

    # 绘制函数坐标表格
    tkinter.Button(
        top,
        text='导入表格',
        command=Fucn_Cul_CSV,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=9,
        row=a_y)
    tkinter.Button(
        top,
        text='生成表格',
        command=Fucn_Numpy,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=10,
        row=a_y)
    tkinter.Button(
        top,
        text='导出表格',
        command=Fucn_Save,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=11,
        row=a_y)

    a_y += 1
    # 显示函数的xy
    Pr_BOX = tkinter.Listbox(top, width=width_B * 3 + 2)  # 暂时不启用多选
    Pr_BOX.grid(
        column=9,
        row=a_y,
        columnspan=3,
        rowspan=TD_a_y +
        4,
        sticky=tkinter.S +
        tkinter.N +
        tkinter.E +
        tkinter.W)

    addNews('加载完成，欢迎使用!')
    top.mainloop()
