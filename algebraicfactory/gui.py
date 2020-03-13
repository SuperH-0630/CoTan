import tkinter
import tkinter.messagebox
import tkinter.font as tkfont

from algebraicfactory.controller import AlgebraPolynomial

algebra_list = []
value_list = []
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


def draw_algebra_core():
    global algebra_controller, can_input, bracket, log_bracket
    name = get_algebraic_name()
    get = algebra_controller.get_expression_from_name(name)
    try:
        wh = can_input.get().split(",")
        w = int(wh[0])
        h = int(wh[1])
    except BaseException:
        w = 1000
        h = 300
    bracket = bool(bracket.get())
    log_bracket = bool(log_bracket.get())
    draw_algebra(get, w, h, bracket, log_bracket)


def draw_algebra(n, w, h, bracket=True, log_bracket=True):
    new_top = tkinter.Toplevel(bg=bg_color)
    new_top.resizable(width=False, height=False)
    new_top.geometry("+10+10")  # 设置所在位置
    paint_container = tkinter.Canvas(new_top, bg=bg_color, width=w, height=h)
    paint_container.pack()
    size = 20
    font = ("Fixdsys", size)
    x = 30
    y = 150
    plot_len = (size / 16) * 5.5
    for i in n:
        if i[0] == "A":
            print(f"A.={i}")
            te = f"{i[1]}"
            x += len(te) * plot_len
            paint_container.create_text(x, y, font=font, text=te)
            x += len(te) * plot_len
        elif i[0] == "B":
            print(f"B.={i}")
            if bracket:
                x, y, q = draw_algebra_son(
                    [["A", "["]],
                    paint_container,
                    x,
                    y,
                    size - 5,
                    [],
                    bracket,
                    log_bracket,
                )  # 递归呼叫儿子
            x, y, h = draw_algebra_son(
                i[1], paint_container, x, y, size, [], bracket, log_bracket
            )  # 底数
            dy = y
            y = h - 10
            x, y, q = draw_algebra_son(
                i[2], paint_container, x, y, size - 5, [], bracket, log_bracket
            )  # 指数
            y = dy
            if bracket:
                x, y, q = draw_algebra_son(
                    [["A", "]"]],
                    paint_container,
                    x,
                    y,
                    size - 5,
                    [],
                    bracket,
                    log_bracket,
                )  # 递归呼叫儿子
        elif i[0] == "C":
            print(f"C.={i}")
            if bracket:
                x, y, q = draw_algebra_son(
                    [["A", "["]],
                    paint_container,
                    x,
                    y,
                    size - 5,
                    [],
                    bracket,
                    log_bracket,
                )  # 递归呼叫儿子
            x, y, h = draw_algebra_son(
                i[1], paint_container, x, y, size, [], bracket, log_bracket
            )  # log符号
            if log_bracket:
                x, y, q = draw_algebra_son(
                    [["A", "("]],
                    paint_container,
                    x,
                    y,
                    size - 5,
                    [],
                    bracket,
                    log_bracket,
                )  # 递归呼叫儿子
            x, y, q = draw_algebra_son(
                i[2], paint_container, x, y, size, [], bracket, log_bracket
            )  # 递归呼叫儿子
            if log_bracket:
                x, y, q = draw_algebra_son(
                    [["A", ")"]],
                    paint_container,
                    x,
                    y,
                    size - 5,
                    [],
                    bracket,
                    log_bracket,
                )  # 递归呼叫儿子
            if bracket:
                x, y, q = draw_algebra_son(
                    [["A", "]"]],
                    paint_container,
                    x,
                    y,
                    size - 5,
                    [],
                    bracket,
                    log_bracket,
                )  # 递归呼叫儿子
        elif i[0] == "D":
            print(f"D.={i}")
            if bracket:
                x, y, q = draw_algebra_son(
                    [["A", "["]],
                    paint_container,
                    x,
                    y,
                    size - 5,
                    [],
                    bracket,
                    log_bracket,
                )  # 递归呼叫儿子
            y -= 20
            a_x, y, h = draw_algebra_son(
                i[1], paint_container, x, y, size, [], bracket, log_bracket
            )  # log符号
            y += 40
            b_x, y, h = draw_algebra_son(
                i[2], paint_container, x, y, size, [], bracket, log_bracket
            )  # log符号
            n_x = max([a_x, b_x]) - x
            y -= 20
            x, y, h = draw_algebra_son(
                [("A", "-" * int((n_x / (2 * plot_len))))],
                paint_container,
                x,
                y,
                size,
                [],
                bracket,
                log_bracket,
            )  # log符号
            if bracket:
                x, y, q = draw_algebra_son(
                    [["A", "]"]],
                    paint_container,
                    x,
                    y,
                    size - 5,
                    [],
                    bracket,
                    log_bracket,
                )  # 递归呼叫儿子

    output_prompt("运算完毕")


