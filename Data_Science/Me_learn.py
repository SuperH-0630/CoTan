import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.messagebox
from Data_Science import Learn
import webbrowser
import os
from tkinter.scrolledtext import ScrolledText
import chardet

# 数据清洗
clean_default_script = """#输入你的数据清洗执行代码

Done_Row=[] #输入操作的行号
Done_Column=[] #输入操作的列号
axis=True #True-操作行，False-操作列
name='' #方法代号

def check(data, row, column, get, R, C): #检查方法
    return True

def done(data, row, column, get, R, C): #应用修正方法
    return DEL
"""

clean_help = """
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
"""

drawing_parameters = """
输入python变量赋值代码:渲染设置
title #设置标题:str
vice_title #设置副标题:str

show_Legend #是否显示图例:bool

show_Visual_mapping #是否使用视觉映射:bool
is_color_Visual_mapping #是否为颜色视觉映射:bool[否则为大小视觉映射]
min_Visual_mapping #映射的最小值
max_Visual_mapping #映射的最大值

......(我太懒了, 设置太多不想写了)
"""


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
    global SCREEN, machine_controller, sheet_list, PATH, bg_color, FONT1, stored_list, clean_list, render_dict
    global top_image, base_image, learn_dict
    render_dict = {}  # 保存了画图的List
    learn_dict = {}  # 保存数据处理
    PATH = os.getcwd()
    sheet_list = []
    machine_controller = Learn.MachineLearner()
    SCREEN = tkinter.Tk()
    bg_color = "#FFFAFA"  # 主颜色
    buttom_bg_color = "#FFFAFA"  # 按钮颜色
    word_color = "#000000"  # 文字颜色
    SCREEN["bg"] = bg_color
    FONT = ("黑体", 11)  # 设置字体
    FONT1 = ("黑体", 13)
    SCREEN.title("CoTan数据处理")
    SCREEN.resizable(width=False, height=False)
    SCREEN.geometry("+10+10")  # 设置所在位置
    gui_width = 13  # 标准宽度
    gui_height = 2
    row = 0
    column = 0
    stored_list = []
    clean_list = []
    # 层叠多图
    base_image = None
    top_image = None

    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="导入CSV",
        command=add_csv,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="导入Py",
        command=add_from_python,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="导出CSV",
        command=to_csv,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    global sheet_name
    row += 1
    tkinter.Label(
        SCREEN,
        text="表格名称:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    sheet_name = tkinter.Entry(SCREEN, width=gui_width)
    sheet_name.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="删除表格",
        command=del_form,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看表格",
        command=show_sheet_html,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看单一表格",
        command=show_one_sheet_html,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    global sheet_box, index_box, column_box, to_html_type, sep, encoding, str_must, index_must
    row += 1
    to_html_type = tkinter.IntVar()  # 正，负，0
    lable = ["选项卡型", "可移动型", "自适应型"]  # 复选框
    for i in range(3):
        tkinter.Radiobutton(
            SCREEN,
            bg=bg_color,
            fg=word_color,
            activebackground=bg_color,
            activeforeground=word_color,
            selectcolor=bg_color,
            text=lable[i],
            variable=to_html_type,
            value=i,
        ).grid(column=column + i, row=row, sticky=tkinter.W)

    str_must = tkinter.IntVar()
    index_must = tkinter.IntVar()
    row += 1
    tkinter.Label(
        SCREEN,
        text="编码方式:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    encoding = tkinter.Entry(SCREEN, width=gui_width)
    encoding.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
    buttom = tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text="字符串类型",
        variable=str_must,
    )
    buttom.grid(column=column + 2, row=row, sticky=tkinter.W)

    row += 1
    tkinter.Label(
        SCREEN,
        text="CSV分隔符:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    sep = tkinter.Entry(SCREEN, width=gui_width)
    sep.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text="重置列名",
        variable=index_must,
    ).grid(column=column + 2, row=row, sticky=tkinter.W)

    row += 1
    sheet_box = tkinter.Listbox(
        SCREEN, width=gui_width * 3, height=gui_height * 5
    )  # 显示符号
    sheet_box.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=5,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 5
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看行名",
        command=get_row,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看列名",
        command=get_column,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="显示表格",
        command=show_sheet,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    global max_row, max_column
    row += 1
    tkinter.Label(
        SCREEN,
        text="最大显示行数:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    max_row = tkinter.Entry(SCREEN, width=gui_width * 2)
    max_row.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

    row += 1
    tkinter.Label(
        SCREEN,
        text="最大显示列数:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    max_column = tkinter.Entry(SCREEN, width=gui_width * 2)
    max_column.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
    )

    # Row与Column Row是横行，tkinter布局中Row变大，表示所在行数变大，向下移动如：
    # 1，2，3，4，5，6
    # 7，8，9，a，b，c
    # 其中数字1-6是第一行，1-c是第二行，第二行在第一行下面，row变大向下移动（Row是横向行而不是横向移动） to 搞不清楚横行竖列的人

    row += 1
    index_box = tkinter.Listbox(
        SCREEN, width=gui_width * 3, height=gui_height * 10
    )  # 显示符号
    index_box.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=10,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )

    global des_bool
    row += 10
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看数据分析",
        command=show_report,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="简单数据统计",
        command=show_describe,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    des_bool = tkinter.IntVar()  # 是否启用
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text="生成统计表格",
        variable=des_bool,
    ).grid(column=column + 2, row=row, sticky=tkinter.W)

    column += 3
    tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
        column=column, row=row
    )  # 设置说明
    column += 1
    row = 0

    tkinter.Label(
        SCREEN,
        text="【数据清洗】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(
        column=column,
        columnspan=3,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )  # 设置说明

    global slice_new, column_type, row_type, column_clist, row_clist
    column_clist = []
    row_clist = []
    label = ["启始(列号):", "终止(列):", "间隔(列):"]
    for i in range(3):
        row += 1
        tkinter.Label(
            SCREEN,
            text=label[i],
            bg=bg_color,
            fg=word_color,
            font=FONT,
            width=gui_width,
            height=gui_height,
        ).grid(
            column=column, row=row
        )  # 设置说明
        column_clist.append(tkinter.Entry(SCREEN, width=gui_width * 2))
        column_clist[-1].grid(
            column=column + 1, row=row, columnspan=2, sticky=tkinter.W + tkinter.E
        )

    label = ["启始(行号):", "终止(行):", "间隔(行):"]
    for i in range(3):
        row += 1
        tkinter.Label(
            SCREEN,
            text=label[i],
            bg=bg_color,
            fg=word_color,
            font=FONT,
            width=gui_width,
            height=gui_height,
        ).grid(
            column=column, row=row
        )  # 设置说明
        row_clist.append(tkinter.Entry(SCREEN, width=gui_width * 2))
        row_clist[-1].grid(
            column=column + 1, row=row, columnspan=2, sticky=tkinter.W + tkinter.E
        )

    row += 1
    column_type = tkinter.IntVar()
    lable = ["根据列号", "根据列名", "输入列号"]  # 复选框
    for i in range(3):
        tkinter.Radiobutton(
            SCREEN,
            bg=bg_color,
            fg=word_color,
            activebackground=bg_color,
            activeforeground=word_color,
            selectcolor=bg_color,
            text=lable[i],
            variable=column_type,
            value=i,
        ).grid(column=column + i, row=row, sticky=tkinter.W)

    row += 1
    row_type = tkinter.IntVar()
    lable = ["根据行号", "根据行名", "输入行号"]  # 复选框
    for i in range(3):
        tkinter.Radiobutton(
            SCREEN,
            bg=bg_color,
            fg=word_color,
            activebackground=bg_color,
            activeforeground=word_color,
            selectcolor=bg_color,
            text=lable[i],
            variable=row_type,
            value=i,
        ).grid(column=column + i, row=row, sticky=tkinter.W)

    row += 1
    slice_new = tkinter.IntVar()
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="切片选定",
        command=slice_data,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="删除选定",
        command=del_data,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text="生成新表格",
        variable=slice_new,
    ).grid(column=column + 2, row=row, sticky=tkinter.W)

    global bool_exp, drop_column
    row += 1
    tkinter.Label(
        SCREEN,
        text="布尔逻辑:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )  # 设置说明
    bool_exp = tkinter.Entry(SCREEN, width=gui_width * 2)
    bool_exp.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.W + tkinter.E
    )

    row += 1
    tkinter.Label(
        SCREEN,
        text="操作的列号:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )  # 设置说明
    drop_column = tkinter.Entry(SCREEN, width=gui_width * 2)
    drop_column.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.W + tkinter.E
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成布尔表格",
        command=to_bool,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看空值",
        command=is_nan,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="清洗空值(按行)",
        command=clear_nan_row,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="添加执行方法",
        command=add_cleaning_script,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="删除执行方法",
        command=del_cleaning_script,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="数据特征提取",
        command=feature_extraction,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    global clean_func_box, clean_code
    row += 1
    clean_func_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 2)
    clean_func_box.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=2,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 2
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看词典",
        command=show_dictionary,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="恢复显示",
        command=reset,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="执行数据清洗",
        command=execute_cleaning_script,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    clean_code = tkinter.Text(SCREEN, width=gui_width * 3, height=gui_height * 7)
    clean_code.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=7,
        sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
    )
    clean_code.insert("0.0", clean_default_script)

    row += 7
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="清空执行方法",
        command=empty_cleaning_script,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看执行方法",
        command=view_cleaning_script,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="导入执行方法",
        command=open_python,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    column += 3
    tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
        column=column, row=row
    )  # 设置说明
    column += 1
    row = 0

    tkinter.Label(
        SCREEN,
        text="【数据可视化】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(
        column=column,
        columnspan=3,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )  # 设置说明

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成柱状图",
        command=to_bar,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成3D柱状图",
        command=to_bar3d,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成折线图",
        command=to_line,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成3D折线图",
        command=to_line3d,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成象形柱状图",
        command=to_pictorialbar,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        columnspan=2,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成散点图",
        command=to_scatter,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成3D散点图",
        command=to_scatter3d,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成箱形图",
        command=to_boxpolt,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成漏斗图",
        command=to_funnel,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成热力图",
        command=to_heat_map,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成饼图",
        command=to_pie,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成多轴图",
        command=to_parallel,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成极坐标图",
        command=to_polar,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成雷达图",
        command=to_radar,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成词云",
        command=to_word_cloud,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成关系图",
        command=to_format_graph,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成XY关系图",
        command=to_graph,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成水球图",
        command=to_liquid,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        columnspan=2,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成仪表图",
        command=to_gauge,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成日历图",
        command=to_calendar,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成河流图",
        command=to_theme_river,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成旭日图",
        command=to_sunburst,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成桑基图",
        command=to_sankey,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成树状图",
        command=to_tree,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成矩形树图",
        command=to_treemap,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成Map地图",
        command=to_map,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成Geo点地图",
        command=to_scattergeo,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成Geo地图",
        command=to_geo,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="选择底图",
        command=add_basemap,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="选择顶图",
        command=add_top_image,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="生成层叠图",
        command=make_overlap,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    global render_box, rendering_parameters, overlap_box
    overlap_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 2)
    overlap_box.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=2,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="渲染HTML",
        command=rendering,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="单独渲染HTML",
        command=rendering_one,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="删除渲染",
        command=del_rendering,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    render_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height)
    render_box.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=2,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 2
    global draw_as_well
    draw_as_well = tkinter.IntVar()
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="清空渲染",
        command=clear_rendering,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="导入渲染",
        command=python_render,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text="马上渲染",
        variable=draw_as_well,
    ).grid(column=column + 2, row=row, sticky=tkinter.W)
    row += 1
    rendering_parameters = tkinter.Text(
        SCREEN, width=gui_width * 3, height=gui_height * 7
    )
    rendering_parameters.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=7,
        sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
    )

    row += 7
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看词典",
        command=show_dictionary,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="恢复显示",
        command=show_tips,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        columnspan=2,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    column += 3
    tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
        column=column, row=row
    )  # 设置说明
    column += 1
    row = 0

    tkinter.Label(
        SCREEN,
        text="【行名与列名】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(
        column=column,
        columnspan=3,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )  # 设置说明

    global replace_dict, replace_index, replace_iloc, date_input, replace_type
    row += 1
    replace_index = tkinter.IntVar()
    lable = ["(列数据)调整行名", "(行数据)调整列名"]  # 复选框
    for i in range(2):
        tkinter.Radiobutton(
            SCREEN,
            bg=bg_color,
            fg=word_color,
            activebackground=bg_color,
            activeforeground=word_color,
            selectcolor=bg_color,
            text=lable[i],
            variable=replace_index,
            value=i,
        ).grid(column=column + i, row=row, sticky=tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="植入行(列)号",
        command=num_with_name,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

    row += 1
    replace_type = []
    lable = ["保留原值", "保留新值"]  # 复选框
    for i in range(2):
        replace_type.append(tkinter.IntVar())
        tkinter.Checkbutton(
            SCREEN,
            bg=bg_color,
            fg=word_color,
            activebackground=bg_color,
            activeforeground=word_color,
            selectcolor=bg_color,
            text=lable[i],
            variable=replace_type[-1],
        ).grid(column=column + i, row=row, sticky=tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="统一行(列)号",
        command=num_to_name,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

    row += 1
    tkinter.Label(
        SCREEN,
        text="替换字典:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    replace_dict = tkinter.Entry(SCREEN, width=gui_width * 2)
    replace_dict.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
    )

    row += 1
    tkinter.Label(
        SCREEN,
        text="替换列(行):",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    replace_iloc = tkinter.Entry(SCREEN, width=gui_width * 2)
    replace_iloc.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="执行替换已有列(行)操作",
        command=change_index,
        font=FONT,
        width=gui_width * 2,
        height=gui_height,
    ).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="执行替换操作",
        command=replace_index,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

    label = ["起点", "终点", "间隔"]
    date_input = []
    for i in range(3):
        row += 1
        tkinter.Label(
            SCREEN,
            text="时间序列" + label[i],
            bg=bg_color,
            fg=word_color,
            font=FONT,
            width=gui_width,
            height=gui_height,
        ).grid(
            column=column, row=row
        )  # 设置说明
        date_input.append(tkinter.Entry(SCREEN, width=gui_width * 2))
        date_input[-1].grid(
            column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
        )

    global date_type
    row += 1
    date_type = tkinter.IntVar()
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="刷入Date序列",
        command=date_index,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="刷入Time序列",
        command=time_index,
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
        text="使用间隔",
        variable=date_type,
    ).grid(column=column + 2, row=row, sticky=tkinter.W)

    global dtype_column, dtype_input, dtype_wrong, dtype_func
    row += 1
    tkinter.Label(
        SCREEN,
        text="【数据类型管理】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(
        column=column,
        columnspan=3,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )  # 设置说明

    row += 1
    tkinter.Label(
        SCREEN,
        text="修改(列号):",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    dtype_column = tkinter.Entry(SCREEN, width=gui_width * 2)
    dtype_column.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
    )

    row += 1
    tkinter.Label(
        SCREEN,
        text="数据类型:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    dtype_input = tkinter.Entry(SCREEN, width=gui_width * 2)
    dtype_input.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
    )

    row += 1
    tkinter.Label(
        SCREEN,
        text="错误值:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    dtype_wrong = tkinter.Entry(SCREEN, width=gui_width * 2)
    dtype_wrong.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="执行转换",
        command=set_dtype,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    dtype_func = tkinter.IntVar()  # 正，负，0
    lable = ["硬转换", "软转换"]  # 复选框
    for i in range(2):
        tkinter.Radiobutton(
            SCREEN,
            bg=bg_color,
            fg=word_color,
            activebackground=bg_color,
            activeforeground=word_color,
            selectcolor=bg_color,
            text=lable[i],
            variable=dtype_func,
            value=i,
        ).grid(column=column + 1 + i, row=row, sticky=tkinter.W)

    row += 1
    tkinter.Label(
        SCREEN,
        text="【排序操作】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(
        column=column, columnspan=3, row=row
    )  # 设置说明

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text=".T",
        command=transpose,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="按行名排序",
        command=sort_by_tow,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="按列名排序",
        command=sort_by_column,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    global sort_by, ascending_type, ascending_new, stored_box
    row += 1
    tkinter.Label(
        SCREEN,
        text="基准列(列号):",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column, row=row
    )  # 设置说明
    sort_by = tkinter.Entry(SCREEN, width=gui_width + 2)
    sort_by.grid(column=column + 1, row=row, sticky=tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="按数据排序",
        command=stored_value,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    ascending_type = tkinter.IntVar()
    ascending_new = tkinter.IntVar()
    lable = ["正序排列", "倒序排列"]  # 复选框
    for i in range(2):
        tkinter.Radiobutton(
            SCREEN,
            bg=bg_color,
            fg=word_color,
            activebackground=bg_color,
            activeforeground=word_color,
            selectcolor=bg_color,
            text=lable[i],
            variable=ascending_type,
            value=i,
        ).grid(column=column + i, row=row, sticky=tkinter.W)
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text="生成新表格",
        variable=ascending_new,
    ).grid(column=column + 2, row=row, sticky=tkinter.W)

    row += 1
    stored_box = tkinter.Listbox(
        SCREEN, width=gui_width * 3, height=gui_height * 4
    )  # 显示符号
    stored_box.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=5,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 5
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="添加基准",
        command=add_baseline,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="删除基准",
        command=del_baseline,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="打乱表格",
        command=sample_data,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    column += 3
    tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
        column=column, row=row
    )  # 设置说明
    column += 1
    row = 0

    tkinter.Label(
        SCREEN,
        text="【机器学习】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(
        column=column,
        columnspan=3,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )  # 设置说明

    global learner_box, chose_learner
    row += 1
    chose_learner = tkinter.StringVar()
    put = tkinter.Entry(SCREEN, width=gui_width * 2, textvariable=chose_learner)
    put.grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
    put["state"] = "readonly"
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="选用学习器",
        command=set_learner,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

    global data_split
    row += 1
    tkinter.Label(
        SCREEN,
        text="测试数据分割:",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row)
    data_split = tkinter.Entry(SCREEN, width=gui_width * 2)
    data_split.grid(
        column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
    )

    row += 1
    learner_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 5)
    learner_box.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=5,
        sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 5
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="导入学习器",
        command=rendering,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="查看数据",
        command=visual_learner,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="删除学习器",
        command=del_learner,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="训练机器",
        command=fit_learner,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="测试机器",
        command=test_learner,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="数据预测",
        command=predict_learner,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Label(
        SCREEN,
        text="【学习器选择和配置】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(
        column=column,
        columnspan=3,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )  # 设置说明

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="线性回归",
        command=add_generalized_linear,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="岭回归",
        command=add_ridge,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="Lasso",
        command=add_lasso,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="逻辑回归",
        command=add_logistic_regression,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="决策树",
        command=show_sorry,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="SVM",
        command=show_sorry,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    row += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="朴素贝叶斯",
        command=show_sorry,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="K邻近分类",
        command=add_knn_regression,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 1,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )
    tkinter.Button(
        SCREEN,
        bg=buttom_bg_color,
        fg=word_color,
        text="K邻近预测",
        command=add_knn_class,
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(
        column=column + 2,
        row=row,
        sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
    )

    global learner_parameters
    row += 1
    learner_parameters = tkinter.Text(
        SCREEN, width=gui_width * 3, height=gui_height * 11
    )
    learner_parameters.grid(
        column=column,
        row=row,
        columnspan=3,
        rowspan=11,
        sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
    )

    SCREEN.mainloop()


def show_tips():
    tkinter.messagebox.showinfo("使用提示", drawing_parameters)


def show_sorry():
    tkinter.messagebox.showinfo("非常抱歉", "高级别的机器学习请到机器学习板块深入研究...")


def clear_rendering():
    machine_controller.clean_render()
    update_render_box()


def del_form():
    name = get_sheet_name()
    machine_controller.del_sheet(name)
    update_sheet_box()


def del_learner():
    learner = get_learner_name(True)
    set_learne = get_learner_name(False)  # 获取学习器Learner
    if set_learne != learner:
        machine_controller.del_leaner(learner)
    update_leaner_box()


def visual_learner():
    learner = get_learner_name(True)
    new = tkinter.messagebox.askokcancel("提示", f"是否将数据生成表格。\n(可绘制成散点图对比数据)")
    data = machine_controller.visual_learner(learner, new)
    title = f"CoTan数据处理 查看数据:{learner}"
    vitables(f"对象:{learner}\n\n{data[0]}\n\n\n{data[1]}", title)
    update_sheet_box()


def get_learner_config():
    global learner_parameters
    return learner_parameters.get("0.0", tkinter.END)


def test_learner():
    global machine_controller
    print("F")
    name = get_sheet_name()  # 表格数据
    learner = get_learner_name()
    try:
        split = float(data_split.get())
        if split < 0 or 1 < split:
            raise Exception
    except BaseException:
        split = 0.3
    socore = machine_controller.training_machine(
        name, learner, Score_Only=True, split=split
    )[1]
    tkinter.messagebox.showinfo("测试完成", f"针对测试数据评分结果为:{socore}")


def predict_learner():
    name = get_sheet_name()  # 表格数据
    learner = get_learner_name()
    data = machine_controller.predict(name, learner)
    title = f"CoTan数据处理 表格:{name} 学习器:{learner}"
    vitables(data, title)
    update_sheet_box()


def fit_learner():
    name = get_sheet_name()  # 表格数据
    learner = get_learner_name()
    try:
        split = float(data_split.get())
        if split < 0 or 1 < split:
            raise Exception
    except BaseException:
        split = 0.3
    socore = machine_controller.training_machine(
        name, learner, parameters=get_learner_config(), split=split
    )
    tkinter.messagebox.showinfo(
        "训练完成",
        f"针对训练数据({(1 - split) * 100}%)评分结果为:{socore[0]}\n"
        f"针对测试数据评分({split * 100}%)结果为:{socore[1]}",
    )


def set_learner():
    global chose_learner
    chose_learner.set(get_learner_name(True))


def get_learner_name(learner_type=False):
    global learn_dict, learner_box, chose_learner
    if learner_type:
        try:
            return list(learn_dict.keys())[learner_box.curselection()[0]]
        except BaseException:
            # raise
            try:
                return list(learn_dict.keys)[0]
            except BaseException:
                return None
    else:
        try:
            return chose_learner.get()
        except BaseException:
            return None


def add_knn_class():
    add_learner_core("Knn_class")


def add_logistic_regression():
    add_learner_core("LogisticRegression")


def add_lasso():
    add_learner_core("Lasso")


def add_knn_regression():
    add_learner_core("Knn")


def add_ridge():
    add_learner_core("Ridge")


def add_generalized_linear():
    add_learner_core("Line")


def add_learner_core(learner_type):  # 添加Lenear的核心
    machine_controller.add_learner(learner_type, parameters=get_learner_config())
    update_leaner_box()


def update_leaner_box():
    global learn_dict, learner_box
    learn_dict = machine_controller.return_learner()
    learner_box.delete(0, tkinter.END)
    learner_box.insert(tkinter.END, *learn_dict.keys())


def feature_extraction():
    name = get_sheet_name()
    machine_controller.decision_tree_classifier(name)
    update_sheet_box()


def replace_index():
    global replace_dict, replace_index, machine_controller
    name = get_sheet_name()
    the_replace_dict = eval(replace_dict.get())
    is_column = bool(replace_index.get())  # 操作行-False，操作列-True
    save = bool(replace_type[0].get())
    machine_controller.replace_index(name, is_column, the_replace_dict, save)
    update_sheet_box()


def change_index():
    global replace_index, replace_iloc, replace_type, machine_controller
    name = get_sheet_name()  # 名字
    is_column = bool(replace_index.get())  # 操作行名-False，操作列名-True
    iloc = int(replace_iloc.get())  # 替换的列号(行号)
    save = bool(replace_type[0].get())
    drop = not bool(replace_type[1].get())

    machine_controller.change_index(name, is_column, iloc, save, drop)
    update_sheet_box()


def num_to_name():
    global replace_index, replace_iloc, replace_type, machine_controller
    name = get_sheet_name()  # 名字
    is_column = bool(replace_index.get())  # 操作行名-False，操作列名-True
    save = bool(replace_type[0].get())

    machine_controller.number_naming(name, is_column, save)
    update_sheet_box()


def num_with_name():
    global replace_index, replace_type, machine_controller
    name = get_sheet_name()  # 名字
    is_column = bool(replace_index.get())  # 操作行名-False，操作列名-True
    save = bool(replace_type[0].get())

    machine_controller.name_with_number(name, is_column, save)
    update_sheet_box()


def datetime_index(is_date=True):
    global replace_index, replace_type, machine_controller, date_input, date_type
    name = get_sheet_name()  # 名字
    is_column = bool(replace_index.get())  # 操作行名-False，操作列名-True
    save = bool(replace_type[0].get())

    k = ["start", "end", "freq"]
    init = {}
    for i in range(len(date_input)):
        data = date_input[i].get()
        if data == "":
            continue
        init[k[i]] = data
    if len(init) == 3:
        if bool(date_type.get()):  # 使用间隔
            del init["end"]
        else:
            del init["freq"]
    if is_date:
        machine_controller.date_index(name, is_column, save, **init)
    else:
        machine_controller.time_naming(name, is_column, save, **init)
    update_sheet_box()


def date_index():
    datetime_index(True)


def time_index():
    datetime_index(False)


def set_dtype():
    global dtype_column, dtype_input, dtype_wrong, dtype_func, machine_controller
    type_ = bool(dtype_func.get())
    name = get_sheet_name()
    column_list = dtype_column.get().split(",")
    if column_list == [""]:
        column_list = []
    dtype = dtype_input.get()
    wrong = dtype_wrong.get()
    if type_:  # 软转换
        if wrong != "ignore":
            wrong = "coerce"
        machine_controller.set_dtype(name, column_list, dtype, wrong)
    else:
        machine_controller.as_dtype(name, column_list, dtype, "ignore")
    update_sheet_box()


def python_render():  # 导入绘制方法
    global clean_code
    file_dir = askopenfilename(
        title="打开Python脚本", filetypes=[("Python", ".py"), ("TXT", ".txt")]
    )
    with open(file_dir) as f:
        get = f.read()
        new_render(machine_controller.custom_graph(get), "自定义图")


def get_rendering_parameters():  # 获取画图的args
    global rendering_parameters
    return rendering_parameters.get("0.0", tkinter.END)


def rendering():
    global render_dict, render_box
    render_dir = asksaveasfilename(title="选择渲染保存地址", filetypes=[("HTML", ".html")])
    if render_dir == "":
        return False
    try:
        if render_dir[-5:] != ".html":
            raise Exception
    except BaseException:
        render_dir += ".html"
    webbrowser.open(
        machine_controller.render_all(get_rendering_parameters(), render_dir)
    )
    update_render_box()


def rendering_one():
    global render_dict, render_box
    render_dir = asksaveasfilename(title="选择渲染保存地址", filetypes=[("HTML", ".html")])
    if render_dir == "":
        return False
    try:
        if render_dir[-5:] != ".html":
            raise Exception
    except BaseException:
        render_dir += ".html"
    list(render_dict.values())[render_box.curselection()[0]].render(render_dir)
    webbrowser.open(render_dir)
    update_render_box()


def make_overlap():
    global machine_controller, top_image, base_image
    if base_image is not None and top_image is not None:
        try:
            new_render(machine_controller.overlap(base_image, top_image), f"合成图")
        except BaseException:
            raise
        base_image = None
        top_image = None
    update_combo_box()


def update_combo_box():
    global overlap_box, base_image, top_image
    overlap_box.delete(0, tkinter.END)
    if base_image is not None:
        overlap_box.insert(tkinter.END, f"底图: {base_image}")
    if top_image is not None:
        overlap_box.insert(tkinter.END, f"顶图: {top_image}")


def add_basemap():
    global base_image
    base_image = list(render_dict.keys())[render_box.curselection()[0]]
    update_combo_box()


def add_top_image():
    global top_image
    top_image = list(render_dict.keys())[render_box.curselection()[0]]
    update_combo_box()


def del_rendering():
    global render_dict, render_box, machine_controller
    key = list(render_dict.keys())[render_box.curselection()[0]]
    machine_controller.del_render(key)
    update_render_box()


def update_render_box():
    global render_dict, render_box, machine_controller
    render_dict = machine_controller.get_all_render()
    render_box.delete(0, tkinter.END)
    render_box.insert(tkinter.END, *render_dict.keys())


def new_render(c, name):
    global render_dict, draw_as_well
    if bool(draw_as_well.get()):
        c.render(f"{PATH}\\{name}.html")
    update_render_box()


def to_geo():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_geo(name, get_rendering_parameters()), "Geo地图")


