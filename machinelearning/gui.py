import os
import tkinter
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
from newtkinter import askopenfilename, asksaveasfilename, askdirectory
import chardet
import webbrowser

import machinelearning.controller
import machinelearning.template

calculation_list = []
calculation_method = []
PATH = os.getcwd()
sheet_list = []
merge_list = []
learner_controller = machinelearning.controller.MachineLearner()
SCREEN = tkinter.Tk()
gui_width = 13  # 标准宽度
gui_height = 2
row = 0
column = 0
bg_color = "#FFFAFA"  # 主颜色
botton_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
SCREEN["bg"] = bg_color
FONT = ("黑体", 11)  # 设置字体


def machine_learning():
    global SCREEN
    SCREEN.mainloop()


def add_reverse_fast_fourier2():  # 添加Lenear的核心
    add_leaner("[2]Reverse_Fast_Fourier")


def add_reverse_fast_fourier():  # 添加Lenear的核心
    add_leaner("Reverse_Fast_Fourier")


def add_fast_fourier():  # 添加Lenear的核心
    add_leaner("Fast_Fourier")


def curve_fitting():
    file_dir = askopenfilename(title="导入参数")
    with open(file_dir, "r") as f:
        learner_controller.add_curve_fitting(f.read())
        update_leaner()


def show_clustering_score():
    show_score(2)


def show_regression_score():
    show_score(1)


def show_class_score():
    show_score(0)


def show_score(func):
    learner = get_learner(True)
    save_dir = askdirectory(title="选择保存位置")
    data = learner_controller.model_evaluation(
        learner, save_dir, get_name(False, True), get_name(False, False), func
    )
    webbrowser.open(data[0])
    webbrowser.open(data[1])  # 还可以打开文件管理器
    update_sheet_box()


def calculation():
    global calculation_list, calculation_method, calculation_type
    func = calculation_type.get()
    if len(calculation_list) == 2 and 1 in calculation_method:
        learner_controller.calculation_matrix(
            calculation_list, calculation_method, func
        )
    update_sheet_box()


def add_calculation_core(num, type_):
    global calculation_list, calculation_method
    if len(calculation_list) == 2:
        del calculation_list[0]
        del calculation_method[0]
    calculation_list.append(num)
    calculation_method.append(type_)


def update_calculation_box():
    global calculation_list, calculation_method, calculation_box
    calculation_box.delete(0, tkinter.END)
    a = ["第一参数", "第二参数"]
    b = ["参数", "矩阵"]
    calculation_box.insert(
        tkinter.END,
        *[
            f"{a[i]} {calculation_list[i]} {b[calculation_method[i]]}"
            for i in range(len(calculation_list))
        ],
    )


def add_calculation_number():
    global calculation_box, calculation_type, value
    num = eval(value.get(), {})
    add_calculation_core(num, 0)
    update_calculation_box()


def add_calculation_object():
    name = get_name()
    add_calculation_core(name, 1)
    update_calculation_box()


def del_leaner():
    learn = get_learner(True)
    set_learne = get_learner(False)  # 获取学习器Learner
    if set_learne != learn:
        learner_controller.del_leaner(learn)
    update_leaner()


def global_seeting():
    global global_settings
    args = [bool(i.get()) for i in global_settings]
    machinelearning.template.set_global(*args)


def reshape():
    global learner_controller, processing_type, shape
    numpy_shape = eval(f"[{shape.get()}]")[0]
    learner_controller.reshape(get_name(), numpy_shape)
    update_sheet_box()


def transpose():
    global learner_controller, processing_type, shape
    try:
        func = eval(f"[{shape.get()}]")
    except BaseException:
        func = None
    learner_controller.transpose(get_name(), func)
    update_sheet_box()


def del_ndim():
    global learner_controller
    learner_controller.del_ndim(get_name())
    update_sheet_box()


def reval():
    global learner_controller, processing_type
    reval_type = processing_type.get()
    learner_controller.reval(get_name(), reval_type)
    update_sheet_box()


def two_split():
    global learner_controller, processing_type, shape
    split_type = processing_type.get()
    learner_controller.two_split(get_name(), shape.get(), split_type)
    update_sheet_box()


def split():
    global learner_controller, processing_type, shape
    split_type = processing_type.get()
    try:
        split_shape_list = eval(f"[{shape.get()}]", {})[0]
    except BaseException:
        split_shape_list = 2
    learner_controller.split(get_name(), split_shape_list, split_type)
    update_sheet_box()


