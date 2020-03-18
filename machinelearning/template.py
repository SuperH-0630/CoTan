import joblib
import re
import tarfile
from abc import ABCMeta, abstractmethod
from os import getcwd, mkdir
from os.path import split as path_split, splitext, basename, exists
import os
import logging

from sklearn.svm import SVC, SVR  # SVC是svm分类，SVR是svm回归
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.manifold import TSNE
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as Lda
from sklearn.decomposition import PCA, IncrementalPCA, KernelPCA, NMF
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import *
from sklearn.feature_selection import *
from sklearn.metrics import *
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
)
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_graphviz
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.linear_model import *
from sklearn.model_selection import train_test_split
from scipy.fftpack import fft, ifft  # 快速傅里叶变换
from scipy import optimize
from scipy.cluster.hierarchy import dendrogram, ward
from pyecharts.components import Table as TableFisrt  # 绘制表格
from pyecharts.options.series_options import JsCode
from pyecharts.charts import Tab as tab_First
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.components import Image
from pyecharts.globals import CurrentConfig

from system import plugin_class_loading, get_path, plugin_func_loading, basicConfig

logging.basicConfig(**basicConfig)
CurrentConfig.ONLINE_HOST = f"{getcwd()}{os.sep}assets{os.sep}"


# 设置
np.set_printoptions(threshold=np.inf)
global_setting = dict(
    toolbox_opts=opts.ToolboxOpts(is_show=True),
    legend_opts=opts.LegendOpts(pos_bottom="3%", type_="scroll"),
)
global_not_legend = dict(
    toolbox_opts=opts.ToolboxOpts(is_show=True),
    legend_opts=opts.LegendOpts(is_show=False),
)
label_setting = dict(label_opts=opts.LabelOpts(is_show=False))

more_global = False  # 是否使用全部特征绘图
all_global = True  # 是否导出charts
csv_global = True  # 是否导出CSV
clf_global = True  # 是否导出模型
tar_global = True  # 是否打包tar
new_dir_global = True  # 是否新建目录


class LearnBase(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.numpy_dict = {}  # name:numpy
        self.fucn_add()  # 制作Func_Dic

    def fucn_add(self):
        self.func_dict = {
            "abs": lambda x, y: np.abs(x),
            "sqrt": lambda x, y: np.sqrt(x),
            "pow": lambda x, y: x ** y,
            "loge": lambda x, y: np.log(x),
            "log10": lambda x, y: np.log10(x),
            "ceil": lambda x, y: np.ceil(x),
            "floor": lambda x, y: np.floor(x),
            "rint": lambda x, y: np.rint(x),
            "sin": lambda x, y: np.sin(x),
            "cos": lambda x, y: np.cos(x),
            "tan": lambda x, y: np.tan(x),
            "tanh": lambda x, y: np.tanh(x),
            "sinh": lambda x, y: np.sinh(x),
            "cosh": lambda x, y: np.cosh(x),
            "asin": lambda x, y: np.arcsin(x),
            "acos": lambda x, y: np.arccos(x),
            "atan": lambda x, y: np.arctan(x),
            "atanh": lambda x, y: np.arctanh(x),
            "asinh": lambda x, y: np.arcsinh(x),
            "acosh": lambda x, y: np.arccosh(x),
            "add": lambda x, y: x + y,  # 矩阵或元素
            "sub": lambda x, y: x - y,  # 矩阵或元素
            "mul": lambda x, y: np.multiply(x, y),  # 元素级别
            "matmul": lambda x, y: np.matmul(x, y),  # 矩阵
            "dot": lambda x, y: np.dot(x, y),  # 矩阵
            "div": lambda x, y: x / y,
            "div_floor": lambda x, y: np.floor_divide(x, y),
            "power": lambda x, y: np.power(x, y),  # 元素级
        }

    def get_form(self) -> dict:
        return self.numpy_dict.copy()

    def get_sheet(self, name) -> np.ndarray:
        return self.numpy_dict[name].copy()

    @abstractmethod
    def add_form(self, data, name):
        pass


@plugin_class_loading(get_path(r"template/machinelearning"))
class LearnerIO(LearnBase):
    def add_form(self, data: np.array, name):
        name = f"{name}[{len(self.numpy_dict)}]"
        self.numpy_dict[name] = data

    def read_csv(
            self,
            file_dir,
            name,
            encoding="utf-8",
            str_must=False,
            sep=","):
        dtype = np.str if str_must else np.float
        dataframe = read_csv(
            file_dir,
            encoding=encoding,
            delimiter=sep,
            header=None)
        try:
            data = dataframe.to_numpy(dtype=dtype)
        except ValueError:
            data = dataframe.to_numpy(dtype=np.str)
        if data.ndim == 1:
            data = np.expand_dims(data, axis=1)
        self.add_form(data, name)
        return data

    def add_python(self, python_file, sheet_name):
        name = {}
        name.update(globals().copy())
        name.update(locals().copy())
        exec(python_file, name)
        exec("get = Creat()", name)
        if isinstance(name["get"], np.array):
            get = name["get"]
        else:
            get = np.array(name["get"])
        self.add_form(get, sheet_name)
        return get

    def to_csv(self, save_dir: str, name, sep) -> str:
        get: np.ndarray = self.get_sheet(name)
        np.savetxt(save_dir, get, delimiter=sep)
        return save_dir

    def to_html_one(self, name, html_dir=""):
        if html_dir == "":
            html_dir = f"{name}.html"
        get: np.ndarray = self.get_sheet(name)
        if get.ndim == 1:
            get = np.expand_dims(get, axis=1)
        get: list = get.tolist()
        for i in range(len(get)):
            get[i] = [i + 1] + get[i]
        headers = [i for i in range(len(get[0]))]
        table = TableFisrt()
        table.add(headers, get).set_global_opts(
            title_opts=opts.ComponentTitleOpts(
                title=f"表格:{name}", subtitle="CoTan~机器学习:查看数据"
            )
        )
        table.render(html_dir)
        return html_dir

    def to_html(self, name, html_dir="", html_type=0):
        if html_dir == "":
            html_dir = f"{name}.html"
        # 把要画的sheet放到第一个
        sheet_dict = self.get_form()
        del sheet_dict[name]
        sheet_list = [name] + list(sheet_dict.keys())

        class TabBase:
            def __init__(self, q):
                self.tab = q  # 一个Tab

            def render(self, render_dir):
                return self.tab.render(render_dir)

        # 生成一个显示页面
        if html_type == 0:

            class NewTab(TabBase):
                def add(self, table_, k, *f):
                    self.tab.add(table_, k)

            tab = NewTab(tab_First(page_title="CoTan:查看表格"))  # 一个Tab
        elif html_type == 1:

            class NewTab(TabBase):
                def add(self, table_, *k):
                    self.tab.add(table_)

            tab = NewTab(
                Page(
                    page_title="CoTan:查看表格",
                    layout=Page.DraggablePageLayout))
        else:

            class NewTab(TabBase):
                def add(self, table_, *k):
                    self.tab.add(table_)

            tab = NewTab(
                Page(
                    page_title="CoTan:查看表格",
                    layout=Page.SimplePageLayout))
        # 迭代添加内容
        for name in sheet_list:
            get: np.ndarray = self.get_sheet(name)
            if get.ndim == 1:
                get = np.expand_dims(get, axis=1)
            get: list = get.tolist()
            for i in range(len(get)):
                get[i] = [i + 1] + get[i]
            headers = [i for i in range(len(get[0]))]
            table = TableFisrt()
            table.add(headers, get).set_global_opts(
                title_opts=opts.ComponentTitleOpts(
                    title=f"表格:{name}", subtitle="CoTan~机器学习:查看数据"
                )
            )
            tab.add(table, f"表格:{name}")
        tab.render(html_dir)
        return html_dir


@plugin_class_loading(get_path(r"template/machinelearning"))
class LearnerMerge(LearnBase, metaclass=ABCMeta):
    def merge(self, name, axis=0):  # aiis:0-横向合并(hstack),1-纵向合并(vstack)，2-深度合并
        sheet_list = []
        for i in name:
            sheet_list.append(self.get_sheet(i))
        get = {0: np.hstack, 1: np.vstack, 2: np.dstack}[axis](sheet_list)
        self.add_form(np.array(get), f"{name[0]}合成")


@plugin_class_loading(get_path(r"template/machinelearning"))
class LearnerSplit(LearnBase, metaclass=ABCMeta):
    def split(self, name, split=2, axis=0):  # aiis:0-横向分割(hsplit),1-纵向分割(vsplit)
        sheet = self.get_sheet(name)
        get = {0: np.hsplit, 1: np.vsplit, 2: np.dsplit}[axis](sheet, split)
        for i in get:
            self.add_form(i, f"{name[0]}分割")

    def two_split(self, name, split, axis):  # 二分切割(0-横向，1-纵向)
        sheet = self.get_sheet(name)
        try:
            split = float(eval(split))
            if split < 1:
                split = int(split * len(sheet) if axis == 1 else len(sheet[0]))
            else:
                assert True
        except (ValueError, AssertionError):
            split = int(split)
        if axis == 0:
            self.add_form(sheet[:, split:], f"{name[0]}分割")
            self.add_form(sheet[:, :split], f"{name[0]}分割")


@plugin_class_loading(get_path(r"template/machinelearning"))
class LearnerDimensions(LearnBase, metaclass=ABCMeta):
    @staticmethod
    def deep(sheet: np.ndarray):
        return sheet.ravel()

    @staticmethod
    def down_ndim(sheet: np.ndarray):  # 横向
        down_list = []
        for i in sheet:
            down_list.append(i.ravel())
        return np.array(down_list)

    @staticmethod
    def longitudinal_down_ndim(sheet: np.ndarray):  # 纵向
        down_list = []
        for i in range(len(sheet[0])):
            down_list.append(sheet[:, i].ravel())
        return np.array(down_list).T

    def reval(self, name, axis):  # axis:0-横向，1-纵向(带.T)，2-深度
        sheet = self.get_sheet(name)
        self.add_form(
            {0: self.down_ndim, 1: self.longitudinal_down_ndim, 2: self.deep}[axis](
                sheet
            ).copy(),
            f"{name}伸展",
        )

    def del_ndim(self, name):  # 删除无用维度
        sheet = self.get_sheet(name)
        self.add_form(np.squeeze(sheet), f"{name}降维")


@plugin_class_loading(get_path(r"template/machinelearning"))
class LearnerShape(LearnBase, metaclass=ABCMeta):
    def transpose(self, name, func: list):
        sheet = self.get_sheet(name)
        if sheet.ndim <= 2:
            self.add_form(sheet.transpose().copy(), f"{name}.T")
        else:
            self.add_form(np.transpose(sheet, func).copy(), f"{name}.T")

    def reshape(self, name, shape: list):
        sheet = self.get_sheet(name)
        self.add_form(sheet.reshape(shape).copy(), f"{name}.r")


@plugin_class_loading(get_path(r"template/machinelearning"))
class Calculation(LearnBase, metaclass=ABCMeta):
    def calculation_matrix(self, data, data_type, func):
        if 1 not in data_type:
            raise Exception
        func = self.func_dict.get(func, lambda x, y: x)
        args_data = []
        for i in range(len(data)):
            if data_type[i] == 0:
                args_data.append(data[i])
            else:
                args_data.append(self.get_sheet(data[i]))
        get = func(*args_data)
        self.add_form(get, f"{func}({data[0]},{data[1]})")
        return get


class Machinebase(metaclass=ABCMeta):  # 学习器的基类
    def __init__(self, *args, **kwargs):
        self.model = None
        self.have_fit = False
        self.have_predict = False
        self.x_traindata = None
        self.y_traindata = None
        # 有监督学习专有的testData
        self.x_testdata = None
        self.y_testdata = None
        # 记录这两个是为了克隆

    @abstractmethod
    def fit_model(self, x_data, y_data, split, increment, kwargs):
        pass

    @abstractmethod
    def score(self, x_data, y_data):
        pass

    @abstractmethod
    def class_score(self, save_dir, x_data, y_really):
        pass

    @staticmethod
    def _accuracy(y_predict, y_really):  # 准确率
        return accuracy_score(y_really, y_predict)

    @staticmethod
    def _macro(y_predict, y_really, func_num=0):
        func = [recall_score, precision_score, f1_score]  # 召回率，精确率和f1
        class_ = np.unique(y_really).tolist()
        result = func[func_num](y_really, y_predict, class_, average=None)
        return result, class_

    @staticmethod
    def _confusion_matrix(y_predict, y_really):  # 混淆矩阵
        class_ = np.unique(y_really).tolist()
        return confusion_matrix(y_really, y_predict), class_

    @staticmethod
    def _kappa_score(y_predict, y_really):
        return cohen_kappa_score(y_really, y_predict)

    @abstractmethod
    def regression_score(self, save_dir, x_data, y_really):
        pass

    @abstractmethod
    def clusters_score(self, save_dir, x_data, args):
        pass

    @staticmethod
    def _mse(y_predict, y_really):  # 均方误差
        return mean_squared_error(y_really, y_predict)

    @staticmethod
    def _mae(y_predict, y_really):  # 中值绝对误差
        return median_absolute_error(y_really, y_predict)

    @staticmethod
    def _r2_score(y_predict, y_really):  # 中值绝对误差
        return r2_score(y_really, y_predict)

    def _rmse(self, y_predict, y_really):  # 中值绝对误差
        return self._mse(y_predict, y_really) ** 0.5

    @staticmethod
    def _coefficient_clustering(x_data, y_predict):
        means_score = silhouette_score(x_data, y_predict)
        outline_score = silhouette_samples(x_data, y_predict)
        return means_score, outline_score

    @abstractmethod
    def predict(self, x_data, args, kwargs):
        pass

    @abstractmethod
    def data_visualization(self, save_dir, args, kwargs):
        pass


@plugin_class_loading(get_path(r"template/machinelearning"))
class StudyMachinebase(Machinebase):
    def fit_model(self, x_data, y_data, split=0.3, increment=True, **kwargs):
        y_data = y_data.ravel()
        try:
            assert self.x_traindata is None or not increment
            self.x_traindata = np.vstack((x_data, self.x_traindata))
            self.y_traindata = np.vstack((y_data, self.y_traindata))
        except (AssertionError, ValueError):
            self.x_traindata = x_data.copy()
            self.y_traindata = y_data.copy()
        x_train, x_test, y_train, y_test = train_test_split(
            x_data, y_data, test_size=split
        )
        try:  # 增量式训练
            assert not increment
            self.model.partial_fit(x_data, y_data)
        except (AssertionError, AttributeError):
            self.model.fit(self.x_traindata, self.y_traindata)
        train_score = self.model.score(x_train, y_train)
        test_score = self.model.score(x_test, y_test)
        self.have_fit = True
        return train_score, test_score

    def score(self, x_data, y_data):
        score = self.model.score(x_data, y_data)
        return score

    def class_score(self, save_dir, x_data: np.ndarray, y_really: np.ndarray):
        y_really: np.ndarray = y_really.ravel()
        y_predict: np.ndarray = self.predict(x_data)[0]

        accuracy = self._accuracy(y_predict, y_really)

        recall, class_list = self._macro(y_predict, y_really, 0)
        precision, class_list = self._macro(y_predict, y_really, 1)
        f1, class_list = self._macro(y_predict, y_really, 2)

        confusion_matrix_, class_list = self._confusion_matrix(
            y_predict, y_really)
        kappa = self._kappa_score(y_predict, y_really)
        class_list: list
        tab = Tab()

        def gauge_base(name: str, value_: float) -> Gauge:
            c = (
                Gauge()
                .add("", [(name, round(value_ * 100, 2))], min_=0, max_=100)
                .set_global_opts(title_opts=opts.TitleOpts(title=name))
            )
            return c

        tab.add(gauge_base("准确率", accuracy), "准确率")
        tab.add(gauge_base("kappa", kappa), "kappa")

        def bar_base(name, value_) -> Bar:
            c = (
                Bar()
                .add_xaxis(class_list)
                .add_yaxis(name, value_, **label_setting)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=name), **global_setting
                )
            )
            return c

        tab.add(bar_base("精确率", precision.tolist()), "精确率")
        tab.add(bar_base("召回率", recall.tolist()), "召回率")
        tab.add(bar_base("F1", f1.tolist()), "F1")

        def heatmap_base(name, value_, max_, min_, show) -> HeatMap:
            c = (
                HeatMap()
                .add_xaxis(class_list)
                .add_yaxis(
                    name,
                    class_list,
                    value_,
                    label_opts=opts.LabelOpts(is_show=show, position="inside"),
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=name),
                    **global_setting,
                    visualmap_opts=opts.VisualMapOpts(
                        max_=max_, min_=min_, pos_right="3%"
                    ),
                )
            )
            return c

        value = [
            [class_list[i], class_list[j], float(confusion_matrix_[i, j])]
            for i in range(len(class_list))
            for j in range(len(class_list))
        ]
        tab.add(
            heatmap_base(
                "混淆矩阵",
                value,
                float(confusion_matrix_.max()),
                float(confusion_matrix_.min()),
                len(class_list) < 7,
            ),
            "混淆矩阵",
        )

        des_to_csv(save_dir, "混淆矩阵", confusion_matrix_, class_list, class_list)
        des_to_csv(
            save_dir, "评分", [
                precision, recall, f1], class_list, [
                "精确率", "召回率", "F1"])
        save = save_dir + rf"{os.sep}分类模型评估.HTML"
        tab.render(save)
        return save,

    def regression_score(
            self,
            save_dir,
            x_data: np.ndarray,
            y_really: np.ndarray):
        y_really = y_really.ravel()
        y_predict = self.predict(x_data)[0]
        tab = Tab()

        mse = self._mse(y_predict, y_really)
        mae = self._mae(y_predict, y_really)
        r2_score_ = self._r2_score(y_predict, y_really)
        rmse = self._rmse(y_predict, y_really)

        tab.add(make_tab(["MSE", "MAE", "RMSE", "r2_Score"], [
            [mse, mae, rmse, r2_score_]]), "评估数据", )

        save = save_dir + rf"{os.sep}回归模型评估.HTML"
        tab.render(save)
        return save,

    def clusters_score(self, save_dir, x_data: np.ndarray, *args):
        y_predict = self.predict(x_data)[0]
        tab = Tab()
        coefficient, coefficient_array = self._coefficient_clustering(
            x_data, y_predict)

        def gauge_base(name: str, value: float) -> Gauge:
            c = (
                Gauge()
                .add(
                    "",
                    [(name, round(value * 100, 2))],
                    min_=0,
                    max_=10 ** (judging_digits(value * 100)),
                )
                .set_global_opts(title_opts=opts.TitleOpts(title=name))
            )
            return c

        def bar_base(name, value, xaxis) -> Bar:
            c = (
                Bar()
                .add_xaxis(xaxis)
                .add_yaxis(name, value, **label_setting)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=name), **global_setting
                )
            )
            return c

        tab.add(gauge_base("平均轮廓系数", coefficient), "平均轮廓系数")

        def bar_(coefficient_array_, name="数据轮廓系数"):
            xaxis = [f"数据{i}" for i in range(len(coefficient_array_))]
            value = coefficient_array_.tolist()
            tab.add(bar_base(name, value, xaxis), name)

        n = 20
        if len(coefficient_array) <= n:
            bar_(coefficient_array)
        elif len(coefficient_array) <= n ** 2:
            a = 0
            while a <= len(coefficient_array):
                b = a + n
                if b >= len(coefficient_array):
                    b = len(coefficient_array) + 1
                cofe_array = coefficient_array[a:b]
                bar_(cofe_array, f"{a}-{b}数据轮廓系数")
                a += n
        else:
            split = np.hsplit(coefficient_array, n)
            a = 0
            for cofe_array in split:
                bar_(cofe_array, f"{a}%-{a + n}%数据轮廓系数")
                a += n

        save = save_dir + rf"{os.sep}聚类模型评估.HTML"
        tab.render(save)
        return save,

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        y_predict = self.model.predict(x_data,)
        self.y_testdata = y_predict.copy()
        self.have_predict = True
        return y_predict, "预测"

    def data_visualization(self, save_dir, *args, **kwargs):
        return save_dir,


