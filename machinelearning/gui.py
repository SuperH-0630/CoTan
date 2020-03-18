import os
import tkinter
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
from newtkinter import askopenfilename, asksaveasfilename, askdirectory
import chardet
import webbrowser

import machinelearning.controller
import machinelearning.template
from system import exception_catch

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
learn_dict = {}


class UIAPI:
    @staticmethod
    @exception_catch()
    def get_split_shape_list_gui():
        try:
            split_shape_list = eval(f"[{shape.get()}]", {})[0]
        except IndexError:
            split_shape_list = 2
        return split_shape_list

    @staticmethod
    @exception_catch()
    def get_reval_type_gui():
        return processing_type.get()

    @staticmethod
    @exception_catch()
    def update_sheet_box_gui():
        global SCREEN, sheet_box, sheet_list
        sheet_list = list(learner_controller.get_form().keys())
        sheet_box.delete(0, tkinter.END)
        sheet_box.insert(tkinter.END, *sheet_list)

    @staticmethod
    @exception_catch()
    def creat_text_sheet_gui(data, name):
        global bg_color
        new_top = tkinter.Toplevel(bg=bg_color)
        new_top.title(name)
        new_top.geometry("+10+10")  # 设置所在位置
        text = ScrolledText(new_top, font=("黑体", 13), height=50)
        text.pack(fill=tkinter.BOTH)
        text.insert("0.0", data)
        text.config(state=tkinter.DISABLED)
        new_top.resizable(width=False, height=False)

    @staticmethod
    @exception_catch()
    def add_python_gui():
        python_dir = askopenfilename(
            title="选择载入的py", filetypes=[("Python", ".py"), ("Txt", ".txt")]
        )
        name = sheet_name.get().replace(" ", "")
        if name == "":
            name = os.path.splitext(os.path.split(python_dir)[1])[0]
        with open(python_dir, "r") as f:
            code = f.read()
        return code, name

    @staticmethod
    @exception_catch()
    def get_data_name_gui(get_from_box=True, is_x_data=True):  # 获得名字统一接口
        global sheet_list, sheet_box, x_data
        if get_from_box:
            try:
                return sheet_list[sheet_box.curselection()[0]]
            except IndexError:
                try:
                    return sheet_list[0]
                except IndexError:
                    return None
        else:
            if is_x_data:
                return x_data.get()
            else:
                return y_data.get()

    @staticmethod
    @exception_catch()
    def add_csv_gui():
        csv_dir = askopenfilename(title="选择载入的CSV", filetypes=[("CSV", ".csv")])
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
        return csv_dir, name, the_encoding, must_str, the_sep

    @staticmethod
    @exception_catch()
    def to_csv_gui():
        save_dir = asksaveasfilename(title="选择保存的CSV", filetypes=[("CSV", ".csv")])
        csv_sep = sep.get()
        name = API.get_data_name_gui()
        return save_dir, name, csv_sep

    @staticmethod
    @exception_catch()
    def update_leaner_gui():
        global learn_dict, learner_box
        learn_dict = learner_controller.return_learner()
        learner_box.delete(0, tkinter.END)
        learner_box.insert(tkinter.END, *learn_dict.keys())

    @staticmethod
    @exception_catch()
    def set_x_data_gui():
        global x_data
        x_data.set(API.get_data_name_gui())

    @staticmethod
    @exception_catch()
    def set_y_data_gui():
        global y_data
        y_data.set(API.get_data_name_gui())

    @staticmethod
    @exception_catch()
    def set_learner_gui():
        global learner_output
        learner_output.set(API.get_learner_gui(True))

    @staticmethod
    @exception_catch()
    def get_learner_gui(return_box=False):
        global learn_dict, learner_box, learner_output
        if return_box:
            try:
                return list(learn_dict.keys())[learner_box.curselection()[0]]
            except IndexError:
                try:
                    return list(learn_dict.keys)[0]
                except IndexError:
                    return API.get_learner_gui(False)
        else:
            return learner_output.get()

    @staticmethod
    @exception_catch()
    def show_score_gui(message):
        tkinter.messagebox.showinfo("完成", message)

    @staticmethod
    @exception_catch()
    def get_learner_parameters_gui():
        global learner_parameters
        return learner_parameters.get("0.0", tkinter.END)

    @staticmethod
    @exception_catch()
    def get_merge_box_index_gui():
        return merge_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def update_merge_box_gui():
        global merge_list, merge_box
        merge_box.delete(0, tkinter.END)
        merge_box.insert(tkinter.END, *merge_list)

    @staticmethod
    @exception_catch()
    def get_merge_split_type_gui():
        return processing_type.get()

    @staticmethod
    @exception_catch()
    def get_shape_gui():
        return eval(f"[{shape.get()}]")[0]

    @staticmethod
    @exception_catch()
    def global_settings_gui():
        return [bool(i.get()) for i in global_settings]

    @staticmethod
    @exception_catch()
    def get_calculation_num_gui():
        return eval(value.get(), {})

    @staticmethod
    @exception_catch()
    def update_calculation_box_gui():
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

    @staticmethod
    @exception_catch()
    def get_calculation_type_gui():
        return calculation_type.get()