def draw_algebra_son(n, paint_container, x, y, size, max_y, kh=True, logkh=True):
    font = ("Fixdsys", size)
    plot_len = (size / 16) * 5.5
    print(f"n={n}")
    for i in n:
        if i[0] == "A":  # 只有A才是真的画图，其他是移动坐标
            max_y.append(y)
            print(f"A={i}")
            te = f"{i[1]}"
            x += len(te) * plot_len
            paint_container.create_text(x, y, font=font, text=te)
            x += len(te) * plot_len
        elif i[0] == "B":
            print(f"B={i}")
            if kh:
                x, y, q = draw_algebra_son(
                    [["A", "["]], paint_container, x, y, size - 5, [], kh, logkh
                )  # 递归呼叫儿子
            x, y, h = draw_algebra_son(
                i[1], paint_container, x, y, size, max_y, kh, logkh
            )  # 底数
            dy = y
            y = h - 10
            x, y, q = draw_algebra_son(
                i[2], paint_container, x, y, size - 5, max_y, kh, logkh
            )  # 递归呼叫儿子
            y = dy
            if kh:
                x, y, q = draw_algebra_son(
                    [["A", "]"]], paint_container, x, y, size - 5, [], kh, logkh
                )  # 递归呼叫儿子
        elif i[0] == "C":
            print(f"C={i}")
            if kh:
                x, y, q = draw_algebra_son(
                    [["A", "["]], paint_container, x, y, size - 5, [], kh, logkh
                )  # 递归呼叫儿子
            x, y, h = draw_algebra_son(
                i[1], paint_container, x, y, size, [], kh, logkh
            )  # log符号
            if logkh:
                x, y, q = draw_algebra_son(
                    [["A", "("]], paint_container, x, y, size - 5, [], kh, logkh
                )  # 递归呼叫儿子
            x, y, q = draw_algebra_son(
                i[2], paint_container, x, y, size, [], kh, logkh
            )  # 递归呼叫儿子
            if logkh:
                x, y, q = draw_algebra_son(
                    [["A", ")"]], paint_container, x, y, size - 5, [], kh, logkh
                )  # 递归呼叫儿子
            if kh:
                x, y, q = draw_algebra_son(
                    [["A", "]"]], paint_container, x, y, size - 5, [], kh, logkh
                )  # 递归呼叫儿子
        elif i[0] == "D":
            print(f"D={i}")
            if kh:
                x, y, q = draw_algebra_son(
                    [["A", "["]], paint_container, x, y, size - 5, [], kh, logkh
                )  # 递归呼叫儿子
            y -= 20
            a_x, y, h = draw_algebra_son(
                i[1], paint_container, x, y, size, [], kh, logkh
            )  # log符号
            y += 40
            b_x, y, h = draw_algebra_son(
                i[2], paint_container, x, y, size, [], kh, logkh
            )  # log符号
            n_x = max([a_x, b_x]) - x
            y -= 20
            x, y, h = draw_algebra_son(
                [("A", "-" * int((n_x / (2 * plot_len))))],
                paint_container,
                x,
                y,
                size,
                [],
                kh,
                logkh,
            )  # log符号
            if kh:
                x, y, q = draw_algebra_son(
                    [["A", "]"]], paint_container, x, y, size - 5, [], kh, logkh
                )  # 递归呼叫儿子
    try:
        re = min(max_y)
    except BaseException:
        re = 150
    return x, y, re


def show_algebraic_expression(str_, w=40, h=20, jh=True):
    global new_text, algebra_controller, bg_color
    if jh:
        try:
            str_ = algebra_controller.print_expression_str(str_)
            output_prompt("树状图计算成功")
        except BaseException:
            output_prompt("树状图计算失败")
            return False
    output_prompt("系统运算中")
    new_top = tkinter.Toplevel(bg=bg_color)
    new_top.resizable(width=False, height=False)
    new_top.geometry("+10+10")  # 设置所在位置
    new_text = tkinter.Text(new_top, width=w, height=h)
    new_text.pack()
    new_text.delete(1.0, tkinter.END)
    new_text.insert(tkinter.END, str_)
    new_text.config(state=tkinter.DISABLED)
    output_prompt("运算完毕")


# 打印接口（按钮）


def show_algebraic():
    global new_text, algebra_controller, can_input
    n = get_algebraic_name()
    print(n)
    try:
        str_ = algebra_controller.print_expression(n)
    except BaseException:
        return False
    try:
        wh = can_input.get().split(",")
        w = int(wh[0]) / 10
        h = int(wh[1]) / 10
    except BaseException:
        w = 40
        h = 20
    show_algebraic_expression(str_, w, h, False)


def clear_algebra():
    global algebra_controller
    try:
        algebra_controller.clean_expression()
        update_symbol_algebraic_box()
        output_prompt("删除完成")
    except BaseException:
        output_prompt("删除失败")


def del_algebra():
    global algebra_controller
    name = get_algebraic_name()
    try:
        algebra_controller.del_expression(name)
        update_symbol_algebraic_box()
        output_prompt("删除完成")
    except BaseException:
        output_prompt("删除失败")


def delete_symbol():
    global algebra_controller
    try:
        value = value_list[variable_box.curselection()[0]]
    except BaseException:
        output_prompt("请选定符号")
        return False
    try:
        algebra_controller.del_symbol(value)
        update_symbol_algebraic_box()
        output_prompt("删除完成")
    except BaseException:
        output_prompt("删除失败")


