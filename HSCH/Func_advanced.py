from __future__ import division  # 让/恢复为除法
import sympy
from matplotlib import pyplot as plt
from matplotlib import rcParams
import tkinter
import tkinter.messagebox
import random
from New_TK import DragWindow
from matplotlib.animation import FuncAnimation
from HSCH.HS import HS_lambda as HS_L
import numpy as np


def type_selection(IN, si=float, n=True):  # Float筛选系统
    x = []
    for i in IN:
        try:
            if si(i) == si(0) and n:
                continue
            x.append(si(i))
        except ValueError:
            pass
    return x


def save_to_csv():  # 导出CSV
    try:
        succ = HS.Out()  # 是否成功
        if not succ:
            raise Exception
        output_prompt('CSV导出成功')
    except BaseException:
        output_prompt('CSV导出失败')


def to_sheet():  # 生成表格
    global HS, Pr_BOX
    try:
        Pr_BOX.delete(0, tkinter.END)
        Pr_BOX.insert(tkinter.END, *HS.returnList())
        output_prompt('表格创建成功')
    except BaseException:
        output_prompt('无法创建表格')


def sympy_computing(c) -> tuple:
    try:
        Name = {
            'Pi': sympy.pi,
            'e': sympy.E,
            'log': sympy.log,
            'sin': sympy.sin,
            'cos': sympy.cos,
            'tan': sympy.tan,
            'cot': lambda x: 1 / sympy.tan(x),
            'csc': lambda x: 1 / sympy.sin(x),
            'sec': lambda x: 1 / sympy.cos(x),
            'sinh': sympy.sinh,
            'cosh': sympy.cosh,
            'tanh': sympy.tanh,
            'asin': sympy.asin,
            'acos': sympy.acos,
            'atan': sympy.atan}
        ans = eval(c, Name)
        return ans, True
    except BaseException:
        return None, False

# 确认表达式被正确计算
def confirmation_expression(c):
    get = sympy_computing(c)
    if not get[1]:
        return c
    return get[0]


def check_center_of_symmetry():
    global HS, YC_Input, YC_BOX, XZ_JD
    a, must = sympy_computing(XZ_JD.get())
    try:
        G = HS.Check_Center_of_symmetry(confirmation_expression(YC_Input.get()), output_prompt, a)
        if G[1]:
            YC_BOX.insert(tkinter.END, G[1])
            output_prompt('预测完成')
        else:
            raise Exception
    except BaseException:
        output_prompt('预测失败')


def check_symmetry_axis():
    global HS, YC_Input, YC_BOX, XZ_JD
    a, must = sympy_computing(XZ_JD.get())
    try:
        G = HS.Check_Symmetry_axis(confirmation_expression(YC_Input.get()), output_prompt, a)
        if G[1]:
            YC_BOX.insert(tkinter.END, G[1])
            output_prompt('预测完成')
        else:
            raise Exception
    except BaseException:
        output_prompt('预测失败')


def check_periodic():
    global HS, YC_Input, YC_BOX, XZ_JD
    a, must = sympy_computing(XZ_JD.get())
    try:
        G = HS.Check_Periodic(confirmation_expression(YC_Input.get()), output_prompt, a)
        if G[1]:
            YC_BOX.insert(tkinter.END, G[1])
            output_prompt('预测完成')
        else:
            raise Exception
    except BaseException:
        output_prompt('预测失败')


def check_monotonic():
    global HS, YC_Input, YC_BOX, XZ_JD
    a, must = sympy_computing(XZ_JD.get())
    try:
        G = HS.Check_Monotonic(YC_Input.get(), output_prompt, a)
        if G[1]:
            YC_BOX.insert(tkinter.END, G[1])
            output_prompt('预测完成')
        else:
            raise Exception
    except BaseException:
        output_prompt('预测失败')


def clear_memory():
    global HS
    try:
        if tkinter.messagebox.askokcancel('提示', f'确定删除{HS}的记忆吗？'):
            R_cul.delete(0, tkinter.END)
            HS.Clear_Memory()
            output_prompt('删除完毕')
        else:
            output_prompt('删除取消')
    except BaseException:
        output_prompt('删除失败')