def to_map():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_map(name, get_rendering_parameters()), "Map地图")


def to_scattergeo():
    global machine_controller
    name = get_sheet_name()
    new_render(
        machine_controller.to_scattergeo(name, get_rendering_parameters()), "Geo点地图"
    )


def to_treemap():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_tree_map(name, get_rendering_parameters()), "矩形树图")


def to_tree():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_tree(name, get_rendering_parameters()), "树状图")


def to_sankey():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_sankey(name, get_rendering_parameters()), "桑基图")


def to_sunburst():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_sunburst(name, get_rendering_parameters()), "旭日图")


def to_theme_river():
    global machine_controller
    name = get_sheet_name()
    new_render(
        machine_controller.to_theme_river(name, get_rendering_parameters()), "河流图"
    )


def to_calendar():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_calendar(name, get_rendering_parameters()), "日历图")


def to_gauge():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_gauge(name, get_rendering_parameters()), "仪表图")


def to_liquid():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_liquid(name, get_rendering_parameters()), "水球图")


def to_line3d():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_line3d(name, get_rendering_parameters()), "3D折线图")


def to_scatter3d():
    global machine_controller
    name = get_sheet_name()
    new_render(
        machine_controller.to_scatter3d(name, get_rendering_parameters()), "3D散点图"
    )


