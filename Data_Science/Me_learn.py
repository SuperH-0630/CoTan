import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.messagebox
from Data_Science import Learn
import webbrowser
import os
from tkinter.scrolledtext import ScrolledText
import chardet

# 数据清洗
clean_default_script = '''#输入你的数据清洗执行代码

Done_Row=[] #输入操作的行号
Done_Column=[] #输入操作的列号
axis=True #True-操作行，False-操作列
name='' #方法代号

def check(data, row, column, get, R, C): #检查方法
    return True

def done(data, row, column, get, R, C): #应用修正方法
    return DEL
'''

clean_help = '''
使用Python代码进行数据清洗
1)代码结构
    Done_Row=[] 代码用来检测的数据的列号
    Done_Column=[] 代码用来检测的数据的行号
        不在以上指定范围内的数据将不会被检测，若为空则整个表格检测
    axis 执行删除方法时删除行或者列
    name 方法代号
    
    check 检查方法
        输入:当前的值(输入的是一个值而不是一行(列)或整个列表)
        输入:row和column当前值来自的行号(row)和列号(column)
        输入:get当前检查的所有数据:类型是表格
        输入:R和C当前值所来自的行和列的所有数据:类型是一维表格
        
        输出:输出布尔为True代表该值可以使用，输出布尔为假表示该值不可使用
        
    done 不可使用的数值改造方法
        输入:内容同上
        输出:改造值或者DEL
            DEL:代表删除改值所在的行(axis=True)或列(axis=False)
2)扩展
    默认:pd-pandas，re-re[正则表达式]，Sheet-包含所有表格，用Sheet['name']访问名字为name的表格(注意引号别漏了)
    支持:可以使用import导入语句，支持python语法
'''

drawing_parameters = '''
输入python变量赋值代码:渲染设置
title #设置标题:str
vice_title #设置副标题:str

show_Legend #是否显示图例:bool

show_Visual_mapping #是否使用视觉映射:bool
is_color_Visual_mapping #是否为颜色视觉映射:bool[否则为大小视觉映射]
min_Visual_mapping #映射的最小值
max_Visual_mapping #映射的最大值

......(我太懒了, 设置太多不想写了)
'''


# top = None
# ML = None
# Form_List = None
# PATH = None
# bg = None
# ft1 = None
# Stored_List = None
# Clean_List = None
# R_Dic = None
# Over_Up = None
# Over_Down = None
#
# Form_BOX = None
# Index_BOX = None
# Column_BOX = None
# to_HTML_Type = None
# Seq_Input = None
# Code_Input = None
# str_must = None
# Index_must = None