def merge():
    global merge_list, learner_controller, processing_type
    if len(merge_list) < 1:
        return False
    merge_type = processing_type.get()
    learner_controller.merge(merge_list, merge_type)
    update_sheet_box()


def update_merge_box():
    global merge_list, merge_box
    merge_box.delete(0, tkinter.END)
    merge_box.insert(tkinter.END, *merge_list)


def merge_del():
    global merge_list, merge_box
    del merge_list[merge_box.curselection()[0]]
    update_merge_box()


def merge_add():
    global merge_list
    name = get_name()
    merge_list.append(name)
    update_merge_box()


def visualization_results():
    learner = get_learner(True)
    save_dir = askdirectory(title="选择保存位置")
    data = learner_controller.model_visualization(learner, save_dir)
    webbrowser.open(data[0])
    webbrowser.open(data[1])  # 还可以打开文件管理器
    update_sheet_box()


def get_learner_parameters():
    global learner_parameters
    return learner_parameters.get("0.0", tkinter.END)


def score_learner():
    learner = get_learner()
    socore = learner_controller.score(
        get_name(False, True), get_name(False, False), learner
    )
    tkinter.messagebox.showinfo("测试完成", f"针对测试数据评分结果为:{socore}")


def predict_learner():
    learner = get_learner()
    data = learner_controller.predict(get_name(False, True), learner)
    title = f"CoTan数据处理 学习器:{learner}"
    creat_text_sheet(data, title)
    update_sheet_box()


def fit_learner():
    learner = get_learner()
    try:
        split = float(data_split.get())
        if split < 0 or 1 < split:
            raise Exception
    except BaseException:
        split = 0.3
    socore = learner_controller.fit_model(
        get_name(False, True),
        get_name(False, False),
        learner,
        Text=get_learner_parameters(),
        split=split,
    )
    tkinter.messagebox.showinfo(
        "训练完成",
        f"针对训练数据({(1 - split) * 100}%)评分结果为:{socore[0]}\n"
        f"针对测试数据评分({split * 100}%)结果为:{socore[1]}",
    )


def set_x_data():
    global x_data
    x_data.set(get_name())


def set_y_data():
    global y_data
    y_data.set(get_name())


def set_learner():
    global learner_output
    learner_output.set(get_learner(True))


def get_learner(return_box=False):
    global learn_dict, learner_box, learner_output
    if return_box:
        try:
            return list(learn_dict.keys())[learner_box.curselection()[0]]
        except BaseException:
            try:
                return list(learn_dict.keys)[0]
            except BaseException:
                return get_learner(False)
    else:
        try:
            return learner_output.get()
        except BaseException:
            return None


def add_statistics():  # 添加Lenear的核心
    add_leaner("Statistics")


def add_correlation():
    add_leaner("Correlation")


def add_matrix_scatter():
    add_leaner("MatrixScatter")


def add_view_data():
    learner_controller.add_view_data(get_learner(), parameters=get_learner_parameters())
    update_leaner()


def add_cluster_tree():
    add_leaner("ClusterTree")


def add_feature_y_x():
    add_leaner("FeatureY-X")


def add_numpy_to_heatmap():
    add_leaner("HeatMap")


def add_predictive_heatmap_more():  # 添加Lenear的核心
    learner_controller.add_predictive_heat_map_more(
        get_learner(), parameters=get_learner_parameters()
    )
    update_leaner()


def add_predictive_heatmap():  # 添加Lenear的核心
    learner_controller.add_predictive_heat_map(
        get_learner(), parameters=get_learner_parameters()
    )
    update_leaner()


def add_feature_scatter_class_all():
    add_leaner("FeatureScatterClass_all")


def add_feature_scatter_all():
    add_leaner("FeatureScatter_all")


def add_feature_scatter_class():
    add_leaner("FeatureScatterClass")


def add_feature_scatter():
    add_leaner("FeatureScatter")


def add_class_bar():
    add_leaner("ClassBar")


def add_dbscan():
    add_leaner("DBSCAN")


def add_agglomerative():
    add_leaner("Agglomerative")


def add_k_means():
    add_leaner("k-means")


def add_mlp_class():
    add_leaner("MLP_class")


def add_mlp():
    add_leaner("MLP")