def to_bar3d():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_bar3d(name, get_rendering_parameters()), "3D柱状图")


def to_word_cloud():
    global machine_controller
    name = get_sheet_name()
    new_render(
        machine_controller.to_word_cloud(name, get_rendering_parameters()), "词云图"
    )


def to_radar():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_radar(name, get_rendering_parameters()), "雷达图")


def to_polar():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_polar(name, get_rendering_parameters()), "极坐标图")


def to_pie():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_pie(name, get_rendering_parameters()), "饼图")


def to_parallel():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_parallel(name, get_rendering_parameters()), "多轴图")


def to_graph():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_graph(name, get_rendering_parameters()), "关系图")


def to_format_graph():
    global machine_controller
    name = get_sheet_name()
    new_render(
        machine_controller.to_format_graph(name, get_rendering_parameters()), "关系图"
    )


def to_funnel():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_funnel(name, get_rendering_parameters()), "漏斗图")


def to_heat_map():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_heatmap(name, get_rendering_parameters()), "热力图")


def to_boxpolt():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_boxpolt(name, get_rendering_parameters()), "箱形图")


def to_pictorialbar():
    global machine_controller
    name = get_sheet_name()
    new_render(
        machine_controller.to_pictorialbar(name, get_rendering_parameters()), "象形柱状图"
    )