def machine_learning():
    global top, ML, Form_List, PATH, bg, ft1, Stored_List, Clean_List, R_Dic, Over_Up, Over_Down, Learn_Dic
    R_Dic = {}  # 保存了画图的List
    Learn_Dic = {}  # 保存数据处理
    PATH = os.getcwd()
    Form_List = []
    ML = Learn.Machine_Learner()
    top = tkinter.Tk()
    bg = '#FFFAFA'  # 主颜色
    bbg = '#FFFAFA'  # 按钮颜色
    fg = '#000000'  # 文字颜色
    top["bg"] = bg
    FONT = ('黑体', 11)  # 设置字体
    ft1 = ('黑体', 13)
    top.title('CoTan数据处理')
    top.resizable(width=False, height=False)
    top.geometry('+10+10')  # 设置所在位置
    width_B = 13  # 标准宽度
    height_B = 2
    a_y = 0
    a_x = 0
    Stored_List = []
    Clean_List = []
    # 层叠多图
    Over_Down = None
    Over_Up = None

    tkinter.Button(top, bg=bbg, fg=fg, text='导入CSV', command=add_csv, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导入Py', command=add_from_python, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导出CSV', command=to_csv, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    global name_Input
    a_y += 1
    tkinter.Label(top, text='表格名称:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y)  # 设置说明
    name_Input = tkinter.Entry(top, width=width_B)
    name_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='删除表格', command=del_form, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看表格', command=show_sheet_html, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看单一表格', command=show_one_sheet_html, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    global Form_BOX, Index_BOX, Column_BOX, to_HTML_Type, Seq_Input, Code_Input, str_must, Index_must
    a_y += 1
    to_HTML_Type = tkinter.IntVar()  # 正，负，0
    lable = ['选项卡型', '可移动型', '自适应型']  # 复选框
    for i in range(3):
        tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i],
                            variable=to_HTML_Type,
                            value=i).grid(column=a_x + i, row=a_y, sticky=tkinter.W)

    str_must = tkinter.IntVar()
    Index_must = tkinter.IntVar()
    a_y += 1
    tkinter.Label(top, text='编码方式:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y)  # 设置说明
    Code_Input = tkinter.Entry(top, width=width_B)
    Code_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    buttom = tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg,
                                 text='字符串类型',
                                 variable=str_must)
    buttom.grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Label(top, text='CSV分隔符:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)  # 设置说明
    Seq_Input = tkinter.Entry(top, width=width_B)
    Seq_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='重置列名',
                        variable=Index_must).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    Form_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 5)  # 显示符号
    Form_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 5
    tkinter.Button(top, bg=bbg, fg=fg, text='查看行名', command=get_row, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看列名', command=get_column, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='显示表格', command=show_sheet, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    global Max_Row, Max_Column
    a_y += 1
    tkinter.Label(top, text='最大显示行数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)  # 设置说明
    Max_Row = tkinter.Entry(top, width=width_B * 2)
    Max_Row.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='最大显示列数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)  # 设置说明
    Max_Column = tkinter.Entry(top, width=width_B * 2)
    Max_Column.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    # Row与Column Row是横行，tkinter布局中Row变大，表示所在行数变大，向下移动如：
    # 1，2，3，4，5，6
    # 7，8，9，a，b，c
    # 其中数字1-6是第一行，1-c是第二行，第二行在第一行下面，row变大向下移动（Row是横向行而不是横向移动） to 搞不清楚横行竖列的人

    a_y += 1
    Index_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 10)  # 显示符号
    Index_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=10, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    global Des_Bool
    a_y += 10
    tkinter.Button(top, bg=bbg, fg=fg, text='查看数据分析', command=show_report, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='简单数据统计', command=show_describe, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    Des_Bool = tkinter.IntVar()  # 是否启用
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='生成统计表格',
                        variable=Des_Bool).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【数据清洗】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                        columnspan=3,
                                                                                                        row=a_y,
                                                                                                        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    global Slice_new, Column_Type, Row_Type, Column_clist, Row_clist
    Column_clist = []
    Row_clist = []
    label = ['启始(列号):', '终止(列):', '间隔(列):']
    for i in range(3):
        a_y += 1
        tkinter.Label(top, text=label[i], bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                        row=a_y)  # 设置说明
        Column_clist.append(tkinter.Entry(top, width=width_B * 2))
        Column_clist[-1].grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.W + tkinter.E)

    label = ['启始(行号):', '终止(行):', '间隔(行):']
    for i in range(3):
        a_y += 1
        tkinter.Label(top, text=label[i], bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                        row=a_y)  # 设置说明
        Row_clist.append(tkinter.Entry(top, width=width_B * 2))
        Row_clist[-1].grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.W + tkinter.E)

    a_y += 1
    Column_Type = tkinter.IntVar()
    lable = ['根据列号', '根据列名', '输入列号']  # 复选框
    for i in range(3):
        tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i],
                            variable=Column_Type, value=i). \
            grid(column=a_x + i, row=a_y, sticky=tkinter.W)

    a_y += 1
    Row_Type = tkinter.IntVar()
    lable = ['根据行号', '根据行名', '输入行号']  # 复选框
    for i in range(3):
        tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i],
                            variable=Row_Type, value=i). \
            grid(column=a_x + i, row=a_y, sticky=tkinter.W)

    a_y += 1
    Slice_new = tkinter.IntVar()
    tkinter.Button(top, bg=bbg, fg=fg, text='切片选定', command=slice_data, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除选定', command=del_data, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='生成新表格',
                        variable=Slice_new).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    global Bool_E, Drop_Column
    a_y += 1
    tkinter.Label(top, text='布尔逻辑:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y,
                                                                                                   sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明
    Bool_E = tkinter.Entry(top, width=width_B * 2)
    Bool_E.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.W + tkinter.E)

    a_y += 1
    tkinter.Label(top, text='操作的列号:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                    row=a_y,
                                                                                                    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明
    Drop_Column = tkinter.Entry(top, width=width_B * 2)
    Drop_Column.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.W + tkinter.E)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成布尔表格', command=to_bool, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看空值', command=is_NaN, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='清洗空值(按行)', command=clear_NaN_by_row, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='添加执行方法', command=add_cleaning_script, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除执行方法', command=del_cleaning_script, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='数据特征提取', command=feature_extraction, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    global Done_CleanBox, Done_Func
    a_y += 1
    Done_CleanBox = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)
    Done_CleanBox.grid(column=a_x, row=a_y, columnspan=3, rowspan=2,
                       sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 2
    tkinter.Button(top, bg=bbg, fg=fg, text='查看词典', command=show_dictionary, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='恢复显示', command=reset, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='执行数据清洗', command=execute_cleaning_script, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    Done_Func = tkinter.Text(top, width=width_B * 3, height=height_B * 7)
    Done_Func.grid(column=a_x, row=a_y, columnspan=3, rowspan=7, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)
    Done_Func.insert('0.0', clean_default_script)

    a_y += 7
    tkinter.Button(top, bg=bbg, fg=fg, text='清空执行方法', command=empty_cleaning_script, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看执行方法', command=view_cleaning_script, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导入执行方法', command=open_python, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【数据可视化】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                         columnspan=3,
                                                                                                         row=a_y,
                                                                                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成柱状图', command=to_Bar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成3D柱状图', command=to_Bar3d, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成折线图', command=to_Line, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成3D折线图', command=to_Line3D, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成象形柱状图', command=to_Pictorialbar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y, columnspan=2,
                                         sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成散点图', command=to_Scatter, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成3D散点图', command=to_Scatter3D, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成箱形图', command=to_Boxpolt, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成漏斗图', command=to_Funnel, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成热力图', command=to_HeatMap, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成饼图', command=to_Pie, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成多轴图', command=to_Parallel, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成极坐标图', command=to_Polar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成雷达图', command=to_Radar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成词云', command=to_WordCloud, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成关系图', command=to_Graph, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成XY关系图', command=to_XY_Graph, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成水球图', command=to_Liquid, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, columnspan=2,
                                         sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成仪表图', command=to_Gauge, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成日历图', command=to_Calendar, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成河流图', command=to_ThemeRiver, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成旭日图', command=to_Sunburst, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成桑基图', command=to_Sankey, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成树状图', command=to_Tree, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成矩形树图', command=to_TreeMap, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='生成Map地图', command=to_Map, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成Geo点地图', command=to_ScatterGeo, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成Geo地图', command=to_Geo, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='选择底图', command=add_basemap, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='选择顶图', command=add_top_image, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='生成层叠图', command=make_OverLap, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    global R_BOX, Args_Input, Over_BOX
    Over_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)
    Over_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='渲染HTML', command=rendering, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='单独渲染HTML', command=rendering_one, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除渲染', command=del_rendering, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    R_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B)
    R_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 2
    global Draw_asWell
    Draw_asWell = tkinter.IntVar()
    tkinter.Button(top, bg=bbg, fg=fg, text='清空渲染', command=clear_rendering, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='导入渲染', command=python_render, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='马上渲染',
                        variable=Draw_asWell).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)
    a_y += 1
    Args_Input = tkinter.Text(top, width=width_B * 3, height=height_B * 7)
    Args_Input.grid(column=a_x, row=a_y, columnspan=3, rowspan=7, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)

    a_y += 7
    tkinter.Button(top, bg=bbg, fg=fg, text='查看词典', command=show_dictionary, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='恢复显示', command=show_tips, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y, columnspan=2,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【行名与列名】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                         columnspan=3,
                                                                                                         row=a_y,
                                                                                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    global replace_Dic, Repalce_RC, replace_iloc, Date_Input, RC_Type
    a_y += 1
    Repalce_RC = tkinter.IntVar()
    lable = ['(列数据)调整行名', '(行数据)调整列名']  # 复选框
    for i in range(2):
        tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i],
                            variable=Repalce_RC, value=i).grid(column=a_x + i, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='植入行(列)号', command=num_with_name, font=FONT, width=width_B,
                   height=height_B). \
        grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    RC_Type = []
    lable = ['保留原值', '保留新值']  # 复选框
    for i in range(2):
        RC_Type.append(tkinter.IntVar())
        tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i],
                            variable=RC_Type[-1]).grid(column=a_x + i, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='统一行(列)号', command=num_to_name, font=FONT, width=width_B, height=height_B). \
        grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='替换字典:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y)  # 设置说明
    replace_Dic = tkinter.Entry(top, width=width_B * 2)
    replace_Dic.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='替换列(行):', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)  # 设置说明
    replace_iloc = tkinter.Entry(top, width=width_B * 2)
    replace_iloc.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='执行替换已有列(行)操作', command=change_index, font=FONT, width=width_B * 2,
                   height=height_B). \
        grid(column=a_x, columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='执行替换操作', command=replace_index, font=FONT, width=width_B, height=height_B). \
        grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    label = ['起点', '终点', '间隔']
    Date_Input = []
    for i in range(3):
        a_y += 1
        tkinter.Label(top, text='时间序列' + label[i], bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(
            column=a_x, row=a_y)  # 设置说明
        Date_Input.append(tkinter.Entry(top, width=width_B * 2))
        Date_Input[-1].grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    global Date_Type
    a_y += 1
    Date_Type = tkinter.IntVar()
    tkinter.Button(top, bg=bbg, fg=fg, text='刷入Date序列', command=date_index, font=FONT, width=width_B, height=height_B). \
        grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='刷入Time序列', command=time_index, font=FONT, width=width_B, height=height_B). \
        grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='使用间隔',
                        variable=Date_Type).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    global Dtype_Column, Dtype_Input, Dtype_Wrong, Dtype_Func
    a_y += 1
    tkinter.Label(top, text='【数据类型管理】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                          columnspan=3,
                                                                                                          row=a_y,
                                                                                                          sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Label(top, text='修改(列号):', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)  # 设置说明
    Dtype_Column = tkinter.Entry(top, width=width_B * 2)
    Dtype_Column.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='数据类型:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                   row=a_y)  # 设置说明
    Dtype_Input = tkinter.Entry(top, width=width_B * 2)
    Dtype_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='错误值:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                  row=a_y)  # 设置说明
    Dtype_Wrong = tkinter.Entry(top, width=width_B * 2)
    Dtype_Wrong.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='执行转换', command=set_dtype, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    Dtype_Func = tkinter.IntVar()  # 正，负，0
    lable = ['硬转换', '软转换']  # 复选框
    for i in range(2):
        tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i],
                            variable=Dtype_Func, value=i).grid(column=a_x + 1 + i, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Label(top, text='【排序操作】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                        columnspan=3,
                                                                                                        row=a_y)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='.T', command=transpose, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='按行名排序', command=sort_by_tow, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='按列名排序', command=sort_by_column, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    global Sort_By, Ascending_Type, Ascending_New, Stored_BOX
    a_y += 1
    tkinter.Label(top, text='基准列(列号):', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y)  # 设置说明
    Sort_By = tkinter.Entry(top, width=width_B + 2)
    Sort_By.grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='按数据排序', command=stored_value, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    Ascending_Type = tkinter.IntVar()
    Ascending_New = tkinter.IntVar()
    lable = ['正序排列', '倒序排列']  # 复选框
    for i in range(2):
        tkinter.Radiobutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text=lable[i],
                            variable=Ascending_Type, value=i). \
            grid(column=a_x + i, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='生成新表格',
                        variable=Ascending_New).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    Stored_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)  # 显示符号
    Stored_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 5
    tkinter.Button(top, bg=bbg, fg=fg, text='添加基准', command=add_baseline, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除基准', command=del_baseline, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='打乱表格', command=sample_data, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【机器学习】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                        columnspan=3,
                                                                                                        row=a_y,
                                                                                                        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    global ML_BOX, ML_OUT
    a_y += 1
    ML_OUT = tkinter.StringVar()
    Put = tkinter.Entry(top, width=width_B * 2, textvariable=ML_OUT)
    Put.grid(column=a_x, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)
    Put['state'] = 'readonly'
    tkinter.Button(top, bg=bbg, fg=fg, text='选用学习器', command=set_learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Split_Input
    a_y += 1
    tkinter.Label(top, text='测试数据分割:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                     row=a_y)
    Split_Input = tkinter.Entry(top, width=width_B * 2)
    Split_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    ML_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 5)
    ML_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 5
    tkinter.Button(top, bg=bbg, fg=fg, text='导入学习器', command=rendering, font=FONT, width=width_B, height=height_B).grid(
        column=a_x, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看数据', command=visual_learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除学习器', command=del_learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='训练机器', command=fit_learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='测试机器', command=test_learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='数据预测', command=predict_learner, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Label(top, text='【学习器选择和配置】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(column=a_x,
                                                                                                            columnspan=3,
                                                                                                            row=a_y,
                                                                                                            sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='线性回归', command=add_GeneralizedLinear, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='岭回归', command=add_Ridge, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='Lasso', command=add_Lasso, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='逻辑回归', command=add_LogisticRegression, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='决策树', command=show_sorry, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 1, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='SVM', command=show_sorry, font=FONT, width=width_B, height=height_B).grid(
        column=a_x + 2, row=a_y,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='朴素贝叶斯', command=show_sorry, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='K邻近分类', command=add_KnnRegression, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 1, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(top, bg=bbg, fg=fg, text='K邻近预测', command=add_KnnClass, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x + 2, row=a_y,
                                         sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    global Args_Learner
    a_y += 1
    Args_Learner = tkinter.Text(top, width=width_B * 3, height=height_B * 11)
    Args_Learner.grid(column=a_x, row=a_y, columnspan=3, rowspan=11,
                      sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)

    top.mainloop()


def show_tips():
    tkinter.messagebox.showinfo('使用提示', drawing_parameters)


def show_sorry():
    tkinter.messagebox.showinfo('非常抱歉', '高级别的机器学习请到机器学习板块深入研究...')


def clear_rendering():
    ML.Tra_RDic()
    update_render_box()


def del_form():
    name = get_sheet_name()
    ML.Del_Form(name)
    update_sheet_box()


def del_learner():
    Learn = get_learner_name(True)
    set_Learne = get_learner_name(False)  # 获取学习器Learner
    if set_Learne != Learn:
        ML.Del_Leaner(Learn)
    update_leaner_box()


def visual_learner():
    learner = get_learner_name(True)
    new = tkinter.messagebox.askokcancel('提示', f'是否将数据生成表格。\n(可绘制成散点图对比数据)')
    Data = ML.Show_Args(learner, new)
    title = f'CoTan数据处理 查看数据:{learner}'
    vitables(f'对象:{learner}\n\n{Data[0]}\n\n\n{Data[1]}', title)
    update_sheet_box()


def get_learner_config():
    global Args_Learner
    return Args_Learner.get('0.0', tkinter.END)


def test_learner():
    global ML
    print('F')
    name = get_sheet_name()  # 表格数据
    learner = get_learner_name()
    try:
        split = float(Split_Input.get())
        if split < 0 or 1 < split: raise Exception
    except:
        split = 0.3
    socore = ML.Fit(name, learner, Score_Only=True, split=split)[1]
    tkinter.messagebox.showinfo('测试完成', f'针对测试数据评分结果为:{socore}')


def predict_learner():
    name = get_sheet_name()  # 表格数据
    learner = get_learner_name()
    Data = ML.Predict(name, learner)
    title = f'CoTan数据处理 表格:{name} 学习器:{learner}'
    vitables(Data, title)
    update_sheet_box()


def fit_learner():
    name = get_sheet_name()  # 表格数据
    learner = get_learner_name()
    try:
        split = float(Split_Input.get())
        if split < 0 or 1 < split: raise Exception
    except:
        split = 0.3
    socore = ML.Fit(name, learner, Text=get_learner_config(), split=split)
    tkinter.messagebox.showinfo('训练完成', f'针对训练数据({(1 - split) * 100}%)评分结果为:{socore[0]}\n'
                                        f'针对测试数据评分({split * 100}%)结果为:{socore[1]}')


def set_learner():
    global ML_OUT
    ML_OUT.set(get_learner_name(True))


def get_learner_name(Type=False):
    global Learn_Dic, ML_BOX, ML_OUT
    if Type:
        try:
            return list(Learn_Dic.keys())[ML_BOX.curselection()[0]]
        except:
            # raise
            try:
                return list(Learn_Dic.keys)[0]
            except:
                return None
    else:
        try:
            return ML_OUT.get()
        except:
            return None


def add_KnnClass():
    add_learner_core('Knn_class')


def add_LogisticRegression():
    add_learner_core('LogisticRegression')


def add_Lasso():
    add_learner_core('Lasso')


def add_KnnRegression():
    add_learner_core('Knn')


def add_Ridge():
    add_learner_core('Ridge')


def add_GeneralizedLinear():
    add_learner_core('Line')


def add_learner_core(Type):  # 添加Lenear的核心
    ML.Add_Learner(Type, Text=get_learner_config())
    update_leaner_box()


def update_leaner_box():
    global Learn_Dic, ML_BOX
    Learn_Dic = ML.Return_Learner()
    ML_BOX.delete(0, tkinter.END)
    ML_BOX.insert(tkinter.END, *Learn_Dic.keys())


def feature_extraction():
    name = get_sheet_name()
    ML.DecisionTreeClassifier(name)
    update_sheet_box()


def replace_index():
    global replace_Dic, Repalce_RC, ML
    name = get_sheet_name()
    Dic = eval(replace_Dic.get())
    is_Column = bool(Repalce_RC.get())  # 操作行-False，操作列-True
    save = bool(RC_Type[0].get())
    ML.Replace_Index(name, is_Column, Dic, save)
    update_sheet_box()


def change_index():
    global Repalce_RC, replace_iloc, RC_Type, ML
    name = get_sheet_name()  # 名字
    is_Column = bool(Repalce_RC.get())  # 操作行名-False，操作列名-True
    iloc = int(replace_iloc.get())  # 替换的列号(行号)
    save = bool(RC_Type[0].get())
    drop = not bool(RC_Type[1].get())

    ML.Change_Index(name, is_Column, iloc, save, drop)
    update_sheet_box()


def num_to_name():
    global Repalce_RC, replace_iloc, RC_Type, ML
    name = get_sheet_name()  # 名字
    is_Column = bool(Repalce_RC.get())  # 操作行名-False，操作列名-True
    save = bool(RC_Type[0].get())

    ML.num_toName(name, is_Column, save)
    update_sheet_box()


def num_with_name():
    global Repalce_RC, RC_Type, ML
    name = get_sheet_name()  # 名字
    is_Column = bool(Repalce_RC.get())  # 操作行名-False，操作列名-True
    save = bool(RC_Type[0].get())

    ML.num_withName(name, is_Column, save)
    update_sheet_box()


def datetime_index(is_Date=True):
    global Repalce_RC, RC_Type, ML, Date_Input, Date_Type
    name = get_sheet_name()  # 名字
    is_Column = bool(Repalce_RC.get())  # 操作行名-False，操作列名-True
    save = bool(RC_Type[0].get())

    k = ['start', 'end', 'freq']
    Init = {}
    for i in range(len(Date_Input)):
        Input = Date_Input[i].get()
        if Input == '': continue
        Init[k[i]] = Input
    if len(Init) == 3:
        if bool(Date_Type.get()):  # 使用间隔
            del Init['end']
        else:
            del Init['freq']
    if is_Date:
        ML.date_index(name, is_Column, save, **Init)
    else:
        ML.Time_Index(name, is_Column, save, **Init)
    update_sheet_box()


def date_index():
    datetime_index(True)


def time_index():
    datetime_index(False)


def set_dtype():
    global Dtype_Column, Dtype_Input, Dtype_Wrong, Dtype_Func, ML
    type_ = bool(Dtype_Func.get())
    name = get_sheet_name()
    column_list = Dtype_Column.get().split(',')
    if column_list == ['']: column_list = []
    dtype = Dtype_Input.get()
    wrong = Dtype_Wrong.get()
    if type_:  # 软转换
        if wrong != 'ignore': wrong = 'coerce'
        ML.Reasonable_Type(name, column_list, dtype, wrong)
    else:
        ML.as_Type(name, column_list, dtype, 'ignore')
    update_sheet_box()


def python_render():  # 导入绘制方法
    global Done_Func
    Dic = askopenfilename(title='打开Python脚本', filetypes=[("Python", ".py"), ("TXT", ".txt")])
    with open(Dic) as f:
        get = f.read()
        new_render(ML.Import_c(get), '自定义图')


def get_rendering_parameters():  # 获取画图的args
    global Args_Input
    return Args_Input.get('0.0', tkinter.END)


def rendering():
    global R_Dic, R_BOX
    Dic = asksaveasfilename(title='选择渲染保存地址', filetypes=[("HTML", ".html")])
    if Dic == '': return False
    try:
        if Dic[-5:] != '.html': raise Exception
    except:
        Dic += '.html'
    webbrowser.open(ML.Draw_Page(get_rendering_parameters(), Dic))
    update_render_box()


def rendering_one():
    global R_Dic, R_BOX
    Dic = asksaveasfilename(title='选择渲染保存地址', filetypes=[("HTML", ".html")])
    if Dic == '': return False
    try:
        if Dic[-5:] != '.html': raise Exception
    except:
        Dic += '.html'
    list(R_Dic.values())[R_BOX.curselection()[0]].render(Dic)
    webbrowser.open(Dic)
    update_render_box()


def make_OverLap():
    global ML, Over_Up, Over_Down
    if Over_Down != None and Over_Up != None:
        try:
            new_render(ML.Overlap(Over_Down, Over_Up), f'合成图')
        except:
            raise
        Over_Down = None
        Over_Up = None
    update_combo_box()


def update_combo_box():
    global Over_BOX, Over_Down, Over_Up
    Over_BOX.delete(0, tkinter.END)
    if Over_Down != None:
        Over_BOX.insert(tkinter.END, f'底图: {Over_Down}')
    if Over_Up != None:
        Over_BOX.insert(tkinter.END, f'顶图: {Over_Up}')


def add_basemap():
    global Over_Down
    Over_Down = list(R_Dic.keys())[R_BOX.curselection()[0]]
    update_combo_box()


def add_top_image():
    global Over_Up
    Over_Up = list(R_Dic.keys())[R_BOX.curselection()[0]]
    update_combo_box()


def del_rendering():
    global R_Dic, R_BOX, ML
    key = list(R_Dic.keys())[R_BOX.curselection()[0]]
    ML.Delete_RDic(key)
    update_render_box()


def update_render_box():
    global R_Dic, R_BOX, ML
    R_Dic = ML.retunr_RDic()
    R_BOX.delete(0, tkinter.END)
    R_BOX.insert(tkinter.END, *R_Dic.keys())


def new_render(c, name):
    global R_Dic, Draw_asWell
    if bool(Draw_asWell.get()):
        c.render(f'{PATH}\\{name}.html')
    update_render_box()


def to_Geo():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Geo(name, get_rendering_parameters()), 'Geo地图')


def to_Map():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Map(name, get_rendering_parameters()), 'Map地图')


def to_ScatterGeo():
    global ML
    name = get_sheet_name()
    new_render(ML.to_ScatterGeo(name, get_rendering_parameters()), 'Geo点地图')


def to_TreeMap():
    global ML
    name = get_sheet_name()
    new_render(ML.to_TreeMap(name, get_rendering_parameters()), '矩形树图')


def to_Tree():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Tree(name, get_rendering_parameters()), '树状图')


def to_Sankey():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Sankey(name, get_rendering_parameters()), '桑基图')


def to_Sunburst():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Sunburst(name, get_rendering_parameters()), '旭日图')


