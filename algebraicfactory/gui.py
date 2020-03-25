import tkinter
import tkinter.messagebox
import tkinter.font as tkfont
import os

from algebraicfactory.controller import AlgebraPolynomial
from system import exception_catch, QueueController


queue_controller = QueueController()
algebra_list = []
variable_list = []
SCREEN = tkinter.Tk()
bg_color = "#FFFAFA"  # 主颜色
buttom_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
SCREEN["bg"] = bg_color
FONT = ("黑体", 11)  # 设置字体
FONT2 = ("Fixdsys", 16)
FONT3 = tkfont.Font(family="Fixdsys", size=11)
SCREEN.title("CoTan代数工厂")
SCREEN.resizable(width=False, height=False)
SCREEN.geometry("+10+10")  # 设置所在位置
SCREEN.iconbitmap(bitmap=f'Pic{os.sep}favicon.ico', default=f'Pic{os.sep}favicon.ico')
option_list = []
value_algebra_dict = {}  # Sub替换字典
left_value = None  # 选定的Sub符号
right_algebra = None  # 选定的Sub代数式
algebra_value_dict = {}  # Sub替换字典
right_value = None  # 选定的Sub符号
left_algebra = None  # 选定的Sub代数式
value_sub_dict = {}  # 代数运算空列表
left_equation = None
right_equation = None
equation_set = []
equation_solution_set = []
left_inequality = None
right_inequality = None
p2d_value = None  # 画图
p3d_value = None
prompt_num = 0
gui_width = 13  # 标准宽度
gui_height = 2
row = 0
column = 0
new_text = None


