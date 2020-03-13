from __future__ import division  # 让/恢复为除法
import random
import tkinter
import tkinter.messagebox

import sympy
from matplotlib import pyplot as plt
from matplotlib import rcParams
from matplotlib.animation import FuncAnimation

from HSCH.HS import ExpFunc as ExpFunc

func = None
fig = None
prompt_num = 0
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
SCREEN = tkinter.Tk()
bg_color = "#FFFAFA"  # 主颜色
botton_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
gui_width = 13  # 标准宽度
gui_height = 2
row = 0
column = 1


def type_selection(sequence, type_=float, convert=True):  # Float筛选系统
    x = []
    for i in sequence:
        try:
            if type_(i) == type_(0) and convert:
                continue
            x.append(type_(i))
        except ValueError:
            pass
    return x


def save_to_csv():  # 导出CSV
    try:
        succ = func.save_csv()  # 是否成功
        if not succ:
            raise Exception
        output_prompt("CSV导出成功")
    except BaseException:
        output_prompt("CSV导出失败")


def to_sheet():  # 生成表格
    global func, sheet_box
    try:
        sheet_box.delete(0, tkinter.END)
        sheet_box.insert(tkinter.END, *func.return_list())
        output_prompt("表格创建成功")
    except BaseException:
        output_prompt("无法创建表格")


def sympy_computing(exp_str) -> tuple:
    try:
        named_domain = {
            "Pi": sympy.pi,
            "e": sympy.E,
            "log": sympy.log,
            "sin": sympy.sin,
            "cos": sympy.cos,
            "tan": sympy.tan,
            "cot": lambda x: 1 / sympy.tan(x),
            "csc": lambda x: 1 / sympy.sin(x),
            "sec": lambda x: 1 / sympy.cos(x),
            "sinh": sympy.sinh,
            "cosh": sympy.cosh,
            "tanh": sympy.tanh,
            "asin": sympy.asin,
            "acos": sympy.acos,
            "atan": sympy.atan,
        }
        ans = eval(exp_str, named_domain)
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
    global func, projection_value, projection_box, prediction_accuracy
    a, must = sympy_computing(prediction_accuracy.get())
    try:
        result = func.check_symmetry_center(
            confirmation_expression(projection_value.get()), output_prompt, a
        )
        if result[1]:
            projection_box.insert(tkinter.END, result[1])
            output_prompt("预测完成")
        else:
            raise Exception
    except BaseException:
        output_prompt("预测失败")


def check_symmetry_axis():
    global func, projection_value, projection_box, prediction_accuracy
    a, must = sympy_computing(prediction_accuracy.get())
    try:
        result = func.check_symmetry_axis(
            confirmation_expression(projection_value.get()), output_prompt, a
        )
        if result[1]:
            projection_box.insert(tkinter.END, result[1])
            output_prompt("预测完成")
        else:
            raise Exception
    except BaseException:
        output_prompt("预测失败")


def check_periodic():
    global func, projection_value, projection_box, prediction_accuracy
    a, must = sympy_computing(prediction_accuracy.get())
    try:
        result = func.check_periodic(
            confirmation_expression(projection_value.get()), output_prompt, a
        )
        if result[1]:
            projection_box.insert(tkinter.END, result[1])
            output_prompt("预测完成")
        else:
            raise Exception
    except BaseException:
        output_prompt("预测失败")


def check_monotonic():
    global func, projection_value, projection_box, prediction_accuracy
    a, must = sympy_computing(prediction_accuracy.get())
    try:
        result = func.check_monotonic(projection_value.get(), output_prompt, a)
        if result[1]:
            projection_box.insert(tkinter.END, result[1])
            output_prompt("预测完成")
        else:
            raise Exception
    except BaseException:
        output_prompt("预测失败")


def clear_memory():
    global func
    try:
        if tkinter.messagebox.askokcancel("提示", f"确定删除{func}的记忆吗？"):
            result_box.delete(0, tkinter.END)
            func.clean_memory()
            output_prompt("删除完毕")
        else:
            output_prompt("删除取消")
    except BaseException:
        output_prompt("删除失败")