def to_scatter():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_scatter(name, get_rendering_parameters()), "散点图")


def to_line():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_line(name, get_rendering_parameters()), "折线图")


def to_bar():
    global machine_controller
    name = get_sheet_name()
    new_render(machine_controller.to_bar(name, get_rendering_parameters()), "柱状图")


def show_dictionary():
    tkinter.messagebox.showinfo("帮助字典", clean_help)


def open_python():
    global clean_code
    file_dir = askopenfilename(
        title="打开Python脚本", filetypes=[("Python", ".py"), ("TXT", ".txt")]
    )
    with open(file_dir) as f:
        get = f.read()
        clean_code.delete("0.0", tkinter.END)
        clean_code.insert("0.0", get)


def reset():
    global clean_code, clean_default_script
    clean_code.delete("0.0", tkinter.END)
    clean_code.insert("0.0", clean_default_script)


def view_cleaning_script():
    global machine_controller, clean_list, clean_func_box, clean_code
    name = clean_list[clean_func_box.curselection()[0]]
    get = machine_controller.get_clean_code(name)
    clean_code.delete("0.0", tkinter.END)
    clean_code.insert("0.0", get)


def empty_cleaning_script():
    global machine_controller
    machine_controller.del_all_clean_func()
    update_sheet_box()


def execute_cleaning_script():
    global machine_controller
    name = get_sheet_name()
    data = machine_controller.data_clean(name)
    title = f"CoTan数据处理 表格:{name}.数据清洗"
    vitables(data, title)
    update_sheet_box()