class UIAPI:
    @staticmethod
    @exception_catch()
    def update_simultaneous_equations_box_gui():
        box = []
        if left_equation is not None or right_equation is not None:
            box.append(f"(选定){left_equation} = {right_equation}")
        for i in equation_set:
            box.append(f"{i[0]} = {i[1]}")
        equation_box.delete(0, tkinter.END)
        equation_box.insert(tkinter.END, *box)

    @staticmethod
    @exception_catch()
    def get_merge_func_gui():
        return merge_func.get()

    @staticmethod
    @exception_catch()
    def add_variable_assignment_gui():
        return number.get(), number_type.get()

    @staticmethod
    @exception_catch()
    def algebraic_partition_gui():
        deep = deep_split.get()
        f = split_func.get().split(",")
        m = return_type.get()
        if m == 1:
            must = False
        else:
            must = True
        return deep, f, m, must

    @staticmethod
    @exception_catch()
    def algebraic_similarity_split_gui():
        name = API.get_algebraic_name_gui()
        value = similar_items.get().split("#")
        f = return_type.get()
        return f, name, value

    @staticmethod
    @exception_catch()
    def algebraic_factorization_gui():
        all_ = return_type.get()
        if all_ == 0:
            return True, False
        elif all_ == 1:
            return False, False
        else:
            return True, True

    @staticmethod
    @exception_catch()
    def askok_gui(message):
        return tkinter.messagebox.askokcancel('提示', message)

    @staticmethod
    @exception_catch()
    def get_algebraic_name_gui():
        global algebra_list, algebra_box
        try:
            name = algebra_list[algebra_box.curselection()[0]]
        except IndexError:
            API.output_prompt_gui("请选定代数式")
            raise
        return name

    @staticmethod
    @exception_catch()
    def add_algebraic_gui():
        alg_str = algebra_expression.get()
        name = algebra_name.get().replace(" ", "")
        ratdio_list = ratdio.get().split("#")
        try:
            the_ratdio = float(ratdio_list[0])
        except (ValueError, IndexError):
            the_ratdio = 1.7
        rat = bool(init_rationalization.get())
        inverse = bool(init_ignore_assumptions.get())
        the_standardization = bool(standardization.get())
        return alg_str, inverse, name, rat, the_ratdio, the_standardization

    @staticmethod
    @exception_catch()
    def update_predictions_box_gui(index):
        predictions_box.delete(0, tkinter.END)
        predictions_box.insert(tkinter.END, *algebra_controller.variable_prediction(index))

    @staticmethod
    @exception_catch()
    def update_symbol_algebraic_box_gui():
        global algebra_controller, variable_box, variable_list, algebra_box, algebra_list, option_list, on_hold_algebra
        # 保存符号
        re = algebra_controller()  # 0-value,1-alg
        variable_list = re[0][1]
        # 显示符号
        variable_box.delete(0, tkinter.END)
        variable_box.insert(tkinter.END, *re[0][0])
        # 保存代数式
        algebra_list = re[1][1]
        # 显示代数式
        algebra_box.delete(0, tkinter.END)
        algebra_box.insert(tkinter.END, *re[1][0])
        option_list = []
        on_hold_algebra.delete(0, tkinter.END)

    @staticmethod
    @exception_catch()
    def update_operation_box_gui():
        global on_hold_algebra, option_list
        re = []
        for i in range(len(option_list)):
            re.append(f"({i + 1}) --> {option_list[i]}")
        on_hold_algebra.delete(0, tkinter.END)
        on_hold_algebra.insert(tkinter.END, *re)

    @staticmethod
    @exception_catch()
    def get_on_hold_algebra_gui():
        return on_hold_algebra.curselection()[0]

    @staticmethod
    @exception_catch()
    def denominator_rationalization_gui():
        try:
            maximum = int(maximum_irrational_term.get())
        except ValueError:
            maximum = 4
        rationalized = bool(rationalized_unknown.get())
        return maximum, rationalized

    @staticmethod
    @exception_catch()
    def get_fully_divided_gui():
        deep = bool(fully_divided.get())
        return deep

    @staticmethod
    @exception_catch()
    def get_apart_gui():
        x = apart.get().replace(" ", "")
        if x == "":
            x = None
        return x

    @staticmethod
    @exception_catch()
    def get_trig_fully_expand_gui():
        return bool(trig_fully_expand.get())

    @staticmethod
    @exception_catch()
    def get_ignore_assumptions_gui():
        return not bool(ignore_assumptions.get())

    @staticmethod
    @exception_catch()
    def get_fully_expand_gui():
        deep = bool(fully_expand.get())
        return deep

    @staticmethod
    @exception_catch()
    def get_reduce_log_gui():
        return not bool(ignore_assumptions_log.get())

    @staticmethod
    @exception_catch()
    def get_expand_log_gui():
        return bool(log_fully_expand.get()), not bool(ignore_assumptions_log.get())

    @staticmethod
    @exception_catch()
    def get_standardization_gui():
        try:
            radio = float(simplify_ratio_input.get())
        except ValueError:
            radio = 1.7
        rat = bool(init_rationalization.get())
        inverse = bool(init_ignore_assumptions.get())
        name = API.get_algebraic_name_gui()
        return inverse, name, radio, rat

    @staticmethod
    @exception_catch()
    def get_factorization_gui():
        gaussian = bool(is_gaussian.get())
        deep = bool(fully_factor.get())
        rat = bool(factor_rat.get())
        try:
            modulus_num = int(modulus.get())
        except ValueError:
            modulus_num = None
        return deep, gaussian, modulus_num, rat

    @staticmethod
    @exception_catch()
    def get_is_expand_complex_gui():
        return bool(is_expand_complex.get())

    @staticmethod
    @exception_catch()
    def get_similar_items_gui():
        global similar_items_object
        return similar_items_object.get().split("#")

    @staticmethod
    @exception_catch()
    def get_valid_number_gui():
        global valid_number
        try:
            num = int(valid_number.get())
        except ValueError:
            num = 5
        return num

    @staticmethod
    @exception_catch()
    def get_value_algebra_box_index_gui():
        return value_algebra_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def update_value_algebraic_box_gui():
        global algebra_controller, variable_list, variable_box, value_algebra_dict, right_algebra, left_value
        global value_algebra_box
        box = []
        if left_value is not None or right_algebra is not None:
            box.append(f"选定:{left_value} = {right_algebra}")
        for v in value_algebra_dict:
            box.append(f"{v} = {value_algebra_dict[v]}")
        value_algebra_box.delete(0, tkinter.END)
        value_algebra_box.insert(tkinter.END, *box)

    @staticmethod
    @exception_catch()
    def get_algebra_value_box_index_gui():
        global algebra_value_box
        return algebra_value_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def update_algebraic_value_box_gui():
        global algebra_controller, algebra_value_dict, left_algebra, right_value, algebra_value_box
        box = []
        if right_value is not None or left_algebra is not None:
            box.append(f"选定:{left_algebra} = {right_value}")
        for v in algebra_value_dict:
            box.append(f"{v} = {algebra_value_dict[v]}")
        algebra_value_box.delete(0, tkinter.END)
        algebra_value_box.insert(tkinter.END, *box)

    @staticmethod
    @exception_catch()
    def get_variable_assignment_box_index_gui():
        global variable_assignment_box
        return variable_assignment_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def update_variable_assignment_box_gui():
        global algebra_controller, value_sub_dict, variable_assignment_box
        box = []
        for v in value_sub_dict:
            box.append(f"{v} = {value_sub_dict[v]}")
        variable_assignment_box.delete(0, tkinter.END)
        variable_assignment_box.insert(tkinter.END, *box)

    @staticmethod
    @exception_catch()
    def get_equation_box_index_gui():
        global equation_box
        return equation_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def update_equation_solution_box_gui(re):
        global equation_solution_box
        equation_solution_box.delete(0, tkinter.END)
        equation_solution_box.insert(tkinter.END, *re)

    @staticmethod
    @exception_catch()
    def equation_solution_set_gui():
        return equation_solution_set[equation_solution_box.curselection()[0]]

    @staticmethod
    @exception_catch()
    def update_inequality_solution_box_gui(get):
        inequality_solution_box.delete(0, tkinter.END)
        inequality_solution_box.insert(tkinter.END, *get)

    @staticmethod
    @exception_catch()
    def get_inequality_symbol_gui():
        return inequality_symbol.get()

    @staticmethod
    @exception_catch()
    def rewrite_algebra_gui():
        func = rewrite_func.get()
        rewrite = rewrite_object.get().split(",")
        deep = bool(rewrite_deep.get())
        name = API.get_algebraic_name_gui()
        if rewrite == [""]:
            rewrite = []
        return deep, func, name, rewrite

    @staticmethod
    @exception_catch()
    def update_inequality_box_gui():
        global left_inequality, right_inequality, inequality_symbol, inequality_box
        re = []
        if left_inequality is not None and right_inequality is not None:
            inequality_type = [">", "<", ">=", "<="][inequality_symbol.get()]
            re.append(f"{left_inequality} {inequality_type} {right_inequality}")
        else:
            if left_inequality is not None:
                re.append(f"左代数式:{left_inequality}")
            if right_inequality is not None:
                re.append(f"右代数式:{right_inequality}")
        inequality_box.delete(0, tkinter.END)
        inequality_box.insert(tkinter.END, *re)

    @staticmethod
    @exception_catch()
    def update_plot_value_gui():
        global plot_object_box, plot_type, p2d_value, p3d_value
        ty = plot_type.get()
        re = []
        try:
            if ty == 0:  # 2D
                re = [f"二维:{p2d_value[0]} -> ({p2d_value[1]},{p2d_value[2]})"]
            else:
                re = [
                    f"三维:{p2d_value[0]} -> ({p2d_value[1]},{p2d_value[2]})",
                    f"三维:{p3d_value[0]} -> ({p3d_value[1]},{p3d_value[2]})",
                ]
        except IndexError:
            pass
        plot_object_box.delete(0, tkinter.END)
        plot_object_box.insert(tkinter.END, *re)

    @staticmethod
    @exception_catch()
    def get_range_of_values_gui():
        global range_of_values
        return range_of_values.get().split(",")

    @staticmethod
    @exception_catch()
    def get_var_name_gui():
        global variable_list, variable_box
        return variable_list[variable_box.curselection()[0]]

    @staticmethod
    @exception_catch()
    def creat_tree_gui(bg_color_, h, str_, w):
        global new_text
        new_top = tkinter.Toplevel(bg=bg_color_)
        new_top.resizable(width=False, height=False)
        new_top.geometry("+10+10")  # 设置所在位置
        new_text = tkinter.Text(new_top, width=w, height=h)
        new_text.pack()
        new_text.delete(1.0, tkinter.END)
        new_text.insert(tkinter.END, str_)
        new_text.config(state=tkinter.DISABLED)

    @staticmethod
    @exception_catch()
    def creat_text_gui(font, paint_container, te, x, y):
        paint_container.create_text(x, y, font=font, text=te)

    @staticmethod
    @exception_catch()
    def make_artboard_gui(h, w):
        new_top = tkinter.Toplevel(bg=bg_color)
        new_top.resizable(width=False, height=False)
        new_top.geometry("+10+10")  # 设置所在位置
        paint_container = tkinter.Canvas(new_top, bg=bg_color, width=w, height=h)
        paint_container.pack()
        return paint_container, new_top

    @staticmethod
    @exception_catch()
    def draw_algebra_gui():
        return bool(bracket.get()), bool(log_bracket.get()), can_input.get().split(",")

    @staticmethod
    @exception_catch()
    def add_custom_symbol_gui():
        # 复选框系统
        parameter = []
        n = 0
        for i in is_complex:
            parameter.append(i.get())
            n += parameter[-1]
        if n == 1:  # 选一个设为True
            is_the_complex = [
                ["complex", "real", "imaginary"][parameter.index(1)],
                True,
            ]  # 对象，布尔
        elif n == 2:  # 选两个设为False
            is_the_complex = [
                ["complex", "real", "imaginary"][parameter.index(0)],
                False,
            ]  # 对象，布尔
        else:
            is_the_complex = None  # 其余
        parameter = []
        n = 0
        for i in is_positives:
            parameter.append(i.get())
            n += parameter[-1]
        if n == 1:  # 选一个设为True
            is_natural = [
                ["positive", "negative", "zero"][parameter.index(1)],
                True,
            ]  # 对象，布尔
        elif n == 2:  # 选两个设为False
            is_natural = [
                ["positive", "negative", "zero"][parameter.index(0)],
                False,
            ]  # 对象，布尔
        else:
            is_natural = None  # 其余
        return [
            is_generation.get(),
            is_rational.get(),
            is_prime.get(),
            is_even.get(),
            is_limited.get(),
            is_the_complex,
            is_natural,
            integer.get(),
        ]

    @staticmethod
    @exception_catch()
    def get_var_name_list_gui():  # 获取variable_name的name而不是box
        name_list = variable_name.get().split(",")
        return name_list

    @staticmethod
    @exception_catch()
    def output_prompt_gui(news):
        global prompt_box, prompt_num, SCREEN
        prompt_num += 1
        news = str(news)
        prompt_box.insert(0, news + f"({prompt_num})")
        SCREEN.update()