def drawing_image():
    global algebra_controller, p2d_value, p3d_value, plot_type
    try:
        ty = plot_type.get()
        if p2d_value is None:
            raise Exception
        if ty == 1 and p3d_value is None:
            raise Exception
        name = get_algebraic_name()
        algebra_controller.plot(name, p2d_value, p3d_value)
    except BaseException:
        output_prompt("画图失败")


def add_plot_value():
    global algebra_controller, p2d_value, p3d_value, range_of_values, plot_type, value_list, variable_box
    try:
        try:
            value = value_list[variable_box.curselection()[0]]
        except BaseException:
            output_prompt("请选定符号")
            return False
        value_range = range_of_values.get().split(",")
        if value_range == [""]:
            value_range = [-10, 10]

        tup = [value] + [
            min((float(value_range[0]), float(value_range[1]))),
            max((float(value_range[0]), float(value_range[1]))),
        ]
        ty = plot_type.get()
    except BaseException:
        output_prompt("修改失败")
        return False
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
    output_prompt("修改完成")
    update_plot_value()


def update_plot_value():
    global plot_object_box, plot_type, p2d_value, p3d_value
    ty = plot_type.get()
    re = []
    try:
        if ty == 0:  # 2D
            re = [f"二维:{p2d_value[0]} -> ({p2d_value[1]},{p2d_value[2]})"]
        else:
            re = [f"三维:{p2d_value[0]} -> ({p2d_value[1]},{p2d_value[2]})"]
            re.append(f"三维:{p3d_value[0]} -> ({p3d_value[1]},{p3d_value[2]})")
    except BaseException:
        pass
    plot_object_box.delete(0, tkinter.END)
    plot_object_box.insert(tkinter.END, *re)


# 重写代数式