def show_hidden_memory():  # 显示xy
    global func, result_box
    try:
        result_box.delete(0, tkinter.END)
        func.hide_or_show()
        output_prompt("已清空卡槽")
    except BaseException:
        output_prompt("隐藏（显示）失败")


def gradient_method_calculation():
    global func, y_value_gradient, gradient_parameters, result_box
    try:
        output_prompt("计算过程程序可能无响应")
        result_box.delete(0, tkinter.END)  # 清空
        E = []
        for i in gradient_parameters:
            E.append(i.get())
        output_prompt("系统运算中")
        answer = func.gradient_calculation(y_value_gradient.get(), *E)
        if answer[1] is not None:
            result_box.insert(tkinter.END, answer[0])
            output_prompt("系统运算完成")
        else:
            output_prompt("系统运算无结果")
    except BaseException:
        output_prompt("系统运算失败，请注意参数设置")


def calculate():
    global x_value, func, result_box
    try:
        output_prompt("计算过程程序可能无响应")
        result_box.delete(0, tkinter.END)
        x = x_value.get().split(",")
        answer = func.calculate(x)
        if answer != []:
            result_box.insert(tkinter.END, *answer)
            output_prompt("系统运算完毕")
        else:
            output_prompt("系统运算无结果")
    except BaseException:
        output_prompt("计算失败")


def sympy_calculation_x():
    global y_value_symbol, func, result_box
    try:
        output_prompt("计算过程程序可能无响应")
        result_box.delete(0, tkinter.END)
        x = y_value_symbol.get().split(",")
        answer = []
        for i in x:
            answer += func.sympy_calculation(i)[0]
        if answer != []:
            result_box.insert(tkinter.END, *answer)
            output_prompt("系统运算完毕")
        else:
            output_prompt("系统运算无结果")
    except BaseException:
        output_prompt("计算失败")


def function_differentiation():
    global x_value_derivation, func, result_box, proximity_accuracy
    try:
        output_prompt("计算过程程序可能无响应")
        result_box.delete(0, tkinter.END)
        x = x_value_derivation.get().split(",")
        accuracy = proximity_accuracy.get()
        answer = []
        for i in x:
            get = func.derivative(i, accuracy)[0]
            if get is not None:
                answer.append(get)
        if answer != []:
            result_box.insert(tkinter.END, *answer)
            output_prompt("系统运算完毕")
        else:
            output_prompt("系统运算无结果")
    except IndexError:
        output_prompt("计算失败")


def approximation():  # 逼近法
    global x_value_derivation, func, result_box, proximity_accuracy
    try:
        output_prompt("计算过程程序可能无响应")
        result_box.delete(0, tkinter.END)
        x = x_value_derivation.get().split(",")
        accuracy = proximity_accuracy.get()
        answer = []
        for i in x:
            get = func.derivative(i, accuracy, True)[0]
            if get is not None:
                answer.append(get)
        if answer != []:
            result_box.insert(tkinter.END, *answer)
            output_prompt("系统运算完毕")
        else:
            output_prompt("系统运算无结果")
    except IndexError:
        output_prompt("计算失败")


def dichotomy():  # 二分法
    global y_value, dicon_parameters, func, result_box
    try:
        output_prompt("计算过程程序可能无响应")
        result_box.delete(0, tkinter.END)  # 清空
        y = y_value.get().split(",")  # 拆解输入
        parameters = [100, 0.0001, 0.1, 0.5, False, True, 1000, 0.1, 0.1, False, None]
        for i in range(11):
            try:
                if i in (4, 5, 9):
                    a = dicon_parameters[i].get()
                else:
                    a = float(dicon_parameters[i].get())
                parameters[i] = a
            except BaseException:
                pass
        answer = []
        output_prompt("系统运算中")
        for i in y:
            try:
                answer += func.dichotomy(float(i), *parameters)[0]
            except BaseException:
                pass
        if answer:
            output_prompt("系统运算完成")
            result_box.insert(tkinter.END, *answer)
        else:
            output_prompt("系统运算无结果")
    except BaseException:
        output_prompt("系统运算失败")