class PrepBase(StudyMachinebase):  # 不允许第二次训练
    def __init__(self, *args, **kwargs):
        super(PrepBase, self).__init__(*args, **kwargs)
        self.model = None

    def fit_model(self, x_data, y_data, increment=True, *args, **kwargs):
        if not self.have_predict:  # 不允许第二次训练
            y_data = y_data.ravel()
            try:
                assert self.x_traindata is None or not increment
                self.x_traindata = np.vstack((x_data, self.x_traindata))
                self.y_traindata = np.vstack((y_data, self.y_traindata))
            except (AssertionError, ValueError):
                self.x_traindata = x_data.copy()
                self.y_traindata = y_data.copy()
            try:  # 增量式训练
                assert not increment
                self.model.partial_fit(x_data, y_data)
            except (AssertionError, AttributeError):
                self.model.fit(self.x_traindata, self.y_traindata)
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = self.model.transform(x_data)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "特征工程"

    def score(self, x_data, y_data):
        return "None"  # 没有score


class Unsupervised(PrepBase):  # 无监督，不允许第二次训练
    def fit_model(self, x_data, increment=True, *args, **kwargs):
        if not self.have_predict:  # 不允许第二次训练
            self.y_traindata = None
            try:
                assert self.x_traindata is None or not increment
                self.x_traindata = np.vstack((x_data, self.x_traindata))
            except (AssertionError, ValueError):
                self.x_traindata = x_data.copy()
            try:  # 增量式训练
                assert not increment
                self.model.partial_fit(x_data)
            except (AssertionError, AttributeError):
                self.model.fit(self.x_traindata, self.y_traindata)
        self.have_fit = True
        return "None", "None"


class UnsupervisedModel(PrepBase):  # 无监督
    def fit_model(self, x_data, increment=True, *args, **kwargs):
        self.y_traindata = None
        try:
            assert self.x_traindata is None or not increment
            self.x_traindata = np.vstack((x_data, self.x_traindata))
        except (AssertionError, ValueError):
            self.x_traindata = x_data.copy()
        try:  # 增量式训练
            if not increment:
                raise Exception
            self.model.partial_fit(x_data)
        except (AssertionError, AttributeError):
            self.model.fit(self.x_traindata, self.y_traindata)
        self.have_fit = True
        return "None", "None"


@plugin_class_loading(get_path(r"template/machinelearning"))
class ToPyebase(StudyMachinebase):
    def __init__(self, model, *args, **kwargs):
        super(ToPyebase, self).__init__(*args, **kwargs)
        self.model = None

        # 记录这两个是为了克隆
        self.k = {}
        self.model_Name = model

    def fit_model(self, x_data, y_data, *args, **kwargs):
        self.x_traindata = x_data.copy()
        self.y_traindata = y_data.ravel().copy()
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.have_predict = True
        return np.array([]), "请使用训练"

    def score(self, x_data, y_data):
        return "None"  # 没有score


class DataAnalysis(ToPyebase):  # 数据分析
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()

        data = self.x_traindata

        def cumulative_calculation(tab_data, func, name, render_tab):
            sum_list = []
            for i in range(len(tab_data)):  # 按行迭代数据
                sum_list.append([])
                for a in range(len(tab_data[i])):
                    s = num_str(func(tab_data[: i + 1, a]), 8)
                    sum_list[-1].append(s)
            des_to_csv(save_dir, f"{name}", sum_list)
            render_tab.add(
                make_tab([f"[{i}]" for i in range(len(sum_list[0]))], sum_list),
                f"{name}",
            )

        def geometric_mean(x):
            return np.power(np.prod(x), 1 / len(x))  # 几何平均数

        def square_mean(x):
            return np.sqrt(np.sum(np.power(x, 2)) / len(x))  # 平方平均数

        def harmonic_mean(x):
            return len(x) / np.sum(np.power(x, -1))  # 调和平均数

        cumulative_calculation(data, np.sum, "累计求和", tab)
        cumulative_calculation(data, np.var, "累计方差", tab)
        cumulative_calculation(data, np.std, "累计标准差", tab)
        cumulative_calculation(data, np.mean, "累计算术平均值", tab)
        cumulative_calculation(data, geometric_mean, "累计几何平均值", tab)
        cumulative_calculation(data, square_mean, "累计平方平均值", tab)
        cumulative_calculation(data, harmonic_mean, "累计调和平均值", tab)
        cumulative_calculation(data, np.median, "累计中位数", tab)
        cumulative_calculation(data, np.max, "累计最大值", tab)
        cumulative_calculation(data, np.min, "累计最小值", tab)

        save = save_dir + rf"{os.sep}数据分析.HTML"
        tab.render(save)  # 生成HTML
        return save,


class Corr(ToPyebase):  # 相关性和协方差
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()

        data = DataFrame(self.x_traindata)
        corr: np.ndarray = data.corr().to_numpy()  # 相关性
        cov: np.ndarray = data.cov().to_numpy()  # 协方差

        def heat_map(data_, name: str, max_, min_):
            x = [f"特征[{i}]" for i in range(len(data_))]
            y = [f"特征[{i}]" for i in range(len(data_[0]))]
            value = [
                (f"特征[{i}]", f"特征[{j}]", float(data_[i][j]))
                for i in range(len(data_))
                for j in range(len(data_[i]))
            ]
            c = (
                HeatMap()
                .add_xaxis(x)
                # 如果特征太多则不显示标签
                .add_yaxis(
                    f"数据",
                    y,
                    value,
                    label_opts=opts.LabelOpts(
                        is_show=True if len(x) <= 10 else False, position="inside"
                    ),
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="矩阵热力图"),
                    **global_not_legend,
                    yaxis_opts=opts.AxisOpts(
                        is_scale=True, type_="category"
                    ),  # 'category'
                    xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                    visualmap_opts=opts.VisualMapOpts(
                        is_show=True, max_=max_, min_=min_, pos_right="3%"
                    ),
                )  # 显示
            )
            tab.add(c, name)

        heat_map(corr, "相关性热力图", 1, -1)
        heat_map(cov, "协方差热力图", float(cov.max()), float(cov.min()))

        des_to_csv(save_dir, f"相关性矩阵", corr)
        des_to_csv(save_dir, f"协方差矩阵", cov)
        save = save_dir + rf"{os.sep}数据相关性.HTML"
        tab.render(save)  # 生成HTML
        return save,


class ViewData(ToPyebase):  # 绘制预测型热力图
    def __init__(
        self, args_use, learner, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(ViewData, self).__init__(args_use, learner, *args, **kwargs)

        self.model = learner.Model
        self.Select_Model = None
        self.have_fit = learner.have_Fit
        self.model_Name = "Select_Model"
        self.learner = learner
        self.learner_name = learner.Model_Name

    def fit_model(self, *args, **kwargs):
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, add_func=None, *args, **kwargs):
        x_traindata = self.learner.x_traindata
        y_traindata = self.learner.y_traindata
        x_name = self.learner_name
        if x_traindata is not None:
            add_func(x_traindata, f"{x_name}:x训练数据")

        try:
            x_testdata = self.x_testdata
            if x_testdata is not None:
                add_func(x_testdata, f"{x_name}:x测试数据")
        except BaseException as e:
            logging.warning(str(e))

        try:
            y_testdata = self.y_testdata.copy()
            if y_testdata is not None:
                add_func(y_testdata, f"{x_name}:y测试数据")
        except BaseException as e:
            logging.warning(str(e))

        self.have_fit = True
        if y_traindata is None:
            return np.array([]), "y训练数据"
        return y_traindata, "y训练数据"

    def data_visualization(self, save_dir, *args, **kwargs):
        return save_dir,


class MatrixScatter(ToPyebase):  # 矩阵散点图
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()

        data = self.x_traindata
        if data.ndim <= 2:  # 维度为2
            c = (
                Scatter()
                .add_xaxis([f"{i}" for i in range(data.shape[1])])
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=f"矩阵散点图"), **global_not_legend
                )
            )
            if data.ndim == 2:
                for num in range(len(data)):
                    i = data[num]
                    c.add_yaxis(f"{num}", [[f"{num}", x]
                                           for x in i], color="#FFFFFF")
            else:
                c.add_yaxis(f"0", [[0, x] for x in data], color="#FFFFFF")
            c.set_series_opts(
                label_opts=opts.LabelOpts(
                    is_show=True,
                    color="#000000",
                    position="inside",
                    formatter=JsCode("function(params){return params.data[2];}"),
                ))
        elif data.ndim == 3:
            c = Scatter3D().set_global_opts(
                title_opts=opts.TitleOpts(title=f"矩阵散点图"), **global_not_legend
            )
            for num in range(len(data)):
                i = data[num]
                for s_num in range(len(i)):
                    s = i[s_num]
                    y_data = [[num, s_num, x, float(s[x])]
                              for x in range(len(s))]
                    c.add(
                        f"{num}",
                        y_data,
                        zaxis3d_opts=opts.Axis3DOpts(
                            type_="category"))
            c.set_series_opts(
                label_opts=opts.LabelOpts(
                    is_show=True,
                    color="#000000",
                    position="inside",
                    formatter=JsCode("function(params){return params.data[3];}"),
                ))
        else:
            c = Scatter()
        tab.add(c, "矩阵散点图")

        save = save_dir + rf"{os.sep}矩阵散点图.HTML"
        tab.render(save)  # 生成HTML
        return save,


class ClusterTree(ToPyebase):  # 聚类树状图
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data = self.x_traindata
        linkage_array = ward(x_data)  # self.y_traindata是结果
        dendrogram(linkage_array)
        plt.savefig(save_dir + rf"{os.sep}Cluster_graph.png")

        image = Image()
        image.add(src=save_dir + rf"{os.sep}Cluster_graph.png",).set_global_opts(
            title_opts=opts.ComponentTitleOpts(title="聚类树状图")
        )
        tab.add(image, "聚类树状图")

        save = save_dir + rf"{os.sep}聚类树状图.HTML"
        tab.render(save)  # 生成HTML
        return save,


class ClassBar(ToPyebase):  # 类型柱状图
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data: np.ndarray = self.x_traindata.transpose()
        y_data: np.ndarray = self.y_traindata
        class_: list = np.unique(y_data).tolist()  # 类型
        class_list = []
        for n_class in class_:  # 生成class_list(class是1,，也就是二维的，下面会压缩成一维)
            class_list.append(y_data == n_class)
        for num_i in range(len(x_data)):  # 迭代每一个特征
            i = x_data[num_i]
            i_con = is_continuous(i)
            if i_con and len(i) >= 11:
                # 存放绘图数据，每一层列表是一个类(leg)，第二层是每个x_data
                c_list = [[0] * 10 for _ in class_list]
                start = i.min()
                end = i.max()
                n = (end - start) / 10  # 生成10条柱子
                x_axis = []  # x轴
                iter_num = 0  # 迭代到第n个
                while iter_num <= 9:  # 把每个特征分为10类进行迭代
                    # x_axis添加数据
                    x_axis.append(
                        f"({iter_num})[{round(start, 2)}-"
                        f"{round((start + n) if (start + n) <= end or not iter_num == 9 else end, 2)}]")
                    try:
                        assert iter_num == 9  # 执行到第10次时，直接获取剩下的所有
                        s = (start <= i) == (i < end)  # 布尔索引
                    except AssertionError:  # 因为start + n有超出end的风险
                        s = (start <= i) == (i <= end)  # 布尔索引
                    # n_data = i[s]  # 取得现在的特征数据

                    for num in range(len(class_list)):  # 根据类别进行迭代
                        # 取得布尔数组：y_data == n_class也就是输出值为指定类型的bool矩阵，用于切片
                        now_class: list = class_list[num]
                        # 切片成和n_data一样的位置一样的形状(now_class就是一个bool矩阵)
                        bool_class = now_class[s].ravel()
                        # 用len计数 c_list = [[class1的数据],[class2的数据],[]]
                        c_list[num][iter_num] = int(np.sum(bool_class))
                    iter_num += 1
                    start += n
            else:
                iter_np = np.unique(i)
                # 存放绘图数据，每一层列表是一个类(leg)，第二层是每个x_data
                c_list = [[0] * len(iter_np) for _ in class_list]
                x_axis = []  # 添加x轴数据
                for i_num in range(len(iter_np)):  # 迭代每一个i(不重复)
                    i_data = iter_np[i_num]
                    # n_data= i[i == i_data]#取得现在特征数据
                    x_axis.append(f"[{i_data}]")
                    for num in range(len(class_list)):  # 根据类别进行迭代
                        now_class = class_list[num]  # 取得class_list的布尔数组
                        # 切片成和n_data一样的位置一样的形状(now_class就是一个bool矩阵)
                        bool_class = now_class[i == i_data]
                        # 用len计数 c_list = [[class1的数据],[class2的数据],[]]
                        c_list[num][i_num] = len(np.sum(bool_class).tolist())
            c = (
                Bar()
                .add_xaxis(x_axis)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="类型-特征统计柱状图"),
                    **global_setting,
                    xaxis_opts=opts.AxisOpts(type_="category"),
                    yaxis_opts=opts.AxisOpts(type_="value"),
                )
            )
            y_axis = []
            for i in range(len(c_list)):
                y_axis.append(f"{class_[i]}")
                c.add_yaxis(f"{class_[i]}", c_list[i], **label_setting)
            des_to_csv(
                save_dir,
                f"类型-[{num_i}]特征统计柱状图",
                c_list,
                x_axis,
                y_axis)
            tab.add(c, f"类型-[{num_i}]特征统计柱状图")

        # 未完成
        save = save_dir + rf"{os.sep}特征统计.HTML"
        tab.render(save)  # 生成HTML
        return save,


class NumpyHeatMap(ToPyebase):  # Numpy矩阵绘制热力图
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()

        data = self.x_traindata
        x = [f"横[{i}]" for i in range(len(data))]
        y = [f"纵[{i}]" for i in range(len(data[0]))]
        value = [
            (f"横[{i}]", f"纵[{j}]", float(data[i][j]))
            for i in range(len(data))
            for j in range(len(data[i]))
        ]
        c = (
            HeatMap()
            .add_xaxis(x)
            .add_yaxis(f"数据", y, value, **label_setting)  # value的第一个数值是x
            .set_global_opts(
                title_opts=opts.TitleOpts(title="矩阵热力图"),
                **global_not_legend,
                yaxis_opts=opts.AxisOpts(
                    is_scale=True, type_="category"),  # 'category'
                xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=True,
                    max_=float(data.max()),
                    min_=float(data.min()),
                    pos_right="3%",
                ),
            )  # 显示
        )
        tab.add(c, "矩阵热力图")
        tab.add(make_tab(x, data.transpose().tolist()), f"矩阵热力图:表格")

        save = save_dir + rf"{os.sep}矩阵热力图.HTML"
        tab.render(save)  # 生成HTML
        return save,


class PredictiveHeatmapBase(ToPyebase):  # 绘制预测型热力图
    def __init__(
        self, args_use, learner, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(
            PredictiveHeatmapBase,
            self).__init__(
            args_use,
            learner,
            *
            args,
            **kwargs)

        self.model = learner.Model
        self.select_model = None
        self.have_fit = learner.have_Fit
        self.model_Name = "Select_Model"
        self.learner = learner
        self.x_traindata = learner.x_traindata.copy()
        self.y_traindata = learner.y_traindata.copy()
        self.means = []

    def fit_model(self, x_data, *args, **kwargs):
        try:
            self.means = x_data.ravel()
        except BaseException as e:
            logging.warning(str(e))
        self.have_fit = True
        return "None", "None"

    def data_visualization(
        self,
        save_dir,
        decision_boundary_func=None,
        prediction_boundary_func=None,
        *args,
        **kwargs,
    ):
        tab = Tab()
        y = self.y_traindata
        x_data = self.x_traindata
        try:  # 如果没有class
            class_ = self.model.classes_.tolist()
            class_heard = [f"类别[{i}]" for i in range(len(class_))]

            # 获取数据
            get, x_means, x_range, data_type = training_visualization(
                x_data, class_, y)
            # 可使用自带的means，并且nan表示跳过
            for i in range(min([len(x_means), len(self.means)])):
                try:
                    g = self.means[i]
                    if g == np.nan:
                        raise Exception
                    x_means[i] = g
                except BaseException as e:
                    logging.warning(str(e))
            get = decision_boundary_func(
                x_range, x_means, self.learner.predict, class_, data_type
            )
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            heard = class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))]
            data = class_ + [f"{i}" for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, "数据表")
        except AttributeError:
            get, x_means, x_range, data_type = regress_visualization(x_data, y)

            get = prediction_boundary_func(
                x_range, x_means, self.learner.predict, data_type
            )
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            heard = [f"普适预测第{i}特征" for i in range(len(x_means))]
            data = [f"{i}" for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, "数据表")

        save = save_dir + rf"{os.sep}预测热力图.HTML"
        tab.render(save)  # 生成HTML
        return save,


class PredictiveHeatmap(PredictiveHeatmapBase):  # 绘制预测型热力图
    def data_visualization(self, save_dir, *args, **kwargs):
        return super().data_visualization(
            save_dir, decision_boundary, prediction_boundary
        )


class PredictiveHeatmapMore(PredictiveHeatmapBase):  # 绘制预测型热力图_More
    def data_visualization(self, save_dir, *args, **kwargs):
        return super().data_visualization(
            save_dir, decision_boundary_more, prediction_boundary_more
        )


@plugin_class_loading(get_path(r"template/machinelearning"))
class NearFeatureScatterClassMore(ToPyebase):
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data = self.x_traindata
        y = self.y_traindata
        class_ = np.unique(y).ravel().tolist()
        class_heard = [f"簇[{i}]" for i in range(len(class_))]

        get, x_means, x_range, data_type = training_visualization_more_no_center(
            x_data, class_, y)
        for i in range(len(get)):
            tab.add(get[i], f"{i}训练数据散点图")

        heard = class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))]
        data = class_ + [f"{i}" for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, "数据表")

        save = save_dir + rf"{os.sep}数据特征散点图(分类).HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class NearFeatureScatterMore(ToPyebase):
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data = self.x_traindata
        x_means = quick_stats(x_data).get()[0]
        get_y = feature_visualization(x_data, "数据散点图")  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f"[{i}]数据x-x散点图")

        heard = [f"普适预测第{i}特征" for i in range(len(x_means))]
        data = [f"{i}" for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, "数据表")

        save = save_dir + rf"{os.sep}数据特征散点图.HTML"
        tab.render(save)  # 生成HTML
        return save,


class NearFeatureScatterClass(ToPyebase):  # 临近特征散点图：分类数据
    def data_visualization(self, save_dir, *args, **kwargs):
        # 获取数据
        class_ = np.unique(self.y_traindata).ravel().tolist()
        class_heard = [f"类别[{i}]" for i in range(len(class_))]
        tab = Tab()

        y = self.y_traindata
        x_data = self.x_traindata
        get, x_means, x_range, data_type = training_visualization(
            x_data, class_, y)
        for i in range(len(get)):
            tab.add(get[i], f"{i}临近特征散点图")

        heard = class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))]
        data = class_ + [f"{i}" for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, "数据表")

        save = save_dir + rf"{os.sep}临近数据特征散点图(分类).HTML"
        tab.render(save)  # 生成HTML
        return save,