def rewrite_algebra():
    global algebra_controller, rewrite_func, rewrite_object, rewrite_deep
    func = rewrite_func.get()
    rewrite = rewrite_object.get().split(",")
    if rewrite == [""]:
        rewrite = []
    deep = bool(rewrite_deep.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.rewrite_exp(name, func, rewrite, deep)
        output_prompt("运行完成")
        apply_algebraic_tips(get, f"代数式重写的结果为:{get},是否应用？")
    except BaseException:
        output_prompt("运行失败")


# 解不等式


def update_inequality_box():
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


def inequality_solve():
    global algebra_controller, left_inequality, right_inequality, inequality_symbol, inequality_solution_box
    if left_inequality is not None and right_inequality is not None:
        type = inequality_symbol.get()
        try:
            get = algebra_controller.solving_inequality(
                [left_inequality, right_inequality], type
            )
            inequality_solution_box.delete(0, tkinter.END)
            inequality_solution_box.insert(tkinter.END, *get)
            output_prompt("运行完成")
        except BaseException:
            output_prompt("解不等式失败")


def add_left_algebra():
    global left_inequality
    left_inequality = get_algebraic_name()
    update_inequality_box()


def add_right_algebra():
    global right_inequality
    right_inequality = get_algebraic_name()
    update_inequality_box()


# 解方程


def add_to_algebraic_box():
    global equation_solution_box, equation_solution_set
    get = equation_solution_set[equation_solution_box.curselection()[0]][1]  # [1]取结果
    apply_algebraic_tips(get, f"联立结果为:{get},是否应用？")


def add_to_value_algebraic_box():
    global equation_solution_box, equation_solution_set, value_algebra_dict
    get = equation_solution_set[equation_solution_box.curselection()[0]]
    value_algebra_dict[get[0]] = get[1]
    update_value_algebraic_box()


def add_to_algebraic_value_box():
    global equation_solution_box, equation_solution_set, algebra_value_dict
    get = equation_solution_set[equation_solution_box.curselection()[0]]
    algebra_value_dict[get[1]] = get[0]
    update_algebraic_value_box()


def solve_simultaneous_equations():
    global equation_set, equation_solution_box, equation_solution_set
    try:
        get = algebra_controller.solving_equations(equation_set)
        output_prompt("运行成功")
    except BaseException:
        output_prompt("解方程失败")
        return False
    equation_solution_set = []
    re = []
    for i in get:
        re.append(f"{i[0]} = {i[1]}")  # i[0]是一个字母=i[1]是一个代数式
        equation_solution_set.append((i[0], i[1]))
    equation_solution_box.delete(0, tkinter.END)
    equation_solution_box.insert(tkinter.END, *re)


def del_equation():
    global equation_set, left_equation, right_equation, equation_box
    num = equation_box.curselection()[0]
    if left_equation is not None or right_equation is not None:
        if num == 0:
            left_equation = None
            right_equation = None
        else:
            num -= 1
            del equation_set[num]
    else:
        del equation_set[num]
    update_simultaneous_equations_box()


def update_simultaneous_equations_box():
    global equation_set, equation_box, left_equation, right_equation
    box = []
    if left_equation is not None or right_equation is not None:
        box.append(f"(选定){left_equation} = {right_equation}")
    for i in equation_set:
        box.append(f"{i[0]} = {i[1]}")
    equation_box.delete(0, tkinter.END)
    equation_box.insert(tkinter.END, *box)


def generating_equation():
    global left_equation, right_equation, equation_set, equation_solution_set
    if left_equation is not None and right_equation is not None:
        equation_set.append((left_equation, right_equation))
        left_equation = None
        right_equation = None
    update_simultaneous_equations_box()


def add_equation_left():
    global left_equation, right_equation, equation_set, equation_solution_set
    left_equation = get_algebraic_name()
    update_simultaneous_equations_box()


def add_equation_right():
    global left_equation, right_equation, equation_set, equation_solution_set
    right_equation = get_algebraic_name()
    update_simultaneous_equations_box()


# 代入数字的运算
def algebraic_assignment():
    global algebra_controller, value_sub_dict
    name = get_algebraic_name()
    try:
        get = algebra_controller.algebraic_assignment(name, value_sub_dict)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("代数运算失败")
        return False
    apply_algebraic_tips(get, f"联立结果为:{get},是否应用？")


def update_variable_assignment_box():
    global algebra_controller, value_sub_dict, variable_assignment_box
    box = []
    for v in value_sub_dict:
        box.append(f"{v} = {value_sub_dict[v]}")
    variable_assignment_box.delete(0, tkinter.END)
    variable_assignment_box.insert(tkinter.END, *box)


def del_variable_assignment():
    global algebra_controller, value_sub_dict, variable_assignment_box
    num = variable_assignment_box.curselection()[0]
    del value_sub_dict[list(value_sub_dict.keys())[num]]
    update_variable_assignment_box()


def add_variable_assignment():
    global number, value_sub_dict, number_type
    try:
        value_name = value_list[variable_box.curselection()[0]]
    except BaseException:
        output_prompt("请选定符号")
        return False
    value_num = algebra_controller.creat_num(number.get(), number_type.get())  # 不同类型
    value_sub_dict[value_name] = value_num
    update_variable_assignment_box()


# 反向联立


def algebragic_value_simultaneous():
    global algebra_controller, algebra_value_dict
    name = get_algebraic_name()
    try:
        get = algebra_controller.algebragic_value_simultaneous(name, algebra_value_dict)
        output_prompt("反向联立完成")
    except BaseException:
        output_prompt("无法联立")
        return False
    apply_algebraic_tips(get, f"联立结果为:{get},是否应用？")


def update_algebraic_value_box():
    global algebra_controller, algebra_value_dict, left_algebra, right_value, algebra_value_box
    box = []
    if right_value is not None or left_algebra is not None:
        box.append(f"选定:{left_algebra} = {right_value}")
    for v in algebra_value_dict:
        box.append(f"{v} = {algebra_value_dict[v]}")
    algebra_value_box.delete(0, tkinter.END)
    algebra_value_box.insert(tkinter.END, *box)


def del_algebraic_value_simultaneousness():
    global algebra_controller, algebra_value_dict, left_algebra, right_value
    num = algebra_value_box.curselection()[0]
    if right_value is not None or left_algebra is not None:
        if num == 0:
            right_value = None
            left_algebra = None
        else:
            num -= 1
            del algebra_value_dict[list(algebra_value_dict.keys())[num]]
    else:
        del algebra_value_dict[list(algebra_value_dict.keys())[num]]
    update_algebraic_value_box()


def add_algebraic_values_simultaneously():
    global algebra_controller, algebra_value_dict, left_algebra, right_value
    if right_value is not None and left_algebra is not None:
        algebra_value_dict[left_algebra] = right_value
        right_value, left_algebra = None, None
    update_algebraic_value_box()


def add_left_simultaneous_algebra():  # 代数式=值的左代数式
    global algebra_controller, left_algebra
    alg_name = get_algebraic_name()
    left_algebra = alg_name
    update_algebraic_value_box()


def add_right_simultaneous_values():  # 解释同上
    global algebra_controller, value_list, variable_box, right_value
    try:
        value_name = value_list[variable_box.curselection()[0]]
    except BaseException:
        output_prompt("请选定符号")
        return False
    right_value = value_name
    update_algebraic_value_box()


# 执行符号->代数式联立


def value_algebraic_simultaneous():
    global algebra_controller, value_algebra_dict
    name = get_algebraic_name()
    try:
        get = algebra_controller.value_algebraic_simultaneous(name, value_algebra_dict)
        output_prompt("联立完成")
    except BaseException:
        output_prompt("无法联立")
        return False
    apply_algebraic_tips(get, f"联立结果为:{get},是否应用？")


def update_value_algebraic_box():
    global algebra_controller, value_list, variable_box, value_algebra_dict, right_algebra, left_value, value_algebra_box
    box = []
    if left_value is not None or right_algebra is not None:
        box.append(f"选定:{left_value} = {right_algebra}")
    for v in value_algebra_dict:
        box.append(f"{v} = {value_algebra_dict[v]}")
    value_algebra_box.delete(0, tkinter.END)
    value_algebra_box.insert(tkinter.END, *box)


def del_value_algebraic_simultaneous():
    global algebra_controller, value_list, variable_box, value_algebra_dict, right_algebra, left_value
    num = value_algebra_box.curselection()[0]
    if left_value is not None or right_algebra is not None:
        if num == 0:
            left_value = None
            right_algebra = None
        else:
            num -= 1
            del value_algebra_dict[list(value_algebra_dict.keys())[num]]
    else:
        del value_algebra_dict[list(value_algebra_dict.keys())[num]]
    update_value_algebraic_box()


def add_value_algebraic_simultaneous():
    global algebra_controller, value_list, variable_box, value_algebra_dict, right_algebra, left_value
    if left_value is not None and right_algebra is not None:
        value_algebra_dict[left_value] = right_algebra
        left_value, right_algebra = None, None
    update_value_algebraic_box()


def add_right_simultaneous_algebra():
    global algebra_controller, value_list, variable_box, right_algebra
    alg_name = get_algebraic_name()
    right_algebra = alg_name
    update_value_algebraic_box()


def add_left_simultaneous_values():
    global algebra_controller, value_list, variable_box, left_value
    try:
        value_name = value_list[variable_box.curselection()[0]]
    except BaseException:
        output_prompt("请选定符号")
        return False
    left_value = value_name
    update_value_algebraic_box()


def algebraic_digitization():
    global algebra_controller, valid_number
    try:
        num = int(valid_number.get())
    except BaseException:
        num = 5
    try:
        get = algebra_controller.algebraic_digitization(num)
        output_prompt("数字化完成")
    except BaseException:
        output_prompt("数字化失败")
        return False
    apply_algebraic_tips(get, f"数字化的结果为:{get},是否应用？")


def expand_special():
    global algebra_controller
    name = get_algebraic_name()
    try:
        get = algebra_controller.expand_special(name)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"展开特殊函数的结果为:{get},是否应用？")