def property_prediction():
    global func, prediction_box, prediction_accuracy
    try:
        a, must = sympy_computing(prediction_accuracy.get())
        output_prompt("预测过程程序可能无响应")
        prediction_box.delete(0, tkinter.END)
        answer = func.property_prediction(output_prompt, True, a)
        prediction_box.insert(tkinter.END, *answer)
        output_prompt("性质预测完成")
    except IndexError:
        output_prompt("性质预测失败")


def function_drawing():
    global x_scale, start_x_plot, start_x_polt, span_x_plot, y_scale, start_y_plot, end_y_plot, span_y_plot
    global start_x_limit, end_x_limit, start_y_limit, end_y_limit
    global func, fig, show_point, show_best_value, show_text, plot_type, frame_rate
    try:
        draw_type = plot_type.curselection()[0]
    except BaseException:
        draw_type = 0
    # 画板创造
    output_prompt("生成绘制取...")
    fig = plt.figure(num="CoTan函数")  # 定义一个图像窗口
    if draw_type in (0, 1, 2, 3, 8, 9):
        plt.grid(True, ls="--")  # 显示网格(不能放到后面，因为后面调整成为了笛卡尔坐标系)
    axis = plt.gca()
    text_y = ""
    text_x = ""

    def init():
        nonlocal text_x, text_y
        if draw_type in (0, 2, 4, 6, 8):
            axis.spines["right"].set_color("none")
            axis.spines["top"].set_color("none")
            axis.xaxis.set_ticks_position("bottom")
            axis.yaxis.set_ticks_position("left")
            axis.spines["bottom"].set_position(("data", 0))  # 设置x轴, y轴在(0, 0)的位置
            axis.spines["left"].set_position(("data", 0))
        # 检测x
        try:
            if x_scale.get()[0] == "c":  # 如果输入函数cx#-10#10#1#1
                plot_parameter = [
                    x_scale.get()[1:],
                    start_x_plot.get(),
                    start_x_polt.get(),
                    span_x_plot.get(),
                    2,
                ]  # 第一部分HS，第二部分S，第三部分E，第四部分KD，第五部分JD
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
                x_exp_scale = type_selection(
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
                axis.set_xticks(x_exp_scale)  # 输入表达式计算刻度
            elif x_scale.get()[0] == "y":  # 输入函数y
                # 不错要错误捕捉，外围有个大的捕捉
                x_exp_scale = abs(int(start_x_plot.get()))
                x_major_locator = plt.MultipleLocator(x_exp_scale)
                axis.xaxis.set_major_locator(x_major_locator)
            else:  # 输入纯数字
                x_exp_scale = type_selection(x_scale.get().split(","))
                axis.set_xticks(x_exp_scale)
        except BaseException:
            x_major_locator = plt.MultipleLocator(2)
            axis.xaxis.set_major_locator(x_major_locator)
        # 检测y
        try:  # 意外捕捉
            if y_scale.get()[0] == "c":  # 如果输入函数cx#-10#10#1#1
                plot_parameter = [
                    y_scale.get()[1:],
                    start_y_plot.get(),
                    end_y_plot.get(),
                    span_y_plot.get(),
                    2,
                ]  # 第一部分HS，第二部分S，第三部分E，第四部分KD，第五部分JD
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
                y_exp_scale = type_selection(
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
            elif y_scale.get()[0] == "y":  # 输入函数y
                y_exp_scale = abs(int(start_y_plot.get()))
                y_major_locator = plt.MultipleLocator(y_exp_scale)
                axis.yaxis.set_major_locator(y_major_locator)
            else:
                y_exp_scale = type_selection(y_scale.get().split(","))
                axis.set_yticks(y_exp_scale)
        except BaseException:
            y_major_locator = plt.MultipleLocator(2)
            axis.yaxis.set_major_locator(y_major_locator)
        # 极限
        try:
            x_limit = type_selection(
                [start_x_limit.get(), end_x_limit.get()], type_=int, convert=False
            )
            y_limit = type_selection(
                [start_y_limit.get(), end_y_limit.get()], type_=int, convert=False
            )
            try:
                _x_limit = [x_limit[0], x_limit[1]]
            except BaseException:
                _x_limit = [-10, 10]
            try:
                _y_limit = [y_limit[0], y_limit[1]]
            except BaseException:
                _y_limit = _x_limit
        except BaseException:
            _x_limit = [-10, 10]
            _y_limit = [-10, 10]
        _x_limit.sort()
        _y_limit.sort()
        axis.set_xlim(_x_limit)
        axis.set_ylim(_y_limit)
        text_x = _x_limit[0] + abs(_x_limit[0]) * 0.01
        text_y = _y_limit[1] - abs(_y_limit[1]) * 0.01

    init()
    # 函数绘图系统
    output_prompt("图像绘制中...")
    if func is None:
        return False
    if draw_type in (0, 1, 4, 5):
        # 绘制曲线
        get = func.get_plot_data()
        plot_x = get[0]
        plot_y = get[1]
        func_label = get[2]
        exp_style = get[3]
        first = True
        for i in range(len(plot_x)):
            plot_x = plot_x[i]
            plot_y = plot_y[i]
            if first:
                plt.plot(plot_x, plot_y, exp_style, label=func_label)  # plot()画出曲线
                first = False
            else:
                plt.plot(plot_x, plot_y, exp_style)
        # 绘制记忆点
        get = func.get_memory()
        plot_memory_x = get[0]
        plot_memory_y = get[1]
        max_x, max_y, min_x, min_y = func.best_value()
        if show_point.get():
            plt.plot(
                plot_memory_x,
                plot_memory_y,
                exp_style[0] + "o",
                label=f"Point of {func_label}",
            )  # 画出一些点
            memory_x = sorted(list(set(plot_memory_x)))  # 去除list重复项目
            extreme_points = max_x + min_x

            if show_text.get():
                last_x = None
                for i in range(len(memory_x)):
                    if i in extreme_points:
                        continue  # 去除极值点
                    now_x = memory_x[i]  # x
                    if last_x is None or abs(now_x - last_x) >= 1:  # 确保位置
                        num = plot_memory_x.index(now_x)  # y的座位
                        now_y = plot_memory_y[num]
                        plt.text(
                            now_x,
                            now_y,
                            f"({now_x},{int(now_y)})",
                            fontdict={"size": "10", "color": "b"},
                        )  # 标出坐标
                        last_x = now_x
        if show_best_value.get():
            last_x = None
            plot_max = []
            for i in range(len(max_x)):  # 画出最大值
                now_x = max_x[i]
                if last_x is None or abs(now_x - last_x) >= 1:  # 确保位置
                    if show_text.get():
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
                    if show_text.get():
                        plt.text(
                            now_x - 1,
                            min_y,
                            f"min:({now_x},{int(min_y)})",
                            fontdict={"size": "10", "color": "b"},
                        )  # 标出坐标
                    last_x = now_x
            plt.plot(plot_min, [min_y] * len(plot_min), exp_style[0] + "o")  # 画出一些点
            plt.plot(plot_max, [max_y] * len(plot_max), exp_style[0] + "o")  # 画出一些点
        plt.legend()  # 显示图示
    elif draw_type in (8, 9):
        get = func.data_packet()
        plot_x = get[0]
        plot_y = get[1]
        plot_x_len = len(plot_x)
        x_data = []
        y_data = []
        func_label = get[2]
        exp_style = get[3]
        plot_ln = axis.plot([], [], exp_style, label=func_label, animated=False)[0]
        text = plt.text(text_x, text_y, "", fontdict={"size": "10", "color": "b"})

        def _init():
            init()
            return plot_ln, text

        def update(n):
            nonlocal x_data, y_data
            if n == 0:
                x_data = []
                y_data = []
            x_data.append(plot_x[n])
            y_data.append(plot_y[n])
            text.set_text(f"x={plot_x[n]},y={plot_y[n]}")
            plot_ln.set_data(x_data, y_data)
            return plot_ln, text

        try:  # 自定义帧率
            frame = int(frame_rate.get())
        except BaseException:
            frame = 100
        FuncAnimation(
            fig,
            update,
            frames=plot_x_len,
            init_func=_init,
            interval=frame,
            blit=False,
            repeat_delay=3000,
        )  # 动态绘图
    elif draw_type in (2, 3, 6, 7):
        text = plt.text(text_x, text_y, "", fontdict={"size": "10", "color": "b"})
        all_func = func.return_son()
        func_cul_list = []
        plot_x_len = len(all_func)
        m = []  # 每个群组中fx分类的个数
        for i in all_func:  # 预先生成函数
            output_prompt(f"迭代计算中...(共{plot_x_len}次)")
            get = i.get_plot_data()
            m.append(len(get[0]))
            func_cul_list.append(get)
        func_cul_list += func_cul_list[::-1]
        ln_list = [text]
        for i in range(max(m)):
            ln_list.append(
                axis.plot([], [], func_cul_list[0][3], animated=False)[0]
            )  # 创建足够的i
        plot_x_len = len(func_cul_list)

        def _init():
            init()
            text.set_text("")
            return None

        def update(n):
            get = func_cul_list[n - 1]
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
            frame = int(frame_rate.get())
        except BaseException:
            frame = 100
        FuncAnimation(
            fig, update, frames=plot_x_len, init_func=_init, interval=frame, blit=False
        )  # 动态绘图
    output_prompt("绘制完毕")
    plt.show()  # 显示图像
    return True


def set_function():
    global func_exp, start_definition, end_definition, span_definition, accuracy, func_name, func_style, line_style
    global point_style, func, SCREEN
    global default_a, start_a, end_a, span_a
    new_func = func_exp.get().replace(" ", "")
    if new_func == "":
        output_prompt("应用失败")
        return None
    default_value = [-10, 10, 0.1, 2, 1, -10, 10, 1]
    get = [
        start_definition,
        end_definition,
        span_definition,
        accuracy,
        default_a,
        start_a,
        end_a,
        span_a,
    ]
    # 参数的处理
    try:
        span_str = span_definition.get().replace(" ", "")
        if span_str[0] == "H":
            domain = {
                "Pi": sympy.pi,
                "e": sympy.E,
                "log": sympy.log,
                "sin": sympy.sin,
                "cos": sympy.cos,
                "tan": sympy.tan,
                "cot": lambda x: 1 / sympy.tan(x),
                "csc": lambda x: 1 / sympy.sin(x),
                "sec": lambda x: 1 / sympy.cos(x),
                "sinh": sympy.sinh,
                "cosh": sympy.cosh,
                "tanh": sympy.tanh,
                "asin": sympy.asin,
                "acos": sympy.acos,
                "atan": sympy.atan,
            }
            span = eval(span_str[1:], domain)
        else:
            raise Exception
    except BaseException:
        span = None
    for i in range(8):
        try:
            default_value[i] = float(get[i].get())
        except BaseException:
            pass
    if span is not None:
        default_value[2] = span

    # View的处理
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
    # Name的处理
    name = func_name.get().replace(" ", "")
    if name == "":
        name = new_func
    try:
        func = ExpFunc(new_func, name, style, *default_value, have_son=True)
        output_prompt("应用成功")
        SCREEN.title(f"CoTan函数工厂  {func}")
    except BaseException:
        output_prompt("应用失败")


def output_prompt(news):
    global prompt_box, prompt_num, SCREEN
    prompt_num += 1
    news = str(news)
    prompt_box.insert(0, news + f"({prompt_num})")
    SCREEN.update()


def function_factory_main():  # H_S-默认函数GF-关闭时询问返回函数
    global SCREEN
    SCREEN.mainloop()


SCREEN["bg"] = bg_color
SCREEN.title("CoTan函数工厂")
SCREEN.resizable(width=False, height=False)
SCREEN.geometry("+10+10")
FONT = (r"Font\ZKST.ttf", 11)  # 设置字体
rcParams["font.family"] = "simhei"
rcParams["axes.unicode_minus"] = False
tkinter.Label(
    SCREEN,
    text="输入解析式:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
func_exp = tkinter.Entry(SCREEN, width=gui_width * 2)
func_exp.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="定义域前端点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
start_definition = tkinter.Entry(SCREEN, width=gui_width * 2)
start_definition.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="定义域后端点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
end_definition = tkinter.Entry(SCREEN, width=gui_width * 2)
end_definition.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="函数绘制跨度:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
span_definition = tkinter.Entry(SCREEN, width=gui_width * 2)
span_definition.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="函数计算精度:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
accuracy = tkinter.Entry(SCREEN, width=gui_width * 2)
accuracy.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="函数名字:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
func_name = tkinter.Entry(SCREEN, width=gui_width * 2)
func_name.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="函数视图:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
func_style = tkinter.Entry(SCREEN, width=gui_width * 2)
func_style.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="常量a默认值:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
default_a = tkinter.Entry(SCREEN, width=gui_width * 2)
default_a.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="常量a起点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
start_a = tkinter.Entry(SCREEN, width=gui_width * 2)
start_a.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="常量a终点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
end_a = tkinter.Entry(SCREEN, width=gui_width * 2)
end_a.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="常量a跨度:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
span_a = tkinter.Entry(SCREEN, width=gui_width * 2)
span_a.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="应用函数",
    command=set_function,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="绘制图像",
    command=function_drawing,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="性质预测",
    command=property_prediction,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数

row += 1
tkinter.Label(
    SCREEN,
    text="预测精度:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
prediction_accuracy = tkinter.Entry(SCREEN, width=gui_width * 2)
prediction_accuracy.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
# 显示函数的xy
prediction_box = tkinter.Listbox(SCREEN, width=gui_width * 3)  # 暂时不启用多选
prediction_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=9,
    sticky=tkinter.S + tkinter.N + tkinter.E + tkinter.W,
)

column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=0
)  # 设置说明

# 第二排的开始
column += 1
row = 0
tkinter.Label(
    SCREEN,
    text="X轴刻度声明:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
x_scale = tkinter.Entry(SCREEN, width=gui_width * 2)
x_scale.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="X轴刻度起点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
start_x_plot = tkinter.Entry(SCREEN, width=gui_width * 2)
start_x_plot.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="X轴刻度终点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
start_x_polt = tkinter.Entry(SCREEN, width=gui_width * 2)
start_x_polt.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="X轴刻度间隔:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
span_x_plot = tkinter.Entry(SCREEN, width=gui_width * 2)
span_x_plot.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="Y轴刻度声明:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
y_scale = tkinter.Entry(SCREEN, width=gui_width * 2)
y_scale.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="Y轴刻度起点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
start_y_plot = tkinter.Entry(SCREEN, width=gui_width * 2)
start_y_plot.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="Y轴刻度终点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
end_y_plot = tkinter.Entry(SCREEN, width=gui_width * 2)
end_y_plot.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="Y轴刻度间隔:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
span_y_plot = tkinter.Entry(SCREEN, width=gui_width * 2)
span_y_plot.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="X轴显示起点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
start_x_limit = tkinter.Entry(SCREEN, width=gui_width * 2)
start_x_limit.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="X轴显示终点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
end_x_limit = tkinter.Entry(SCREEN, width=gui_width * 2)
end_x_limit.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="Y轴显示起点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
start_y_limit = tkinter.Entry(SCREEN, width=gui_width * 2)
start_y_limit.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="Y轴显示终点:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
end_y_limit = tkinter.Entry(SCREEN, width=gui_width * 2)
end_y_limit.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="帧率(帧/ms):",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
frame_rate = tkinter.Entry(SCREEN, width=gui_width * 2)
frame_rate.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
show_point = tkinter.IntVar()
show_best_value = tkinter.IntVar()
show_text = tkinter.IntVar()

tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="显示记忆点",
    variable=show_point,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="显示最值",
    variable=show_best_value,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="显示文字",
    variable=show_text,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
# 显示函数的xy
plot_type = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 4
)  # 暂时不启用多选
plot_type.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=3,
    sticky=tkinter.S + tkinter.N + tkinter.E + tkinter.W,
)
plot_type.insert(
    tkinter.END,
    *[
        "笛卡尔坐标系静态图像(默认)",
        "矩形坐标系静态图像",
        "笛卡尔坐标系动态图像",
        "矩形坐标系动态图像",
        "笛卡尔坐标系静态图像(无线框)",
        "矩形坐标系静态图像(无线框)",
        "笛卡尔坐标系动态图像(无线框)",
        "矩形坐标系动态图像(无线框)",
        "笛卡尔坐标系动态画图",
        "矩形坐标系动态画图",
    ],
)
row += 3
# 显示函数的xy
prompt_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 2
)  # 暂时不启用多选
prompt_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=2,
    sticky=tkinter.S + tkinter.N + tkinter.E + tkinter.W,
)

