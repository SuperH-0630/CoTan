from os import path
import math
import random
import tkinter
import tkinter.messagebox

import numpy
import pandas
from matplotlib import pyplot as plt
from matplotlib import rcParams

from funcsystem.controller import SheetFunc, ExpFunc
from newtkinter import askopenfilename, asksaveasfilename

func_logger = []
fig = None
func_str_list = []
prompt_num = 0
FONT = (r"Font\ZKST.ttf", 11)  # 设置字体
SCREEN = tkinter.Tk()  # 设置屏幕
bg_color = "#FFFAFA"  # 主颜色
SCREEN["bg"] = bg_color
botton_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
line_style = {
    "实线": "-",
    "短横线": "--",
    "点划线": "-,",
    "虚线": ":",
    "点标记": ".",
    "圆标记": "o",
    "倒三角": "v",
    "正三角": "^",
    "左三角": "&lt",
    "下箭头": "1",
    "上箭头": "2",
    "左箭头": "3",
    "右箭头": "4",
    "正方形": "s",
    "五边形": "p",
    "星形": "*",
    "六边形": "h",
    "六边形2": "H",
    "+号": "+",
    "X标记": "x",
}  # 函数样式翻译表
point_style = ["g", "r", "c", "m", "y", "k"]
csv_list = []

gui_width = 13  # 标准宽度
gui_height = 2


def get_save_dir_gui():
    return asksaveasfilename(title="选择导出位置", filetypes=[("CSV", ".csv")])


def output_prompt_gui(news):
    global prompt_box, prompt_num
    prompt_num += 1
    news = str(news)
    prompt_box.insert(0, news + f"({prompt_num})")
    SCREEN.update()


def get_y_value_gradient_gui():
    parameters = y_value_gradient.get().split("#")  # 拆解输入
    return parameters


def dichotomy_gui():
    y = y_value.get().split(",")  # 拆解输入
    parameters = dicon_parameters.get().split("#")  # 拆解输入
    return parameters, y


def get_func_exp_box_index_gui():
    return func_exp_box.curselection()[0]


def get_x_value_gui():
    return x_value.get().split(",")


def update_property_box_gui(answer):
    property_box.delete(0, tkinter.END)
    property_box.insert(tkinter.END, *answer)


def update_result_box_gui(answer):
    result_box.delete(0, tkinter.END)
    result_box.insert(tkinter.END, *answer)


def get_func_logger_gui():
    return func_logger[func_exp_box.curselection()[0]]