class NearFeatureScatter(ToPyebase):  # 临近特征散点图：连续数据
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data = self.x_traindata.transpose()

        get, x_means, x_range, data_type = training_visualization_no_class(
            x_data)
        for i in range(len(get)):
            tab.add(get[i], f"{i}临近特征散点图")

        columns = [f"普适预测第{i}特征" for i in range(len(x_means))]
        data = [f"{i}" for i in x_means]
        tab.add(make_tab(columns, [data]), "数据表")

        save = save_dir + rf"{os.sep}临近数据特征散点图.HTML"
        tab.render(save)  # 生成HTML
        return save,


class FeatureScatterYX(ToPyebase):  # y-x图
    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data = self.x_traindata
        y = self.y_traindata

        get, x_means, x_range, data_type = regress_visualization(x_data, y)
        for i in range(len(get)):
            tab.add(get[i], f"{i}特征x-y散点图")

        columns = [f"普适预测第{i}特征" for i in range(len(x_means))]
        data = [f"{i}" for i in x_means]
        tab.add(make_tab(columns, [data]), "数据表")

        save = save_dir + rf"{os.sep}特征y-x图像.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class LineModel(StudyMachinebase):
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(LineModel, self).__init__(*args, **kwargs)
        all_model = {
            "Line": LinearRegression,
            "Ridge": Ridge,
            "Lasso": Lasso}[model]
        if model == "Line":
            self.model = all_model()
            self.k = {}
        else:
            self.model = all_model(
                alpha=args_use["alpha"], max_iter=args_use["max_iter"]
            )
            self.k = {
                "alpha": args_use["alpha"],
                "max_iter": args_use["max_iter"]}
        # 记录这两个是为了克隆
        self.Alpha = args_use["alpha"]
        self.max_iter = args_use["max_iter"]
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data = self.x_traindata
        y = self.y_traindata
        w_list = self.model.coef_.tolist()
        w_heard = [f"系数w[{i}]" for i in range(len(w_list))]
        b = self.model.intercept_.tolist()

        get, x_means, x_range, data_type = regress_visualization(x_data, y)
        get_line = regress_w(x_data, w_list, b, x_means.copy())
        for i in range(len(get)):
            tab.add(get[i].overlap(get_line[i]), f"{i}预测类型图")

        get = prediction_boundary(x_range, x_means, self.predict, data_type)
        for i in range(len(get)):
            tab.add(get[i], f"{i}预测热力图")

        tab.add(coefficient_scatter_plot(w_heard, w_list), "系数w散点图")
        tab.add(coefficient_bar_plot(w_heard, self.model.coef_), "系数柱状图")

        columns = [
            f"普适预测第{i}特征" for i in range(
                len(x_means))] + w_heard + ["截距b"]
        data = [f"{i}" for i in x_means] + w_list + [b]
        if self.model_Name != "Line":
            columns += ["阿尔法", "最大迭代次数"]
            data += [self.model.alpha, self.model.max_iter]
        tab.add(make_tab(columns, [data]), "数据表")

        des_to_csv(
            save_dir,
            "系数表",
            [w_list + [b]],
            [f"系数W[{i}]" for i in range(len(w_list))] + ["截距"],
        )
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )

        save = save_dir + rf"{os.sep}线性回归模型.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class LogisticregressionModel(StudyMachinebase):
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(LogisticregressionModel, self).__init__(*args, **kwargs)
        self.model = LogisticRegression(
            C=args_use["C"], max_iter=args_use["max_iter"])
        # 记录这两个是为了克隆
        self.C = args_use["C"]
        self.max_iter = args_use["max_iter"]
        self.k = {"C": args_use["C"], "max_iter": args_use["max_iter"]}
        self.model_Name = model

    def data_visualization(self, save_dir="render.html", *args, **kwargs):
        # 获取数据
        w_array = self.model.coef_
        w_list = w_array.tolist()  # 变为表格
        b = self.model.intercept_
        c = self.model.C
        max_iter = self.model.max_iter
        class_ = self.model.classes_.tolist()
        class_heard = [f"类别[{i}]" for i in range(len(class_))]
        tab = Tab()

        y = self.y_traindata
        x_data = self.x_traindata
        get, x_means, x_range, data_type = training_visualization(
            x_data, class_, y)
        get_line = training_w(x_data, class_, y, w_list, b, x_means.copy())
        for i in range(len(get)):
            tab.add(get[i].overlap(get_line[i]), f"{i}决策边界散点图")

        for i in range(len(w_list)):
            w = w_list[i]
            w_heard = [f"系数w[{i},{j}]" for j in range(len(w))]
            tab.add(coefficient_scatter_plot(w_heard, w), f"系数w[{i}]散点图")
            tab.add(coefficient_bar_plot(w_heard, w_array[i]), f"系数w[{i}]柱状图")

        columns = class_heard + \
            [f"截距{i}" for i in range(len(b))] + ["C", "最大迭代数"]
        data = class_ + b.tolist() + [c, max_iter]
        c = Table().add(headers=columns, rows=[data])
        tab.add(c, "数据表")
        c = Table().add(
            headers=[f"系数W[{i}]" for i in range(len(w_list[0]))], rows=w_list
        )
        tab.add(c, "系数数据表")

        c = Table().add(
            headers=[f"普适预测第{i}特征" for i in range(len(x_means))],
            rows=[[f"{i}" for i in x_means]],
        )
        tab.add(c, "普适预测数据表")

        des_to_csv(save_dir, "系数表", w_list, [
            f"系数W[{i}]" for i in range(len(w_list[0]))])
        des_to_csv(save_dir, "截距表", [b], [f"截距{i}" for i in range(len(b))])
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )

        save = save_dir + rf"{os.sep}逻辑回归.HTML"
        tab.render(save)  # 生成HTML
        return save,


class CategoricalData:  # 数据统计助手
    def __init__(self):
        self.x_means = []
        self.x_range = []
        self.data_type = []

    def __call__(self, x1, *args, **kwargs):
        get = self.is_continuous(x1)
        return get

    def is_continuous(self, x1: np.array):
        try:
            x1_con = is_continuous(x1)
            if x1_con:
                self.x_means.append(np.mean(x1))
                self.add_range(x1)
            else:
                assert True
            return x1_con
        except TypeError:  # 找出出现次数最多的元素
            new = np.unique(x1)  # 去除相同的元素
            count_list = []
            for i in new:
                count_list.append(np.sum(x1 == i))
            index = count_list.index(max(count_list))  # 找出最大值的索引
            self.x_means.append(x1[index])
            self.add_range(x1, False)
            return False

    def add_range(self, x1: np.array, range_=True):
        try:
            assert not range_
            min_ = int(x1.min()) - 1
            max_ = int(x1.max()) + 1
            # 不需要复制列表
            self.x_range.append([min_, max_])
            self.data_type.append(1)
        except AssertionError:
            self.x_range.append(list(set(x1.tolist())))  # 去除多余元素
            self.data_type.append(2)

    def get(self):
        return self.x_means, self.x_range, self.data_type


@plugin_class_loading(get_path(r"template/machinelearning"))
class KnnModel(StudyMachinebase):
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(KnnModel, self).__init__(*args, **kwargs)
        all_model = {
            "Knn_class": KNeighborsClassifier,
            "Knn": KNeighborsRegressor}[model]
        self.model = all_model(
            p=args_use["p"],
            n_neighbors=args_use["n_neighbors"])
        # 记录这两个是为了克隆
        self.n_neighbors = args_use["n_neighbors"]
        self.p = args_use["p"]
        self.k = {"n_neighbors": args_use["n_neighbors"], "p": args_use["p"]}
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y = self.y_traindata
        x_data = self.x_traindata
        y_test = self.y_testdata
        x_test = self.x_testdata
        if self.model_Name == "Knn_class":
            class_ = self.model.classes_.tolist()
            class_heard = [f"类别[{i}]" for i in range(len(class_))]

            get, x_means, x_range, data_type = training_visualization(
                x_data, class_, y)
            for i in range(len(get)):
                tab.add(get[i], f"{i}训练数据散点图")

            if y_test is not None:
                get = training_visualization(x_test, class_, y_test)[0]
                for i in range(len(get)):
                    tab.add(get[i], f"{i}测试数据散点图")

            get = decision_boundary(
                x_range, x_means, self.predict, class_, data_type)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            heard = class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))]
            data = class_ + [f"{i}" for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, "数据表")
        else:
            get, x_means, x_range, data_type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f"{i}训练数据散点图")

            get = regress_visualization(x_test, y_test)[0]
            for i in range(len(get)):
                tab.add(get[i], f"{i}测试数据类型图")

            get = prediction_boundary(
                x_range, x_means, self.predict, data_type)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            heard = [f"普适预测第{i}特征" for i in range(len(x_means))]
            data = [f"{i}" for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, "数据表")
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )
        save = save_dir + rf"{os.sep}K.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class TreeModel(StudyMachinebase):
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(TreeModel, self).__init__(*args, **kwargs)
        all_model = {
            "Tree_class": DecisionTreeClassifier,
            "Tree": DecisionTreeRegressor,
        }[model]
        self.model = all_model(
            criterion=args_use["criterion"],
            splitter=args_use["splitter"],
            max_features=args_use["max_features"],
            max_depth=args_use["max_depth"],
            min_samples_split=args_use["min_samples_split"],
        )
        # 记录这两个是为了克隆
        self.criterion = args_use["criterion"]
        self.splitter = args_use["splitter"]
        self.max_features = args_use["max_features"]
        self.max_depth = args_use["max_depth"]
        self.min_samples_split = args_use["min_samples_split"]
        self.k = {
            "criterion": args_use["criterion"],
            "splitter": args_use["splitter"],
            "max_features": args_use["max_features"],
            "max_depth": args_use["max_depth"],
            "min_samples_split": args_use["min_samples_split"],
        }
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        importance = self.model.feature_importances_.tolist()

        with open(save_dir + fr"{os.sep}Tree_Gra.dot", "w") as f:
            export_graphviz(self.model, out_file=f)

        make_bar("特征重要性", importance, tab)
        des_to_csv(
            save_dir,
            "特征重要性",
            [importance],
            [f"[{i}]特征" for i in range(len(importance))],
        )
        tab.add(see_tree(save_dir + fr"{os.sep}Tree_Gra.dot"), "决策树可视化")

        y = self.y_traindata
        x_data = self.x_traindata
        y_test = self.y_testdata
        x_test = self.x_testdata
        if self.model_Name == "Tree_class":
            class_ = self.model.classes_.tolist()
            class_heard = [f"类别[{i}]" for i in range(len(class_))]

            get, x_means, x_range, data_type = training_visualization(
                x_data, class_, y)
            for i in range(len(get)):
                tab.add(get[i], f"{i}训练数据散点图")

            get = training_visualization(x_test, class_, y_test)[0]
            for i in range(len(get)):
                tab.add(get[i], f"{i}测试数据散点图")

            get = decision_boundary(
                x_range, x_means, self.predict, class_, data_type)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            tab.add(
                make_tab(
                    class_heard
                    + [f"普适预测第{i}特征" for i in range(len(x_means))]
                    + [f"特征{i}重要性" for i in range(len(importance))],
                    [class_ + [f"{i}" for i in x_means] + importance],
                ),
                "数据表",
            )
        else:
            get, x_means, x_range, data_type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f"{i}训练数据散点图")

            get = regress_visualization(x_test, y_test)[0]
            for i in range(len(get)):
                tab.add(get[i], f"{i}测试数据类型图")

            get = prediction_boundary(
                x_range, x_means, self.predict, data_type)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            tab.add(
                make_tab(
                    [f"普适预测第{i}特征" for i in range(len(x_means))]
                    + [f"特征{i}重要性" for i in range(len(importance))],
                    [[f"{i}" for i in x_means] + importance],
                ),
                "数据表",
            )
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )
        save = save_dir + rf"{os.sep}决策树.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class ForestModel(StudyMachinebase):
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(ForestModel, self).__init__(*args, **kwargs)
        model = {
            "Forest_class": RandomForestClassifier,
            "Forest": RandomForestRegressor,
        }[model]
        self.model = model(
            n_estimators=args_use["n_Tree"],
            criterion=args_use["criterion"],
            max_features=args_use["max_features"],
            max_depth=args_use["max_depth"],
            min_samples_split=args_use["min_samples_split"],
        )
        # 记录这两个是为了克隆
        self.n_estimators = args_use["n_Tree"]
        self.criterion = args_use["criterion"]
        self.max_features = args_use["max_features"]
        self.max_depth = args_use["max_depth"]
        self.min_samples_split = args_use["min_samples_split"]
        self.k = {
            "n_estimators": args_use["n_Tree"],
            "criterion": args_use["criterion"],
            "max_features": args_use["max_features"],
            "max_depth": args_use["max_depth"],
            "min_samples_split": args_use["min_samples_split"],
        }
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        # 多个决策树可视化
        for i in range(len(self.model.estimators_)):
            with open(save_dir + rf"{os.sep}Tree_Gra[{i}].dot", "w") as f:
                export_graphviz(self.model.estimators_[i], out_file=f)

            tab.add(
                see_tree(
                    save_dir +
                    rf"{os.sep}Tree_Gra[{i}].dot"),
                f"[{i}]决策树可视化")

        y = self.y_traindata
        x_data = self.x_traindata
        if self.model_Name == "Forest_class":
            class_ = self.model.classes_.tolist()
            class_heard = [f"类别[{i}]" for i in range(len(class_))]

            get, x_means, x_range, data_type = training_visualization(
                x_data, class_, y)
            for i in range(len(get)):
                tab.add(get[i], f"{i}训练数据散点图")

            get = decision_boundary(
                x_range, x_means, self.predict, class_, data_type)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            tab.add(
                make_tab(
                    class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))],
                    [class_ + [f"{i}" for i in x_means]],
                ),
                "数据表",
            )
        else:
            get, x_means, x_range, data_type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测类型图")

            get = prediction_boundary(
                x_range, x_means, self.predict, data_type)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            tab.add(
                make_tab(
                    [f"普适预测第{i}特征" for i in range(len(x_means))],
                    [[f"{i}" for i in x_means]],
                ),
                "数据表",
            )
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )
        save = save_dir + rf"{os.sep}随机森林.HTML"
        tab.render(save)  # 生成HTML
        return save,


class GradienttreeModel(StudyMachinebase):  # 继承Tree_Model主要是继承Des
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(
            GradienttreeModel,
            self).__init__(
            *args,
            **kwargs)  # 不需要执行Tree_Model的初始化
        model = {
            "GradientTree_class": GradientBoostingClassifier,
            "GradientTree": GradientBoostingRegressor,
        }[model]
        self.model = model(
            n_estimators=args_use["n_Tree"],
            max_features=args_use["max_features"],
            max_depth=args_use["max_depth"],
            min_samples_split=args_use["min_samples_split"],
        )
        # 记录这两个是为了克隆
        self.criterion = args_use["criterion"]
        self.splitter = args_use["splitter"]
        self.max_features = args_use["max_features"]
        self.max_depth = args_use["max_depth"]
        self.min_samples_split = args_use["min_samples_split"]
        self.k = {
            "criterion": args_use["criterion"],
            "splitter": args_use["splitter"],
            "max_features": args_use["max_features"],
            "max_depth": args_use["max_depth"],
            "min_samples_split": args_use["min_samples_split"],
        }
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        # 多个决策树可视化
        for a in range(len(self.model.estimators_)):
            for i in range(len(self.model.estimators_[a])):
                with open(save_dir + rf"{os.sep}Tree_Gra[{a},{i}].dot", "w") as f:
                    export_graphviz(self.model.estimators_[a][i], out_file=f)

                tab.add(
                    see_tree(
                        save_dir +
                        rf"{os.sep}Tree_Gra[{a},{i}].dot"),
                    f"[{a},{i}]决策树可视化")

        y = self.y_traindata
        x_data = self.x_traindata
        if self.model_Name == "Tree_class":
            class_ = self.model.classes_.tolist()
            class_heard = [f"类别[{i}]" for i in range(len(class_))]

            get, x_means, x_range, data_type = training_visualization(
                x_data, class_, y)
            for i in range(len(get)):
                tab.add(get[i], f"{i}训练数据散点图")

            get = decision_boundary(
                x_range, x_means, self.predict, class_, data_type)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            tab.add(
                make_tab(
                    class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))],
                    [class_ + [f"{i}" for i in x_means]],
                ),
                "数据表",
            )
        else:
            get, x_means, x_range, data_type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测类型图")

            get = prediction_boundary(
                x_range, x_means, self.predict, data_type)
            for i in range(len(get)):
                tab.add(get[i], f"{i}预测热力图")

            tab.add(
                make_tab(
                    [f"普适预测第{i}特征" for i in range(len(x_means))],
                    [[f"{i}" for i in x_means]],
                ),
                "数据表",
            )
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )
        save = save_dir + rf"{os.sep}梯度提升回归树.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class SvcModel(StudyMachinebase):
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SvcModel, self).__init__(*args, **kwargs)
        self.model = SVC(
            C=args_use["C"], gamma=args_use["gamma"], kernel=args_use["kernel"]
        )
        # 记录这两个是为了克隆
        self.C = args_use["C"]
        self.gamma = args_use["gamma"]
        self.kernel = args_use["kernel"]
        self.k = {
            "C": args_use["C"],
            "gamma": args_use["gamma"],
            "kernel": args_use["kernel"],
        }
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        try:
            w_list = self.model.coef_.tolist()  # 未必有这个属性
            b = self.model.intercept_.tolist()
        except AttributeError:
            w_list = []  # 未必有这个属性
            b = []

        class_ = self.model.classes_.tolist()
        class_heard = [f"类别[{i}]" for i in range(len(class_))]

        y = self.y_traindata
        x_data = self.x_traindata
        get, x_means, x_range, data_type = training_visualization(
            x_data, class_, y)
        if w_list:
            get_line: list = training_w(
                x_data, class_, y, w_list, b, x_means.copy())
        else:
            get_line = []
        for i in range(len(get)):
            if get_line:
                tab.add(get[i].overlap(get_line[i]), f"{i}决策边界散点图")
            else:
                tab.add(get[i], f"{i}决策边界散点图")

        get = decision_boundary(
            x_range,
            x_means,
            self.predict,
            class_,
            data_type)
        for i in range(len(get)):
            tab.add(get[i], f"{i}预测热力图")

        dic = {2: "离散", 1: "连续"}
        tab.add(make_tab(class_heard +
                         [f"普适预测第{i}特征:{dic[data_type[i]]}" for i in range(len(x_means))],
                         [class_ + [f"{i}" for i in x_means]],), "数据表", )

        if w_list:
            des_to_csv(save_dir, "系数表", w_list, [
                f"系数W[{i}]" for i in range(len(w_list[0]))])
        if w_list:
            des_to_csv(save_dir, "截距表", [b], [f"截距{i}" for i in range(len(b))])
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )

        save = save_dir + rf"{os.sep}支持向量机分类.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class SvrModel(StudyMachinebase):
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SvrModel, self).__init__(*args, **kwargs)
        self.model = SVR(
            C=args_use["C"], gamma=args_use["gamma"], kernel=args_use["kernel"]
        )
        # 记录这两个是为了克隆
        self.C = args_use["C"]
        self.gamma = args_use["gamma"]
        self.kernel = args_use["kernel"]
        self.k = {
            "C": args_use["C"],
            "gamma": args_use["gamma"],
            "kernel": args_use["kernel"],
        }
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data = self.x_traindata
        y = self.y_traindata
        try:
            w_list = self.model.coef_.tolist()  # 未必有这个属性
            b = self.model.intercept_.tolist()
        except AttributeError:
            w_list = []  # 未必有这个属性
            b = []

        get, x_means, x_range, data_type = regress_visualization(x_data, y)
        if w_list:
            get_line = regress_w(x_data, w_list, b, x_means.copy())
        else:
            get_line = []
        for i in range(len(get)):
            if get_line:
                tab.add(get[i].overlap(get_line[i]), f"{i}预测类型图")
            else:
                tab.add(get[i], f"{i}预测类型图")

        get = prediction_boundary(x_range, x_means, self.predict, data_type)
        for i in range(len(get)):
            tab.add(get[i], f"{i}预测热力图")

        if w_list:
            des_to_csv(save_dir, "系数表", w_list, [
                f"系数W[{i}]" for i in range(len(w_list[0]))])
        if w_list:
            des_to_csv(save_dir, "截距表", [b], [f"截距{i}" for i in range(len(b))])
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )

        tab.add(
            make_tab(
                [f"普适预测第{i}特征" for i in range(len(x_means))],
                [[f"{i}" for i in x_means]],
            ),
            "数据表",
        )
        save = save_dir + rf"{os.sep}支持向量机回归.HTML"
        tab.render(save)  # 生成HTML
        return save,