def to_ThemeRiver():
    global ML
    name = get_sheet_name()
    new_render(ML.to_ThemeRiver(name, get_rendering_parameters()), '河流图')


def to_Calendar():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Calendar(name, get_rendering_parameters()), '日历图')


def to_Gauge():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Gauge(name, get_rendering_parameters()), '仪表图')


def to_Liquid():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Liquid(name, get_rendering_parameters()), '水球图')


def to_Line3D():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Line3D(name, get_rendering_parameters()), '3D折线图')


def to_Scatter3D():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Scatter3D(name, get_rendering_parameters()), '3D散点图')


def to_Bar3d():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Bar3d(name, get_rendering_parameters()), '3D柱状图')


def to_WordCloud():
    global ML
    name = get_sheet_name()
    new_render(ML.to_WordCloud(name, get_rendering_parameters()), '词云图')


def to_Radar():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Radar(name, get_rendering_parameters()), '雷达图')


def to_Polar():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Polar(name, get_rendering_parameters()), '极坐标图')


def to_Pie():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Pie(name, get_rendering_parameters()), '饼图')


def to_Parallel():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Parallel(name, get_rendering_parameters()), '多轴图')


def to_XY_Graph():
    global ML
    name = get_sheet_name()
    new_render(ML.to_XY_Graph(name, get_rendering_parameters()), '关系图')