column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=0
)  # 设置说明

column += 1
row = 0
tkinter.Label(
    SCREEN,
    text="计算(y):",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
x_value = tkinter.Entry(SCREEN, width=gui_width * 2)
x_value.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="二分法计算(x):",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
y_value = tkinter.Entry(SCREEN, width=gui_width * 2)
y_value.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

dicon_parameters = []  # 二分法参数输入
name_list = [
    "最大迭代数",
    "计算精度",
    "最值允许偏移量",
    "零点最小间隔",
    "减少计算",
    "允许梯度计算",
    "最大扩张深度",
    "扩张限制",
    "扩张偏移量",
    "开启二级验证",
    "二级验证程度",
]
for i in range(11):
    row += 1
    dicon_parameters.append(tkinter.StringVar())
    tkinter.Label(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        text=name_list[i] + ":",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    tkinter.Entry(
        SCREEN, width=gui_width * 2, textvariable=dicon_parameters[-1]
    ).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="梯度法计算(x):",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
y_value_gradient = tkinter.Entry(SCREEN, width=gui_width * 2)
y_value_gradient.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

gradient_parameters = []  # 梯度法法参数输入
name_list = ["梯度起点", "梯度终点", "计算深度", "计算精度"]
for i in range(4):
    row += 1
    gradient_parameters.append(tkinter.StringVar())
    tkinter.Label(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        text=name_list[i] + ":",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    tkinter.Entry(
        SCREEN, width=gui_width * 2, textvariable=gradient_parameters[-1]
    ).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, height=1).grid(
    column=1, row=row
)  # 底部

column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=0
)  # 设置说明

column += 1
row = 0

tkinter.Label(
    SCREEN,
    text="代数法计算(x):",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
y_value_symbol = tkinter.Entry(SCREEN, width=gui_width * 2)
y_value_symbol.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="求(x)导数:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
x_value_derivation = tkinter.Entry(SCREEN, width=gui_width * 2)
x_value_derivation.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="逼近求导精度:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
proximity_accuracy = tkinter.Entry(SCREEN, width=gui_width * 2)
proximity_accuracy.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="计算(y)",
    command=calculate,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="二分法计算(x)",
    command=dichotomy,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="梯度法计算(x)",
    command=gradient_method_calculation,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row)

row += 1
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="代数法计算",
    command=sympy_calculation_x,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.N + tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="逼近法导数计算",
    command=approximation,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.N + tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="导数计算",
    command=function_differentiation,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.N + tkinter.E + tkinter.W)

