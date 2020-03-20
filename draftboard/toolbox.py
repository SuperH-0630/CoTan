import os
from tkinter.colorchooser import askcolor
from newtkinter import asksaveasfilename, askopenfilename
import tkinter.messagebox

from draftboard import drawingfunction

SCREEN = None
pen_weight_input = None
span_input = None
background_image = None
func_logger = drawingfunction.Logger()
coordinate_system_drawing_method = None
background_color = None
pen_weight = None
pen_color = None
increasing_color = None
subtraction_color = None
save_dir = None
gui_width = 20
gui_height = 3
span = None
bg_color = "#FFFAFA"  # 主颜色
botton_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
help_doc = """
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
"""


class UIAPI:
    @staticmethod
    def askok_gui(message):
        return tkinter.messagebox.askokcancel('提示', message)


class API:
    @staticmethod
    def increasing_func_color():
        global increasing_color
        increasing_color = askcolor(title="选择颜色")[0]

    @staticmethod
    def subtraction_func_color():
        global subtraction_color
        subtraction_color = askcolor(title="选择颜色")[0]

    @staticmethod
    def select_color():
        global pen_color
        pen_color = askcolor(title="选择颜色")[0]

    @staticmethod
    def choose_save():
        global save_dir
        save_dir = asksaveasfilename(
            title="选择保存位置", filetypes=[("PNG", ".png")]
        )
        if not save_dir:
            save_dir = None
        else:
            save_dir += ".png"

    @staticmethod
    def choose_open():
        global background_image
        background_image = askopenfilename(
            title="选择载入图片", filetypes=[("PNG", ".png"), ("JPG", ".jpg")]
        )
        if not background_image:
            background_image = None

    @staticmethod
    def switch_brush():
        global pen_weight
        if UIAPI.askok_gui("要切换到刷子吗（可当橡皮使用）"):
            pen_weight = 10

    @staticmethod
    def switch_big():
        global pen_weight
        if UIAPI.askok_gui("要切换到大笔吗"):
            pen_weight = 3

    @staticmethod
    def set_pen():
        global pen_weight, pen_weight_input
        pen = pen_weight_input.get().replace(" ", "")
        try:
            pen = int(pen)
        except ValueError:
            if UIAPI.askok_gui("设置失败，是否要切换到中笔吗"):
                pen_weight = 2
        else:
            if UIAPI.askok_gui(f"是否设定大小为{pen}(系统默认大小为：2)"):
                pen_weight = pen

    @staticmethod
    def switch_stroke():
        global pen_weight
        if UIAPI.askok_gui("要切换到中笔吗"):
            pen_weight = 2

    @staticmethod
    def switch_small():
        global pen_weight
        if UIAPI.askok_gui("要切换到小笔吗？"):
            pen_weight = 1

    @staticmethod
    def plot_coordinate():
        global coordinate_system_drawing_method
        if tkinter.messagebox.askokcancel(
            "提示", "是否绘制坐标系，确定后返回草图界面任一点三点开始绘制(点击取消可撤销未执行的清空)"
        ):
            coordinate_system_drawing_method = 1
        else:
            coordinate_system_drawing_method = None

    @staticmethod
    def plot_coordinate_small():
        global coordinate_system_drawing_method
        if tkinter.messagebox.askokcancel(
            "提示", "是否绘制小跨度的坐标系，确定后返回草图界面任一点三点开始绘制(点击取消可撤销未执行的清空)"
        ):
            coordinate_system_drawing_method = 2
        else:
            coordinate_system_drawing_method = None

    @staticmethod
    def plot_coordinate_big_span():
        global coordinate_system_drawing_method
        if tkinter.messagebox.askokcancel(
            "提示", "是否绘制大跨度的坐标系，确定后返回草图界面任一点三点开始绘制(点击取消可撤销未执行的清空)"
        ):
            coordinate_system_drawing_method = 3
        else:
            coordinate_system_drawing_method = None

    @staticmethod
    def set_span():
        global coordinate_system_drawing_method, span, span_input
        span_input_str = span_input.get().replace(" ", "")
        try:
            span_input_str = int(span_input_str)
        except ValueError:
            span = None
            if tkinter.messagebox.askokcancel(
                "提示", "是否绘制大跨度的坐标系，确定后返回草图界面任一点三点开始绘制(点击取消可撤销未执行的清空)"
            ):
                coordinate_system_drawing_method = 3
            else:
                coordinate_system_drawing_method = None
        else:
            if tkinter.messagebox.askokcancel(
                "提示", f"是否设定跨度为{span_input_str}(跨度代表坐标系一个单位大小的实际像素，系统默认大跨度为：120)"
            ):
                span = span_input_str
                coordinate_system_drawing_method = 1
            else:
                coordinate_system_drawing_method = None
                span = None

    @staticmethod
    def empty():
        global background_color
        if UIAPI.askok_gui("是否清空草稿(点击取消可撤销未执行的清空)"):
            background_color = askcolor(title="选择背景颜色")[0]
        else:
            background_color = None

    @staticmethod
    def open_func_box():
        global func_logger
        func_logger = drawingfunction.func_box()

    @staticmethod
    def show_help():
        global help_doc
        tkinter.messagebox.showinfo(title="帮助", message=help_doc)