def show_hidden_memory():  # 显示xy
    global HS, R_cul
    try:
        R_cul.delete(0, tkinter.END)
        HS.YC_On_Off()
        output_prompt('已清空卡槽')
    except BaseException:
        output_prompt('隐藏（显示）失败')


def show_memory():  # 显示xy
    global HS, R_cul
    try:
        Fucn = HS[lb.curselection()[0]]
        R_cul.delete(0, tkinter.END)
        m_x, m_y = Fucn.getMemory()
        answer = []
        for i in range(len(m_x)):
            answer.append(f'x={m_x[i]} -> y={m_y[i]}')
        R_cul.insert(tkinter.END, *answer)
        output_prompt('输出完成')
    except BaseException:
        output_prompt('操作失败')


def gradient_method_calculation():
    global HS, Xcul_TD_Input, Xcul_TD_CS, R_cul
    try:
        output_prompt('计算过程程序可能无响应')
        R_cul.delete(0, tkinter.END)  # 清空
        E = []
        for i in Xcul_TD_CS:
            E.append(i.get())
        output_prompt('系统运算中')
        answer = HS.Iterative_method_Of_Huan(Xcul_TD_Input.get(), *E)
        if answer[1] is not None:
            R_cul.insert(tkinter.END, answer[0])
            output_prompt('系统运算完成')
        else:
            output_prompt('系统运算无结果')
    except BaseException:
        output_prompt('系统运算失败，请注意参数设置')


def calculate():
    global Ycul_Input, HS, R_cul
    try:
        output_prompt('计算过程程序可能无响应')
        R_cul.delete(0, tkinter.END)
        x = Ycul_Input.get().split(',')
        answer = HS.Cul_Y(x)
        if answer != []:
            R_cul.insert(tkinter.END, *answer)
            output_prompt('系统运算完毕')
        else:
            output_prompt('系统运算无结果')
    except BaseException:
        output_prompt('计算失败')


def sympy_calculation_x():
    global Xcul_DS_Input, HS, R_cul
    try:
        output_prompt('计算过程程序可能无响应')
        R_cul.delete(0, tkinter.END)
        x = Xcul_DS_Input.get().split(',')
        answer = []
        for i in x:
            answer += HS.Sympy_Cul(i)[0]
        if answer != []:
            R_cul.insert(tkinter.END, *answer)
            output_prompt('系统运算完毕')
        else:
            output_prompt('系统运算无结果')
    except BaseException:
        output_prompt('计算失败')


def function_differentiation():
    global DScul_Input, HS, R_cul, DScul_JD_Input
    try:
        output_prompt('计算过程程序可能无响应')
        R_cul.delete(0, tkinter.END)
        x = DScul_Input.get().split(',')
        JD = DScul_JD_Input.get()
        answer = []
        for i in x:
            get = HS.Sympy_DHS(i, JD)[0]
            if get is not None:
                answer.append(get)
        if answer != []:
            R_cul.insert(tkinter.END, *answer)
            output_prompt('系统运算完毕')
        else:
            output_prompt('系统运算无结果')
    except IndexError:
        output_prompt('计算失败')


def approximation():# 逼近法
    global DScul_Input, HS, R_cul, DScul_JD_Input
    try:
        output_prompt('计算过程程序可能无响应')
        R_cul.delete(0, tkinter.END)
        x = DScul_Input.get().split(',')
        JD = DScul_JD_Input.get()
        answer = []
        for i in x:
            get = HS.Sympy_DHS(i, JD, True)[0]
            if get is not None:
                answer.append(get)
        if answer != []:
            R_cul.insert(tkinter.END, *answer)
            output_prompt('系统运算完毕')
        else:
            output_prompt('系统运算无结果')
    except IndexError:
        output_prompt('计算失败')