class API(UIAPI):
    @staticmethod
    @exception_catch()
    def algebraic_factorization():
        name = API.get_algebraic_name_gui()
        try:
            re = algebra_controller.split_mul(name, *API.algebraic_factorization_gui())
        except BaseException:
            API.output_prompt_gui("拆分失败")
            raise
        else:
            API.output_prompt_gui("拆分成功")
        if tkinter.messagebox.askokcancel("提示", f"{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?"):
            for in_alg in re[0]:
                algebra_controller.add_expression("", in_alg)
                API.update_symbol_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def draw_algebra_core():
        bracket_, log_bracket_, wh = API.draw_algebra_gui()
        name = API.get_algebraic_name_gui()
        get = algebra_controller.get_expression_from_name(name)
        try:
            w = int(wh[0])
            h = int(wh[1])
        except (ValueError, IndexError):
            w = 1000
            h = 300
        size = 20
        font = ("Fixdsys", size)
        x = 30
        y = 150
        plot_len = (size / 16) * 5.5
        paint_container, new_top = API.make_artboard_gui(h, w)
        for i in get:
            if i[0] == "A":
                te = f"{i[1]}"
                x += len(te) * plot_len
                API.creat_text_gui(font, paint_container, te, x, y)
                x += len(te) * plot_len
            elif i[0] == "B":
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "["]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                x, y, h = API.draw_algebra_son(
                    i[1], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # 底数
                dy = y
                y = h - 10
                x, y, q = API.draw_algebra_son(
                    i[2], paint_container, x, y, size - 5, [], bracket_, log_bracket_
                )  # 指数
                y = dy
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "]"]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
            elif i[0] == "C":
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "["]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                x, y, h = API.draw_algebra_son(
                    i[1], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # log符号
                if log_bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "("]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                x, y, q = API.draw_algebra_son(
                    i[2], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # 递归呼叫儿子
                if log_bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", ")"]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "]"]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
            elif i[0] == "D":
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "["]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                y -= 20
                a_x, y, h = API.draw_algebra_son(
                    i[1], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # log符号
                y += 40
                b_x, y, h = API.draw_algebra_son(
                    i[2], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # log符号
                n_x = max([a_x, b_x]) - x
                y -= 20
                x, y, h = API.draw_algebra_son(
                    [("A", "-" * int((n_x / (2 * plot_len))))],
                    paint_container,
                    x,
                    y,
                    size,
                    [],
                    bracket_,
                    log_bracket_,
                )  # log符号
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "]"]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
        API.output_prompt_gui("运算完毕")

    @staticmethod
    @exception_catch()
    def draw_algebra_son(n, paint_container, x, y, size, max_y, bracket_=True, log_bracket_=True):
        font = ("Fixdsys", size)
        plot_len = (size / 16) * 5.5
        for i in n:
            if i[0] == "A":  # 只有A才是真的画图，其他是移动坐标
                max_y.append(y)
                te = f"{i[1]}"
                x += len(te) * plot_len
                API.creat_text_gui(font, paint_container, te, x, y)
                x += len(te) * plot_len
            elif i[0] == "B":
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "["]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                x, y, h = API.draw_algebra_son(
                    i[1], paint_container, x, y, size, max_y, bracket_, log_bracket_
                )  # 底数
                dy = y
                y = h - 10
                x, y, q = API.draw_algebra_son(
                    i[2], paint_container, x, y, size - 5, max_y, bracket_, log_bracket_
                )  # 递归呼叫儿子
                y = dy
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "]"]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
            elif i[0] == "C":
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "["]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                x, y, h = API.draw_algebra_son(
                    i[1], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # log符号
                if log_bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "("]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                x, y, q = API.draw_algebra_son(
                    i[2], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # 递归呼叫儿子
                if log_bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", ")"]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "]"]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
            elif i[0] == "D":
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "["]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
                y -= 20
                a_x, y, h = API.draw_algebra_son(
                    i[1], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # log符号
                y += 40
                b_x, y, h = API.draw_algebra_son(
                    i[2], paint_container, x, y, size, [], bracket_, log_bracket_
                )  # log符号
                n_x = max([a_x, b_x]) - x
                y -= 20
                x, y, h = API.draw_algebra_son(
                    [("A", "-" * int((n_x / (2 * plot_len))))],
                    paint_container,
                    x,
                    y,
                    size,
                    [],
                    bracket_,
                    log_bracket_,
                )  # log符号
                if bracket_:
                    x, y, q = API.draw_algebra_son(
                        [["A", "]"]],
                        paint_container,
                        x,
                        y,
                        size - 5,
                        [],
                        bracket_,
                        log_bracket_,
                    )  # 递归呼叫儿子
        try:
            re = min(max_y)
        except ValueError:
            re = 150
        return x, y, re

    @staticmethod
    @exception_catch()
    def show_algebraic():
        str_ = algebra_controller.print_expression(API.get_algebraic_name_gui())
        try:
            wh = can_input.get().split(",")
            w = int(wh[0]) / 10
            h = int(wh[1]) / 10
        except (ValueError, IndexError):
            w = 40
            h = 20
        API.output_prompt_gui("系统运算中")
        API.creat_tree_gui(bg_color, h, str_, w)
        API.output_prompt_gui("运算完毕")

    @staticmethod
    @exception_catch()
    def clear_algebra():
        try:
            algebra_controller.clean_expression()
            API.update_symbol_algebraic_box_gui()
            API.output_prompt_gui("删除完成")
        except BaseException:
            API.output_prompt_gui("删除失败")
            raise

    @staticmethod
    @exception_catch()
    def del_algebra():
        name = API.get_algebraic_name_gui()
        try:
            algebra_controller.del_expression(name)
        except BaseException:
            API.output_prompt_gui("删除失败")
            raise
        else:
            API.update_symbol_algebraic_box_gui()
            API.output_prompt_gui("删除完成")

    @staticmethod
    @exception_catch()
    def del_symbol():
        name = API.get_var_name_gui()
        try:
            algebra_controller.del_symbol(name)
        except BaseException:
            API.output_prompt_gui("删除失败")
            raise
        else:
            API.update_symbol_algebraic_box_gui()
            API.output_prompt_gui("删除完成")

    @staticmethod
    @exception_catch()
    def get_plot_type():
        global plot_type
        return plot_type.get()

    @staticmethod
    @exception_catch()
    def drawing_image():
        try:
            the_plot_type = API.get_plot_type()
            if p2d_value is None:
                raise Exception
            if the_plot_type == 1 and p3d_value is None:
                raise Exception
            name = API.get_algebraic_name_gui()
            algebra_controller.plot(name, p2d_value, p3d_value)
        except BaseException:
            API.output_prompt_gui("画图失败")
            raise

    @staticmethod
    @exception_catch()
    def add_plot_value():
        global p2d_value, p3d_value
        try:
            try:
                value = API.get_var_name_gui()
            except BaseException:
                API.output_prompt_gui("请选定符号")
                raise
            value_range = API.get_range_of_values_gui()
            if value_range == [""]:
                value_range = [-10, 10]

            tup = [value] + [
                min((float(value_range[0]), float(value_range[1]))),
                max((float(value_range[0]), float(value_range[1]))),
            ]
            ty = API.get_plot_type()
        except BaseException:
            API.output_prompt_gui("修改失败")
            raise
        if p2d_value is None:
            p2d_value = tup
        elif p3d_value is None and ty == 1:
            if p2d_value[0] != tup[0]:
                p3d_value = tup
            else:
                p2d_value = tup
        else:
            if ty == 0:  # 2D
                p2d_value = tup
                p3d_value = None
            else:  # 3D
                if p2d_value[0] == tup[0]:
                    p2d_value = tup
                elif p3d_value[0] == tup[0]:
                    p3d_value = tup
                else:
                    p2d_value = p3d_value
                    p3d_value = tup
        API.output_prompt_gui("修改完成")
        API.update_plot_value_gui()

    @staticmethod
    @exception_catch()
    def rewrite_algebra():
        deep, func, name, rewrite = API.rewrite_algebra_gui()
        try:
            get = algebra_controller.rewrite_exp(name, func, rewrite, deep)
            API.output_prompt_gui("运行完成")
            API.apply_algebraic_tips(get, f"代数式重写的结果为:{get},是否应用？")
        except BaseException:
            API.output_prompt_gui("运行失败")
            raise

    @staticmethod
    @exception_catch()
    def inequality_solve():
        if left_inequality is not None and right_inequality is not None:
            type_ = API.get_inequality_symbol_gui()
            try:
                get = algebra_controller.solving_inequality(
                    [left_inequality, right_inequality], type_
                )
                API.update_inequality_solution_box_gui(get)
                API.output_prompt_gui("运行完成")
            except BaseException:
                API.output_prompt_gui("解不等式失败")
                raise

    @staticmethod
    @exception_catch()
    def add_left_algebra():
        global left_inequality
        left_inequality = API.get_algebraic_name_gui()
        API.update_inequality_box_gui()

    @staticmethod
    @exception_catch()
    def add_right_algebra():
        global right_inequality
        right_inequality = API.get_algebraic_name_gui()
        API.update_inequality_box_gui()

    @staticmethod
    @exception_catch()
    def add_to_algebraic_box():
        get = API.equation_solution_set_gui()[1]
        API.apply_algebraic_tips(get, f"联立结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def add_to_value_algebraic_box():
        get = API.equation_solution_set_gui()
        value_algebra_dict[get[0]] = get[1]
        API.update_value_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def add_to_algebraic_value_box():
        get = API.equation_solution_set_gui()
        algebra_value_dict[get[1]] = get[0]
        API.update_algebraic_value_box_gui()

    @staticmethod
    @exception_catch()
    def solve_simultaneous_equations():
        global equation_solution_set
        try:
            get = algebra_controller.solving_equations(equation_set)
            API.output_prompt_gui("运行成功")
        except BaseException:
            API.output_prompt_gui("解方程失败")
            raise
        equation_solution_set = []
        re = []
        for i in get:
            re.append(f"{i[0]} = {i[1]}")  # i[0]是一个字母=i[1]是一个代数式
            equation_solution_set.append((i[0], i[1]))
        API.update_equation_solution_box_gui(re)

    @staticmethod
    @exception_catch()
    def del_equation():
        global left_equation, right_equation
        num = API.get_equation_box_index_gui()
        if left_equation is not None or right_equation is not None:
            if num == 0:
                left_equation = None
                right_equation = None
            else:
                num -= 1
                del equation_set[num]
        else:
            del equation_set[num]
        API.update_simultaneous_equations_box_gui()

    @staticmethod
    @exception_catch()
    def generating_equation():
        global left_equation, right_equation
        if left_equation is not None and right_equation is not None:
            equation_set.append((left_equation, right_equation))
            left_equation = None
            right_equation = None
        API.update_simultaneous_equations_box_gui()

    @staticmethod
    @exception_catch()
    def add_equation_left():
        global left_equation
        left_equation = API.get_algebraic_name_gui()
        API.update_simultaneous_equations_box_gui()

    @staticmethod
    @exception_catch()
    def add_equation_right():
        global right_equation
        right_equation = API.get_algebraic_name_gui()
        API.update_simultaneous_equations_box_gui()

    @staticmethod
    @exception_catch()
    def algebraic_assignment():
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.algebraic_assignment(name, value_sub_dict)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("代数运算失败")
            raise
        API.apply_algebraic_tips(get, f"联立结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def del_variable_assignment():
        num = API.get_variable_assignment_box_index_gui()
        del value_sub_dict[list(value_sub_dict.keys())[num]]
        API.update_variable_assignment_box_gui()

    @staticmethod
    @exception_catch()
    def add_variable_assignment():
        try:
            value_name = API.get_variable_assignment_box_index_gui()
        except BaseException:
            API.output_prompt_gui("请选定符号")
            raise
        value_num = algebra_controller.creat_num(*API.add_variable_assignment_gui())  # 不同类型
        value_sub_dict[value_name] = value_num
        API.update_variable_assignment_box_gui()

    @staticmethod
    @exception_catch()
    def algebragic_value_simultaneous():
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.algebragic_value_simultaneous(name, algebra_value_dict)
            API.output_prompt_gui("反向联立完成")
        except BaseException:
            API.output_prompt_gui("无法联立")
            raise
        API.apply_algebraic_tips(get, f"联立结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def del_algebraic_value_simultaneousness():
        global left_algebra, right_value
        num = API.get_algebra_value_box_index_gui()
        if right_value is not None or left_algebra is not None:
            if num == 0:
                right_value = None
                left_algebra = None
            else:
                num -= 1
                del algebra_value_dict[list(algebra_value_dict.keys())[num]]
        else:
            del algebra_value_dict[list(algebra_value_dict.keys())[num]]
        API.update_algebraic_value_box_gui()

    @staticmethod
    @exception_catch()
    def add_algebraic_values_simultaneously():
        global left_algebra, right_value
        if right_value is not None and left_algebra is not None:
            algebra_value_dict[left_algebra] = right_value
            right_value, left_algebra = None, None
        API.update_algebraic_value_box_gui()

    @staticmethod
    @exception_catch()
    def add_left_simultaneous_algebra():  # 代数式=值的左代数式
        global left_algebra
        alg_name = API.get_algebraic_name_gui()
        left_algebra = alg_name
        API.update_algebraic_value_box_gui()

    @staticmethod
    @exception_catch()
    def add_right_simultaneous_values():  # 解释同上
        global right_value
        try:
            value_name = API.get_var_name_gui()
        except BaseException:
            API.output_prompt_gui("请选定符号")
            raise
        right_value = value_name
        API.update_algebraic_value_box_gui()

    @staticmethod
    @exception_catch()
    def value_algebraic_simultaneous():
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.value_algebraic_simultaneous(name, value_algebra_dict)
            API.output_prompt_gui("联立完成")
        except BaseException:
            API.output_prompt_gui("无法联立")
            raise
        API.apply_algebraic_tips(get, f"联立结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def del_value_algebraic_simultaneous():
        global right_algebra, left_value
        num = API.get_value_algebra_box_index_gui()
        if left_value is not None or right_algebra is not None:
            if num == 0:
                left_value = None
                right_algebra = None
            else:
                num -= 1
                del value_algebra_dict[list(value_algebra_dict.keys())[num]]
        else:
            del value_algebra_dict[list(value_algebra_dict.keys())[num]]
        API.update_value_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def add_value_algebraic_simultaneous():
        global right_algebra, left_value
        if left_value is not None and right_algebra is not None:
            value_algebra_dict[left_value] = right_algebra
            left_value, right_algebra = None, None
        API.update_value_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def add_right_simultaneous_algebra():
        global right_algebra
        alg_name = API.get_algebraic_name_gui()
        right_algebra = alg_name
        API.update_value_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def add_left_simultaneous_values():
        global left_value
        try:
            value_name = API.get_var_name_gui()
        except BaseException:
            API.output_prompt_gui("请选定符号")
            raise
        left_value = value_name
        API.update_value_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def algebraic_digitization():
        try:
            get = (algebra_controller
                   .algebraic_digitization(API.get_algebraic_name_gui(), API.get_valid_number_gui()))
            API.output_prompt_gui("数字化完成")
        except BaseException:
            API.output_prompt_gui("数字化失败")
            raise
        API.apply_algebraic_tips(get, f"数字化的结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def expand_special():
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.expand_special(name)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"展开特殊函数的结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def expand_complex():
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.expand_complex(name)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"展开虚数的结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def merger_of_similar_items():
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.merger_of_similar_items(name, API.get_similar_items_gui())
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"合并同类项的结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def general_expansion():
        complex_ = API.get_is_expand_complex_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.expansion(name, complex_)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"普遍展开的结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def factorization():
        name = API.get_algebraic_name_gui()
        deep, gaussian, modulus_num, rat = API.get_factorization_gui()
        try:
            get = algebra_controller.factor(name, modulus_num, gaussian, deep, rat)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"因式分解的结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def simplify_standardization():
        inverse, name, radio, rat = API.get_standardization_gui()
        try:
            get = algebra_controller.simplify(name, radio, rat=rat, inv=inverse)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"化简(标准化)为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def apply_algebraic_tips(re, message):
        if API.askok_gui(message):
            algebra_controller.add_expression("", re)
            API.update_symbol_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def expand_log():
        deep, ignore_assumptions_ = API.get_expand_log_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.log_expansion(name, ignore_assumptions_, deep)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"展开对数结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def reduce_log():
        ignore = API.get_reduce_log_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.log_simp(name, ignore)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"化简对数结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def expand_mul():
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.mul_expansion(name)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"展开乘法结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def expand_additive_index():
        global algebra_controller, ignore_assumptions
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.multinomial_expansion(name)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"展开加法式幂结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def composite_index():
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.pow_simp_multinomial(name)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"合成幂指数的结果为:{get},是否应用？(彻底化简加法式幂可以使用因式分解)")

    @staticmethod
    @exception_catch()
    def expand_exp_base():
        deep = API.get_fully_expand_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.pow_expansion_base(name, deep)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"展开指数底数结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def expand_exp_index():
        deep = API.get_fully_expand_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.pow_expansion_exp(name, deep)
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"展开指数幂结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def expand_power():
        deep = API.get_fully_expand_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.pow_expansion_core(name, deep)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"展开指数结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def reduce_exp_base():
        ignore = API.get_ignore_assumptions_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.pow_simp_base(name, ignore)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"化简指数底数结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def reduce_exp_index():
        ignore = API.get_ignore_assumptions_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.pow_simp_exp(name, ignore)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"化简指数幂结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def reduced_power():
        ignore = API.get_ignore_assumptions_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.pow_simp_core(name, ignore)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"化简指数结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def reduced_trigonometric():  # 三角函数化简
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.trig_simp(name)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"三角化简结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def expand_trigonometric():  # 三角展开
        deep = API.get_trig_fully_expand_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.trig_expansion(name, deep)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"三角展开结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def fractional_division():  # 通分
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.fractional_merge(name)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"分式通分结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def fraction_reduction():  # 约分
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.fraction_reduction(name)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"分式约分结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def fractional_fission():  # 裂项
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.fractional_fission(name, API.get_apart_gui())
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"分式裂项结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def fractional_synthesis():  # together
        deep = API.get_fully_divided_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.as_fraction(name, deep)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"合成分式结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def denominator_rationalization():  # 分母有理化
        maximum, rationalized = API.denominator_rationalization_gui()
        name = API.get_algebraic_name_gui()
        try:
            get = algebra_controller.fractional_rat(name, rationalized, maximum)
            API.output_prompt_gui("运算成功")
        except BaseException:
            API.output_prompt_gui("运算失败")
            raise
        API.apply_algebraic_tips(get, f"分母有理化结果为:{get},是否应用？")

    @staticmethod
    @exception_catch()
    def add_operation_algebra():
        name = API.get_algebraic_name_gui()
        if name is None:
            raise
        option_list.append(name)
        API.update_operation_box_gui()

    @staticmethod
    @exception_catch()
    def del_operation_algebra():
        del option_list[API.get_on_hold_algebra_gui()]
        API.update_operation_box_gui()

    @staticmethod
    @exception_catch()
    def clear_operational_algebra():
        API.update_symbol_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def algebraic_composition():
        global algebra_controller, option_list
        name = option_list.copy()
        if len(name) < 2:
            raise Exception
        try:
            re = algebra_controller.merge_func(name, API.get_merge_func_gui())
            API.output_prompt_gui("合成成功")
        except BaseException:
            API.output_prompt_gui("合成失败")
            raise
        API.apply_algebraic_tips(re, f"合成结果为:{re}，是否应用?")

    @staticmethod
    @exception_catch()
    def algebraic_multiplication():
        name = option_list.copy()
        if len(name) < 2:
            raise Exception
        try:
            re = algebra_controller.merge_mul(name)
            API.output_prompt_gui("合成成功")
        except BaseException:
            API.output_prompt_gui("合成失败")
            raise
        API.apply_algebraic_tips(re, f"合成结果为:{re}，是否应用?")

    @staticmethod
    @exception_catch()
    def algebraic_addition():
        name = option_list.copy()
        if len(name) < 2:
            raise Exception
        try:
            re = algebra_controller.merge_add(name)
            API.output_prompt_gui("合成成功")
        except BaseException:
            API.output_prompt_gui("合成失败")
            raise
        API.apply_algebraic_tips(re, f"合成结果为:{re}，是否应用?")

    @staticmethod
    @exception_catch()
    def algebraic_partition():
        name = API.get_algebraic_name_gui()
        deep, f, m, must = API.algebraic_partition_gui()
        try:
            re = algebra_controller.split_func(name, deep, f, must)
            API.output_prompt_gui("拆分成功")
        except BaseException:
            API.output_prompt_gui("拆分失败")
            raise
        API.split_apply_algebraic_tips(re, f"{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?")

    @staticmethod
    @exception_catch()
    def split_apply_algebraic_tips(re, message):
        if API.askok_gui(message):
            for in_alg in re[0]:
                algebra_controller.add_expression("", in_alg)
                API.update_symbol_algebraic_box_gui()

    @staticmethod
    @exception_catch()
    def algebraic_similarity_split():
        f, name, value = API.algebraic_similarity_split_gui()
        try:
            re = algebra_controller.split_add(name, value, f)
            API.output_prompt_gui("拆分成功")
        except BaseException:
            API.output_prompt_gui("拆分失败")
            raise
        API.split_apply_algebraic_tips(re, f"{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?")

    @staticmethod
    @exception_catch()
    def add_algebraic():
        try:
            (
                alg_str,
                inverse,
                name,
                rat,
                the_ratdio,
                the_standardization,
            ) = API.add_algebraic_gui()
            if the_standardization:  # 标准化
                new_alg = algebra_controller.simplify(
                    alg_str, ratdio=the_ratdio, rat=rat, inv=inverse
                )
                alg_str = API.application(alg_str, new_alg)

            algebra_controller.add_expression(name, alg_str)

            API.update_symbol_algebraic_box_gui()
            API.output_prompt_gui("代数式新增成功")
        except BaseException:
            API.output_prompt_gui("新增代数式无法应用")
            raise

    @staticmethod
    @exception_catch()
    def application(alg_str, new_alg):
        if new_alg is not None and API.askok_gui(f"约简函数为:{new_alg}，是否应用?"):
            alg_str = new_alg
        return alg_str

    @staticmethod
    @exception_catch()
    def get_predictions():
        global variable_box, variable_list, algebra_controller, predictions_box
        try:
            try:
                index = API.get_var_name_gui()
            except BaseException:
                API.output_prompt_gui("请选定符号")
                raise
            API.update_predictions_box_gui(index)
            API.output_prompt_gui("性质预测成功")
        except BaseException:
            API.output_prompt_gui("性质预测失败")
            raise

    @staticmethod
    @exception_catch()
    def add_custom_symbol():  # 添加自定义Symbol
        try:
            API.__add_symbot_core(*API.add_custom_symbol_gui())
        except BaseException:
            API.output_prompt_gui("自定义符号新增失败")
            raise

    @staticmethod
    @exception_catch()
    def add_real():  # 添加实数符号
        API.__add_symbot_core(is_complex_=["real", True], describe_="实数(且复数)符号")

    @staticmethod
    @exception_catch()
    def add_integer():  # 添加整数符号
        API.__add_symbot_core(is_integer_=1, describe_="整数(且实数)符号")

    @staticmethod
    @exception_catch()
    def add_non_negative_real():  # 非负实数
        API.__add_symbot_core(
            is_natural_=["negative", False], is_complex_=["real", True], describe_="非负实数符号"
        )

    @staticmethod
    @exception_catch()
    def add_even():  # 偶数
        API.__add_symbot_core(is_even_=1, describe_="偶数(且整数)符号")

    @staticmethod
    @exception_catch()
    def add_odd():  # 奇数
        API.__add_symbot_core(is_even_=2, describe_="奇数(且整数)符号")

    @staticmethod
    @exception_catch()
    def add_positive_real():  # 正实数
        API.__add_symbot_core(
            is_natural_=["positive", True], is_complex_=["real", True], describe_="正实数符号"
        )

    @staticmethod
    @exception_catch()
    def add_positive_integer():  # 正整数
        API.__add_symbot_core(is_natural_=["positive", True], is_integer_=1, describe_="正整数符号")

    @staticmethod
    @exception_catch()
    def add_natural():  # 自然数
        API.__add_symbot_core(
            is_natural_=["negative", False], is_integer_=1, describe_="自然数(非负整数)符号"
        )

    @staticmethod
    @exception_catch()
    def add_no_constraints():  # 无约束
        API.__add_symbot_core(no_constraint_=1, describe_="仅满足交换律的无约束符号")

    @staticmethod
    @exception_catch()
    def __add_symbot_core(
        is_generation_=0,
        is_rational_=0,
        is_prime_=0,
        is_even_=0,
        is_finite_=0,
        is_complex_=None,
        is_natural_=None,
        is_integer_=0,
        no_constraint_=0,
        describe_="自定义符号",
    ):
        # 代数，有理，质数，偶数，有限实数，复数，正负，整数，取消
        name_list = API.get_var_name_list_gui()
        for name in name_list:
            try:
                if not algebra_controller.add_symbol(
                    name,
                    is_generation_,
                    is_rational_,
                    is_prime_,
                    is_even_,
                    is_finite_,
                    is_complex_,
                    is_natural_,
                    is_integer_,
                    no_constraint_,
                    describe_,
                ):
                    raise Exception
            except BaseException:
                API.output_prompt_gui(f"新增“{name}”失败")
                raise
        API.output_prompt_gui(f"新增“{describe_}”完成")
        API.update_symbol_algebraic_box_gui()


def algebraic_factory_main(in_queue, out_queue):
    global SCREEN
    API.output_prompt_gui("加载完成")
    queue_controller.set_queue(in_queue, out_queue)
    queue_controller()
    SCREEN.mainloop()
    queue_controller.stop_process()


algebra_controller = AlgebraPolynomial(API.output_prompt_gui)
tkinter.Label(
    SCREEN,
    text="符号名字:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
variable_name = tkinter.Entry(SCREEN, width=gui_width * 2)
variable_name.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="实数符号(R)",
    command=API.add_real,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="整数符号(Z)",
    command=API.add_integer,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="非负实数符号",
    command=API.add_non_negative_real,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="偶数符号",
    command=API.add_even,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="奇数符号",
    command=API.add_odd,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="正数符号",
    command=API.add_positive_real,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="自然数符号",
    command=API.add_natural,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="正整数符号",
    command=API.add_positive_integer,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="无约束符号",
    command=API.add_no_constraints,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
is_generation = tkinter.IntVar()  # 代数或者超越数
lable = ["均可", "代数", "超越数"]
for i in range(3):
    tkinter.Radiobutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=is_generation,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
is_rational = tkinter.IntVar()  # 有理数或者无理数
lable = ["均可", "有理数", "无理数"]
for i in range(3):
    tkinter.Radiobutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=is_rational,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
is_prime = tkinter.IntVar()  # 质数合数
lable = ["均可", "质数", "合数"]
for i in range(3):
    tkinter.Radiobutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=is_prime,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
is_even = tkinter.IntVar()  # 奇数偶数
lable = ["均可", "偶数", "奇数"]
for i in range(3):
    tkinter.Radiobutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=is_even,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
is_complex = []  # 实数虚数
lable = ["复数", "实数", "虚数"]
for i in range(3):
    is_complex.append(tkinter.IntVar())
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=is_complex[-1],
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
is_positives = []  # 正，负，0
lable = ["正数", "负数", "零"]  # 复选框
for i in range(3):
    is_positives.append(tkinter.IntVar())
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=is_positives[-1],
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
is_limited = tkinter.IntVar()  # 实数
lable = ["均可", "有限实数", "无穷数", "广义实数"]
for i in range(3):
    tkinter.Radiobutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=is_limited,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)
row += 1
tkinter.Radiobutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text=lable[3],
    variable=is_limited,
    value=3,
).grid(
    column=column, row=row, sticky=tkinter.W
)  # 同上的

integer = tkinter.IntVar()
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="整数",
    variable=integer,
).grid(column=column + 2, row=row, sticky=tkinter.W)

row += 1
variable_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 4
)  # 显示符号
variable_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=6,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 6
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="自定义符号",
    command=API.add_custom_symbol,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="查看假设",
    command=API.get_predictions,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 1, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除符号",
    command=API.del_symbol,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数

row += 1
predictions_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 5
)  # 显示函数假设
predictions_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=5,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=0
)
column += 1
row = 0
tkinter.Label(
    SCREEN,
    text="代数式:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
algebra_expression = tkinter.Entry(SCREEN, width=gui_width * 2)
algebra_expression.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="标识:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
algebra_name = tkinter.Entry(SCREEN, width=gui_width * 2)
algebra_name.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="标准:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
ratdio = tkinter.Entry(SCREEN, width=gui_width * 2)
ratdio.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
init_rationalization = tkinter.IntVar()
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="有理化",
    variable=init_rationalization,
).grid(column=column, row=row, sticky=tkinter.W)

