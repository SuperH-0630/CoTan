import os
import webbrowser
import tkinter
from newtkinter import askopenfilename, asksaveasfilename
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText

import chardet

import datascience.controller

render_dict = {}  # 保存了画图的List
learn_dict = {}  # 保存数据处理
PATH = os.getcwd()
sheet_list = []
machine_controller = datascience.controller.MachineLearner()
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


class UIAPI:
    @staticmethod
    def add_from_python_gui():
        file_dir = askopenfilename(
            title="选择载入的py", filetypes=[("Python", ".py"), ("Txt", ".txt")]
        )
        name = sheet_name.get().replace(" ", "")
        if name == "":
            name = os.path.splitext(os.path.split(file_dir)[1])[0]
        with open(file_dir, "r") as f:
            code = f.read()
        return code, name

    @staticmethod
    def get_sheet_name_gui():  # 获得名字统一接口
        global sheet_list
        try:
            return sheet_list[sheet_box.curselection()[0]]
        except BaseException:
            try:
                return sheet_list[0]
            except BaseException:
                return None

    @staticmethod
    def update_sheet_box_gui():
        global SCREEN, sheet_box, sheet_list
        sheet_list = machine_controller.get_sheet_list()
        sheet_box.delete(0, tkinter.END)
        sheet_box.insert(tkinter.END, *sheet_list)

    @staticmethod
    def update_combo_box_gui():
        overlap_box.delete(0, tkinter.END)
        if base_image is not None:
            overlap_box.insert(tkinter.END, f"底图: {base_image}")
        if top_image is not None:
            overlap_box.insert(tkinter.END, f"顶图: {top_image}")

    @staticmethod
    def add_csv_gui():
        file_dir = askopenfilename(title="选择载入的CSV", filetypes=[("CSV", ".csv")])
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
        return csv_encoding, csv_sep, file_dir, index, name, str_

    @staticmethod
    def to_csv_gui():
        save_dir = asksaveasfilename(title="选择保存的CSV", filetypes=[("CSV", ".csv")])
        csv_sep = sep.get()
        return csv_sep, save_dir

    @staticmethod
    def update_index_box_gui(index):
        global SCREEN, index_box
        index_box.delete(0, tkinter.END)
        index_box.insert(tkinter.END, *index)

    @staticmethod
    def vitables_gui(data, name):
        global bg_color, FONT1
        new_top = tkinter.Toplevel(bg=bg_color)
        new_top.title(name)
        new_top.geometry("+10+10")  # 设置所在位置
        text = ScrolledText(new_top, font=FONT1, height=50)
        text.pack(fill=tkinter.BOTH)
        text.insert("0.0", data)
        text.config(state=tkinter.DISABLED)
        new_top.resizable(width=False, height=False)

    @staticmethod
    def get_des_bool_gui():
        return bool(des_bool.get())

    @staticmethod
    def sort_by_column_gui():
        ascending = not bool(ascending_type.get())
        new = bool(ascending_new.get())
        return new, ascending

    @staticmethod
    def add_baseline_gui(ascending_type, sort_by):
        ascending = not bool(ascending_type.get())
        value = int(sort_by.get())
        return ascending, value

    @staticmethod
    def update_sort_box_gui():
        global stored_list, stored_box
        re = []
        d = {True: "正序", False: "倒叙"}
        for i in stored_list:
            re.append(f"列号:{i[0]}, 排序方式{d[i[1]]}")
        stored_box.delete(0, tkinter.END)
        stored_box.insert(tkinter.END, *re)

    @staticmethod
    def get_stored_box_index_gui():
        return stored_box.curselection()[0]

    @staticmethod
    def get_ascending_new_gui():
        new = bool(ascending_new.get())
        return new

    @staticmethod
    def slice_data_gui():
        def split_slice_core(slice_list, func_type):
            a = []
            for i in slice_list:
                b = i.get().replace(" ", "")
                if b == "":
                    a.append(None)
                else:
                    try:
                        a.append(func_type(b))
                    except BaseException:
                        a.append(None)
            if a[0] is not None and a[1] is None:
                a[1] = a[0] + 1
                a[2] = None
            return a

        the_column_type = column_type.get()
        is_iloc = True
        if the_column_type == 0:  # 输入的列号
            column = slice(*split_slice_core(column_clist, int))
        elif the_column_type == 1:
            is_iloc = False
            column = slice(*split_slice_core(column_clist, str))
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
            row = slice(*split_slice_core(row_clist, int))
        elif the_row_type == 1:
            row = slice(*split_slice_core(row_clist, str))
        else:
            get = row_clist[0].get().replace(" ", "").split(",")
            row = []
            for i in get:
                try:
                    row.append(int(i))
                except BaseException:
                    pass
        new = bool(slice_new.get())
        return column, is_iloc, new, row

    @staticmethod
    def del_data_gui():
        column = column_clist[0].get().replace(" ", "").split(",")
        row = row_clist[0].get().replace(" ", "").split(",")
        new = bool(slice_new.get())
        return column, new, row

    @staticmethod
    def get_clean_code_gui():
        exp = clean_code.get("0.0", tkinter.END)
        return exp

    @staticmethod
    def view_cleaning_script_gui():
        name = clean_list[API.get_clean_func_box_index_gui()]
        API.update_clean_code(machine_controller.get_clean_code(name))

    @staticmethod
    def get_clean_func_box_index_gui():
        return clean_func_box.curselection()[0]

    @staticmethod
    def show_dictionary_gui():
        tkinter.messagebox.showinfo("帮助字典", clean_help)

    @staticmethod
    def open_python_for_clean_gui():
        global clean_code
        file_dir = askopenfilename(
            title="打开Python脚本", filetypes=[("Python", ".py"), ("TXT", ".txt")]
        )
        with open(file_dir) as f:
            get = f.read()
            clean_code.delete("0.0", tkinter.END)
            clean_code.insert("0.0", get)

    @staticmethod
    def reset_clean_code_gui():
        global clean_code, clean_default_script
        API.update_clean_code(clean_default_script)

    @staticmethod
    def update_render_box_gui():
        global render_dict, render_box, machine_controller
        render_dict = machine_controller.get_all_render()
        render_box.delete(0, tkinter.END)
        render_box.insert(tkinter.END, *render_dict.keys())

    @staticmethod
    def get_draw_as_well_gui():
        return bool(draw_as_well.get())

    @staticmethod
    def render_box_index_gui():
        return render_box.curselection()[0]

    @staticmethod
    def rendering_one_gui():
        render_dir = asksaveasfilename(title="选择渲染保存地址", filetypes=[("HTML", ".html")])
        try:
            if render_dir[-5:] != ".html":
                raise Exception
        except BaseException:
            render_dir += ".html"
        return render_dir

    @staticmethod
    def rendering_gui():
        render_dir = asksaveasfilename(title="选择渲染保存地址", filetypes=[("HTML", ".html")])
        try:
            if render_dir[-5:] != ".html":
                raise Exception
        except BaseException:
            render_dir += ".html"
        return render_dir

    @staticmethod
    def set_dtype_gui():
        type_ = bool(dtype_func.get())
        name = API.get_sheet_name_gui()
        column_list = dtype_column.get().split(",")
        if column_list == [""]:
            column_list = []
        dtype = dtype_input.get()
        wrong = dtype_wrong.get()
        return column_list, dtype, name, type_, wrong

    @staticmethod
    def datetime_index_gui():
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
        return init, is_column, save

    @staticmethod
    def num_with_name_gui():
        is_column = bool(replace_index.get())  # 操作行名-False，操作列名-True
        save = bool(replace_type[0].get())
        return is_column, save

    @staticmethod
    def num_to_name_gui():
        is_column = bool(replace_index.get())  # 操作行名-False，操作列名-True
        save = bool(replace_type[0].get())
        return is_column, save

    @staticmethod
    def change_index_gui():
        is_column = bool(replace_index.get())  # 操作行名-False，操作列名-True
        iloc = int(replace_iloc.get())  # 替换的列号(行号)
        save = bool(replace_type[0].get())
        drop = not bool(replace_type[1].get())
        return drop, iloc, is_column, save

    @staticmethod
    def replace_index_func_gui():
        the_replace_dict = eval(replace_dict.get())
        is_column = bool(replace_index.get())  # 操作行-False，操作列-True
        save = bool(replace_type[0].get())
        return is_column, save, the_replace_dict

    @staticmethod
    def update_leaner_box_gui():
        global learn_dict, learner_box
        learn_dict = machine_controller.return_learner()
        learner_box.delete(0, tkinter.END)
        learner_box.insert(tkinter.END, *learn_dict.keys())

    @staticmethod
    def get_data_split_gui():
        try:
            split = float(data_split.get())
            if split < 0 or 1 < split:
                raise Exception
        except BaseException:
            split = 0.3
        return split

    @staticmethod
    def set_learner_gui():
        global chose_learner
        chose_learner.set(API.get_learner_name_gui(True))

    @staticmethod
    def get_learner_name_gui(learner_type=False):
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

    @staticmethod
    def askokcancel_gui(messgae):
        return tkinter.messagebox.askokcancel("提示", messgae)

    @staticmethod
    def show_tips_gui():
        tkinter.messagebox.showinfo("使用提示", drawing_parameters)

    @staticmethod
    def show_sorry_gui():
        tkinter.messagebox.showinfo("非常抱歉", "高级别的机器学习请到机器学习板块深入研究...")