def expand_complex():
    global algebra_controller
    name = get_algebraic_name()
    try:
        get = algebra_controller.expand_complex(name)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"展开虚数的结果为:{get},是否应用？")


def merger_of_similar_items():
    global algebra_controller, similar_items_object
    x = similar_items_object.get().split("#")
    name = get_algebraic_name()
    try:
        get = algebra_controller.merger_of_similar_items(name, x)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"合并同类项的结果为:{get},是否应用？")


def general_expansion():
    global algebra_controller, is_expand_complex
    complex = bool(is_expand_complex.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.expansion(name, complex)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"普遍展开的结果为:{get},是否应用？")


def factorization():
    global algebra_controller, is_gaussian, modulus, fully_factor, factor_rat
    name = get_algebraic_name()
    gaussian = bool(is_gaussian.get())
    deep = bool(fully_factor.get())
    rat = bool(factor_rat.get())
    try:
        modulus_num = int(modulus.get())
    except BaseException:
        modulus_num = None
    try:
        get = algebra_controller.factor(name, modulus_num, gaussian, deep, rat)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"因式分解的结果为:{get},是否应用？")


def standardization():
    global algebra_controller, simplify_ratio_input, simplify_func_Input, init_ignore_assumptions, init_rationalization
    try:
        radio = float(simplify_ratio_input.get())
    except BaseException:
        radio = 1.7
    rat = bool(init_rationalization.get())
    inverse = bool(init_ignore_assumptions.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.simplify(name, radio, rat=rat, inv=inverse)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"化简(标准化)为:{get},是否应用？")


def apply_algebraic_tips(re, message):
    if tkinter.messagebox.askokcancel("提示", message):
        algebra_controller.add_expression("", re)
        update_symbol_algebraic_box()


def expand_log():
    global algebra_controller, ignore_assumptions_log, log_fully_expand
    ignore_assumptions = not bool(ignore_assumptions_log.get())
    deep = bool(log_fully_expand.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.log_expansion(name, ignore_assumptions, deep)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"展开对数结果为:{get},是否应用？")


def reduce_log():
    global algebra_controller, ignore_assumptions_log
    ignore_assumptions = not bool(ignore_assumptions_log.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.log_simp(name, ignore_assumptions)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"化简对数结果为:{get},是否应用？")


def expand_mul():
    global algebra_controller, ignore_assumptions
    name = get_algebraic_name()
    try:
        get = algebra_controller.mul_expansion(name)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"展开乘法结果为:{get},是否应用？")


def expand_additive_index():
    global algebra_controller, ignore_assumptions
    name = get_algebraic_name()
    try:
        get = algebra_controller.multinomial_expansion(name)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"展开加法式幂结果为:{get},是否应用？")


def composite_index():
    global algebra_controller, ignore_assumptions
    name = get_algebraic_name()
    try:
        get = algebra_controller.pow_simp_multinomial(name)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"合成幂指数的结果为:{get},是否应用？(彻底化简加法式幂可以使用因式分解)")


def expand_exp_base():
    global algebra_controller, ignore_assumptions
    deep = bool(fully_expand.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.pow_expansion_base(name, deep)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"展开指数底数结果为:{get},是否应用？")


def expand_exp_index():
    global algebra_controller, fully_expand
    deep = bool(fully_expand.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.pow_expansion_exp(name, deep)
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"展开指数幂结果为:{get},是否应用？")


def expand_power():
    global algebra_controller, fully_expand
    deep = bool(fully_expand.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.pow_expansion_core(name, deep)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"展开指数结果为:{get},是否应用？")


def reduce_exp_base():
    global algebra_controller, ignore_assumptions
    ignore = not bool(ignore_assumptions.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.pow_simp_base(name, ignore)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"化简指数底数结果为:{get},是否应用？")


