import tkinter,tkinter.messagebox
import tkinter.font as tkFont
from DSGC.Algebra import Algebra_Polynomial

#树状图打印核心组件
def draw_algebra_core():
    global alg,Can_Input,kd_bool,logkd_bool
    name = get_algebraic_name()
    get = alg.Draw(name)
    try:
        wh = Can_Input.get().split(',')
        w = int(wh[0])
        h = int(wh[1])
    except:
        w = 1000
        h = 300
    kd = bool(kd_bool.get())
    logkd = bool(logkd_bool.get())
    draw_algebra(get, w, h, kd, logkd)

def draw_algebra(n, w, h, kh=True, logkh=True):
    new_top = tkinter.Toplevel(bg=bg)
    new_top.resizable(width=False, height=False)
    new_top.geometry('+10+10')  # 设置所在位置
    Can = tkinter.Canvas(new_top,bg=bg, width=w, height=h)
    Can.pack()
    size = 20
    F2 = ('Fixdsys', size)
    x = 30
    y = 150
    l = (size/16)*5.5
    for i in n:
        if i[0] == 'A':
            print(f'A.={i}')
            te = f'{i[1]}'
            x += len(te) * l
            Can.create_text(x, y,font=F2, text=te)
            x += len(te) * l
        elif i[0] == 'B':
            print(f'B.={i}')
            if kh:x, y, q = draw_algebra_son([['A', '[']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            x, y,h = draw_algebra_son(i[1], Can, x, y, size, [], kh, logkh)  # 底数
            dy = y
            y = h-10
            x, y,q = draw_algebra_son(i[2], Can, x, y, size - 5, [], kh, logkh)  # 指数
            y = dy
            if kh:x, y, q = draw_algebra_son([['A', ']']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
        elif i[0] == 'C':
            print(f'C.={i}')
            if kh:x, y, q = draw_algebra_son([['A', '[']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            x, y, h = draw_algebra_son(i[1], Can, x, y, size, [], kh, logkh)  # log符号
            if logkh:x, y, q = draw_algebra_son([['A', '(']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            x, y, q = draw_algebra_son(i[2], Can, x, y, size, [], kh, logkh)  # 递归呼叫儿子
            if logkh:x, y, q = draw_algebra_son([['A', ')']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            if kh:x, y, q = draw_algebra_son([['A', ']']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
        elif i[0] == 'D':
            print(f'D.={i}')
            if kh:x, y, q = draw_algebra_son([['A', '[']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            y -= 20
            a_x, y, h = draw_algebra_son(i[1], Can, x, y, size, [], kh, logkh)  # log符号
            y += 40
            b_x, y, h = draw_algebra_son(i[2], Can, x, y, size, [], kh, logkh)  # log符号
            n_x = max([a_x, b_x]) - x
            y -= 20
            x, y, h = draw_algebra_son([('A', '-' * int((n_x / (2 * l))))], Can, x, y, size, [], kh, logkh)  # log符号
            if kh:x, y, q = draw_algebra_son([['A', ']']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子

    output_prompt('运算完毕')

def draw_algebra_son(n, Can, x, y, size, max_y, kh=True, logkh=True):
    F2 = ('Fixdsys', size)
    l = (size/16)*5.5
    print(f'n={n}')
    for i in n:
        if i[0] == 'A':#只有A才是真的画图，其他是移动坐标
            max_y.append(y)
            print(f'A={i}')
            te = f'{i[1]}'
            x += len(te) * l
            Can.create_text(x, y,font=F2, text=te)
            x += len(te) * l
        elif i[0] == 'B':
            print(f'B={i}')
            if kh:x, y, q = draw_algebra_son([['A', '[']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            x, y, h = draw_algebra_son(i[1], Can, x, y, size, max_y, kh, logkh)  # 底数
            dy = y
            y = h-10
            x, y,q = draw_algebra_son(i[2], Can, x, y, size - 5, max_y, kh, logkh)  # 递归呼叫儿子
            y = dy
            if kh:x, y, q = draw_algebra_son([['A', ']']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
        elif i[0] == 'C':
            print(f'C={i}')
            if kh:x, y, q = draw_algebra_son([['A', '[']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            x, y, h = draw_algebra_son(i[1], Can, x, y, size, [], kh, logkh)  # log符号
            if logkh:x, y, q = draw_algebra_son([['A', '(']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            x, y, q = draw_algebra_son(i[2], Can, x, y, size, [], kh, logkh)  # 递归呼叫儿子
            if logkh:x, y, q = draw_algebra_son([['A', ')']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            if kh:x, y, q = draw_algebra_son([['A', ']']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
        elif i[0] == 'D':
            print(f'D={i}')
            if kh:x, y, q = draw_algebra_son([['A', '[']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
            y -= 20
            a_x, y, h = draw_algebra_son(i[1], Can, x, y, size, [], kh, logkh)  # log符号
            y += 40
            b_x, y, h = draw_algebra_son(i[2], Can, x, y, size, [], kh, logkh)  # log符号
            n_x = max([a_x, b_x]) - x
            y -= 20
            x, y, h = draw_algebra_son([('A', '-' * int((n_x / (2 * l))))], Can, x, y, size, [], kh, logkh)  # log符号
            if kh:x, y, q = draw_algebra_son([['A', ']']], Can, x, y, size - 5, [], kh, logkh)  # 递归呼叫儿子
    try:
        re = min(max_y)
    except:
        re = 150
    return x,y,re

def show_algebraic_expression(str_, w=40, h=20, jh=True):
    global New_Text,alg,bg
    if jh:
        try:
            str_ = alg.rprint_expression(str_)
            output_prompt('树状图计算成功')
        except:
            output_prompt('树状图计算失败')
            return False
    output_prompt('系统运算中')
    new_top = tkinter.Toplevel(bg=bg)
    new_top.resizable(width=False, height=False)
    new_top.geometry('+10+10')  # 设置所在位置
    New_Text = tkinter.Text(new_top, width=w, height=h)
    New_Text.pack()
    New_Text.delete(1.0, tkinter.END)
    New_Text.insert(tkinter.END,str_)
    New_Text.config(state=tkinter.DISABLED)
    output_prompt('运算完毕')

#打印接口（按钮）
def show_algebraic():
    global New_Text,alg,Can_Input
    n = get_algebraic_name()
    print(n)
    try:
        str_ = alg.print_expression(n)
    except:
        return False
    try:
        wh = Can_Input.get().split(',')
        w = int(wh[0])/10
        h = int(wh[1])/10
    except:
        w = 40
        h = 20
    show_algebraic_expression(str_, w, h, False)

def clear_algebra():
    global alg
    try:
        alg.Tra_Alg()
        update_symbol_algebraic_box()
        output_prompt('删除完成')
    except:
        output_prompt('删除失败')

def del_algebra():
    global alg
    name = get_algebraic_name()
    try:
        alg.del_Alg(name)
        update_symbol_algebraic_box()
        output_prompt('删除完成')
    except:
        output_prompt('删除失败')

def delete_symbol():
    global alg
    try:
        value = Value_List[Value_BOX.curselection()[0]]
    except:
        output_prompt('请选定符号')
        return False
    try:
        alg.del_Symbol(value)
        update_symbol_algebraic_box()
        output_prompt('删除完成')
    except:
        # raise
        output_prompt('删除失败')

#画图系统
def drawing_image():
    global alg, p2D_Value, p3D_Value, Plot_Type
    try:
        ty = Plot_Type.get()
        if p2D_Value == None:raise Exception
        if ty == 1 and p3D_Value == None:raise Exception
        name = get_algebraic_name()
        alg.Plot(name,p2D_Value,p3D_Value)
    except:
        output_prompt('画图失败')

def add_plot_value():
    global alg,p2D_Value,p3D_Value,Range_Input,Plot_Type,Value_List,Value_BOX
    try:
        try:
            value = Value_List[Value_BOX.curselection()[0]]
        except:
            output_prompt('请选定符号')
            return False
        R = Range_Input.get().split(',')
        if R == ['']:R = [-10,10]
        Range = [min((float(R[0]),float(R[1]))),max((float(R[0]),float(R[1])))]
        tup = [value]+Range
        ty = Plot_Type.get()
    except:
        output_prompt('修改失败')
        return False
    if p2D_Value == None:
        p2D_Value = tup
    elif p3D_Value == None and ty == 1:
        if p2D_Value[0] != tup[0]:
            p3D_Value = tup
        else:
            p2D_Value = tup
    else:
        if ty == 0:#2D
            p2D_Value = tup
            p3D_Value = None
        else:#3D
            if p2D_Value[0] == tup[0]:
                p2D_Value = tup
            elif p3D_Value[0] == tup[0]:
                p3D_Value = tup
            else:
                p2D_Value = p3D_Value
                p3D_Value = tup
    output_prompt('修改完成')
    update_plot_value()

def update_plot_value():
    global PlotValue_BOX,Plot_Type,p2D_Value,p3D_Value
    ty = Plot_Type.get()
    re = []
    try:
        if ty == 0:#2D
            re = [f'二维:{p2D_Value[0]} -> ({p2D_Value[1]},{p2D_Value[2]})']
        else:
            re = [f'三维:{p2D_Value[0]} -> ({p2D_Value[1]},{p2D_Value[2]})']
            re.append(f'三维:{p3D_Value[0]} -> ({p3D_Value[1]},{p3D_Value[2]})')
    except:pass
    PlotValue_BOX.delete(0, tkinter.END)
    PlotValue_BOX.insert(tkinter.END, *re)

#重写代数式
def rewrite_algebra():
    global alg,Rewrite_Input,Rewrite_F_Input,Rewrite_deep
    Func = Rewrite_Input.get()
    DX = Rewrite_F_Input.get().split(',')
    if DX == ['']:DX = []
    deep = bool(Rewrite_deep.get())
    name = get_algebraic_name()
    try:
        get = alg.rewrite_algebra(name, Func, DX, deep)
        output_prompt('运行完成')
    except:
        output_prompt('运行失败')
    apply_algebraic_tips(get, f'代数式重写的结果为:{get},是否应用？')

#解不等式
def update_inequality_box():
    global Z_Inequality,Y_Inequality,Inequality_Type,Inequality_BOX
    re = []
    if Z_Inequality != None and Y_Inequality != None:
        Type = ['>', '<', '>=', '<='][Inequality_Type.get()]
        re.append(f'{Z_Inequality} {Type} {Y_Inequality}')
    else:
        if Z_Inequality != None:
            re.append(f'左代数式:{Z_Inequality}')
        if Y_Inequality != None:
            re.append(f'右代数式:{Y_Inequality}')
    Inequality_BOX.delete(0, tkinter.END)
    Inequality_BOX.insert(tkinter.END, *re)

def inequality_solve():
    global alg,Z_Inequality,Y_Inequality,Inequality_Type,AnswerInequality_BOX
    if Z_Inequality != None and Y_Inequality != None:
        type = Inequality_Type.get()
        try:
            get = alg.Solve_Inequality([Z_Inequality,Y_Inequality],type)
            AnswerInequality_BOX.delete(0, tkinter.END)
            AnswerInequality_BOX.insert(tkinter.END, *get)
            output_prompt('运行完成')
        except:
            output_prompt('解不等式失败')

def add_left_algebra():
    global Z_Inequality
    Z_Inequality = get_algebraic_name()
    update_inequality_box()

def add_right_algebra():
    global Y_Inequality
    Y_Inequality = get_algebraic_name()
    update_inequality_box()

#解方程
def add_to_algebraic_box():
    global Answer_BOX, Answer_List
    get = Answer_List[Answer_BOX.curselection()[0]][1]#[1]取结果
    apply_algebraic_tips(get, f'联立结果为:{get},是否应用？')

def add_to_value_algebraic_box():
    global Answer_BOX, Answer_List,Sub_Dic
    get = Answer_List[Answer_BOX.curselection()[0]]
    Sub_Dic[get[0]] = get[1]
    update_value_algebraic_box()

def add_to_algebraic_value_box():
    global Answer_BOX, Answer_List,RSub_Dic
    get = Answer_List[Answer_BOX.curselection()[0]]
    RSub_Dic[get[1]] = get[0]
    update_algebraic_value_box()

def solve_simultaneous_equations():
    global Solve_list,Answer_BOX,Answer_List
    try:
        get = alg.Solve(Solve_list)
        output_prompt('运行成功')
    except:
        output_prompt('解方程失败')
        return False
    Answer_List = []
    re = []
    for i in get:
        re.append(f'{i[0]} = {i[1]}')#i[0]是一个字母=i[1]是一个代数式
        Answer_List.append((i[0],i[1]))
    Answer_BOX.delete(0, tkinter.END)
    Answer_BOX.insert(tkinter.END, *re)

def del_equation():
    global Solve_list,Z_alg, Y_alg,Solve_BOX
    num = Solve_BOX.curselection()[0]
    if Z_alg != None or Y_alg != None:
        if num == 0:
            Z_alg = None
            Y_alg = None
        else:
            num -= 1
            del Solve_list[num]
    else:
        del Solve_list[num]
    update_simultaneous_equations_box()

def update_simultaneous_equations_box():
    global Solve_list,Solve_BOX,Z_alg, Y_alg
    BOX = []
    if Z_alg != None or Y_alg != None:
        BOX.append(f'(选定){Z_alg} = {Y_alg}')
    for i in Solve_list:
        BOX.append(f'{i[0]} = {i[1]}')
    Solve_BOX.delete(0, tkinter.END)
    Solve_BOX.insert(tkinter.END, *BOX)

def generating_equation():
    global Z_alg, Y_alg, Solve_list, Answer_List
    if Z_alg != None and Y_alg != None:
        Solve_list.append((Z_alg,Y_alg))
        Z_alg = None
        Y_alg = None
    update_simultaneous_equations_box()

def add_equation_left():
    global Z_alg, Y_alg, Solve_list, Answer_List
    Z_alg = get_algebraic_name()
    update_simultaneous_equations_box()


def add_equation_right():
    global Z_alg, Y_alg, Solve_list, Answer_List
    Y_alg = get_algebraic_name()
    update_simultaneous_equations_box()


#代数运算
def algebraic_assignment():
    global alg,Value_Sub_Dic
    name = get_algebraic_name()
    try:
        get = alg.SubNum_Value(name,Value_Sub_Dic)
        output_prompt('运算成功')
    except:
        output_prompt('代数运算失败')
        return False
    apply_algebraic_tips(get, f'联立结果为:{get},是否应用？')

def update_variable_assignment_box():
    global alg, Value_Sub_Dic,ValueNUM_BOX
    BOX = []
    for v in Value_Sub_Dic:
        BOX.append(f'{v} = {Value_Sub_Dic[v]}')
    ValueNUM_BOX.delete(0, tkinter.END)
    ValueNUM_BOX.insert(tkinter.END, *BOX)

def del_variable_assignment():
    global alg,Value_Sub_Dic,ValueNUM_BOX
    num = ValueNUM_BOX.curselection()[0]
    del Value_Sub_Dic[list(Value_Sub_Dic.keys())[num]]
    update_variable_assignment_box()

def add_variable_assignment():
    global ValueNUM_Input,Value_Sub_Dic,Num_Type
    try:
        value_name = Value_List[Value_BOX.curselection()[0]]
    except:
        output_prompt('请选定符号')
        return False
    value_num = alg.Creat_Num(ValueNUM_Input.get(),Num_Type.get())#不同类型
    Value_Sub_Dic[value_name] = value_num
    update_variable_assignment_box()

#反向联立
def algebragic_value_simultaneous():
    global alg,RSub_Dic
    name = get_algebraic_name()
    try:
        get = alg.RSub_Value(name,RSub_Dic)
        output_prompt('反向联立完成')
    except:
        output_prompt('无法联立')
        return False
    apply_algebraic_tips(get, f'联立结果为:{get},是否应用？')


def update_algebraic_value_box():
    global alg, RSub_Dic, RSub_Alg, RSub_Value, RSub_BOX
    BOX = []
    if RSub_Value != None or RSub_Alg != None:
        BOX.append(f'选定:{RSub_Alg} = {RSub_Value}')
    for v in RSub_Dic:
        BOX.append(f'{v} = {RSub_Dic[v]}')
    RSub_BOX.delete(0, tkinter.END)
    RSub_BOX.insert(tkinter.END, *BOX)


def del_algebraic_value_simultaneousness():
    global alg,RSub_Dic, RSub_Alg, RSub_Value
    num = RSub_BOX.curselection()[0]
    if RSub_Value != None or RSub_Alg != None:
        if num == 0:
            RSub_Value = None
            RSub_Alg = None
        else:
            num -= 1
            del RSub_Dic[list(RSub_Dic.keys())[num]]
    else:
        del RSub_Dic[list(RSub_Dic.keys())[num]]
    update_algebraic_value_box()

def add_algebraic_values_simultaneously():
    global alg, RSub_Dic, RSub_Alg,RSub_Value
    if RSub_Value != None and RSub_Alg != None:
        RSub_Dic[RSub_Alg] = RSub_Value
        RSub_Value,RSub_Alg = None,None
    update_algebraic_value_box()

def add_left_simultaneous_algebra():#代数式=值的左代数式
    global alg,RSub_Alg
    alg_name = get_algebraic_name()
    RSub_Alg = alg_name
    update_algebraic_value_box()

def add_right_simultaneous_values():#解释同上
    global alg,Value_List,Value_BOX,RSub_Value
    try:
        value_name = Value_List[Value_BOX.curselection()[0]]
    except:
        output_prompt('请选定符号')
        return False
    RSub_Value = value_name
    update_algebraic_value_box()

#执行符号->代数式联立
def value_algebraic_simultaneous():
    global alg,Sub_Dic
    name = get_algebraic_name()
    try:
        get = alg.Sub_Value(name,Sub_Dic)
        output_prompt('联立完成')
    except:
        output_prompt('无法联立')
        return False
    apply_algebraic_tips(get, f'联立结果为:{get},是否应用？')


def update_value_algebraic_box():
    global alg, Value_List, Value_BOX, Sub_Dic, Sub_Alg, Sub_Value, Sub_BOX
    BOX = []
    if Sub_Value != None or Sub_Alg != None:
        BOX.append(f'选定:{Sub_Value} = {Sub_Alg}')
    for v in Sub_Dic:
        BOX.append(f'{v} = {Sub_Dic[v]}')
    Sub_BOX.delete(0, tkinter.END)
    Sub_BOX.insert(tkinter.END, *BOX)


def del_value_algebraic_simultaneous():
    global alg, Value_List, Value_BOX, Sub_Dic, Sub_Alg, Sub_Value
    num = Sub_BOX.curselection()[0]
    if Sub_Value != None or Sub_Alg != None:
        if num == 0:
            Sub_Value = None
            Sub_Alg = None
        else:
            num -= 1
            del Sub_Dic[list(Sub_Dic.keys())[num]]
    else:
        del Sub_Dic[list(Sub_Dic.keys())[num]]
    update_value_algebraic_box()

def add_value_algebraic_simultaneous():
    global alg, Value_List, Value_BOX, Sub_Dic, Sub_Alg,Sub_Value
    if Sub_Value != None and Sub_Alg != None:
        Sub_Dic[Sub_Value] = Sub_Alg
        Sub_Value,Sub_Alg = None,None
    update_value_algebraic_box()

def add_right_simultaneous_algebra():
    global alg,Value_List,Value_BOX,Sub_Alg
    alg_name = get_algebraic_name()
    Sub_Alg = alg_name
    update_value_algebraic_box()

def add_left_simultaneous_values():
    global alg,Value_List,Value_BOX,Sub_Value
    try:
        value_name = Value_List[Value_BOX.curselection()[0]]
    except:
        output_prompt('请选定符号')
        return False
    Sub_Value = value_name
    update_value_algebraic_box()

def algebraic_digitization():
    global alg,Num_Input
    try:
        num = int(Num_Input.get())
    except:
        num = 5
    try:
        get = alg.to_num(num)
        output_prompt('数字化完成')
    except:
        output_prompt('数字化失败')
        return False
    apply_algebraic_tips(get, f'数字化的结果为:{get},是否应用？')

def expand_special():
    global alg
    name = get_algebraic_name()
    try:
        get = alg.func_Ex(name)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'展开特殊函数的结果为:{get},是否应用？')

def expand_complex():
    global alg
    name = get_algebraic_name()
    try:
        get = alg.complex_Ex(name)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'展开虚数的结果为:{get},是否应用？')

def merger_of_similar_items():
    global alg,CollX_Input
    x = CollX_Input.get().split('#')
    name = get_algebraic_name()
    try:
        get = alg.Collect(name,x)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'合并同类项的结果为:{get},是否应用？')

def general_expansion():
    global alg,EX_IM
    IM = bool(EX_IM.get())
    name = get_algebraic_name()
    try:
        get = alg.expansion(name,IM)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'普遍展开的结果为:{get},是否应用？')

def factorization():
    global alg,GAOSI, FactorM_Input,Factor_Deep,Factor_Rat
    name = get_algebraic_name()
    GS = bool(GAOSI.get())
    Deep = bool(Factor_Deep.get())
    Rat = bool(Factor_Rat.get())
    try:
        M = int(FactorM_Input.get())
    except:
        M = None
    try:
        get = alg.factor(name,M,GS,Deep,Rat)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'因式分解的结果为:{get},是否应用？')

def standardization():
    global alg,Simpratio_Input,SimpFunc_Input,simp_in,simp_rat
    try:
        radio = float(Simpratio_Input.get())
    except:radio = 1.7
    rat = bool(simp_rat.get())
    inverse = bool(simp_in.get())
    name = get_algebraic_name()
    try:
        get = alg.simplify(name,radio,rat=rat,inv=inverse)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'化简(标准化)为:{get},是否应用？')

def apply_algebraic_tips(re, message):
    if tkinter.messagebox.askokcancel('提示', message):
        alg.addAlgebra('', re)
        update_symbol_algebraic_box()

def expand_log():
    global alg,Fo_log,Deep_log
    Fo = not bool(Fo_log.get())
    Deep = bool(Deep_log.get())
    name = get_algebraic_name()
    try:
        get = alg.log_Expansion(name,Fo,Deep)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'展开对数结果为:{get},是否应用？')

def reduce_log():
    global alg,Fo_log
    Fo = not bool(Fo_log.get())
    name = get_algebraic_name()
    try:
        get = alg.log_Simp(name, Fo)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'化简对数结果为:{get},是否应用？')

def expand_mul():
    global alg,Fo_exp
    name = get_algebraic_name()
    try:
        get = alg.Mul_Expansion(name)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'展开乘法结果为:{get},是否应用？')

def expand_additive_index():
    global alg,Fo_exp
    name = get_algebraic_name()
    try:
        get = alg.Multinomial_Expansion(name)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'展开加法式幂结果为:{get},是否应用？')

def composite_index():
    global alg,Fo_exp
    name = get_algebraic_name()
    try:
        get = alg.Pow_Simp_Multinomial(name)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'合成幂指数的结果为:{get},是否应用？(彻底化简加法式幂可以使用因式分解)')

def expand_exp_base():
    global alg,Fo_exp
    deep = bool(Deep_exp.get())
    name = get_algebraic_name()
    try:
        get = alg.Pow_Expansion_base(name,deep)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'展开指数底数结果为:{get},是否应用？')

def expand_exp_index():
    global alg,Deep_exp
    deep = bool(Deep_exp.get())
    name = get_algebraic_name()
    try:
        get = alg.Pow_Expansion_exp(name,deep)
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'展开指数幂结果为:{get},是否应用？')

def expand_power():
    global alg,Deep_exp
    deep = bool(Deep_exp.get())
    name = get_algebraic_name()
    try:
        get = alg.Pow_Expansion(name,deep)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'展开指数结果为:{get},是否应用？')

def reduce_exp_base():
    global alg,Fo_exp
    Fo = not bool(Fo_exp.get())
    name = get_algebraic_name()
    try:
        get = alg.Pow_Simp_base(name,Fo)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'化简指数底数结果为:{get},是否应用？')

def reduce_exp_index():
    global alg,Fo_exp
    Fo = not bool(Fo_exp.get())
    name = get_algebraic_name()
    try:
        get = alg.Pow_Simp_exp(name,Fo)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'化简指数幂结果为:{get},是否应用？')

def reduced_power():
    global alg,Fo_exp
    Fo = not bool(Fo_exp.get())
    name = get_algebraic_name()
    try:
        get = alg.Pow_Simp(name,Fo)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'化简指数结果为:{get},是否应用？')

def reduced_trigonometric():#三角函数化简
    global alg
    name = get_algebraic_name()
    try:
        get = alg.Trig_Simp(name)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'三角化简结果为:{get},是否应用？')

def expand_trigonometric():#三角展开
    global alg,simp_deep
    deep = bool(simp_deep.get())
    name = get_algebraic_name()
    try:
        get = alg.Trig_Expansion(name,deep)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'三角展开结果为:{get},是否应用？')

def fractional_division():#通分
    global alg
    name = get_algebraic_name()
    try:
        get = alg.Fractional_merge(name)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'分式通分结果为:{get},是否应用？')

def fraction_reduction():#约分
    global alg
    name = get_algebraic_name()
    try:
        get = alg.Fraction_reduction(name)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'分式约分结果为:{get},是否应用？')

def fractional_fission():#裂项
    global alg,apart_Input
    x = apart_Input.get().replace(' ','')
    if x == '':x = None
    name = get_algebraic_name()
    try:
        get = alg.Fractional_fission(name,x)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'分式裂项结果为:{get},是否应用？')

def fractional_synthesis():#together
    global alg,together_deep
    deep = bool(together_deep.get())
    name = get_algebraic_name()
    try:
        get = alg.as_Fraction(name, deep)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'合成分式结果为:{get},是否应用？')

def denominator_rationalization():#分母有理化
    global alg,radsymbol,radMax_Input
    #Max
    try:M = int(radMax_Input.get())
    except:M=4
    #Symbol
    s = bool(radsymbol.get())
    name = get_algebraic_name()
    try:
        get = alg.Fractional_rat(name,s,M)
        output_prompt('运算成功')
    except:
        output_prompt('运算失败')
        return False
    apply_algebraic_tips(get, f'分母有理化结果为:{get},是否应用？')

def add_operation_algebra():
    global alg,Option_BOX,Option_List
    name = get_algebraic_name()
    if name == None:return False
    Option_List.append(name)
    update_operation_box()

def del_operation_algebra():
    global Option_BOX, Option_List
    del Option_List[Option_BOX.curselection()[0]]
    update_operation_box()

def clear_operational_algebra():
    global Option_BOX, Option_List
    update_symbol_algebraic_box()

def update_operation_box():
    global Option_BOX, Option_List
    re = []
    for i in range(len(Option_List)):
        re.append(f'({i + 1}) --> {Option_List[i]}')
    Option_BOX.delete(0, tkinter.END)
    Option_BOX.insert(tkinter.END, *re)

def algebraic_composition():
    global alg, Option_List,Merge_Func_Input
    name = Option_List.copy()
    if len(name) < 2: raise Exception
    try:
        re = alg.Merge_Func(name,Merge_Func_Input.get())
        output_prompt('合成成功')
    except:
        output_prompt('合成失败')
        return False
    if tkinter.messagebox.askokcancel('提示', f'合成结果为:{re}，是否应用?'):
        alg.addAlgebra('', re)
        update_symbol_algebraic_box()

def algebraic_multiplication():
    global alg, Option_List
    name = Option_List.copy()
    if len(name)<2:raise Exception
    try:
        re = alg.Merge_Mul(name)
        output_prompt('合成成功')
    except:
        output_prompt('合成失败')
        return False
    if tkinter.messagebox.askokcancel('提示', f'合成结果为:{re}，是否应用?'):
        alg.addAlgebra('',re)
        update_symbol_algebraic_box()

def algebraic_addition():
    global alg,Option_List
    name = Option_List.copy()
    if len(name)<2:raise Exception
    try:
        re = alg.Merge_Add(name)
        output_prompt('合成成功')
    except:
        output_prompt('合成失败')
        return False
    if tkinter.messagebox.askokcancel('提示', f'合成结果为:{re}，是否应用?'):
        alg.addAlgebra('',re)
        update_symbol_algebraic_box()

def algebraic_partition():
    global alg,Deep_Split,Func_Input,Split_XS
    name = get_algebraic_name()
    Deep = Deep_Split.get()
    f = Func_Input.get().split(',')
    m = Split_XS.get()
    if m == 1:must = False
    else:must = True
    try:
        re = alg.Split_Func(name,Deep,f,must)
        output_prompt('拆分成功')
    except:
        output_prompt('拆分失败')
        return False
    if tkinter.messagebox.askokcancel('提示', f'{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?'):
        for in_alg in re[0]:
            alg.addAlgebra('',in_alg)
            update_symbol_algebraic_box()

def algebraic_similarity_split():
    global alg,Object_Input,Split_XS
    name = get_algebraic_name()
    Value = Object_Input.get().split('#')
    f = Split_XS.get()
    try:
        re = alg.Split_Add(name,Value,f)
        output_prompt('拆分成功')
    except:
        output_prompt('拆分失败')
        return False
    if tkinter.messagebox.askokcancel('提示', f'{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?'):
        for in_alg in re[0]:
            alg.addAlgebra('',in_alg)
            update_symbol_algebraic_box()

def algebraic_factorization():
    global alg,Split_XS
    name = get_algebraic_name()
    all = Split_XS.get()
    if all == 0:
        k = [True,False]
    elif all == 1:
        k = [False, False]
    else:
        k = [True, True]
    try:
        re = alg.Split_Mul(name,*k)
        output_prompt('拆分成功')
    except:
        output_prompt('拆分失败')
        return False
    if tkinter.messagebox.askokcancel('提示', f'{name}分解结果为:{re[1]},拆分之后:{re[0]}，是否应用?'):
        for in_alg in re[0]:
            alg.addAlgebra('',in_alg)
            update_symbol_algebraic_box()

#统一接口：得到alg的名字(提取第一个)
def get_algebraic_name():
    global alg_list,Alg_BOX
    try:
        name = alg_list[Alg_BOX.curselection()[0]]
    except:
        name = None
        output_prompt('请选定代数式')
    return name


def add__algebraic():
    global AlgName_Input,Alg_Input,Alg_BOX,simp_in,simp_rat,ratio_Input,simp_bool
    try:
        in_alg = Alg_Input.get()
        name = AlgName_Input.get().replace(' ','')
        if bool(simp_bool.get()):
            radio_list = ratio_Input.get().split('#')
            radio = float(radio_list[0])
            rat = bool(simp_rat.get())
            inverse = bool(simp_in.get())
            new_alg = alg.Simplify(in_alg,radio=radio,rat=rat,inv=inverse)
            if new_alg != None and tkinter.messagebox.askokcancel('提示', f'约简函数为:{new_alg}，是否应用?'):
                in_alg = new_alg
        if not alg.addAlgebra(name,in_alg):raise Exception
        update_symbol_algebraic_box()
        output_prompt('代数式新增成功')
    except:
        output_prompt('新增代数式无法应用')
#获取预测
def get_predictions():
    global Value_BOX,Value_List,alg,JS_BOX
    try:
        try:
            n = Value_List[Value_BOX.curselection()[0]]
        except:
            output_prompt('请选定符号')
            return False
        JS_BOX.delete(0, tkinter.END)
        JS_BOX.insert(tkinter.END, *alg.Value_assumptions0(n))
        output_prompt('性质预测成功')
    except:
        output_prompt('性质预测失败')
#更新列表显示
def update_symbol_algebraic_box():
    global alg,Value_BOX,Value_List,Alg_BOX,alg_list,Option_List,Option_BOX
    #保存符号
    re = alg()#0-value,1-alg
    Value_List = re[0][1]
    #显示符号
    Value_BOX.delete(0, tkinter.END)
    Value_BOX.insert(tkinter.END, *re[0][0])
    #保存代数式
    alg_list = re[1][1]
    #显示代数式
    Alg_BOX.delete(0, tkinter.END)
    Alg_BOX.insert(tkinter.END, *re[1][0])
    Option_List = []
    Option_BOX.delete(0, tkinter.END)

def add_custom_symbol():#添加自定义Symbol
    global AT, RI, PC, EO, FI, CIR, NZ, ValueName_Input,Value_BOX,NONE,INT
    #复选框系统
    C = []
    n = 0
    for i in CIR:
        C.append(i.get())
        n += C[-1]
    if n == 1:#选一个设为True
        RCIR = [['complex','real','imaginary'][C.index(1)],True]#对象，布尔
    elif n == 2:#选两个设为False
        RCIR = [['complex','real','imaginary'][C.index(0)],False]#对象，布尔
    else:
        RCIR = None#其余

    C = []
    n = 0
    for i in CIR:
        C.append(i.get())
        n += C[-1]
    if n == 1:  # 选一个设为True
        RNZ = [['positive', 'negative', 'zero'][C.index(1)], True]  # 对象，布尔
    elif n == 2:  # 选两个设为False
        RNZ = [['positive', 'negative', 'zero'][C.index(0)], False]  # 对象，布尔
    else:
        RNZ = None  # 其余
    try:
        __add_symbot_core(AT.get(), RI.get(), PC.get(), EO.get(), FI.get(), RCIR, RNZ, INT.get())
    except:
        output_prompt('自定义符号新增失败')

def add_real():#添加实数符号
    __add_symbot_core(RCIR=['real', True], ms='实数(且复数)符号')
def add_integer():#添加整数符号
    __add_symbot_core(INT=1, ms='整数(且实数)符号')
def add_non_negative_real():#非负实数
    __add_symbot_core(RNZ=['negative', False], RCIR=['real', True], ms='非负实数符号')
def add_even():#偶数
    __add_symbot_core(EO=1, ms='偶数(且整数)符号')
def add_odd():#奇数
    __add_symbot_core(EO=2, ms='奇数(且整数)符号')
def add_positive_real():#正实数
    __add_symbot_core(RNZ=['positive', True], RCIR=['real', True], ms='正实数符号')
def add_positive_integer():#正整数
    __add_symbot_core(RNZ=['positive', True], INT=1, ms='正整数符号')
def add_natural():#自然数
    __add_symbot_core(RNZ=['negative', False], INT=1, ms='自然数(非负整数)符号')
def add_no_constraints():#无约束
    __add_symbot_core(NONE=1, ms='仅满足交换律的无约束符号')
#添加Symbol的统一接口
def __add_symbot_core(AT=0, RI=0, PC=0, EO=0, FI=0, RCIR=None, RNZ=None, INT=0, NONE=0, ms='自定义符号'):
    global alg
    #代数，有理，质数，偶数，有限实数，复数，正负，整数，取消
    name_list = ValueName_Input.get().split(',')
    for name in name_list:
        try:
            if not alg.addSymbol(name, AT, RI, PC, EO, FI, RCIR, RNZ, INT, NONE,ms): raise Exception
        except:
            output_prompt(f'新增“{name}”失败')
    output_prompt(f'新增“{ms}”完成')
    update_symbol_algebraic_box()

def output_prompt(News):
    global News_BOX,T,top
    T += 1
    News = str(News)
    News_BOX.insert(0, News+f'({T})')
    top.update()

def algebraic_factory_main():
    global alg,top,Value_List,alg_list,Option_List,Sub_Dic,Sub_Value,Sub_Alg,RSub_Dic,RSub_Value,RSub_Alg,Value_Sub_Dic
    global Z_alg,Y_alg,Solve_list,Answer_List,Z_Inequality,Y_Inequality,p2D_Value,p3D_Value,T
    global bg,bbg,fg,F2,FONT,F3

    alg = Algebra_Polynomial(output_prompt)

    alg_list = []
    Value_List = []
    top = tkinter.Tk()
    bg = '#FFFAFA'#主颜色
    bbg = '#FFFAFA'#按钮颜色
    fg = '#000000'#文字颜色
    top["bg"] = bg
    FONT = ('黑体', 11)#设置字体
    # F2 = tkFont.Font(family='Fixdsys', size=16)
    F2 = ('Fixdsys',16)
    F3 = tkFont.Font(family='Fixdsys', size=11)
    top.title('CoTan代数工厂')
    top.resizable(width=False, height=False)
    top.geometry('+10+10')#设置所在位置
    Option_List = []
    Sub_Dic = {}#Sub替换字典
    Sub_Value = None#选定的Sub符号
    Sub_Alg = None#选定的Sub代数式
    RSub_Dic = {}  # Sub替换字典
    RSub_Value = None  # 选定的Sub符号
    RSub_Alg = None  # 选定的Sub代数式
    Value_Sub_Dic = {}#代数运算空列表
    Z_alg = None
    Y_alg = None
    Solve_list = []
    Answer_List = []
    Z_Inequality = None
    Y_Inequality = None
    p2D_Value = None#画图
    p3D_Value = None
    T = 0

    width_B = 13#标准宽度
    height_B=2

    global Name_Input,FZ_Input,FM_Input,NUM_BOX,AT, RI, PC, EO, FI, CIR, NZ, ValueName_Input, Value_BOX, NONE, INT
    a_y = 0
    a_x = 0
    tkinter.Label(top, text='符号名字:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    ValueName_Input = tkinter.Entry(top, width=width_B * 2)
    ValueName_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='实数符号(R)', command=add_real, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='整数符号(Z)', command=add_integer, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='非负实数符号', command=add_non_negative_real, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='偶数符号', command=add_even, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='奇数符号', command=add_odd, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='正数符号', command=add_positive_real, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='自然数符号', command=add_natural, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x , row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='正整数符号', command=add_positive_integer, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='无约束符号', command=add_no_constraints, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)
    a_y += 1
    AT = tkinter.IntVar()#代数或者超越数
    lable = ['均可','代数','超越数']
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i], variable=AT, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    RI = tkinter.IntVar()#有理数或者无理数
    lable = ['均可','有理数','无理数']
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i], variable=RI, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    PC = tkinter.IntVar()#质数合数
    lable = ['均可','质数','合数']
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i], variable=PC, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    EO = tkinter.IntVar()#奇数偶数
    lable = ['均可','偶数','奇数']
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i], variable=EO, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    CIR = []#实数虚数
    lable = ['复数','实数','虚数']
    for i in range(3):
        CIR.append(tkinter.IntVar())
        tkinter.Checkbutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i], variable=CIR[-1]).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    NZ = []#正，负，0
    lable = ['正数','负数','零']#复选框
    for i in range(3):
        NZ.append(tkinter.IntVar())
        tkinter.Checkbutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i], variable=NZ[-1]).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    FI = tkinter.IntVar()#实数
    lable = ['均可','有限实数','无穷数','广义实数']
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i], variable=FI, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)
    a_y += 1
    tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[3],
                        variable=FI, value=3).grid(column=a_x, row=a_y, sticky=tkinter.W)#同上的

    INT = tkinter.IntVar()
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='整数',
                        variable=INT).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    Value_BOX = tkinter.Listbox(top, width=width_B * 3,height = height_B*4)  # 显示符号
    Value_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=6,sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 6
    tkinter.Button(top, bg=bbg, fg=fg, text='自定义符号', command=add_custom_symbol, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)  # 添加函数
    tkinter.Button(top, bg=bbg, fg=fg, text='查看假设', command = get_predictions, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)  # 添加函数
    tkinter.Button(top, bg=bbg, fg=fg, text='删除符号', command = delete_symbol, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)  # 添加函数

    global JS_BOX
    a_y += 1
    JS_BOX = tkinter.Listbox(top, width=width_B * 3,height = height_B*5)  # 显示函数假设
    JS_BOX.grid(column=a_x, row=a_y,columnspan = 3,rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=0)
    a_x += 1

    global AlgName_Input,Alg_Input,Alg_BOX,simp_in,simp_rat,ratio_Input,simp_bool
    a_y = 0
    tkinter.Label(top, text='代数式:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y)  # 设置说明
    Alg_Input = tkinter.Entry(top, width=width_B * 2)
    Alg_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='标识:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                        row=a_y)  # 设置说明
    AlgName_Input = tkinter.Entry(top, width=width_B * 2)
    AlgName_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='标准:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                 row=a_y)  # 设置说明
    ratio_Input = tkinter.Entry(top, width=width_B * 2)
    ratio_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    simp_rat = tkinter.IntVar()
    tkinter.Checkbutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text='有理化', variable=simp_rat).grid(
        column=a_x, row=a_y, sticky=tkinter.W)

    simp_in = tkinter.IntVar()
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='忽略假设',
                        variable=simp_in).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    simp_bool = tkinter.IntVar()
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='标准化',
                        variable=simp_bool).grid(column=a_x + 1, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='清空代数式', command=clear_algebra, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成代数式', command=add__algebraic, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)  # 添加函数
    tkinter.Button(top, bg=bbg, fg=fg, text='删除代数式', command=del_algebra, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    Alg_BOX = tkinter.Listbox(top, width=width_B * 3)  # 显示代数式
    Alg_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    global Object_Input,Split_XS,Deep_Split,Func_Input,Rewrite_Input,Rewrite_F_Input,Rewrite_deep
    a_y += 4
    tkinter.Label(top, text='重写对象:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y)  # 设置说明
    Rewrite_F_Input = tkinter.Entry(top, width=width_B*2)
    Rewrite_F_Input.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.W + tkinter.E)


    a_y += 1
    tkinter.Label(top, text='重写方法:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Rewrite_Input = tkinter.Entry(top, width=width_B*2)
    Rewrite_Input.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.W + tkinter.E)

    a_y += 1
    Rewrite_deep = tkinter.IntVar()
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='重写子代数式',
                        variable=Rewrite_deep).grid(column=a_x+2, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='重写代数式', command=rewrite_algebra, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='同类项:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Object_Input = tkinter.Entry(top, width=width_B * 2)
    Object_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    Split_XS = tkinter.IntVar()#正，负，0
    lable = ['仅系数(同类项)','仅代数式','均保留']#复选框
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i], variable=Split_XS, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Label(top, text='拆分函数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)  # 设置说明
    Func_Input = tkinter.Entry(top, width=width_B)
    Func_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    Deep_Split = tkinter.IntVar()
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='完全拆分',
                        variable=Deep_Split).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='同类项拆分', command=algebraic_similarity_split, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='乘法拆分', command=algebraic_factorization, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)  # 添加函数
    tkinter.Button(top, bg=bbg, fg=fg, text='函数拆分', command=algebraic_partition, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Option_BOX
    a_y += 1
    Option_BOX = tkinter.Listbox(top, width=width_B * 3,height = height_B*4)  # 显示代数式
    Option_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 4
    tkinter.Button(top, bg=bbg, fg=fg, text='添加', command=add_operation_algebra, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空', command=clear_operational_algebra, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)  # 添加函数
    tkinter.Button(top, bg=bbg, fg=fg, text='删除', command=del_operation_algebra, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Merge_Func_Input
    a_y += 1
    tkinter.Label(top, text='合成函数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Merge_Func_Input = tkinter.Entry(top, width=width_B * 2)
    Merge_Func_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='多项式合成', command=algebraic_addition, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='因式合成', command=algebraic_multiplication, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)  # 添加函数
    tkinter.Button(top, bg=bbg, fg=fg, text='函数合成', command=algebraic_composition, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Num_Input
    a_y += 1
    tkinter.Label(top, text='有效数字:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x+1,
                                                                                                   row=a_y)  # 设置说明
    Num_Input = tkinter.Entry(top, width=width_B)
    Num_Input.grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    tkinter.Button(top, bg=bbg, fg=fg, text='代数式数字化', command=algebraic_digitization, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=0)

    a_x += 1
    a_y = 0
    tkinter.Label(top, text='【分式恒等变形】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(
        column=a_x,row=a_y,columnspan=3)  # 设置说明

    global apart_Input,together_deep,radsymbol,radMax_Input
    a_y += 1
    together_deep = tkinter.IntVar()
    tkinter.Label(top, text='裂项关注对象:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    apart_Input = tkinter.Entry(top, width=width_B)
    apart_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='完全转化分式',
                        variable=together_deep).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    radsymbol = tkinter.IntVar()
    tkinter.Label(top, text='最大无理项:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    radMax_Input = tkinter.Entry(top, width=width_B)
    radMax_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='有理化符号分母',
                        variable=radsymbol).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='最小公分母', command=fractional_division, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='分式约分', command=fraction_reduction, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='分式裂项', command=fractional_fission, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='分母有理化', command=denominator_rationalization, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='转化为分式(小改动)', command=fractional_synthesis, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='【三角恒等变换】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(
        column=a_x,row=a_y,columnspan=3)  # 设置说明

    global simp_deep
    a_y += 1
    simp_deep = tkinter.IntVar()
    tkinter.Button(top, bg=bbg, fg=fg, text='展开三角函数', command=expand_trigonometric, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='三角函数合成', command=reduced_trigonometric, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='完全展开',
                        variable=simp_deep).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    global Fo_exp,Deep_exp
    a_y += 1
    tkinter.Label(top, text='【乘法、指数、对数恒等变形】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(
        column=a_x,row=a_y,columnspan=3)  # 设置说明

    a_y += 1
    Fo_exp = tkinter.IntVar()
    Deep_exp = tkinter.IntVar()
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='忽略假设',
                        variable=Fo_exp).grid(column=a_x + 1, row=a_y, sticky=tkinter.W)

    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='完全展开',
                        variable=Deep_exp).grid(column=a_x, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='展开乘法', command=expand_mul, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='展开加法式幂', command=expand_additive_index, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='指数合成', command=composite_index, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='化简指数底数', command=reduce_exp_base, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='化简指数幂', command=reduce_exp_index, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='化简指数', command=reduced_power, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='展开指数底数', command=expand_exp_base, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='展开指数幂', command=expand_exp_index, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='展开指数', command=expand_power, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Fo_log,Deep_log
    Fo_log = tkinter.IntVar()
    Deep_log = tkinter.IntVar()

    a_y += 1
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='完全展开',
                        variable=Deep_log).grid(column=a_x, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='忽略假设',
                        variable=Fo_log).grid(column=a_x+1, row=a_y, sticky=tkinter.W)
    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='展开对数', command=expand_log, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='化简对数', command=reduce_log, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='【虚数与特殊函数】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(
        column=a_x,row=a_y,columnspan=3)  # 设置说明
    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='展开特殊函数', command=expand_special, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='展开虚数', command=expand_complex, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W)


    global Simpratio_Input,SimpFunc_Input
    a_y += 1
    tkinter.Label(top, text='【普遍操作类】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(
        column=a_x,row=a_y,columnspan=3)  # 设置说明
    a_y += 1
    tkinter.Label(top, text='简化方案:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    SimpFunc_Input = tkinter.Entry(top, width=width_B)#简化方案
    SimpFunc_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='有理化',
                        variable=simp_rat).grid(column=a_x+2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Label(top, text='简化比率:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Simpratio_Input = tkinter.Entry(top, width=width_B)#简化比率
    Simpratio_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='忽略假设',
                        variable=simp_in).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    global GAOSI,FactorM_Input,Factor_Deep,Factor_Rat
    GAOSI = tkinter.IntVar()
    Factor_Deep = tkinter.IntVar()
    Factor_Rat = tkinter.IntVar()
    a_y += 1
    tkinter.Label(top, text='模数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    FactorM_Input = tkinter.Entry(top, width=width_B)  # 简化比率
    FactorM_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='高斯因式分解',
                        variable=GAOSI).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='完全因式分解',
                        variable=Factor_Deep).grid(column=a_x, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='因式分解有理代数式',
                        variable=Factor_Rat).grid(column=a_x+1, row=a_y,columnspan=2, sticky=tkinter.W)

    global EX_IM,CollX_Input
    a_y += 1
    EX_IM = tkinter.IntVar()
    tkinter.Label(top, text='同类项对象:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    CollX_Input = tkinter.Entry(top, width=width_B)
    CollX_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='展开复数',
                        variable=EX_IM).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='化简标准化', command=standardization, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='普遍运算展开', command=general_expansion, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='因式分解', command=factorization, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='合并同类项', command=merger_of_similar_items, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,columnspan=3, sticky=tkinter.E + tkinter.W)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=0)
    a_x += 1

    a_y = 0
    tkinter.Label(top, text='【联立操作】', bg=bg, fg=fg, font=FONT, width=width_B*3, height=height_B).grid(
        column=a_x,row=a_y,columnspan=3)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='选定符号', command = add_left_simultaneous_values, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='选定代数式', command = add_right_simultaneous_algebra, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='新键联立', command = add_value_algebraic_simultaneous, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成联立代数式', command=value_algebraic_simultaneous, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, columnspan=2,row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除联立', command = del_value_algebraic_simultaneous, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Sub_BOX
    a_y += 1
    Sub_BOX = tkinter.Listbox(top, width=width_B * 3,height = height_B*4)  # 显示代数式
    Sub_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 4
    tkinter.Label(top, text='【反向联立操作】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x, row=a_y, columnspan=3)  # 设置说明

    #反向联立系统
    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='选定代数式', command=add_left_simultaneous_algebra, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='选定符号', command=add_right_simultaneous_values, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='新键联立', command=add_algebraic_values_simultaneously, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成联立代数式', command=algebraic_value_simultaneous, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除联立', command=del_algebraic_value_simultaneousness, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global RSub_BOX
    a_y += 1
    RSub_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)  # 显示代数式
    RSub_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    global ValueNUM_Input,Num_Type
    #代数运算
    a_y += 4
    tkinter.Label(top, text='【赋值运算操作】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x, row=a_y, columnspan=3)  # 设置说明

    a_y += 1
    tkinter.Label(top, text='数值:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    ValueNUM_Input = tkinter.Entry(top, width=width_B+2)
    ValueNUM_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='指定符号', command=add_variable_assignment, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    Num_Type = tkinter.IntVar()#正，负，0
    lable = ['浮点数','整数','分数有理数','无约束数字']#复选框
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg,
                            text=lable[i], variable=Num_Type, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)
    a_y += 1
    tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg,
                        text=lable[3], variable=Num_Type, value=3).grid(column=a_x + 1, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成赋值代数式', command=algebraic_assignment, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除赋值', command=del_variable_assignment, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global ValueNUM_BOX
    a_y += 1
    ValueNUM_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)  # 显示代数式
    ValueNUM_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=0)
    a_x += 1

    a_y = 0
    tkinter.Label(top, text='【方程联立】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x, row=a_y, columnspan=3)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='左代数式', command=add_equation_left, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='右代数式', command=add_equation_right, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='新建方程', command=generating_equation, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='解联立方程', command=solve_simultaneous_equations, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除方程', command=del_equation, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Solve_BOX
    a_y += 1
    Solve_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)  # 显示代数式
    Solve_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y +=2
    tkinter.Button(top, bg=bbg, fg=fg, text='应用为代数式', command=add_to_algebraic_box, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='添加联立', command=add_to_value_algebraic_box, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='添加反联立', command=add_to_algebraic_value_box, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Answer_BOX
    a_y += 1
    Answer_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)  # 显示代数式
    Answer_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 2
    tkinter.Label(top, text='【解不等式】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x, row=a_y, columnspan=3)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='左代数式', command=add_left_algebra, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='右代数式', command=add_right_algebra, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='不等式运算', command=inequality_solve, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Inequality_BOX,Inequality_Type,AnswerInequality_BOX,Range_Input
    a_y += 1
    Inequality_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B)  # 显示代数式
    Inequality_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=1, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    Inequality_Type = tkinter.IntVar()#实数
    lable = ['大于>','小于<','大于等于>=','小于等于<=']
    for i in range(2):
        tkinter.Radiobutton(top, command=update_inequality_box, bg = bg, fg = fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i], variable=Inequality_Type, value=i).grid(column=a_x + i, row=a_y, sticky=tkinter.W)
    a_y += 1
    for i in range(2):
        i += 2
        tkinter.Radiobutton(top, command=update_inequality_box, bg = bg, fg = fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i], variable=Inequality_Type, value=i).grid(column=a_x + i - 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    AnswerInequality_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B)  # 显示代数式
    AnswerInequality_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 2
    tkinter.Label(top, text='【代数式画图】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x, row=a_y, columnspan=3)  # 设置说明

    a_y += 1
    tkinter.Label(top, text='符号取值范围:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)  # 设置说明
    Range_Input = tkinter.Entry(top, width=width_B+2)
    Range_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='指定符号', command=add_plot_value, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global PlotValue_BOX,Plot_Type
    a_y += 1
    PlotValue_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B)  # 显示代数式
    PlotValue_BOX.grid(column=a_x, row=a_y, columnspan=3, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    Plot_Type = tkinter.IntVar()#实数
    lable = ['二维图像','三维图像']
    for i in range(2):
        tkinter.Radiobutton(top, command=update_plot_value, bg = bg, fg = fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i], variable=Plot_Type, value=i).grid(column=a_x + i, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='绘制图像', command=drawing_image, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='绘制代数式', command=draw_algebra_core, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='绘制树状图', command=show_algebraic, font=FONT, width=width_B,
                   height=height_B).grid(
        column=a_x + 1, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W)

    global News_BOX,Can_Input,kd_bool,logkd_bool
    a_y += 1
    kd_bool = tkinter.IntVar()
    logkd_bool = tkinter.IntVar()
    Can_Input = tkinter.Entry(top, width=width_B)
    Can_Input.grid(column=a_x, row=a_y, sticky=tkinter.W+tkinter.E)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='每项绘制括号',
                        variable=kd_bool).grid(column=a_x+1, row=a_y,columnspan=2, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='对数绘制括号',
                        variable=logkd_bool).grid(column=a_x+2, row=a_y,columnspan=2, sticky=tkinter.W)

    a_y += 1
    News_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B)  # 显示代数式
    News_BOX.grid(column=a_x, row=a_y, columnspan=3,rowspan=3, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    output_prompt('加载完成')
    top.mainloop()