def to_Graph():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Graph(name, get_rendering_parameters()), '关系图')


def to_Funnel():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Funnel(name, get_rendering_parameters()), '漏斗图')


def to_HeatMap():
    global ML
    name = get_sheet_name()
    new_render(ML.to_HeatMap(name, get_rendering_parameters()), '热力图')


def to_Boxpolt():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Boxpolt(name, get_rendering_parameters()), '箱形图')


def to_Pictorialbar():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Pictorialbar(name, get_rendering_parameters()), '象形柱状图')


def to_Scatter():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Scatter(name, get_rendering_parameters()), '散点图')


def to_Line():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Line(name, get_rendering_parameters()), '折线图')


def to_Bar():
    global ML
    name = get_sheet_name()
    new_render(ML.to_Bar(name, get_rendering_parameters()), '柱状图')


def show_dictionary():
    tkinter.messagebox.showinfo('帮助字典', clean_help)


def open_python():
    global Done_Func
    Dic = askopenfilename(title='打开Python脚本', filetypes=[("Python", ".py"), ("TXT", ".txt")])
    with open(Dic) as f:
        get = f.read()
        Done_Func.delete('0.0', tkinter.END)
        Done_Func.insert('0.0', get)


def reset():
    global Done_Func, clean_default_script
    Done_Func.delete('0.0', tkinter.END)
    Done_Func.insert('0.0', clean_default_script)