class VarianceModel(Unsupervised):  # 无监督
    def __init__(
        self, args_use, model, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(VarianceModel, self).__init__(*args, **kwargs)
        self.model = VarianceThreshold(
            threshold=(args_use["P"] * (1 - args_use["P"])))
        # 记录这两个是为了克隆
        self.threshold = args_use["P"]
        self.k = {"threshold": args_use["P"]}
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        var = self.model.variances_  # 标准差
        y_data = self.y_testdata
        if isinstance(y_data, np.ndarray):
            get = feature_visualization(self.y_testdata)
            for i in range(len(get)):
                tab.add(get[i], f"[{i}]数据x-x散点图")

        c = (
            Bar()
            .add_xaxis([f"[{i}]特征" for i in range(len(var))])
            .add_yaxis("标准差", var.tolist(), **label_setting)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="系数w柱状图"), **global_setting
            )
        )
        tab.add(c, "数据标准差")
        save = save_dir + rf"{os.sep}方差特征选择.HTML"
        tab.render(save)  # 生成HTML
        return save,


class SelectkbestModel(PrepBase):  # 有监督
    def __init__(self, args_use, model, *args, **kwargs):
        super(SelectkbestModel, self).__init__(*args, **kwargs)
        self.model = SelectKBest(
            k=args_use["k"],
            score_func=args_use["score_func"])
        # 记录这两个是为了克隆
        self.k_ = args_use["k"]
        self.score_func = args_use["score_func"]
        self.k = {"k": args_use["k"], "score_func": args_use["score_func"]}
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        score = self.model.scores_.tolist()
        support: np.ndarray = self.model.get_support()
        y_data = self.y_traindata
        x_data = self.x_traindata
        if isinstance(x_data, np.ndarray):
            get = feature_visualization(x_data)
            for i in range(len(get)):
                tab.add(get[i], f"[{i}]训练数据x-x散点图")

        if isinstance(y_data, np.ndarray):
            get = feature_visualization(y_data)
            for i in range(len(get)):
                tab.add(get[i], f"[{i}]保留训练数据x-x散点图")

        y_data = self.y_testdata
        x_data = self.x_testdata
        if isinstance(x_data, np.ndarray):
            get = feature_visualization(x_data)
            for i in range(len(get)):
                tab.add(get[i], f"[{i}]数据x-x散点图")

        if isinstance(y_data, np.ndarray):
            get = feature_visualization(y_data)
            for i in range(len(get)):
                tab.add(get[i], f"[{i}]保留数据x-x散点图")

        choose = []
        un_choose = []
        for i in range(len(score)):
            if support[i]:
                choose.append(score[i])
                un_choose.append(0)  # 占位
            else:
                un_choose.append(score[i])
                choose.append(0)

        c = (
            Bar()
            .add_xaxis([f"[{i}]特征" for i in range(len(score))])
            .add_yaxis("选中特征", choose, **label_setting)
            .add_yaxis("抛弃特征", un_choose, **label_setting)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="系数w柱状图"), **global_setting
            )
        )
        tab.add(c, "单变量重要程度")

        save = save_dir + rf"{os.sep}单一变量特征选择.HTML"
        tab.render(save)  # 生成HTML
        return save,


class SelectFromModel(PrepBase):  # 有监督
    def __init__(
        self, args_use, learner, *args, **kwargs
    ):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SelectFromModel, self).__init__(*args, **kwargs)

        self.model = learner.Model
        self.Select_Model = SelectFromModel(
            estimator=learner.Model,
            max_features=args_use["k"],
            prefit=learner.have_Fit)
        self.max_features = args_use["k"]
        self.estimator = learner.Model
        self.k = {
            "max_features": args_use["k"],
            "estimator": learner.Model,
            "have_Fit": learner.have_Fit,
        }
        self.have_fit = learner.have_Fit
        self.model_Name = "SelectFrom_Model"
        self.learner = learner

    def fit_model(self, x_data, y_data, split=0.3, *args, **kwargs):
        y_data = y_data.ravel()
        if not self.have_fit:  # 不允许第二次训练
            self.Select_Model.fit(x_data, y_data)
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        try:
            self.x_testdata = x_data.copy()
            x_predict = self.Select_Model.transform(x_data)
            self.y_testdata = x_predict.copy()
            self.have_predict = True
            return x_predict, "模型特征工程"
        except BaseException as e:
            logging.debug(str(e))
            self.have_predict = True
            return np.array([]), "无结果工程"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        support: np.ndarray = self.Select_Model.get_support()
        y_data = self.y_testdata
        x_data = self.x_testdata
        if isinstance(x_data, np.ndarray):
            get = feature_visualization(x_data)
            for i in range(len(get)):
                tab.add(get[i], f"[{i}]数据x-x散点图")

        if isinstance(y_data, np.ndarray):
            get = feature_visualization(y_data)
            for i in range(len(get)):
                tab.add(get[i], f"[{i}]保留数据x-x散点图")

        def make_bar_(score):
            choose = []
            un_choose = []
            for i in range(len(score)):
                if support[i]:
                    choose.append(abs(score[i]))
                    un_choose.append(0)  # 占位
                else:
                    un_choose.append(abs(score[i]))
                    choose.append(0)
            c = (
                Bar()
                .add_xaxis([f"[{i}]特征" for i in range(len(score))])
                .add_yaxis("选中特征", choose, **label_setting)
                .add_yaxis("抛弃特征", un_choose, **label_setting)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="系数w柱状图"), **global_setting
                )
            )
            tab.add(c, "单变量重要程度")

        try:
            make_bar_(self.model.coef_)
        except AttributeError:
            try:
                make_bar_(self.model.feature_importances_)
            except BaseException as e:
                logging.warning(str(e))

        save = save_dir + rf"{os.sep}模型特征选择.HTML"
        tab.render(save)  # 生成HTML
        return save,


class StandardizationModel(Unsupervised):  # z-score标准化 无监督
    def __init__(self, *args, **kwargs):
        super(StandardizationModel, self).__init__(*args, **kwargs)
        self.model = StandardScaler()

        self.k = {}
        self.model_Name = "StandardScaler"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        var = self.model.var_.tolist()
        means = self.model.mean_.tolist()
        scale_ = self.model.scale_.tolist()
        conversion_control(y_data, x_data, tab)

        make_bar("标准差", var, tab)
        make_bar("方差", means, tab)
        make_bar("Scale", scale_, tab)

        save = save_dir + rf"{os.sep}z-score标准化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class MinmaxscalerModel(Unsupervised):  # 离差标准化
    def __init__(self, args_use, *args, **kwargs):
        super(MinmaxscalerModel, self).__init__(*args, **kwargs)
        self.model = MinMaxScaler(feature_range=args_use["feature_range"])

        self.k = {}
        self.model_Name = "MinMaxScaler"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        scale_ = self.model.scale_.tolist()
        max_ = self.model.data_max_.tolist()
        min_ = self.model.data_min_.tolist()
        conversion_control(y_data, x_data, tab)
        make_bar("Scale", scale_, tab)
        tab.add(
            make_tab(
                heard=[f"[{i}]特征最大值" for i in range(len(max_))]
                + [f"[{i}]特征最小值" for i in range(len(min_))],
                row=[max_ + min_],
            ),
            "数据表格",
        )

        save = save_dir + rf"{os.sep}离差标准化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class LogscalerModel(PrepBase):  # 对数标准化
    def __init__(self, *args, **kwargs):
        super(LogscalerModel, self).__init__(*args, **kwargs)
        self.model = None

        self.k = {}
        self.model_Name = "LogScaler"

    def fit_model(self, x_data, *args, **kwargs):
        if not self.have_predict:  # 不允许第二次训练
            self.max_logx = np.log(x_data.max())
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        try:
            max_logx = self.max_logx
        except AttributeError:
            self.have_fit = False
            self.fit_model(x_data)
            max_logx = self.max_logx
        self.x_testdata = x_data.copy()
        x_predict = np.log(x_data) / max_logx
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "对数变换"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        conversion_control(y_data, x_data, tab)
        tab.add(make_tab(heard=["最大对数值(自然对数)"],
                         row=[[str(self.max_logx)]]), "数据表格")

        save = save_dir + rf"{os.sep}对数标准化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class AtanscalerModel(PrepBase):  # atan标准化
    def __init__(self, *args, **kwargs):
        super(AtanscalerModel, self).__init__(*args, **kwargs)
        self.model = None

        self.k = {}
        self.model_Name = "atanScaler"

    def fit_model(self, x_data, *args, **kwargs):
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = np.arctan(x_data) * (2 / np.pi)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "atan变换"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        conversion_control(y_data, x_data, tab)

        save = save_dir + rf"{os.sep}反正切函数标准化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class DecimalscalerModel(PrepBase):  # 小数定标准化
    def __init__(self, *args, **kwargs):
        super(DecimalscalerModel, self).__init__(*args, **kwargs)
        self.model = None

        self.k = {}
        self.model_Name = "Decimal_normalization"

    def fit_model(self, x_data, *args, **kwargs):
        if not self.have_predict:  # 不允许第二次训练
            self.j = max([judging_digits(x_data.max()),
                          judging_digits(x_data.min())])
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        try:
            j = self.j
        except AttributeError:
            self.have_fit = False
            self.fit_model(x_data)
            j = self.j
        x_predict = x_data / (10 ** j)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "小数定标标准化"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        j = self.j
        conversion_control(y_data, x_data, tab)
        tab.add(make_tab(heard=["小数位数:j"], row=[[j]]), "数据表格")

        save = save_dir + rf"{os.sep}小数定标标准化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class MapzoomModel(PrepBase):  # 映射标准化
    def __init__(self, args_use, *args, **kwargs):
        super(MapzoomModel, self).__init__(*args, **kwargs)
        self.model = None

        self.feature_range = args_use["feature_range"]
        self.k = {}
        self.model_Name = "Decimal_normalization"

    def fit_model(self, x_data, *args, **kwargs):
        if not self.have_predict:  # 不允许第二次训练
            self.max_ = x_data.max()
            self.min_ = x_data.min()
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        try:
            max_ = self.max_
            min_ = self.min_
        except AttributeError:
            self.have_fit = False
            self.fit_model(x_data)
            max_ = self.max_
            min_ = self.min_
        x_predict = (x_data * (self.feature_range[1] - self.feature_range[0])) / (
            max_ - min_
        )
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "映射标准化"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        max_ = self.max_
        min_ = self.min_
        conversion_control(y_data, x_data, tab)
        tab.add(make_tab(heard=["最大值", "最小值"], row=[[max_, min_]]), "数据表格")

        save = save_dir + rf"{os.sep}映射标准化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class SigmodscalerModel(PrepBase):  # sigmod变换
    def __init__(self, *args, **kwargs):
        super(SigmodscalerModel, self).__init__(*args, **kwargs)
        self.model = None

        self.k = {}
        self.model_Name = "sigmodScaler_Model"

    def fit_model(self, x_data, *args, **kwargs):
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data: np.array, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = 1 / (1 + np.exp(-x_data))
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "Sigmod变换"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        conversion_control(y_data, x_data, tab)

        save = save_dir + rf"{os.sep}Sigmoid变换.HTML"
        tab.render(save)  # 生成HTML
        return save,


class FuzzyQuantizationModel(PrepBase):  # 模糊量化标准化
    def __init__(self, args_use, *args, **kwargs):
        super(FuzzyQuantizationModel, self).__init__(*args, **kwargs)
        self.model = None

        self.feature_range = args_use["feature_range"]
        self.k = {}
        self.model_Name = "Fuzzy_quantization"

    def fit_model(self, x_data, *args, **kwargs):
        if not self.have_predict:  # 不允许第二次训练
            self.max_ = x_data.max()
            self.max_ = x_data.min()
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        try:
            max_ = self.max_
            min_ = self.max_
        except AttributeError:
            self.have_fit = False
            self.fit_model(x_data)
            max_ = self.max_
            min_ = self.max_
        x_predict = 1 / 2 + (1 / 2) * np.sin(
            np.pi / (max_ - min_) * (x_data - (max_ - min_) / 2)
        )
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "模糊量化标准化"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_traindata
        x_data = self.x_traindata
        max_ = self.max_
        min_ = self.max_
        conversion_control(y_data, x_data, tab)
        tab.add(make_tab(heard=["最大值", "最小值"], row=[[max_, min_]]), "数据表格")

        save = save_dir + rf"{os.sep}模糊量化标准化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class RegularizationModel(Unsupervised):  # 正则化
    def __init__(self, args_use, *args, **kwargs):
        super(RegularizationModel, self).__init__(*args, **kwargs)
        self.model = Normalizer(norm=args_use["norm"])

        self.k = {"norm": args_use["norm"]}
        self.model_Name = "Regularization"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata.copy()
        x_data = self.x_testdata.copy()
        conversion_control(y_data, x_data, tab)

        save = save_dir + rf"{os.sep}正则化.HTML"
        tab.render(save)  # 生成HTML
        return save,


# 离散数据


class BinarizerModel(Unsupervised):  # 二值化
    def __init__(self, args_use, *args, **kwargs):
        super(BinarizerModel, self).__init__(*args, **kwargs)
        self.model = Binarizer(threshold=args_use["threshold"])

        self.k = {}
        self.model_Name = "Binarizer"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        get_y = discrete_feature_visualization(y_data, "转换数据")  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f"[{i}]数据x-x离散散点图")

        heard = [f"特征:{i}" for i in range(len(x_data[0]))]
        tab.add(make_tab(heard, x_data.tolist()), f"原数据")
        tab.add(make_tab(heard, y_data.tolist()), f"编码数据")
        tab.add(
            make_tab(
                heard, np.dstack(
                    (x_data, y_data)).tolist()), f"合成[原数据,编码]数据")

        save = save_dir + rf"{os.sep}二值离散化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class DiscretizationModel(PrepBase):  # n值离散
    def __init__(self, args_use, *args, **kwargs):
        super(DiscretizationModel, self).__init__(*args, **kwargs)
        self.model = None

        range_ = args_use["split_range"]
        if not range_:
            raise Exception
        elif len(range_) == 1:
            range_.append(range_[0])
        self.range = range_
        self.k = {}
        self.model_Name = "Discretization"

    def fit_model(self, *args, **kwargs):
        # t值在模型创建时已经保存
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = x_data.copy()  # 复制
        range_ = self.range
        bool_list = []
        max_ = len(range_) - 1
        o_t = None
        for i in range(len(range_)):
            try:
                t = float(range_[i])
            except ValueError:
                continue
            if o_t is None:  # 第一个参数
                bool_list.append(x_predict <= t)
            else:
                bool_list.append((o_t <= x_predict) == (x_predict < t))
                if i == max_:
                    bool_list.append(t <= x_predict)
            o_t = t
        for i in range(len(bool_list)):
            x_predict[bool_list[i]] = i
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, f"{len(bool_list)}值离散化"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        get_y = discrete_feature_visualization(y_data, "转换数据")  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f"[{i}]数据x-x离散散点图")

        heard = [f"特征:{i}" for i in range(len(x_data[0]))]
        tab.add(make_tab(heard, x_data.tolist()), f"原数据")
        tab.add(make_tab(heard, y_data.tolist()), f"编码数据")
        tab.add(
            make_tab(
                heard, np.dstack(
                    (x_data, y_data)).tolist()), f"合成[原数据,编码]数据")

        save = save_dir + rf"{os.sep}多值离散化.HTML"
        tab.render(save)  # 生成HTML
        return save,


class LabelModel(PrepBase):  # 数字编码
    def __init__(self, *args, **kwargs):
        super(LabelModel, self).__init__(*args, **kwargs)
        self.model = []
        self.k = {}
        self.model_Name = "LabelEncoder"

    def fit_model(self, x_data, *args, **kwargs):
        if not self.have_predict:  # 不允许第二次训练
            self.model = []
            if x_data.ndim == 1:
                x_data = np.array([x_data])
            for i in range(x_data.shape[1]):
                self.model.append(
                    LabelEncoder().fit(np.ravel(x_data[:, i]))
                )  # 训练机器(每个特征一个学习器)
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = x_data.copy()
        if x_data.ndim == 1:
            x_data = np.array([x_data])
        for i in range(x_data.shape[1]):
            x_predict[:, i] = self.model[i].transform(x_data[:, i])
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "数字编码"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        x_data = self.x_testdata
        y_data = self.y_testdata
        get_y = discrete_feature_visualization(y_data, "转换数据")  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f"[{i}]数据x-x离散散点图")

        heard = [f"特征:{i}" for i in range(len(x_data[0]))]
        tab.add(make_tab(heard, x_data.tolist()), f"原数据")
        tab.add(make_tab(heard, y_data.tolist()), f"编码数据")
        tab.add(
            make_tab(
                heard, np.dstack(
                    (x_data, y_data)).tolist()), f"合成[原数据,编码]数据")

        save = save_dir + rf"{os.sep}数字编码.HTML"
        tab.render(save)  # 生成HTML
        return save,