init_ignore_assumptions = tkinter.IntVar()
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="忽略假设",
    variable=init_ignore_assumptions,
).grid(column=column + 2, row=row, sticky=tkinter.W)

standardization = tkinter.IntVar()
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="标准化",
    variable=standardization,
).grid(column=column + 1, row=row, sticky=tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="清空代数式",
    command=API.clear_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="生成代数式",
    command=API.add_algebraic,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 1, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除代数式",
    command=API.del_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
algebra_box = tkinter.Listbox(SCREEN, width=gui_width * 3)  # 显示代数式
algebra_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 4
tkinter.Label(
    SCREEN,
    text="重写对象:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
rewrite_object = tkinter.Entry(SCREEN, width=gui_width * 2)
rewrite_object.grid(
    column=column + 1, columnspan=2, row=row, sticky=tkinter.W + tkinter.E
)

row += 1
tkinter.Label(
    SCREEN,
    text="重写方法:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
rewrite_func = tkinter.Entry(SCREEN, width=gui_width * 2)
rewrite_func.grid(
    column=column + 1, columnspan=2, row=row, sticky=tkinter.W + tkinter.E
)

row += 1
rewrite_deep = tkinter.IntVar()
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="重写子代数式",
    variable=rewrite_deep,
).grid(column=column + 2, row=row, sticky=tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="重写代数式",
    command=API.rewrite_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="同类项:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
similar_items = tkinter.Entry(SCREEN, width=gui_width * 2)
similar_items.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
return_type = tkinter.IntVar()  # 正，负，0
lable = ["仅系数(同类项)", "仅代数式", "均保留"]  # 复选框
for i in range(3):
    tkinter.Radiobutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=return_type,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="拆分函数:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
split_func = tkinter.Entry(SCREEN, width=gui_width)
split_func.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
deep_split = tkinter.IntVar()
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="完全拆分",
    variable=deep_split,
).grid(column=column + 2, row=row, sticky=tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="同类项拆分",
    command=API.algebraic_similarity_split,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="乘法拆分",
    command=API.algebraic_factorization,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 1, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="函数拆分",
    command=API.algebraic_partition,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
on_hold_algebra = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 4
)  # 显示代数式
on_hold_algebra.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 4
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="添加",
    command=API.add_operation_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="清空",
    command=API.clear_operational_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 1, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除",
    command=API.del_operation_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="合成函数:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
merge_func = tkinter.Entry(SCREEN, width=gui_width * 2)
merge_func.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="多项式合成",
    command=API.algebraic_addition,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="因式合成",
    command=API.algebraic_multiplication,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 1, row=row, sticky=tkinter.E + tkinter.W
)  # 添加函数
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="函数合成",
    command=API.algebraic_composition,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="有效数字:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 1, row=row
)  # 设置说明
valid_number = tkinter.Entry(SCREEN, width=gui_width)
valid_number.grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="代数式数字化",
    command=API.algebraic_digitization,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=0
)