def view_cleaning_script():
    global ML, Clean_List, Done_CleanBox, Done_Func
    name = Clean_List[Done_CleanBox.curselection()[0]]
    get = ML.Return_CleanExp(name)
    Done_Func.delete('0.0', tkinter.END)
    Done_Func.insert('0.0', get)


def empty_cleaning_script():
    global ML
    ML.Tra_Clean()
    update_sheet_box()


def execute_cleaning_script():
    global ML
    name = get_sheet_name()
    Data = ML.Done_CleanFunc(name)
    title = f'CoTan数据处理 表格:{name}.数据清洗'
    vitables(Data, title)
    update_sheet_box()


def del_cleaning_script():
    global ML, Clean_List, Done_CleanBox
    name = Clean_List[Done_CleanBox.curselection()[0]]
    ML.Delete_CleanFunc(name)
    update_cleaning_script_box()


def update_cleaning_script_box():
    global ML, Done_CleanBox, Clean_List
    Clean_List = ML.Return_CleanFunc()
    Done_CleanBox.delete(0, tkinter.END)
    Done_CleanBox.insert(tkinter.END, *Clean_List)


def add_cleaning_script():
    global ML, Done_CleanBox, Done_Func
    Exp = Done_Func.get('0.0', tkinter.END)
    print(Exp)
    ML.Add_CleanFunc(Exp)
    update_cleaning_script_box()