class API(UIAPI):
    @staticmethod
    def clear_rendering():
        machine_controller.clean_render()
        API.update_render_box_gui()

    @staticmethod
    def del_form():
        name = API.get_sheet_name_gui()
        machine_controller.del_sheet(name)
        API.update_sheet_box_gui()

    @staticmethod
    def del_learner():
        learner = API.get_learner_name_gui(True)
        set_learne = API.get_learner_name_gui(False)  # 获取学习器Learner
        if set_learne != learner:
            machine_controller.del_leaner(learner)
        API.update_leaner_box_gui()

    @staticmethod
    def visual_learner():
        learner = API.get_learner_name_gui(True)
        data = machine_controller.visual_learner(
            learner, API.askokcancel_gui(f"是否将数据生成表格。\n(可绘制成散点图对比数据)")
        )
        API.vitables_gui(
            f"对象:{learner}\n\n{data[0]}\n\n\n{data[1]}", f"CoTan数据处理 查看数据:{learner}"
        )
        API.update_sheet_box_gui()

    @staticmethod
    def get_learner_config():
        return learner_parameters.get("0.0", tkinter.END)

    @staticmethod
    def test_learner():
        name = API.get_sheet_name_gui()  # 表格数据
        learner = API.get_learner_name_gui()
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

    @staticmethod
    def predict_learner():
        name = API.get_sheet_name_gui()  # 表格数据
        learner = API.get_learner_name_gui()
        data = machine_controller.predict(name, learner)
        title = f"CoTan数据处理 表格:{name} 学习器:{learner}"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def fit_learner():
        name = API.get_sheet_name_gui()  # 表格数据
        learner = API.get_learner_name_gui()
        split = API.get_data_split_gui()
        socore = machine_controller.training_machine(
            name, learner, parameters=API.get_learner_config(), split=split
        )
        tkinter.messagebox.showinfo(
            "训练完成",
            f"针对训练数据({(1 - split) * 100}%)评分结果为:{socore[0]}\n"
            f"针对测试数据评分({split * 100}%)结果为:{socore[1]}",
        )

    @staticmethod
    def add_knn_class():
        API.add_learner_core("Knn_class")

    @staticmethod
    def add_logistic_regression():
        API.add_learner_core("LogisticRegression")

    @staticmethod
    def add_lasso():
        API.add_learner_core("Lasso")

    @staticmethod
    def add_knn_regression():
        API.add_learner_core("Knn")

    @staticmethod
    def add_ridge():
        API.add_learner_core("Ridge")

    @staticmethod
    def add_generalized_linear():
        API.add_learner_core("Line")

    @staticmethod
    def add_learner_core(learner_type):  # 添加Lenear的核心
        machine_controller.add_learner(learner_type, parameters=API.get_learner_config())
        API.update_leaner_box_gui()

    @staticmethod
    def feature_extraction():
        name = API.get_sheet_name_gui()
        machine_controller.decision_tree_classifier(name)
        API.update_sheet_box_gui()

    @staticmethod
    def replace_index_func():
        name = API.get_sheet_name_gui()
        is_column, save, the_replace_dict = API.replace_index_func_gui()
        machine_controller.replace_index(name, is_column, the_replace_dict, save)
        API.update_sheet_box_gui()

    @staticmethod
    def change_index():
        name = API.get_sheet_name_gui()  # 名字
        drop, iloc, is_column, save = API.change_index_gui()

        machine_controller.change_index(name, is_column, iloc, save, drop)
        API.update_sheet_box_gui()

    @staticmethod
    def num_to_name():
        name = API.get_sheet_name_gui()  # 名字
        is_column, save = API.num_to_name_gui()

        machine_controller.number_naming(name, is_column, save)
        API.update_sheet_box_gui()

    @staticmethod
    def num_with_name():
        name = API.get_sheet_name_gui()  # 名字
        is_column, save = API.num_with_name_gui()

        machine_controller.name_with_number(name, is_column, save)
        API.update_sheet_box_gui()

    @staticmethod
    def datetime_index(is_date=True):
        name = API.get_sheet_name_gui()  # 名字
        init, is_column, save = API.datetime_index_gui()
        if is_date:
            machine_controller.date_index(name, is_column, save, **init)
        else:
            machine_controller.time_naming(name, is_column, save, **init)
        API.update_sheet_box_gui()

    @staticmethod
    def date_index():
        API.datetime_index(True)

    @staticmethod
    def time_index():
        API.datetime_index(False)

    @staticmethod
    def set_dtype():
        column_list, dtype, name, type_, wrong = API.set_dtype_gui()
        if type_:  # 软转换
            if wrong != "ignore":
                wrong = "coerce"
            machine_controller.set_dtype(name, column_list, dtype, wrong)
        else:
            machine_controller.as_dtype(name, column_list, dtype, "ignore")
        API.update_sheet_box_gui()

    @staticmethod
    def python_render():  # 导入绘制方法
        file_dir = askopenfilename(
            title="打开Python脚本", filetypes=[("Python", ".py"), ("TXT", ".txt")]
        )
        with open(file_dir) as f:
            code = f.read()
        API.new_render(machine_controller.custom_graph(code), "自定义图")

    @staticmethod
    def get_rendering_parameters():  # 获取画图的args
        return rendering_parameters.get("0.0", tkinter.END)

    @staticmethod
    def rendering():
        render_dir = API.rendering_gui()
        webbrowser.open(
            machine_controller.render_all(API.get_rendering_parameters(), render_dir)
        )
        API.update_render_box_gui()

    @staticmethod
    def rendering_one():
        render_dir = API.rendering_one_gui()
        list(render_dict.values())[API.render_box_index_gui()].render(render_dir)
        webbrowser.open(render_dir)
        API.update_render_box_gui()

    @staticmethod
    def make_overlap():
        global top_image, base_image
        if base_image is not None and top_image is not None:
            try:
                API.new_render(machine_controller.overlap(base_image, top_image), f"合成图")
            except BaseException:
                raise
            base_image = None
            top_image = None
        API.update_combo_box_gui()

    @staticmethod
    def add_basemap():
        global base_image
        base_image = list(render_dict.keys())[API.render_box_index_gui()]
        API.update_combo_box_gui()

    @staticmethod
    def add_top_image():
        global top_image
        top_image = list(render_dict.keys())[API.render_box_index_gui()]
        API.update_combo_box_gui()

    @staticmethod
    def del_rendering():
        key = list(render_dict.keys())[API.render_box_index_gui()]
        machine_controller.del_render(key)
        API.update_render_box_gui()

    @staticmethod
    def new_render(c, name):
        if API.get_draw_as_well_gui():
            c.render(f"{PATH}\\{name}.html")
        API.update_render_box_gui()

    @staticmethod
    def to_geo():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_geo(name, API.get_rendering_parameters()), "Geo地图")

    @staticmethod
    def to_map():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_map(name, API.get_rendering_parameters()), "Map地图")

    @staticmethod
    def to_scattergeo():
        name = API.get_sheet_name_gui()
        API.new_render(
            machine_controller.to_scattergeo(name, API.get_rendering_parameters()), "Geo点地图"
        )

    @staticmethod
    def to_treemap():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_tree_map(name, API.get_rendering_parameters()), "矩形树图")

    @staticmethod
    def to_tree():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_tree(name, API.get_rendering_parameters()), "树状图")

    @staticmethod
    def to_sankey():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_sankey(name, API.get_rendering_parameters()), "桑基图")

    @staticmethod
    def to_sunburst():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_sunburst(name, API.get_rendering_parameters()), "旭日图")

    @staticmethod
    def to_theme_river():
        name = API.get_sheet_name_gui()
        API.new_render(
            machine_controller.to_theme_river(name, API.get_rendering_parameters()), "河流图"
        )

    @staticmethod
    def to_calendar():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_calendar(name, API.get_rendering_parameters()), "日历图")

    @staticmethod
    def to_gauge():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_gauge(name, API.get_rendering_parameters()), "仪表图")

    @staticmethod
    def to_liquid():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_liquid(name, API.get_rendering_parameters()), "水球图")

    @staticmethod
    def to_line3d():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_line3d(name, API.get_rendering_parameters()), "3D折线图")

    @staticmethod
    def to_scatter3d():
        name = API.get_sheet_name_gui()
        API.new_render(
            machine_controller.to_scatter3d(name, API.get_rendering_parameters()), "3D散点图"
        )

    @staticmethod
    def to_bar3d():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_bar3d(name, API.get_rendering_parameters()), "3D柱状图")

    @staticmethod
    def to_word_cloud():
        name = API.get_sheet_name_gui()
        API.new_render(
            machine_controller.to_word_cloud(name, API.get_rendering_parameters()), "词云图"
        )

    @staticmethod
    def to_radar():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_radar(name, API.get_rendering_parameters()), "雷达图")

    @staticmethod
    def to_polar():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_polar(name, API.get_rendering_parameters()), "极坐标图")

    @staticmethod
    def to_pie():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_pie(name, API.get_rendering_parameters()), "饼图")

    @staticmethod
    def to_parallel():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_parallel(name, API.get_rendering_parameters()), "多轴图")

    @staticmethod
    def to_graph():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_graph(name, API.get_rendering_parameters()), "关系图")

    @staticmethod
    def to_format_graph():
        name = API.get_sheet_name_gui()
        API.new_render(
            machine_controller.to_format_graph(name, API.get_rendering_parameters()), "关系图"
        )

    @staticmethod
    def to_funnel():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_funnel(name, API.get_rendering_parameters()), "漏斗图")

    @staticmethod
    def to_heat_map():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_heatmap(name, API.get_rendering_parameters()), "热力图")

    @staticmethod
    def to_boxpolt():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_boxpolt(name, API.get_rendering_parameters()), "箱形图")

    @staticmethod
    def to_pictorialbar():
        name = API.get_sheet_name_gui()
        API.new_render(
            machine_controller.to_pictorialbar(name, API.get_rendering_parameters()), "象形柱状图"
        )

    @staticmethod
    def to_scatter():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_scatter(name, API.get_rendering_parameters()), "散点图")

    @staticmethod
    def to_line():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_line(name, API.get_rendering_parameters()), "折线图")

    @staticmethod
    def to_bar():
        name = API.get_sheet_name_gui()
        API.new_render(machine_controller.to_bar(name, API.get_rendering_parameters()), "柱状图")

    @staticmethod
    def update_clean_code(clean_default_script):
        clean_code.delete("0.0", tkinter.END)
        clean_code.insert("0.0", clean_default_script)

    @staticmethod
    def empty_cleaning_script():
        machine_controller.del_all_clean_func()
        API.update_sheet_box_gui()

    @staticmethod
    def execute_cleaning_script():
        name = API.get_sheet_name_gui()
        data = machine_controller.data_clean(name)
        title = f"CoTan数据处理 表格:{name}.数据清洗"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def del_cleaning_script():
        name = clean_list[API.get_clean_func_box_index_gui()]
        machine_controller.del_clean_func(name)
        API.update_cleaning_script_box()

    @staticmethod
    def update_cleaning_script_box():
        clean_list = machine_controller.get_clean_func()
        clean_func_box.delete(0, tkinter.END)
        clean_func_box.insert(tkinter.END, *clean_list)

    @staticmethod
    def add_cleaning_script():
        exp = API.get_clean_code_gui()
        machine_controller.add_clean_func(exp)
        API.update_cleaning_script_box()

    @staticmethod
    def clean_nan_row():
        name = API.get_sheet_name_gui()
        data = machine_controller.del_nan(name, True)
        title = f"CoTan数据处理 表格:{name}.NaN"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def is_nan():
        name = API.get_sheet_name_gui()
        data = machine_controller.is_nan(name)
        title = f"CoTan数据处理 表格:{name}.NaN"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def to_bool():
        the_bool_exp = bool_exp.get()
        name = API.get_sheet_name_gui()
        data = machine_controller.to_bool(name, the_bool_exp, True)
        title = f"CoTan数据处理 表格:{name} 布尔化"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def del_data():
        name = API.get_sheet_name_gui()
        column, new, row = API.del_data_gui()
        try:
            data = machine_controller.del_slice(name, column, row, new)
        except BaseException:
            data = "None 你的操作不被允许"
        title = f"CoTan数据处理 表格:{name}"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def slice_data():
        column, is_iloc, new, row = API.slice_data_gui()
        name = API.get_sheet_name_gui()
        try:
            data = machine_controller.get_slice(name, column, row, is_iloc, new)
        except BaseException:
            data = "None 你的操作不被允许"
        title = f"CoTan数据处理 表格:{name}"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def sample_data():
        name = API.get_sheet_name_gui()
        new = API.get_ascending_new_gui()
        data = machine_controller.sample(name, new)
        title = f"CoTan数据处理 打乱表格:{name}"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def stored_value():
        name = API.get_sheet_name_gui()
        new = API.get_ascending_new_gui()
        data = machine_controller.stored_value(name, stored_list, new)
        title = f"CoTan数据处理 表格:{name}.Stored"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def del_baseline():
        global stored_list, stored_box
        del stored_list[API.get_stored_box_index_gui()]
        API.update_sort_box_gui()

    @staticmethod
    def add_baseline():  # 按基准列排行
        try:
            ascending, value = API.add_baseline_gui(ascending_type, sort_by)
            stored_list.append((value, ascending))
        except BaseException:
            pass
        API.update_sort_box_gui()

    @staticmethod
    def sort_by_column():  # 行
        name = API.get_sheet_name_gui()
        new, ascending = API.sort_by_column_gui()
        data = machine_controller.sorted_index(name, False, new, ascending)
        title = f"CoTan数据处理 表格:{name}.Stored by Column"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def sort_by_tow():  # 行
        name = API.get_sheet_name_gui()
        new, ascending = API.sort_by_column_gui()
        data = machine_controller.sorted_index(name, True, new, ascending)
        title = f"CoTan数据处理 表格:{name}.Stored by Row"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def transpose():
        name = API.get_sheet_name_gui()
        new = API.get_ascending_new_gui()
        data = machine_controller.transpose(name, new)
        title = f"CoTan数据处理 表格:{name}.T"
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def show_report():
        if not API.askokcancel_gui(f"是否统计数据，大量的数据需要耗费一定的时间(确定后，系统会在后台统计)"):
            raise Exception
        report_dir = f"{PATH}/$Show_Des_Sheet.html"
        try:
            name = API.get_sheet_name_gui()
            if name is None:
                raise Exception
            machine_controller.to_report(name, report_dir)
            webbrowser.open(report_dir)
        except BaseException:
            pass

    @staticmethod
    def show_describe():
        describe = API.get_des_bool_gui()
        name = API.get_sheet_name_gui()
        title = f"CoTan数据处理 表格:{name}_describe"
        data = str(machine_controller.describe(name, describe))
        API.vitables_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    def show_sheet():
        name = API.get_sheet_name_gui()
        title = f"CoTan数据处理 表格:{name}"
        data = str(machine_controller.get_sheet(name))
        API.vitables_gui(data, title)

    @staticmethod
    def get_column():  # 列名(横行竖列，列名是上面的)
        name = API.get_sheet_name_gui()
        API.update_index_box_gui(machine_controller.get_column(name))

    @staticmethod
    def get_row():  # 行名(横行竖列，行名左)
        name = API.get_sheet_name_gui()
        API.update_index_box_gui(machine_controller.get_index(name))

    @staticmethod
    def show_one_sheet_html():
        global PATH, to_html_type
        html_dir = f"{PATH}/$Show_Sheet.html"
        try:
            name = API.get_sheet_name_gui()
            if name is None:
                raise Exception
            machine_controller.render_html_one(name, html_dir)
            webbrowser.open(html_dir)
        except BaseException:
            pass

    @staticmethod
    def show_sheet_html():
        global PATH, to_html_type
        html_dir = f"{PATH}/$Show_Sheet.html"
        try:
            name = API.get_sheet_name_gui()
            if name is None:
                raise Exception
            machine_controller.render_html_all(name, html_dir, to_html_type.get())
            webbrowser.open(html_dir)
        except BaseException:
            pass

    @staticmethod
    def to_csv():
        global SCREEN, sep, encoding, str_must, index_must
        csv_sep, save_dir = API.to_csv_gui()
        name = API.get_sheet_name_gui()
        machine_controller.to_csv(name, save_dir, csv_sep)
        API.update_sheet_box_gui()

    @staticmethod
    def add_csv():
        global SCREEN, sep, encoding, str_must, index_must, sheet_name
        csv_encoding, csv_sep, file_dir, index, name, str_ = API.add_csv_gui()
        machine_controller.add_csv(file_dir, name, csv_sep, csv_encoding, str_, index)
        API.update_sheet_box_gui()

    @staticmethod
    def add_from_python():
        global SCREEN, sep, encoding, str_must, index_must
        code, name = API.add_from_python_gui()
        machine_controller.add_python(code, name)
        API.update_sheet_box_gui()