class OneHotEncoderModel(PrepBase):  # 独热编码
    def __init__(self, args_use, *args, **kwargs):
        super(OneHotEncoderModel, self).__init__(*args, **kwargs)
        self.model = []

        self.ndim_up = args_use["ndim_up"]
        self.k = {}
        self.model_Name = "OneHotEncoder"
        self.OneHot_Data = None  # 三维独热编码

    def fit_model(self, x_data, *args, **kwargs):
        if not self.have_predict:  # 不允许第二次训练
            if x_data.ndim == 1:
                x_data = [x_data]
            for i in range(x_data.shape[1]):
                data = np.expand_dims(x_data[:, i], axis=1)  # 独热编码需要升维
                self.model.append(OneHotEncoder().fit(data))  # 训练机器
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_new = []
        for i in range(x_data.shape[1]):
            data = np.expand_dims(x_data[:, i], axis=1)  # 独热编码需要升维
            one_hot = self.model[i].transform(data).toarray().tolist()
            x_new.append(one_hot)  # 添加到列表中
        # 新列表的行数据是原data列数据的独热码(只需要ndim=2，暂时没想到numpy的做法)
        x_new = np.array(x_new)
        x_predict = []
        for i in range(x_new.shape[1]):
            x_predict.append(x_new[:, i])
        x_predict = np.array(x_predict)  # 转换回array
        self.OneHot_Data = x_predict.copy()  # 保存未降维数据
        if not self.ndim_up:  # 压缩操作
            new_x_predict = []
            for i in x_predict:
                new_list = []
                list_ = i.tolist()
                for a in list_:
                    new_list += a
                new = np.array(new_list)
                new_x_predict.append(new)

            self.y_testdata = np.array(new_x_predict)
            return self.y_testdata.copy(), "独热编码"

        self.y_testdata = self.OneHot_Data
        self.have_predict = True
        return x_predict, "独热编码"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        oh_data = self.OneHot_Data
        if not self.ndim_up:
            get_y = discrete_feature_visualization(y_data, "转换数据")  # 转换
            for i in range(len(get_y)):
                tab.add(get_y[i], f"[{i}]数据x-x离散散点图")

        heard = [f"特征:{i}" for i in range(len(x_data[0]))]
        tab.add(make_tab(heard, x_data.tolist()), f"原数据")
        tab.add(make_tab(heard, oh_data.tolist()), f"编码数据")
        tab.add(
            make_tab(
                heard, np.dstack(
                    (oh_data, x_data)).tolist()), f"合成[原数据,编码]数据")
        tab.add(make_tab([f"编码:{i}" for i in range(
            len(y_data[0]))], y_data.tolist()), f"数据")
        save = save_dir + rf"{os.sep}独热编码.HTML"
        tab.render(save)  # 生成HTML
        return save,


class MissedModel(Unsupervised):  # 缺失数据补充
    def __init__(self, args_use, *args, **kwargs):
        super(MissedModel, self).__init__(*args, **kwargs)
        self.model = SimpleImputer(
            missing_values=args_use["miss_value"],
            strategy=args_use["fill_method"],
            fill_value=args_use["fill_value"],
        )

        self.k = {}
        self.model_Name = "Missed"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = self.model.transform(x_data)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "填充缺失"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        statistics = self.model.statistics_.tolist()
        conversion_control(y_data, x_data, tab)
        tab.add(make_tab([f"特征[{i}]" for i in range(
            len(statistics))], [statistics]), "填充值")
        save = save_dir + rf"{os.sep}缺失数据填充.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class PcaModel(Unsupervised):
    def __init__(self, args_use, *args, **kwargs):
        super(PcaModel, self).__init__(*args, **kwargs)
        self.model = PCA(
            n_components=args_use["n_components"], whiten=args_use["white_PCA"]
        )

        self.whiten = args_use["white_PCA"]
        self.n_components = args_use["n_components"]
        self.k = {
            "n_components": args_use["n_components"],
            "whiten": args_use["white_PCA"],
        }
        self.model_Name = "PCA"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = self.model.transform(x_data)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "PCA"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        importance = self.model.components_.tolist()
        var = self.model.explained_variance_.tolist()  # 方量差
        conversion_separate_format(y_data, tab)

        x_data = [f"第{i+1}主成分" for i in range(len(importance))]  # 主成分
        y_data = [f"特征[{i}]" for i in range(len(importance[0]))]  # 主成分
        value = [
            (f"第{i+1}主成分", f"特征[{j}]", importance[i][j])
            for i in range(len(importance))
            for j in range(len(importance[i]))
        ]
        c = (
            HeatMap()
            .add_xaxis(x_data)
            .add_yaxis(f"", y_data, value, **label_setting)  # value的第一个数值是x
            .set_global_opts(
                title_opts=opts.TitleOpts(title="预测热力图"),
                **global_not_legend,
                yaxis_opts=opts.AxisOpts(is_scale=True),  # 'category'
                xaxis_opts=opts.AxisOpts(is_scale=True),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=True,
                    max_=int(self.model.components_.max()) + 1,
                    min_=int(self.model.components_.min()),
                    pos_right="3%",
                ),
            )  # 显示
        )
        tab.add(c, "成分热力图")
        c = (
            Bar()
            .add_xaxis([f"第[{i}]主成分" for i in range(len(var))])
            .add_yaxis("方量差", var, **label_setting)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="方量差柱状图"), **global_setting
            )
        )

        des_to_csv(save_dir, "成分重要性", importance, [x_data], [y_data])
        des_to_csv(
            save_dir, "方量差", [var], [
                f"第[{i}]主成分" for i in range(
                    len(var))])

        tab.add(c, "方量差柱状图")
        save = save_dir + rf"{os.sep}主成分分析.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class RpcaModel(Unsupervised):
    def __init__(self, args_use, *args, **kwargs):
        super(RpcaModel, self).__init__(*args, **kwargs)
        self.model = IncrementalPCA(
            n_components=args_use["n_components"], whiten=args_use["white_PCA"]
        )

        self.n_components = args_use["n_components"]
        self.whiten = args_use["white_PCA"]
        self.k = {
            "n_components": args_use["n_components"],
            "whiten": args_use["white_PCA"],
        }
        self.model_Name = "RPCA"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = self.model.transform(x_data)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "RPCA"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_traindata
        importance = self.model.components_.tolist()
        var = self.model.explained_variance_.tolist()  # 方量差
        conversion_separate_format(y_data, tab)

        x_data = [f"第{i + 1}主成分" for i in range(len(importance))]  # 主成分
        y_data = [f"特征[{i}]" for i in range(len(importance[0]))]  # 主成分
        value = [
            (f"第{i + 1}主成分", f"特征[{j}]", importance[i][j])
            for i in range(len(importance))
            for j in range(len(importance[i]))
        ]
        c = (
            HeatMap()
            .add_xaxis(x_data)
            .add_yaxis(f"", y_data, value, **label_setting)  # value的第一个数值是x
            .set_global_opts(
                title_opts=opts.TitleOpts(title="预测热力图"),
                **global_not_legend,
                yaxis_opts=opts.AxisOpts(is_scale=True),  # 'category'
                xaxis_opts=opts.AxisOpts(is_scale=True),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=True,
                    max_=int(self.model.components_.max()) + 1,
                    min_=int(self.model.components_.min()),
                    pos_right="3%",
                ),
            )  # 显示
        )
        tab.add(c, "成分热力图")
        c = (
            Bar()
            .add_xaxis([f"第[{i}]主成分" for i in range(len(var))])
            .add_yaxis("放量差", var, **label_setting)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="方量差柱状图"), **global_setting
            )
        )
        tab.add(c, "方量差柱状图")
        des_to_csv(save_dir, "成分重要性", importance, [x_data], [y_data])
        des_to_csv(
            save_dir, "方量差", [var], [
                f"第[{i}]主成分" for i in range(
                    len(var))])
        save = save_dir + rf"{os.sep}RPCA(主成分分析).HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class KpcaModel(Unsupervised):
    def __init__(self, args_use, *args, **kwargs):
        super(KpcaModel, self).__init__(*args, **kwargs)
        self.model = KernelPCA(
            n_components=args_use["n_components"], kernel=args_use["kernel"]
        )
        self.n_components = args_use["n_components"]
        self.kernel = args_use["kernel"]
        self.k = {
            "n_components": args_use["n_components"],
            "kernel": args_use["kernel"],
        }
        self.model_Name = "KPCA"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = self.model.transform(x_data)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "KPCA"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        conversion_separate_format(y_data, tab)

        save = save_dir + rf"{os.sep}KPCA(主成分分析).HTML"
        tab.render(save)  # 生成HTML
        return save,


class LdaModel(PrepBase):  # 有监督学习
    def __init__(self, args_use, *args, **kwargs):
        super(LdaModel, self).__init__(*args, **kwargs)
        self.model = Lda(n_components=args_use["n_components"])
        self.n_components = args_use["n_components"]
        self.k = {"n_components": args_use["n_components"]}
        self.model_Name = "LDA"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = self.model.transform(x_data)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "LDA"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()

        x_data = self.x_testdata
        y_data = self.y_testdata
        conversion_separate_format(y_data, tab)

        w_list = self.model.coef_.tolist()  # 变为表格
        b = self.model.intercept_
        tab = Tab()

        x_means = quick_stats(x_data).get()[0]
        # 回归的y是历史遗留问题 不用分类回归：因为得不到分类数据（predict结果是降维数据不是预测数据）
        get = regress_w(x_data, w_list, b, x_means.copy())
        for i in range(len(get)):
            tab.add(get[i].overlap(get[i]), f"类别:{i}LDA映射曲线")

        save = save_dir + rf"{os.sep}render.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class NmfModel(Unsupervised):
    def __init__(self, args_use, *args, **kwargs):
        super(NmfModel, self).__init__(*args, **kwargs)
        self.model = NMF(n_components=args_use["n_components"])

        self.n_components = args_use["n_components"]
        self.k = {"n_components": args_use["n_components"]}
        self.model_Name = "NFM"
        self.h_testdata = None
        # x_traindata保存的是W，h_traindata和y_traindata是后来数据

    def predict(self, x_data, x_name="", add_func=None, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = self.model.transform(x_data)
        self.y_testdata = x_predict.copy()
        self.h_testdata = self.model.components_
        if add_func is not None and x_name != "":
            add_func(self.h_testdata, f"{x_name}:V->NMF[H]")
        self.have_predict = True
        return x_predict, "V->NMF[W]"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        x_data = self.x_testdata
        h_data = self.h_testdata
        conversion_separate_wh(y_data, h_data, tab)

        wh_data = np.matmul(y_data, h_data)
        difference_data = x_data - wh_data

        def make_heat_map(data, name, data_max, data_min):
            x = [f"数据[{i}]" for i in range(len(data))]  # 主成分
            y = [f"特征[{i}]" for i in range(len(data[0]))]  # 主成分
            value = [
                (f"数据[{i}]", f"特征[{j}]", float(data[i][j]))
                for i in range(len(data))
                for j in range(len(data[i]))
            ]

            c = (
                HeatMap()
                .add_xaxis(x)
                .add_yaxis(f"数据", y, value, **label_setting)  # value的第一个数值是x
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="原始数据热力图"),
                    **global_not_legend,
                    yaxis_opts=opts.AxisOpts(
                        is_scale=True, type_="category"
                    ),  # 'category'
                    xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                    visualmap_opts=opts.VisualMapOpts(
                        is_show=True, max_=data_max, min_=data_min, pos_right="3%"
                    ),
                )  # 显示
            )
            tab.add(c, name)

        max_ = (max(int(x_data.max()), int(wh_data.max()),
                    int(difference_data.max())) + 1)
        min_ = min(int(x_data.min()), int(wh_data.min()),
                   int(difference_data.min()))

        make_heat_map(x_data, "原始数据热力图", max_, min_)
        make_heat_map(wh_data, "W * H数据热力图", max_, min_)
        make_heat_map(difference_data, "数据差热力图", max_, min_)

        des_to_csv(save_dir, "权重矩阵", y_data)
        des_to_csv(save_dir, "系数矩阵", h_data)
        des_to_csv(save_dir, "系数*权重矩阵", wh_data)

        save = save_dir + rf"{os.sep}非负矩阵分解.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class TsneModel(Unsupervised):
    def __init__(self, args_use, *args, **kwargs):
        super(TsneModel, self).__init__(*args, **kwargs)
        self.model = TSNE(n_components=args_use["n_components"])

        self.n_components = args_use["n_components"]
        self.k = {"n_components": args_use["n_components"]}
        self.model_Name = "t-SNE"

    def fit_model(self, *args, **kwargs):
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        x_predict = self.model.fit_transform(x_data)
        self.y_testdata = x_predict.copy()
        self.have_predict = True
        return x_predict, "SNE"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testdata
        conversion_separate_format(y_data, tab)

        save = save_dir + rf"{os.sep}T-SNE.HTML"
        tab.render(save)  # 生成HTML
        return save,


class MlpModel(StudyMachinebase):  # 神经网络(多层感知机)，有监督学习
    def __init__(self, args_use, model, *args, **kwargs):
        super(MlpModel, self).__init__(*args, **kwargs)
        all_model = {"MLP": MLPRegressor, "MLP_class": MLPClassifier}[model]
        self.model = all_model(
            hidden_layer_sizes=args_use["hidden_size"],
            activation=args_use["activation"],
            solver=args_use["solver"],
            alpha=args_use["alpha"],
            max_iter=args_use["max_iter"],
        )
        # 记录这两个是为了克隆
        self.hidden_layer_sizes = args_use["hidden_size"]
        self.activation = args_use["activation"]
        self.max_iter = args_use["max_iter"]
        self.solver = args_use["solver"]
        self.alpha = args_use["alpha"]
        self.k = {
            "hidden_layer_sizes": args_use["hidden_size"],
            "activation": args_use["activation"],
            "max_iter": args_use["max_iter"],
            "solver": args_use["solver"],
            "alpha": args_use["alpha"],
        }
        self.model_Name = model

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()

        x_data = self.x_testdata
        y_data = self.y_testdata
        coefs = self.model.coefs_
        class_ = self.model.classes_
        n_layers_ = self.model.n_layers_

        def make_heat_map(data_, name):
            x = [f"特征(节点)[{i}]" for i in range(len(data_))]
            y = [f"节点[{i}]" for i in range(len(data_[0]))]
            value = [
                (f"特征(节点)[{i}]", f"节点[{j}]", float(data_[i][j]))
                for i in range(len(data_))
                for j in range(len(data_[i]))
            ]

            c = (
                HeatMap()
                .add_xaxis(x)
                .add_yaxis(f"数据", y, value, **label_setting)  # value的第一个数值是x
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=name),
                    **global_not_legend,
                    yaxis_opts=opts.AxisOpts(
                        is_scale=True, type_="category"
                    ),  # 'category'
                    xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                    visualmap_opts=opts.VisualMapOpts(
                        is_show=True,
                        max_=float(data_.max()),
                        min_=float(data_.min()),
                        pos_right="3%",
                    ),
                )  # 显示
            )
            tab.add(c, name)
            tab.add(make_tab(x, data_.transpose().tolist()), f"{name}:表格")
            des_to_csv(save_dir, f"{name}:表格", data_.transpose().tolist(), x, y)

        get, x_means, x_range, data_type = regress_visualization(
            x_data, y_data)
        for i in range(len(get)):
            tab.add(get[i], f"{i}训练数据散点图")

        get = prediction_boundary(x_range, x_means, self.predict, data_type)
        for i in range(len(get)):
            tab.add(get[i], f"{i}预测热力图")

        heard = ["神经网络层数"]
        data = [n_layers_]
        for i in range(len(coefs)):
            make_heat_map(coefs[i], f"{i}层权重矩阵")
            heard.append(f"第{i}层节点数")
            data.append(len(coefs[i][0]))

        if self.model_Name == "MLP_class":
            heard += [f"[{i}]类型" for i in range(len(class_))]
            data += class_.tolist()

        tab.add(make_tab(heard, [data]), "数据表")

        save = save_dir + rf"{os.sep}多层感知机.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class KmeansModel(UnsupervisedModel):
    def __init__(self, args_use, *args, **kwargs):
        super(KmeansModel, self).__init__(*args, **kwargs)
        self.model = KMeans(n_clusters=args_use["n_clusters"])

        self.class_ = []
        self.n_clusters = args_use["n_clusters"]
        self.k = {"n_clusters": args_use["n_clusters"]}
        self.model_Name = "k-means"

    def fit_model(self, x_data, *args, **kwargs):
        return_ = super().fit_model(x_data, *args, **kwargs)
        self.class_ = list(set(self.model.labels_.tolist()))
        self.have_fit = True
        return return_

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        y_predict = self.model.predict(x_data)
        self.y_testdata = y_predict.copy()
        self.have_predict = True
        return y_predict, "k-means"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y = self.y_testdata
        x_data = self.x_testdata
        class_ = self.class_
        center = self.model.cluster_centers_
        class_heard = [f"簇[{i}]" for i in range(len(class_))]

        func = (
            training_visualization_more
            if more_global
            else training_visualization_center
        )
        get, x_means, x_range, data_type = func(x_data, class_, y, center)
        for i in range(len(get)):
            tab.add(get[i], f"{i}数据散点图")

        get = decision_boundary(
            x_range,
            x_means,
            self.predict,
            class_,
            data_type)
        for i in range(len(get)):
            tab.add(get[i], f"{i}预测热力图")

        heard = class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))]
        data = class_ + [f"{i}" for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, "数据表")
        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )
        save = save_dir + rf"{os.sep}k-means聚类.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class AgglomerativeModel(UnsupervisedModel):
    def __init__(self, args_use, *args, **kwargs):
        super(AgglomerativeModel, self).__init__(*args, **kwargs)
        self.model = AgglomerativeClustering(
            n_clusters=args_use["n_clusters"]
        )  # 默认为2，不同于k-means

        self.class_ = []
        self.n_clusters = args_use["n_clusters"]
        self.k = {"n_clusters": args_use["n_clusters"]}
        self.model_Name = "Agglomerative"

    def fit_model(self, x_data, *args, **kwargs):
        return_ = super().fit_model(x_data, *args, **kwargs)
        self.class_ = list(set(self.model.labels_.tolist()))
        self.have_fit = True
        return return_

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        y_predict = self.model.fit_predict(x_data)
        self.y_traindata = y_predict.copy()
        self.have_predict = True
        return y_predict, "Agglomerative"

    def data_visualization(self, save_dir, *args, **kwargs):
        tab = Tab()
        y = self.y_testdata
        x_data = self.x_testdata
        class_ = self.class_
        class_heard = [f"簇[{i}]" for i in range(len(class_))]

        func = (
            training_visualization_more_no_center
            if more_global
            else training_visualization
        )
        get, x_means, x_range, data_type = func(x_data, class_, y)
        for i in range(len(get)):
            tab.add(get[i], f"{i}训练数据散点图")

        get = decision_boundary(
            x_range,
            x_means,
            self.predict,
            class_,
            data_type)
        for i in range(len(get)):
            tab.add(get[i], f"{i}预测热力图")

        linkage_array = ward(self.x_traindata)  # self.y_traindata是结果
        dendrogram(linkage_array)
        plt.savefig(save_dir + rf"{os.sep}Cluster_graph.png")

        image = Image()
        image.add(src=save_dir + rf"{os.sep}Cluster_graph.png",).set_global_opts(
            title_opts=opts.ComponentTitleOpts(title="聚类树状图")
        )

        tab.add(image, "聚类树状图")

        heard = class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))]
        data = class_ + [f"{i}" for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, "数据表")

        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )
        save = save_dir + rf"{os.sep}层次聚类.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class DbscanModel(UnsupervisedModel):
    def __init__(self, args_use, *args, **kwargs):
        super(DbscanModel, self).__init__(*args, **kwargs)
        self.model = DBSCAN(
            eps=args_use["eps"],
            min_samples=args_use["min_samples"])
        # eps是距离(0.5)，min_samples(5)是簇与噪音分界线(每个簇最小元素数)
        # min_samples
        self.eps = args_use["eps"]
        self.min_samples = args_use["min_samples"]
        self.k = {
            "min_samples": args_use["min_samples"],
            "eps": args_use["eps"]}
        self.class_ = []
        self.model_Name = "DBSCAN"

    def fit_model(self, x_data, *args, **kwargs):
        return_ = super().fit_model(x_data, *args, **kwargs)
        self.class_ = list(set(self.model.labels_.tolist()))
        self.have_fit = True
        return return_

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        y_predict = self.model.fit_predict(x_data)
        self.y_testdata = y_predict.copy()
        self.have_predict = True
        return y_predict, "DBSCAN"

    def data_visualization(self, save_dir, *args, **kwargs):
        # DBSCAN没有预测的必要
        tab = Tab()
        y = self.y_testdata.copy()
        x_data = self.x_testdata.copy()
        class_ = self.class_
        class_heard = [f"簇[{i}]" for i in range(len(class_))]

        func = (
            training_visualization_more_no_center
            if more_global
            else training_visualization
        )
        get, x_means, x_range, data_type = func(x_data, class_, y)
        for i in range(len(get)):
            tab.add(get[i], f"{i}训练数据散点图")

        heard = class_heard + [f"普适预测第{i}特征" for i in range(len(x_means))]
        data = class_ + [f"{i}" for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, "数据表")

        des_to_csv(
            save_dir,
            "预测表",
            [[f"{i}" for i in x_means]],
            [f"普适预测第{i}特征" for i in range(len(x_means))],
        )
        save = save_dir + rf"{os.sep}密度聚类.HTML"
        tab.render(save)  # 生成HTML
        return save,