def clear_NaN_by_row():
    global Drop_Column
    name = get_sheet_name()
    Data = ML.Dropna(name, True)
    title = f'CoTan数据处理 表格:{name}.NaN'
    vitables(Data, title)
    update_sheet_box()


def is_NaN():
    global Bool_E
    name = get_sheet_name()
    Data = ML.is_Na(name)
    title = f'CoTan数据处理 表格:{name}.NaN'
    vitables(Data, title)
    update_sheet_box()


def to_bool():
    global Bool_E
    Bool_Exp = Bool_E.get()
    name = get_sheet_name()
    Data = ML.Done_Bool(name, Bool_Exp, True)
    print(Data)
    title = f'CoTan数据处理 表格:{name} 布尔化'
    vitables(Data, title)
    update_sheet_box()


def del_data():
    global Slice_new, Column_clist, Row_clist
    Column = Column_clist[0].get().replace(' ', '').split(',')
    Row = Row_clist[0].get().replace(' ', '').split(',')
    print(Column)
    new = bool(Slice_new.get())
    name = get_sheet_name()
    try:
        Data = ML.Delete(name, Column, Row, new)
    except:
        Data = 'None 你的操作不被允许'
    title = f'CoTan数据处理 表格:{name}'
    vitables(Data, title)
    update_sheet_box()