def machine_learning():
    global SCREEN
    SCREEN.mainloop()


tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="导入CSV",
    command=API.add_csv,
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
    command=API.add_from_python,
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
    command=API.to_csv,
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
sheet_name.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除表格",
    command=API.del_form,
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
    command=API.show_sheet_html,
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
    command=API.show_one_sheet_html,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)

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
sheet_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 5)  # 显示符号
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
    command=API.get_row,
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
    command=API.get_column,
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
    command=API.show_sheet,
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
max_column.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

# Row与Column Row是横行，tkinter布局中Row变大，表示所在行数变大，向下移动如：
# 1，2，3，4，5，6
# 7，8，9，a，b，c
# 其中数字1-6是第一行，1-c是第二行，第二行在第一行下面，row变大向下移动（Row是横向行而不是横向移动） to 搞不清楚横行竖列的人

row += 1
index_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 10)  # 显示符号
index_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=10,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 10
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="查看数据分析",
    command=API.show_report,
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
    command=API.show_describe,
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
    command=API.slice_data,
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
    command=API.del_data,
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
bool_exp.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.W + tkinter.E)

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
drop_column.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.W + tkinter.E)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="生成布尔表格",
    command=API.to_bool,
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
    command=API.is_nan,
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
    command=API.clean_nan_row,
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
    command=API.add_cleaning_script,
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
    command=API.del_cleaning_script,
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
    command=API.feature_extraction,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)

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
    command=API.show_dictionary_gui,
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
    command=API.reset_clean_code_gui,
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
    command=API.execute_cleaning_script,
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
    command=API.empty_cleaning_script,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="查看执行方法",
    command=API.view_cleaning_script_gui,
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
    command=API.open_python_for_clean_gui,
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
    command=API.to_bar,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="生成3D柱状图",
    command=API.to_bar3d,
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
    command=API.to_line,
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
    command=API.to_line3d,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="生成象形柱状图",
    command=API.to_pictorialbar,
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
    command=API.to_scatter,
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
    command=API.to_scatter3d,
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
    command=API.to_boxpolt,
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
    command=API.to_funnel,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="生成热力图",
    command=API.to_heat_map,
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
    command=API.to_pie,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="生成多轴图",
    command=API.to_parallel,
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
    command=API.to_polar,
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
    command=API.to_radar,
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
    command=API.to_word_cloud,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="生成关系图",
    command=API.to_format_graph,
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
    command=API.to_graph,
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
    command=API.to_liquid,
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
    command=API.to_gauge,
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
    command=API.to_calendar,
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
    command=API.to_theme_river,
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
    command=API.to_sunburst,
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
    command=API.to_sankey,
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
    command=API.to_tree,
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
    command=API.to_treemap,
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
    command=API.to_map,
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
    command=API.to_scattergeo,
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
    command=API.to_geo,
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
    command=API.add_basemap,
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
    command=API.add_top_image,
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
    command=API.make_overlap,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)