def dichotomy():# 二分法
    global Xcul_Input, Xcul_CS, HS, R_cul
    try:
        output_prompt('计算过程程序可能无响应')
        R_cul.delete(0, tkinter.END)  # 清空
        y = Xcul_Input.get().split(',')  # 拆解输入
        E = [100, 0.0001, 0.1, 0.5, False, True, 1000, 0.1, 0.1, False, None]
        for i in range(11):
            try:
                if i in (4, 5, 9):
                    a = Xcul_CS[i].get()
                else:
                    a = float(Xcul_CS[i].get())
                E[i] = a
            except BaseException:
                pass
        answer = []
        output_prompt('系统运算中')
        for i in y:
            try:
                answer += HS.Cul_dichotomy(float(i), *E)[0]
            except BaseException:
                pass
        if answer:
            output_prompt('系统运算完成')
            R_cul.insert(tkinter.END, *answer)
        else:
            output_prompt('系统运算无结果')
    except BaseException:
        output_prompt('系统运算失败')


def property_prediction():
    global HS, lb, XZ_BOX, XZ_JD
    try:
        a, must = sympy_computing(XZ_JD.get())
        output_prompt('预测过程程序可能无响应')
        XZ_BOX.delete(0, tkinter.END)
        answer = HS.Nature(output_prompt, True, a, must)
        XZ_BOX.insert(tkinter.END, *answer)
        output_prompt('性质预测完成')
    except IndexError:
        output_prompt('性质预测失败')