class FastFourier(StudyMachinebase):  # 快速傅里叶变换
    def __init__(self, *args, **kwargs):
        super(FastFourier, self).__init__(*args, **kwargs)
        self.model = None
        self.fourier = None  # fft复数
        self.frequency = None  # 频率range
        self.angular_Frequency = None  # 角频率range
        self.phase = None  # 相位range
        self.breadth = None  # 震幅range
        self.sample_size = None  # 样本数

    def fit_model(self, y_data, *args, **kwargs):
        y_data = y_data.ravel()  # 扯平为一维数组
        try:
            assert self.y_traindata is None
            self.y_traindata = np.hstack((y_data, self.x_traindata))
        except (AssertionError, ValueError):
            self.y_traindata = y_data.copy()
        fourier = fft(y_data)
        self.sample_size = len(y_data)
        self.frequency = np.linspace(0, 1, self.sample_size)  # 频率N_range
        self.angular_Frequency = self.frequency / (np.pi * 2)  # 角频率w
        self.phase = np.angle(fourier)
        self.breadth = np.abs(fourier)
        self.fourier = fourier
        self.have_fit = True
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        return np.array([]), ""

    def data_visualization(self, save_dir, *args, **kwargs):
        # DBSCAN没有预测的必要
        tab = Tab()
        y = self.y_traindata.copy()
        n = self.sample_size
        phase = self.phase  # 相位range
        breadth = self.breadth  # 震幅range
        normalization_breadth = breadth / n

        def line(name, value, s=slice(0, None)) -> Line:
            c = (
                Line()
                .add_xaxis(self.frequency[s].tolist())
                .add_yaxis(
                    "",
                    value,
                    **label_setting,
                    symbol="none" if self.sample_size >= 500 else None,
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=name),
                    **global_not_legend,
                    xaxis_opts=opts.AxisOpts(type_="value"),
                    yaxis_opts=opts.AxisOpts(type_="value"),
                )
            )
            return c

        tab.add(line("原始数据", y.tolist()), "原始数据")
        tab.add(line("双边振幅谱", breadth.tolist()), "双边振幅谱")
        tab.add(
            line(
                "双边振幅谱(归一化)",
                normalization_breadth.tolist()),
            "双边振幅谱(归一化)")
        tab.add(
            line("单边相位谱", breadth[: int(n / 2)].tolist(), slice(0, int(n / 2))), "单边相位谱"
        )
        tab.add(
            line(
                "单边相位谱(归一化)",
                normalization_breadth[: int(n / 2)].tolist(),
                slice(0, int(n / 2)),
            ),
            "单边相位谱(归一化)",
        )
        tab.add(line("双边相位谱", phase.tolist()), "双边相位谱")
        tab.add(
            line("单边相位谱", phase[: int(n / 2)].tolist(), slice(0, int(n / 2))), "单边相位谱"
        )

        tab.add(make_tab(self.frequency.tolist(), [breadth.tolist()]), "双边振幅谱")
        tab.add(make_tab(self.frequency.tolist(), [phase.tolist()]), "双边相位谱")
        tab.add(
            make_tab(
                self.frequency.tolist(), [
                    self.fourier.tolist()]), "快速傅里叶变换")

        save = save_dir + rf"{os.sep}快速傅里叶.HTML"
        tab.render(save)  # 生成HTML
        return save,


class ReverseFastFourier(StudyMachinebase):  # 快速傅里叶变换
    def __init__(self, *args, **kwargs):
        super(ReverseFastFourier, self).__init__(*args, **kwargs)
        self.model = None
        self.sample_size = None
        self.y_testdata_real = None
        self.phase = None
        self.breadth = None

    def fit_model(self, y_data, *args, **kwargs):
        return "None", "None"

    def predict(self, x_data, x_name="", add_func=None, *args, **kwargs):
        self.x_testdata = x_data.ravel().astype(np.complex_)
        fourier = ifft(self.x_testdata)
        self.y_testdata = fourier.copy()
        self.y_testdata_real = np.real(fourier)
        self.sample_size = len(self.y_testdata_real)
        self.phase = np.angle(self.x_testdata)
        self.breadth = np.abs(self.x_testdata)
        add_func(self.y_testdata_real.copy(), f"{x_name}:逆向快速傅里叶变换[实数]")
        return fourier, "逆向快速傅里叶变换"

    def data_visualization(self, save_dir, *args, **kwargs):
        # DBSCAN没有预测的必要
        tab = Tab()
        y = self.y_testdata_real.copy()
        y_data = self.y_testdata.copy()
        n = self.sample_size
        range_n: list = np.linspace(0, 1, n).tolist()
        phase = self.phase  # 相位range
        breadth = self.breadth  # 震幅range

        def line(name, value, s=slice(0, None)) -> Line:
            c = (
                Line() .add_xaxis(
                    range_n[s]) .add_yaxis(
                    "",
                    value,
                    **label_setting,
                    symbol="none" if n >= 500 else None) .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=name),
                    **global_not_legend,
                    xaxis_opts=opts.AxisOpts(
                        type_="value"),
                    yaxis_opts=opts.AxisOpts(
                        type_="value"),
                ))
            return c

        tab.add(line("逆向傅里叶变换", y.tolist()), "逆向傅里叶变换[实数]")
        tab.add(make_tab(range_n, [y_data.tolist()]), "逆向傅里叶变换数据")
        tab.add(make_tab(range_n, [y.tolist()]), "逆向傅里叶变换数据[实数]")
        tab.add(line("双边振幅谱", breadth.tolist()), "双边振幅谱")
        tab.add(
            line("单边相位谱", breadth[: int(n / 2)].tolist(), slice(0, int(n / 2))), "单边相位谱"
        )
        tab.add(line("双边相位谱", phase.tolist()), "双边相位谱")
        tab.add(
            line("单边相位谱", phase[: int(n / 2)].tolist(), slice(0, int(n / 2))), "单边相位谱"
        )

        save = save_dir + rf"{os.sep}快速傅里叶.HTML"
        tab.render(save)  # 生成HTML
        return save,


class ReverseFastFourierTwonumpy(ReverseFastFourier):  # 2快速傅里叶变换
    def fit_model(
            self,
            x_data,
            y_data=None,
            x_name="",
            add_func=None,
            *args,
            **kwargs):
        r = np.multiply(np.cos(x_data), y_data)
        j = np.multiply(np.sin(x_data), y_data) * 1j
        super(ReverseFastFourierTwonumpy, self).predict(
            r + j, x_name=x_name, add_func=add_func, *args, **kwargs
        )
        return "None", "None"


class CurveFitting(StudyMachinebase):  # 曲线拟合
    def __init__(self, name, str_, model, *args, **kwargs):
        super(CurveFitting, self).__init__(*args, **kwargs)

        def ndim_down(data: np.ndarray):
            if data.ndim == 1:
                return data
            new_data = []
            for i in data:
                new_data.append(np.sum(i))
            return np.array(new_data)

        named_domain = {"np": np, "Func": model, "ndimDown": ndim_down}
        protection_func = f"""
@plugin_func_loading(get_path(r'template/machinelearning'))
def FUNC({",".join(model.__code__.co_varnames)}):
    answer = Func({",".join(model.__code__.co_varnames)})
    return ndimDown(answer)
"""
        exec(protection_func, named_domain)
        self.func = named_domain["FUNC"]
        self.fit_data = None
        self.name = name
        self.func_str = str_

    def fit_model(
            self,
            x_data: np.ndarray,
            y_data: np.ndarray,
            *args,
            **kwargs):
        y_data = y_data.ravel()
        x_data = x_data.astype(np.float64)
        try:
            assert self.x_traindata is None
            self.x_traindata = np.vstack((x_data, self.x_traindata))
            self.y_traindata = np.vstack((y_data, self.y_traindata))
        except (AssertionError, ValueError):
            self.x_traindata = x_data.copy()
            self.y_traindata = y_data.copy()
        self.fit_data = optimize.curve_fit(
            self.func, self.x_traindata, self.y_traindata
        )
        self.model = self.fit_data[0].copy()
        return "None", "None"

    def predict(self, x_data, *args, **kwargs):
        self.x_testdata = x_data.copy()
        predict = self.func(x_data, *self.model)
        y_predict = []
        for i in predict:
            y_predict.append(np.sum(i))
        y_predict = np.array(y_predict)
        self.y_testdata = y_predict.copy()
        self.have_predict = True
        return y_predict, self.name

    def data_visualization(self, save_dir, *args, **kwargs):
        # DBSCAN没有预测的必要
        tab = Tab()
        y = self.y_testdata.copy()
        x_data = self.x_testdata.copy()

        get, x_means, x_range, data_type = regress_visualization(x_data, y)
        for i in range(len(get)):
            tab.add(get[i], f"{i}预测类型图")

        get = prediction_boundary(x_range, x_means, self.predict, data_type)
        for i in range(len(get)):
            tab.add(get[i], f"{i}预测热力图")

        tab.add(
            make_tab(
                [f"普适预测第{i}特征" for i in range(len(x_means))],
                [[f"{i}" for i in x_means]],
            ),
            "普适预测特征数据",
        )
        tab.add(
            make_tab(
                [f"参数[{i}]" for i in range(len(self.model))],
                [[f"{i}" for i in self.model]],
            ),
            "拟合参数",
        )

        save = save_dir + rf"{os.sep}曲线拟合.HTML"
        tab.render(save)  # 生成HTML
        return save,


@plugin_class_loading(get_path(r"template/machinelearning"))
class Tab(tab_First):
    def __init__(self, *args, **kwargs):
        super(Tab, self).__init__(*args, **kwargs)
        self.element = {}  # 记录tab组成元素 name:charts

    def add(self, chart, tab_name):
        self.element[tab_name] = chart
        return super(Tab, self).add(chart, tab_name)

    def render(
        self,
        path: str = "render.html",
        template_name: str = "simple_tab.html",
        *args,
        **kwargs,
    ) -> str:
        if all_global:
            render_dir = path_split(path)[0]
            for i in self.element:
                self.element[i].render(render_dir + os.sep + i + ".html")
        return super(Tab, self).render(path, template_name, *args, **kwargs)


@plugin_class_loading(get_path(r"template/machinelearning"))
class Table(TableFisrt):
    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.HEADERS = []
        self.ROWS = [[]]

    def add(self, headers, rows, attributes=None):
        if len(rows) == 1:
            new_headers = ["数据类型", "数据"]
            new_rows = list(zip(headers, rows[0]))
            self.HEADERS = new_headers
            self.ROWS = new_rows
            return super().add(new_headers, new_rows, attributes)
        else:
            self.HEADERS = headers
            self.ROWS = rows
            return super().add(headers, rows, attributes)

    def render(self, path="render.html", *args, **kwargs,) -> str:
        if csv_global:
            save_dir, name = path_split(path)
            name = splitext(name)[0]
            try:
                DataFrame(self.ROWS, columns=self.HEADERS).to_csv(
                    save_dir + os.sep + name + ".csv"
                )
            except BaseException as e:
                logging.warning(str(e))
        return super().render(path, *args, **kwargs)


@plugin_func_loading(get_path(r"template/machinelearning"))
def make_list(first, end, num=35):
    n = num / (end - first)
    if n == 0:
        n = 1
    return_ = []
    n_first = first * n
    n_end = end * n
    while n_first <= n_end:
        cul = n_first / n
        return_.append(round(cul, 2))
        n_first += 1
    return return_


@plugin_func_loading(get_path(r"template/machinelearning"))
def list_filter(original_list, num=70):
    if len(original_list) <= num:
        return original_list
    n = int(num / len(original_list))
    return_ = original_list[::n]
    return return_


@plugin_func_loading(get_path(r"template/machinelearning"))
def prediction_boundary(x_range, x_means, predict_func, data_type):  # 绘制回归型x-x热力图
    # r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调
    # a-特征x，b-特征x-1，c-其他特征
    render_list = []
    if len(x_means) == 1:
        return render_list
    for i in range(len(x_means)):
        for j in range(len(x_means)):
            if j <= i:
                continue
            a_range = x_range[j]
            a_type = data_type[j]
            b_range = x_range[i]
            b_type = data_type[i]
            if a_type == 1:
                a_list = make_list(a_range[0], a_range[1], 70)
            else:
                a_list = list_filter(a_range)  # 可以接受最大为70

            if b_type == 1:
                b_list = make_list(b_range[0], b_range[1], 35)
            else:
                b_list = list_filter(b_range)  # 可以接受最大为70
            a = np.array([i for i in a_list for _ in b_list]).T
            b = np.array([i for _ in a_list for i in b_list]).T
            data = np.array([x_means for _ in a_list for i in b_list])
            data[:, j] = a
            data[:, i] = b
            y_data = predict_func(data)[0].tolist()
            value = [[float(a[i]), float(b[i]), y_data[i]]
                     for i in range(len(a))]
            c = (
                HeatMap()
                .add_xaxis(np.unique(a))
                # value的第一个数值是x
                .add_yaxis(f"数据", np.unique(b), value, **label_setting)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="预测热力图"),
                    **global_not_legend,
                    yaxis_opts=opts.AxisOpts(
                        is_scale=True, type_="category"
                    ),  # 'category'
                    xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                    visualmap_opts=opts.VisualMapOpts(
                        is_show=True,
                        max_=int(max(y_data)) + 1,
                        min_=int(min(y_data)),
                        pos_right="3%",
                    ),
                )  # 显示
            )
            render_list.append(c)
    return render_list


@plugin_func_loading(get_path(r"template/machinelearning"))
def prediction_boundary_more(x_range, x_means, predict_func, data_type):
    # r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调
    # a-特征x，b-特征x-1，c-其他特征
    render_list = []
    if len(x_means) == 1:
        return render_list
    for i in range(len(x_means)):
        if i == 0:
            continue
        a_range = x_range[i - 1]
        a_type = data_type[i - 1]
        b_range = x_range[i]
        b_type = data_type[i]
        if a_type == 1:
            a_list = make_list(a_range[0], a_range[1], 70)
        else:
            a_list = list_filter(a_range)  # 可以接受最大为70

        if b_type == 1:
            b_list = make_list(b_range[0], b_range[1], 35)
        else:
            b_list = list_filter(b_range)  # 可以接受最大为70
        a = np.array([i for i in a_list for _ in b_list]).T
        b = np.array([i for _ in a_list for i in b_list]).T
        data = np.array([x_means for _ in a_list for i in b_list])
        data[:, i - 1] = a
        data[:, i] = b
        y_data = predict_func(data)[0].tolist()
        value = [[float(a[i]), float(b[i]), y_data[i]] for i in range(len(a))]
        c = (
            HeatMap()
            .add_xaxis(np.unique(a))
            # value的第一个数值是x
            .add_yaxis(f"数据", np.unique(b), value, **label_setting)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="预测热力图"),
                **global_not_legend,
                yaxis_opts=opts.AxisOpts(
                    is_scale=True, type_="category"),  # 'category'
                xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=True,
                    max_=int(max(y_data)) + 1,
                    min_=int(min(y_data)),
                    pos_right="3%",
                ),
            )  # 显示
        )
        render_list.append(c)
    return render_list


def decision_boundary(
    x_range, x_means, predict_func, class_list, data_type, no_unknow=False
):  # 绘制分类型预测图x-x热力图
    # r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调,class_是分类,add_o是可以合成的图
    # a-特征x，b-特征x-1，c-其他特征
    # 规定，i-1是x轴，a是x轴，x_1是x轴
    class_dict = dict(zip(class_list, [i for i in range(len(class_list))]))
    if not no_unknow:
        map_dict = [{"min": -1.5, "max": -0.5, "label": "未知"}]  # 分段显示
    else:
        map_dict = []
    for i in class_dict:
        map_dict.append(
            {"min": class_dict[i] - 0.5, "max": class_dict[i] + 0.5, "label": str(i)}
        )
    render_list = []
    if len(x_means) == 1:
        a_range = x_range[0]
        if data_type[0] == 1:
            a_list = make_list(a_range[0], a_range[1], 70)
        else:
            a_list = a_range

        a = np.array([i for i in a_list]).reshape(-1, 1)
        y_data = predict_func(a)[0].tolist()
        value = [[0, float(a[i]), class_dict.get(y_data[i], -1)]
                 for i in range(len(a))]
        c = (
            HeatMap()
            .add_xaxis(["None"])
            # value的第一个数值是x
            .add_yaxis(f"数据", np.unique(a), value, **label_setting)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="预测热力图"),
                **global_not_legend,
                yaxis_opts=opts.AxisOpts(
                    is_scale=True, type_="category"),  # 'category'
                xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=True,
                    max_=max(class_dict.values()),
                    min_=-1,
                    is_piecewise=True,
                    pieces=map_dict,
                    orient="horizontal",
                    pos_bottom="3%",
                ),
            )
        )
        render_list.append(c)
        return render_list
    # 如果x_means长度不等于1则执行下面
    for i in range(len(x_means)):
        if i == 0:
            continue

        a_range = x_range[i - 1]
        a_type = data_type[i - 1]
        b_range = x_range[i]
        b_type = data_type[i]
        if a_type == 1:
            a_list = make_list(a_range[0], a_range[1], 70)
        else:
            a_list = a_range

        if b_type == 1:
            rb = make_list(b_range[0], b_range[1], 35)
        else:
            rb = b_range
        a = np.array([i for i in a_list for _ in rb]).T
        b = np.array([i for _ in a_list for i in rb]).T
        data = np.array([x_means for _ in a_list for i in rb])
        data[:, i - 1] = a
        data[:, i] = b
        y_data = predict_func(data)[0].tolist()
        value = [
            [float(a[i]), float(b[i]), class_dict.get(y_data[i], -1)]
            for i in range(len(a))
        ]
        c = (
            HeatMap()
            .add_xaxis(np.unique(a))
            # value的第一个数值是x
            .add_yaxis(f"数据", np.unique(b), value, **label_setting)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="预测热力图"),
                **global_not_legend,
                yaxis_opts=opts.AxisOpts(
                    is_scale=True, type_="category"),  # 'category'
                xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=True,
                    max_=max(class_dict.values()),
                    min_=-1,
                    is_piecewise=True,
                    pieces=map_dict,
                    orient="horizontal",
                    pos_bottom="3%",
                ),
            )
        )
        render_list.append(c)
    return render_list