row += 1
k = 5
result_box = tkinter.Listbox(SCREEN, height=gui_height * (k - 1))  # 暂时不启用多选
result_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=k,
    sticky=tkinter.N + tkinter.E + tkinter.W,
)

row += k - 1
tkinter.Label(
    SCREEN,
    text="性质预测值:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row, sticky=tkinter.N + tkinter.S
)  # 设置说明
projection_value = tkinter.Entry(SCREEN, width=gui_width * 2)
projection_value.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="周期性",
    command=check_periodic,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.N + tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="对称轴",
    command=check_symmetry_axis,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.N + tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="对称中心",
    command=check_center_of_symmetry,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.N + tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="单调性",
    command=check_monotonic,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3, sticky=tkinter.N + tkinter.E + tkinter.W
)

row += 1
# 显示函数的xy
projection_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 5
)  # 暂时不启用多选
projection_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=6,
    sticky=tkinter.S + tkinter.N + tkinter.E + tkinter.W,
)

column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=0
)  # 设置说明

column += 1
row = 0
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="生成表格",
    command=to_sheet,
    font=FONT,
    width=gui_width * 2,
    height=gui_height,
).grid(column=column, row=row, columnspan=2)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="导出表格",
    command=save_to_csv,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row)

row += 1
# 显示函数的xy
sheet_box = tkinter.Listbox(SCREEN, width=gui_width * 3)  # 暂时不启用多选
sheet_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=17,
    sticky=tkinter.S + tkinter.N + tkinter.E + tkinter.W,
)

output_prompt("加载完毕")