def add_svr():
    add_leaner("SVR")


def add_svc():
    add_leaner("SVC")


def add_gradient_tree():
    add_leaner("GradientTree")


def add_gradient_tree_class():
    add_leaner("GradientTree_class")


def add_tsne():
    add_leaner("t-SNE")


def add_nmf():
    add_leaner("NMF")


def add_lda():
    add_leaner("LDA")


def add_kpca():
    add_leaner("KPCA")


def add_rpca():
    add_leaner("RPCA")


def add_pca():
    add_leaner("PCA")


def add_missed():
    add_leaner("Missed")


def add_label():
    add_leaner("Label")


def add_one_hot_encoder():
    add_leaner("OneHotEncoder")


def add_discretization():
    add_leaner("Discretization")


def add_binarizer():
    add_leaner("Binarizer")


def add_regularization():
    add_leaner("Regularization")


def add_fuzzy_quantization():
    add_leaner("Fuzzy_quantization")


def add_mapzoom():
    add_leaner("Mapzoom")


def add_sigmod_scaler():
    add_leaner("sigmodScaler")


def add_decimal_scaler():
    add_leaner("decimalScaler")


def add_atan_scaler():
    add_leaner("atanScaler")


def add_log_scaler():
    add_leaner("LogScaler")


def add_min_max_scaler():
    add_leaner("MinMaxScaler")


def add_z_score():
    add_leaner("Z-Score")


def add_forest():
    add_leaner("Forest")


def add_forest_class():
    add_leaner("Forest_class")


def add_tree_class():
    add_leaner("Tree_class")


def add_tree():
    add_leaner("Tree")


def add_select_k_best():
    add_leaner("SelectKBest")


def add_knn_class():
    add_leaner("Knn_class")


def add_logistic_regression():
    add_leaner("LogisticRegression")


def add_lasso():
    add_leaner("Lasso")


def add_variance():
    add_leaner("Variance")


def add_knn():
    add_leaner("Knn")


def add_ridge():
    add_leaner("Ridge")


def add_line():
    add_leaner("Line")


def add_select_from_model():  # 添加Lenear的核心
    learner_controller.add_select_from_model(
        get_learner(), parameters=get_learner_parameters()
    )
    update_leaner()


def add_leaner(learner_type):  # 添加Lenear的核心
    learner_controller.add_learner(learner_type, parameters=get_learner_parameters())
    update_leaner()


def update_leaner():
    global learn_dict, learner_box
    learn_dict = learner_controller.return_learner()
    learner_box.delete(0, tkinter.END)
    learner_box.insert(tkinter.END, *learn_dict.keys())


def to_html_one():
    global PATH, to_html_type
    html_dir = f"{PATH}/$Show_Sheet.html"
    try:
        name = get_name()
        if name is None:
            raise Exception
        learner_controller.to_html_one(name, html_dir)
        webbrowser.open(html_dir)
    except BaseException:
        # pass
        raise


def to_html():
    global PATH, to_html_type
    html_dir = f"{PATH}/$Show_Sheet.html"
    try:
        name = get_name()
        if name is None:
            raise Exception
        learner_controller.to_html(name, html_dir, to_html_type.get())
        webbrowser.open(html_dir)
    except BaseException:
        pass


def to_csv():
    global SCREEN, sep, encoding, dtype_str
    save_dir = asksaveasfilename(title="选择保存的CSV", filetypes=[("CSV", ".csv")])
    csv_sep = sep.get()
    name = get_name()
    learner_controller.to_csv(save_dir, name, csv_sep)
    update_sheet_box()


def add_csv():
    global SCREEN, sep, encoding, dtype_str, sheet_name
    csv_dir = askopenfilename(title="选择载入的CSV", filetypes=[("CSV", ".csv")])
    if csv_dir == "":
        return False
    the_sep = sep.get()
    the_encoding = encoding.get()
    must_str = bool(dtype_str.get())
    name = sheet_name.get().replace(" ", "")
    if name == "":
        name = os.path.splitext(os.path.split(csv_dir)[1])[0]
    if the_encoding == "":
        with open(csv_dir, "rb") as f:
            the_encoding = chardet.detect(f.read())["encoding"]
    if the_sep == "":
        the_sep = ","
    learner_controller.read_csv(
        csv_dir, name, the_encoding, must_str, the_sep,
    )
    update_sheet_box()


