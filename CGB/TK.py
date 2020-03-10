from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile
import tkinter.messagebox
from CGB import TK_HS

help_doc = '''
*快捷键：
    d-不用点击左键画线（再次点击关闭）
    g-画直线（2）
    f-画填充矩阵3
    s-画矩阵边框4
    k-画横线5
    l-画竖线6
    j-画多段线7
    i-横线多段线打点（再次点击结束绘制）8
    u-竖线多段线打点（再次点击结束绘制）9
    h-横线和竖线多段线打点并由虚线标注（再次点击结束绘制）10
    q-绘制虚线11
    c-绘制填充圆形12
    v-绘制圆形边框（13）
    n和m-绘制多边形（14）
    n-再次点击完成填充多边形绘制（14）
    m-再次点击完成多边形边框绘制（14）
    o-捕捉坐标原点（请先点击功能快捷键）
    x-捕捉坐标x轴（请先点击功能快捷键并选择起点）
    y-捕捉坐标y轴（同上）
    b-关闭当前所有快捷键操作
    e-绘制填充椭圆（15）
    r-绘制椭圆边框（16）
    w-再次保存（前提是现在工具箱点击过一次保存）
*鼠标操作：
    左键-按下画曲线
    中键-快捷键启动后，用于选择点
    右键-打开工具箱
*视图
    顶部-显示鼠标坐标，按键点击模式，笔的大小，坐标系位置和颜色系统以及坐标系原点的位置（处于快捷键状态时，显示中键当前选择了的点）
    底部-显示当前时间（处于快捷键状态时，显示快捷键提示mod:yes None xxx,其中yes表示快捷键d启动，None表示快捷键注释，xxx表示快捷功能解释）
*工具箱操作：
    选择颜色-画线颜色
    选择增函数颜色-绘制函数时增函数颜色
    选择减函数颜色-绘制函数时减函数颜色
    选择笔的大小（刷子）-画线的粗细
    清空-清空所有笔记并可以选择新的背景颜色
    绘制坐标系-三点绘制坐标系（使用中键选择点）
    保存-保存笔记为图片格式，保存一次后快捷键w可重复保存
    绘制函数-绘制基本初等函数和字定义解析函数
'''


def increasing_func_color():
    global ZColo
    ZColo = askcolor(title='选择颜色')[0]


def subtraction_func_color():
    global JColo
    JColo = askcolor(title='选择颜色')[0]


def select_color():
    global colo
    colo = askcolor(title='选择颜色')[0]


def choose_save():
    global BC
    BC = tkinter.filedialog.asksaveasfilename(
        title='选择保存位置', filetypes=[("PNG", ".png")])
    if not BC:
        BC = None
    else:
        BC += '.png'


def choose_open():
    global BG_IM
    BG_IM = tkinter.filedialog.askopenfilename(
        title='选择载入图片', filetypes=[
            ("PNG", ".png"), ("JPG", ".jpg")])
    if not BG_IM:
        BG_IM = None


def switch_brush():
    global d
    if tkinter.messagebox.askokcancel('提示', '要切换到刷子吗（可当橡皮使用）'):
        d = 10


def switch_big():
    global d
    if tkinter.messagebox.askokcancel('提示', '要切换到大笔吗'):
        d = 3


def Set_d():
    global d, d_Input
    Input = d_Input.get().replace(' ', '')
    try:
        Input = int(Input)
        if tkinter.messagebox.askokcancel('提示', f'是否设定大小为{Input}(系统默认大小为：2)'):
            d = Input
    except BaseException:
        if tkinter.messagebox.askokcancel('提示', '设置失败，是否要切换到中笔吗'):
            d = 2


def switch_stroke():
    global d
    if tkinter.messagebox.askokcancel('提示', '要切换到中笔吗'):
        d = 2


def switch_small():
    global d
    if tkinter.messagebox.askokcancel('提示', '要切换到小笔吗？'):
        d = 1


def plot_coordinate():
    global XY
    if tkinter.messagebox.askokcancel(
            '提示', '是否绘制坐标系，确定后返回草图界面任一点三点开始绘制(点击取消可撤销未执行的清空)'):
        XY = 1
    else:
        XY = None


def plot_coordinate_small():
    global XY
    if tkinter.messagebox.askokcancel(
            '提示', '是否绘制小跨度的坐标系，确定后返回草图界面任一点三点开始绘制(点击取消可撤销未执行的清空)'):
        XY = 2
    else:
        XY = None


def plot_coordinate_big_span():
    global XY
    if tkinter.messagebox.askokcancel(
            '提示', '是否绘制大跨度的坐标系，确定后返回草图界面任一点三点开始绘制(点击取消可撤销未执行的清空)'):
        XY = 3
    else:
        XY = None