def reduce_exp_index():
    global algebra_controller, ignore_assumptions
    ignore = not bool(ignore_assumptions.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.pow_simp_exp(name, ignore)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"化简指数幂结果为:{get},是否应用？")


def reduced_power():
    global algebra_controller, ignore_assumptions
    ignore = not bool(ignore_assumptions.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.pow_simp_core(name, ignore)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"化简指数结果为:{get},是否应用？")


def reduced_trigonometric():  # 三角函数化简
    global algebra_controller
    name = get_algebraic_name()
    try:
        get = algebra_controller.trig_simp(name)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"三角化简结果为:{get},是否应用？")


def expand_trigonometric():  # 三角展开
    global algebra_controller, trig_fully_expand
    deep = bool(trig_fully_expand.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.trig_expansion(name, deep)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"三角展开结果为:{get},是否应用？")


def fractional_division():  # 通分
    global algebra_controller
    name = get_algebraic_name()
    try:
        get = algebra_controller.fractional_merge(name)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"分式通分结果为:{get},是否应用？")


def fraction_reduction():  # 约分
    global algebra_controller
    name = get_algebraic_name()
    try:
        get = algebra_controller.fraction_reduction(name)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"分式约分结果为:{get},是否应用？")


def fractional_fission():  # 裂项
    global algebra_controller, apart
    x = apart.get().replace(" ", "")
    if x == "":
        x = None
    name = get_algebraic_name()
    try:
        get = algebra_controller.fractional_fission(name, x)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"分式裂项结果为:{get},是否应用？")


def fractional_synthesis():  # together
    global algebra_controller, fully_divided
    deep = bool(fully_divided.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.as_fraction(name, deep)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"合成分式结果为:{get},是否应用？")


def denominator_rationalization():  # 分母有理化
    global algebra_controller, rationalized_unknown, maximum_irrational_term
    # Max
    try:
        maximum = int(maximum_irrational_term.get())
    except BaseException:
        maximum = 4
    rationalized = bool(rationalized_unknown.get())
    name = get_algebraic_name()
    try:
        get = algebra_controller.fractional_rat(name, rationalized, maximum)
        output_prompt("运算成功")
    except BaseException:
        output_prompt("运算失败")
        return False
    apply_algebraic_tips(get, f"分母有理化结果为:{get},是否应用？")


def add_operation_algebra():
    global algebra_controller, on_hold_algebra, option_list
    name = get_algebraic_name()
    if name is None:
        return False
    option_list.append(name)
    update_operation_box()


def del_operation_algebra():
    global on_hold_algebra, option_list
    del option_list[on_hold_algebra.curselection()[0]]
    update_operation_box()


def clear_operational_algebra():
    global on_hold_algebra, option_list
    update_symbol_algebraic_box()


def update_operation_box():
    global on_hold_algebra, option_list
    re = []
    for i in range(len(option_list)):
        re.append(f"({i + 1}) --> {option_list[i]}")
    on_hold_algebra.delete(0, tkinter.END)
    on_hold_algebra.insert(tkinter.END, *re)


def algebraic_composition():
    global algebra_controller, option_list, merge_func
    name = option_list.copy()
    if len(name) < 2:
        raise Exception
    try:
        re = algebra_controller.merge_func(name, merge_func.get())
        output_prompt("合成成功")
    except BaseException:
        output_prompt("合成失败")
        return False
    if tkinter.messagebox.askokcancel("提示", f"合成结果为:{re}，是否应用?"):
        algebra_controller.add_expression("", re)
        update_symbol_algebraic_box()


def algebraic_multiplication():
    global algebra_controller, option_list
    name = option_list.copy()
    if len(name) < 2:
        raise Exception
    try:
        re = algebra_controller.merge_mul(name)
        output_prompt("合成成功")
    except BaseException:
        output_prompt("合成失败")
        return False
    if tkinter.messagebox.askokcancel("提示", f"合成结果为:{re}，是否应用?"):
        algebra_controller.add_expression("", re)
        update_symbol_algebraic_box()


def algebraic_addition():
    global algebra_controller, option_list
    name = option_list.copy()
    if len(name) < 2:
        raise Exception
    try:
        re = algebra_controller.merge_add(name)
        output_prompt("合成成功")
    except BaseException:
        output_prompt("合成失败")
        return False
    if tkinter.messagebox.askokcancel("提示", f"合成结果为:{re}，是否应用?"):
        algebra_controller.add_expression("", re)
        update_symbol_algebraic_box()


def algebraic_partition():
    global algebra_controller, deep_split, split_func, return_type
    name = get_algebraic_name()
    deep = deep_split.get()
    f = split_func.get().split(",")
    m = return_type.get()
    if m == 1:
        must = False
    else:
        must = True
    try:
        re = algebra_controller.split_func(name, deep, f, must)
        output_prompt("拆分成功")
    except BaseException:
        output_prompt("拆分失败")
        return False
    if tkinter.messagebox.askokcancel("提示", f"{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?"):
        for in_alg in re[0]:
            algebra_controller.add_expression("", in_alg)
            update_symbol_algebraic_box()