class API(UIAPI):
    @staticmethod
    @exception_catch()
    def add_reverse_fast_fourier2():  # 添加Lenear的核心
        API.add_leaner("[2]Reverse_Fast_Fourier")

    @staticmethod
    @exception_catch()
    def add_reverse_fast_fourier():  # 添加Lenear的核心
        API.add_leaner("Reverse_Fast_Fourier")

    @staticmethod
    @exception_catch()
    def add_fast_fourier():  # 添加Lenear的核心
        API.add_leaner("Fast_Fourier")

    @staticmethod
    @exception_catch()
    def curve_fitting():
        file_dir = askopenfilename(title="导入参数")
        with open(file_dir, "r") as f:
            learner_controller.add_curve_fitting(f.read())
            API.update_leaner_gui()

    @staticmethod
    @exception_catch()
    def show_clustering_score():
        API.show_score(2)

    @staticmethod
    @exception_catch()
    def show_regression_score():
        API.show_score(1)

    @staticmethod
    @exception_catch()
    def show_class_score():
        API.show_score(0)

    @staticmethod
    @exception_catch()
    def show_score(func):
        learner = API.get_learner_gui(True)
        save_dir = askdirectory(title="选择保存位置")
        data = learner_controller.model_evaluation(
            learner,
            save_dir,
            API.get_data_name_gui(False, True),
            API.get_data_name_gui(False, False),
            func,
        )
        webbrowser.open(data[0])
        webbrowser.open(data[1])  # 还可以打开文件管理器
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def calculation():
        global calculation_list, calculation_method
        func = API.get_calculation_type_gui()
        if len(calculation_list) == 2 and 1 in calculation_method:
            learner_controller.calculation_matrix(
                calculation_list, calculation_method, func
            )
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def add_calculation_core(num, type_):
        if len(calculation_list) == 2:
            del calculation_list[0]
            del calculation_method[0]
        calculation_list.append(num)
        calculation_method.append(type_)

    @staticmethod
    @exception_catch()
    def add_calculation_number():
        API.add_calculation_core(API.get_calculation_num_gui(), 0)
        API.update_calculation_box_gui()

    @staticmethod
    @exception_catch()
    def add_calculation_object():
        name = API.get_data_name_gui()
        API.add_calculation_core(name, 1)
        API.update_calculation_box_gui()

    @staticmethod
    @exception_catch()
    def del_leaner():
        learn = API.get_learner_gui(True)
        set_learne = API.get_learner_gui(False)  # 获取学习器Learner
        if set_learne != learn:
            learner_controller.del_leaner(learn)
        API.update_leaner_gui()

    @staticmethod
    @exception_catch()
    def global_seeting():
        args = API.global_settings_gui()
        machinelearning.template.set_global(*args)

    @staticmethod
    @exception_catch()
    def reshape():
        numpy_shape = API.get_shape_gui()
        learner_controller.reshape(API.get_data_name_gui(), numpy_shape)
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def transpose():
        try:
            func = API.get_shape_gui()
        except AssertionError:
            func = None
        learner_controller.transpose(API.get_data_name_gui(), func)
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def del_ndim():
        learner_controller.del_ndim(API.get_data_name_gui())
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def reval():
        global learner_controller
        reval_type = API.get_reval_type_gui()
        learner_controller.reval(API.get_data_name_gui(), reval_type)
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def two_split():
        split_type = API.get_merge_split_type_gui()
        learner_controller.two_split(API.get_data_name_gui(), shape.get(), split_type)
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def split():
        global learner_controller, shape
        split_type = API.get_merge_split_type_gui()
        split_shape_list = API.get_split_shape_list_gui()
        learner_controller.split(API.get_data_name_gui(), split_shape_list, split_type)
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def merge():
        if len(merge_list) < 1:
            return False
        merge_type = API.get_merge_split_type_gui()
        learner_controller.merge(merge_list, merge_type)
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def merge_del():
        del merge_list[API.get_merge_box_index_gui()]
        API.update_merge_box_gui()

    @staticmethod
    @exception_catch()
    def merge_add():
        merge_list.append(API.get_data_name_gui())
        API.update_merge_box_gui()

    @staticmethod
    @exception_catch()
    def visualization_results():
        learner = API.get_learner_gui(True)
        save_dir = askdirectory(title="选择保存位置")
        data = learner_controller.model_visualization(learner, save_dir)
        webbrowser.open(data[0])
        webbrowser.open(data[1])  # 还可以打开文件管理器
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def score_learner():
        learner = API.get_learner_gui()
        score = learner_controller.score(
            API.get_data_name_gui(False, True), API.get_data_name_gui(False, False), learner
        )
        API.show_score_gui(f"针对测试数据评分结果为:{score}")

    @staticmethod
    @exception_catch()
    def predict_learner():
        learner = API.get_learner_gui()
        data = learner_controller.predict(API.get_data_name_gui(False, True), learner)
        title = f"CoTan数据处理 学习器:{learner}"
        API.creat_text_sheet_gui(data, title)
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def fit_learner():
        learner = API.get_learner_gui()
        try:
            split = float(data_split.get())
            assert split < 0 or 1 < split
        except (AssertionError, ValueError):
            split = 0.3
        socore = learner_controller.fit_model(
            API.get_data_name_gui(False, True),
            API.get_data_name_gui(False, False),
            learner,
            Text=API.get_learner_parameters_gui(),
            split=split,
        )
        API.show_score_gui(
            f"针对训练数据({(1 - split) * 100}%)评分结果为:{socore[0]}\n"
            f"针对测试数据评分({split * 100}%)结果为:{socore[1]}",
        )

    @staticmethod
    @exception_catch()
    def add_statistics():  # 添加Lenear的核心
        API.add_leaner("Statistics")

    @staticmethod
    @exception_catch()
    def add_correlation():
        API.add_leaner("Correlation")

    @staticmethod
    @exception_catch()
    def add_matrix_scatter():
        API.add_leaner("MatrixScatter")

    @staticmethod
    @exception_catch()
    def add_view_data():
        learner_controller.add_view_data(
            API.get_learner_gui(), parameters=API.get_learner_parameters_gui()
        )
        API.update_leaner_gui()

    @staticmethod
    @exception_catch()
    def add_cluster_tree():
        API.add_leaner("ClusterTree")

    @staticmethod
    @exception_catch()
    def add_feature_y_x():
        API.add_leaner("FeatureY-X")

    @staticmethod
    @exception_catch()
    def add_numpy_to_heatmap():
        API.add_leaner("HeatMap")

    @staticmethod
    @exception_catch()
    def add_predictive_heatmap_more():  # 添加Lenear的核心
        learner_controller.add_predictive_heat_map_more(
            API.get_learner_gui(), parameters=API.get_learner_parameters_gui()
        )
        API.update_leaner_gui()

    @staticmethod
    @exception_catch()
    def add_predictive_heatmap():  # 添加Lenear的核心
        learner_controller.add_predictive_heat_map(
            API.get_learner_gui(), parameters=API.get_learner_parameters_gui()
        )
        API.update_leaner_gui()

    @staticmethod
    @exception_catch()
    def add_feature_scatter_class_all():
        API.add_leaner("FeatureScatterClass_all")

    @staticmethod
    @exception_catch()
    def add_feature_scatter_all():
        API.add_leaner("FeatureScatter_all")

    @staticmethod
    @exception_catch()
    def add_feature_scatter_class():
        API.add_leaner("FeatureScatterClass")

    @staticmethod
    @exception_catch()
    def add_feature_scatter():
        API.add_leaner("FeatureScatter")

    @staticmethod
    @exception_catch()
    def add_class_bar():
        API.add_leaner("ClassBar")

    @staticmethod
    @exception_catch()
    def add_dbscan():
        API.add_leaner("DBSCAN")

    @staticmethod
    @exception_catch()
    def add_agglomerative():
        API.add_leaner("Agglomerative")

    @staticmethod
    @exception_catch()
    def add_k_means():
        API.add_leaner("k-means")

    @staticmethod
    @exception_catch()
    def add_mlp_class():
        API.add_leaner("MLP_class")

    @staticmethod
    @exception_catch()
    def add_mlp():
        API.add_leaner("MLP")

    @staticmethod
    @exception_catch()
    def add_svr():
        API.add_leaner("SVR")

    @staticmethod
    @exception_catch()
    def add_svc():
        API.add_leaner("SVC")

    @staticmethod
    @exception_catch()
    def add_gradient_tree():
        API.add_leaner("GradientTree")

    @staticmethod
    @exception_catch()
    def add_gradient_tree_class():
        API.add_leaner("GradientTree_class")

    @staticmethod
    @exception_catch()
    def add_tsne():
        API.add_leaner("t-SNE")

    @staticmethod
    @exception_catch()
    def add_nmf():
        API.add_leaner("NMF")

    @staticmethod
    @exception_catch()
    def add_lda():
        API.add_leaner("LDA")

    @staticmethod
    @exception_catch()
    def add_kpca():
        API.add_leaner("KPCA")

    @staticmethod
    @exception_catch()
    def add_rpca():
        API.add_leaner("RPCA")

    @staticmethod
    @exception_catch()
    def add_pca():
        API.add_leaner("PCA")

    @staticmethod
    @exception_catch()
    def add_missed():
        API.add_leaner("Missed")

    @staticmethod
    @exception_catch()
    def add_label():
        API.add_leaner("Label")

    @staticmethod
    @exception_catch()
    def add_one_hot_encoder():
        API.add_leaner("OneHotEncoder")

    @staticmethod
    @exception_catch()
    def add_discretization():
        API.add_leaner("Discretization")

    @staticmethod
    @exception_catch()
    def add_binarizer():
        API.add_leaner("Binarizer")

    @staticmethod
    @exception_catch()
    def add_regularization():
        API.add_leaner("Regularization")

    @staticmethod
    @exception_catch()
    def add_fuzzy_quantization():
        API.add_leaner("Fuzzy_quantization")

    @staticmethod
    @exception_catch()
    def add_mapzoom():
        API.add_leaner("Mapzoom")

    @staticmethod
    @exception_catch()
    def add_sigmod_scaler():
        API.add_leaner("sigmodScaler")

    @staticmethod
    @exception_catch()
    def add_decimal_scaler():
        API.add_leaner("decimalScaler")

    @staticmethod
    @exception_catch()
    def add_atan_scaler():
        API.add_leaner("atanScaler")

    @staticmethod
    @exception_catch()
    def add_log_scaler():
        API.add_leaner("LogScaler")

    @staticmethod
    @exception_catch()
    def add_min_max_scaler():
        API.add_leaner("MinMaxScaler")

    @staticmethod
    @exception_catch()
    def add_z_score():
        API.add_leaner("Z-Score")

    @staticmethod
    @exception_catch()
    def add_forest():
        API.add_leaner("Forest")

    @staticmethod
    @exception_catch()
    def add_forest_class():
        API.add_leaner("Forest_class")

    @staticmethod
    @exception_catch()
    def add_tree_class():
        API.add_leaner("Tree_class")

    @staticmethod
    @exception_catch()
    def add_tree():
        API.add_leaner("Tree")

    @staticmethod
    @exception_catch()
    def add_select_k_best():
        API.add_leaner("SelectKBest")

    @staticmethod
    @exception_catch()
    def add_knn_class():
        API.add_leaner("Knn_class")

    @staticmethod
    @exception_catch()
    def add_logistic_regression():
        API.add_leaner("LogisticRegression")

    @staticmethod
    @exception_catch()
    def add_lasso():
        API.add_leaner("Lasso")

    @staticmethod
    @exception_catch()
    def add_variance():
        API.add_leaner("Variance")

    @staticmethod
    @exception_catch()
    def add_knn():
        API.add_leaner("Knn")

    @staticmethod
    @exception_catch()
    def add_ridge():
        API.add_leaner("Ridge")

    @staticmethod
    @exception_catch()
    def add_line():
        API.add_leaner("Line")

    @staticmethod
    @exception_catch()
    def add_select_from_model():  # 添加Lenear的核心
        learner_controller.add_select_from_model(
            API.get_learner_gui(), parameters=API.get_learner_parameters_gui()
        )
        API.update_leaner_gui()

    @staticmethod
    @exception_catch()
    def add_leaner(learner_type):  # 添加Lenear的核心
        learner_controller.add_learner(
            learner_type, parameters=API.get_learner_parameters_gui()
        )
        API.update_leaner_gui()

    @staticmethod
    @exception_catch()
    def to_html_one():
        html_dir = f"{PATH}{os.sep}$Show_Sheet.html"
        name = API.get_data_name_gui()
        assert name is None
        learner_controller.to_html_one(name, html_dir)
        webbrowser.open(html_dir)

    @staticmethod
    @exception_catch()
    def to_html():
        html_dir = f"{PATH}{os.sep}$Show_Sheet.html"
        name = API.get_data_name_gui()
        assert name is None
        learner_controller.to_html(name, html_dir, to_html_type.get())
        webbrowser.open(html_dir)

    @staticmethod
    @exception_catch()
    def to_csv():
        learner_controller.to_csv(*API.to_csv_gui())
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def add_csv():
        learner_controller.read_csv(*API.add_csv_gui())
        API.update_sheet_box_gui()

    @staticmethod
    @exception_catch()
    def add_python():
        code, name = API.add_python_gui()
        learner_controller.add_python(code, name)
        API.update_sheet_box_gui()


