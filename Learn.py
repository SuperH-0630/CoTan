import pandas as pd
import re
import pandas_profiling as pp
# from multiprocessing import Process
from threading import Thread
from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.globals import SymbolType
from pyecharts.components import Table
import numpy as np

class Form:
    def __init__(self):
        class DEL:pass
        self.Sheet_Dic = {}
        self.Clean_Func = {}
        self.Clean_Func_Exp = {}
        self.DEL = DEL()
        self.Name = {'pd':pd,'DEL':self.DEL,'re':re,'Sheet':self.Sheet_Dic}
        self.R_Dic = {}#存放所有的图

    def get_Sheet(self,name,all_Row = None,all_Colunms=None) -> pd.DataFrame:
        try:
            pd.set_option('display.max_rows',all_Row)
            pd.set_option('display.max_columns',all_Colunms)
        except:pass
        return self.Sheet_Dic[name]

    def Describe(self,name,make_Sheet=False):#生成描述
        get = self.get_Sheet(name)
        Des = get.describe()
        if make_Sheet:self.Add_Form(Des,f'{name}_describe[{len(self.Sheet_Dic)}]')
        shape = get.shape
        dtype = get.dtypes
        n = get.ndim
        head = get.head()
        tail = get.tail(3)
        return f'1)基本\n{Des}\n\n2)形状:{shape}\n\n3)数据类型\n{dtype}\n\n4)数据维度:{n}\n\n5)头部数据\n{head}\n\n6)尾部数据\n{tail}' \
               f'\n\n7)行名\n{get.index}\n\n8)列名\n{get.columns}'

    def Add_Form(self,Data,name=''):
        if name == '':name = f'Sheet[{len(self.Sheet_Dic)}]'
        self.Sheet_Dic[name] = Data
        return Data

    def __Add_Form(self,Dic,Func,name='',Index=True,**kwargs):#新增表格的核心方式
        try:
            Data = Func(Dic,**kwargs)
        except UnicodeDecodeError:
            return False
        if not Index:
            Data.index = Data.iloc[:,0].tolist()
            Data.drop(Data.columns.values.tolist()[0],inplace=True,axis=1)
        return self.Add_Form(Data,name)

    def Add_CSV(self,Dic,name='',Sep=',',code='utf-8',str_=True,Index=True):
        if str_:
            k = {'dtype':'object'}
        else:
            k = {}
        return self.__Add_Form(Dic,pd.read_csv,name,Index,sep=Sep,encoding=code,**k)

    def Add_Python(self,Text,sheet_name=''):
        name = {}
        name.update(globals().copy())
        name.update(locals().copy())
        exec(Text,name)
        exec('get = Creat()',name)
        if isinstance(name['get'],pd.DataFrame):
            self.Add_Form(name['get'],sheet_name)
        else:
            try:
                get = pd.DataFrame(name['get'])
                self.Add_Form(get, sheet_name)
            except:pass

    def Add_Html(self,Dic,name='',code='utf-8',str_=True,Index=True):
        if str_:
            k = {'dtype':'object'}
        else:
            k = {}
        return self.__Add_Form(Dic,pd.read_html,name,Index,encoding=code,**k)

    def get_FormList(self):
        return list(self.Sheet_Dic.keys())#返回列表

    def to_Html(self,name,Dic='',type_=0):
        if Dic == '': Dic = f'{name}.html'
        #把要画的sheet放到第一个
        Sheet_Dic = self.Sheet_Dic.copy()
        del Sheet_Dic[name]
        Sheet_list = [name] + list(Sheet_Dic.keys())

        class TAB_F:
            def __init__(self, q):
                self.tab = q  # 一个Tab
            def render(self, Dic):
                return self.tab.render(Dic)

        #生成一个显示页面
        if type_ == 0:
            class TAB(TAB_F):
                def add(self,table,k,*f):
                    self.tab.add(table,k)
            tab = TAB(Tab(page_title='CoTan:查看表格'))#一个Tab
        elif type_ == 1:
            class TAB(TAB_F):
                def add(self,table,*k):
                    self.tab.add(table)
            tab = TAB(Page(page_title='CoTan:查看表格', layout=Page.DraggablePageLayout))
        else:
            class TAB(TAB_F):
                def add(self,table,*k):
                    self.tab.add(table)
            tab = TAB(Page(page_title='CoTan:查看表格', layout=Page.SimplePageLayout))
        #迭代添加内容
        for name in Sheet_list:
            get = self.get_Sheet(name)
            headers = [f'{name}'] + self.get_Column(name,True).tolist()
            rows = []
            table = Table()
            for i in get.iterrows():  # 按行迭代
                q = i[1].tolist()
                rows.append([f'{i[0]}']+q)
                table.add(headers, rows).set_global_opts(title_opts=opts.ComponentTitleOpts(title=f"表格:{name}", subtitle="CoTan~机器学习:查看表格"))
                tab.add(table,f'表格:{name}')
        tab.render(Dic)
        return Dic

    def To_Sheet_Des(self,Sheet,Dic):
        re = pp.ProfileReport(Sheet)
        re.to_file(Dic)

    def to_Report(self,name,Dic=''):
        if Dic == '': Dic = f'{name}.html'
        Sheet = self.get_Sheet(name)
        self.To_Sheet_Des(Sheet,Dic)
        return Dic

    def get_Column(self,name,only=False):#列名
        get = self.get_Sheet(name)
        if only:
            re = get.columns.values
        else:
            re = []
            loc_list = get.columns.values
            print(loc_list)
            a = 0
            for i in loc_list:
                data = get[i].to_list()
                re.append(f'[列号:{a}]{i} -> {data}')
                a += 1
        return re

    def get_Index(self,name,only=False):
        get = self.get_Sheet(name)
        if only:
           re = get.index.values
        else:
            re = []
            loc_list = get.index.values
            print(loc_list)
            a = 0
            for i in range(len(loc_list)):
                l = loc_list[i]
                data = get.iloc[i].to_list()
                re.append(f'[行号:{a}]{l} -> {data}')
                a += 1
        return re

    def Sorted(self,name,row:bool,new=False,a=True):
        get = self.get_Sheet(name)
        if row:#row-行名排序
            so = get.sort_index(axis=0, ascending=a)
        else:
            so = get.sort_index(axis=1, ascending=a)
        if new:
            self.Add_Form(so)
        return so

    def Stored_Valuse(self,name,F,new=False):
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
        so = get.sort_values(by=a,ascending=b)
        if new:
            self.Add_Form(so)
        return so

    def T(self,name,new=True):
        get = self.get_Sheet(name)
        re = get.T
        if new:
            self.Add_Form(re)
        return re

    def get_Clice(self,name,Column,Row,U_iloc=True,new=False):#iloc(Row,Column) or loc
        get = self.get_Sheet(name)
        if U_iloc:
            Cli = get.iloc[Row,Column]
        else:
            Cli = get.loc[Row, Column]
        if new:
            self.Add_Form(Cli)
        return Cli

    def Delete(self,name,Column,Row,new):
        get = self.get_Sheet(name)
        Column_List = get.columns.values
        for i in Column:
            try:
                get = get.drop(Column_List[int(i)],axis=1)
            except:pass
        Row_List = get.index.values
        for i in Row:
            try:
                get = get.drop(Row_List[int(i)])
            except:raise
        if new:
            self.Add_Form(get)
        return get

    def Done_Bool(self,name,Exp,new=False):
        get = self.get_Sheet(name)
        try:
            re = eval(Exp,{'S':get,'Sheet':get.iloc})
            if new:
                self.Add_Form(re)
            return re
        except:
            return None
            # raise

    def is_Na(self,name):
        get = self.get_Sheet(name)
        Na = pd.isna(get)
        return Na

    def Dropna(self,name,new):
        get = self.get_Sheet(name)
        Clean = get.dropna(axis=0)
        if new:
            self.Add_Form(Clean)
        return Clean

    def Add_CleanFunc(self,Exp):
        Name = self.Name.copy()
        try:
            exec(Exp,Name)
        except:
            return False
        Sava = {}
        Sava['Done_Row'] = Name.get('Done_Row', [])
        Sava['Done_Column'] = Name.get('Done_Column', [])
        Sava['axis'] = Name.get('axis', True)
        Sava['check'] = Name.get('check', lambda data,x,b,c,d,e:True)
        Sava['done'] = Name.get('done', lambda data,x,b,c,d,e:data)
        title = f"[{Name.get('name', f'{len(self.Clean_Func)}')}] Done_Row={Sava['Done_Row']}_Done_Column={Sava['Done_Column']}_axis={Sava['axis']}"
        self.Clean_Func[title] = Sava
        self.Clean_Func_Exp[title] = Exp

    def Return_CleanFunc(self):
        return list(self.Clean_Func.keys())

    def Delete_CleanFunc(self,key):
        try:
            del self.Clean_Func[key]
            del self.Clean_Func_Exp[key]
        except:
            pass

    def Tra_Clean(self):
        self.Clean_Func = {}
        self.Clean_Func_Exp = {}

    def Return_CleanExp(self,key):
        return self.Clean_Func_Exp[key]

    def Done_CleanFunc(self,name):
        get = self.get_Sheet(name).copy()
        for i in list(self.Clean_Func.values()):
            Done_Row = i['Done_Row']
            Done_Column = i['Done_Column']
            if Done_Row == []:
                Done_Row = range(get.shape[0])#shape=[行,列]#不需要回调
            if Done_Column == []:
                Done_Column = range(get.shape[1])  # shape=[行,列]#不需要回调
            if i['axis']:axis = 0
            else:axis = 1
            check = i['check']
            done = i['done']
            for r in Done_Row:
                for c in Done_Column:
                    try:
                        print(f'r={r},c={c}')
                        n = eval(f"get.iloc[{r},{c}]")#第一个是行名，然后是列名
                        r_h = eval(f"get.iloc[{r}]")
                        c_h = eval(f"get.iloc[:,{c}]")
                        print(f'n={n}')
                        if not check(n,r,c,get,r_h,c_h):
                            d = done(n,r,c,get,r_h,c_h)
                            if d == self.DEL:
                                if axis == 0:#常规删除
                                    Row_List = get.index.values
                                    get = get.drop(Row_List[int(r)])
                                else:#常规删除
                                    Columns_List = get.columns.values
                                    get = get.drop(Columns_List[int(r)],axis=1)
                            else:
                                exec(f"get.iloc[{r},{c}] = {d}")#第一个是行名，然后是列名
                    except:raise
        return get

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
        args_use['title'] = args.get('title',None)
        args_use['vice_title'] = args.get('vice_title', 'CoTan~机器学习:')
        args_use['show_Legend'] = bool(args.get('show_Legend', True))#是否显示图例
        args_use['ori_Legend'] = args.get('ori_Legend', 'horizontal')#朝向

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

        args_use['Tool_BOX'] = bool(args.get('Tool_BOX', True))  # 开启工具箱

        args_use['Theme'] = args.get('Theme', 'white')  # 设置style
        args_use['BG_Color'] = args.get('BG_Color', None)  # 设置背景颜色
        args_use['width'] = args.get('width', '900px')  # 设置宽度
        args_use['heigh'] = args.get('heigh', '500px') if not bool(args.get('Square', False)) else args.get('width', '900px')  # 设置高度
        args_use['page_Title'] = args.get('page_Title', '')  # 设置HTML标题
        args_use['show_Animation'] = args.get('show_Animation', True)  # 设置HTML标题

        args_use['show_Axis'] = bool(args.get('show_Axis', True))  # 显示坐标轴
        args_use['Axis_Zero'] = bool(args.get('Axis_Zero', False))  # 重叠于原点
        args_use['show_Axis_Scale'] = bool(args.get('show_Axis_Scale', True))  # 显示刻度

        args_use['x_type'] = args.get('x_type', None)  # 坐标轴类型
        args_use['y_type'] = args.get('y_type', None)
        args_use['z_type'] = args.get('z_type', None)

        args_use['make_Line'] = args.get('make_Line', [])  # 设置直线
        args_use['Datazoom'] = args.get('Datazoom', 'N')  # 设置Datazoom

        args_use['show_Text'] = bool(args.get('show_Text', False))  # 显示文字

        #Bar设置
        args_use['bar_Stacking'] = bool(args.get('bar_Stacking', False))  # 堆叠(2D和3D)

        #散点图设置
        args_use['EffectScatter'] = bool(args.get('EffectScatter', True))  # 开启特效(2D和3D)
        args_use['symbol_Scatter'] = args.get('EffectScatter', 'circle')  # 散点样式
        args_use['size_Scatter'] = args.get('size_Scatter', 10)  # 散点图大小

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

        args_use['Area_radar'] = bool(args.get('symbol_Graph', True))  # 雷达图面积

        args_use['HTML_Type'] = args.get('HTML_Type', 1)  # 雷达图面积
        return args_use

    #全局设定，返回一个全局设定的字典，解包即可使用
    def global_set(self,args_use,title,Min,Max,DataZoom=False,Visual_mapping=True):
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

        return k

    def get_name(self,args_use):
        return f":{args_use['title']}"

    def initSetting(self,args_use):
        k = {}
        #设置标题
        if args_use['page_Title'] == '':title = 'CoTan_机器学习'
        else:title = f"CoTan_机器学习:{args_use['page_Title']}"
        k['init_opts'] = opts.InitOpts(theme=args_use['Theme'],bg_color=args_use['BG_Color'],width=args_use['width'],
                                       height=args_use['heigh'],page_title=title,
                                       animation_opts=opts.AnimationOpts(animation=args_use['show_Animation']))
        return k

    #标记符，包含线标记、点标记以及面积标记
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

    #坐标轴设定，输入设定的坐标轴即可
    def axis_Seeting(self,args_use,axis='x'):
        k = {}
        if args_use[f'{axis[0]}_type'] == 'Display' or not args_use['show_Axis']:k[f'{axis[0]}axis_opts'] = opts.AxisOpts(is_show=False)
        else:
            k[f'{axis[0]}axis_opts'] = opts.AxisOpts(type_=args_use[f'{axis[0]}_type'],axisline_opts=opts.AxisLineOpts(is_on_zero=args_use['Axis_Zero']),
                                               axistick_opts=opts.AxisTickOpts(is_show=args_use['show_Axis_Scale']))
        return k

    #标签设定，可以放在系列设置中或者坐标轴y轴设置中
    def Label(self,args_use):
        return {'label_opts':opts.LabelOpts(is_show=args_use['show_Text'])}

    def y_Label(self,args_use):
        return {'label_opts':opts.LabelOpts(is_show=args_use['show_Text'],position="inside")}

    #放在不同的图~.add中的设定
    def Per_Seeting(self,args_use,type_):#私人设定
        k = {}
        if type_ == 'Bar':#设置y的重叠
            if args_use['bar_Stacking']:
                k =  {"stack":"stack1"}
        elif type_ == 'Scatter':
            k['Beautiful'] = args_use['EffectScatter']
            k['symbol'] = args_use['symbol_Scatter']
            k['symbol_size'] = args_use['size_Scatter']
        elif type_ == 'Line':
            k['is_connect_nones'] = args_use['connect_None']
            k['is_smooth'] = True if args_use['Smooth_Line'] or args_use['paste_Y'] else False#平滑曲线或连接y轴
            k['areastyle_opts']=opts.AreaStyleOpts(opacity=0.5 if args_use['Area_chart'] else 0)
            if args_use['step_Line']:
                del k['is_smooth']
                k['is_step'] = True
        elif type_ == 'PictorialBar':
            k['symbol_size'] = args_use['size_PictorialBar']
        elif type_ == 'Polar':
            return args_use['Polar_units']#回复的是单位制而不是设定
        elif type_ == 'WordCloud':
            k['word_size_range'] = args_use['WordCould_Size']#放到x轴
            k['shape'] = args_use['WordCould_Shape']  # 放到x轴
        elif type_ == 'Graph':
            k['symbol_Graph'] = args_use['symbol_Scatter']#放到x轴
        elif type_ == 'Radar':
            if args_use['Area_radar']:
                k['areastyle_opts']=opts.AreaStyleOpts(opacity=0.1)
        return k

    #坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_Bar(self,name,text) -> Bar:#Bar:数据堆叠
        get = self.get_Sheet(name)
        x = self.get_Index(name,True).tolist()
        args = self.Parsing_Parameters(text)
        c = (
            Bar(**self.initSetting(args))
            .add_xaxis(x)
        )
        y = []
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                y += q
                c.add_yaxis(i[0], q,**self.Per_Seeting(args,'Bar'),**self.y_Label(args))#i[0]是名字，i是tuple，其中i[1]是data
            except:
                pass
        c.set_global_opts(**self.global_set(args,f"{name}柱状图",min(y),max(y),True),
                          **self.axis_Seeting(args,'y'),**self.axis_Seeting(args,'x'))
        c.set_series_opts(**self.Mark(args),**self.Label(args))
        self.R_Dic[f'{name}柱状图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    # 坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_Line(self,name,text) -> Line:#折线图：连接空数据、显示数值、平滑曲线、面积图以及紧贴Y轴
        get = self.get_Sheet(name)
        x = self.get_Index(name,True).tolist()
        args = self.Parsing_Parameters(text)
        c = (
            Line(**self.initSetting(args))
            .add_xaxis(x)
        )
        y = []
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                y += q#记录最大值最小值
                c.add_yaxis(i[0], q,**self.Per_Seeting(args,'Line'),**self.y_Label(args))#i[0]是名字，i是tuple，其中i[1]是data
            except:
                pass
        c.set_global_opts(**self.global_set(args, f"{name}折线图", min(y), max(y), True),
                          **self.axis_Seeting(args, 'y'), **self.axis_Seeting(args, 'x'))
        c.set_series_opts(**self.Mark(args), **self.Label(args))
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
            .add_xaxis(x)
        )
        y = []
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                y += q
                c.add_yaxis(i[0], q,**type_,**self.y_Label(args))#i[0]是名字，i是tuple，其中i[1]是data
            except:
                pass
        c.set_global_opts(**self.global_set(args, f"{name}散点图", min(y), max(y), True),
                          **self.axis_Seeting(args, 'y'), **self.axis_Seeting(args, 'x'))
        c.set_series_opts(**self.Mark(args), **self.Label(args))
        self.R_Dic[f'{name}散点图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    # 坐标系图像:水平和垂直的数据轴：DataZoom+inside
    def to_Pictorialbar(self,name,text) -> PictorialBar:#象形柱状图：图形、剪裁图像、元素重复和间隔
        get = self.get_Sheet(name)
        x = self.get_Index(name, True).tolist()
        args = self.Parsing_Parameters(text)
        c = (
            PictorialBar(**self.initSetting(args))
                .add_xaxis(x)
                .reversal_axis()
        )
        y = []

        k = self.Per_Seeting(args, 'PictorialBar')
        for i in get.iteritems():#按列迭代
            q = i[1].tolist()#转换为列表
            try:
                y += q
                c.add_yaxis(
                i[0],
                q,
                label_opts=opts.LabelOpts(is_show=False),
                symbol_repeat=True,
                is_symbol_clip=True,
                symbol=SymbolType.ROUND_RECT,
                **k
            )
            except:
                pass
            c.set_global_opts(**self.global_set(args, f"{name}象形柱状图", min(y), max(y), True),
                              **self.axis_Seeting(args, 'y'), **self.axis_Seeting(args, 'x'))
            c.set_series_opts(**self.Mark(args), **self.Label(args))
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
            y += q
            try:
                c.add_yaxis(i[0],[q],**self.y_Label(args))
            except:
                pass
        c.set_global_opts(**self.global_set(args, f"{name}箱形图", min(y), max(y), True),
                          **self.axis_Seeting(args, 'y'), **self.axis_Seeting(args, 'x'))
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
        MAX,MIN = max(q),min(q)
        args = self.Parsing_Parameters(text)
        c = (
            HeatMap(**self.initSetting(args))
            .add_xaxis(x)
            .add_yaxis(f'{name}', y, value_list,**self.y_Label(args))
            .set_global_opts(**self.global_set(args, f"{name}热力图", MIN, MAX, True),
                                 **self.axis_Seeting(args, 'y'), **self.axis_Seeting(args, 'x'))
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
                .add(f'{name}', value)
                .set_global_opts(**self.global_set(args, f"{name}漏斗图", min(y), max(y), True, False))
                .set_series_opts(**self.Label(args))
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
                .add(f"{y_name[0]}", nodes, link, repulsion=8000,**self.y_Label(args))
                .set_global_opts(**self.global_set(args, f"{name}关系图", 0, 100, False,False))
        )
        self.R_Dic[f'{name}关系图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
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
                .add(f"{name}", data,**self.Label(args))
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
            c.add(*i,**self.y_Label(args),**k)#对i解包，取得name和data
        self.R_Dic[f'{name}雷达图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def to_WordCloud(self,name,text) -> WordCloud:
        get = self.get_Sheet(name)
        data = []
        for i in get.iterrows():  # 按行迭代
            try:
                data.append([i[0],float(i[1].tolist()[0])])
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
                .set_global_opts(title_opts=opts.TitleOpts(title=f"{name}水球图", subtitle="CoTan~机器学习"))
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
                .set_global_opts(title_opts=opts.TitleOpts(title=f"{name}仪表图", subtitle="CoTan~机器学习"))
        )
        self.R_Dic[f'{name}仪表图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
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
                    v = float(eval(f'get.iloc[{r},{c}]'))  # 先行后列
                except:continue
                q.append(v)
                value_list.append([c, r, v])
        args = self.Parsing_Parameters(text)
        c = (
            Bar3D(**self.initSetting(args))
                .add(f"{name}",value_list,
                xaxis3d_opts=opts.Axis3DOpts(x, type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(y, type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
            )
                .set_global_opts(**self.global_set(args,f"{name}3D柱状图",min(y),max(y),True),
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
                    v = float(eval(f'get.iloc[{r},{c}]'))  # 先行后列
                except:continue
                q.append(v)
                value_list.append([c, r, v])
        args = self.Parsing_Parameters(text)
        c = (
            Scatter3D(**self.initSetting(args))
                .add(f"{name}",value_list,
                xaxis3d_opts=opts.Axis3DOpts(x, type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(y, type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
            )
                .set_global_opts(**self.global_set(args,f"{name}3D散点图",min(y),max(y),True))
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
                    v = float(eval(f'get.iloc[{r},{c}]'))  # 先行后列
                except:continue
                q.append(v)
                value_list.append([c, r, v])
        args = self.Parsing_Parameters(text)
        c = (
            Line3D(**self.initSetting(args))
                .add(f"{name}",value_list,
                xaxis3d_opts=opts.Axis3DOpts(x, type_=args["x_type"]),
                yaxis3d_opts=opts.Axis3DOpts(y, type_=args["y_type"]),
                zaxis3d_opts=opts.Axis3DOpts(type_=args["z_type"]),
                grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
            )
                .set_global_opts(**self.global_set(args,f"{name}3D折线图",min(y),max(y),True))
            )
        self.R_Dic[f'{name}3D折线图[{len(self.R_Dic)}]{self.get_name(args)}'] = c
        return c

    def Import_c(self,text):
        Name = {}
        Name.update(locals())
        Name.update(globals())
        exec(text,Name)
        exec('c = Page()',Name)
        self.R_Dic[f'自定义图[{len(self.R_Dic)}]'] = Name['c']
        return Name['c']

    def retunr_RDic(self):
        return self.R_Dic.copy()

    def Delete_RDic(self,key):
        del self.R_Dic[key]

    def Draw_Page(self,text,Dic) -> Page:
        args = self.Parsing_Parameters(text)
        if args['page_Title'] == '':
            title = 'CoTan_机器学习'
        else:
            title = f"CoTan_机器学习:{args['page_Title']}"
        if args['HTML_Type'] == 1:
            page = Page(page_title=title,layout=Page.DraggablePageLayout)
            page.add(*self.R_Dic.values())
        elif args['HTML_Type'] == 2:
            page = Page(page_title=title, layout=Page.SimplePageLayout)
            page.add(*self.R_Dic.values())
        else:
            page = Tab(page_title=title)
            for i in self.R_Dic:
                page.add(self.R_Dic[i],i)
        page.render(Dic)
        return Dic

    def Reasonable_Type(self,name,column,dtype,wrong):
        get = self.get_Sheet(name).copy()
        for i in range(len(column)):
            try:
                column[i] = int(column[i])
            except:pass

        if dtype != '':
            func_Dic = {'Num':pd.to_numeric,'Date':pd.to_datetime,'Time':pd.to_timedelta}
            if column != []:
                get.iloc[:,column] = get.iloc[:,column].apply(func_Dic.get(dtype,pd.to_numeric),errors=wrong)
                print('A')
            else:
                get = get.apply(func_Dic.get(dtype,pd.to_numeric), errors=wrong)
        else:
            if column != []:
                get.iloc[:,column] = get.iloc[:,column].infer_objects()
                print('A')
            else:
                get = get.infer_objects()
        self.Add_Form(get)
        return get

    def as_Type(self,name,column,dtype,wrong):
        get = self.get_Sheet(name).copy()
        for i in range(len(column)):
            try:
                column[i] = int(column[i])
            except:
                pass
        func_Dic = {'Int': int, 'Float': float, 'Str':str}
        if column != []:
            get.iloc[:, column] = get.iloc[:, column].astype(func_Dic.get(dtype,dtype),errors=wrong)
            print('A')
        else:
            get = get.astype(func_Dic.get(dtype,dtype),errors=wrong)
        self.Add_Form(get)
        return get

    def Replace(self,name,is_column,Dic):
        get = self.get_Sheet(name)
        if is_column:
            new = get.rename(columns=Dic)
        else:
            new = get.rename(index=Dic)
        self.Add_Form(new)
        return new

    def Replace_ByList(self,name,is_column,iloc):
        pass