def function_drawing():
    global XZ_Input, XZstart_Input, XZend_Input, XZkd_Input, YZ_Input, YZstart_Input, YZend_Input, YZkd_Input
    global Xlimstart_Input, Xlimend_Input, Ylimstart_Input, Ylimend_Input
    global HS, fig, Point_Draw, Best_Draw, Test_Draw, Draw_BOX, ZL_Input
    try:
        Draw_Type = Draw_BOX.curselection()[0]
    except BaseException:
        Draw_Type = 0
    # 画板创造
    output_prompt('生成绘制取...')
    fig = plt.figure(num='CoTan函数')  # 定义一个图像窗口
    if Draw_Type in (0, 1, 2, 3, 8, 9):
        plt.grid(True, ls='--')  # 显示网格(不能放到后面，因为后面调整成为了笛卡尔坐标系)
    ax = plt.gca()

    def init():
        if Draw_Type in (0, 2, 4, 6, 8):
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            ax.spines['bottom'].set_position(('data', 0))  # 设置x轴, y轴在(0, 0)的位置
            ax.spines['left'].set_position(('data', 0))
        # 检测x
        try:
            if XZ_Input.get()[0] == 'c':  # 如果输入函数cx#-10#10#1#1
                _HS = [
                    XZ_Input.get()[
                        1:],
                    XZstart_Input.get(),
                    XZend_Input.get(),
                    XZkd_Input.get(),
                    2]  # 第一部分HS，第二部分S，第三部分E，第四部分KD，第五部分JD
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
                x = type_selection(
                    HS_L(
                        _HS[0],
                        'x',
                        '',
                        _HS[1],
                        _HS[2],
                        _HS[3],
                        _HS[4]).Cul()[1])  # 取y
                ax.set_xticks(x)
            elif XZ_Input.get()[0] == 'y':  # 输入函数y
                # 不错要错误捕捉，外围有个大的捕捉
                x = abs(int(XZstart_Input.get()))
                x_major_locator = plt.MultipleLocator(x)
                ax.xaxis.set_major_locator(x_major_locator)
            else:  # 输入纯数字
                x = type_selection(XZ_Input.get().split(','))
                ax.set_xticks(x)
        except BaseException:
            x_major_locator = plt.MultipleLocator(2)
            ax.xaxis.set_major_locator(x_major_locator)
        # 检测y
        try:  # 意外捕捉
            if YZ_Input.get()[0] == 'c':  # 如果输入函数cx#-10#10#1#1
                _HS = [
                    YZ_Input.get()[
                        1:],
                    YZstart_Input.get(),
                    YZend_Input.get(),
                    YZkd_Input.get(),
                    2]  # 第一部分HS，第二部分S，第三部分E，第四部分KD，第五部分JD
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
                y = type_selection(
                    HS_L(
                        _HS[0],
                        'y',
                        '',
                        _HS[1],
                        _HS[2],
                        _HS[3],
                        _HS[4]).Cul()[1])  # 取y
                ax.set_yticks(y)
            elif YZ_Input.get()[0] == 'y':  # 输入函数y
                y = abs(int(YZstart_Input.get()))
                y_major_locator = plt.MultipleLocator(y)
                ax.yaxis.set_major_locator(y_major_locator)
            else:
                y = type_selection(YZ_Input.get().split(','))
                ax.set_yticks(y)
        except BaseException:
            y_major_locator = plt.MultipleLocator(2)
            ax.yaxis.set_major_locator(y_major_locator)
        # 极限设计
        try:
            xlim_IN = type_selection(
                [Xlimstart_Input.get(), Xlimend_Input.get()], si=int, n=False)
            ylim_IN = type_selection(
                [Ylimstart_Input.get(), Ylimend_Input.get()], si=int, n=False)
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
        ax.set_xlim(_xlim)
        ax.set_ylim(_ylim)
        global text_x, text_y
        text_x = _xlim[0] + abs(_xlim[0]) * 0.01
        text_y = _ylim[1] - abs(_ylim[1]) * 0.01
    init()
    # 函数绘图系统
    output_prompt('图像绘制中...')
    if HS is None:
        return False
    if Draw_Type in (0, 1, 4, 5):
        # 绘制曲线
        get = HS.Draw_Cul()
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
        # 绘制记忆点
        get = HS.getMemory()
        m_x = get[0]
        m_y = get[1]
        max_x, max_y, min_x, min_y = HS.Best_value()
        if Point_Draw.get():
            plt.plot(
                m_x,
                m_y,
                View[0] + 'o',
                label=f'Point of {Func_label}')  # 画出一些点
            len_x = sorted(list(set(m_x)))  # 去除list重复项目
            JZD = max_x + min_x

            if Test_Draw.get():
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
        if Best_Draw.get():
            o_x = None
            n_max = []
            for i in range(len(max_x)):  # 画出最大值
                _x = max_x[i]
                if o_x is None or abs(_x - o_x) >= 1:  # 确保位置
                    if Test_Draw.get():
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
                    if Test_Draw.get():
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
        plt.legend()  # 显示图示
    elif Draw_Type in (8, 9):
        get = HS.Cul()
        x = get[0]
        y = get[1]
        l = len(x)
        global xdata, ydata
        xdata = []
        ydata = []
        Func_label = get[2]
        View = get[3]
        ln = ax.plot([], [], View, label=Func_label, animated=False)[0]
        text = plt.text(
            text_x, text_y, '', fontdict={
                'size': '10', 'color': 'b'})

        def _init():
            init()
            return ln, text

        def update(n):
            global xdata, ydata
            if n == 0:
                xdata = []
                ydata = []
            xdata.append(x[n])
            ydata.append(y[n])
            text.set_text(f'x={x[n]},y={y[n]}')
            ln.set_data(xdata, ydata)
            return ln, text
        try:  # 自定义帧率
            ZL = int(ZL_Input.get())
        except BaseException:
            ZL = 100
        ani = FuncAnimation(
            fig,
            update,
            frames=l,
            init_func=_init,
            interval=ZL,
            blit=False,
            repeat_delay=3000)  # 动态绘图
    elif Draw_Type in (2, 3, 6, 7):
        text = plt.text(
            text_x, text_y, '', fontdict={
                'size': '10', 'color': 'b'})
        HS_List = HS.Return_Son()
        pr_List = []
        l = len(HS_List)
        m = []  # 每个群组中fx分类的个数
        for i in HS_List:  # 预先生成函数
            output_prompt(f'迭代计算中...(共{l}次)')
            get = i.Draw_Cul()
            m.append(len(get[0]))
            pr_List.append(get)
        pr_List += pr_List[::-1]
        ln_list = [text]
        for i in range(max(m)):
            ln_list.append(
                ax.plot(
                    [],
                    [],
                    pr_List[0][3],
                    animated=False)[0])  # 创建足够的i
        l = len(pr_List)

        def _init():
            init()
            text.set_text('')
            return None

        def update(n):
            get = pr_List[n - 1]
            ln_list[0].set_text(get[2])
            for i in range(max(m)):
                try:
                    x = get[0][i]
                    y = get[1][i]
                    ln_list[i + 1].set_data(x, y)
                except BaseException:
                    ln_list[i + 1].set_data([], [])
            return ln_list
        try:  # 自定义帧率
            ZL = int(ZL_Input.get())
        except BaseException:
            ZL = 100
        ani = FuncAnimation(
            fig,
            update,
            frames=l,
            init_func=_init,
            interval=ZL,
            blit=False)  # 动态绘图
    output_prompt('绘制完毕')
    plt.show()  # 显示图像
    return True