def add_python():
    global SCREEN, sep, encoding, dtype_str
    python_dir = askopenfilename(
        title="选择载入的py", filetypes=[("Python", ".py"), ("Txt", ".txt")]
    )
    name = sheet_name.get().replace(" ", "")
    if name == "":
        name = os.path.splitext(os.path.split(python_dir)[1])[0]
    with open(python_dir, "r") as f:
        learner_controller.add_python(f.read(), name)
    update_sheet_box()


def get_name(get_from_box=True, is_x_data=True):  # 获得名字统一接口
    global sheet_list, sheet_box, x_data
    if get_from_box:
        try:
            return sheet_list[sheet_box.curselection()[0]]
        except BaseException:
            try:
                return sheet_list[0]
            except BaseException:
                return None
    else:
        try:
            if is_x_data:
                return x_data.get()
            else:
                return y_data.get()
        except BaseException:
            return None


def update_sheet_box():
    global SCREEN, sheet_box, sheet_list
    sheet_list = list(learner_controller.get_form().keys())
    sheet_box.delete(0, tkinter.END)
    sheet_box.insert(tkinter.END, *sheet_list)


def creat_text_sheet(data, name):
    global bg_color
    new_top = tkinter.Toplevel(bg=bg_color)
    new_top.title(name)
    new_top.geometry("+10+10")  # 设置所在位置
    text = ScrolledText(new_top, font=("黑体", 13), height=50)
    text.pack(fill=tkinter.BOTH)
    text.insert("0.0", data)
    text.config(state=tkinter.DISABLED)
    new_top.resizable(width=False, height=False)


SCREEN.title("CoTan机器学习")
SCREEN.resizable(width=False, height=False)
SCREEN.geometry("+10+10")  # 设置所在位置
tkinter.Button(
    SCREEN,
    bg=botton_color,
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
    bg=botton_color,
    fg=word_color,
    text="导入Py",
    command=add_python,
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
    bg=botton_color,
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
    bg=botton_color,
    fg=word_color,
    text="删除表格",
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
    bg=botton_color,
    fg=word_color,
    text="查看表格",
    command=to_html,
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
    bg=botton_color,
    fg=word_color,
    text="查看单一表格",
    command=to_html_one,
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

dtype_str = tkinter.IntVar()
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
    variable=dtype_str,
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
sep.grid(column=column + 1, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
sheet_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 10
)  # 显示符号
sheet_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=10,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
# 422
row += 10
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="添加数据",
    command=merge_add,
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
    bg=botton_color,
    fg=word_color,
    text="删除数据",
    command=merge_del,
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
    bg=botton_color,
    fg=word_color,
    text="组合数据",
    command=merge,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)

row += 1
merge_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 3
)  # 显示符号
merge_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=3,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 3
processing_type = tkinter.IntVar()  # 正，负，0
lable = ["横向处理", "纵向处理", "深度处理"]  # 复选框
for i in range(3):
    tkinter.Radiobutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=processing_type,
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="数据切片",
    command=two_split,
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
    bg=botton_color,
    fg=word_color,
    text="数据分割",
    command=split,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 1,
    row=row,
    columnspan=2,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)

row += 1
tkinter.Label(
    SCREEN,
    text="重塑形状:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
shape = tkinter.Entry(SCREEN, width=gui_width)
shape.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="矩阵重塑",
    command=reshape,
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
    bg=botton_color,
    fg=word_color,
    text="矩阵伸展",
    command=reval,
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
    bg=botton_color,
    fg=word_color,
    text="矩阵降维",
    command=del_ndim,
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
    bg=botton_color,
    fg=word_color,
    text="矩阵转置",
    command=transpose,
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
x_data = tkinter.StringVar()
put = tkinter.Entry(SCREEN, width=gui_width * 2, textvariable=x_data)
put.grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
put["state"] = "readonly"
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="选用X集",
    command=set_x_data,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

y_data = tkinter.StringVar()
row += 1
put = tkinter.Entry(SCREEN, width=gui_width * 2, textvariable=y_data)
put.grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
put["state"] = "readonly"
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="选用Y集",
    command=set_y_data,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

learner_output = tkinter.StringVar()
row += 1
put = tkinter.Entry(SCREEN, width=gui_width * 2, textvariable=learner_output)
put.grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
put["state"] = "readonly"
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="选用学习器",
    command=set_learner,
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
    bg=botton_color,
    fg=word_color,
    text="导入学习器",
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
    bg=botton_color,
    fg=word_color,
    text="查看数据",
    command=visualization_results,
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
    bg=botton_color,
    fg=word_color,
    text="删除学习器",
    command=del_leaner,
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
    bg=botton_color,
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
    bg=botton_color,
    fg=word_color,
    text="测试机器",
    command=score_learner,
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
    bg=botton_color,
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
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="单一变量特征选择",
    command=add_select_k_best,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column,
    row=row,
    columnspan=2,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)

tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="映射标准化",
    command=add_mapzoom,
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
    bg=botton_color,
    fg=word_color,
    text="方差特征选择",
    command=add_variance,
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
    bg=botton_color,
    fg=word_color,
    text="使用学习器筛选",
    command=add_select_from_model,
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
    bg=botton_color,
    fg=word_color,
    text="模糊量化标准化",
    command=add_fuzzy_quantization,
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
    bg=botton_color,
    fg=word_color,
    text="Z-score",
    command=add_z_score,
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
    bg=botton_color,
    fg=word_color,
    text="离差标准化",
    command=add_min_max_scaler,
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
    bg=botton_color,
    fg=word_color,
    text="Log变换",
    command=add_log_scaler,
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
    bg=botton_color,
    fg=word_color,
    text="atan变换",
    command=add_atan_scaler,
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
    bg=botton_color,
    fg=word_color,
    text="小数定标准化",
    command=add_decimal_scaler,
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
    bg=botton_color,
    fg=word_color,
    text="Sigmod变换",
    command=add_sigmod_scaler,
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
    bg=botton_color,
    fg=word_color,
    text="正则化",
    command=add_regularization,
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
    bg=botton_color,
    fg=word_color,
    text="二值离散",
    command=add_binarizer,
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
    bg=botton_color,
    fg=word_color,
    text="多值离散",
    command=add_discretization,
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
    bg=botton_color,
    fg=word_color,
    text="独热编码",
    command=add_one_hot_encoder,
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
    bg=botton_color,
    fg=word_color,
    text="数字编码",
    command=add_label,
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
    bg=botton_color,
    fg=word_color,
    text="缺失填充",
    command=add_missed,
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
    bg=botton_color,
    fg=word_color,
    text="PCA降维",
    command=add_pca,
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
    bg=botton_color,
    fg=word_color,
    text="RPCA降维",
    command=add_rpca,
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
    bg=botton_color,
    fg=word_color,
    text="KPCA升维",
    command=add_kpca,
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
    bg=botton_color,
    fg=word_color,
    text="LDA降维",
    command=add_lda,
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
    bg=botton_color,
    fg=word_color,
    text="NMF降维",
    command=add_nmf,
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
    bg=botton_color,
    fg=word_color,
    text="t-SNE",
    command=add_tsne,
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
    bg=botton_color,
    fg=word_color,
    text="线性回归",
    command=add_line,
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
    bg=botton_color,
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
    bg=botton_color,
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
    bg=botton_color,
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
    bg=botton_color,
    fg=word_color,
    text="K邻近预测",
    command=add_knn,
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
    bg=botton_color,
    fg=word_color,
    text="K邻近分类",
    command=add_knn_class,
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
    bg=botton_color,
    fg=word_color,
    text="梯度回归树回归",
    command=add_gradient_tree,
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
    bg=botton_color,
    fg=word_color,
    text="决策树回归",
    command=add_tree,
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
    bg=botton_color,
    fg=word_color,
    text="决策树分类",
    command=add_tree_class,
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
    bg=botton_color,
    fg=word_color,
    text="梯度回归树分类",
    command=add_gradient_tree_class,
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
    bg=botton_color,
    fg=word_color,
    text="随机森林回归",
    command=add_forest,
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
    bg=botton_color,
    fg=word_color,
    text="随机森林分类",
    command=add_forest_class,
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

tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="多层感知机回归",
    command=add_mlp,
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
    bg=botton_color,
    fg=word_color,
    text="多层感知机分类",
    command=add_mlp_class,
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
    bg=botton_color,
    fg=word_color,
    text="随机森林分类",
    command=add_forest_class,
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
    bg=botton_color,
    fg=word_color,
    text="支持向量机分类:SVC",
    command=add_svc,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column,
    row=row,
    columnspan=2,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="回归:SVR",
    command=add_svr,
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
    bg=botton_color,
    fg=word_color,
    text="k-means",
    command=add_k_means,
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
    bg=botton_color,
    fg=word_color,
    text="凝聚聚类",
    command=add_agglomerative,
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
    bg=botton_color,
    fg=word_color,
    text="DBSCAN",
    command=add_dbscan,
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
    bg=botton_color,
    fg=word_color,
    text="特征分类图",
    command=add_class_bar,
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
    bg=botton_color,
    fg=word_color,
    text="临近特征回归图",
    command=add_feature_scatter,
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
    bg=botton_color,
    fg=word_color,
    text="临近特征分类图",
    command=add_feature_scatter_class,
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
    bg=botton_color,
    fg=word_color,
    text="所有特征回归图",
    command=add_feature_scatter_all,
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
    bg=botton_color,
    fg=word_color,
    text="所有特征分类图",
    command=add_feature_scatter_class_all,
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
    bg=botton_color,
    fg=word_color,
    text="临近特征预测图",
    command=add_predictive_heatmap,
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
    bg=botton_color,
    fg=word_color,
    text="所有特征预测图",
    command=add_predictive_heatmap_more,
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
    bg=botton_color,
    fg=word_color,
    text="矩阵热力图",
    command=add_numpy_to_heatmap,
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
    bg=botton_color,
    fg=word_color,
    text="数据y-x散点图",
    command=add_feature_y_x,
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
    bg=botton_color,
    fg=word_color,
    text="聚类树状图",
    command=add_cluster_tree,
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
    bg=botton_color,
    fg=word_color,
    text="获取数据",
    command=add_view_data,
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
    bg=botton_color,
    fg=word_color,
    text="矩阵散点图",
    command=add_matrix_scatter,
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
    bg=botton_color,
    fg=word_color,
    text="特征相关性",
    command=add_correlation,
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
    bg=botton_color,
    fg=word_color,
    text="曲线拟合",
    command=curve_fitting,
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
    bg=botton_color,
    fg=word_color,
    text="快速傅里叶",
    command=add_fast_fourier,
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
    bg=botton_color,
    fg=word_color,
    text="数据统计",
    command=add_statistics,
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
    bg=botton_color,
    fg=word_color,
    text="双逆向傅里叶",
    command=add_reverse_fast_fourier2,
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
    bg=botton_color,
    fg=word_color,
    text="逆向傅里叶",
    command=add_reverse_fast_fourier,
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
    bg=botton_color,
    fg=word_color,
    text="分类模型评估",
    command=show_class_score,
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
    bg=botton_color,
    fg=word_color,
    text="回归模型评估",
    command=show_regression_score,
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
    bg=botton_color,
    fg=word_color,
    text="聚类模型评估",
    command=show_clustering_score,
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
    text="【学习器配置】",
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
global_settings = []
lable = ["聚类仅邻近特征", "导出单独页面", "导出表格CSV"]  # 复选框
for i in range(3):
    global_settings.append(tkinter.IntVar())
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=global_settings[-1],
        command=global_seeting,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

row += 1
lable = ["导出模型", "压缩为tar.gz", "创建新目录"]  # 复选框
for i in range(3):
    global_settings.append(tkinter.IntVar())
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=global_settings[-1],
        command=global_seeting,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

for i in global_settings[1:]:
    i.set(1)
global_seeting()

row += 1
learner_parameters = tkinter.Text(
    SCREEN, width=gui_width * 3, height=gui_height * 6
)
learner_parameters.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=6,
    sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
)

row += 6
tkinter.Label(
    SCREEN,
    text="【矩阵运算】",
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
calculation_box = tkinter.Listbox(
    SCREEN, width=gui_width * 3, height=gui_height * 1
)
calculation_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=1,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 1
tkinter.Label(
    SCREEN,
    text="运算类型:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
calculation_type = tkinter.Entry(SCREEN, width=gui_width * 2)
calculation_type.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="键入参数:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
value = tkinter.Entry(SCREEN, width=gui_width * 2)
value.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="选择参数",
    command=add_calculation_object,
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
    bg=botton_color,
    fg=word_color,
    text="键入参数",
    command=add_calculation_number,
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
    bg=botton_color,
    fg=word_color,
    text="矩阵运算",
    command=calculation,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)