def del_cleaning_script():
    global machine_controller, clean_list, clean_func_box
    name = clean_list[clean_func_box.curselection()[0]]
    machine_controller.del_clean_func(name)
    update_cleaning_script_box()


def update_cleaning_script_box():
    global machine_controller, clean_func_box, clean_list
    clean_list = machine_controller.get_clean_func()
    clean_func_box.delete(0, tkinter.END)
    clean_func_box.insert(tkinter.END, *clean_list)


def add_cleaning_script():
    global machine_controller, clean_func_box, clean_code
    exp = clean_code.get("0.0", tkinter.END)
    machine_controller.add_clean_func(exp)
    update_cleaning_script_box()


def clear_nan_row():
    global drop_column
    name = get_sheet_name()
    data = machine_controller.del_nan(name, True)
    title = f"CoTan数据处理 表格:{name}.NaN"
    vitables(data, title)
    update_sheet_box()


def is_nan():
    global bool_exp
    name = get_sheet_name()
    data = machine_controller.is_nan(name)
    title = f"CoTan数据处理 表格:{name}.NaN"
    vitables(data, title)
    update_sheet_box()


def to_bool():
    global bool_exp
    bool_exp = bool_exp.get()
    name = get_sheet_name()
    data = machine_controller.to_bool(name, bool_exp, True)
    print(data)
    title = f"CoTan数据处理 表格:{name} 布尔化"
    vitables(data, title)
    update_sheet_box()