def algebraic_similarity_split():
    global algebra_controller, similar_items, return_type
    name = get_algebraic_name()
    value = similar_items.get().split("#")
    f = return_type.get()
    try:
        re = algebra_controller.split_add(name, value, f)
        output_prompt("拆分成功")
    except BaseException:
        output_prompt("拆分失败")
        return False
    if tkinter.messagebox.askokcancel("提示", f"{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?"):
        for in_alg in re[0]:
            algebra_controller.add_expression("", in_alg)
            update_symbol_algebraic_box()


def algebraic_factorization():
    global algebra_controller, return_type
    name = get_algebraic_name()
    all = return_type.get()
    if all == 0:
        k = [True, False]
    elif all == 1:
        k = [False, False]
    else:
        k = [True, True]
    try:
        re = algebra_controller.split_mul(name, *k)
        output_prompt("拆分成功")
    except BaseException:
        output_prompt("拆分失败")
        return False
    if tkinter.messagebox.askokcancel("提示", f"{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?"):
        for in_alg in re[0]:
            algebra_controller.add_expression("", in_alg)
            update_symbol_algebraic_box()


# 统一接口：得到alg的名字(提取第一个)


def get_algebraic_name():
    global algebra_list, algebra_box
    try:
        name = algebra_list[algebra_box.curselection()[0]]
    except BaseException:
        name = None
        output_prompt("请选定代数式")
    return name


def add__algebraic():
    global algebra_name, algebra_expression, algebra_box, init_ignore_assumptions, init_rationalization, ratio, standardization
    try:
        in_alg = algebra_expression.get()
        name = algebra_name.get().replace(" ", "")
        if bool(standardization.get()):
            radio_list = ratio.get().split("#")
            radio = float(radio_list[0])
            rat = bool(init_rationalization.get())
            inverse = bool(init_ignore_assumptions.get())
            new_alg = algebra_controller.Simplify(
                in_alg, radio=radio, rat=rat, inv=inverse
            )
            if new_alg is not None and tkinter.messagebox.askokcancel(
                "提示", f"约简函数为:{new_alg}，是否应用?"
            ):
                in_alg = new_alg
        if not algebra_controller.add_expression(name, in_alg):
            raise Exception
        update_symbol_algebraic_box()
        output_prompt("代数式新增成功")
    except BaseException:
        output_prompt("新增代数式无法应用")


# 获取预测


def get_predictions():
    global variable_box, value_list, algebra_controller, predictions_box
    try:
        try:
            n = value_list[variable_box.curselection()[0]]
        except BaseException:
            output_prompt("请选定符号")
            return False
        predictions_box.delete(0, tkinter.END)
        predictions_box.insert(tkinter.END, *algebra_controller.variable_prediction(n))
        output_prompt("性质预测成功")
    except BaseException:
        output_prompt("性质预测失败")


# 更新列表显示


def update_symbol_algebraic_box():
    global algebra_controller, variable_box, value_list, algebra_box, algebra_list, option_list, on_hold_algebra
    # 保存符号
    re = algebra_controller()  # 0-value,1-alg
    value_list = re[0][1]
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


def add_custom_symbol():  # 添加自定义Symbol
    global is_generation, is_rational, is_prime, is_even, is_limited, is_complex, is_positives, variable_name
    global variable_box, no_constraint, integer
    # 复选框系统
    parameter = []
    n = 0
    for i in is_complex:
        parameter.append(i.get())
        n += parameter[-1]
    if n == 1:  # 选一个设为True
        is_complex = [
            ["complex", "real", "imaginary"][parameter.index(1)],
            True,
        ]  # 对象，布尔
    elif n == 2:  # 选两个设为False
        is_complex = [
            ["complex", "real", "imaginary"][parameter.index(0)],
            False,
        ]  # 对象，布尔
    else:
        is_complex = None  # 其余

    parameter = []
    n = 0
    for i in is_complex:
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
    try:
        __add_symbot_core(
            is_generation.get(),
            is_rational.get(),
            is_prime.get(),
            is_even.get(),
            is_limited.get(),
            is_complex,
            is_natural,
            integer.get(),
        )
    except BaseException:
        output_prompt("自定义符号新增失败")


def add_real():  # 添加实数符号
    __add_symbot_core(is_complex=["real", True], describe="实数(且复数)符号")


def add_integer():  # 添加整数符号
    __add_symbot_core(is_integer=1, describe="整数(且实数)符号")


def add_non_negative_real():  # 非负实数
    __add_symbot_core(
        is_natural=["negative", False], is_complex=["real", True], describe="非负实数符号"
    )


def add_even():  # 偶数
    __add_symbot_core(is_even=1, describe="偶数(且整数)符号")


def add_odd():  # 奇数
    __add_symbot_core(is_even=2, describe="奇数(且整数)符号")


def add_positive_real():  # 正实数
    __add_symbot_core(
        is_natural=["positive", True], is_complex=["real", True], describe="正实数符号"
    )


def add_positive_integer():  # 正整数
    __add_symbot_core(is_natural=["positive", True], is_integer=1, describe="正整数符号")


def add_natural():  # 自然数
    __add_symbot_core(
        is_natural=["negative", False], is_integer=1, describe="自然数(非负整数)符号"
    )


def add_no_constraints():  # 无约束
    __add_symbot_core(no_constraint=1, describe="仅满足交换律的无约束符号")


# 添加Symbol的统一接口