column += 1
row = 0
tkinter.Label(
    SCREEN,
    text="【分式恒等变形】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

row += 1
fully_divided = tkinter.IntVar()
tkinter.Label(
    SCREEN,
    text="裂项关注对象:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
apart = tkinter.Entry(SCREEN, width=gui_width)
apart.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="完全转化分式",
    variable=fully_divided,
).grid(column=column + 2, row=row, sticky=tkinter.W)

row += 1
rationalized_unknown = tkinter.IntVar()
tkinter.Label(
    SCREEN,
    text="最大无理项:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
maximum_irrational_term = tkinter.Entry(SCREEN, width=gui_width)
maximum_irrational_term.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="有理化符号分母",
    variable=rationalized_unknown,
).grid(column=column + 2, row=row, sticky=tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="最小公分母",
    command=API.fractional_division,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="分式约分",
    command=API.fraction_reduction,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="分式裂项",
    command=API.fractional_fission,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="分母有理化",
    command=API.denominator_rationalization,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="转化为分式(小改动)",
    command=API.fractional_synthesis,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="【三角恒等变换】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

row += 1
trig_fully_expand = tkinter.IntVar()
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开三角函数",
    command=API.expand_trigonometric,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="三角函数合成",
    command=API.reduced_trigonometric,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="完全展开",
    variable=trig_fully_expand,
).grid(column=column + 2, row=row, sticky=tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="【乘法、指数、对数恒等变形】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

row += 1
ignore_assumptions = tkinter.IntVar()
fully_expand = tkinter.IntVar()
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="忽略假设",
    variable=ignore_assumptions,
).grid(column=column + 1, row=row, sticky=tkinter.W)

tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="完全展开",
    variable=fully_expand,
).grid(column=column, row=row, sticky=tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开乘法",
    command=API.expand_mul,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开加法式幂",
    command=API.expand_additive_index,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="指数合成",
    command=API.composite_index,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="化简指数底数",
    command=API.reduce_exp_base,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="化简指数幂",
    command=API.reduce_exp_index,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="化简指数",
    command=API.reduced_power,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开指数底数",
    command=API.expand_exp_base,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开指数幂",
    command=API.expand_exp_index,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开指数",
    command=API.expand_power,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

ignore_assumptions_log = tkinter.IntVar()
log_fully_expand = tkinter.IntVar()

row += 1
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="完全展开",
    variable=log_fully_expand,
).grid(column=column, row=row, sticky=tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="忽略假设",
    variable=ignore_assumptions_log,
).grid(column=column + 1, row=row, sticky=tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开对数",
    command=API.expand_log,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="化简对数",
    command=API.reduce_log,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="【虚数与特殊函数】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开特殊函数",
    command=API.expand_special,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开虚数",
    command=API.expand_complex,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="【普遍操作类】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明
row += 1
tkinter.Label(
    SCREEN,
    text="简化方案:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
simplify_func_Input = tkinter.Entry(SCREEN, width=gui_width)  # 简化方案
simplify_func_Input.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="有理化",
    variable=init_rationalization,
).grid(column=column + 2, row=row, sticky=tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="简化比率:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
simplify_ratio_input = tkinter.Entry(SCREEN, width=gui_width)  # 简化比率
simplify_ratio_input.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="忽略假设",
    variable=init_ignore_assumptions,
).grid(column=column + 2, row=row, sticky=tkinter.W)

is_gaussian = tkinter.IntVar()
fully_factor = tkinter.IntVar()
factor_rat = tkinter.IntVar()
row += 1
tkinter.Label(
    SCREEN,
    text="模数:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
modulus = tkinter.Entry(SCREEN, width=gui_width)  # 简化比率
modulus.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="高斯因式分解",
    variable=is_gaussian,
).grid(column=column + 2, row=row, sticky=tkinter.W)

row += 1
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="完全因式分解",
    variable=fully_factor,
).grid(column=column, row=row, sticky=tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="因式分解有理代数式",
    variable=factor_rat,
).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.W)