def machine_learning():
    global SCREEN
    SCREEN.mainloop()


SCREEN.title("CoTan机器学习")
SCREEN.resizable(width=False, height=False)
SCREEN.geometry("+10+10")  # 设置所在位置
tkinter.Button(
    SCREEN,
    bg=botton_color,
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
    bg=botton_color,
    fg=word_color,
    text="导入Py",
    command=API.add_python,
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
    command=API.to_html,
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
    command=API.to_html_one,
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
sheet_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 10)  # 显示符号
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
    command=API.merge_add,
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
    command=API.merge_del,
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
    command=API.merge,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)

row += 1
merge_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 3)  # 显示符号
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
    command=API.two_split,
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
    command=API.split,
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
    command=API.reshape,
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
    command=API.reval,
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
    command=API.del_ndim,
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
    command=API.transpose,
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
    command=API.set_x_data_gui,
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
    command=API.set_y_data_gui,
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
    command=API.visualization_results,
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
    command=API.del_leaner,
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
    bg=botton_color,
    fg=word_color,
    text="测试机器",
    command=API.score_learner,
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
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="单一变量特征选择",
    command=API.add_select_k_best,
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
    command=API.add_mapzoom,
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
    command=API.add_variance,
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
    command=API.add_select_from_model,
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
    command=API.add_fuzzy_quantization,
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
    command=API.add_z_score,
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
    command=API.add_min_max_scaler,
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
    command=API.add_log_scaler,
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
    command=API.add_atan_scaler,
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
    command=API.add_decimal_scaler,
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
    command=API.add_sigmod_scaler,
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
    command=API.add_regularization,
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
    command=API.add_binarizer,
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
    command=API.add_discretization,
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
    command=API.add_one_hot_encoder,
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
    command=API.add_label,
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
    command=API.add_missed,
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
    command=API.add_pca,
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
    command=API.add_rpca,
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
    command=API.add_kpca,
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
    command=API.add_lda,
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
    command=API.add_nmf,
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
    command=API.add_tsne,
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
    command=API.add_line,
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
    bg=botton_color,
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
    bg=botton_color,
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
    bg=botton_color,
    fg=word_color,
    text="K邻近预测",
    command=API.add_knn,
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
tkinter.Button(
    SCREEN,
    bg=botton_color,
    fg=word_color,
    text="梯度回归树回归",
    command=API.add_gradient_tree,
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
    command=API.add_tree,
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
    command=API.add_tree_class,
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
    command=API.add_gradient_tree_class,
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
    command=API.add_forest,
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
    command=API.add_forest_class,
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
    command=API.add_mlp,
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
    command=API.add_mlp_class,
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
    command=API.add_forest_class,
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
    command=API.add_svc,
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
    command=API.add_svr,
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
    command=API.add_k_means,
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
    command=API.add_agglomerative,
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
    command=API.add_dbscan,
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
    command=API.add_class_bar,
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
    command=API.add_feature_scatter,
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
    command=API.add_feature_scatter_class,
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
    command=API.add_feature_scatter_all,
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
    command=API.add_feature_scatter_class_all,
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
    command=API.add_predictive_heatmap,
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
    command=API.add_predictive_heatmap_more,
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
    command=API.add_numpy_to_heatmap,
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
    command=API.add_feature_y_x,
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
    command=API.add_cluster_tree,
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
    command=API.add_view_data,
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
    command=API.add_matrix_scatter,
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
    command=API.add_correlation,
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
    command=API.curve_fitting,
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
    command=API.add_fast_fourier,
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
    command=API.add_statistics,
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
    command=API.add_reverse_fast_fourier2,
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
    command=API.add_reverse_fast_fourier,
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
    command=API.show_class_score,
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
    command=API.show_regression_score,
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
    command=API.show_clustering_score,
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
        command=API.global_seeting,
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
        command=API.global_seeting,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

for i in global_settings[1:]:
    i.set(1)
API.global_seeting()

row += 1
learner_parameters = tkinter.Text(SCREEN, width=gui_width * 3, height=gui_height * 6)
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
calculation_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 1)
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
    command=API.add_calculation_object,
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
    command=API.add_calculation_number,
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
    command=API.calculation,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 2,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)