def __split_slice(n, t):
    a = []
    for i in n:
        b = i.get().replace(' ', '')
        if b == '':
            a.append(None)
        else:
            try:
                a.append(t(b))
            except:
                a.append(None)
    if a[0] != None and a[1] == None:
        a[1] = a[0] + 1
        a[2] = None
    return a


def slice_data():
    global Slice_new, Column_Type, Row_Type, Column_clist, Row_clist
    CT = Column_Type.get()
    U = True
    if CT == 0:  # 输入的列号
        Column = slice(*__split_slice(Column_clist, int))
    elif CT == 1:
        U = False
        Column = slice(*__split_slice(Column_clist, str))
    else:
        get = Column_clist[0].get().replace(' ', '').split(',')
        Column = []
        for i in get:
            try:
                Column.append(int(i))
            except:
                pass

    RT = Row_Type.get()
    if RT == 0:  # 输入的列号
        Row = slice(*__split_slice(Row_clist, int))
    elif RT == 1:
        Row = slice(*__split_slice(Row_clist, str))
    else:
        get = Row_clist[0].get().replace(' ', '').split(',')
        Row = []
        for i in get:
            try:
                Row.append(int(i))
            except:
                pass
    new = bool(Slice_new.get())
    name = get_sheet_name()
    try:
        Data = ML.get_Clice(name, Column, Row, U, new)
    except:
        Data = 'None 你的操作不被允许'
    title = f'CoTan数据处理 表格:{name}'
    vitables(Data, title)
    update_sheet_box()


def sample_data():
    global ML, Ascending_New
    name = get_sheet_name()
    new = bool(Ascending_New.get())
    Data = ML.Sample(name, new)
    title = f'CoTan数据处理 打乱表格:{name}'
    vitables(Data, title)
    update_sheet_box()


def stored_value():
    global ML, Stored_List, Ascending_New
    name = get_sheet_name()
    new = bool(Ascending_New.get())
    Data = ML.Stored_Valuse(name, Stored_List, new)
    title = f'CoTan数据处理 表格:{name}.Stored'
    vitables(Data, title)
    update_sheet_box()


def del_baseline():
    global Stored_List, Stored_BOX, Ascending_Type
    del Stored_List[Stored_BOX.curselection()[0]]
    update_sort_box()


def add_baseline():  # 按基准列排行
    global ML, Stored_List, Sort_By, Ascending_Type
    try:
        a = not bool(Ascending_Type.get())
        value = int(Sort_By.get())
        Stored_List.append((value, a))
    except:
        pass
    update_sort_box()


def update_sort_box():
    global Stored_List, Stored_BOX
    re = []
    d = {True: '正序', False: '倒叙'}
    for i in Stored_List:
        re.append(f"列号:{i[0]}, 排序方式{d[i[1]]}")
    Stored_BOX.delete(0, tkinter.END)
    Stored_BOX.insert(tkinter.END, *re)