row += 1
is_expand_complex = tkinter.IntVar()
tkinter.Label(
    SCREEN,
    text="同类项对象:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
similar_items_object = tkinter.Entry(SCREEN, width=gui_width)
similar_items_object.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="展开复数",
    variable=is_expand_complex,
).grid(column=column + 2, row=row, sticky=tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="化简标准化",
    command=API.simplify_standardization,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="普遍运算展开",
    command=API.general_expansion,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="因式分解",
    command=API.factorization,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="合并同类项",
    command=API.merger_of_similar_items,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, columnspan=3, sticky=tkinter.E + tkinter.W)

column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=0
)
column += 1

row = 0
tkinter.Label(
    SCREEN,
    text="【联立操作】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="选定符号",
    command=API.add_left_simultaneous_values,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="选定代数式",
    command=API.add_right_simultaneous_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="新键联立",
    command=API.add_value_algebraic_simultaneous,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="生成联立代数式",
    command=API.value_algebraic_simultaneous,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除联立",
    command=API.del_value_algebraic_simultaneous,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
value_algebra_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 4
)  # 显示代数式
value_algebra_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 4
tkinter.Label(
    SCREEN,
    text="【反向联立操作】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

# 反向联立系统
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="选定代数式",
    command=API.add_left_simultaneous_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="选定符号",
    command=API.add_right_simultaneous_values,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="新键联立",
    command=API.add_algebraic_values_simultaneously,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="生成联立代数式",
    command=API.algebragic_value_simultaneous,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除联立",
    command=API.del_algebraic_value_simultaneousness,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
algebra_value_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 4
)  # 显示代数式
algebra_value_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