row += 1
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
    command=API.rendering,
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
    command=API.rendering_one,
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
    command=API.del_rendering,
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
draw_as_well = tkinter.IntVar()
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="清空渲染",
    command=API.clear_rendering,
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
    command=API.python_render,
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
rendering_parameters = tkinter.Text(SCREEN, width=gui_width * 3, height=gui_height * 7)
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
    command=API.show_dictionary_gui,
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
    command=API.show_tips_gui,
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
    command=API.num_with_name,
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
    command=API.num_to_name,
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
    command=API.change_index,
    font=FONT,
    width=gui_width * 2,
    height=gui_height,
).grid(column=column, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="执行替换操作",
    command=API.replace_index_func,
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

row += 1
date_type = tkinter.IntVar()
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="刷入Date序列",
    command=API.date_index,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="刷入Time序列",
    command=API.time_index,
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
dtype_input.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

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
dtype_wrong.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="执行转换",
    command=API.set_dtype,
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
    command=API.transpose,
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
    command=API.sort_by_tow,
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
    command=API.sort_by_column,
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
    command=API.stored_value,
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
stored_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 4)  # 显示符号
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
    command=API.add_baseline,
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
    command=API.del_baseline,
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
    command=API.sample_data,
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
    command=API.set_learner_gui,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

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
data_split.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

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
    command=API.rendering,
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
    command=API.visual_learner,
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
    command=API.del_learner,
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
    command=API.fit_learner,
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
    command=API.test_learner,
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
    command=API.predict_learner,
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
    command=API.add_generalized_linear,
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
    command=API.add_ridge,
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
    command=API.add_lasso,
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
    command=API.add_logistic_regression,
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
    command=API.show_sorry_gui,
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
    command=API.show_sorry_gui,
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
    command=API.show_sorry_gui,
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
    command=API.add_knn_regression,
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
    command=API.add_knn_class,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)

row += 1
learner_parameters = tkinter.Text(SCREEN, width=gui_width * 3, height=gui_height * 11)
learner_parameters.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=11,
    sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
)