def del_data():
    global slice_new, column_clist, row_clist
    column = column_clist[0].get().replace(" ", "").split(",")
    row = row_clist[0].get().replace(" ", "").split(",")
    new = bool(slice_new.get())
    name = get_sheet_name()
    try:
        data = machine_controller.del_slice(name, column, row, new)
    except BaseException:
        data = "None 你的操作不被允许"
    title = f"CoTan数据处理 表格:{name}"
    vitables(data, title)
    update_sheet_box()


def __split_slice(n, t):
    a = []
    for i in n:
        b = i.get().replace(" ", "")
        if b == "":
            a.append(None)
        else:
            try:
                a.append(t(b))
            except BaseException:
                a.append(None)
    if a[0] is not None and a[1] is None:
        a[1] = a[0] + 1
        a[2] = None
    return a


def slice_data():
    global slice_new, column_type, row_type, column_clist, row_clist
    the_column_type = column_type.get()
    is_iloc = True
    if the_column_type == 0:  # 输入的列号
        column = slice(*__split_slice(column_clist, int))
    elif the_column_type == 1:
        is_iloc = False
        column = slice(*__split_slice(column_clist, str))
    else:
        get = column_clist[0].get().replace(" ", "").split(",")
        column = []
        for i in get:
            try:
                column.append(int(i))
            except BaseException:
                pass

    the_row_type = row_type.get()
    if the_row_type == 0:  # 输入的列号
        row = slice(*__split_slice(row_clist, int))
    elif the_row_type == 1:
        row = slice(*__split_slice(row_clist, str))
    else:
        get = row_clist[0].get().replace(" ", "").split(",")
        row = []
        for i in get:
            try:
                row.append(int(i))
            except BaseException:
                pass
    new = bool(slice_new.get())
    name = get_sheet_name()
    try:
        data = machine_controller.get_slice(name, column, row, is_iloc, new)
    except BaseException:
        data = "None 你的操作不被允许"
    title = f"CoTan数据处理 表格:{name}"
    vitables(data, title)
    update_sheet_box()