def set_function():
    global Func_Input, start_Input, end_Input, kd_Input, JD_Input, FuncName_Input, FuncView_Input, View_C, View_Co, HS, top
    global a_MR, a_start, a_end, a_kd
    getHS = Func_Input.get().replace(' ', '')
    if getHS == '':
        output_prompt('应用失败')
        return None
    X_I = [-10, 10, 0.1, 2, 1, -10, 10, 1]
    get = [
        start_Input,
        end_Input,
        kd_Input,
        JD_Input,
        a_MR,
        a_start,
        a_end,
        a_kd]
    # 参数的处理
    try:
        c = kd_Input.get().replace(' ', '')
        if c[0] == 'H':
            Name = {
                'Pi': sympy.pi,
                'e': sympy.E,
                'log': sympy.log,
                'sin': sympy.sin,
                'cos': sympy.cos,
                'tan': sympy.tan,
                'cot': lambda x: 1 / sympy.tan(x),
                'csc': lambda x: 1 / sympy.sin(x),
                'sec': lambda x: 1 / sympy.cos(x),
                'sinh': sympy.sinh,
                'cosh': sympy.cosh,
                'tanh': sympy.tanh,
                'asin': sympy.asin,
                'acos': sympy.acos,
                'atan': sympy.atan}
            kd = eval(c[1:], Name)
        else:
            raise Exception
    except BaseException:
        kd = None
    for i in range(8):
        try:
            a = float(get[i].get())
            X_I[i] = a
        except BaseException:
            pass
    if kd is not None:
        X_I[2] = kd

    # View的处理
    view = FuncView_Input.get().split('#')
    try:
        if view[0] not in View_Co:
            view[0] = 'b'
        v_2 = View_C.get(view[1], '-')
    except BaseException:
        view = ['', '']
        view[0] = random.choice(View_Co)
        v_2 = '-'
    V = view[0] + v_2
    # Name的处理
    name = FuncName_Input.get().replace(' ', '')
    if name == '':
        name = getHS
    try:
        HS = HS_L(getHS, name, V, *X_I, c_Son=True)
        output_prompt('应用成功')
        top.title(f'CoTan函数工厂  {HS}')
    except BaseException:
        output_prompt('应用失败')


def output_prompt(News):
    global News_BOX, T, top
    T += 1
    News = str(News)
    News_BOX.insert(0, News + f'({T})')
    top.update()