def decision_boundary_more(
    x_range, x_means, predict_func, class_list, data_type, no_unknow=False
):
    # r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调,class_是分类,add_o是可以合成的图
    # a-特征x，b-特征x-1，c-其他特征
    # 规定，i-1是x轴，a是x轴，x_1是x轴
    class_dict = dict(zip(class_list, [i for i in range(len(class_list))]))
    if not no_unknow:
        map_dict = [{"min": -1.5, "max": -0.5, "label": "未知"}]  # 分段显示
    else:
        map_dict = []
    for i in class_dict:
        map_dict.append(
            {"min": class_dict[i] - 0.5, "max": class_dict[i] + 0.5, "label": str(i)}
        )
    render_list = []
    if len(x_means) == 1:
        return decision_boundary(
            x_range, x_means, predict_func, class_list, data_type, no_unknow
        )
    # 如果x_means长度不等于1则执行下面
    for i in range(len(x_means)):
        for j in range(len(x_means)):
            if j <= i:
                continue

            a_range = x_range[j]
            a_type = data_type[j]
            b_range = x_range[i]
            b_type = data_type[i]
            if a_type == 1:
                a_range = make_list(a_range[0], a_range[1], 70)
            else:
                a_range = a_range

            if b_type == 1:
                b_range = make_list(b_range[0], b_range[1], 35)
            else:
                b_range = b_range
            a = np.array([i for i in a_range for _ in b_range]).T
            b = np.array([i for _ in a_range for i in b_range]).T
            data = np.array([x_means for _ in a_range for i in b_range])
            data[:, j] = a
            data[:, i] = b
            y_data = predict_func(data)[0].tolist()
            value = [
                [float(a[i]), float(b[i]), class_dict.get(y_data[i], -1)]
                for i in range(len(a))
            ]
            c = (
                HeatMap()
                .add_xaxis(np.unique(a))
                # value的第一个数值是x
                .add_yaxis(f"数据", np.unique(b), value, **label_setting)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="预测热力图"),
                    **global_not_legend,
                    yaxis_opts=opts.AxisOpts(
                        is_scale=True, type_="category"
                    ),  # 'category'
                    xaxis_opts=opts.AxisOpts(is_scale=True, type_="category"),
                    visualmap_opts=opts.VisualMapOpts(
                        is_show=True,
                        max_=max(class_dict.values()),
                        min_=-1,
                        is_piecewise=True,
                        pieces=map_dict,
                        orient="horizontal",
                        pos_bottom="3%",
                    ),
                )
            )
            render_list.append(c)
    return render_list


@plugin_func_loading(get_path(r"template/machinelearning"))
def see_tree(tree_file_dir):
    node_regex = re.compile(r'^([0-9]+) \[label="(.+)"\] ;$')  # 匹配节点正则表达式
    link_regex = re.compile("^([0-9]+) -> ([0-9]+) (.*);$")  # 匹配节点正则表达式
    node_dict = {}
    link_list = []

    with open(tree_file_dir, "r") as f:  # 貌似必须分开w和r
        for i in f:
            try:
                regex_result = re.findall(node_regex, i)[0]
                if regex_result[0] != "":
                    try:
                        v = float(regex_result[0])
                    except ValueError:
                        v = 0
                    node_dict[regex_result[0]] = {
                        "name": regex_result[1].replace("\\n", "\n"),
                        "value": v,
                        "children": [],
                    }
                    continue
            except BaseException as e:
                logging.warning(str(e))
            try:
                regex_result = re.findall(link_regex, i)[0]
                if regex_result[0] != "" and regex_result[1] != "":
                    link_list.append((regex_result[0], regex_result[1]))
            except BaseException as e:
                logging.warning(str(e))

    father_list = []  # 已经有父亲的list
    for i in link_list:
        father = i[0]  # 父节点
        son = i[1]  # 子节点
        try:
            node_dict[father]["children"].append(node_dict[son])
            father_list.append(son)
        except BaseException as e:
            logging.warning(str(e))

    father = list(set(node_dict.keys()) - set(father_list))

    c = (
        Tree()
        .add("", [node_dict[father[0]]], is_roam=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="决策树可视化"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
    )
    return c


@plugin_func_loading(get_path(r"template/machinelearning"))
def make_tab(heard, row):
    return Table().add(headers=heard, rows=row)


@plugin_func_loading(get_path(r"template/machinelearning"))
def coefficient_scatter_plot(w_heard, w):
    c = (
        Scatter() .add_xaxis(w_heard) .add_yaxis(
            "", w, **label_setting) .set_global_opts(
            title_opts=opts.TitleOpts(
                title="系数w散点图"), **global_setting))
    return c


@plugin_func_loading(get_path(r"template/machinelearning"))
def coefficient_bar_plot(w_heard, w):
    c = (
        Bar() .add_xaxis(w_heard) .add_yaxis(
            "",
            abs(w).tolist(),
            **label_setting) .set_global_opts(
            title_opts=opts.TitleOpts(
                title="系数w柱状图"),
            **global_setting))
    return c


@plugin_func_loading(get_path(r"template/machinelearning"))
def is_continuous(data: np.array, f: float = 0.1):
    data = data.tolist()
    l: list = np.unique(data).tolist()
    return len(l) / len(data) >= f or len(data) <= 3


@plugin_func_loading(get_path(r"template/machinelearning"))
def quick_stats(x_data):
    statistics_assistant = CategoricalData()
    print(x_data)
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        statistics_assistant(x1)
    return statistics_assistant


@plugin_func_loading(get_path(r"template/machinelearning"))
def training_visualization_more_no_center(x_data, class_list, y_data):
    x_data = x_data.transpose()
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
    statistics_assistant = quick_stats(x_data)
    render_list = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i:
                continue
            x1 = x_data[i]  # x坐标
            x1_is_continuous = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_is_continuous = is_continuous(x2)

            base_render = None  # 旧的C
            for class_num in range(len(class_list)):
                now_class = class_list[class_num]
                plot_x1 = x1[y_data == now_class].tolist()
                plot_x2 = x2[y_data == now_class]
                axis_x2 = np.unique(plot_x2)
                plot_x2 = x2[y_data == now_class].tolist()
                # x与散点图不同，这里是纵坐标
                c = (
                    Scatter()
                    .add_xaxis(plot_x2)
                    .add_yaxis(f"{now_class}", plot_x1, **label_setting)
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title=f"[{a}-{i}]训练数据散点图"),
                        **global_setting,
                        yaxis_opts=opts.AxisOpts(
                            type_="value" if x1_is_continuous else "category",
                            is_scale=True,
                        ),
                        xaxis_opts=opts.AxisOpts(
                            type_="value" if x2_is_continuous else "category",
                            is_scale=True,
                        ),
                    )
                )
                c.add_xaxis(axis_x2)

                if base_render is None:
                    base_render = c
                else:
                    base_render = base_render.overlap(c)
            render_list.append(base_render)
    means, x_range, data_type = statistics_assistant.get()
    return render_list, means, x_range, data_type


@plugin_func_loading(get_path(r"template/machinelearning"))
def training_visualization_more(x_data, class_list, y_data, center):
    x_data = x_data.transpose()
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
    statistics_assistant = quick_stats(x_data)
    render_list = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i:
                continue
            x1 = x_data[i]  # x坐标
            x1_is_continuous = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_is_continuous = is_continuous(x2)

            base_render = None  # 旧的C
            for class_num in range(len(class_list)):
                now_class = class_list[class_num]
                plot_x1 = x1[y_data == now_class].tolist()
                plot_x2 = x2[y_data == now_class]
                axis_x2 = np.unique(plot_x2)
                plot_x2 = x2[y_data == now_class].tolist()
                # x与散点图不同，这里是纵坐标
                c = (
                    Scatter()
                    .add_xaxis(plot_x2)
                    .add_yaxis(f"{now_class}", plot_x1, **label_setting)
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title=f"[{a}-{i}]训练数据散点图"),
                        **global_setting,
                        yaxis_opts=opts.AxisOpts(
                            type_="value" if x1_is_continuous else "category",
                            is_scale=True,
                        ),
                        xaxis_opts=opts.AxisOpts(
                            type_="value" if x2_is_continuous else "category",
                            is_scale=True,
                        ),
                    )
                )
                c.add_xaxis(axis_x2)

                # 添加簇中心
                try:
                    center_x2 = [center[class_num][a]]
                except IndexError:
                    center_x2 = [0]
                b = (
                    Scatter()
                    .add_xaxis(center_x2)
                    .add_yaxis(
                        f"[{now_class}]中心",
                        [center[class_num][i]],
                        **label_setting,
                        symbol="triangle",
                    )
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title="簇中心"),
                        **global_setting,
                        yaxis_opts=opts.AxisOpts(
                            type_="value" if x1_is_continuous else "category",
                            is_scale=True,
                        ),
                        xaxis_opts=opts.AxisOpts(
                            type_="value" if x2_is_continuous else "category",
                            is_scale=True,
                        ),
                    )
                )
                c.overlap(b)

                if base_render is None:
                    base_render = c
                else:
                    base_render = base_render.overlap(c)
            render_list.append(base_render)
    means, x_range, data_type = statistics_assistant.get()
    return render_list, means, x_range, data_type


@plugin_func_loading(get_path(r"template/machinelearning"))
def training_visualization_center(x_data, class_data, y_data, center):
    x_data = x_data.transpose()
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
    statistics_assistant = quick_stats(x_data)
    render_list = []
    for i in range(len(x_data)):
        if i == 0:
            continue
        x1 = x_data[i]  # x坐标
        x1_is_continuous = is_continuous(x1)

        x2 = x_data[i - 1]  # y坐标
        x2_is_continuous = is_continuous(x2)

        base_render = None  # 旧的C
        for class_num in range(len(class_data)):
            n_class = class_data[class_num]
            x_1 = x1[y_data == n_class].tolist()
            x_2 = x2[y_data == n_class]
            x_2_new = np.unique(x_2)
            x_2 = x2[y_data == n_class].tolist()
            # x与散点图不同，这里是纵坐标
            c = (
                Scatter() .add_xaxis(x_2) .add_yaxis(
                    f"{n_class}",
                    x_1,
                    **label_setting) .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"[{i-1}-{i}]训练数据散点图"),
                    **global_setting,
                    yaxis_opts=opts.AxisOpts(
                        type_="value" if x1_is_continuous else "category",
                        is_scale=True),
                    xaxis_opts=opts.AxisOpts(
                        type_="value" if x2_is_continuous else "category",
                        is_scale=True),
                ))
            c.add_xaxis(x_2_new)

            # 添加簇中心
            try:
                center_x_2 = [center[class_num][i - 1]]
            except IndexError:
                center_x_2 = [0]
            b = (
                Scatter() .add_xaxis(center_x_2) .add_yaxis(
                    f"[{n_class}]中心",
                    [
                        center[class_num][i]],
                    **label_setting,
                    symbol="triangle",
                ) .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="簇中心"),
                    **global_setting,
                    yaxis_opts=opts.AxisOpts(
                        type_="value" if x1_is_continuous else "category",
                        is_scale=True),
                    xaxis_opts=opts.AxisOpts(
                        type_="value" if x2_is_continuous else "category",
                        is_scale=True),
                ))
            c.overlap(b)

            if base_render is None:
                base_render = c
            else:
                base_render = base_render.overlap(c)
        render_list.append(base_render)
    means, x_range, data_type = statistics_assistant.get()
    return render_list, means, x_range, data_type


@plugin_func_loading(get_path(r"template/machinelearning"))
def training_visualization(x_data, class_, y_data):  # 根据不同类别绘制x-x分类散点图
    x_data = x_data.transpose()
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
    statistics_assistant = quick_stats(x_data)
    render_list = []
    for i in range(len(x_data)):
        if i == 0:
            continue

        x1 = x_data[i]  # x坐标
        x1_is_continuous = is_continuous(x1)

        x2 = x_data[i - 1]  # y坐标
        x2_is_continuous = is_continuous(x2)

        render_list = None  # 旧的C
        for now_class in class_:
            plot_x1 = x1[y_data == now_class].tolist()
            plot_x2 = x2[y_data == now_class]
            axis_x2 = np.unique(plot_x2)
            plot_x2 = x2[y_data == now_class].tolist()
            # x与散点图不同，这里是纵坐标
            c = (
                Scatter() .add_xaxis(plot_x2) .add_yaxis(
                    f"{now_class}",
                    plot_x1,
                    **label_setting) .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="训练数据散点图"),
                    **global_setting,
                    yaxis_opts=opts.AxisOpts(
                        type_="value" if x1_is_continuous else "category",
                        is_scale=True),
                    xaxis_opts=opts.AxisOpts(
                        type_="value" if x2_is_continuous else "category",
                        is_scale=True),
                ))
            c.add_xaxis(axis_x2)
            if render_list is None:
                render_list = c
            else:
                render_list = render_list.overlap(c)
        render_list.append(render_list)
    means, x_range, data_type = statistics_assistant.get()
    return render_list, means, x_range, data_type


@plugin_func_loading(get_path(r"template/machinelearning"))
def training_visualization_no_class(x_data):  # 根据绘制x-x分类散点图(无类别)
    x_data = x_data.transpose()
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
    statistics_assistant = quick_stats(x_data)
    render_list = []
    for i in range(len(x_data)):
        if i == 0:
            continue
        x1 = x_data[i]  # x坐标
        x1_is_continuous = is_continuous(x1)

        x2 = x_data[i - 1]  # y坐标
        x2_is_continuous = is_continuous(x2)
        x2_only = np.unique(x2)
        # x与散点图不同，这里是纵坐标
        c = (
            Scatter() .add_xaxis(x2) .add_yaxis(
                "",
                x1.tolist(),
                **label_setting) .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="训练数据散点图"),
                **global_not_legend,
                yaxis_opts=opts.AxisOpts(
                    type_="value" if x1_is_continuous else "category",
                    is_scale=True),
                xaxis_opts=opts.AxisOpts(
                    type_="value" if x2_is_continuous else "category",
                    is_scale=True),
            ))
        c.add_xaxis(x2_only)
        render_list.append(c)
    means, x_range, data_type = statistics_assistant.get()
    return render_list, means, x_range, data_type


def training_w(
    x_data, class_list, y_data, w_list, b_list, x_means: list
):  # 针对分类问题绘制决策边界
    x_data = x_data.transpose()
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
    render_list = []
    x_means.append(0)
    x_means = np.array(x_means)
    for i in range(len(x_data)):
        if i == 0:
            continue

        x1_is_continuous = is_continuous(x_data[i])
        x2 = x_data[i - 1]  # y坐标
        x2_is_continuous = is_continuous(x2)

        o_c = None  # 旧的C
        for class_num in range(len(class_list)):
            n_class = class_list[class_num]
            x2_only = np.unique(x2[y_data == n_class])
            # x与散点图不同，这里是纵坐标

            # 加入这个判断是为了解决sklearn历史遗留问题
            if len(class_list) == 2:  # 二分类问题
                if class_num == 0:
                    continue
                w = w_list[0]
                b = b_list[0]
            else:  # 多分类问题
                w = w_list[class_num]
                b = b_list[class_num]

            if x2_is_continuous:
                x2_only = np.array(make_list(x2_only.min(), x2_only.max(), 5))

            w = np.append(w, 0)
            y_data = (
                -(x2_only * w[i - 1]) / w[i]
                + b
                + (x_means[: i - 1] * w[: i - 1]).sum()
                + (x_means[i + 1:] * w[i + 1:]).sum()
            )  # 假设除了两个特征意外，其余特征均为means列表的数值
            c = (
                Line() .add_xaxis(x2_only) .add_yaxis(
                    f"决策边界:{n_class}=>[{i}]",
                    y_data.tolist(),
                    is_smooth=True,
                    **label_setting,
                ) .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"系数w曲线"),
                    **global_setting,
                    yaxis_opts=opts.AxisOpts(
                        type_="value" if x1_is_continuous else "category",
                        is_scale=True),
                    xaxis_opts=opts.AxisOpts(
                        type_="value" if x2_is_continuous else "category",
                        is_scale=True),
                ))
            if o_c is None:
                o_c = c
            else:
                o_c = o_c.overlap(c)
            # 下面不要接任何代码，因为上面会continue
        render_list.append(o_c)
    return render_list


@plugin_func_loading(get_path(r"template/machinelearning"))
def regress_w(x_data, w_data: np.array, intercept_b, x_means: list):  # 针对回归问题(y-x图)
    x_data = x_data.transpose()
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
    render_list = []
    x_means.append(0)  # 确保mean[i+1]不会超出index
    x_means = np.array(x_means)
    w_data = np.append(w_data, 0)
    for i in range(len(x_data)):
        x1 = x_data[i]
        x1_is_continuous = is_continuous(x1)
        if x1_is_continuous:
            x1 = np.array(make_list(x1.min(), x1.max(), 5))
        x1_only = np.unique(x1)
        # 假设除了两个特征意外，其余特征均为means列表的数值
        y_data = (
            x1_only * w_data[i]
            + intercept_b
            + (x_means[:i] * w_data[:i]).sum()
            + (x_means[i + 1:] * w_data[i + 1:]).sum()
        )
        y_is_continuous = is_continuous(y_data)
        c = (
            Line() .add_xaxis(x1_only) .add_yaxis(
                f"拟合结果=>[{i}]",
                y_data.tolist(),
                is_smooth=True,
                **label_setting) .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"系数w曲线"),
                **global_setting,
                yaxis_opts=opts.AxisOpts(
                    type_="value" if y_is_continuous else None,
                    is_scale=True),
                xaxis_opts=opts.AxisOpts(
                    type_="value" if x1_is_continuous else None,
                    is_scale=True),
            ))
        render_list.append(c)
    return render_list


@plugin_func_loading(get_path(r"template/machinelearning"))
def regress_visualization(x_data, y_data):  # y-x数据图
    x_data = x_data.transpose()
    y_is_continuous = is_continuous(y_data)
    statistics_assistant = quick_stats(x_data)
    render_list = []
    try:
        visualmap_opts = opts.VisualMapOpts(
            is_show=True,
            max_=int(y_data.max()) + 1,
            min_=int(y_data.min()),
            pos_right="3%",
        )
    except ValueError:
        visualmap_opts = None
        y_is_continuous = False
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        x1_is_continuous = is_continuous(x1)
        # 不转换成list因为保持dtype的精度，否则绘图会出现各种问题(数值重复)
        if not y_is_continuous and x1_is_continuous:
            y_is_continuous, x1_is_continuous = x1_is_continuous, y_is_continuous
            x1, y_data = y_data, x1

        c = (
            Scatter()
            .add_xaxis(x1.tolist())  # 研究表明，这个是横轴
            .add_yaxis("数据", y_data.tolist(), **label_setting)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="预测类型图"),
                **global_setting,
                yaxis_opts=opts.AxisOpts(
                    type_="value" if y_is_continuous else "category", is_scale=True
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="value" if x1_is_continuous else "category", is_scale=True
                ),
                visualmap_opts=visualmap_opts,
            )
        )
        c.add_xaxis(np.unique(x1))
        render_list.append(c)
    means, x_range, data_type = statistics_assistant.get()
    return render_list, means, x_range, data_type


@plugin_func_loading(get_path(r"template/machinelearning"))
def feature_visualization(x_data, data_name=""):  # x-x数据图
    seeting = global_setting if data_name else global_not_legend
    x_data = x_data.transpose()
    only = False
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
        only = True
    render_list = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i:
                continue  # 重复内容，跳过
            x1 = x_data[i]  # x坐标
            x1_is_continuous = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_is_continuous = is_continuous(x2)
            x2_only = np.unique(x2)
            if only:
                x2_is_continuous = False
            # x与散点图不同，这里是纵坐标
            c = (
                Scatter() .add_xaxis(x2) .add_yaxis(
                    data_name,
                    x1,
                    **label_setting) .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"[{i}-{a}]数据散点图"),
                    **seeting,
                    yaxis_opts=opts.AxisOpts(
                        type_="value" if x1_is_continuous else "category",
                        is_scale=True),
                    xaxis_opts=opts.AxisOpts(
                        type_="value" if x2_is_continuous else "category",
                        is_scale=True),
                ))
            c.add_xaxis(x2_only)
            render_list.append(c)
    return render_list