def sample_data():
    global machine_controller, ascending_new
    name = get_sheet_name()
    new = bool(ascending_new.get())
    data = machine_controller.sample(name, new)
    title = f"CoTan数据处理 打乱表格:{name}"
    vitables(data, title)
    update_sheet_box()


def stored_value():
    global machine_controller, stored_list, ascending_new
    name = get_sheet_name()
    new = bool(ascending_new.get())
    data = machine_controller.stored_value(name, stored_list, new)
    title = f"CoTan数据处理 表格:{name}.Stored"
    vitables(data, title)
    update_sheet_box()


def del_baseline():
    global stored_list, stored_box, ascending_type
    del stored_list[stored_box.curselection()[0]]
    update_sort_box()


def add_baseline():  # 按基准列排行
    global machine_controller, stored_list, sort_by, ascending_type
    try:
        a = not bool(ascending_type.get())
        value = int(sort_by.get())
        stored_list.append((value, a))
    except BaseException:
        pass
    update_sort_box()


def update_sort_box():
    global stored_list, stored_box
    re = []
    d = {True: "正序", False: "倒叙"}
    for i in stored_list:
        re.append(f"列号:{i[0]}, 排序方式{d[i[1]]}")
    stored_box.delete(0, tkinter.END)
    stored_box.insert(tkinter.END, *re)