def function_factory_main():  # H_S-默认函数GF-关闭时询问返回函数
    global View_C, View_Co, HS, T, top
    HS = None
    T = 0
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

    # top = tkinter.Tk()  # 设置屏幕
    top = DragWindow()
    bg = '#FFFAFA'  # 主颜色
    bbg = '#FFFAFA'  # 按钮颜色
    fg = '#000000'  # 文字颜色
    top["bg"] = bg
    top.title('CoTan函数工厂')
    top.resizable(width=False, height=False)
    top.geometry('+10+10')
    FONT = (r'Font\ZKST.ttf', 11)  # 设置字体
    rcParams['font.family'] = 'simhei'
    rcParams['axes.unicode_minus'] = False

    width_B = 13  # 标准宽度
    height_B = 2
    a_y = 0
    a_x = 1
    global Func_Input, start_Input, end_Input, kd_Input, JD_Input, FuncName_Input, FuncView_Input
    tkinter.Label(
        top,
        text='输入解析式:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Func_Input = tkinter.Entry(top, width=width_B * 2)
    Func_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='定义域前端点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    start_Input = tkinter.Entry(top, width=width_B * 2)
    start_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='定义域后端点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    end_Input = tkinter.Entry(top, width=width_B * 2)
    end_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='函数绘制跨度:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    kd_Input = tkinter.Entry(top, width=width_B * 2)
    kd_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='函数计算精度:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    JD_Input = tkinter.Entry(top, width=width_B * 2)
    JD_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='函数名字:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    FuncName_Input = tkinter.Entry(top, width=width_B * 2)
    FuncName_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='函数视图:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    FuncView_Input = tkinter.Entry(top, width=width_B * 2)
    FuncView_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    global a_MR, a_start, a_end, a_kd

    a_y += 1
    tkinter.Label(
        top,
        text='常量a默认值:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    a_MR = tkinter.Entry(top, width=width_B * 2)
    a_MR.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='常量a起点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    a_start = tkinter.Entry(top, width=width_B * 2)
    a_start.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='常量a终点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    a_end = tkinter.Entry(top, width=width_B * 2)
    a_end.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='常量a跨度:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    a_kd = tkinter.Entry(top, width=width_B * 2)
    a_kd.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='应用函数',
        command=set_function,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)  # 添加函数
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='绘制图像',
        command=function_drawing,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='性质预测',
        command=property_prediction,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)  # 添加函数

    global XZ_BOX, XZ_JD

    a_y += 1
    tkinter.Label(
        top,
        text='预测精度:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    XZ_JD = tkinter.Entry(top, width=width_B * 2)
    XZ_JD.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    # 显示函数的xy
    XZ_BOX = tkinter.Listbox(top, width=width_B * 3)  # 暂时不启用多选
    XZ_BOX.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=9,
        sticky=tkinter.S +
        tkinter.N +
        tkinter.E +
        tkinter.W)

    a_x += 3
    tkinter.Label(
        top,
        text='',
        bg=bg,
        fg=fg,
        font=FONT,
        width=1).grid(
        column=a_x,
        row=0)  # 设置说明

    # 第二排的开始
    global XZ_Input, XZstart_Input, XZend_Input, XZkd_Input, YZ_Input, YZstart_Input, YZend_Input, YZkd_Input
    global Xlimstart_Input, Xlimend_Input, Ylimstart_Input, Ylimend_Input
    a_x += 1
    a_y = 0
    tkinter.Label(
        top,
        text='X轴刻度声明:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    XZ_Input = tkinter.Entry(top, width=width_B * 2)
    XZ_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='X轴刻度起点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    XZstart_Input = tkinter.Entry(top, width=width_B * 2)
    XZstart_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='X轴刻度终点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    XZend_Input = tkinter.Entry(top, width=width_B * 2)
    XZend_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='X轴刻度间隔:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    XZkd_Input = tkinter.Entry(top, width=width_B * 2)
    XZkd_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='Y轴刻度声明:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    YZ_Input = tkinter.Entry(top, width=width_B * 2)
    YZ_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='Y轴刻度起点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    YZstart_Input = tkinter.Entry(top, width=width_B * 2)
    YZstart_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='Y轴刻度终点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    YZend_Input = tkinter.Entry(top, width=width_B * 2)
    YZend_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='Y轴刻度间隔:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    YZkd_Input = tkinter.Entry(top, width=width_B * 2)
    YZkd_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='X轴显示起点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Xlimstart_Input = tkinter.Entry(top, width=width_B * 2)
    Xlimstart_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='X轴显示终点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Xlimend_Input = tkinter.Entry(top, width=width_B * 2)
    Xlimend_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='Y轴显示起点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Ylimstart_Input = tkinter.Entry(top, width=width_B * 2)
    Ylimstart_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='Y轴显示终点:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Ylimend_Input = tkinter.Entry(top, width=width_B * 2)
    Ylimend_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    global ZL_Input
    a_y += 1
    tkinter.Label(
        top,
        text='帧率(帧/ms):',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    ZL_Input = tkinter.Entry(top, width=width_B * 2)
    ZL_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    global Point_Draw, Best_Draw, Test_Draw
    a_y += 1
    Point_Draw = tkinter.IntVar()
    Best_Draw = tkinter.IntVar()
    Test_Draw = tkinter.IntVar()

    tkinter.Checkbutton(
        top,
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        selectcolor=bg,
        text="显示记忆点",
        variable=Point_Draw).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Checkbutton(
        top,
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        selectcolor=bg,
        text="显示最值",
        variable=Best_Draw).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Checkbutton(
        top,
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        selectcolor=bg,
        text="显示文字",
        variable=Test_Draw).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    global News_BOX, Draw_BOX
    a_y += 1
    # 显示函数的xy
    Draw_BOX = tkinter.Listbox(
        top,
        width=width_B *
        3,
        height=height_B *
        4)  # 暂时不启用多选
    Draw_BOX.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=3,
        sticky=tkinter.S +
        tkinter.N +
        tkinter.E +
        tkinter.W)
    Draw_BOX.insert(tkinter.END,
                    *['笛卡尔坐标系静态图像(默认)',
                      '矩形坐标系静态图像',
                      '笛卡尔坐标系动态图像',
                      '矩形坐标系动态图像',
                      '笛卡尔坐标系静态图像(无线框)',
                      '矩形坐标系静态图像(无线框)',
                      '笛卡尔坐标系动态图像(无线框)',
                      '矩形坐标系动态图像(无线框)',
                      '笛卡尔坐标系动态画图',
                      '矩形坐标系动态画图'])
    a_y += 3
    # 显示函数的xy
    News_BOX = tkinter.Listbox(
        top,
        width=width_B *
        3,
        height=height_B *
        2)  # 暂时不启用多选
    News_BOX.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=2,
        sticky=tkinter.S +
        tkinter.N +
        tkinter.E +
        tkinter.W)

    a_x += 3
    tkinter.Label(
        top,
        text='',
        bg=bg,
        fg=fg,
        font=FONT,
        width=1).grid(
        column=a_x,
        row=0)  # 设置说明

    global Ycul_Input, Xcul_Input, Xcul_CS, Xcul_TD_Input, Xcul_TD_CS, R_cul
    a_x += 1
    a_y = 0
    tkinter.Label(
        top,
        text='计算(y):',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Ycul_Input = tkinter.Entry(top, width=width_B * 2)
    Ycul_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='二分法计算(x):',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Xcul_Input = tkinter.Entry(top, width=width_B * 2)
    Xcul_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    Xcul_CS = []  # 二分法参数输入
    name_List = [
        '最大迭代数',
        '计算精度',
        '最值允许偏移量',
        '零点最小间隔',
        '减少计算',
        '允许梯度计算',
        '最大扩张深度',
        '扩张限制',
        '扩张偏移量',
        '开启二级验证',
        '二级验证程度']
    for i in range(11):
        a_y += 1
        Xcul_CS.append(tkinter.StringVar())
        tkinter.Label(
            top,
            bg=bg,
            fg=fg,
            text=name_List[i] + ':',
            font=FONT,
            width=width_B,
            height=height_B).grid(
            column=a_x,
            row=a_y)  # 设置说明
        tkinter.Entry(top,
                      width=width_B * 2,
                      textvariable=Xcul_CS[-1]).grid(column=a_x + 1,
                                                     row=a_y,
                                                     columnspan=2,
                                                     sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='梯度法计算(x):',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Xcul_TD_Input = tkinter.Entry(top, width=width_B * 2)
    Xcul_TD_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    Xcul_TD_CS = []  # 梯度法法参数输入
    name_List = ['梯度起点', '梯度终点', '计算深度', '计算精度']
    for i in range(4):
        a_y += 1
        Xcul_TD_CS.append(tkinter.StringVar())
        tkinter.Label(
            top,
            bg=bg,
            fg=fg,
            text=name_List[i] + ':',
            font=FONT,
            width=width_B,
            height=height_B).grid(
            column=a_x,
            row=a_y)  # 设置说明
        tkinter.Entry(top,
                      width=width_B * 2,
                      textvariable=Xcul_TD_CS[-1]).grid(column=a_x + 1,
                                                        row=a_y,
                                                        columnspan=2,
                                                        sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='',
        bg=bg,
        fg=fg,
        height=1).grid(
        column=1,
        row=a_y)  # 底部

    a_x += 3
    tkinter.Label(
        top,
        text='',
        bg=bg,
        fg=fg,
        font=FONT,
        width=1).grid(
        column=a_x,
        row=0)  # 设置说明

    global Xcul_DS_Input, DScul_Input, DScul_JD_Input

    a_x += 1
    a_y = 0

    tkinter.Label(
        top,
        text='代数法计算(x):',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    Xcul_DS_Input = tkinter.Entry(top, width=width_B * 2)
    Xcul_DS_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='求(x)导数:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    DScul_Input = tkinter.Entry(top, width=width_B * 2)
    DScul_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        top,
        text='逼近求导精度:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    DScul_JD_Input = tkinter.Entry(top, width=width_B * 2)
    DScul_JD_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='计算(y)',
        command=calculate,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)  # 设置说明
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='二分法计算(x)',
        command=dichotomy,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x + 1,
        row=a_y)
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='梯度法计算(x)',
        command=gradient_method_calculation,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x + 2,
        row=a_y)

    a_y += 1
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='代数法计算',
        command=sympy_calculation_x,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='逼近法导数计算',
        command=approximation,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='导数计算',
        command=function_differentiation,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    a_y += 1
    k = 5
    R_cul = tkinter.Listbox(top, height=height_B * (k - 1))  # 暂时不启用多选
    R_cul.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=k,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    global YC_Input, YC_BOX
    a_y += k - 1
    tkinter.Label(
        top,
        text='性质预测值:',
        bg=bg,
        fg=fg,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.N +
        tkinter.S)  # 设置说明
    YC_Input = tkinter.Entry(top, width=width_B * 2)
    YC_Input.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='周期性',
        command=check_periodic,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='对称轴',
        command=check_symmetry_axis,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='对称中心',
        command=check_center_of_symmetry,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='单调性',
        command=check_monotonic,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    a_y += 1
    # 显示函数的xy
    YC_BOX = tkinter.Listbox(
        top,
        width=width_B *
        3,
        height=height_B *
        5)  # 暂时不启用多选
    YC_BOX.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=6,
        sticky=tkinter.S +
        tkinter.N +
        tkinter.E +
        tkinter.W)

    a_x += 3
    tkinter.Label(
        top,
        text='',
        bg=bg,
        fg=fg,
        font=FONT,
        width=1).grid(
        column=a_x,
        row=0)  # 设置说明

    a_x += 1
    a_y = 0
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='生成表格',
        command=to_sheet,
        font=FONT,
        width=width_B * 2,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        columnspan=2)
    tkinter.Button(
        top,
        bg=bbg,
        fg=fg,
        text='导出表格',
        command=save_to_csv,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x + 2,
        row=a_y)

    global Pr_BOX
    a_y += 1
    # 显示函数的xy
    Pr_BOX = tkinter.Listbox(top, width=width_B * 3)  # 暂时不启用多选
    Pr_BOX.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=17,
        sticky=tkinter.S +
        tkinter.N +
        tkinter.E +
        tkinter.W)

    output_prompt('加载完毕')
    tkinter.mainloop()