# 代数运算
row += 4
tkinter.Label(
    SCREEN,
    text="【赋值运算操作】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

row += 1
tkinter.Label(
    SCREEN,
    text="数值:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
number = tkinter.Entry(SCREEN, width=gui_width + 2)
number.grid(column=column + 1, row=row, sticky=tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="指定符号",
    command=API.add_variable_assignment,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
number_type = tkinter.IntVar()  # 正，负，0
lable = ["浮点数", "整数", "分数有理数", "无约束数字"]  # 复选框
for i in range(3):
    tkinter.Radiobutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=number_type,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)
row += 1
tkinter.Radiobutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text=lable[3],
    variable=number_type,
    value=3,
).grid(column=column + 1, row=row, sticky=tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="生成赋值代数式",
    command=API.algebraic_assignment,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除赋值",
    command=API.del_variable_assignment,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
variable_assignment_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 4
)  # 显示代数式
variable_assignment_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=5,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=0
)
column += 1

row = 0
tkinter.Label(
    SCREEN,
    text="【方程联立】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="左代数式",
    command=API.add_equation_left,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="右代数式",
    command=API.add_equation_right,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="新建方程",
    command=API.generating_equation,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="解联立方程",
    command=API.solve_simultaneous_equations,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除方程",
    command=API.del_equation,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
equation_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 2
)  # 显示代数式
equation_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=2,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 2
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="应用为代数式",
    command=API.add_to_algebraic_box,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="添加联立",
    command=API.add_to_value_algebraic_box,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="添加反联立",
    command=API.add_to_algebraic_value_box,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