def sort_by_column():  # 行
    global machine_controller
    name = get_sheet_name()
    a = not bool(ascending_type.get())
    new = bool(ascending_new.get())
    data = machine_controller.sorted_index(name, False, new, a)
    title = f"CoTan数据处理 表格:{name}.Stored by Column"
    vitables(data, title)
    update_sheet_box()


def sort_by_tow():  # 行
    global machine_controller
    name = get_sheet_name()
    new = bool(ascending_new.get())
    a = not bool(ascending_type.get())
    data = machine_controller.sorted_index(name, True, new, a)
    title = f"CoTan数据处理 表格:{name}.Stored by Row"
    vitables(data, title)
    update_sheet_box()


def transpose():
    global machine_controller
    name = get_sheet_name()
    new = bool(ascending_new.get())
    data = machine_controller.transpose(name, new)
    title = f"CoTan数据处理 表格:{name}.T"
    vitables(data, title)
    update_sheet_box()


def show_report():
    global PATH, SCREEN
    if not tkinter.messagebox.askokcancel("提示", f"是否统计数据，大量的数据需要耗费一定的时间(确定后，系统会在后台统计)"):
        return False
    report_dir = f"{PATH}/$Show_Des_Sheet.html"
    try:
        name = get_sheet_name()
        if name is None:
            raise Exception
        machine_controller.to_report(name, report_dir)
        webbrowser.open(report_dir)
    except BaseException:
        pass


def show_describe():
    global machine_controller, des_bool
    describe = bool(des_bool.get())
    name = get_sheet_name()
    title = f"CoTan数据处理 表格:{name}_describe"
    data = str(machine_controller.describe(name, describe))
    vitables(data, title)
    update_sheet_box()


def show_sheet():
    global machine_controller, SCREEN
    name = get_sheet_name()
    title = f"CoTan数据处理 表格:{name}"
    data = str(machine_controller.get_sheet(name))
    vitables(data, title)


def vitables(data, name):
    global bg_color, FONT1
    new_top = tkinter.Toplevel(bg=bg_color)
    new_top.title(name)
    new_top.geometry("+10+10")  # 设置所在位置
    text = ScrolledText(new_top, font=FONT1, height=50)
    text.pack(fill=tkinter.BOTH)
    text.insert("0.0", data)
    text.config(state=tkinter.DISABLED)
    new_top.resizable(width=False, height=False)


def get_column():  # 列名(横行竖列，列名是上面的)
    global machine_controller
    name = get_sheet_name()
    update_index_box(machine_controller.get_column(name))


def get_row():  # 行名(横行竖列，行名左)
    global machine_controller
    name = get_sheet_name()
    update_index_box(machine_controller.get_index(name))


def update_index_box(index):
    global SCREEN, index_box
    index_box.delete(0, tkinter.END)
    index_box.insert(tkinter.END, *index)


def show_one_sheet_html():
    global PATH, to_html_type
    html_dir = f"{PATH}/$Show_Sheet.html"
    try:
        name = get_sheet_name()
        if name is None:
            raise Exception
        machine_controller.render_html_one(name, html_dir)
        webbrowser.open(html_dir)
    except BaseException:
        # pass
        raise


def show_sheet_html():
    global PATH, to_html_type
    html_dir = f"{PATH}/$Show_Sheet.html"
    try:
        name = get_sheet_name()
        if name is None:
            raise Exception
        machine_controller.render_html_all(name, html_dir, to_html_type.get())
        webbrowser.open(html_dir)
    except BaseException:
        pass


def to_csv():
    global SCREEN, sep, encoding, str_must, index_must
    save_dir = asksaveasfilename(title="选择保存的CSV", filetypes=[("CSV", ".csv")])
    csv_sep = sep.get()
    name = get_sheet_name()
    machine_controller.to_csv(name, save_dir, csv_sep)
    update_sheet_box()


def add_csv():
    global SCREEN, sep, encoding, str_must, index_must, sheet_name
    file_dir = askopenfilename(title="选择载入的CSV", filetypes=[("CSV", ".csv")])
    if file_dir == "":
        return False
    csv_sep = sep.get()
    csv_encoding = encoding.get()
    str_ = bool(str_must.get())
    index = bool(index_must.get())
    name = sheet_name.get().replace(" ", "")
    if name == "":
        name = os.path.splitext(os.path.split(file_dir)[1])[0]
    if csv_encoding == "":
        with open(file_dir, "rb") as f:
            csv_encoding = chardet.detect(f.read())["encoding"]
    if csv_sep == "":
        csv_sep = ","
    machine_controller.add_csv(file_dir, name, csv_sep, csv_encoding, str_, index)
    update_sheet_box()


def add_from_python():
    global SCREEN, sep, encoding, str_must, index_must
    file_dir = askopenfilename(
        title="选择载入的py", filetypes=[("Python", ".py"), ("Txt", ".txt")]
    )
    name = sheet_name.get().replace(" ", "")
    if name == "":
        name = os.path.splitext(os.path.split(file_dir)[1])[0]
    with open(file_dir, "r") as f:
        machine_controller.add_python(f.read(), name)
    update_sheet_box()


def get_sheet_name():  # 获得名字统一接口
    global sheet_list
    try:
        return sheet_list[sheet_box.curselection()[0]]
    except BaseException:
        try:
            return sheet_list[0]
        except BaseException:
            return None


def update_sheet_box():
    global SCREEN, sheet_box, sheet_list
    sheet_list = machine_controller.get_sheet_list()
    sheet_box.delete(0, tkinter.END)
    sheet_box.insert(tkinter.END, *sheet_list)


machine_learning()
