import pandas as pd
import re
import pandas_profiling as pp
from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.globals import SymbolType
from pyecharts.components import Table
from pyecharts.globals import GeoType #地图推荐使用GeoType而不是str
from random import randint
from sklearn.model_selection import train_test_split
from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
import sklearn as sk
from sklearn.feature_extraction import DictVectorizer
import numpy as np

class Form:
    def __init__(self, *args, **kwargs):
        class DEL: pass

        self.Sheet_Dic = {}
        self.Clean_Func = {}
        self.Clean_Func_Exp = {}
        self.DEL = DEL()
        self.Name = {'pd': pd, 'DEL': self.DEL, 're': re, 'Sheet': self.Sheet_Dic}
        self.R_Dic = {}  # 存放所有的图

    def get_Sheet(self, name, all_Row=None, all_Colunms=None) -> pd.DataFrame:
        try:
            pd.set_option('display.max_rows', all_Row)
            pd.set_option('display.max_columns', all_Colunms)
        except:
            pass
        return self.Sheet_Dic[name]

    def Describe(self, name, make_Sheet=False):  # 生成描述
        get = self.get_Sheet(name)
        Des = get.describe()
        if make_Sheet: self.Add_Form(Des, f'{name}_describe[{len(self.Sheet_Dic)}]')
        shape = get.shape
        dtype = get.dtypes
        n = get.ndim
        head = get.head()
        tail = get.tail(3)
        return f'1)基本\n{Des}\n\n2)形状:{shape}\n\n3)数据类型\n{dtype}\n\n4)数据维度:{n}\n\n5)头部数据\n{head}\n\n6)尾部数据\n{tail}' \
               f'\n\n7)行名\n{get.index}\n\n8)列名\n{get.columns}'

    def Add_Form(self, Data, name=''):
        if name == '': name = f'Sheet[{len(self.Sheet_Dic)}]'
        else:name += f'_[{len(self.Sheet_Dic)}]'
        self.Sheet_Dic[name] = Data
        return Data

    def Del_Form(self,name):
        del self.Sheet_Dic[name]

    def __Add_Form(self, Dic, Func, name='', Index=True, **kwargs):  # 新增表格的核心方式
        try:
            Data = Func(Dic, **kwargs)
        except UnicodeDecodeError:  # 找不到编码方式
            return False
        if not Index:
            Data.index = Data.iloc[:, 0].tolist()
            Data.drop(Data.columns.values.tolist()[0], inplace=True, axis=1)
        return self.Add_Form(Data, name)

    def Add_CSV(self, Dic, name='', Sep=',', code='utf-8', str_=True, Index=True):
        if str_:
            k = {'dtype': 'object'}
        else:
            k = {}
        return self.__Add_Form(Dic, pd.read_csv, name, Index, sep=Sep, encoding=code, **k)

    def Add_Python(self, Text, sheet_name='') -> pd.DataFrame:
        name = {'Sheet': self.get_Sheet}
        name.update(globals().copy())
        name.update(locals().copy())
        exec(Text, name)
        exec('get = Creat()', name)
        if isinstance(name['get'], pd.DataFrame):  # 已经是DataFram
            get = name['get']
        elif isinstance(name['get'], np.array):
            if bool(name.get('downNdim',False)):#执行降或升维操作
                a = name['get']
                array = []
                for i in a:
                    try:
                        c = i.np.ravel(a[i], 'C')
                        array.append(c)
                    except:
                        array.append(i)
                get = pd.DataFrame(array)
            else:
                array = name['get'].tolist()
                get = pd.DataFrame(array)
        else:
            try:
                get = pd.DataFrame(name['get'])
            except:
                get = pd.DataFrame([name['get']])
        self.Add_Form(get, sheet_name)
        return get

    def Add_Html(self, Dic, name='', code='utf-8', str_=True, Index=True):
        if str_:
            k = {'dtype': 'object'}
        else:
            k = {}
        return self.__Add_Form(Dic, pd.read_html, name, Index, encoding=code, **k)

    def get_FormList(self):
        return list(self.Sheet_Dic.keys())  # 返回列表

    def to_Html_One(self,name,Dic=''):
        if Dic == '': Dic = f'{name}.html'
        get = self.get_Sheet(name)
        headers = [f'{name}'] + self.get_Column(name, True).tolist()
        rows = []
        table = Table()
        for i in get.iterrows():  # 按行迭代
            q = i[1].tolist()
            rows.append([f'{i[0]}'] + q)
        table.add(headers, rows).set_global_opts(
            title_opts=opts.ComponentTitleOpts(title=f"表格:{name}", subtitle="CoTan~数据处理:查看表格"))
        table.render(Dic)
        return Dic

    def to_Html(self, name, Dic='', type_=0):
        if Dic == '': Dic = f'{name}.html'
        # 把要画的sheet放到第一个
        Sheet_Dic = self.Sheet_Dic.copy()
        del Sheet_Dic[name]
        Sheet_list = [name] + list(Sheet_Dic.keys())

        class TAB_F:
            def __init__(self, q):
                self.tab = q  # 一个Tab

            def render(self, Dic):
                return self.tab.render(Dic)

        # 生成一个显示页面
        if type_ == 0:
            class TAB(TAB_F):
                def add(self, table, k, *f):
                    self.tab.add(table, k)

            tab = TAB(Tab(page_title='CoTan:查看表格'))  # 一个Tab
        elif type_ == 1:
            class TAB(TAB_F):
                def add(self, table, *k):
                    self.tab.add(table)

            tab = TAB(Page(page_title='CoTan:查看表格', layout=Page.DraggablePageLayout))
        else:
            class TAB(TAB_F):
                def add(self, table, *k):
                    self.tab.add(table)

            tab = TAB(Page(page_title='CoTan:查看表格', layout=Page.SimplePageLayout))
        # 迭代添加内容
        for name in Sheet_list:
            get = self.get_Sheet(name)
            headers = [f'{name}'] + self.get_Column(name, True).tolist()
            rows = []
            table = Table()
            for i in get.iterrows():  # 按行迭代
                q = i[1].tolist()
                rows.append([f'{i[0]}'] + q)
            table.add(headers, rows).set_global_opts(
                title_opts=opts.ComponentTitleOpts(title=f"表格:{name}", subtitle="CoTan~数据处理:查看表格"))
            tab.add(table, f'表格:{name}')
        tab.render(Dic)
        return Dic

    def To_Sheet_Des(self, Sheet, Dic):
        re = pp.ProfileReport(Sheet)
        re.to_file(Dic)

    def to_Report(self, name, Dic=''):
        if Dic == '': Dic = f'{name}.html'
        Sheet = self.get_Sheet(name)
        self.To_Sheet_Des(Sheet, Dic)
        return Dic

    def get_Column(self, name, only=False):  # 列名
        get = self.get_Sheet(name)
        if only:
            re = get.columns.values
        else:
            re = []
            loc_list = get.columns.values
            a = 0
            for i in loc_list:
                data = get[i].to_list()
                re.append(f'[列号:{a}]{i} -> {data}')
                a += 1
        return re

    def get_Index(self, name, only=False):
        get = self.get_Sheet(name)
        if only:
            re = get.index.values
        else:
            re = []
            loc_list = get.index.values
            a = 0
            for i in range(len(loc_list)):
                l = loc_list[i]
                data = get.iloc[i].to_list()
                re.append(f'[行号:{a}]{l} -> {data}')
                a += 1
        return re

    def Sorted(self, name, row: bool, new=False, a=True):
        get = self.get_Sheet(name)
        if row:  # row-行名排序
            so = get.sort_index(axis=0, ascending=a)
        else:
            so = get.sort_index(axis=1, ascending=a)
        if new:
            self.Add_Form(so,f'{name}:排序')
        return so

    def Stored_Valuse(self, name, F, new=False):
        get = self.get_Sheet(name)
        row = get.columns.values
        a = []
        b = []
        for i in F:
            a.append(row[i[0]])
            b.append(i[1])
        if len(a) == 1:
            a = a[0]
            b = b[0]
        so = get.sort_values(by=a, ascending=b)
        if new:
            self.Add_Form(so,f'{name}:排序')
        return so

    def T(self, name, new=True):
        get = self.get_Sheet(name)
        re = get.T
        if new:
            self.Add_Form(re,f'{name}.T')
        return re

    def get_Clice(self, name, Column, Row, U_iloc=True, new=False):  # iloc(Row,Column) or loc
        get = self.get_Sheet(name)
        if U_iloc:
            Cli = get.iloc[Row, Column]
        else:
            Cli = get.loc[Row, Column]
        if new:
            self.Add_Form(Cli,f'{name}:切片')
        return Cli

    def Delete(self, name, Column, Row, new):
        get = self.get_Sheet(name)
        Column_List = get.columns.values
        for i in Column:
            try:
                get = get.drop(Column_List[int(i)], axis=1)
            except:
                pass
        Row_List = get.index.values
        for i in Row:
            try:
                get = get.drop(Row_List[int(i)])
            except:
                pass
        if new:
            self.Add_Form(get,f'{name}:删减')
        return get

    def Done_Bool(self, name, Exp, new=False):
        get = self.get_Sheet(name)
        try:
            re = eval(Exp, {'S': get, 'Sheet': get.iloc})
            if new:
                self.Add_Form(re,f'{name}:布尔')
            return re
        except:
            return None
            # raise

    def is_Na(self, name):
        get = self.get_Sheet(name)
        Na = pd.isna(get)
        return Na

    def Dropna(self, name, new):
        get = self.get_Sheet(name)
        Clean = get.dropna(axis=0)
        if new:
            self.Add_Form(Clean,f'{name}:清洗')
        return Clean

    def Add_CleanFunc(self, Exp):
        Name = self.Name.copy()
        try:
            exec(Exp, Name)
        except:
            return False
        Sava = {}
        Sava['Done_Row'] = Name.get('Done_Row', [])
        Sava['Done_Column'] = Name.get('Done_Column', [])
        Sava['axis'] = Name.get('axis', True)
        Sava['check'] = Name.get('check', lambda data, x, b, c, d, e: True)
        Sava['done'] = Name.get('done', lambda data, x, b, c, d, e: data)
        print(f'{len(self.Clean_Func)}')
        title = f"[{Name.get('name', f'[{len(self.Clean_Func)}')}] Done_Row={Sava['Done_Row']}_Done_Column={Sava['Done_Column']}_axis={Sava['axis']}"
        self.Clean_Func[title] = Sava
        self.Clean_Func_Exp[title] = Exp

    def Return_CleanFunc(self):
        return list(self.Clean_Func.keys())

    def Delete_CleanFunc(self, key):
        try:
            del self.Clean_Func[key]
            del self.Clean_Func_Exp[key]
        except:
            pass

    def Tra_Clean(self):
        self.Clean_Func = {}
        self.Clean_Func_Exp = {}

    def Return_CleanExp(self, key):
        return self.Clean_Func_Exp[key]

    def Done_CleanFunc(self, name):
        get = self.get_Sheet(name).copy()
        for i in list(self.Clean_Func.values()):
            Done_Row = i['Done_Row']
            Done_Column = i['Done_Column']
            if Done_Row == []:
                Done_Row = range(get.shape[0])  # shape=[行,列]#不需要回调
            if Done_Column == []:
                Done_Column = range(get.shape[1])  # shape=[行,列]#不需要回调
            if i['axis']:
                axis = 0
            else:
                axis = 1
            check = i['check']
            done = i['done']
            for r in Done_Row:
                for c in Done_Column:
                    try:
                        n = eval(f"get.iloc[{r},{c}]")  # 第一个是行号，然后是列号
                        r_h = eval(f"get.iloc[{r}]")
                        c_h = eval(f"get.iloc[:,{c}]")
                        if not check(n, r, c, get.copy(), r_h.copy(), c_h.copy()):
                            d = done(n, r, c, get.copy(), r_h.copy(), c_h.copy())
                            if d == self.DEL:
                                if axis == 0:  # 常规删除
                                    Row_List = get.index.values
                                    get = get.drop(Row_List[int(r)])
                                else:  # 常规删除
                                    Columns_List = get.columns.values
                                    get = get.drop(Columns_List[int(r)], axis=1)
                            else:
                                exec(f"get.iloc[{r},{c}] = {d}")  # 第一个是行名，然后是列名
                    except:
                        pass
        self.Add_Form(get,f'{name}:清洗')
        return get

    def Import_c(self, text):
        Name = {}
        Name.update(locals())
        Name.update(globals())
        exec(text, Name)
        exec('c = Page()', Name)
        self.R_Dic[f'自定义图[{len(self.R_Dic)}]'] = Name['c']
        return Name['c']

    def retunr_RDic(self):
        return self.R_Dic.copy()

    def Delete_RDic(self, key):
        del self.R_Dic[key]

    def Reasonable_Type(self, name, column, dtype, wrong):
        get = self.get_Sheet(name).copy()
        for i in range(len(column)):
            try:
                column[i] = int(column[i])
            except:
                pass

        if dtype != '':
            func_Dic = {'Num': pd.to_numeric, 'Date': pd.to_datetime, 'Time': pd.to_timedelta}
            if column != []:
                get.iloc[:, column] = get.iloc[:, column].apply(func_Dic.get(dtype, pd.to_numeric), errors=wrong)
            else:
                get = get.apply(func_Dic.get(dtype, pd.to_numeric), errors=wrong)
        else:
            if column != []:
                get.iloc[:, column] = get.iloc[:, column].infer_objects()
                print('A')
            else:
                get = get.infer_objects()
        self.Add_Form(get,f'{name}')
        return get

    def as_Type(self, name, column, dtype, wrong):
        get = self.get_Sheet(name).copy()
        for i in range(len(column)):
            try:
                column[i] = int(column[i])
            except:
                pass
        func_Dic = {'Int': int, 'Float': float, 'Str': str, 'Date': pd.Timestamp, 'TimeDelta': pd.Timedelta}
        if column != []:
            get.iloc[:, column] = get.iloc[:, column].astype(func_Dic.get(dtype, dtype), errors=wrong)
            print('A')
        else:
            get = get.astype(func_Dic.get(dtype, dtype), errors=wrong)
        self.Add_Form(get,f'{name}')
        return get

    def Replace_Index(self, name, is_column, Dic, save):
        get = self.get_Sheet(name)
        if is_column:
            if save:  # 保存原数据
                get.loc['column'] = self.get_Column(name, True)
            new = get.rename(columns=Dic)
        else:
            if save:
                get.loc[:, 'row'] = self.get_Index(name, True)
            new = get.rename(index=Dic)
        self.Add_Form(new,f'{name}')
        return new

    def Change_Index(self, name: str, is_column: bool, iloc: int, save: bool = True, drop: bool = False):
        get = self.get_Sheet(name).copy()
        if is_column:  # 列名
            Row = self.get_Index(name, True)#行数据
            t = Row.tolist()[iloc]
            if save:  # 保存原数据
                get.loc['column'] = self.get_Column(name,True)
            # new_colums = get.loc[t].values
            get.columns = get.loc[t].values
            if drop:
                get.drop(t, axis=0, inplace=True)  # 删除行
        else:
            Col = self.get_Column(name, True)
            t = Col.tolist()[iloc]
            print(t)
            if save:
                get.loc[:, 'row'] = self.get_Index(name,True)
            get.index = get.loc[:, t].values  # 调整
            if drop:
                get.drop(t, axis=1, inplace=True)  # 删除行
        self.Add_Form(get,f'{name}')
        return get

    def num_toName(self, name, is_column, save):
        get = self.get_Sheet(name).copy()
        if is_column:  # 处理列名
            Col = self.get_Column(name, True)
            if save:  # 保存原数据
                get.loc['column'] = Col
            get.columns = [i for i in range(len(Col))]
        else:
            Row = self.get_Index(name, True)
            if save:
                get.loc[:, 'row'] = Row
            get.index = [i for i in range(len(Row))]
        self.Add_Form(get,f'{name}')
        return get

    def num_withName(self, name, is_column, save):
        get = self.get_Sheet(name).copy()
        if is_column:  # 处理列名
            Col = self.get_Column(name, True)
            if save:  # 保存原数据
                get.loc['column'] = Col
            get.columns = [f'[{i}]{Col[i]}' for i in range(len(Col))]
        else:
            Row = self.get_Index(name, True)
            if save:
                get.loc[:, 'row'] = Row
            get.index = [f'[{i}]{Row[i]}' for i in range(len(Row))]
        self.Add_Form(get,f'{name}')
        return get

    def Date_Index(self, name, is_column, save, **Date_Init):
        # Date_Init:start,end,freq 任意两样
        get = self.get_Sheet(name)
        if is_column:  # 处理列名
            Col = self.get_Column(name, True)
            if save:  # 保存原数据
                get.loc['column'] = Col
            Date_Init['periods'] = len(Col)
            get.columns = pd.date_range(**Date_Init)
        else:
            Row = self.get_Index(name, True)
            if save:
                get.loc[:, 'row'] = Row
            Date_Init['periods'] = len(Row)
            get.index = pd.date_range(**Date_Init)
        self.Add_Form(get,f'{name}')
        return get

    def Time_Index(self, name, is_column, save, **Time_Init):
        # Date_Init:start,end,freq 任意两样
        get = self.get_Sheet(name)
        if is_column:  # 处理列名
            Col = self.get_Column(name, True)
            if save:  # 保存原数据
                get.loc['column'] = Col
            Time_Init['periods'] = len(Col)
            get.columns = pd.timedelta_range(**Time_Init)
        else:
            Row = self.get_Index(name, True)
            if save:
                get.loc[:, 'row'] = Row
            Time_Init['periods'] = len(Row)
            get.index = pd.timedelta_range(**Time_Init)
        self.Add_Form(get,f'{name}')
        return get

    def Sample(self,name,new):
        get = self.get_Sheet(name)
        sample = get.sample(frac=1)#返回比，默认按行打乱
        if new:
            self.Add_Form(sample,f'{name}:打乱')
        return sample

    def to_CSV(self,name,Dic,Sep=','):
        if Sep == '':Sep = ','
        get = self.get_Sheet(name)
        get.to_csv(Dic,sep=Sep,na_rep='')

