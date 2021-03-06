from abc import ABCMeta, abstractmethod
from random import randint
import re
from os import getcwd
import os
import logging

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.linear_model import *
from sklearn.model_selection import train_test_split
from pyecharts.components import Table
from pyecharts.globals import SymbolType
from pyecharts.charts import *
from pyecharts import options as opts
import pandas as pd
import pandas_profiling as pp

from pyecharts.globals import CurrentConfig
from pyecharts.globals import GeoType  # 地图推荐使用GeoType而不是str
from system import plugin_class_loading, get_path, basicConfig

logging.basicConfig(**basicConfig)
CurrentConfig.ONLINE_HOST = f"{getcwd()}{os.sep}assets{os.sep}"


class FormBase(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        class Del:
            pass

        self.sheet_dict = {}
        self.clean_func = {}
        self.clean_func_code = {}
        self.DEL = Del()
        self.named_domain = {
            "pd": pd,
            "DEL": self.DEL,
            "re": re,
            "Sheet": self.sheet_dict,
        }
        self.all_render = {}  # 存放所有的图

    @abstractmethod
    def add_sheet(self, data, name):
        pass

    @abstractmethod
    def get_column(self, name, only):
        pass

    @abstractmethod
    def get_index(self, name, only):
        pass

    @abstractmethod
    def get_sheet(self, name, all_row=None, all_colunm=None) -> pd.DataFrame:
        pass


@plugin_class_loading(get_path(r"template/datascience"))
class SheetIO(FormBase, metaclass=ABCMeta):
    def add_sheet(self, data, name=""):
        if name == "":
            name = f"Sheet[{len(self.sheet_dict)}]"
        else:
            name += f"_[{len(self.sheet_dict)}]"
        self.sheet_dict[name] = data
        return data

    def __add_sheet(self, data_dir, func, name="", index=True, **kwargs):  # 新增表格的核心方式
        try:
            data = func(data_dir, **kwargs)
        except UnicodeDecodeError:  # 找不到编码方式
            return False
        if not index:
            data.index = data.iloc[:, 0].tolist()
            data.drop(data.columns.values.tolist()[0], inplace=True, axis=1)
        return self.add_sheet(data, name)

    def add_csv(
        self, data_dir, name="", sep=",", encodeding="utf-8", str_=True, index=True
    ):
        if str_:
            k = {"dtype": "object"}
        else:
            k = {}
        return self.__add_sheet(
            data_dir, pd.read_csv, name, index, sep=sep, encoding=encodeding, **k
        )

    def add_python(self, python_file, sheet_name="") -> pd.DataFrame:
        name = {"Sheet": self.get_sheet}
        name.update(globals().copy())
        name.update(locals().copy())
        exec(python_file, name)
        exec("get = Creat()", name)
        if isinstance(name["get"], pd.DataFrame):  # 已经是DataFram
            get = name["get"]
        elif isinstance(name["get"], np.array):
            if bool(name.get("downNdim", False)):  # 执行降或升维操作
                a = name["get"]
                array = []
                for i in a:
                    c = np.ravel(i, "C")
                    array.append(c)
                get = pd.DataFrame(array)
            else:
                array = name["get"].tolist()
                get = pd.DataFrame(array)
        else:
            get = pd.DataFrame(name["get"])
        self.add_sheet(get, sheet_name)
        return get

    def add_html(self, data_dir, name="", encoding="utf-8", str_=True, index=True):
        if str_:
            k = {"dtype": "object"}
        else:
            k = {}
        return self.__add_sheet(
            data_dir, pd.read_html, name, index, encoding=encoding, **k
        )

    def get_sheet_list(self):
        return list(self.sheet_dict.keys())  # 返回列表

    def to_csv(self, name, save_dir, sep=","):
        if sep == "":
            sep = ","
        get = self.get_sheet(name)
        get.to_csv(save_dir, sep=sep, na_rep="")

    def get_sheet(self, name, all_row=None, all_colunm=None) -> pd.DataFrame:
        try:
            pd.set_option("display.max_rows", all_row)
            pd.set_option("display.max_columns", all_colunm)
        finally:
            return self.sheet_dict[name]

    def del_sheet(self, name):
        del self.sheet_dict[name]


@plugin_class_loading(get_path(r"template/datascience"))
class SheetRender(FormBase, metaclass=ABCMeta):
    def render_html_one(self, name, render_dir=""):
        if render_dir == "":
            render_dir = f"{name}.html"
        get = self.get_sheet(name)
        headers = [f"{name}"] + self.get_column(name, True).tolist()
        rows = []
        table = Table()
        for i in get.iterrows():  # 按行迭代
            q = i[1].tolist()
            rows.append([f"{i[0]}"] + q)
        table.add(headers, rows).set_global_opts(
            title_opts=opts.ComponentTitleOpts(
                title=f"表格:{name}", subtitle="CoTan~数据处理:查看表格"
            )
        )
        table.render(render_dir)
        return render_dir

    def render_html_all(self, name, tab_render_dir="", render_type=0):
        if tab_render_dir == "":
            tab_render_dir = f"{name}.html"
        # 把要画的sheet放到第一个
        sheet_dict = self.sheet_dict.copy()
        del sheet_dict[name]
        sheet_list = [name] + list(sheet_dict.keys())

        class TabNew:
            def __init__(self, original_tab):
                self.original_tab = original_tab  # 一个Tab

            def render(self, render_dir):
                return self.original_tab.render(render_dir)

        # 生成一个显示页面
        if render_type == 0:

            class TabZero(TabNew):
                def add(self, render, k, *more):
                    self.original_tab.add(render, k)

            tab = TabZero(Tab(page_title="CoTan:查看表格"))  # 一个Tab
        elif render_type == 1:

            class TabOne(TabNew):
                def add(self, render, *more):
                    self.original_tab.add(render)

            tab = TabOne(Page(page_title="CoTan:查看表格", layout=Page.DraggablePageLayout))
        else:

            class TabTwo(TabNew):
                def add(self, render, *more):
                    self.original_tab.add(render)

            tab = TabTwo(Page(page_title="CoTan:查看表格", layout=Page.SimplePageLayout))
        # 迭代添加内容
        for name in sheet_list:
            try:
                get = self.get_sheet(name)
                headers = [f"{name}"] + self.get_column(name, True).tolist()
                rows = []
                table = Table()
                for i in get.iterrows():  # 按行迭代
                    q = i[1].tolist()
                    rows.append([f"{i[0]}"] + q)
                table.add(headers, rows).set_global_opts(
                    title_opts=opts.ComponentTitleOpts(
                        title=f"表格:{name}", subtitle="CoTan~数据处理:查看表格"
                    )
                )
                tab.add(table, f"表格:{name}")
            finally:
                tab.render(tab_render_dir)
                return tab_render_dir


@plugin_class_loading(get_path(r"template/datascience"))
class SheetReport(FormBase, metaclass=ABCMeta):
    def describe(self, name, new=False):  # 生成描述
        get = self.get_sheet(name)
        des = get.describe()
        if new:
            self.add_sheet(des, f"{name}_describe[{len(self.sheet_dict)}]")
        shape = get.shape
        dtype = get.dtypes
        n = get.ndim
        head = get.head()
        tail = get.tail(3)
        return (
            f"1)基本\n{des}\n\n2)形状:{shape}\n\n3)数据类型\n{dtype}\n\n4)数据维度:{n}\n\n5)头部数据\n{head}"
            f"\n\n6)尾部数据\n{tail}\n\n7)行名\n{get.index}\n\n8)列名\n{get.columns}"
        )

    @staticmethod
    def sheet_profile_report_core(sheet, save_dir):
        report = pp.ProfileReport(sheet)
        report.to_file(save_dir)

    def to_report(self, name, save_dir=""):
        if save_dir == "":
            save_dir = f"{name}.html"
        sheet = self.get_sheet(name)
        self.sheet_profile_report_core(sheet, save_dir)
        return save_dir


@plugin_class_loading(get_path(r"template/datascience"))
class Rename(FormBase, metaclass=ABCMeta):
    def number_naming(self, name, is_column, save):
        get = self.get_sheet(name).copy()
        if is_column:  # 处理列名
            column = self.get_column(name, True)
            if save:  # 保存原数据
                get.loc["column"] = column
            get.columns = [i for i in range(len(column))]
        else:
            row = self.get_index(name, True)
            if save:
                get.loc[:, "row"] = row
            get.index = [i for i in range(len(row))]
        self.add_sheet(get, f"{name}")
        return get

    def name_with_number(self, name, is_column, save):
        get = self.get_sheet(name).copy()
        if is_column:  # 处理列名
            column = self.get_column(name, True)
            if save:  # 保存原数据
                get.loc["column"] = column
            get.columns = [f"[{i}]{column[i]}" for i in range(len(column))]
        else:
            row = self.get_index(name, True)
            if save:
                get.loc[:, "row"] = row
            get.index = [f"[{i}]{row[i]}" for i in range(len(row))]
        self.add_sheet(get, f"{name}")
        return get

    def data_naming(self, name, is_column, save, **data_init):
        # Date_Init:start,end,freq 任意两样
        get = self.get_sheet(name)
        if is_column:  # 处理列名
            column = self.get_column(name, True)
            if save:  # 保存原数据
                get.loc["column"] = column
            data_init["periods"] = len(column)
            get.columns = pd.date_range(**data_init)
        else:
            row = self.get_index(name, True)
            if save:
                get.loc[:, "row"] = row
            data_init["periods"] = len(row)
            get.index = pd.date_range(**data_init)
        self.add_sheet(get, f"{name}")
        return get

    def time_naming(self, name, is_column, save, **time_init):
        # Date_Init:start,end,freq 任意两样
        get = self.get_sheet(name)
        if is_column:  # 处理列名
            column = self.get_column(name, True)
            if save:  # 保存原数据
                get.loc["column"] = column
            time_init["periods"] = len(column)
            get.columns = pd.timedelta_range(**time_init)
        else:
            row = self.get_index(name, True)
            if save:
                get.loc[:, "row"] = row
            time_init["periods"] = len(row)
            get.index = pd.timedelta_range(**time_init)
        self.add_sheet(get, f"{name}")
        return get


@plugin_class_loading(get_path(r"template/datascience"))
class Sorted(FormBase, metaclass=ABCMeta):
    def sorted_index(self, name, row: bool, new=False, a=True):
        get = self.get_sheet(name)
        if row:  # row-行名排序
            sorted_sheet = get.sort_index(axis=0, ascending=a)
        else:
            sorted_sheet = get.sort_index(axis=1, ascending=a)
        if new:
            self.add_sheet(sorted_sheet, f"{name}:排序")
        return sorted_sheet

    def stored_value(self, name, collation, new=False):
        get = self.get_sheet(name)
        row = get.columns.values
        by = []
        ascending = []
        for i in collation:
            by.append(row[i[0]])
            ascending.append(i[1])
        if len(by) == 1:
            by = by[0]
            ascending = ascending[0]
        sorted_sheet = get.sort_values(by=by, ascending=ascending)
        if new:
            self.add_sheet(sorted_sheet, f"{name}:排序")
        return sorted_sheet


@plugin_class_loading(get_path(r"template/datascience"))
class RowColumn(Rename, Sorted, metaclass=ABCMeta):
    def get_column(self, name, only=False):  # 列名
        get = self.get_sheet(name)
        if only:
            return_ = get.columns.values
        else:
            return_ = []
            loc_list = get.columns.values
            a = 0
            for i in loc_list:
                data = get[i].to_list()
                return_.append(f"[列号:{a}]{i} -> {data}")
                a += 1
        return return_

    def get_index(self, name, only=False):
        get = self.get_sheet(name)
        if only:
            values = get.index.values
        else:
            values = []
            loc_list = get.index.values
            a = 0
            for i in range(len(loc_list)):
                index_num = loc_list[i]
                data = get.iloc[i].to_list()
                values.append(f"[行号:{a}]{index_num} -> {data}")
                a += 1
        return values

    def replace_index(self, name, is_column, rename, save):
        get = self.get_sheet(name)
        if is_column:
            if save:  # 保存原数据
                get.loc["column"] = self.get_column(name, True)
            new = get.rename(columns=rename)
        else:
            if save:
                get.loc[:, "row"] = self.get_index(name, True)
            new = get.rename(index=rename)
        self.add_sheet(new, f"{name}")
        return new

    def change_index(
        self,
        name: str,
        is_column: bool,
        iloc: int,
        save: bool = True,
        drop: bool = False,
    ):
        get = self.get_sheet(name).copy()
        if is_column:  # 列名
            row = self.get_index(name, True)  # 行数据
            t = row.tolist()[iloc]
            if save:  # 保存原数据
                get.loc["column"] = self.get_column(name, True)
            # new_colums = get.loc[t].values
            get.columns = get.loc[t].values
            if drop:
                get.drop(t, axis=0, inplace=True)  # 删除行
        else:
            column = self.get_column(name, True)
            t = column.tolist()[iloc]
            if save:
                get.loc[:, "row"] = self.get_index(name, True)
            get.index = get.loc[:, t].values  # 调整
            if drop:
                get.drop(t, axis=1, inplace=True)  # 删除行
        self.add_sheet(get, f"{name}")
        return get


@plugin_class_loading(get_path(r"template/datascience"))
class SheetSlice(FormBase, metaclass=ABCMeta):
    def get_slice(
        self, name, column, row, is_iloc=True, new=False
    ):  # iloc(Row,Column) or loc
        get = self.get_sheet(name)
        if is_iloc:
            new_sheet = get.iloc[row, column]
        else:
            new_sheet = get.loc[row, column]
        if new:
            self.add_sheet(new_sheet, f"{name}:切片")
        return new_sheet

    def del_slice(self, name, column, row, new):
        new_sheet = self.get_sheet(name)
        column_list = new_sheet.columns.values
        for i in column:
            try:
                new_sheet = new_sheet.drop(column_list[int(i)], axis=1)
            except BaseException as e:
                logging.warning(str(e))
        row_list = new_sheet.index.values
        for i in row:
            try:
                new_sheet = new_sheet.drop(row_list[int(i)])
            except BaseException as e:
                logging.warning(str(e))
        if new:
            self.add_sheet(new_sheet, f"{name}:删减")
        return new_sheet


@plugin_class_loading(get_path(r"template/datascience"))
class DatacleaningFunc(FormBase, metaclass=ABCMeta):
    def add_clean_func(self, code):
        name = self.named_domain.copy()
        exec(code, name)
        func_dict = {
            "Done_Row": name.get("Done_Row", []),
            "Done_Column": name.get("Done_Column", []),
            "axis": name.get("axis", True),
            "check": name.get("check", lambda data, x, b, c, d, e: True),
            "done": name.get("done", lambda data, x, b, c, d, e: data),
        }
        title = (
            f"[{name.get('name', f'[{len(self.clean_func)}')}] Done_Row={func_dict['Done_Row']}_Done_Column="
            f"{func_dict['Done_Column']}_axis={func_dict['axis']}"
        )
        self.clean_func[title] = func_dict
        self.clean_func_code[title] = code

    def get_clean_func(self):
        return list(self.clean_func.keys())

    def del_clean_func(self, key):
        del self.clean_func[key]
        del self.clean_func_code[key]

    def del_all_clean_func(self):
        self.clean_func = {}
        self.clean_func_code = {}

    def get_clean_code(self, key):
        return self.clean_func_code[key]

    def data_clean(self, name):
        get = self.get_sheet(name).copy()
        for i in list(self.clean_func.values()):
            done_row = i["Done_Row"]
            done_column = i["Done_Column"]
            if not done_row:
                done_row = range(get.shape[0])  # shape=[行,列]#不需要回调
            if not done_column:
                done_column = range(get.shape[1])  # shape=[行,列]#不需要回调
            if i["axis"]:
                axis = 0
            else:
                axis = 1
            check = i["check"]
            done = i["done"]
            for row in done_row:
                for column in done_column:
                    try:
                        data = eval(
                            f"get.iloc[{row},{column}]", {"get": get}
                        )  # 第一个是行号，然后是列号
                        column_data = eval(f"get.iloc[{row}]", {"get": get})
                        row_data = eval(f"get.iloc[:,{column}]", {"get": get})
                        if not check(
                            data,
                            row,
                            column,
                            get.copy(),
                            column_data.copy(),
                            row_data.copy(),
                        ):
                            d = done(
                                data,
                                row,
                                column,
                                get.copy(),
                                column_data.copy(),
                                row_data.copy(),
                            )
                            if d == self.DEL:
                                if axis == 0:  # 常规删除
                                    row_list = get.index.values
                                    get = get.drop(row_list[int(row)])
                                else:  # 常规删除
                                    columns_list = get.columns.values
                                    get = get.drop(columns_list[int(row)], axis=1)
                            else:
                                # 第一个是行名，然后是列名
                                exec(f"get.iloc[{row},{column}] = {d}", {"get": get})
                    except BaseException as e:
                        logging.warning(str(e))
        self.add_sheet(get, f"{name}:清洗")
        return get


@plugin_class_loading(get_path(r"template/datascience"))
class SheetDtype(FormBase, metaclass=ABCMeta):
    def set_dtype(self, name, column, dtype, wrong):
        get = self.get_sheet(name).copy()
        for i in range(len(column)):
            try:
                column[i] = int(column[i])
            except BaseException as e:
                logging.warning(str(e))

        if dtype != "":
            func_dic = {
                "Num": pd.to_numeric,
                "Date": pd.to_datetime,
                "Time": pd.to_timedelta,
            }
            if column:
                get.iloc[:, column] = get.iloc[:, column].apply(
                    func_dic.get(dtype, pd.to_numeric), errors=wrong
                )
            else:
                get = get.apply(func_dic.get(dtype, pd.to_numeric), errors=wrong)
        else:
            if column:
                get.iloc[:, column] = get.iloc[:, column].infer_objects()
            else:
                get = get.infer_objects()
        self.add_sheet(get, f"{name}")
        return get

    def as_dtype(self, name, column, dtype, wrong):
        get = self.get_sheet(name).copy()
        for i in range(len(column)):
            try:
                column[i] = int(column[i])
            except BaseException as e:
                logging.warning(str(e))
        func_dic = {
            "Int": int,
            "Float": float,
            "Str": str,
            "Date": pd.Timestamp,
            "TimeDelta": pd.Timedelta,
        }
        if column:
            get.iloc[:, column] = get.iloc[:, column].astype(
                func_dic.get(dtype, dtype), errors=wrong
            )
        else:
            get = get.astype(func_dic.get(dtype, dtype), errors=wrong)
        self.add_sheet(get, f"{name}")
        return get


@plugin_class_loading(get_path(r"template/datascience"))
class DataNan(FormBase, metaclass=ABCMeta):
    def is_nan(self, name):
        get = self.get_sheet(name)
        bool_nan = pd.isna(get)
        return bool_nan

    def del_nan(self, name, new):
        get = self.get_sheet(name)
        clean_sheet = get.dropna(axis=0)
        if new:
            self.add_sheet(clean_sheet, f"{name}:清洗")
        return clean_sheet


@plugin_class_loading(get_path(r"template/datascience"))
class BoolSheet(FormBase, metaclass=ABCMeta):
    def to_bool(self, name, exp, new=False):
        get = self.get_sheet(name)
        bool_sheet = eval(exp, {"S": get, "Sheet": get.iloc})
        if new:
            self.add_sheet(bool_sheet, f"{name}:布尔")
        return bool_sheet


@plugin_class_loading(get_path(r"template/datascience"))
class DataSample(FormBase, metaclass=ABCMeta):
    def sample(self, name, new):
        get = self.get_sheet(name)
        sample = get.sample(frac=1)  # 返回比，默认按行打乱
        if new:
            self.add_sheet(sample, f"{name}:打乱")
        return sample


@plugin_class_loading(get_path(r"template/datascience"))
class DataTranspose(FormBase, metaclass=ABCMeta):
    def transpose(self, name, new=True):
        get = self.get_sheet(name)
        t = get.T.copy()  # 复制一份，防止冲突
        if new:
            self.add_sheet(t, f"{name}.T")
        return t


@plugin_class_loading(get_path(r"template/datascience"))
class PlotBase(
    SheetRender,
    SheetReport,
    RowColumn,
    SheetSlice,
    DatacleaningFunc,
    SheetDtype,
    DataNan,
    BoolSheet,
    DataSample,
    DataTranspose,
    SheetIO,
):
    @staticmethod
    def parsing_parameters(text):  # 解析文本参数
        args = {}  # 解析到的参数
        exec(text, args)
        args_use = {
            "title": args.get("title", None),
            "vice_title": args.get("vice_title", "CoTan~数据处理:"),
            "show_Legend": bool(args.get("show_Legend", True)),
            "ori_Legend": args.get("ori_Legend", "horizontal"),
            "show_Visual_mapping": bool(args.get("show_Visual_mapping", True)),
            "is_color_Visual_mapping": bool(args.get("is_color_Visual_mapping", True)),
            "min_Visual_mapping": args.get("min_Visual_mapping", None),
            "max_Visual_mapping": args.get("max_Visual_mapping", None),
            "color_Visual_mapping": args.get("color_Visual_mapping", None),
            "size_Visual_mapping": args.get("size_Visual_mapping", None),
            "text_Visual_mapping": args.get("text_Visual_mapping", None),
            "is_Subsection": bool(args.get("is_Subsection", False)),
            "Subsection_list": args.get("Subsection_list", []),
            "ori_Visual": args.get("ori_Visual", "vertical"),
            "Tool_BOX": bool(args.get("Tool_BOX", True)),
            "Theme": args.get("Theme", "white"),
            "BG_Color": args.get("BG_Color", None),
            "width": args.get("width", "900px"),
            "heigh": (
                args.get("heigh", "500px")
                if not bool(args.get("Square", False))
                else args.get("width", "900px")
            ),
            "page_Title": args.get("page_Title", ""),
            "show_Animation": args.get("show_Animation", True),
            "show_Axis": bool(args.get("show_Axis", True)),
            "Axis_Zero": bool(args.get("Axis_Zero", False)),
            "show_Axis_Scale": bool(args.get("show_Axis_Scale", True)),
            "x_type": args.get("x_type", None),
            "y_type": args.get("y_type", None),
            "z_type": args.get("z_type", None),
            "make_Line": args.get("make_Line", []),
            "Datazoom": args.get("Datazoom", "N"),
            "show_Text": bool(args.get("show_Text", False)),
            "Size": args.get("Size", 10),
            "Symbol": args.get("Symbol", "circle"),
            "bar_Stacking": bool(args.get("bar_Stacking", False)),
            "EffectScatter": bool(args.get("EffectScatter", False)),
            "connect_None": bool(args.get("connect_None", False)),
            "Smooth_Line": bool(args.get("Smooth_Line", False)),
            "Area_chart": bool(args.get("Area_chart", False)),
            "paste_Y": bool(args.get("paste_Y", False)),
            "step_Line": bool(args.get("step_Line", False)),
            "size_PictorialBar": args.get("size_PictorialBar", None),
            "Polar_units": args.get("Polar_units", "100"),
            "More": bool(args.get("More", False)),
            "WordCould_Size": args.get("WordCould_Size", [20, 100]),
            "WordCould_Shape": args.get("WordCould_Shape", "circle"),
            "symbol_Graph": args.get("symbol_Graph", "circle"),
            "Repulsion": float(args.get("Repulsion", 8000)),
            "Area_radar": bool(args.get("Area_radar", True)),
            "HTML_Type": args.get("HTML_Type", 2),
            "Map": args.get("Map", "china"),
            "show_Map_Symbol": bool(args.get("show_Map_Symbol", False)),
            "Geo_Type": {
                "heatmap": GeoType.HEATMAP,
                "scatter": "scatter",
                "EFFECT": GeoType.EFFECT_SCATTER,
            }.get(args.get("Geo_Type", "heatmap"), GeoType.HEATMAP),
            "map_Type": args.get("map_Type", "2D"),
            "is_Dark": bool(args.get("is_Dark", False)),
        }  # 真实的参数
        # 标题设置，global
        # 图例设置global
        # 视觉映射设置global
        # 工具箱设置global
        # Init设置global
        # 坐标轴设置，2D坐标图和3D坐标图
        # Mark设置 坐标图专属
        # Datazoom设置 坐标图专属

        # 显示文字设置

        # 统一化的设置

        # Bar设置

        # 散点图设置

        # 折线图设置

        return args_use

    @staticmethod
    def global_set(
        args_use, title, min_, max_, data_zoom=False, visual_mapping=True, axis=()
    ):
        k = {}
        # 标题设置
        if args_use["title"] is None:
            args_use["title"] = title
        k["title_opts"] = opts.TitleOpts(
            title=args_use["title"], subtitle=args_use["vice_title"]
        )

        # 图例设置
        if not args_use["show_Legend"]:
            k["legend_opts"] = opts.LegendOpts(is_show=False)
        else:
            k["legend_opts"] = opts.LegendOpts(
                type_="scroll", orient=args_use["ori_Legend"], pos_bottom="2%"
            )  # 移动到底部，避免和标题冲突

        # 视觉映射
        if not args_use["show_Visual_mapping"]:
            pass
        elif not visual_mapping:
            pass
        else:
            if args_use["min_Visual_mapping"] is not None:
                min_ = args_use["min_Visual_mapping"]
            if args_use["max_Visual_mapping"] is not None:
                max_ = args_use["max_Visual_mapping"]
            k["visualmap_opts"] = opts.VisualMapOpts(
                type_="color" if args_use["is_color_Visual_mapping"] else "size",
                max_=max_,
                min_=min_,
                range_color=args_use["color_Visual_mapping"],
                range_size=args_use["size_Visual_mapping"],
                range_text=args_use["text_Visual_mapping"],
                is_piecewise=args_use["is_Subsection"],
                pieces=args_use["Subsection_list"],
                orient=args_use["ori_Visual"],
            )

        k["toolbox_opts"] = opts.ToolboxOpts(is_show=args_use["Tool_BOX"])

        if data_zoom:
            if args_use["Datazoom"] == "all":
                k["datazoom_opts"] = [
                    opts.DataZoomOpts(),
                    opts.DataZoomOpts(orient="horizontal"),
                ]
            elif args_use["Datazoom"] == "horizontal":
                k["datazoom_opts"] = opts.DataZoomOpts(type_="inside")
            elif args_use["Datazoom"] == "vertical":
                opts.DataZoomOpts(orient="vertical")
            elif args_use["Datazoom"] == "inside_vertical":
                opts.DataZoomOpts(type_="inside", orient="vertical")
            elif args_use["Datazoom"] == "inside_vertical":
                opts.DataZoomOpts(type_="inside", orient="horizontal")

        # 坐标轴设定，输入设定的坐标轴即可
        def axis_seeting(args_use_, axis_="x"):
            axis_k = {}
            if args_use_[f"{axis_[0]}_type"] == "Display" or not args_use_["show_Axis"]:
                axis_k[f"{axis_[0]}axis_opts"] = opts.AxisOpts(is_show=False)
            else:
                axis_k[f"{axis_[0]}axis_opts"] = opts.AxisOpts(
                    type_=args_use_[f"{axis_[0]}_type"],
                    axisline_opts=opts.AxisLineOpts(is_on_zero=args_use_["Axis_Zero"]),
                    axistick_opts=opts.AxisTickOpts(
                        is_show=args_use_["show_Axis_Scale"]
                    ),
                )
            return axis_k

        for i in axis:
            k.update(axis_seeting(args_use, i))
        return k

    @staticmethod
    def init_setting(args_use):
        k = {}
        # 设置标题
        if args_use["page_Title"] == "":
            title = "CoTan_数据处理"
        else:
            title = f"CoTan_数据处理:{args_use['page_Title']}"
        k["init_opts"] = opts.InitOpts(
            theme=args_use["Theme"],
            bg_color=args_use["BG_Color"],
            width=args_use["width"],
            height=args_use["heigh"],
            page_title=title,
            animation_opts=opts.AnimationOpts(animation=args_use["show_Animation"]),
        )
        return k

    @staticmethod
    def get_title(args_use):
        return f":{args_use['title']}"

    @staticmethod
    def mark(args_use):
        k = {}
        line = []
        for i in args_use["make_Line"]:
            if i[2] == "c" or i[0] in ("min", "max", "average"):
                line.append(opts.MarkLineItem(type_=i[0], name=i[1]))
            elif i[2] == "x":
                line.append(opts.MarkLineItem(x=i[0], name=i[1]))
            else:
                line.append(opts.MarkLineItem(y=i[0], name=i[1]))
        if not line:
            return k
        k["markline_opts"] = opts.MarkLineOpts(data=line)
        return k

    @staticmethod
    def yaxis_label(args_use, position="inside"):
        return {
            "label_opts": opts.LabelOpts(
                is_show=args_use["show_Text"], position=position
            )
        }

    @staticmethod
    def special_setting(args_use, type_):  # 私人设定
        k = {}
        if type_ == "Bar":  # 设置y的重叠
            if args_use["bar_Stacking"]:
                k = {"stack": "stack1"}
        elif type_ == "Scatter":
            k["Beautiful"] = args_use["EffectScatter"]
            k["symbol"] = args_use["Symbol"]
            k["symbol_size"] = args_use["Size"]
        elif type_ == "Line":
            k["is_connect_nones"] = args_use["connect_None"]
            # 平滑曲线或连接y轴
            k["is_smooth"] = (
                True if args_use["Smooth_Line"] or args_use["paste_Y"] else False
            )
            k["areastyle_opts"] = opts.AreaStyleOpts(
                opacity=0.5 if args_use["Area_chart"] else 0
            )
            if args_use["step_Line"]:
                del k["is_smooth"]
                k["is_step"] = True
        elif type_ == "PictorialBar":
            k["symbol_size"] = args_use["Size"]
        elif type_ == "Polar":
            return args_use["Polar_units"]  # 回复的是单位制而不是设定
        elif type_ == "WordCloud":
            k["word_size_range"] = args_use["WordCould_Size"]  # 放到x轴
            k["shape"] = args_use["Symbol"]  # 放到x轴
        elif type_ == "Graph":
            k["symbol_Graph"] = args_use["Symbol"]  # 放到x轴
        elif type_ == "Radar":  # 雷达图
            k["areastyle_opts"] = opts.AreaStyleOpts(
                opacity=0.1 if args_use["Area_chart"] else 0
            )
            k["symbol"] = args_use["Symbol"]  # 雷达图symbol
        return k


@plugin_class_loading(get_path(r"template/datascience"))
class Render(PlotBase):
    def render_all(self, text, render_dir) -> Page:
        args = self.parsing_parameters(text)
        if args["page_Title"] == "":
            title = "CoTan_数据处理"
        else:
            title = f"CoTan_数据处理:{args['page_Title']}"
        if args["HTML_Type"] == 1:
            page = Page(page_title=title, layout=Page.DraggablePageLayout)
            page.add(*self.all_render.values())
        elif args["HTML_Type"] == 2:
            page = Page(page_title=title, layout=Page.SimplePageLayout)
            page.add(*self.all_render.values())
        else:
            page = Tab(page_title=title)
            for i in self.all_render:
                page.add(self.all_render[i], i)
        page.render(render_dir)
        return render_dir

    def overlap(self, down, up):
        over_down = self.all_render[down]
        over_up = self.all_render[up]
        over_down.overlap(over_up)
        return over_down

    @staticmethod
    def get_random_color():
        # 随机颜色，雷达图默认非随机颜色
        rgb = [randint(0, 255), randint(0, 255), randint(0, 255)]
        color = "#"
        for a in rgb:
            # 转换为16进制,upper表示小写(规范化)
            color += str(hex(a))[-2:].replace("x", "0").upper()
        return color

    def get_all_render(self):
        return self.all_render.copy()

    def del_render(self, key):
        del self.all_render[key]

    def clean_render(self):
        self.all_render = {}

    def custom_graph(self, text):
        named_domain = {}
        named_domain.update(locals())
        named_domain.update(globals())
        exec(text, named_domain)
        exec("c = Page()", named_domain)
        self.all_render[f"自定义图[{len(self.all_render)}]"] = named_domain["c"]
        return named_domain["c"]


@plugin_class_loading(get_path(r"template/datascience"))
class AxisPlot(Render):
    def to_bar(self, name, text) -> Bar:  # Bar:数据堆叠
        get = self.get_sheet(name)
        x = self.get_index(name, True).tolist()
        args = self.parsing_parameters(text)
        c = Bar(**self.init_setting(args)).add_xaxis(
            list(map(str, list(set(x))))
        )  # 转变为str类型
        y = []
        for i in get.iteritems():  # 按列迭代
            q = i[1].tolist()  # 转换为列表
            try:
                c.add_yaxis(
                    f"{name}_{i[0]}",
                    q,
                    **self.special_setting(args, "Bar"),
                    **self.yaxis_label(args),
                    color=self.get_random_color(),
                )  # i[0]是名字，i是tuple，其中i[1]是data
                # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
                y += list(map(int, q))
            except BaseException as e:
                logging.warning(str(e))
        if not y:
            args["show_Visual_mapping"] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(
            **self.global_set(args, f"{name}柱状图", min(y), max(y), True, axis=["x", "y"])
        )
        c.set_series_opts(**self.mark(args))
        self.all_render[f"{name}柱状图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_line(self, name, text) -> Line:  # 折线图：连接空数据、显示数值、平滑曲线、面积图以及紧贴Y轴
        get = self.get_sheet(name)
        x = self.get_index(name, True).tolist()
        args = self.parsing_parameters(text)
        c = Line(**self.init_setting(args)).add_xaxis(
            list(map(str, list(set(x))))
        )  # 转变为str类型
        y = []
        for i in get.iteritems():  # 按列迭代
            q = i[1].tolist()  # 转换为列表
            try:
                c.add_yaxis(
                    f"{name}_{i[0]}",
                    q,
                    **self.special_setting(args, "Line"),
                    **self.yaxis_label(args),
                    color=self.get_random_color(),
                )  # i[0]是名字，i是tuple，其中i[1]是data
                # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
                y += list(map(int, q))
            except BaseException as e:
                logging.warning(str(e))
        if not y:
            args["show_Visual_mapping"] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(
            **self.global_set(args, f"{name}折线图", min(y), max(y), True, axis=["x", "y"])
        )
        c.set_series_opts(**self.mark(args))
        self.all_render[f"{name}折线图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_scatter(self, name, text) -> Scatter:  # 散点图标记形状和大小、特效、标记线
        get = self.get_sheet(name)
        args = self.parsing_parameters(text)
        x = self.get_index(name, True).tolist()
        type_ = self.special_setting(args, "Scatter")
        if type_["Beautiful"]:
            func = EffectScatter
        else:
            func = Scatter
        del type_["Beautiful"]
        c = func(**self.init_setting(args)).add_xaxis(
            list(map(str, list(set(x))))
        )  # 转变为str类型
        y = []
        for i in get.iteritems():  # 按列迭代
            q = i[1].tolist()  # 转换为列表
            try:
                c.add_yaxis(
                    f"{name}_{i[0]}",
                    q,
                    **type_,
                    **self.yaxis_label(args),
                    color=self.get_random_color(),
                )  # i[0]是名字，i是tuple，其中i[1]是data
                # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
                y += list(map(int, q))
            except BaseException as e:
                logging.warning(str(e))
        if not y:
            args["show_Visual_mapping"] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(
            **self.global_set(args, f"{name}散点图", min(y), max(y), True, axis=["x", "y"])
        )
        c.set_series_opts(**self.mark(args))
        self.all_render[f"{name}散点图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_pictorialbar(self, name, text) -> PictorialBar:  # 象形柱状图：图形、剪裁图像、元素重复和间隔
        get = self.get_sheet(name)
        x = self.get_index(name, True).tolist()
        args = self.parsing_parameters(text)
        c = (
            PictorialBar(**self.init_setting(args))
            .add_xaxis(list(map(str, list(set(x)))))  # 转变为str类型
            .reversal_axis()
        )
        y = []
        k = self.special_setting(args, "PictorialBar")
        for i in get.iteritems():  # 按列迭代
            q = i[1].tolist()  # 转换为列表
            try:
                c.add_yaxis(
                    f"{name}_{i[0]}",
                    q,
                    label_opts=opts.LabelOpts(is_show=False),
                    symbol_repeat=True,
                    is_symbol_clip=True,
                    symbol=SymbolType.ROUND_RECT,
                    **k,
                    color=self.get_random_color(),
                )
                # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
                y += list(map(int, q))
            except BaseException as e:
                logging.warning(str(e))
        if not y:
            args["show_Visual_mapping"] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(
            **self.global_set(
                args, f"{name}象形柱状图", min(y), max(y), True, axis=["x", "y"]
            )
        )
        c.set_series_opts(**self.mark(args))
        self.all_render[f"{name}[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_boxpolt(self, name, text) -> Boxplot:
        get = self.get_sheet(name)
        args = self.parsing_parameters(text)
        c = Boxplot(**self.init_setting(args)).add_xaxis([f"{name}"])
        y = []
        for i in get.iteritems():  # 按列迭代
            q = i[1].tolist()  # 转换为列表
            try:
                c.add_yaxis(f"{name}_{i[0]}", [q], **self.yaxis_label(args))
                # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
                y += list(map(float, q))
            except BaseException as e:
                logging.warning(str(e))
        if not y:
            args["show_Visual_mapping"] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(
            **self.global_set(args, f"{name}箱形图", min(y), max(y), True, axis=["x", "y"])
        )
        c.set_series_opts(**self.mark(args))
        self.all_render[f"{name}箱形图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_heatmap(self, name, text) -> HeatMap:  # 显示数据
        get = self.get_sheet(name)
        x = self.get_column(name, True).tolist()  # 图的x轴，下侧，列名
        y = self.get_index(name, True).tolist()  # 图的y轴，左侧，行名
        value_list = []
        q = []
        for c in range(len(x)):  # c-列，r-行
            for r in range(len(y)):
                try:
                    v = float(eval(f"get.iloc[{r},{c}]", {"get": get}))  # 先行后列
                except ValueError:
                    continue
                q.append(v)
                value_list.append([c, r, v])
        args = self.parsing_parameters(text)
        try:
            max_, min_ = max(q), min(q)
        except TypeError:
            args["show_Visual_mapping"] = False  # 关闭视觉映射
            max_, min_ = 0, 100
        c = (
            HeatMap(**self.init_setting(args))
            .add_xaxis(list(map(str, list(set(x)))))  # 转变为str类型
            .add_yaxis(
                f"{name}", list(map(str, y)), value_list, **self.yaxis_label(args)
            )
            .set_global_opts(
                **self.global_set(args, f"{name}热力图", min_, max_, True, axis=["x", "y"])
            )
            .set_series_opts(**self.mark(args))
        )
        self.all_render[f"{name}热力图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c


@plugin_class_loading(get_path(r"template/datascience"))
class GeneralPlot(Render):
    def to_format_graph(self, name, text) -> Graph:
        get = self.get_sheet(name)
        y_name = self.get_index(name, True).tolist()  # 拿行名
        nodes = []
        link = []
        for i in get.iterrows():  # 按行迭代
            q = i[1].tolist()  # 转换为列表
            try:
                nodes.append(
                    {"name": f"{i[0]}", "symbolSize": float(q[0]), "value": float(q[0])}
                )
                for a in q[1:]:
                    n = str(a).split(":")
                    try:
                        link.append(
                            {"source": f"{i[0]}", "target": n[0], "value": float(n[1])}
                        )
                    except BaseException as e:
                        logging.warning(str(e))
            except BaseException as e:
                logging.warning(str(e))
        if not link:
            for i in nodes:
                for j in nodes:
                    link.append(
                        {
                            "source": i.get("name"),
                            "target": j.get("name"),
                            "value": abs(i.get("value") - j.get("value")),
                        }
                    )
        args = self.parsing_parameters(text)
        c = (
            Graph(**self.init_setting(args))
            .add(
                f"{y_name[0]}",
                nodes,
                link,
                repulsion=args["Repulsion"],
                **self.yaxis_label(args),
            )
            .set_global_opts(
                **self.global_set(args, f"{name}关系图", 0, 100, False, False)
            )
        )
        self.all_render[f"{name}关系图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_graph(self, name, text) -> Graph:  # XY关系图，新的书写方式
        get = self.get_sheet(name)
        args = self.parsing_parameters(text)
        size = args["Size"] * 3

        # 生成节点信息
        y_name = self.get_index(name, True).tolist()  # 拿行名
        x_name = self.get_column(name, True).tolist()  # 拿列名
        nodes_list = list(set(y_name + x_name))  # 处理重复，作为nodes列表
        nodes = []
        for i in nodes_list:
            nodes.append({"name": f"{i}", "symbolSize": size})

        # 生成link信息
        link = []  # 记录连接的信息
        have = []
        for y in range(len(y_name)):  # 按行迭代
            for x in range(len(x_name)):
                y_n = y_name[y]  # 节点1
                x_n = x_name[x]  # 节点2
                if y_n == x_n:
                    continue
                if (y_n, x_n) in have or (x_n, y_n) in have:
                    continue
                else:
                    have.append((y_n, x_n))
                try:
                    v = float(eval(f"get.iloc[{y},{x}]", {"get": get}))  # 取得value
                    link.append({"source": y_n, "target": x_n, "value": v})
                except BaseException as e:
                    logging.warning(str(e))
        c = (
            Graph(**self.init_setting(args))
            .add(
                f"{y_name[0]}",
                nodes,
                link,
                repulsion=args["Repulsion"],
                **self.yaxis_label(args),
            )
            .set_global_opts(
                **self.global_set(args, f"{name}关系图", 0, 100, False, False)
            )
        )
        self.all_render[f"{name}关系图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_sankey(self, name, text):
        get = self.get_sheet(name)
        args = self.parsing_parameters(text)

        # 生成节点信息
        y_name = self.get_index(name, True).tolist()  # 拿行名
        x_name = self.get_column(name, True).tolist()  # 拿列名
        nodes_list = list(set(y_name + x_name))  # 处理重复，作为nodes列表
        nodes = []
        source = {}
        target = {}
        for i in nodes_list:
            nodes.append({"name": f"{i}"})
            source[i] = set()  # 记录该元素source边连接的节点
            target[i] = set()  # 记录改元素target边连接的节点

        # 生成link信息
        link = []  # 记录连接的信息
        have = []
        for y in range(len(y_name)):  # 按行迭代
            for x in range(len(x_name)):
                y_n = y_name[y]  # 节点1
                x_n = x_name[x]  # 节点2
                if y_n == x_n:
                    continue  # 是否相同
                if (y_n, x_n) in have or (x_n, y_n) in have:
                    continue  # 是否重复
                else:
                    have.append((y_n, x_n))
                # 固定的，y在s而x在t，桑基图不可以绕环形，所以要做检查
                if source[y_n] & target[x_n] != set():
                    continue
                try:
                    v = float(eval(f"get.iloc[{y},{x}]", {"get": get}))  # 取得value
                    link.append({"source": y_n, "target": x_n, "value": v})
                    target[y_n].add(x_n)
                    source[x_n].add(y_n)
                except BaseException as e:
                    logging.warning(str(e))
        c = (
            Sankey()
            .add(
                f"{name}",
                nodes,
                link,
                linestyle_opt=opts.LineStyleOpts(
                    opacity=0.2, curve=0.5, color="source"
                ),
                label_opts=opts.LabelOpts(position="right"),
            )
            .set_global_opts(
                **self.global_set(args, f"{name}桑基图", 0, 100, False, False)
            )
        )
        self.all_render[f"{name}桑基图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_parallel(self, name, text) -> Parallel:
        get = self.get_sheet(name)
        dim = []
        dim_list = self.get_index(name, True).tolist()
        for i in range(len(dim_list)):
            dim.append({"dim": i, "name": f"{dim_list[i]}"})
        args = self.parsing_parameters(text)
        c = (
            Parallel(**self.init_setting(args))
            .add_schema(dim)
            .set_global_opts(
                **self.global_set(args, f"{name}多轴图", 0, 100, False, False)
            )
        )
        for i in get.iteritems():  # 按列迭代
            q = i[1].tolist()  # 转换为列表
            c.add(f"{i[0]}", [q], **self.yaxis_label(args))
        self.all_render[f"{name}多轴图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_pie(self, name, text) -> Pie:
        get = self.get_sheet(name)
        data = []
        for i in get.iterrows():  # 按行迭代
            try:
                data.append([f"{i[0]}", float(i[1].tolist()[0])])
            except BaseException as e:
                logging.warning(str(e))
        args = self.parsing_parameters(text)
        c = (
            Pie(**self.init_setting(args))
            .add(f"{name}", data, **self.yaxis_label(args, "top"))
            .set_global_opts(**self.global_set(args, f"{name}饼图", 0, 100, False, False))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        self.all_render[f"{name}饼图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_polar(self, name, text) -> Polar:
        get = self.get_sheet(name)
        data = []
        args = self.parsing_parameters(text)
        setting = self.special_setting(args, "Polar")
        if setting == "rad":  # 弧度制
            convert = 0.0628
        elif setting == "360":  # 角度制
            convert = 0.36
        else:
            convert = 1
        for i in get.iterrows():  # 按行迭代
            try:
                q = i[1].tolist()
                data.append((float(q[0]), float(q[1]) / convert))
            except BaseException as e:
                logging.warning(str(e))
        c = (
            Polar(**self.init_setting(args))
            .add(f"{name}", data, type_="scatter", **self.yaxis_label(args))
            .set_global_opts(
                **self.global_set(args, f"{name}极坐标图", 0, 100, False, False)
            )
        )
        self.all_render[f"{name}极坐标图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_radar(self, name, text) -> Radar:
        get = self.get_sheet(name)
        x = self.get_index(name, True).tolist()
        max_list = [[] for _ in range(len(x))]  # 保存每个x栏目的最大值
        data = []  # y的组成数据，包括name和list
        x_list = []  # 保存x的数据

        for i in get.iteritems():  # 按列迭代计算每一项的abcd
            q = i[1].tolist()
            add = []
            for a in range(len(q)):
                try:
                    f = float(q[a])
                    max_list[a].append(f)
                    add.append(f)
                except BaseException as e:
                    logging.warning(str(e))
            data.append([f"{i[0]}", [add]])  # add是包含在一个list中的

        for i in range(len(max_list)):  # 计算x_list
            x_list.append(opts.RadarIndicatorItem(name=x[i], max_=max(max_list[i])))
        args = self.parsing_parameters(text)
        c = (
            Radar(**self.init_setting(args))
            .add_schema(schema=x_list)
            .set_global_opts(
                **self.global_set(args, f"{name}雷达图", 0, 100, False, False)
            )
        )
        k = self.special_setting(args, "Radar")
        for i in data:
            c.add(
                *i, **self.yaxis_label(args), color=self.get_random_color(), **k
            )  # 对i解包，取得name和data 随机颜色
        self.all_render[f"{name}雷达图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_funnel(self, name, text) -> Funnel:
        get = self.get_sheet(name)
        y_name = self.get_index(name, True).tolist()  # 拿行名
        value = []
        y = []
        for r in range(len(y_name)):
            try:
                v = float(eval(f"get.iloc[{r},0]", {"get": get}))
            except ValueError:
                continue
            value.append([f"{y_name[r]}", v])
            y.append(v)
        args = self.parsing_parameters(text)
        c = (
            Funnel(**self.init_setting(args))
            .add(f"{name}", value, **self.yaxis_label(args, "top"))
            .set_global_opts(
                **self.global_set(args, f"{name}漏斗图", min(y), max(y), True, False)
            )
        )
        self.all_render[f"{name}漏斗图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_calendar(self, name, text) -> Calendar:
        get = self.get_sheet(name)
        data = [[] for _ in self.get_column(name, True)]
        x_name = self.get_column(name, True).tolist()
        y = []
        for i in get.iterrows():
            date = str(i[0])  # 时间数据
            q = i[1].tolist()
            for a in range(len(q)):
                try:
                    data[a].append([date, q[a]])
                    y.append(float(q[a]))
                except BaseException as e:
                    logging.warning(str(e))
        args = self.parsing_parameters(text)
        if not y:
            y = [0, 100]
            args["show_Visual_mapping"] = False  # 关闭视觉映射
        c = Calendar(**self.init_setting(args)).set_global_opts(
            **self.global_set(args, f"{name}日历图", min(y), max(y), True)
        )
        for i in range(len(x_name)):
            start_date = data[i][0][0]
            end_date = data[i][-1][0]
            c.add(
                str(x_name[i]),
                data[i],
                calendar_opts=opts.CalendarOpts(range_=[start_date, end_date]),
                **self.yaxis_label(args),
            )
        self.all_render[f"{name}日历图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_theme_river(self, name, text) -> ThemeRiver:
        get = self.get_sheet(name)
        data = []
        x_name = self.get_column(name, True).tolist()
        y = []
        for i in get.iterrows():
            date = str(i[0])
            q = i[1].tolist()
            for a in range(len(x_name)):
                try:
                    data.append([date, q[a], x_name[a]])
                    y.append(float(q[a]))
                except BaseException as e:
                    logging.warning(str(e))
        args = self.parsing_parameters(text)
        if not y:
            y = [0, 100]
            args["show_Visual_mapping"] = False  # 关闭视觉映射
        c = (
            ThemeRiver(**self.init_setting(args))
            # 抑制大小
            .add(
                x_name,
                data,
                singleaxis_opts=opts.SingleAxisOpts(
                    type_=args["x_type"], pos_bottom="10%"
                ),
            ).set_global_opts(
                **self.global_set(args, f"{name}河流图", min(y), max(y), True, False)
            )
        )
        self.all_render[f"{name}河流图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c


@plugin_class_loading(get_path(r"template/datascience"))
class RelationshipPlot(Render):
    def to_sunburst(self, name, text) -> Sunburst:
        get = self.get_sheet(name)

        def convert_data(iter_object, name_):
            k = {"name": name_, "children": []}
            v = 0
            for i in iter_object:
                content = iter_object[i]
                if isinstance(content, dict):
                    new_c = convert_data(content, str(i))
                    v += new_c["value"]
                    k["children"].append(new_c)
                else:
                    try:
                        q = float(content)
                    except ValueError:
                        q = len(str(content))
                    v += q
                    k["children"].append({"name": f"{i}={content}", "value": q})
            k["value"] = v
            return k

        data = convert_data(get.to_dict(), name)["children"]
        args = self.parsing_parameters(text)
        c = (
            Sunburst()
            .add(
                series_name=f"{name}",
                data_pair=data,
                radius=[abs(args["Size"] - 10), "90%"],
            )
            .set_global_opts(
                **self.global_set(args, f"{name}旭日图", 0, 100, False, False)
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
        )
        self.all_render[f"{name}旭日图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_tree(self, name, text) -> Tree:
        get = self.get_sheet(name)

        def convert_data(iter_object, name_):
            k = {"name": name_, "children": []}
            for i in iter_object:
                content = iter_object[i]
                if isinstance(content, dict):
                    new_children = convert_data(content, str(i))
                    k["children"].append(new_children)
                else:
                    k["children"].append(
                        {"name": f"{i}", "children": [{"name": f"{content}"}]}
                    )
            return k

        data = [convert_data(get.to_dict(), name)]
        args = self.parsing_parameters(text)
        c = (
            Tree()
            .add(f"{name}", data)
            .set_global_opts(
                **self.global_set(args, f"{name}树状图", 0, 100, False, False)
            )
        )
        self.all_render[f"{name}树状图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_tree_map(self, name, text) -> TreeMap:
        get = self.get_sheet(name)

        def convert_data(iter_object, name_):
            k = {"name": name_, "children": []}
            v = 0
            for i in iter_object:
                content = iter_object[i]
                if isinstance(content, dict):
                    new_c = convert_data(content, str(i))
                    v += new_c["value"]
                    k["children"].append(new_c)
                else:
                    try:
                        q = float(content)
                    except ValueError:
                        q = len(str(content))
                    v += q
                    k["children"].append({"name": f"{i}={content}", "value": q})
            k["value"] = v
            return k

        data = convert_data(get.to_dict(), name)["children"]
        args = self.parsing_parameters(text)
        c = (
            TreeMap()
            .add(
                f"{name}",
                data,
                label_opts=opts.LabelOpts(is_show=True, position="inside"),
            )
            .set_global_opts(
                **self.global_set(args, f"{name}矩形树图", 0, 100, False, False)
            )
        )
        self.all_render[f"{name}矩形树图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_scattergeo(self, name, text) -> Geo:
        get = self.get_sheet(name)
        column = self.get_column(name, True).tolist()
        data_type = ["scatter" for _ in column]
        data = [[] for _ in column]
        y = []
        for i in get.iterrows():  # 按行迭代
            map_ = str(i[0])
            q = i[1].tolist()
            for a in range(len(q)):
                try:
                    v = float(q[a])
                    y.append(v)
                except ValueError:
                    v = str(q[a])
                    try:
                        if v[:5] == "[##S]":
                            # 特效图
                            v = float(v[5:])
                            y.append(v)
                            column.append(column[a])
                            data_type.append(GeoType.EFFECT_SCATTER)
                            data.append([])
                            a = -1
                        elif v[:5] == "[##H]":
                            # 特效图
                            v = float(v[5:])
                            y.append(v)
                            column.append(column[a])
                            data_type.append(GeoType.HEATMAP)
                            data.append([])
                            a = -1
                        else:
                            assert False
                    except (AssertionError, ValueError):
                        data_type[a] = GeoType.LINES  # 当前变为Line
                data[a].append((map_, v))
        args = self.parsing_parameters(text)
        args["show_Visual_mapping"] = True  # 必须视觉映射
        if not y:
            y = [0, 100]
        if args["is_Dark"]:
            g = {
                "itemstyle_opts": opts.ItemStyleOpts(
                    color="#323c48", border_color="#111"
                )
            }
        else:
            g = {}
        c = (
            Geo().add_schema(maptype=str(args["Map"]), **g)
            # 必须要有视觉映射(否则会显示奇怪的数据)
            .set_global_opts(
                **self.global_set(args, f"{name}Geo点地图", min(y), max(y), False)
            )
        )
        for i in range(len(data)):
            if data_type[i] != GeoType.LINES:
                ka = dict(
                    symbol=args["Symbol"],
                    symbol_size=args["Size"],
                    color="#1E90FF" if args["is_Dark"] else "#0000FF",
                )
            else:
                ka = dict(
                    symbol=SymbolType.ARROW,
                    symbol_size=6,
                    effect_opts=opts.EffectOpts(
                        symbol=SymbolType.ARROW, symbol_size=6, color="blue"
                    ),
                    linestyle_opts=opts.LineStyleOpts(
                        curve=0.2, color="#FFF8DC" if args["is_Dark"] else "#000000"
                    ),
                )
            c.add(f"{column[i]}", data[i], type_=data_type[i], **ka)
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示数据,必须放在add后面生效
        self.all_render[
            f"{name}Geo点地图[{len(self.all_render)}]{self.get_title(args)}"
        ] = c
        return c


@plugin_class_loading(get_path(r"template/datascience"))
class GeographyPlot(Render):
    def to_map(self, name, text) -> Map:
        get = self.get_sheet(name)
        column = self.get_column(name, True).tolist()
        data = [[] for _ in column]
        y = []
        for i in get.iterrows():  # 按行迭代
            map_ = str(i[0])
            q = i[1].tolist()
            for a in range(len(q)):
                try:
                    v = float(q[a])
                    y.append(v)
                    data[a].append((map_, v))
                except BaseException as e:
                    logging.warning(str(e))
        args = self.parsing_parameters(text)
        args["show_Visual_mapping"] = True  # 必须视觉映射
        if not y:
            y = [0, 100]
        if args["map_Type"] == "GLOBE":
            func = MapGlobe
        else:
            func = Map
        c = func().set_global_opts(
            **self.global_set(args, f"{name}Map地图", min(y), max(y), False)
        )  # 必须要有视觉映射(否则会显示奇怪的数据)
        for i in range(len(data)):
            c.add(
                f"{column[i]}",
                data[i],
                str(args["Map"]),
                is_map_symbol_show=args["show_Map_Symbol"],
                symbol=args["Symbol"],
                **self.yaxis_label(args),
            )
        self.all_render[
            f"{name}Map地图[{len(self.all_render)}]{self.get_title(args)}"
        ] = c
        return c

    def to_geo(self, name, text) -> Geo:
        get = self.get_sheet(name)
        column = self.get_column(name, True).tolist()
        index = self.get_index(name, True).tolist()
        args = self.parsing_parameters(text)
        args["show_Visual_mapping"] = True  # 必须视觉映射
        if args["is_Dark"]:
            g = {
                "itemstyle_opts": opts.ItemStyleOpts(
                    color="#323c48", border_color="#111"
                )
            }
        else:
            g = {}
        c = Geo().add_schema(maptype=str(args["Map"]), **g)
        m = []
        for y in column:  # 维度
            for x in index:  # 精度
                value = get.loc[x, y]
                type_ = "scatter"
                try:
                    v = float(value)  # 数值
                    type_ = args["Geo_Type"]
                except ValueError:
                    try:
                        q = str(value)
                        v = float(value[5:])
                        if q[:5] == "[##S]":  # 点图
                            type_ = GeoType.SCATTER
                        elif q[:5] == "[##E]":  # 带点特效
                            type_ = GeoType.EFFECT_SCATTER
                        else:  # 画线
                            v = q.split(";")
                            c.add_coordinate(
                                name=f"({v[0]},{v[1]})",
                                longitude=float(v[0]),
                                latitude=float(v[1]),
                            )
                            c.add_coordinate(
                                name=f"({x},{y})", longitude=float(x), latitude=float(y)
                            )
                            c.add(
                                f"{name}",
                                [[f"({x},{y})", f"({v[0]},{v[1]})"]],
                                type_=GeoType.LINES,
                                effect_opts=opts.EffectOpts(
                                    symbol=SymbolType.ARROW, symbol_size=6, color="blue"
                                ),
                                linestyle_opts=opts.LineStyleOpts(
                                    curve=0.2,
                                    color="#FFF8DC" if args["is_Dark"] else "#000000",
                                ),
                            )
                            c.add(
                                f"{name}_XY",
                                [[f"({x},{y})", 5], [f"({v[0]},{v[1]})", 5]],
                                type_=GeoType.EFFECT_SCATTER,
                                color="#1E90FF" if args["is_Dark"] else "#0000FF",
                            )
                            assert False  # continue
                    except (ValueError, TypeError, AssertionError):
                        continue
                try:
                    c.add_coordinate(
                        name=f"({x},{y})", longitude=float(x), latitude=float(y)
                    )
                    c.add(
                        f"{name}",
                        [[f"({x},{y})", v]],
                        type_=type_,
                        symbol=args["Symbol"],
                        symbol_size=args["Size"],
                    )
                    if type_ == GeoType.HEATMAP:
                        c.add(
                            f"{name}_XY",
                            [[f"({x},{y})", v]],
                            type_="scatter",
                            color="#1E90FF" if args["is_Dark"] else "#0000FF",
                        )
                    m.append(v)
                except BaseException as e:
                    logging.warning(str(e))
        if not m:
            m = [0, 100]
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示
        c.set_global_opts(
            **self.global_set(args, f"{name}Geo地图", min(m), max(m), False)
        )
        self.all_render[
            f"{name}Geo地图[{len(self.all_render)}]{self.get_title(args)}"
        ] = c
        return c


@plugin_class_loading(get_path(r"template/datascience"))
class WordPlot(Render):
    def to_word_cloud(self, name, text) -> WordCloud:
        get = self.get_sheet(name)
        data = []
        for i in get.iterrows():  # 按行迭代
            try:
                data.append([str(i[0]), float(i[1].tolist()[0])])
            except BaseException as e:
                logging.warning(str(e))
        args = self.parsing_parameters(text)
        c = (
            WordCloud(**self.init_setting(args))
            .add(f"{name}", data, **self.special_setting(args, "WordCloud"))
            .set_global_opts(**self.global_set(args, f"{name}词云", 0, 100, False, False))
        )
        self.all_render[f"{name}词云[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_liquid(self, name, text) -> Liquid:
        get = self.get_sheet(name)
        data = str(get.iloc[0, 0])
        c = data.split(".")
        try:
            data = float(f"0.{c[1]}")
        except ValueError:
            data = float(f"0.{c[0]}")
        args = self.parsing_parameters(text)
        c = (
            Liquid(**self.init_setting(args))
            .add(f"{name}", [data, data])
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"{name}水球图", subtitle="CoTan~数据处理")
            )
        )
        self.all_render[f"{name}水球图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c

    def to_gauge(self, name, text) -> Gauge:
        get = self.get_sheet(name)
        data = float(get.iloc[0, 0])
        if data > 100:
            data = str(data / 100)
            c = data.split(".")
            try:
                data = float(f"0.{c[1]}") * 100
            except ValueError:
                data = float(f"0.{data}") * 100
        args = self.parsing_parameters(text)
        c = (
            Gauge(**self.init_setting(args))
            .add(f"{name}", [(f"{name}", data)])
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"{name}仪表图", subtitle="CoTan~数据处理")
            )
        )
        self.all_render[f"{name}仪表图[{len(self.all_render)}]{self.get_title(args)}"] = c
        return c


@plugin_class_loading(get_path(r"template/datascience"))
class SolidPlot(Render):
    def to_bar3d(self, name, text) -> Bar3D:
        get = self.get_sheet(name)
        x = self.get_column(name, True).tolist()  # 图的x轴，下侧，列名
        y = self.get_index(name, True).tolist()  # 图的y轴，左侧，行名
        value_list = []
        q = []
        for c in range(len(x)):  # c-列，r-行
            for r in range(len(y)):
                try:
                    v = eval(f"get.iloc[{r},{c}]", {"get": get})  # 先行后列
                    value_list.append([c, r, v])
                    q.append(float(v))
                except BaseException as e:
                    logging.warning(str(e))
        args = self.parsing_parameters(text)
        if not q:
            q = [0, 100]
            args["show_Visual_mapping"] = False  # 关闭视觉映射
        c = (
            Bar3D(**self.init_setting(args))
            .add(
                f"{name}",
                value_list,
                xaxis3d_opts=opts.Axis3DOpts(list(map(str, x)), type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(list(map(str, y)), type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
            )
            .set_global_opts(
                **self.global_set(args, f"{name}3D柱状图", min(q), max(q), True),
            )
        )
        if args["bar_Stacking"]:
            c.set_series_opts(**{"stack": "stack"})  # 层叠
        self.all_render[
            f"{name}3D柱状图[{len(self.all_render)}]{self.get_title(args)}"
        ] = c
        return c

    def to_scatter3d(self, name, text) -> Scatter3D:
        get = self.get_sheet(name)
        x = self.get_column(name, True).tolist()  # 图的x轴，下侧，列名
        y = self.get_index(name, True).tolist()  # 图的y轴，左侧，行名
        value_list = []
        q = []
        for c in range(len(x)):  # c-列，r-行
            for r in range(len(y)):
                try:
                    v = eval(f"get.iloc[{r},{c}]", {"get": get})  # 先行后列
                    value_list.append([c, r, v])
                    q.append(float(v))
                except BaseException as e:
                    logging.warning(str(e))
        args = self.parsing_parameters(text)
        if not q:
            q = [0, 100]
            args["show_Visual_mapping"] = False  # 关闭视觉映射
        c = (
            Scatter3D(**self.init_setting(args))
            .add(
                f"{name}",
                value_list,
                xaxis3d_opts=opts.Axis3DOpts(list(map(str, x)), type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(list(map(str, y)), type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
            )
            .set_global_opts(
                **self.global_set(args, f"{name}3D散点图", min(q), max(q), True)
            )
        )
        self.all_render[
            f"{name}3D散点图[{len(self.all_render)}]{self.get_title(args)}"
        ] = c
        return c

    def to_line3d(self, name, text) -> Line3D:
        get = self.get_sheet(name)
        x = self.get_column(name, True).tolist()  # 图的x轴，下侧，列名
        y = self.get_index(name, True).tolist()  # 图的y轴，左侧，行名
        value_list = []
        q = []
        for c in range(len(x)):  # c-列，r-行
            for r in range(len(y)):
                try:
                    v = eval(f"get.iloc[{r},{c}]", {"get": get})  # 先行后列
                    value_list.append([c, r, v])
                    q.append(float(v))
                except BaseException as e:
                    logging.warning(str(e))
        args = self.parsing_parameters(text)
        if not q:
            q = [0, 100]
            args["show_Visual_mapping"] = False  # 关闭视觉映射
        c = (
            Line3D(**self.init_setting(args))
            .add(
                f"{name}",
                value_list,
                xaxis3d_opts=opts.Axis3DOpts(list(map(str, x)), type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(list(map(str, y)), type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
                grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
            )
            .set_global_opts(
                **self.global_set(args, f"{name}3D折线图", min(q), max(q), True)
            )
        )
        self.all_render[
            f"{name}3D折线图[{len(self.all_render)}]{self.get_title(args)}"
        ] = c
        return c


class MachineLearnerBase(
    AxisPlot, GeneralPlot, RelationshipPlot, GeographyPlot, WordPlot, SolidPlot
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.learner = {}  # 记录机器
        self.learn_dict = {
            "Line": (LinearRegression, ()),
            "Ridge": (Ridge, ("alpha", "max_iter",)),
            "Lasso": (Lasso, ("alpha", "max_iter",)),
            "LogisticRegression": (LogisticRegression, ("C",)),
            "Knn": (KNeighborsClassifier, ("n_neighbors",)),
            "Knn_class": (KNeighborsRegressor, ("n_neighbors",)),
        }
        self.learner_type = {}  # 记录机器的类型

    @staticmethod
    def parsing(parameters):  # 解析参数
        args = {}
        args_use = {}
        # 输入数据
        exec(parameters, args)
        # 处理数据
        args_use["alpha"] = float(args.get("alpha", 1.0))  # L1和L2正则化用
        args_use["C"] = float(args.get("C", 1.0))  # L1和L2正则化用
        args_use["max_iter"] = int(args.get("max_iter", 1000))  # L1和L2正则化用
        args_use["n_neighbors"] = int(args.get("K_knn", 5))  # knn邻居数 (命名不同)
        args_use["nDim_2"] = bool(args.get("nDim_2", True))  # 数据是否降维
        return args_use

    def get_learner(self, name):
        return self.learner[name]

    def get_learner_type(self, name):
        return self.learner_type[name]


@plugin_class_loading(get_path(r"template/datascience"))
class VisualLearner(MachineLearnerBase):
    def visual_learner(self, learner, new=False):  # 显示参数
        learner = self.get_learner(learner)
        learner_type = self.get_learner_type(learner)
        if learner_type in ("Ridge", "Lasso"):
            alpha = learner.alpha  # 阿尔法
            w = learner.coef_.tolist()  # w系数
            b = learner.intercept_  # 截距
            max_iter = learner.max_iter
            w_name = [f"权重:W[{i}]" for i in range(len(w))]
            index = ["阿尔法:Alpha"] + w_name + ["截距:b", "最大迭代数"]
            data = [alpha] + w + [b] + [max_iter]
            # 文档
            doc = (
                f"阿尔法:alpha = {alpha}\n\n权重:\nw = \n{pd.DataFrame(w)}\n\n截距:b = {b}\n\n最大迭代数:{max_iter}"
                f"\n\n\nEND"
            )
            data = pd.DataFrame(data, index=index)
        elif learner_type in ("Line",):
            w = learner.coef_.tolist()  # w系数
            b = learner.intercept_
            index = [f"权重:W[{i}]" for i in range(len(w))] + ["截距:b"]
            data = w + [b]  # 截距
            # 文档
            doc = f"权重:w = \n{pd.DataFrame(w)}\n\n截距:b = {b}\n\n\nEND"
            data = pd.DataFrame(data, index=index)
        elif learner_type in ("Knn",):  # Knn_class
            classes = learner.classes_.tolist()  # 分类
            n = learner.n_neighbors  # 个数
            p = {1: "曼哈顿距离", 2: "欧几里得距离"}.get(learner.p)
            index = [f"类目[{i}]" for i in range(len(classes))] + ["邻居个数", "距离公式"]
            data = classes + [n, p]
            doc = f"分类类目:\n{pd.DataFrame(classes)}\n\n邻居个数:{n}\n\n计算距离的方式:{p}\n\n\nEND"
            data = pd.DataFrame(data, index=index)
        elif learner_type in ("Knn_class",):
            n = learner.n_neighbors  # 个数
            p = {1: "曼哈顿距离", 2: "欧几里得距离"}.get(learner.p)
            index = ["邻居个数", "距离公式"]
            data = [n, p]
            doc = f"邻居个数:{n}\n\n计算距离的方式:{p}\n\n\nEND"
            data = pd.DataFrame(data, index=index)
        elif learner_type in ("LogisticRegression",):
            classes = learner.classes_.tolist()  # 分类
            w = learner.coef_.tolist()  # w系数
            b = learner.intercept_
            c = learner.C
            index = (
                [f"类目[{i}]" for i in range(len(classes))]
                + [f"权重:W[{j}][{i}]" for i in range(len(w)) for j in range(len(w[i]))]
                + [f"截距:b[{i}]" for i in range(len(b))]
                + ["C"]
            )
            data = classes + [j for i in w for j in i] + [i for i in b] + [c]
            doc = f"分类类目:\n{pd.DataFrame(classes)}\n\n权重:w = \n{pd.DataFrame(w)}\n\n截距:b = {b}\n\nC={c}\n\n\n"
            data = pd.DataFrame(data, index=index)
        else:
            return "", []
        if new:
            self.add_sheet(data, f"{learner}:属性")
        return doc, data


@plugin_class_loading(get_path(r"template/datascience"))
class Learner(MachineLearnerBase):
    def decision_tree_classifier(self, name):  # 特征提取
        get = self.get_sheet(name)
        dver = DictVectorizer()
        get_dic = get.to_dict(orient="records")
        new = dver.fit_transform(get_dic).toarray()
        dec = pd.DataFrame(new, columns=dver.feature_names_)
        self.add_sheet(dec, f"{name}:特征")
        return dec

    def training_machine_core(
        self, name, learner, score_only=False, down_ndim=True, split=0.3, **kwargs
    ):
        get = self.get_sheet(name)
        x = get.to_numpy()
        y = self.get_index(name, True)  # 获取y值(用index作为y)
        if down_ndim or x.ndim == 1:  # 执行降维处理（也包括升维，ravel让一切变成一维度，包括数字）
            a = x
            x = []
            for i in a:
                try:
                    c = i.np.ravel(a[i], "C")
                    x.append(c)
                except ValueError:
                    x.append(i)
            x = np.array(x)
        model = self.get_learner(learner)
        if not score_only:  # 只计算得分，全部数据用于测试
            train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=split)
            model.fit(train_x, train_y)
            train_score = model.score(train_x, train_y)
            test_score = model.score(test_x, test_y)
            return train_score, test_score
        test_score = model.score(x, y)
        return 0, test_score

    def training_machine(self, name, learnner, parameters="", **kwargs):
        type_ = self.get_learner_type(learnner)
        args_use = self.parsing(parameters)
        if type_ in (
            "Line",
            "Ridge",
            "Lasso",
            "LogisticRegression",
            "Knn",
            "Knn_class",
        ):
            return self.training_machine_core(
                name, learnner, down_ndim=args_use["nDim_2"], **kwargs
            )

    def predict_simp(self, name, learner, down_ndim=True, **kwargs):
        get = self.get_sheet(name)
        column = self.get_column(name, True)
        x = get.to_numpy()
        if down_ndim or x.ndim == 1:  # 执行降维处理（也包括升维，ravel让一切变成一维度，包括数字）
            a = x
            x = []
            for i in a:
                try:
                    c = i.np.ravel(a[i], "C")
                    x.append(c)
                except ValueError:
                    x.append(i)
            x = np.array(x)
        model = self.get_learner(learner)
        answer = model.predict(x)
        data = pd.DataFrame(x, index=answer, columns=column)
        self.add_sheet(data, f"{name}:预测")
        return data

    def predict(self, name, learner, parameters="", **kwargs):
        type_ = self.get_learner_type(learner)
        args_use = self.parsing(parameters)
        if type_ in (
            "Line",
            "Ridge",
            "Lasso",
            "LogisticRegression",
            "Knn",
            "Knn_class",
        ):
            return self.predict_simp(
                name, learner, down_ndim=args_use["nDim_2"], **kwargs
            )