def tool_box():
    global SCREEN, span_input, pen_weight_input  # 初始化屏幕
    SCREEN = tkinter.Tk()  # 设置屏幕
    SCREEN["bg"] = bg_color
    SCREEN.title("Tool")
    SCREEN.resizable(width=False, height=False)
    SCREEN.geometry(f"+10+10")
    SCREEN.iconbitmap(bitmap=f'Pic{os.sep}favicon.ico', default=f'Pic{os.sep}favicon.ico')
    tkinter.Button(
        SCREEN,
        text="选择颜色",
        bg=bg_color,
        fg=word_color,
        command=API.select_color,
        width=gui_width,
        height=gui_height,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="选择增函数颜色",
        bg=bg_color,
        fg=word_color,
        command=API.increasing_func_color,
        width=gui_width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="选择减函数颜色",
        bg=bg_color,
        fg=word_color,
        command=API.subtraction_func_color,
        width=gui_width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="使用中笔(默认笔)",
        bg=bg_color,
        fg=word_color,
        command=API.switch_stroke,
        width=gui_width,
        height=gui_height,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="使用大笔",
        bg=bg_color,
        fg=word_color,
        command=API.switch_big,
        width=gui_width,
        height=1,
    ).pack()  # 切换到大笔
    tkinter.Button(
        SCREEN,
        text="使用小笔",
        bg=bg_color,
        fg=word_color,
        command=API.switch_small,
        width=gui_width,
        height=1,
    ).pack()  # 切换笔
    tkinter.Button(
        SCREEN,
        text="使用刷子",
        bg=bg_color,
        fg=word_color,
        command=API.switch_brush,
        width=gui_width,
        height=1,
    ).pack()  # 切换笔
    pen_weight_input = tkinter.Entry(SCREEN, width=gui_width - 2)
    pen_weight_input.pack(fill=tkinter.BOTH)
    tkinter.Button(
        SCREEN,
        text="使用自定义大小",
        bg=bg_color,
        fg=word_color,
        command=API.set_pen,
        width=gui_width,
        height=1,
    ).pack()  # 切换笔
    tkinter.Button(
        SCREEN,
        text="清空草稿",
        bg=bg_color,
        fg=word_color,
        command=API.empty,
        width=gui_width,
        height=gui_height,
    ).pack()  # 填充背景
    tkinter.Button(
        SCREEN,
        text="绘制坐标系",
        bg=bg_color,
        fg=word_color,
        command=API.plot_coordinate,
        width=gui_width,
        height=gui_height,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="绘制坐标系(小跨度)",
        bg=bg_color,
        fg=word_color,
        command=API.plot_coordinate_small,
        width=gui_width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="绘制坐标系(大跨度)",
        command=API.plot_coordinate_big_span,
        width=gui_width,
        height=1,
        bg=bg_color,
        fg=word_color,
    ).pack()  # 绘制坐标系
    span_input = tkinter.Entry(SCREEN, width=gui_width - 2)
    span_input.pack(fill=tkinter.BOTH)
    tkinter.Button(
        SCREEN,
        text="使用自定义跨度",
        bg=bg_color,
        fg=word_color,
        command=API.set_span,
        width=gui_width,
        height=1,
    ).pack()  # 切换笔
    tkinter.Button(
        SCREEN,
        text="绘制函数",
        bg=bg_color,
        fg=word_color,
        command=API.open_func_box,
        width=gui_width,
        height=gui_height,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="保存",
        bg=bg_color,
        fg=word_color,
        command=API.choose_save,
        width=gui_width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="载入",
        bg=bg_color,
        fg=word_color,
        command=API.choose_open,
        width=gui_width,
        height=1,
    ).pack()
    tkinter.Button(
        SCREEN,
        text="帮助",
        bg=bg_color,
        fg=word_color,
        command=API.show_help,
        width=gui_width,
        height=1,
    ).pack()  # help是系统保留关键词，用_help代替
    SCREEN.mainloop()
    func = func_logger()
    return [
        pen_color,
        pen_weight,
        background_color,
        coordinate_system_drawing_method,
        func,
        save_dir,
        increasing_color,
        subtraction_color,
        span,
        background_image,
    ]