def set_span():
    global XY, k, k_Input
    Input = k_Input.get().replace(' ', '')
    try:
        Input = int(Input)
        if tkinter.messagebox.askokcancel(
                '提示', f'是否设定跨度为{Input}(跨度代表坐标系一个单位大小的实际像素，系统默认大跨度为：120)'):
            k = Input
            XY = 1
        else:
            XY = None
            k = None
    except BaseException:
        k = None
        if tkinter.messagebox.askokcancel(
                '提示', '是否绘制大跨度的坐标系，确定后返回草图界面任一点三点开始绘制(点击取消可撤销未执行的清空)'):
            XY = 3
        else:
            XY = None


def empty():
    global BG
    if tkinter.messagebox.askokcancel('提示', '是否清空草稿(点击取消可撤销未执行的清空)'):
        BG = askcolor(title='选择背景颜色')[0]
    else:
        BG = None


def open_func_box():
    global HS_List, closeable
    HS_List = TK_HS.func_box()


def _help():
    global help_doc
    tkinter.messagebox.showinfo(title='帮助', message=help_doc)


def close():  # 关闭屏幕事件
    global top
    try:
        TK_HS.TK_DoneHS.top.destroy()
    except BaseException:
        pass
    try:
        TK_HS.top.destroy()
    except BaseException:
        pass
    top.destroy()


def tool_box():
    global colo  # 三个月还有这个一般v额u
    global ZColo, JColo
    global top  # 初始化屏幕
    global d
    global BG
    global XY
    global HS_List  # 绘制函数列表
    global BC  # 保存路径
    global k
    global d_Input, k_Input  # 定义Enter组件
    global BG_IM
    global closeable
    closeable = True
    BG_IM = None
    HS_List = {}
    XY = None
    BG = None
    d = None
    colo = None
    ZColo = None
    JColo = None
    BC = None
    w_b = 20
    h_b = 3
    k = None

    top = tkinter.Tk()  # 设置屏幕
    top.title('')
    top.resizable(width=False, height=False)
    top.geometry(f'+10+10')

    tkinter.Button(top, text="选择颜色", command=select_color,
                   width=w_b, height=h_b).pack()  # 选择颜色组件
    tkinter.Button(
        top,
        text="选择增函数颜色",
        command=increasing_func_color,
        width=w_b,
        height=1).pack()  # 选择颜色组件
    tkinter.Button(
        top,
        text="选择减函数颜色",
        command=subtraction_func_color,
        width=w_b,
        height=1).pack()  # 选择颜色组件
    tkinter.Button(
        top,
        text="使用中笔(默认笔)",
        command=switch_stroke,
        width=w_b,
        height=h_b).pack()  # 切换笔
    tkinter.Button(
        top,
        text="使用大笔",
        command=switch_big,
        width=w_b,
        height=1).pack()  # 切换到大笔
    tkinter.Button(
        top,
        text="使用小笔",
        command=switch_small,
        width=w_b,
        height=1).pack()  # 切换笔
    tkinter.Button(
        top,
        text="使用刷子",
        command=switch_brush,
        width=w_b,
        height=1).pack()  # 切换笔
    d_Input = tkinter.Entry(top, width=w_b - 2)
    d_Input.pack(fill=tkinter.BOTH)
    tkinter.Button(
        top,
        text="使用自定义大小",
        command=Set_d,
        width=w_b,
        height=1).pack()  # 切换笔
    tkinter.Button(
        top,
        text="清空草稿",
        command=empty,
        width=w_b,
        height=h_b).pack()  # 填充背景
    tkinter.Button(
        top,
        text="绘制坐标系",
        command=plot_coordinate,
        width=w_b,
        height=h_b).pack()  # 绘制坐标系
    tkinter.Button(
        top,
        text="绘制坐标系(小跨度)",
        command=plot_coordinate_small,
        width=w_b,
        height=1).pack()  # 绘制坐标系
    tkinter.Button(
        top,
        text="绘制坐标系(大跨度)",
        command=plot_coordinate_big_span,
        width=w_b,
        height=1).pack()  # 绘制坐标系
    k_Input = tkinter.Entry(top, width=w_b - 2)
    k_Input.pack(fill=tkinter.BOTH)
    tkinter.Button(
        top,
        text="使用自定义跨度",
        command=set_span,
        width=w_b,
        height=1).pack()  # 切换笔
    tkinter.Button(
        top,
        text="绘制函数",
        command=open_func_box,
        width=w_b,
        height=h_b).pack()
    tkinter.Button(
        top,
        text="保存",
        command=choose_save,
        width=w_b,
        height=1).pack()
    tkinter.Button(
        top,
        text="载入",
        command=choose_open,
        width=w_b,
        height=1).pack()
    tkinter.Button(top, text="帮助", command=_help, width=w_b,
                   height=1).pack()  # help是系统保留关键词，用_help代替
    top.protocol('WM_DELETE_WINDOW', close)
    top.mainloop()
    return [colo, d, BG, XY, HS_List, BC, ZColo, JColo, k, BG_IM]
    # [0]-笔的颜色
    # [1]-笔的大小
    # [2]-背景填充
    # [3]-坐标系绘制
    # [4]-函数绘制
    # [5]-保存