def add_func_gui():
    get = func_exp.get().replace(" ", "")
    definition = definition_domain.get().split(",")
    name = func_name.get().replace(" ", "")
    style_str = func_style.get().split("#")
    if not name:
        name = get
    try:
        if style_str[0] not in point_style:
            style_str[0] = "b"
        line_style_str = line_style.get(style_str[1], "-")
    except BaseException:
        style_str = ["", ""]
        style_str[0] = random.choice(point_style)
        line_style_str = "-"
    style = style_str[0] + line_style_str
    try:
        span_str = definition[2]
        if span_str.startswith("H"):
            named_domain = {
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
            definition[2] = eval(span_str[1:], named_domain)
    except BaseException:
        pass
    return get, [name, style] + definition


def update_func_exp_box_gui():
    func_exp_box.delete(0, tkinter.END)
    func_exp_box.insert(tkinter.END, *func_logger)


def read_csv_gui():
    file = askopenfilename(title="载入表格", filetypes=[("CSV", ".csv")])
    style_str = func_style.get().split("#")
    try:
        if style_str[0] not in point_style:
            style_str[0] = "b"
        line_style_str = line_style.get(style_str[1], "-")
    except BaseException:
        style_str = ["", ""]
        style_str[0] = random.choice(point_style)
        line_style_str = "-"
    style = style_str[0] + line_style_str
    name = path.basename(file)[0:-4].replace(" ", "")
    if not name:
        name = random.randint(1, 1000)
    name += "(In CSV)"
    return pandas.read_csv(file).tolist(), name, style


class API:
    @staticmethod
    def type_selection(iter_object, si=float, no_zero=True):  # Float筛选系统
        x = []
        for i in iter_object:
            try:
                if si(i) == si(0) and no_zero:
                    continue
                x.append(si(i))
            except ValueError:
                pass
        return x

    @staticmethod
    def plot_func():
        global func_logger, definition_domain, fig, x_limit, y_limit, y_axis, x_axis
        # 画板创造
        output_prompt_gui("生成绘制取...")
        fig = plt.figure(num="CoTan函数")  # 定义一个图像窗口
        plt.grid(True, ls="--")  # 显示网格(不能放到后面，因为后面调整成为了笛卡尔坐标系)
        axis = plt.gca()
        axis.spines["right"].set_color("none")
        axis.spines["top"].set_color("none")
        axis.xaxis.set_ticks_position("bottom")
        axis.yaxis.set_ticks_position("left")
        axis.spines["bottom"].set_position(("data", 0))  # 设置x轴, y轴在(0, 0)的位置
        axis.spines["left"].set_position(("data", 0))
        # 检测x
        try:
            if x_axis.get()[0] == "c":  # 如果输入函数cx#-10#10#1#1
                # 第一部分HS，第二部分S，第三部分E，第四部分KD，第五部分JD
                plot_parameter = x_axis.get()[1:].split("#")
                exp_parameter = ["x", -10, 10, 1, 2]  # 保护系统
                try:
                    exp_parameter[0] = plot_parameter[0]
                    exp_parameter[1] = int(plot_parameter[1])
                    exp_parameter[2] = int(plot_parameter[2])
                    exp_parameter[3] = int(plot_parameter[3])
                    exp_parameter[4] = int(plot_parameter[4])
                except BaseException:  # 迭代匹配直到出现错误
                    pass
                plot_parameter = exp_parameter
                x_exp_scale = API.type_selection(
                    ExpFunc(
                        plot_parameter[0],
                        "x",
                        "",
                        plot_parameter[1],
                        plot_parameter[2],
                        plot_parameter[3],
                        plot_parameter[4],
                    ).data_packet()[1]
                )  # 取y
                axis.set_xticks(x_exp_scale)
            elif x_axis.get()[0] == "y":  # 输入函数y
                x_exp_scale = abs(int(x_axis.get()[1:]))
                x_major_locator = plt.MultipleLocator(x_exp_scale)
                axis.xaxis.set_major_locator(x_major_locator)
            else:  # 输入纯数字
                x_exp_scale = API.type_selection(x_axis.get().split(","))
                axis.set_xticks(x_exp_scale)
        except BaseException:
            x_major_locator = plt.MultipleLocator(2)
            axis.xaxis.set_major_locator(x_major_locator)
        # 检测y
        try:  # 意外捕捉
            if y_axis.get()[0] == "c":  # 如果输入函数cx#-10#10#1#1
                # 第一部分HS，第二部分S，第三部分E，第四部分KD，第五部分JD
                plot_parameter = y_axis.get()[1:].split("#")
                exp_parameter = ["x", -10, 10, 1, 2]  # 保护系统
                try:
                    exp_parameter[0] = plot_parameter[0]
                    exp_parameter[1] = int(plot_parameter[1])
                    exp_parameter[2] = int(plot_parameter[2])
                    exp_parameter[3] = int(plot_parameter[3])
                    exp_parameter[4] = int(plot_parameter[4])
                except BaseException:  # 迭代匹配直到出现错误
                    pass
                plot_parameter = exp_parameter
                y_exp_scale = API.type_selection(
                    ExpFunc(
                        plot_parameter[0],
                        "y",
                        "",
                        plot_parameter[1],
                        plot_parameter[2],
                        plot_parameter[3],
                        plot_parameter[4],
                    ).data_packet()[1]
                )  # 取y
                axis.set_yticks(y_exp_scale)
            elif y_axis.get()[0] == "y":  # 输入函数y
                y_exp_scale = abs(int(y_axis.get()[1:]))
                y_major_locator = plt.MultipleLocator(y_exp_scale)
                axis.yaxis.set_major_locator(y_major_locator)
            else:
                y_exp_scale = API.type_selection(y_axis.get().split(","))
                axis.set_yticks(y_exp_scale)
        except BaseException:
            y_major_locator = plt.MultipleLocator(2)
            axis.yaxis.set_major_locator(y_major_locator)
        # 极限
        try:
            _x_limit = API.type_selection(x_limit.get().split(","), si=int, no_zero=False)
            _y_limit = API.type_selection(y_limit.get().split(","), si=int, no_zero=False)
            try:
                _x_limit = [_x_limit[0], _x_limit[1]]
            except BaseException:
                _x_limit = [-10, 10]
            try:
                _y_limit = [_y_limit[0], _y_limit[1]]
            except BaseException:
                _y_limit = _x_limit
        except BaseException:
            _x_limit = [-10, 10]
            _y_limit = [-10, 10]
        _x_limit.sort()
        _y_limit.sort()
        plt.xlim(_x_limit)
        plt.ylim(_y_limit)
        # 函数绘图系统
        output_prompt_gui("图像绘制中...")
        if not func_logger:
            return False
        for Fucn in func_logger:
            get = Fucn.get_plot_data()
            plot_x = get[0]
            plot_y = get[1]
            func_label = get[2]
            exp_style = get[3]
            first = True
            for i in range(len(plot_x)):
                x_exp_scale = plot_x[i]
                y_exp_scale = plot_y[i]
                if first:
                    plt.plot(
                        x_exp_scale, y_exp_scale, exp_style, label=func_label
                    )  # plot()画出曲线
                    first = False
                else:
                    plt.plot(x_exp_scale, y_exp_scale, exp_style)
            get = Fucn.get_memory()
            memory_x = get[0]
            memory_y = get[1]
            max_x, max_y, min_x, min_y = Fucn.best_value()
            plt.plot(
                memory_x, memory_y, exp_style[0] + "o", label=f"Point of {func_label}"
            )  # 画出一些点
            len_x = sorted(list(set(memory_x)))  # 去除list重复项目
            extreme_points = max_x + min_x

            last_x = None
            for i in range(len(len_x)):
                if i in extreme_points:
                    continue  # 去除极值点
                now_x = len_x[i]  # x
                if last_x is None or abs(now_x - last_x) >= 1:  # 确保位置
                    num = memory_x.index(now_x)  # y的座位
                    now_y = memory_y[num]
                    plt.text(
                        now_x,
                        now_y,
                        f"({now_x},{int(now_y)})",
                        fontdict={"size": "10", "color": "b"},
                    )  # 标出坐标
                    last_x = now_x

            last_x = None
            plot_max = []
            for i in range(len(max_x)):  # 画出最大值
                now_x = max_x[i]
                if last_x is None or abs(now_x - last_x) >= 1:  # 确保位置
                    plt.text(
                        now_x - 1,
                        max_y,
                        f"max:({now_x},{int(max_y)})",
                        fontdict={"size": "10", "color": "b"},
                    )  # 标出坐标
                    plot_max.append(now_x)
                    last_x = now_x

            last_x = None
            plot_min = []
            for i in range(len(min_x)):  # 画出最小值
                now_x = min_x[i]
                if last_x is None or abs(now_x - last_x) >= 1:
                    plot_min.append(now_x)
                    plt.text(
                        now_x - 1,
                        min_y,
                        f"min:({now_x},{int(min_y)})",
                        fontdict={"size": "10", "color": "b"},
                    )  # 标出坐标
                    last_x = now_x
            plt.plot(plot_min, [min_y] * len(plot_min), exp_style[0] + "o")  # 画出一些点
            plt.plot(plot_max, [max_y] * len(plot_max), exp_style[0] + "o")  # 画出一些点
        output_prompt_gui("绘制完毕")
        plt.legend()  # 显示图示
        plt.show()  # 显示图像
        return True

    @staticmethod
    def add_from_csv():  # 添加函数
        file, name, style = read_csv_gui()
        try:
            output_prompt_gui("读取CSV")
            func_str_list.append(name)
            func_logger.append(SheetFunc(file, name, style))
            update_func_exp_box_gui()
            output_prompt_gui("读取完毕")
        except BaseException:
            output_prompt_gui("读取失败")

    @staticmethod
    def add_func():  # 添加函数
        get, definition = add_func_gui()
        if get and get not in func_str_list:
            func_str_list.append(get)
            func_logger.append(ExpFunc(get, *definition))
            update_func_exp_box_gui()
            output_prompt_gui("函数生成完毕")
        else:
            output_prompt_gui("函数生成失败")

    @staticmethod
    def clean_func_box():  # 添加函数
        global func_logger, func_str_list
        if API.show_askokcancel("是否清空所有函数？)"):
            func_str_list = []
            func_logger = []
            update_func_exp_box_gui()
            output_prompt_gui("函数清空完毕")

    @staticmethod
    def func_to_sheet_gui():  # 显示xy
        try:
            func = get_func_logger_gui()
            sheet_box.delete(0, tkinter.END)
            sheet_box.insert(tkinter.END, *func.return_list())
            output_prompt_gui("表格创建成功")
        except BaseException:
            output_prompt_gui("无法创建表格")
            pass

    @staticmethod
    def show_askokcancel(message):
        return tkinter.messagebox.askokcancel("提示", message)

    @staticmethod
    def clean_func_memory():
        global x_value, func_exp_box, func_logger
        try:
            if API.show_askokcancel(f"确定删除{func_logger[func_exp_box.curselection()[0]]}的记忆吗？"):
                get_func_logger_gui().clean_memory()
                update_result_box_gui([])
                output_prompt_gui("删除完毕")
            else:
                output_prompt_gui("删除取消")
        except BaseException:
            output_prompt_gui("删除失败")

    @staticmethod
    def hide_memory():  # 显示xy
        global func_logger, result_box
        try:
            get_func_logger_gui().hide_or_show()
            update_result_box_gui([])
            output_prompt_gui("已清空卡槽")
        except BaseException:
            output_prompt_gui("隐藏（显示）失败")

    @staticmethod
    def show_memory():  # 显示xy
        global func_logger, result_box
        try:
            answer = []
            for i in zip(get_func_logger_gui().get_memory()):
                answer.append(f"x={i[0]} -> y={i[1]}")
            update_result_box_gui(answer)
            output_prompt_gui("输出完成")
        except BaseException:
            output_prompt_gui("操作失败")

    @staticmethod
    def property_prediction():
        try:
            output_prompt_gui("预测过程程序可能无响应")
            answer = get_func_logger_gui().property_prediction(output_prompt_gui)
            update_property_box_gui(answer)
            output_prompt_gui("性质预测完成")
        except IndexError:
            output_prompt_gui("性质预测失败")

    @staticmethod
    def calculate():
        global func_logger, result_box, x_value
        try:
            output_prompt_gui("计算过程程序可能无响应")
            answer = get_func_logger_gui().calculation(get_x_value_gui())
            update_result_box_gui(answer)
            output_prompt_gui("系统计算完毕")
        except IndexError:
            output_prompt_gui("计算失败")

    @staticmethod
    def func_to_csv():  # 导出CSV
        global csv_list
        try:
            get_func_logger_gui().save_csv(get_save_dir_gui())
            output_prompt_gui("CSV导出成功")
        except BaseException:
            output_prompt_gui("CSV导出失败")

    @staticmethod
    def del_func():  # 删除函数
        global func_logger, func_str_list, func_exp_box
        del_index = get_func_exp_box_index_gui()
        del func_logger[del_index]
        del func_str_list[del_index]
        update_func_exp_box_gui()
        output_prompt_gui("函数删除完毕")

    @staticmethod
    def dichotomy():
        try:
            output_prompt_gui("计算过程程序可能无响应")
            parameters, y = dichotomy_gui()
            answer = []
            output_prompt_gui("系统运算中")
            for i in y:
                answer += get_func_logger_gui().dichotomy(float(i), *parameters)[0]
            if answer:
                output_prompt_gui("系统运算完成")
            else:
                output_prompt_gui("系统运算无结果")
            update_result_box_gui(answer)
        except BaseException:
            output_prompt_gui("系统运算失败")

    @staticmethod
    def gradient_method_calculation():
        try:
            output_prompt_gui("计算过程程序可能无响应")
            output_prompt_gui("系统运算中")
            answer = get_func_logger_gui().gradient_calculation(*get_y_value_gradient_gui())
            if answer[1]:
                output_prompt_gui("系统运算完成")
            else:
                output_prompt_gui("系统运算无结果")
            update_result_box_gui(answer)
        except BaseException:
            output_prompt_gui("系统运算失败，请注意参数设置")

    @staticmethod
    def func_differentiation():
        global func_logger, func_exp_box, property_box, func_str_list, func_name, line_style, point_style, func_style
        try:
            fucn = get_func_logger_gui()
            diff = fucn.derivatives
            if diff is not None and str(diff):
                get = str(diff)
                func_str_list.append(get)
                func_logger.append(
                    ExpFunc(
                        get,
                        "(导)" + fucn.func_name + " Of ",
                        fucn.style,
                        fucn.start,
                        fucn.end,
                        fucn.span,
                        fucn.accuracy,
                    )
                )
                update_func_exp_box_gui()
                output_prompt_gui("函数生成完毕")
            else:
                raise Exception
        except BaseException:
            output_prompt_gui("导函数创建失败")


def function_mapping():
    global SCREEN
    SCREEN.mainloop()


SCREEN.title("CoTan函数测绘")
SCREEN.resizable(width=False, height=False)
SCREEN.geometry(f"+10+10")
rcParams["font.family"] = "simhei"
rcParams["axes.unicode_minus"] = False
tkinter.Label(
    SCREEN,
    text="输入解析式：",
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=0, row=0
)  # 设置说明
func_exp = tkinter.Entry(SCREEN, width=gui_width * 2)
func_exp.grid(column=1, row=0, columnspan=2, sticky=tkinter.E + tkinter.W)

# 设置定义域
tkinter.Label(
    SCREEN,
    font=FONT,
    text="定义域：",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=0, row=1
)  # 设置说明
definition_domain = tkinter.Entry(SCREEN, width=gui_width * 2)
definition_domain.grid(column=1, row=1, columnspan=2, sticky=tkinter.E + tkinter.W)

# 设置函数名字
tkinter.Label(
    SCREEN,
    font=FONT,
    text="函数名字：",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=0, row=2
)  # 设置说明
func_name = tkinter.Entry(SCREEN, width=gui_width * 2)
func_name.grid(column=1, row=2, columnspan=2, sticky=tkinter.E + tkinter.W)

# 设置函数图示
tkinter.Label(
    SCREEN,
    font=FONT,
    text="函数样式：",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=0, row=3
)  # 设置说明
func_style = tkinter.Entry(SCREEN, width=gui_width * 2)
func_style.grid(column=1, row=3, columnspan=2, sticky=tkinter.E + tkinter.W)

a_y = 4  # 按钮统一纵坐标
tkinter.Button(
    SCREEN,
    text="添加新函数",
    command=API.add_func,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=0, row=a_y
)  # 添加函数
tkinter.Button(
    SCREEN,
    text="删除选中函数",
    command=API.del_func,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=1, row=a_y
)  # 删除函数
tkinter.Button(
    SCREEN,
    text="清除函数",
    command=API.clean_func_box,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=2, row=a_y
)  # 绘制函数
a_y += 1
# 显示函数
func_exp_box = tkinter.Listbox(SCREEN, width=gui_width * 3 + 2)  # 暂时不启用多选
rowspan = 12
func_exp_box.grid(
    column=0,
    row=a_y,
    columnspan=3,
    rowspan=rowspan,
    sticky=tkinter.S + tkinter.N + tkinter.E + tkinter.W,
)
a_y += rowspan
tkinter.Label(
    SCREEN, font=FONT, text="", width=gui_width, height=1, bg=bg_color, fg=word_color
).grid(column=0, row=a_y)

tkinter.Label(SCREEN, font=FONT, text="", width=1, bg=bg_color, fg=word_color).grid(
    column=4, row=0
)  # 占用第四
a_y = 0
# 输入x函数求y值
tkinter.Label(
    SCREEN,
    font=FONT,
    text="计算(y):",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 设置说明
x_value = tkinter.Entry(SCREEN, width=gui_width * 2)
x_value.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

a_y += 1
# 输入x函数求y值
tkinter.Label(
    SCREEN,
    font=FONT,
    text="二分法计算(y):",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 设置说明
y_value = tkinter.Entry(SCREEN, width=gui_width * 2)
y_value.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

a_y += 1
tkinter.Label(
    SCREEN,
    font=FONT,
    text="二分法参数:",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 设置说明
dicon_parameters = tkinter.Entry(SCREEN, width=gui_width * 2)
dicon_parameters.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

a_y += 1
# 输入x函数求y值
tkinter.Label(
    SCREEN,
    font=FONT,
    text="梯度法计算(y):",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 设置说明
y_value_gradient = tkinter.Entry(SCREEN, width=gui_width * 2)
y_value_gradient.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

a_y += 1
tkinter.Button(
    SCREEN,
    text="计算(y)",
    command=API.calculate,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 设置说明
tkinter.Button(
    SCREEN,
    text="二分法计算(x)",
    command=API.dichotomy,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(column=6, row=a_y)
tkinter.Button(
    SCREEN,
    text="梯度法计算(x)",
    command=API.gradient_method_calculation,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(column=7, row=a_y)

a_y += 1
# 绘制函数坐标表格
tkinter.Button(
    SCREEN,
    text="查看记忆",
    command=API.show_memory,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(column=5, row=a_y)
tkinter.Button(
    SCREEN,
    text="隐藏记忆",
    command=API.hide_memory,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(column=6, row=a_y)
tkinter.Button(
    SCREEN,
    text="清空记忆",
    command=API.clean_func_memory,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(column=7, row=a_y)

a_y += 1
# 显示函数
result_box = tkinter.Listbox(SCREEN, width=gui_width * 3 + 2, height=8)  # 暂时不启用多选
result_box.grid(
    column=5, row=a_y, columnspan=3, sticky=tkinter.N + tkinter.E + tkinter.W
)

a_y += 1
# 设置坐标系刻度
tkinter.Label(
    SCREEN,
    font=FONT,
    text="X轴(函数):",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y, sticky=tkinter.N
)  # 设置说明
x_axis = tkinter.Entry(SCREEN, width=gui_width * 2)
x_axis.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.N + tkinter.E + tkinter.W)

a_y += 1
# 设置坐标系刻度
tkinter.Label(
    SCREEN,
    font=FONT,
    text="Y轴(函数):",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 设置说明
y_axis = tkinter.Entry(SCREEN, width=gui_width * 2)
y_axis.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

a_y += 1
# 设置坐标系刻度
tkinter.Label(
    SCREEN,
    font=FONT,
    text="X轴极限:",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 设置说明
x_limit = tkinter.Entry(SCREEN, width=gui_width * 2)
x_limit.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

a_y += 1
# 设置坐标系刻度
tkinter.Label(
    SCREEN,
    font=FONT,
    text="Y轴极限:",
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 设置说明
y_limit = tkinter.Entry(SCREEN, width=gui_width * 2)
y_limit.grid(column=6, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

a_y += 1
tkinter.Button(
    SCREEN,
    text="绘制函数",
    command=API.plot_func,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=5, row=a_y
)  # 绘制函数
tkinter.Button(
    SCREEN,
    text="计算性质",
    command=API.property_prediction,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=6, row=a_y
)  # 绘制函数
tkinter.Button(
    SCREEN,
    text="创建导函数",
    command=API.func_differentiation,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(
    column=7, row=a_y
)  # 绘制函数
a_y += 1
property_box = tkinter.Listbox(SCREEN, width=gui_width * 3 + 2, height=10)  # 暂时不启用多选
property_box.grid(
    column=5, row=a_y, columnspan=3, sticky=tkinter.N + tkinter.E + tkinter.W
)
a_y += 1
prompt_box = tkinter.Listbox(SCREEN, width=gui_width * 3 + 2, height=3)  # 暂时不启用多选
prompt_box.grid(
    column=5, row=a_y, columnspan=3, sticky=tkinter.N + tkinter.E + tkinter.W
)

tkinter.Label(SCREEN, font=FONT, text="", width=1, bg=bg_color, fg=word_color).grid(
    column=8, row=a_y
)  # 占用第四
a_y = 0

# 绘制函数坐标表格
tkinter.Button(
    SCREEN,
    text="导入表格",
    command=API.add_from_csv,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(column=9, row=a_y)
tkinter.Button(
    SCREEN,
    text="生成表格",
    command=API.func_to_sheet_gui,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(column=10, row=a_y)
tkinter.Button(
    SCREEN,
    text="导出表格",
    command=API.func_to_csv,
    font=FONT,
    width=gui_width,
    height=gui_height,
    bg=bg_color,
    fg=word_color,
).grid(column=11, row=a_y)

a_y += 1
# 显示函数的xy
sheet_box = tkinter.Listbox(SCREEN, width=gui_width * 3 + 2)  # 暂时不启用多选
sheet_box.grid(
    column=9,
    row=a_y,
    columnspan=3,
    rowspan=rowspan + 4,
    sticky=tkinter.S + tkinter.N + tkinter.E + tkinter.W,
)

output_prompt_gui("加载完成，欢迎使用!")