def sort_by_column():  # 行
    global ML
    name = get_sheet_name()
    a = not bool(Ascending_Type.get())
    new = bool(Ascending_New.get())
    Data = ML.Sorted(name, False, new, a)
    title = f'CoTan数据处理 表格:{name}.Stored by Column'
    vitables(Data, title)
    update_sheet_box()


def sort_by_tow():  # 行
    global ML
    name = get_sheet_name()
    new = bool(Ascending_New.get())
    a = not bool(Ascending_Type.get())
    Data = ML.Sorted(name, True, new, a)
    title = f'CoTan数据处理 表格:{name}.Stored by Row'
    vitables(Data, title)
    update_sheet_box()


def transpose():
    global ML
    name = get_sheet_name()
    new = bool(Ascending_New.get())
    Data = ML.T(name, new)
    title = f'CoTan数据处理 表格:{name}.T'
    vitables(Data, title)
    update_sheet_box()


def show_report():
    global PATH, top
    if not tkinter.messagebox.askokcancel('提示', f'是否统计数据，大量的数据需要耗费一定的时间(确定后，系统会在后台统计)'): return False
    Dic = f'{PATH}/$Show_Des_Sheet.html'
    try:
        name = get_sheet_name()
        if name == None: raise Exception
        ML.to_Report(name, Dic)
        webbrowser.open(Dic)
    except:
        pass


def show_describe():
    global ML, Des_Bool
    Des = bool(Des_Bool.get())
    name = get_sheet_name()
    title = f'CoTan数据处理 表格:{name}_describe'
    Data = str(ML.Describe(name, Des))
    vitables(Data, title)
    update_sheet_box()


def show_sheet():
    global ML, top
    name = get_sheet_name()
    title = f'CoTan数据处理 表格:{name}'
    Data = str(ML.get_Sheet(name))
    vitables(Data, title)


def vitables(data, name):
    global bg, ft1
    new_top = tkinter.Toplevel(bg=bg)
    new_top.title(name)
    new_top.geometry('+10+10')  # 设置所在位置
    text = ScrolledText(new_top, font=ft1, height=50)
    text.pack(fill=tkinter.BOTH)
    text.insert('0.0', data)
    text.config(state=tkinter.DISABLED)
    new_top.resizable(width=False, height=False)


def get_column():  # 列名(横行竖列，列名是上面的)
    global ML
    name = get_sheet_name()
    update_index_box(ML.get_Column(name))


def get_row():  # 行名(横行竖列，行名左)
    global ML
    name = get_sheet_name()
    update_index_box(ML.get_Index(name))


def update_index_box(index):
    global top, Index_BOX
    Index_BOX.delete(0, tkinter.END)
    Index_BOX.insert(tkinter.END, *index)


def show_one_sheet_html():
    global PATH, to_HTML_Type
    Dic = f'{PATH}/$Show_Sheet.html'
    try:
        name = get_sheet_name()
        if name == None: raise Exception
        ML.to_Html_One(name, Dic)
        webbrowser.open(Dic)
    except:
        # pass
        raise


def show_sheet_html():
    global PATH, to_HTML_Type
    Dic = f'{PATH}/$Show_Sheet.html'
    try:
        name = get_sheet_name()
        if name == None: raise Exception
        ML.to_Html(name, Dic, to_HTML_Type.get())
        webbrowser.open(Dic)
    except:
        pass


def to_csv():
    global top, Seq_Input, Code_Input, str_must, Index_must
    Dic = asksaveasfilename(title='选择保存的CSV', filetypes=[("CSV", ".csv")])
    Seq = Seq_Input.get()
    name = get_sheet_name()
    ML.to_CSV(name, Dic, Seq)
    update_sheet_box()


def add_csv():
    global top, Seq_Input, Code_Input, str_must, Index_must, name_Input
    Dic = askopenfilename(title='选择载入的CSV', filetypes=[("CSV", ".csv")])
    if Dic == '': return False
    Seq = Seq_Input.get()
    Codeing = Code_Input.get()
    str_ = bool(str_must.get())
    Index = bool(Index_must.get())
    name = name_Input.get().replace(' ', '')
    if name == '':
        name = os.path.splitext(os.path.split(Dic)[1])[0]
        print(name)
    if Codeing == '':
        with open(Dic, 'rb') as f:
            Codeing = chardet.detect(f.read())['encoding']
    if Seq == '': Seq = ','
    ML.Add_CSV(Dic, name, Seq, Codeing, str_, Index)
    update_sheet_box()


def add_from_python():
    global top, Seq_Input, Code_Input, str_must, Index_must
    Dic = askopenfilename(title='选择载入的py', filetypes=[("Python", ".py"), ("Txt", ".txt")])
    name = name_Input.get().replace(' ', '')
    if name == '':
        name = os.path.splitext(os.path.split(Dic)[1])[0]
    with open(Dic, 'r') as f:
        ML.Add_Python(f.read(), name)
    update_sheet_box()


def get_sheet_name():  # 获得名字统一接口
    global Form_List
    try:
        return Form_List[Form_BOX.curselection()[0]]
    except:
        try:
            return Form_List[0]
        except:
            return None


def update_sheet_box():
    global top, Form_BOX, Form_List
    Form_List = ML.get_FormList()
    Form_BOX.delete(0, tkinter.END)
    Form_BOX.insert(tkinter.END, *Form_List)

machine_learning()