def __add_symbot_core(
    is_generation=0,
    is_rational=0,
    is_prime=0,
    is_even=0,
    is_finite=0,
    is_complex=None,
    is_natural=None,
    is_integer=0,
    no_constraint=0,
    describe="自定义符号",
):
    global algebra_controller
    # 代数，有理，质数，偶数，有限实数，复数，正负，整数，取消
    name_list = variable_name.get().split(",")
    for name in name_list:
        try:
            if not algebra_controller.add_symbol(
                name,
                is_generation,
                is_rational,
                is_prime,
                is_even,
                is_finite,
                is_complex,
                is_natural,
                is_integer,
                no_constraint,
                describe,
            ):
                raise Exception
        except BaseException:
            output_prompt(f"新增“{name}”失败")
    output_prompt(f"新增“{describe}”完成")
    update_symbol_algebraic_box()


def output_prompt(news):
    global prompt_box, prompt_num, SCREEN
    prompt_num += 1
    news = str(news)
    prompt_box.insert(0, news + f"({prompt_num})")
    SCREEN.update()


def algebraic_factory_main():
    global algebra_controller, SCREEN, value_list, algebra_list, option_list, value_algebra_dict, left_value, right_algebra, algebra_value_dict
    global right_value, left_algebra, value_sub_dict
    global left_equation, right_equation, equation_set, equation_solution_set, left_inequality, right_inequality, p2d_value, p3d_value, prompt_num
    global bg_color, buttom_color, word_color, FONT2, FONT, FONT3

    SCREEN.mainloop()


algebra_controller = AlgebraPolynomial(output_prompt)
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
    command=add_real,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="整数符号(Z)",
    command=add_integer,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="非负实数符号",
    command=add_non_negative_real,
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
    command=add_even,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="奇数符号",
    command=add_odd,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="正数符号",
    command=add_positive_real,
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
    command=add_natural,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="正整数符号",
    command=add_positive_integer,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="无约束符号",
    command=add_no_constraints,
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
    command=add_custom_symbol,
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
    command=get_predictions,
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
    command=delete_symbol,
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
ratio = tkinter.Entry(SCREEN, width=gui_width * 2)
ratio.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

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
    command=clear_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="生成代数式",
    command=add__algebraic,
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
    command=del_algebra,
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
    command=rewrite_algebra,
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
    command=algebraic_similarity_split,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="乘法拆分",
    command=algebraic_factorization,
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
    command=algebraic_partition,
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
    command=add_operation_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="清空",
    command=clear_operational_algebra,
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
    command=del_operation_algebra,
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
    command=algebraic_addition,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="因式合成",
    command=algebraic_multiplication,
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
    command=algebraic_composition,
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
    command=algebraic_digitization,
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
    command=fractional_division,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="分式约分",
    command=fraction_reduction,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="分式裂项",
    command=fractional_fission,
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
    command=denominator_rationalization,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="转化为分式(小改动)",
    command=fractional_synthesis,
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
    command=expand_trigonometric,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="三角函数合成",
    command=reduced_trigonometric,
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
    command=expand_mul,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开加法式幂",
    command=expand_additive_index,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="指数合成",
    command=composite_index,
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
    command=reduce_exp_base,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="化简指数幂",
    command=reduce_exp_index,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="化简指数",
    command=reduced_power,
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
    command=expand_exp_base,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开指数幂",
    command=expand_exp_index,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开指数",
    command=expand_power,
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
    command=expand_log,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="化简对数",
    command=reduce_log,
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
    command=expand_special,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="展开虚数",
    command=expand_complex,
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
    command=standardization,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="普遍运算展开",
    command=general_expansion,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="因式分解",
    command=factorization,
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
    command=merger_of_similar_items,
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
    command=add_left_simultaneous_values,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="选定代数式",
    command=add_right_simultaneous_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="新键联立",
    command=add_value_algebraic_simultaneous,
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
    command=value_algebraic_simultaneous,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除联立",
    command=del_value_algebraic_simultaneous,
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
    command=add_left_simultaneous_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="选定符号",
    command=add_right_simultaneous_values,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="新键联立",
    command=add_algebraic_values_simultaneously,
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
    command=algebragic_value_simultaneous,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除联立",
    command=del_algebraic_value_simultaneousness,
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
    command=add_variable_assignment,
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
    command=algebraic_assignment,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除赋值",
    command=del_variable_assignment,
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
    command=add_equation_left,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="右代数式",
    command=add_equation_right,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="新建方程",
    command=generating_equation,
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
    command=solve_simultaneous_equations,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除方程",
    command=del_equation,
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
    command=add_to_algebraic_box,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="添加联立",
    command=add_to_value_algebraic_box,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="添加反联立",
    command=add_to_algebraic_value_box,
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
    command=add_left_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="右代数式",
    command=add_right_algebra,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="不等式运算",
    command=inequality_solve,
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
        command=update_inequality_box,
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
        command=update_inequality_box,
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
    command=add_plot_value,
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
        command=update_plot_value,
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
    command=drawing_image,
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
    command=draw_algebra_core,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="绘制树状图",
    command=show_algebraic,
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
prompt_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height
)  # 显示代数式
prompt_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=3,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

output_prompt("加载完成")