equation_solution_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 2
)  # 显示代数式
equation_solution_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=2,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 2
tkinter.Label(
    SCREEN,
    text="【解不等式】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="左代数式",
    command=API.add_left_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="右代数式",
    command=API.add_right_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="不等式运算",
    command=API.inequality_solve,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
inequality_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height
)  # 显示代数式
inequality_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=1,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 1
inequality_symbol = tkinter.IntVar()  # 实数
lable = ["大于>", "小于<", "大于等于>=", "小于等于<="]
for i in range(2):
    tkinter.Radiobutton(
        SCREEN,
        command=API.update_inequality_box_gui,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=inequality_symbol,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)
row += 1
for i in range(2):
    i += 2
    tkinter.Radiobutton(
        SCREEN,
        command=API.update_inequality_box_gui,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=inequality_symbol,
        value=i,
    ).grid(column=column + i - 2, row=row, sticky=tkinter.W)

row += 1
inequality_solution_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height
)  # 显示代数式
inequality_solution_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=2,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 2
tkinter.Label(
    SCREEN,
    text="【代数式画图】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column, row=row, columnspan=3
)  # 设置说明

row += 1
tkinter.Label(
    SCREEN,
    text="符号取值范围:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column, row=row
)  # 设置说明
range_of_values = tkinter.Entry(SCREEN, width=gui_width + 2)
range_of_values.grid(column=column + 1, row=row, sticky=tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="指定符号",
    command=API.add_plot_value,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
plot_object_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height
)  # 显示代数式
plot_object_box.grid(
    column=column,
    row=row,
    columnspan=3,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 1
plot_type = tkinter.IntVar()  # 实数
lable = ["二维图像", "三维图像"]
for i in range(2):
    tkinter.Radiobutton(
        SCREEN,
        command=API.update_plot_value_gui,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=plot_type,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="绘制图像",
    command=API.drawing_image,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="绘制代数式",
    command=API.draw_algebra_core,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="绘制树状图",
    command=API.show_algebraic,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
bracket = tkinter.IntVar()
log_bracket = tkinter.IntVar()
can_input = tkinter.Entry(SCREEN, width=gui_width)
can_input.grid(column=column, row=row, sticky=tkinter.W + tkinter.E)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="每项绘制括号",
    variable=bracket,
).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="对数绘制括号",
    variable=log_bracket,
).grid(column=column + 2, row=row, columnspan=2, sticky=tkinter.W)

row += 1
prompt_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height)  # 显示代数式
prompt_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=3,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