@plugin_func_loading(get_path(r"template/machinelearning"))
def feature_visualization_format(x_data, data_name=""):  # x-x数据图
    seeting = global_setting if data_name else global_not_legend
    x_data = x_data.transpose()
    only = False
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
        only = True
    render_list = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i:
                continue  # 重复内容，跳过（a读取的是i后面的）
            x1 = x_data[i]  # x坐标
            x1_is_continuous = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_is_continuous = is_continuous(x2)
            x2_only = np.unique(x2)
            x1_list = x1.astype(np.str).tolist()
            for j in range(len(x1_list)):
                x1_list[j] = [x1_list[j], f"特征{j}"]
            if only:
                x2_is_continuous = False
            # x与散点图不同，这里是纵坐标
            c = (
                Scatter() .add_xaxis(x2) .add_yaxis(
                    data_name,
                    x1_list,
                    **label_setting) .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title=f"[{i}-{a}]数据散点图"),
                    **seeting,
                    yaxis_opts=opts.AxisOpts(
                        type_="value" if x1_is_continuous else "category",
                        is_scale=True),
                    xaxis_opts=opts.AxisOpts(
                        type_="value" if x2_is_continuous else "category",
                        is_scale=True),
                    tooltip_opts=opts.TooltipOpts(
                        is_show=True,
                        axis_pointer_type="cross",
                        formatter="{c}"),
                ))
            c.add_xaxis(x2_only)
            render_list.append(c)
    return render_list


@plugin_func_loading(get_path(r"template/machinelearning"))
def discrete_feature_visualization(x_data, data_name=""):  # 必定离散x-x数据图
    seeting = global_setting if data_name else global_not_legend
    x_data = x_data.transpose()
    if len(x_data) == 1:
        x_data = np.array([x_data[0], np.zeros(len(x_data[0]))])
    render_list = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i:
                continue  # 重复内容，跳过
            x1 = x_data[i]  # x坐标
            x2 = x_data[a]  # y坐标
            x2_only = np.unique(x2)

            # x与散点图不同，这里是纵坐标
            c = (
                Scatter()
                .add_xaxis(x2)
                .add_yaxis(data_name, x1, **label_setting)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=f"[{i}-{a}]数据散点图"),
                    **seeting,
                    yaxis_opts=opts.AxisOpts(type_="category", is_scale=True),
                    xaxis_opts=opts.AxisOpts(type_="category", is_scale=True),
                )
            )
            c.add_xaxis(x2_only)
            render_list.append(c)
    return render_list


@plugin_func_loading(get_path(r"template/machinelearning"))
def conversion_control(y_data, x_data, tab):  # 合并两x-x图
    if isinstance(x_data, np.ndarray) and isinstance(y_data, np.ndarray):
        get_x = feature_visualization(x_data, "原数据")  # 原来
        get_y = feature_visualization(y_data, "转换数据")  # 转换
        for i in range(len(get_x)):
            tab.add(get_x[i].overlap(get_y[i]), f"[{i}]数据x-x散点图")
    return tab


@plugin_func_loading(get_path(r"template/machinelearning"))
def conversion_separate(y_data, x_data, tab):  # 并列显示两x-x图
    if isinstance(x_data, np.ndarray) and isinstance(y_data, np.ndarray):
        get_x = feature_visualization(x_data, "原数据")  # 原来
        get_y = feature_visualization(y_data, "转换数据")  # 转换
        for i in range(len(get_x)):
            try:
                tab.add(get_x[i], f"[{i}]数据x-x散点图")
            except IndexError:
                pass
            try:
                tab.add(get_y[i], f"[{i}]变维数据x-x散点图")
            except IndexError:
                pass
    return tab


@plugin_func_loading(get_path(r"template/machinelearning"))
def conversion_separate_format(y_data, tab):  # 并列显示两x-x图
    if isinstance(y_data, np.ndarray):
        get_y = feature_visualization_format(y_data, "转换数据")  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f"[{i}]变维数据x-x散点图")
    return tab


@plugin_func_loading(get_path(r"template/machinelearning"))
def conversion_separate_wh(w_array, h_array, tab):  # 并列显示两x-x图
    if isinstance(w_array, np.ndarray) and isinstance(w_array, np.ndarray):
        get_x = feature_visualization_format(w_array, "W矩阵数据")  # 原来
        get_y = feature_visualization(
            h_array.transpose(), "H矩阵数据"
        )  # 转换(先转T，再转T变回原样，W*H是横对列)
        for i in range(len(get_x)):
            try:
                tab.add(get_x[i], f"[{i}]W矩阵x-x散点图")
            except IndexError:
                pass
            try:
                tab.add(get_y[i], f"[{i}]H.T矩阵x-x散点图")
            except IndexError:
                pass
    return tab


@plugin_func_loading(get_path(r"template/machinelearning"))
def make_bar(name, value, tab):  # 绘制柱状图
    c = (
        Bar()
        .add_xaxis([f"[{i}]特征" for i in range(len(value))])
        .add_yaxis(name, value, **label_setting)
        .set_global_opts(title_opts=opts.TitleOpts(title="系数w柱状图"), **global_setting)
    )
    tab.add(c, name)


@plugin_func_loading(get_path(r"template/machinelearning"))
def judging_digits(num: (int, float)):  # 查看小数位数
    a = str(abs(num)).split(".")[0]
    if a == "":
        raise ValueError
    return len(a)


@plugin_func_loading(get_path(r"template/machinelearning"))
def num_str(num, accuracy):
    num = str(round(float(num), accuracy))
    if len(num.replace(".", "")) == accuracy:
        return num
    n = num.split(".")
    if len(n) == 0:  # 无小数
        return num + "." + "0" * (accuracy - len(num))
    else:
        return num + "0" * (accuracy - len(num) + 1)  # len(num)多算了一位小数点


@plugin_func_loading(get_path(r"template/machinelearning"))
def des_to_csv(save_dir, name, data, columns=None, row=None):
    save_dir = save_dir + os.sep + name + ".csv"
    print(columns)
    print(row)
    print(data)
    DataFrame(data, columns=columns, index=row).to_csv(
        save_dir,
        header=False if columns is None else True,
        index=False if row is None else True,
    )
    return data


@plugin_func_loading(get_path(r"template/machinelearning"))
def pack(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=basename(source_dir))
    return output_filename


def set_global(
    more=more_global,
    all_=all_global,
    csv=csv_global,
    clf=clf_global,
    tar=tar_global,
    new=new_dir_global,
):
    global more_global, all_global, csv_global, clf_global, tar_global, new_dir_global
    more_global = more  # 是否使用全部特征绘图
    all_global = all_  # 是否导出charts
    csv_global = csv  # 是否导出CSV
    clf_global = clf  # 是否导出模型
    tar_global = tar  # 是否打包tar
    new_dir_global = new  # 是否新建目录


class MachineLearnerInit(
    LearnerIO, Calculation, LearnerMerge, LearnerSplit, LearnerDimensions, LearnerShape, metaclass=ABCMeta
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.learner = {}  # 记录机器
        self.learn_dict = {
            "Line": LineModel,
            "Ridge": LineModel,
            "Lasso": LineModel,
            "LogisticRegression": LogisticregressionModel,
            "Knn_class": KnnModel,
            "Knn": KnnModel,
            "Tree_class": TreeModel,
            "Tree": TreeModel,
            "Forest": ForestModel,
            "Forest_class": ForestModel,
            "GradientTree_class": GradienttreeModel,
            "GradientTree": GradienttreeModel,
            "Variance": VarianceModel,
            "SelectKBest": SelectkbestModel,
            "Z-Score": StandardizationModel,
            "MinMaxScaler": MinmaxscalerModel,
            "LogScaler": LogscalerModel,
            "atanScaler": AtanscalerModel,
            "decimalScaler": DecimalscalerModel,
            "sigmodScaler": SigmodscalerModel,
            "Mapzoom": MapzoomModel,
            "Fuzzy_quantization": FuzzyQuantizationModel,
            "Regularization": RegularizationModel,
            "Binarizer": BinarizerModel,
            "Discretization": DiscretizationModel,
            "Label": LabelModel,
            "OneHotEncoder": OneHotEncoderModel,
            "Missed": MissedModel,
            "PCA": PcaModel,
            "RPCA": RpcaModel,
            "KPCA": KpcaModel,
            "LDA": LdaModel,
            "SVC": SvcModel,
            "SVR": SvrModel,
            "MLP": MlpModel,
            "MLP_class": MlpModel,
            "NMF": NmfModel,
            "t-SNE": TsneModel,
            "k-means": KmeansModel,
            "Agglomerative": AgglomerativeModel,
            "DBSCAN": DbscanModel,
            "ClassBar": ClassBar,
            "FeatureScatter": NearFeatureScatter,
            "FeatureScatterClass": NearFeatureScatterClass,
            "FeatureScatter_all": NearFeatureScatterMore,
            "FeatureScatterClass_all": NearFeatureScatterClassMore,
            "HeatMap": NumpyHeatMap,
            "FeatureY-X": FeatureScatterYX,
            "ClusterTree": ClusterTree,
            "MatrixScatter": MatrixScatter,
            "Correlation": Corr,
            "Statistics": DataAnalysis,
            "Fast_Fourier": FastFourier,
            "Reverse_Fast_Fourier": ReverseFastFourier,
            "[2]Reverse_Fast_Fourier": ReverseFastFourierTwonumpy,
        }
        self.data_type = {}  # 记录机器的类型

    @staticmethod
    def learner_parameters(parameters, data_type):  # 解析参数
        original_parameter = {}
        target_parameter = {}
        # 输入数据
        exec(parameters, original_parameter)
        # 处理数据
        if data_type in ("MLP", "MLP_class"):
            target_parameter["alpha"] = float(
                original_parameter.get("alpha", 0.0001)
            )  # MLP正则化用
        else:
            target_parameter["alpha"] = float(
                original_parameter.get("alpha", 1.0)
            )  # L1和L2正则化用
        target_parameter["C"] = float(
            original_parameter.get(
                "C", 1.0))  # L1和L2正则化用
        if data_type in ("MLP", "MLP_class"):
            target_parameter["max_iter"] = int(
                original_parameter.get("max_iter", 200)
            )  # L1和L2正则化用
        else:
            target_parameter["max_iter"] = int(
                original_parameter.get("max_iter", 1000)
            )  # L1和L2正则化用
        target_parameter["n_neighbors"] = int(
            original_parameter.get("K_knn", 5)
        )  # knn邻居数 (命名不同)
        target_parameter["p"] = int(original_parameter.get("p", 2))  # 距离计算方式
        target_parameter["nDim_2"] = bool(
            original_parameter.get("nDim_2", True)
        )  # 数据是否降维

        if data_type in ("Tree", "Forest", "GradientTree"):
            target_parameter["criterion"] = (
                "mse" if bool(
                    original_parameter.get(
                        "is_MSE",
                        True)) else "mae")  # 是否使用基尼不纯度
        else:
            target_parameter["criterion"] = (
                "gini" if bool(
                    original_parameter.get(
                        "is_Gini",
                        True)) else "entropy")  # 是否使用基尼不纯度
        target_parameter["splitter"] = (
            "random" if bool(
                original_parameter.get(
                    "is_random",
                    False)) else "best")  # 决策树节点是否随机选用最优
        target_parameter["max_features"] = original_parameter.get(
            "max_features", None
        )  # 选用最多特征数
        target_parameter["max_depth"] = original_parameter.get(
            "max_depth", None
        )  # 最大深度
        target_parameter["min_samples_split"] = int(
            original_parameter.get("min_samples_split", 2)
        )  # 是否继续划分（容易造成过拟合）

        target_parameter["P"] = float(
            original_parameter.get(
                "min_samples_split", 0.8))
        target_parameter["k"] = original_parameter.get("k", 1)
        target_parameter["score_func"] = {
            "chi2": chi2,
            "f_classif": f_classif,
            "mutual_info_classif": mutual_info_classif,
            "f_regression": f_regression,
            "mutual_info_regression": mutual_info_regression,
        }.get(original_parameter.get("score_func", "f_classif"), f_classif)

        target_parameter["feature_range"] = tuple(
            original_parameter.get("feature_range", (0, 1))
        )
        target_parameter["norm"] = original_parameter.get(
            "norm", "l2")  # 正则化的方式L1或者L2

        target_parameter["threshold"] = float(
            original_parameter.get("threshold", 0.0)
        )  # 二值化特征

        target_parameter["split_range"] = list(
            original_parameter.get("split_range", [0])
        )  # 二值化特征

        target_parameter["ndim_up"] = bool(
            original_parameter.get("ndim_up", False))
        target_parameter["miss_value"] = original_parameter.get(
            "miss_value", np.nan)
        target_parameter["fill_method"] = original_parameter.get(
            "fill_method", "mean")
        target_parameter["fill_value"] = original_parameter.get(
            "fill_value", None)

        target_parameter["n_components"] = original_parameter.get(
            "n_components", 1)
        target_parameter["kernel"] = original_parameter.get(
            "kernel", "rbf" if data_type in ("SVR", "SVC") else "linear"
        )

        target_parameter["n_Tree"] = original_parameter.get("n_Tree", 100)
        target_parameter["gamma"] = original_parameter.get("gamma", 1)
        target_parameter["hidden_size"] = tuple(
            original_parameter.get("hidden_size", (100,))
        )
        target_parameter["activation"] = str(
            original_parameter.get("activation", "relu")
        )
        target_parameter["solver"] = str(
            original_parameter.get("solver", "adam"))
        if data_type in ("k-means",):
            target_parameter["n_clusters"] = int(
                original_parameter.get("n_clusters", 8)
            )
        else:
            target_parameter["n_clusters"] = int(
                original_parameter.get("n_clusters", 2)
            )
        target_parameter["eps"] = float(
            original_parameter.get(
                "n_clusters", 0.5))
        target_parameter["min_samples"] = int(
            original_parameter.get("n_clusters", 5))
        target_parameter["white_PCA"] = bool(
            original_parameter.get("white_PCA", False))
        return target_parameter

    def get_learner(self, name):
        return self.learner[name]

    def get_learner_type(self, name):
        return self.data_type[name]


@plugin_class_loading(get_path(r"template/machinelearning"))
class MachineLearnerAdd(MachineLearnerInit, metaclass=ABCMeta):
    def add_learner(self, learner_str, parameters=""):
        get = self.learn_dict[learner_str]
        name = f"Le[{len(self.learner)}]{learner_str}"
        # 参数调节
        args_use = self.learner_parameters(parameters, learner_str)
        # 生成学习器
        self.learner[name] = get(model=learner_str, args_use=args_use)
        self.data_type[name] = learner_str

    def add_curve_fitting(self, learner):
        named_domain = {}
        exec(learner, named_domain)
        name = f'Le[{len(self.learner)}]{named_domain.get("name", "SELF")}'
        func = named_domain.get("f", lambda x, k, b: k * x + b)
        self.learner[name] = CurveFitting(name, learner, func)
        self.data_type[name] = "Curve_fitting"

    def add_select_from_model(self, learner, parameters=""):
        model = self.get_learner(learner)
        name = f"Le[{len(self.learner)}]SelectFrom_Model:{learner}"
        # 参数调节
        args_use = self.learner_parameters(parameters, "SelectFrom_Model")
        # 生成学习器
        self.learner[name] = SelectFromModel(
            learner=model, args_use=args_use, Dic=self.learn_dict
        )
        self.data_type[name] = "SelectFrom_Model"

    def add_predictive_heat_map(self, learner, parameters=""):
        model = self.get_learner(learner)
        name = f"Le[{len(self.learner)}]Predictive_HeatMap:{learner}"
        # 生成学习器
        args_use = self.learner_parameters(parameters, "Predictive_HeatMap")
        self.learner[name] = PredictiveHeatmap(
            learner=model, args_use=args_use)
        self.data_type[name] = "Predictive_HeatMap"

    def add_predictive_heat_map_more(self, learner, parameters=""):
        model = self.get_learner(learner)
        name = f"Le[{len(self.learner)}]Predictive_HeatMap_More:{learner}"
        # 生成学习器
        args_use = self.learner_parameters(
            parameters, "Predictive_HeatMap_More")
        self.learner[name] = PredictiveHeatmapMore(
            learner=model, args_use=args_use)
        self.data_type[name] = "Predictive_HeatMap_More"

    def add_view_data(self, learner, parameters=""):
        model = self.get_learner(learner)
        name = f"Le[{len(self.learner)}]View_data:{learner}"
        # 生成学习器
        args_use = self.learner_parameters(parameters, "View_data")
        self.learner[name] = ViewData(learner=model, args_use=args_use)
        self.data_type[name] = "View_data"


@plugin_class_loading(get_path(r"template/machinelearning"))
class MachineLearnerScore(MachineLearnerInit, metaclass=ABCMeta):
    def score(self, name_x, name_y, learner):  # Score_Only表示仅评分 Fit_Simp 是普遍类操作
        model = self.get_learner(learner)
        x = self.get_sheet(name_x)
        y = self.get_sheet(name_y)
        return model.score(x, y)

    def model_evaluation(self, learner, save_dir, name_x, name_y, func=0):  # 显示参数
        x = self.get_sheet(name_x)
        y = self.get_sheet(name_y)
        if new_dir_global:
            dic = save_dir + f"{os.sep}{learner}分类评分[CoTan]"
            new_dic = dic
            a = 0
            while exists(new_dic):  # 直到他不存在 —— False
                new_dic = dic + f"[{a}]"
                a += 1
            mkdir(new_dic)
        else:
            new_dic = save_dir
        model = self.get_learner(learner)
        # 打包
        func = [
            model.class_score,
            model.regression_score,
            model.clusters_score][func]
        save = func(new_dic, x, y)[0]
        if tar_global:
            pack(f"{new_dic}.tar.gz", new_dic)
        return save, new_dic

    def model_visualization(self, learner, save_dir):  # 显示参数
        if new_dir_global:
            dic = save_dir + f"{os.sep}{learner}数据[CoTan]"
            new_dic = dic
            a = 0
            while exists(new_dic):  # 直到他不存在 —— False
                new_dic = dic + f"[{a}]"
                a += 1
            mkdir(new_dic)
        else:
            new_dic = save_dir
        model = self.get_learner(learner)
        if (not (model.model is None) or not (
                model.model is list)) and clf_global:
            joblib.dump(model.model, new_dic + f"{os.sep}MODEL.model")  # 保存模型
        # 打包
        save = model.data_visualization(new_dic)[0]
        if tar_global:
            pack(f"{new_dic}.tar.gz", new_dic)
        return save, new_dic


@plugin_class_loading(get_path(r"template/machinelearning"))
class LearnerActions(MachineLearnerInit, metaclass=ABCMeta):
    def fit_model(self, x_name, y_name, learner, split=0.3, *args, **kwargs):
        x_data = self.get_sheet(x_name)
        y_data = self.get_sheet(y_name)
        model = self.get_learner(learner)
        return model.fit_model(
            x_data, y_data, split=split, x_name=x_name, add_func=self.add_form
        )

    def predict(self, x_name, learner, **kwargs):
        x_data = self.get_sheet(x_name)
        model = self.get_learner(learner)
        y_data, name = model.predict(
            x_data, x_name=x_name, add_func=self.add_form)
        self.add_form(y_data, f"{x_name}:{name}")
        return y_data