class Draw(Form):

    # 1）图例位置、朝向和是否显示
    # 2）视觉映射是否开启、是否有最大值和最小值、两端文本以及颜色、分段和朝向、size或color
    # 3）自动设置图标ID，标题
    # 4）工具箱显示
    # 5）title配置
    # 6）是否显示刻度线、数轴类型、分割线

    def Parsing_Parameters(self,text):#解析文本参数
        args = {}#解析到的参数
        exec(text,args)
        args_use = {}#真实的参数
        #标题设置，global
        args_use['title'] = args.get('title',None)
        args_use['vice_title'] = args.get('vice_title', 'CoTan~数据处理:')
        #图例设置global
        args_use['show_Legend'] = bool(args.get('show_Legend', True))#是否显示图例
        args_use['ori_Legend'] = args.get('ori_Legend', 'horizontal')#朝向
        #视觉映射设置global
        args_use['show_Visual_mapping'] = bool(args.get('show_Visual_mapping', True))#是否显示视觉映射
        args_use['is_color_Visual_mapping'] = bool(args.get('is_color_Visual_mapping', True))#颜色 or 大小
        args_use['min_Visual_mapping'] = args.get('min_Visual_mapping', None)#最小值(None表示现场计算)
        args_use['max_Visual_mapping'] = args.get('max_Visual_mapping', None)#最大值(None表示现场计算)
        args_use['color_Visual_mapping'] = args.get('color_Visual_mapping', None)#颜色列表
        args_use['size_Visual_mapping'] = args.get('size_Visual_mapping', None)#大小列表
        args_use['text_Visual_mapping'] = args.get('text_Visual_mapping', None)#文字
        args_use['is_Subsection'] = bool(args.get('is_Subsection', False))  # 分段类型
        args_use['Subsection_list'] = args.get('Subsection_list', [])  # 分段列表
        args_use['ori_Visual'] = args.get('ori_Visual', 'vertical')  # 朝向
        #工具箱设置global
        args_use['Tool_BOX'] = bool(args.get('Tool_BOX', True))  # 开启工具箱
        #Init设置global
        args_use['Theme'] = args.get('Theme', 'white')  # 设置style
        args_use['BG_Color'] = args.get('BG_Color', None)  # 设置背景颜色
        args_use['width'] = args.get('width', '900px')  # 设置宽度
        args_use['heigh'] = args.get('heigh', '500px') if not bool(args.get('Square', False)) else args.get('width', '900px')  # 设置高度
        args_use['page_Title'] = args.get('page_Title', '')  # 设置HTML标题
        args_use['show_Animation'] = args.get('show_Animation', True)  # 设置HTML标题
        #坐标轴设置，2D坐标图和3D坐标图
        args_use['show_Axis'] = bool(args.get('show_Axis', True))  # 显示坐标轴
        args_use['Axis_Zero'] = bool(args.get('Axis_Zero', False))  # 重叠于原点
        args_use['show_Axis_Scale'] = bool(args.get('show_Axis_Scale', True))  # 显示刻度
        args_use['x_type'] = args.get('x_type', None)  # 坐标轴类型
        args_use['y_type'] = args.get('y_type', None)
        args_use['z_type'] = args.get('z_type', None)
        #Mark设置 坐标图专属
        args_use['make_Line'] = args.get('make_Line', [])  # 设置直线
        #Datazoom设置 坐标图专属
        args_use['Datazoom'] = args.get('Datazoom', 'N')  # 设置Datazoom

        #显示文字设置
        args_use['show_Text'] = bool(args.get('show_Text', False))  # 显示文字

        #统一化的设置
        args_use['Size'] = args.get('Size', 10)  # Size
        args_use['Symbol'] = args.get('Symbol', 'circle')  # 散点样式

        #Bar设置
        args_use['bar_Stacking'] = bool(args.get('bar_Stacking', False))  # 堆叠(2D和3D)

        #散点图设置
        args_use['EffectScatter'] = bool(args.get('EffectScatter', False))  # 开启特效(2D和3D)

        # 折线图设置
        args_use['connect_None'] = bool(args.get('connect_None', False))  # 连接None
        args_use['Smooth_Line'] = bool(args.get('Smooth_Line', False))  # 平滑曲线
        args_use['Area_chart'] = bool(args.get('Area_chart', False))  # 面积图
        args_use['paste_Y'] = bool(args.get('paste_Y', False))  # 紧贴Y轴
        args_use['step_Line'] = bool(args.get('step_Line', False))  # 阶梯式图

        args_use['size_PictorialBar'] = args.get('size_PictorialBar', None)  # 象形柱状图大小

        args_use['Polar_units'] = args.get('Polar_units', '100')  # 极坐标图单位制

        args_use['More'] = bool(args.get('More', False))  # 均绘制水球图、仪表图

        args_use['WordCould_Size'] = args.get('WordCould_Size', [20,100])  # 开启特效
        args_use['WordCould_Shape'] = args.get('WordCould_Shape', "circle")  # 开启特效

        args_use['symbol_Graph'] = args.get('symbol_Graph', 'circle')  # 关系点样式
        args_use['Repulsion'] = float(args.get('Repulsion', 8000))  # 斥力因子

        args_use['Area_radar'] = bool(args.get('Area_radar', True))  # 雷达图面积

        args_use['HTML_Type'] = args.get('HTML_Type', 2)  # 输出Page的类型

        args_use['Map'] = args.get('Map', 'china')  # 输出Page的面积
        args_use['show_Map_Symbol'] = bool(args.get('show_Map_Symbol', False))  # 输出Page的面积
        args_use['Geo_Type'] = {'heatmap':GeoType.HEATMAP,'scatter':'scatter','EFFECT':GeoType.EFFECT_SCATTER
                                }.get(args.get('Geo_Type', 'heatmap'),GeoType.HEATMAP)  # 输出Page的面积
        args_use['map_Type'] = args.get('map_Type', '2D')  # 输出Page的面积
        args_use['is_Dark'] = bool(args.get('is_Dark', False))  # 输出Page的面积
        return args_use

    #全局设定，返回一个全局设定的字典，解包即可使用
    def global_set(self,args_use,title,Min,Max,DataZoom=False,Visual_mapping=True,axis=()):
        k = {}
        #标题设置
        if args_use['title'] == None:args_use['title'] = title
        k['title_opts']=opts.TitleOpts(title=args_use['title'], subtitle=args_use['vice_title'])

        #图例设置
        if not args_use['show_Legend']:k['legend_opts']=opts.LegendOpts(is_show=False)
        else:
            k['legend_opts'] = opts.LegendOpts(type_='scroll',orient=args_use['ori_Legend'],pos_bottom='2%')#移动到底部，避免和标题冲突

        #视觉映射
        if not args_use['show_Visual_mapping']:
            pass
        elif not Visual_mapping:
            pass
        else:
            if args_use['min_Visual_mapping'] != None:Min = args_use['min_Visual_mapping']
            if args_use['max_Visual_mapping'] != None:Max = args_use['max_Visual_mapping']
            k['visualmap_opts'] = opts.VisualMapOpts(type_= 'color'if args_use['is_color_Visual_mapping'] else 'size',
                                                     max_=Max,min_=Min,range_color=args_use['color_Visual_mapping'],
                                                     range_size=args_use['size_Visual_mapping'],range_text=args_use['text_Visual_mapping'],
                                                     is_piecewise=args_use['is_Subsection'],pieces=args_use['Subsection_list'],
                                                     orient=args_use['ori_Visual'])

        k['toolbox_opts']=opts.ToolboxOpts(is_show=args_use['Tool_BOX'])

        if DataZoom:
            if args_use['Datazoom'] == 'all':
                k['datazoom_opts'] = [opts.DataZoomOpts(), opts.DataZoomOpts(orient = "horizontal")]
            elif args_use['Datazoom'] == 'horizontal':
                k['datazoom_opts'] = opts.DataZoomOpts(type_="inside")
            elif args_use['Datazoom'] == 'vertical':
                opts.DataZoomOpts(orient="vertical")
            elif args_use['Datazoom'] == 'inside_vertical':
                opts.DataZoomOpts(type_="inside", orient="vertical")
            elif args_use['Datazoom'] == 'inside_vertical':
                opts.DataZoomOpts(type_="inside", orient="horizontal")

        # 坐标轴设定，输入设定的坐标轴即可
        def axis_Seeting(args_use, axis='x'):
            axis_k = {}
            if args_use[f'{axis[0]}_type'] == 'Display' or not args_use['show_Axis']:
                axis_k[f'{axis[0]}axis_opts'] = opts.AxisOpts(is_show=False)
            else:
                axis_k[f'{axis[0]}axis_opts'] = opts.AxisOpts(type_=args_use[f'{axis[0]}_type'],
                                                         axisline_opts=opts.AxisLineOpts(
                                                             is_on_zero=args_use['Axis_Zero']),
                                                         axistick_opts=opts.AxisTickOpts(
                                                             is_show=args_use['show_Axis_Scale']))
            return axis_k
        for i in axis:
            k.update(axis_Seeting(args_use, i))
        return k

    #初始化设定
    def initSetting(self,args_use):
        k = {}
        #设置标题
        if args_use['page_Title'] == '':title = 'CoTan_数据处理'
        else:title = f"CoTan_数据处理:{args_use['page_Title']}"
        k['init_opts'] = opts.InitOpts(theme=args_use['Theme'],bg_color=args_use['BG_Color'],width=args_use['width'],
                                       height=args_use['heigh'],page_title=title,
                                       animation_opts=opts.AnimationOpts(animation=args_use['show_Animation']))
        return k

    #获取title专用
    def get_name(self,args_use):
        return f":{args_use['title']}"

    #标记符，包含线标记、点
    def Mark(self,args_use):
        k = {}
        line = []
        for i in args_use['make_Line']:
            try:
                if i[2] == 'c' or i[0] in ('min', 'max', 'average'):
                    line.append(opts.MarkLineItem(type_=i[0], name=i[1]))
                elif i[2] == 'x':
                    line.append(opts.MarkLineItem(x=i[0], name=i[1]))
                else:
                    raise Exception
            except:
                line.append(opts.MarkLineItem(y=i[0], name=i[1]))
        if line == []:return k
        k['markline_opts'] = opts.MarkLineOpts(data=line)
        return k

    #标签设定，可以放在系列设置中或者坐标轴y轴设置中
    def y_Label(self,args_use,position="inside"):
        return {'label_opts':opts.LabelOpts(is_show=args_use['show_Text'],position=position)}

    #放在不同的图~.add中的设定
    def Per_Seeting(self,args_use,type_):#私人设定
        k = {}
        if type_ == 'Bar':#设置y的重叠
            if args_use['bar_Stacking']:
                k =  {"stack":"stack1"}
        elif type_ == 'Scatter':
            k['Beautiful'] = args_use['EffectScatter']
            k['symbol'] = args_use['Symbol']
            k['symbol_size'] = args_use['Size']
        elif type_ == 'Line':
            k['is_connect_nones'] = args_use['connect_None']
            k['is_smooth'] = True if args_use['Smooth_Line'] or args_use['paste_Y'] else False#平滑曲线或连接y轴
            k['areastyle_opts']=opts.AreaStyleOpts(opacity=0.5 if args_use['Area_chart'] else 0)
            if args_use['step_Line']:
                del k['is_smooth']
                k['is_step'] = True
        elif type_ == 'PictorialBar':
            k['symbol_size'] = args_use['Size']
        elif type_ == 'Polar':
            return args_use['Polar_units']#回复的是单位制而不是设定
        elif type_ == 'WordCloud':
            k['word_size_range'] = args_use['WordCould_Size']#放到x轴
            k['shape'] = args_use['Symbol']  # 放到x轴
        elif type_ == 'Graph':
            k['symbol_Graph'] = args_use['Symbol']#放到x轴
        elif type_ == 'Radar':#雷达图
            k['areastyle_opts']=opts.AreaStyleOpts(opacity=0.1 if args_use['Area_chart'] else 0)
            k['symbol'] = args_use['Symbol']#雷达图symbol
        return k

    #坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_Bar(self,name,text) -> Bar:#Bar:数据堆叠
        get = self.get_Sheet(name)
        x = self.get_Index(name,True).tolist()
        args = self.Parsing_Parameters(text)
        c = (
            Bar(**self.initSetting(args))
            .add_xaxis(list(map(str, list(set(x)))))#转变为str类型
        )
        y = []
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                c.add_yaxis(f'{name}_{i[0]}', q,**self.Per_Seeting(args,'Bar'),**self.y_Label(args),color=self.get_Color())#i[0]是名字，i是tuple，其中i[1]是data
                y += list(map(int, q))  # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
            except:
                pass
        if y == []:
            args['show_Visual_mapping'] = False  # 关闭视觉映射
            y = [0,100]
        c.set_global_opts(**self.global_set(args,f"{name}柱状图",min(y),max(y),True,axis=['x','y']))
        c.set_series_opts(**self.Mark(args))
        self.R_Dic[f'{name}柱状图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    # 坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_Line(self,name,text) -> Line:#折线图：连接空数据、显示数值、平滑曲线、面积图以及紧贴Y轴
        get = self.get_Sheet(name)
        x = self.get_Index(name,True).tolist()
        args = self.Parsing_Parameters(text)
        c = (
            Line(**self.initSetting(args))
            .add_xaxis(list(map(str,  list(set(x)))))#转变为str类型
        )
        y = []
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                c.add_yaxis(f'{name}_{i[0]}', q,**self.Per_Seeting(args,'Line'),**self.y_Label(args),color=self.get_Color())#i[0]是名字，i是tuple，其中i[1]是data
                y += list(map(int, q))  # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
            except:
                pass
        if y == []:
            args['show_Visual_mapping'] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(**self.global_set(args, f"{name}折线图", min(y), max(y), True,axis=['x','y']))
        c.set_series_opts(**self.Mark(args))
        self.R_Dic[f'{name}折线图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    # 坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_Scatter(self,name,text) -> Scatter:#散点图标记形状和大小、特效、标记线
        get = self.get_Sheet(name)
        args = self.Parsing_Parameters(text)
        x = self.get_Index(name,True).tolist()
        type_ = self.Per_Seeting(args, 'Scatter')
        if type_['Beautiful']:Func = EffectScatter
        else:Func = Scatter
        del type_['Beautiful']
        c = (
            Func(**self.initSetting(args))
            .add_xaxis(list(map(str,  list(set(x)))))#转变为str类型
        )
        y = []
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                c.add_yaxis(f'{name}_{i[0]}', q,**type_,**self.y_Label(args),color=self.get_Color())#i[0]是名字，i是tuple，其中i[1]是data
                y += list(map(int, q))  # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
            except:
                pass
        if y == []:
            args['show_Visual_mapping'] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(**self.global_set(args, f"{name}散点图", min(y), max(y), True,axis=['x','y']))
        c.set_series_opts(**self.Mark(args))
        self.R_Dic[f'{name}散点图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    # 坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_Pictorialbar(self,name,text) -> PictorialBar:#象形柱状图：图形、剪裁图像、元素重复和间隔
        get = self.get_Sheet(name)
        x = self.get_Index(name, True).tolist()
        args = self.Parsing_Parameters(text)
        c = (
            PictorialBar(**self.initSetting(args))
                .add_xaxis(list(map(str,  list(set(x)))))#转变为str类型
                .reversal_axis()
        )
        y = []
        k = self.Per_Seeting(args, 'PictorialBar')
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                c.add_yaxis(
                f'{name}_{i[0]}',q,
                label_opts=opts.LabelOpts(is_show=False),
                symbol_repeat=True,
                is_symbol_clip=True,
                symbol=SymbolType.ROUND_RECT,
                **k,color=self.get_Color())
                y += list(map(int, q))  # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
            except:
                pass
        if y == []:
            args['show_Visual_mapping'] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(**self.global_set(args, f"{name}象形柱状图", min(y), max(y), True,axis=['x','y']))
        c.set_series_opts(**self.Mark(args))
        self.R_Dic[f'{name}[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    # 坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_Boxpolt(self,name,text) -> Boxplot:
        get = self.get_Sheet(name)
        args = self.Parsing_Parameters(text)
        c = (
            Boxplot(**self.initSetting(args))
                .add_xaxis([f'{name}'])
            )
        y = []
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                c.add_yaxis(f'{name}_{i[0]}',[q],**self.y_Label(args))
                y += list(map(float, q))  # q不需要float，因为应多不同的type他会自动变更，但是y是用来比较大小
            except:
                pass
        if y == []:
            args['show_Visual_mapping'] = False  # 关闭视觉映射
            y = [0, 100]
        c.set_global_opts(**self.global_set(args, f"{name}箱形图", min(y), max(y), True,axis=['x','y']))
        c.set_series_opts(**self.Mark(args))
        self.R_Dic[f'{name}箱形图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    # 坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_HeatMap(self,name,text) -> HeatMap:#显示数据
        get = self.get_Sheet(name)
        x = self.get_Column(name, True).tolist()  # 图的x轴，下侧，列名
        y = self.get_Index(name, True).tolist()  # 图的y轴，左侧，行名
        value_list = []
        q = []
        for c in range(len(x)):  # c-列，r-行
            for r in range(len(y)):
                try:
                    v = float(eval(f'get.iloc[{r},{c}]'))  # 先行后列
                except:continue
                q.append(v)
                value_list.append([c, r, v])
        args = self.Parsing_Parameters(text)
        try:
            MAX,MIN = max(q),min(q)
        except:
            args['show_Visual_mapping'] = False  # 关闭视觉映射
            MAX, MIN = 0,100
        c = (
            HeatMap(**self.initSetting(args))
            .add_xaxis(list(map(str,  list(set(x)))))#转变为str类型
            .add_yaxis(f'{name}', list(map(str, y)), value_list,**self.y_Label(args))
            .set_global_opts(**self.global_set(args, f"{name}热力图", MIN, MAX, True,axis=['x','y']))
            .set_series_opts(**self.Mark(args))
        )
        self.R_Dic[f'{name}热力图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    #数据哪部全，要设置More
    def to_Funnel(self,name,text) -> Funnel:
        get = self.get_Sheet(name)
        y_name = self.get_Index(name,True).tolist()#拿行名
        x = self.get_Column(name,True).tolist()[0]
        value = []
        y = []
        for r in range(len(y_name)):
            try:
                v = float(eval(f'get.iloc[{r},0]'))
            except:continue
            value.append([f'{y_name[r]}',v])
            y.append(v)
        args = self.Parsing_Parameters(text)
        c = (
            Funnel(**self.initSetting(args))
                .add(f'{name}', value,**self.y_Label(args,'top'))
                .set_global_opts(**self.global_set(args, f"{name}漏斗图", min(y), max(y), True, False))
        )
        self.R_Dic[f'{name}漏斗图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Graph(self,name,text) -> Graph:
        get = self.get_Sheet(name)
        y_name = self.get_Index(name,True).tolist()#拿行名
        nodes = []
        link = []
        for i in get.iterrows():#按行迭代
            q = i[1].tolist()#转换为列表
            try:
                nodes.append({"name": f"{i[0]}", "symbolSize": float(q[0]),"value": float(q[0])})
                for a in q[1:]:
                    n = str(a).split(':')
                    try:
                        link.append({"source": f"{i[0]}", "target": n[0], "value":float(n[1])})
                    except:pass
            except:
                pass
        if link == []:
            for i in nodes:
                for j in nodes:
                    link.append({"source": i.get("name"), "target": j.get("name"),"value":abs(i.get("value")-j.get("value"))})
        args = self.Parsing_Parameters(text)
        c = (
            Graph(**self.initSetting(args))
                .add(f"{y_name[0]}", nodes, link, repulsion=args['Repulsion'],**self.y_Label(args))
                .set_global_opts(**self.global_set(args, f"{name}关系图", 0, 100, False,False))
        )
        self.R_Dic[f'{name}关系图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_XY_Graph(self,name,text) -> Graph:#XY关系图，新的书写方式
        get = self.get_Sheet(name)
        args = self.Parsing_Parameters(text)
        size = args['Size']*3

        #生成节点信息
        y_name = self.get_Index(name,True).tolist()#拿行名
        x_name = self.get_Column(name,True).tolist()#拿列名
        nodes_list = list(set(y_name + x_name))#处理重复，作为nodes列表
        nodes = []
        for i in nodes_list:
            nodes.append({"name": f"{i}", "symbolSize": size})

        #生成link信息
        link = []  # 记录连接的信息
        have = []
        for y in range(len(y_name)):#按行迭代
            for x in range(len(x_name)):
                y_n = y_name[y]#节点1
                x_n = x_name[x]#节点2
                if y_n == x_n:continue
                if  (y_n,x_n) in have or (x_n,y_n) in have :continue
                else:
                    have.append((y_n,x_n))
                try:
                    v = float(eval(f'get.iloc[{y},{x}]'))#取得value
                    link.append({"source": y_n, "target": x_n, "value": v})
                except:
                    pass
        c = (
            Graph(**self.initSetting(args))
                .add(f"{y_name[0]}", nodes, link, repulsion=args['Repulsion'],**self.y_Label(args))
                .set_global_opts(**self.global_set(args, f"{name}关系图", 0, 100, False,False))
        )
        self.R_Dic[f'{name}关系图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Sankey(self,name,text):
        get = self.get_Sheet(name)
        args = self.Parsing_Parameters(text)
        size = args['Size']*3

        #生成节点信息
        y_name = self.get_Index(name,True).tolist()#拿行名
        x_name = self.get_Column(name,True).tolist()#拿列名
        nodes_list = list(set(y_name + x_name))#处理重复，作为nodes列表
        nodes = []
        source = {}
        target = {}
        for i in nodes_list:
            nodes.append({"name": f"{i}"})
            source[i] = set()#记录该元素source边连接的节点
            target[i] = set()#记录改元素target边连接的节点

        #生成link信息
        link = []  # 记录连接的信息
        have = []
        for y in range(len(y_name)):#按行迭代
            for x in range(len(x_name)):
                y_n = y_name[y]#节点1
                x_n = x_name[x]#节点2
                if y_n == x_n:continue#是否相同
                if (y_n,x_n) in have or (x_n,y_n) in have :continue#是否重复
                else:have.append((y_n,x_n))
                #固定的，y在s而x在t，桑基图不可以绕环形，所以要做检查
                if source[y_n] & target[x_n] != set():continue
                try:
                    v = float(eval(f'get.iloc[{y},{x}]'))#取得value
                    link.append({"source": y_n, "target": x_n, "value": v})
                    target[y_n].add(x_n)
                    source[x_n].add(y_n)
                except:
                    pass
        c = (
            Sankey()
                .add(
                f"{name}",
                nodes,
                link,
                linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
                label_opts=opts.LabelOpts(position="right"),
            )
                .set_global_opts(**self.global_set(args, f"{name}桑基图", 0, 100, False, False))
        )
        self.R_Dic[f'{name}桑基图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Parallel(self,name,text) -> Parallel:
        get = self.get_Sheet(name)
        dim = []
        dim_list = self.get_Index(name,True).tolist()
        for i in range(len(dim_list)):
            dim.append({"dim": i, "name": f"{dim_list[i]}"})
        args = self.Parsing_Parameters(text)
        c = (
            Parallel(**self.initSetting(args))
                .add_schema(dim)
                .set_global_opts(**self.global_set(args, f"{name}多轴图", 0, 100, False, False))
        )
        for i in get.iteritems():  # 按列迭代
            q = i[1].tolist()  # 转换为列表
            c.add(f"{i[0]}",[q],**self.y_Label(args))
        self.R_Dic[f'{name}多轴图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Pie(self,name,text) -> Pie:
        get = self.get_Sheet(name)
        data = []
        for i in get.iterrows():#按行迭代
            try:
                data.append([f'{i[0]}',float(i[1].tolist()[0])])
            except:pass
        args = self.Parsing_Parameters(text)
        c = (
            Pie(**self.initSetting(args))
                .add(f"{name}", data,**self.y_Label(args,'top'))
                .set_global_opts(**self.global_set(args, f"{name}饼图", 0, 100, False, False))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        self.R_Dic[f'{name}饼图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Polar(self,name,text) -> Polar:
        get = self.get_Sheet(name)
        data = []
        args = self.Parsing_Parameters(text)
        setting = self.Per_Seeting(args, 'Polar')
        if setting == 'rad':#弧度制
            D = 0.0628
        elif setting == '360':#角度制
            D = 0.36
        else:
            D = 1
        for i in get.iterrows():#按行迭代
            try:
                q = i[1].tolist()
                data.append((float(q[0]),float(q[1])/D))
            except:pass
        c = (
            Polar(**self.initSetting(args))
                .add(f"{name}", data, type_="scatter",**self.y_Label(args))
                .set_global_opts(**self.global_set(args, f"{name}极坐标图", 0, 100, False, False))
        )
        self.R_Dic[f'{name}极坐标图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Radar(self,name,text) -> Radar:
        get = self.get_Sheet(name)
        x = self.get_Index(name,True).tolist()
        Max_list = [[] for i in range(len(x))]#保存每个x栏目的最大值
        data = []#y的组成数据，包括name和list
        x_list = []#保存x的数据

        for i in get.iteritems():  # 按列迭代计算每一项的abcd
            q = i[1].tolist()
            add = []
            for a in range(len(q)):
                try:
                    f = float(q[a])
                    Max_list[a].append(f)
                    add.append(f)
                except:pass
            data.append([f'{i[0]}',[add]])#add是包含在一个list中的

        for i in range(len(Max_list)):#计算x_list
            x_list.append(opts.RadarIndicatorItem(name=x[i], max_=max(Max_list[i])))
        args = self.Parsing_Parameters(text)
        c = (
            Radar(**self.initSetting(args))
                .add_schema(
                schema=x_list
            )
                .set_global_opts(**self.global_set(args, f"{name}雷达图", 0, 100, False, False))
        )
        k = self.Per_Seeting(args,'Radar')
        for i in data:
            c.add(*i,**self.y_Label(args),color=self.get_Color(),**k)#对i解包，取得name和data 随机颜色
        self.R_Dic[f'{name}雷达图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def get_Color(self):
        # 随机颜色，雷达图默认非随机颜色
        rgb = [randint(0, 255), randint(0, 255), randint(0, 255)]
        color = '#'
        for a in rgb:
            color += str(hex(a))[-2:].replace('x', '0').upper()  # 转换为16进制,upper表示小写(规范化)
        return color

    def to_WordCloud(self,name,text) -> WordCloud:
        get = self.get_Sheet(name)
        data = []
        for i in get.iterrows():  # 按行迭代
            try:
                data.append([str(i[0]),float(i[1].tolist()[0])])
            except:pass
        args = self.Parsing_Parameters(text)
        c = (
            WordCloud(**self.initSetting(args))
                .add(f"{name}", data, **self.Per_Seeting(args,'WordCloud'))
                .set_global_opts(**self.global_set(args, f"{name}词云", 0, 100, False, False))
        )
        self.R_Dic[f'{name}词云[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Liquid(self,name,text) -> Liquid:
        get = self.get_Sheet(name)
        data = str(get.iloc[0,0])
        c = data.split('.')
        try:
            data = float(f'0.{c[1]}')
        except:
            data = float(f'0.{c[0]}')
        args = self.Parsing_Parameters(text)
        c = (
            Liquid(**self.initSetting(args))
                .add(f"{name}", [data, data])
                .set_global_opts(title_opts=opts.TitleOpts(title=f"{name}水球图", subtitle="CoTan~数据处理"))
        )
        self.R_Dic[f'{name}水球图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Gauge(self,name,text) -> Gauge:
        get = self.get_Sheet(name)
        data = float(get.iloc[0,0])
        if data > 100:
            data = str(data/100)
            c = data.split('.')
            try:
                data = float(f'0.{c[1]}')*100
            except:
                data = float(f'0.{data}')*100
        args = self.Parsing_Parameters(text)
        c = (
            Gauge(**self.initSetting(args))
                .add(f"{name}", [(f"{name}", data)])
                .set_global_opts(title_opts=opts.TitleOpts(title=f"{name}仪表图", subtitle="CoTan~数据处理"))
        )
        self.R_Dic[f'{name}仪表图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Calendar(self,name,text) -> Calendar:
        get = self.get_Sheet(name)
        data = [[] for i in self.get_Column(name,True)]
        x_name = self.get_Column(name,True).tolist()
        y = []
        for i in get.iterrows():
            Date = str(i[0])#时间数据
            q = i[1].tolist()
            for a in range(len(q)):
                try:
                    data[a].append([Date,q[a]])
                    y.append(float(q[a]))
                except:
                    pass
        args = self.Parsing_Parameters(text)
        if y == []:
            y = [0,100]
            args['show_Visual_mapping'] = False  # 关闭视觉映射
        c = (
            Calendar(**self.initSetting(args))
                .set_global_opts(**self.global_set(args,f"{name}日历图",min(y),max(y),True))
        )
        for i in range(len(x_name)):
            start_Date = data[i][0][0]
            end_Date = data[i][-1][0]
            c.add(str(x_name[i]), data[i], calendar_opts=opts.CalendarOpts(range_=[start_Date,end_Date]), **self.y_Label(args))
        self.R_Dic[f'{name}日历图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_ThemeRiver(self,name,text) -> ThemeRiver:
        get = self.get_Sheet(name)
        data = []
        x_name = self.get_Column(name,True).tolist()
        y = []
        for i in get.iterrows():
            Date = str(i[0])
            q = i[1].tolist()
            for a in range(len(x_name)):
                try:
                    data.append([Date, q[a], x_name[a]])
                    y.append(float(q[a]))
                except:
                    pass
        args = self.Parsing_Parameters(text)
        if y == []:
            y = [0,100]
            args['show_Visual_mapping'] = False  # 关闭视觉映射
        c = (
            ThemeRiver(**self.initSetting(args))
                .add(x_name,data,singleaxis_opts=opts.SingleAxisOpts(type_=args['x_type'],pos_bottom="10%"))#抑制大小
                .set_global_opts(**self.global_set(args,f"{name}河流图",min(y),max(y),True,False))
        )
        self.R_Dic[f'{name}河流图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Sunburst(self,name,text) -> Sunburst:
        get = self.get_Sheet(name)
        def Done(Iter, name):
            k = {'name': name, 'children': []}
            v = 0
            for i in Iter:
                content = Iter[i]
                if isinstance(content, dict):
                    new_C = Done(content, str(i))
                    v += new_C['value']
                    k['children'].append(new_C)
                else:
                    try:
                        q = float(content)
                    except:
                        q = len(str(content))
                    v += q
                    k['children'].append({'name': f'{i}={content}', 'value': q})
            k['value'] = v
            return k
        data = Done(get.to_dict(),name)['children']
        args = self.Parsing_Parameters(text)
        c = (
            Sunburst()
                .add(series_name=f'{name}', data_pair=data, radius=[abs(args['Size']-10), "90%"])
                .set_global_opts(**self.global_set(args, f"{name}旭日图", 0, 100, False, False))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
        )
        self.R_Dic[f'{name}旭日图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Tree(self,name,text) -> Tree:
        get = self.get_Sheet(name)
        def Done(Iter, name):
            k = {'name': name, 'children': []}
            for i in Iter:
                content = Iter[i]
                if isinstance(content, dict):
                    new_C = Done(content, str(i))
                    k['children'].append(new_C)
                else:
                    k['children'].append({'name': f'{i}', 'children': [{'name': f'{content}'}]})
            return k
        data = [Done(get.to_dict(),name)]
        args = self.Parsing_Parameters(text)
        c = (
            Tree()
                .add(f"{name}", data)
                .set_global_opts(**self.global_set(args, f"{name}树状图", 0, 100, False, False))
        )
        self.R_Dic[f'{name}树状图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_TreeMap(self,name,text) -> TreeMap:
        get = self.get_Sheet(name)
        def Done(Iter, name):
            k = {'name': name, 'children': []}
            v = 0
            for i in Iter:
                content = Iter[i]
                if isinstance(content, dict):
                    new_C = Done(content, str(i))
                    v += new_C['value']
                    k['children'].append(new_C)
                else:
                    try:
                        q = float(content)
                    except:
                        q = len(str(content))
                    v += q
                    k['children'].append({'name': f'{i}={content}', 'value': q})
            k['value'] = v
            return k
        data = Done(get.to_dict(),name)['children']
        args = self.Parsing_Parameters(text)
        c = (
            TreeMap()
                .add(f"{name}", data, label_opts=opts.LabelOpts(is_show=True, position='inside'))
                .set_global_opts(**self.global_set(args, f"{name}矩形树图", 0, 100, False, False))
        )
        self.R_Dic[f'{name}矩形树图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_ScatterGeo(self,name,text) -> Geo:
        get = self.get_Sheet(name)
        column = self.get_Column(name,True).tolist()
        data_Type = ["scatter" for _ in column]
        data = [[] for _ in column]
        y = []
        for i in get.iterrows():  # 按行迭代
            map = str(i[0])
            q = i[1].tolist()
            for a in range(len(q)):
                try:
                    v = float(q[a])
                    y.append(v)
                except:
                    v = str(q[a])
                    try:
                        if v[:5] == '[##S]':
                            #特效图
                            v = float(v[5:])
                            y.append(v)
                            column.append(column[a])
                            data_Type.append(GeoType.EFFECT_SCATTER)
                            data.append([])
                            a = -1
                        elif v[:5] == '[##H]':
                            # 特效图
                            v = float(v[5:])
                            y.append(v)
                            column.append(column[a])
                            data_Type.append(GeoType.HEATMAP)
                            data.append([])
                            a = -1
                        else:raise Exception
                    except:
                        data_Type[a] = GeoType.LINES#当前变为Line
                data[a].append((map, v))
        args = self.Parsing_Parameters(text)
        args['show_Visual_mapping'] = True#必须视觉映射
        if y == []:y = [0,100]
        if args['is_Dark']:
            g = {'itemstyle_opts':opts.ItemStyleOpts(color="#323c48", border_color="#111")}
        else:
            g = {}
        c = (
            Geo()
                .add_schema(
                maptype=str(args['Map']),**g
            )
                .set_global_opts(**self.global_set(args, f"{name}Geo点地图", min(y), max(y), False))#必须要有视觉映射(否则会显示奇怪的数据)
        )
        for i in range(len(data)):
            if data_Type[i] != GeoType.LINES:
                ka = dict(symbol=args['Symbol'],symbol_size=args['Size'],color='#1E90FF' if args['is_Dark'] else '#0000FF')
            else:
                ka = dict(symbol=SymbolType.ARROW, symbol_size=6,effect_opts=opts.EffectOpts(symbol=SymbolType.ARROW, symbol_size=6, color="blue"),linestyle_opts=opts.LineStyleOpts(curve=0.2,color='#FFF8DC' if args['is_Dark'] else '#000000'))
            c.add(f'{column[i]}',data[i],type_=data_Type[i],**ka)
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示数据,必须放在add后面生效
        self.R_Dic[f'{name}Geo点地图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Map(self,name,text) -> Map:
        get = self.get_Sheet(name)
        column = self.get_Column(name,True).tolist()
        data = [[] for _ in column]
        y = []
        for i in get.iterrows():  # 按行迭代
            map = str(i[0])
            q = i[1].tolist()
            for a in range(len(q)):
                try:
                    v = float(q[a])
                    y.append(v)
                    data[a].append((map, v))
                except:
                    pass
        args = self.Parsing_Parameters(text)
        args['show_Visual_mapping'] = True#必须视觉映射
        if y == []:y = [0,100]
        if args['map_Type'] == 'GLOBE':
            Func = MapGlobe
        else:
            Func = Map
        c = Func().set_global_opts(**self.global_set(args, f"{name}Map地图", min(y), max(y), False))#必须要有视觉映射(否则会显示奇怪的数据)
        for i in range(len(data)):
            c.add(f'{column[i]}',data[i],str(args['Map']),is_map_symbol_show=args['show_Map_Symbol'],symbol=args['Symbol'],**self.y_Label(args))
        self.R_Dic[f'{name}Map地图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Geo(self,name,text) -> Geo:
        get = self.get_Sheet(name)
        column = self.get_Column(name,True).tolist()
        index = self.get_Index(name,True).tolist()
        args = self.Parsing_Parameters(text)
        args['show_Visual_mapping'] = True  # 必须视觉映射
        if args['is_Dark']:
            g = {'itemstyle_opts':opts.ItemStyleOpts(color="#323c48", border_color="#111")}
        else:
            g = {}
        c = (
            Geo()
                .add_schema(maptype=str(args['Map']),**g)
            )
        m = []
        for y in column:  # 维度
            for x in index:  # 精度
                value = get.loc[x, y]
                try:
                    v = float(value)  # 数值
                    type_ = args['Geo_Type']
                except:
                    try:
                        q = str(value)
                        v = float(value[5:])
                        if q[:5] == '[##S]':#点图
                            type_ = GeoType.SCATTER
                        elif q[:5] == '[##E]':#带点特效
                            type_ = GeoType.EFFECT_SCATTER
                        else:#画线
                            v = q.split(';')
                            c.add_coordinate(name=f'({v[0]},{v[1]})', longitude=float(v[0]), latitude=float(v[1]))
                            c.add_coordinate(name=f'({x},{y})', longitude=float(x), latitude=float(y))
                            c.add(f'{name}', [[f'({x},{y})',f'({v[0]},{v[1]})']], type_=GeoType.LINES,
                                  effect_opts=opts.EffectOpts(symbol=SymbolType.ARROW, symbol_size=6, color="blue"),
                                  linestyle_opts=opts.LineStyleOpts(curve=0.2, color='#FFF8DC' if args[
                                      'is_Dark'] else '#000000', ))
                            c.add(f'{name}_XY', [[f'({x},{y})',5],[f'({v[0]},{v[1]})',5]], type_=GeoType.EFFECT_SCATTER,
                                  color='#1E90FF' if args['is_Dark'] else '#0000FF', )
                            raise Exception #continue
                    except:
                        continue
                try:
                    c.add_coordinate(name=f'({x},{y})', longitude=float(x), latitude=float(y))
                    c.add(f'{name}', [[f'({x},{y})', v]],type_=type_,symbol=args['Symbol'],symbol_size=args['Size'])
                    if type_ == GeoType.HEATMAP:
                        c.add(f'{name}_XY', [[f'({x},{y})', v]], type_='scatter',
                              color='#1E90FF' if args['is_Dark'] else '#0000FF',)
                    m.append(v)
                except:pass
        if m == []:m = [0,100]
        c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))#不显示
        c.set_global_opts(**self.global_set(args, f"{name}Geo地图", min(m), max(m), False))
        self.R_Dic[f'{name}Geo地图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Bar3d(self,name,text) -> Bar3D:
        get = self.get_Sheet(name)
        x = self.get_Column(name, True).tolist()  # 图的x轴，下侧，列名
        y = self.get_Index(name, True).tolist()  # 图的y轴，左侧，行名
        value_list = []
        q = []
        for c in range(len(x)):  # c-列，r-行
            for r in range(len(y)):
                try:
                    v = eval(f'get.iloc[{r},{c}]')  # 先行后列
                    value_list.append([c, r, v])
                    q.append(float(v))
                except:
                    pass
        args = self.Parsing_Parameters(text)
        if q == []:
            q = [0,100]
            args['show_Visual_mapping'] = False  # 关闭视觉映射
        c = (
            Bar3D(**self.initSetting(args))
                .add(f"{name}",value_list,
                xaxis3d_opts=opts.Axis3DOpts(list(map(str,x)), type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(list(map(str,y)), type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
            )
                .set_global_opts(**self.global_set(args,f"{name}3D柱状图",min(q),max(q),True),
            ))
        if args['bar_Stacking']:c.set_series_opts(**{"stack": "stack"})#层叠
        self.R_Dic[f'{name}3D柱状图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Scatter3D(self,name,text) -> Scatter3D:
        get = self.get_Sheet(name)
        x = self.get_Column(name, True).tolist()  # 图的x轴，下侧，列名
        y = self.get_Index(name, True).tolist()  # 图的y轴，左侧，行名
        value_list = []
        q = []
        for c in range(len(x)):  # c-列，r-行
            for r in range(len(y)):
                try:
                    v = eval(f'get.iloc[{r},{c}]')  # 先行后列
                    value_list.append([c, r, v])
                    q.append(float(v))
                except:
                    pass
        args = self.Parsing_Parameters(text)
        if q == []:
            q = [0,100]
            args['show_Visual_mapping'] = False  # 关闭视觉映射
        c = (
            Scatter3D(**self.initSetting(args))
                .add(f"{name}",value_list,
                xaxis3d_opts=opts.Axis3DOpts(list(map(str, x)), type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(list(map(str, y)), type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
            )
                .set_global_opts(**self.global_set(args,f"{name}3D散点图",min(q),max(q),True))
        )
        self.R_Dic[f'{name}3D散点图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_Line3D(self,name,text) -> Line3D:
        get = self.get_Sheet(name)
        x = self.get_Column(name, True).tolist()  # 图的x轴，下侧，列名
        y = self.get_Index(name, True).tolist()  # 图的y轴，左侧，行名
        value_list = []
        q = []
        for c in range(len(x)):  # c-列，r-行
            for r in range(len(y)):
                try:
                    v = eval(f'get.iloc[{r},{c}]')  # 先行后列
                    value_list.append([c, r, v])
                    q.append(float(v))
                except:
                    pass
        args = self.Parsing_Parameters(text)
        if q == []:
            q = [0,100]
            args['show_Visual_mapping'] = False  # 关闭视觉映射
        c = (
            Line3D(**self.initSetting(args))
                .add(f"{name}",value_list,
                xaxis3d_opts=opts.Axis3DOpts(list(map(str, x)), type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(list(map(str, y)), type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
                grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
            )
                .set_global_opts(**self.global_set(args,f"{name}3D折线图",min(q),max(q),True))
            )
        self.R_Dic[f'{name}3D折线图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c


    def Tra_RDic(self):
        self.R_Dic = {}

    def Draw_Page(self, text, Dic) -> Page:
        args = self.Parsing_Parameters(text)
        if args['page_Title'] == '':
            title = 'CoTan_数据处理'
        else:
            title = f"CoTan_数据处理:{args['page_Title']}"
        if args['HTML_Type'] == 1:
            page = Page(page_title=title, layout=Page.DraggablePageLayout)
            page.add(*self.R_Dic.values())
        elif args['HTML_Type'] == 2:
            page = Page(page_title=title, layout=Page.SimplePageLayout)
            page.add(*self.R_Dic.values())
        else:
            page = Tab(page_title=title)
            for i in self.R_Dic:
                page.add(self.R_Dic[i], i)
        page.render(Dic)
        return Dic

    def Overlap(self, down, up):
        Over_Down = self.R_Dic[down]
        Over_Up = self.R_Dic[up]
        Over_Down.overlap(Over_Up)
        return Over_Down

class Machine_Learner(Draw):#数据处理者

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Learner = {}#记录机器
        self.Learn_Dic = {'Line':(LinearRegression,()),
                          'Ridge':(Ridge,('alpha','max_iter',)),
                          'Lasso':(Lasso,('alpha','max_iter',)),
                          'LogisticRegression':(LogisticRegression,('C')),
                          'Knn':(KNeighborsClassifier,('n_neighbors',)),
                          'Knn_class': (KNeighborsRegressor, ('n_neighbors',)),
                          }
        self.Learner_Type = {}#记录机器的类型

    def DecisionTreeClassifier(self, name):#特征提取
        get = self.get_Sheet(name)
        Dver = DictVectorizer()
        get_Dic = get.to_dict(orient='records')
        new = Dver.fit_transform(get_Dic).toarray()
        Dec = pd.DataFrame(new, columns=Dver.feature_names_)
        self.Add_Form(Dec,f'{name}:特征')
        return Dec

    def p_Args(self,Text):#解析参数
        args = {}
        args_use = {}
        #输入数据
        exec(Text,args)
        #处理数据
        args_use['alpha'] = float(args.get('alpha',1.0))#L1和L2正则化用
        args_use['C'] = float(args.get('C', 1.0))  # L1和L2正则化用
        args_use['max_iter'] = int(args.get('max_iter', 1000))  # L1和L2正则化用
        args_use['n_neighbors'] = int(args.get('K_knn', 5))#knn邻居数 (命名不同)
        args_use['nDim_2'] = bool(args.get('nDim_2', True))  # 数据是否降维
        return args_use

    def Add_Learner(self,Learner,Text=''):
        get,args_Tuple = self.Learn_Dic[Learner]
        name = f'Le[{len(self.Learner)}]{Learner}'
        #参数调节
        args_use = self.p_Args(Text)
        args = {}
        for i in args_Tuple:
            args[i] = args_use[i]
        #生成学习器
        self.Learner[name] = get(**args)
        self.Learner_Type[name] = Learner

    def Return_Learner(self):
        return self.Learner.copy()

    def get_Learner(self,name):
        return self.Learner[name]

    def get_Learner_Type(self,name):
        return self.Learner_Type[name]

    def Fit(self,name,Learnner,Text='',**kwargs):
        Type = self.get_Learner_Type(Learnner)
        args_use = self.p_Args(Text)
        if Type in ('Line','Ridge','Lasso','LogisticRegression','Knn','Knn_class'):
            return self.Fit_Simp(name,Learnner,Down_Ndim=args_use['nDim_2'],**kwargs)

    def Fit_Simp(self,name,Learner,Score_Only=False,Down_Ndim=True,split=0.3,**kwargs):#Score_Only表示仅评分 Fit_Simp 是普遍类操作
        get = self.get_Sheet(name)
        x = get.to_numpy()
        y = self.get_Index(name,True)#获取y值(用index作为y)
        if Down_Ndim or x.ndim == 1:#执行降维处理（也包括升维，ravel让一切变成一维度，包括数字）
            a = x
            x = []
            for i in a:
                try:
                    c = i.np.ravel(a[i], 'C')
                    x.append(c)
                except:
                    x.append(i)
            x = np.array(x)
        model = self.get_Learner(Learner)
        if not Score_Only:#只计算得分，全部数据用于测试
            train_x,test_x,train_y,test_y = train_test_split(x,y,test_size=split)
            model.fit(train_x,train_y)
            train_Score = model.score(train_x, train_y)
            test_Score = model.score(test_x, test_y)
            return train_Score,test_Score
        test_Score = model.score(x, y)
        return 0, test_Score

    def Predict(self,name,Learner,Text='',**kwargs):
        Type = self.get_Learner_Type(Learner)
        args_use = self.p_Args(Text)
        if Type in ('Line','Ridge','Lasso','LogisticRegression','Knn','Knn_class'):
            return self.Predict_Simp(name,Learner,Down_Ndim=args_use['nDim_2'],**kwargs)

    def Predict_Simp(self,name,Learner,Down_Ndim=True,**kwargs):
        get = self.get_Sheet(name)
        column = self.get_Column(name,True)
        x = get.to_numpy()
        if Down_Ndim or x.ndim == 1:#执行降维处理（也包括升维，ravel让一切变成一维度，包括数字）
            a = x
            x = []
            for i in a:
                try:
                    c = i.np.ravel(a[i], 'C')
                    x.append(c)
                except:
                    x.append(i)
            x = np.array(x)
        model = self.get_Learner(Learner)
        answer = model.predict(x)
        data = pd.DataFrame(x,index=answer,columns=column)
        self.Add_Form(data,f'{name}:预测')
        return data

    def Show_Args(self,Learner,new=False):#显示参数
        learner = self.get_Learner(Learner)
        learner_Type = self.get_Learner_Type(Learner)
        if learner_Type in ('Ridge','Lasso'):
            Alpha = learner.alpha#阿尔法
            w = learner.coef_.tolist()#w系数
            b = learner.intercept_#截距
            max_iter = learner.max_iter
            w_name = [f'权重:W[{i}]' for i in range(len(w))]
            index = ['阿尔法:Alpha'] + w_name + ['截距:b','最大迭代数']
            data = [Alpha] + w + [b] + [max_iter]
            #文档
            doc = (f'阿尔法:alpha = {Alpha}\n\n权重:\nw = \n{pd.DataFrame(w)}\n\n截距:b = {b}\n\n最大迭代数:{max_iter}\n\n\nEND')
            data = pd.DataFrame(data,index=index)
        elif learner_Type in ('Line'):
            w = learner.coef_.tolist()  # w系数
            b = learner.intercept_
            index = [f'权重:W[{i}]' for i in range(len(w))] + ['截距:b']
            data = w + [b]  # 截距
            #文档
            doc = (f'权重:w = \n{pd.DataFrame(w)}\n\n截距:b = {b}\n\n\nEND')
            data = pd.DataFrame(data, index=index)
        elif learner_Type in ('Knn'):#Knn_class
            classes = learner.classes_.tolist()#分类
            n = learner.n_neighbors#个数
            p = {1:'曼哈顿距离',2:'欧几里得距离'}.get(learner.p)
            index = [f'类目[{i}]' for i in range(len(classes))] + ['邻居个数','距离公式']
            data = classes + [n,p]
            doc = f'分类类目:\n{pd.DataFrame(classes)}\n\n邻居个数:{n}\n\n计算距离的方式:{p}\n\n\nEND'
            data = pd.DataFrame(data,index=index)
        elif learner_Type in ('Knn_class'):
            n = learner.n_neighbors#个数
            p = {1:'曼哈顿距离',2:'欧几里得距离'}.get(learner.p)
            index = ['邻居个数','距离公式']
            data = [n,p]
            doc = f'邻居个数:{n}\n\n计算距离的方式:{p}\n\n\nEND'
            data = pd.DataFrame(data,index=index)
        elif learner_Type in ('LogisticRegression',):
            classes = learner.classes_.tolist()#分类
            w = learner.coef_.tolist()  # w系数
            b = learner.intercept_
            C = learner.C
            index = [f'类目[{i}]' for i in range(len(classes))] + [f'权重:W[{j}][{i}]' for i in range(len(w)) for j in range(len(w[i]))] + [f'截距:b[{i}]' for i in range(len(b))]+['C']
            data = classes + [j for i in w for j in i] + [i for i in b] + [C]
            doc = f'分类类目:\n{pd.DataFrame(classes)}\n\n权重:w = \n{pd.DataFrame(w)}\n\n截距:b = {b}\n\nC={C}\n\n\n'
            data = pd.DataFrame(data,index=index)
        else:
            return '',[]
        if new:
            self.Add_Form(data,f'{Learner}:属性')
        return doc,data

    def Del_Leaner(self,Leaner):
        del self.Learner[Leaner]
        del self.Learner_Type[Leaner]