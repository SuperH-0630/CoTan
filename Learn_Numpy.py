from pyecharts.components import Table as Table_Fisrt#绘制表格
from pyecharts.components import Image
from pyecharts import options as opts
from random import randint
from pyecharts.charts import *
from pyecharts.charts import Tab as tab_First
from pyecharts.options.series_options import JsCode
from scipy.cluster.hierarchy import dendrogram, ward
import matplotlib.pyplot as plt
from pandas import DataFrame,read_csv
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor,export_graphviz
from sklearn.ensemble import (RandomForestClassifier,RandomForestRegressor,GradientBoostingClassifier,
                              GradientBoostingRegressor)
from sklearn.metrics import *
from sklearn.feature_selection import *
from sklearn.preprocessing import *
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA, IncrementalPCA,KernelPCA,NMF
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC,SVR#SVC是svm分类，SVR是svm回归
from sklearn.neural_network import MLPClassifier,MLPRegressor
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN
from scipy import optimize
from scipy.fftpack import fft,ifft,ifftn,fftn#快速傅里叶变换
from os.path import split as path_split
from os.path import exists,basename,splitext
from os import mkdir
import tarfile
import pickle
import joblib

#设置
np.set_printoptions(threshold=np.inf)
global_Set = dict(toolbox_opts=opts.ToolboxOpts(is_show=True),legend_opts=opts.LegendOpts(pos_bottom='3%',type_='scroll'))
global_Leg = dict(toolbox_opts=opts.ToolboxOpts(is_show=True),legend_opts=opts.LegendOpts(is_show=False))
Label_Set = dict(label_opts=opts.LabelOpts(is_show=False))

More_Global = False#是否使用全部特征绘图
All_Global = True#是否导出charts
CSV_Global = True#是否导出CSV
CLF_Global = True#是否导出模型
TAR_Global = True#是否打包tar
NEW_Global = True#是否新建目录

class Tab(tab_First):
    def __init__(self, *args,**kwargs):
        super(Tab, self).__init__(*args,**kwargs)
        self.element = {}#记录tab组成元素 name:charts

    def add(self, chart, tab_name):
        self.element[tab_name] = chart
        return super(Tab, self).add(chart, tab_name)

    def render(self,path: str = "render.html",template_name: str = "simple_tab.html",*args,**kwargs,) -> str:
        if All_Global:
            Dic = path_split(path)[0]
            for i in self.element:
                self.element[i].render(Dic + '/' + i + '.html')
        return super(Tab, self).render(path,template_name,*args,**kwargs)

class Table(Table_Fisrt):
    def __init__(self,*args,**kwargs):
        super(Table, self).__init__(*args,**kwargs)
        self.HEADERS = []
        self.ROWS = [[]]

    def add(self, headers, rows, attributes = None):
        if len(rows) == 1:
            new_headers = ['数据类型','数据']
            new_rows = list(zip(headers,rows[0]))
            self.HEADERS = new_headers
            self.ROWS = new_rows
            return super().add(new_headers,new_rows,attributes)
        else:
            self.HEADERS = headers
            self.ROWS = rows
            return super().add(headers, rows, attributes)

    def render(self,path= "render.html",*args,**kwargs,) -> str:
        if CSV_Global:
            Dic,name = path_split(path)
            name = splitext(name)[0]
            try:
                DataFrame(self.ROWS,columns = self.HEADERS).to_csv(Dic + '/' + name + '.csv')
            except:
                pass
        return super().render(path,*args,**kwargs)

def make_list(first,end,num=35):
    n = num / (end - first)
    if n == 0: n = 1
    re = []
    n_first = first * n
    n_end = end * n
    while n_first <= n_end:
        cul = n_first / n
        re.append(round(cul,2))
        n_first += 1
    return re

def list_filter(list_,num=70):
    #假设列表已经不重复
    if len(list_) <= num:return list_
    n = int(num / len(list_))
    re = list_[::n]
    return re

def Prediction_boundary(x_range,x_means,Predict_Func,Type):#绘制回归型x-x热力图
    #r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调
    # a-特征x，b-特征x-1，c-其他特征
    o_cList = []
    if len(x_means) == 1:
        return o_cList
    for i in range(len(x_means)):
        for j in range(len(x_means)):
            if j <= i:continue
            n_ra = x_range[j]
            Type_ra = Type[j]
            n_rb = x_range[i]
            Type_rb = Type[i]
            if Type_ra == 1:
                ra = make_list(n_ra[0],n_ra[1],70)
            else:
                ra = list_filter(n_ra)#可以接受最大为70

            if Type_rb == 1:
                rb = make_list(n_rb[0],n_rb[1],35)
            else:
                rb = list_filter(n_rb)#可以接受最大为70
            a = np.array([i for i in ra for _ in rb]).T
            b = np.array([i for _ in ra for i in rb]).T
            data = np.array([x_means for _ in ra for i in rb])
            data[:, j] = a
            data[:, i] = b
            y_data = Predict_Func(data)[0].tolist()
            value = [[float(a[i]), float(b[i]), y_data[i]] for i in range(len(a))]
            c = (HeatMap()
                 .add_xaxis(np.unique(a))
                 .add_yaxis(f'数据', np.unique(b), value, **Label_Set)  # value的第一个数值是x
                 .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Leg,
                                  yaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),  # 'category'
                                  xaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),
                                  visualmap_opts=opts.VisualMapOpts(is_show=True, max_=int(max(y_data))+1, min_=int(min(y_data)),
                                                                    pos_right='3%'))#显示
                 )
            o_cList.append(c)
    return o_cList

def Prediction_boundary_More(x_range,x_means,Predict_Func,Type):#绘制回归型x-x热力图
    #r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调
    # a-特征x，b-特征x-1，c-其他特征
    o_cList = []
    if len(x_means) == 1:
        return o_cList
    for i in range(len(x_means)):
        if i == 0:
            continue
        n_ra = x_range[i - 1]
        Type_ra = Type[i - 1]
        n_rb = x_range[i]
        Type_rb = Type[i]
        if Type_ra == 1:
            ra = make_list(n_ra[0],n_ra[1],70)
        else:
            ra = list_filter(n_ra)#可以接受最大为70

        if Type_rb == 1:
            rb = make_list(n_rb[0],n_rb[1],35)
        else:
            rb = list_filter(n_rb)#可以接受最大为70
        a = np.array([i for i in ra for _ in rb]).T
        b = np.array([i for _ in ra for i in rb]).T
        data = np.array([x_means for _ in ra for i in rb])
        data[:, i - 1] = a
        data[:, i] = b
        y_data = Predict_Func(data)[0].tolist()
        value = [[float(a[i]), float(b[i]), y_data[i]] for i in range(len(a))]
        c = (HeatMap()
             .add_xaxis(np.unique(a))
             .add_yaxis(f'数据', np.unique(b), value, **Label_Set)  # value的第一个数值是x
             .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Leg,
                              yaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),  # 'category'
                              xaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),
                              visualmap_opts=opts.VisualMapOpts(is_show=True, max_=int(max(y_data))+1, min_=int(min(y_data)),
                                                                pos_right='3%'))#显示
             )
        o_cList.append(c)
    return o_cList

def Decision_boundary(x_range,x_means,Predict_Func,class_,Type,nono=False):#绘制分类型预测图x-x热力图
    #r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调,class_是分类,add_o是可以合成的图
    # a-特征x，b-特征x-1，c-其他特征
    #规定，i-1是x轴，a是x轴，x_1是x轴
    class_dict = dict(zip(class_,[i for i in range(len(class_))]))
    if not nono:
        v_dict = [{'min':-1.5,'max':-0.5,'label':'未知'}]#分段显示
    else:v_dict = []
    for i in class_dict:
        v_dict.append({'min':class_dict[i]-0.5,'max':class_dict[i]+0.5,'label':str(i)})
    o_cList = []
    if len(x_means) == 1:
        n_ra = x_range[0]
        if Type[0] == 1:
            ra = make_list(n_ra[0], n_ra[1], 70)
        else:
            ra = n_ra

        a = np.array([i for i in ra]).reshape(-1,1)
        y_data = Predict_Func(a)[0].tolist()
        value = [[0,float(a[i]), class_dict.get(y_data[i], -1)] for i in range(len(a))]
        c = (HeatMap()
             .add_xaxis(['None'])
             .add_yaxis(f'数据', np.unique(a), value, **Label_Set)  # value的第一个数值是x
             .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Leg,
                              yaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),  # 'category'
                              xaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),
                              visualmap_opts=opts.VisualMapOpts(is_show=True, max_=max(class_dict.values()),
                                                                min_=-1,
                                                                is_piecewise=True, pieces=v_dict,
                                                                orient='horizontal', pos_bottom='3%'))
             )
        o_cList.append(c)
        return o_cList
    #如果x_means长度不等于1则执行下面
    for i in range(len(x_means)):
        if i == 0:
            continue

        n_ra = x_range[i-1]
        Type_ra = Type[i-1]
        n_rb = x_range[i]
        Type_rb = Type[i]
        if Type_ra == 1:
            ra = make_list(n_ra[0],n_ra[1],70)
        else:
            ra = n_ra

        if Type_rb == 1:
            rb = make_list(n_rb[0],n_rb[1],35)
        else:
            rb = n_rb
        a = np.array([i for i in ra for _ in rb]).T
        b = np.array([i for _ in ra for i in rb]).T
        data = np.array([x_means for _ in ra for i in rb])
        data[:, i - 1] = a
        data[:, i] = b
        y_data = Predict_Func(data)[0].tolist()
        value = [[float(a[i]), float(b[i]), class_dict.get(y_data[i],-1)] for i in range(len(a))]
        c = (HeatMap()
             .add_xaxis(np.unique(a))
             .add_yaxis(f'数据', np.unique(b), value, **Label_Set)#value的第一个数值是x
             .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Leg,
                              yaxis_opts=opts.AxisOpts(is_scale=True,type_='category'),#'category'
                              xaxis_opts=opts.AxisOpts(is_scale=True,type_='category'),
                              visualmap_opts=opts.VisualMapOpts(is_show=True,max_=max(class_dict.values()),min_=-1,
                              is_piecewise=True,pieces=v_dict,orient='horizontal',pos_bottom='3%'))
             )
        o_cList.append(c)
    return o_cList

def Decision_boundary_More(x_range,x_means,Predict_Func,class_,Type,nono=False):#绘制分类型预测图x-x热力图
    #r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调,class_是分类,add_o是可以合成的图
    # a-特征x，b-特征x-1，c-其他特征
    #规定，i-1是x轴，a是x轴，x_1是x轴
    class_dict = dict(zip(class_,[i for i in range(len(class_))]))
    if not nono:
        v_dict = [{'min':-1.5,'max':-0.5,'label':'未知'}]#分段显示
    else:v_dict = []
    for i in class_dict:
        v_dict.append({'min':class_dict[i]-0.5,'max':class_dict[i]+0.5,'label':str(i)})
    o_cList = []
    if len(x_means) == 1:
        return Decision_boundary(x_range,x_means,Predict_Func,class_,Type,nono)
    #如果x_means长度不等于1则执行下面
    for i in range(len(x_means)):
        for j in range(len(x_means)):
            if j <= i:continue

            n_ra = x_range[j]
            Type_ra = Type[j]
            n_rb = x_range[i]
            Type_rb = Type[i]
            if Type_ra == 1:
                ra = make_list(n_ra[0],n_ra[1],70)
            else:
                ra = n_ra

            if Type_rb == 1:
                rb = make_list(n_rb[0],n_rb[1],35)
            else:
                rb = n_rb
            a = np.array([i for i in ra for _ in rb]).T
            b = np.array([i for _ in ra for i in rb]).T
            data = np.array([x_means for _ in ra for i in rb])
            data[:, j] = a
            data[:, i] = b
            y_data = Predict_Func(data)[0].tolist()
            value = [[float(a[i]), float(b[i]), class_dict.get(y_data[i],-1)] for i in range(len(a))]
            c = (HeatMap()
                 .add_xaxis(np.unique(a))
                 .add_yaxis(f'数据', np.unique(b), value, **Label_Set)#value的第一个数值是x
                 .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Leg,
                                  yaxis_opts=opts.AxisOpts(is_scale=True,type_='category'),#'category'
                                  xaxis_opts=opts.AxisOpts(is_scale=True,type_='category'),
                                  visualmap_opts=opts.VisualMapOpts(is_show=True,max_=max(class_dict.values()),min_=-1,
                                  is_piecewise=True,pieces=v_dict,orient='horizontal',pos_bottom='3%'))
                 )
            o_cList.append(c)
    return o_cList

def SeeTree(Dic):
    node_re = re.compile('^([0-9]+) \[label="(.+)"\] ;$')  # 匹配节点正则表达式
    link_re = re.compile('^([0-9]+) -> ([0-9]+) (.*);$')  # 匹配节点正则表达式
    node_Dict = {}
    link_list = []

    with open(Dic, 'r') as f:  # 貌似必须分开w和r
        for i in f:
            try:
                get = re.findall(node_re, i)[0]
                if get[0] != '':
                    try:
                        v = float(get[0])
                    except:
                        v = 0
                    node_Dict[get[0]] = {'name': get[1].replace('\\n', '\n'), 'value': v, 'children': []}
                    continue
            except:
                pass
            try:
                get = re.findall(link_re, i)[0]
                if get[0] != '' and get[1] != '':
                    link_list.append((get[0], get[1]))
            except:
                pass

    father_list = []  # 已经有父亲的list
    for i in link_list:
        father = i[0]  # 父节点
        son = i[1]  # 子节点
        try:
            node_Dict[father]['children'].append(node_Dict[son])
            father_list.append(son)
            if int(son) == 0: print('F')
        except:
            pass

    father = list(set(node_Dict.keys()) - set(father_list))

    c = (
        Tree()
            .add("", [node_Dict[father[0]]], is_roam=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="决策树可视化"),
                             toolbox_opts=opts.ToolboxOpts(is_show=True))
    )
    return c

def make_Tab(heard,row):
    return Table().add(headers=heard, rows=row)

def scatter(w_heard,w):
    c = (
        Scatter()
            .add_xaxis(w_heard)
            .add_yaxis('', w, **Label_Set)
            .set_global_opts(title_opts=opts.TitleOpts(title='系数w散点图'), **global_Set)
    )
    return c

def bar(w_heard,w):
    c = (
        Bar()
            .add_xaxis(w_heard)
            .add_yaxis('', abs(w).tolist(), **Label_Set)
            .set_global_opts(title_opts=opts.TitleOpts(title='系数w柱状图'), **global_Set)
    )
    return c

# def line(w_sum,w,b):
#     x = np.arange(-5, 5, 1)
#     c = (
#         Line()
#             .add_xaxis(x.tolist())
#             .set_global_opts(title_opts=opts.TitleOpts(title=f"系数w曲线"), **global_Set)
#     )
#     for i in range(len(w)):
#         y = x * w[i] + b
#         c.add_yaxis(f"系数w[{i}]", y.tolist(), is_smooth=True, **Label_Set)
#     return c

def see_Line(x_trainData,y_trainData,w,w_sum,b):
    y = y_trainData.tolist()
    x_data = x_trainData.T
    re = []
    for i in range(len(x_data)):
        x = x_data[i]
        p = int(x.max() - x.min()) / 5
        x_num = np.arange(x.min(), x.min() + p * 6, p)  # 固定5个点，并且正好包括端点
        y_num = x_num * w[i] + (w[i] / w_sum) * b
        c = (
            Line()
                .add_xaxis(x_num.tolist())
                .add_yaxis(f"{i}预测曲线", y_num.tolist(), is_smooth=True, **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title=f"系数w曲线"), **global_Set)
        )
        t = (
            Scatter()
                .add_xaxis(x.tolist())
                .add_yaxis(f'{i}特征', y, **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title='类型划分图'), **global_Set)
        )
        t.overlap(c)
        re.append(t)
    return re

def get_Color():
    # 随机颜色，雷达图默认非随机颜色
    rgb = [randint(0, 255), randint(0, 255), randint(0, 255)]
    color = '#'
    for a in rgb:
        color += str(hex(a))[-2:].replace('x', '0').upper()  # 转换为16进制,upper表示小写(规范化)
    return color

def is_continuous(data:np.array,f:float=0.1):
    data = data.tolist()
    l = np.unique(data).tolist()
    try:
        re = len(l)/len(data)>=f or len(data) <= 3
        return re
    except:return False

def make_Cat(x_data):
    Cat = Categorical_Data()
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        Cat(x1)
    return Cat

def Training_visualization_More_NoCenter(x_trainData,class_,y):#根据不同类别绘制x-x分类散点图(可以绘制更多的图)
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
    Cat = make_Cat(x_data)
    o_cList = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i: continue
            x1 = x_data[i]  # x坐标
            x1_con = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_con = is_continuous(x2)

            o_c = None  # 旧的C
            for class_num in range(len(class_)):
                n_class = class_[class_num]
                x_1 = x1[y == n_class].tolist()
                x_2 = x2[y == n_class]
                x_2_new = np.unique(x_2)
                x_2 = x2[y == n_class].tolist()
                #x与散点图不同，这里是纵坐标
                c = (Scatter()
                     .add_xaxis(x_2)
                     .add_yaxis(f'{n_class}', x_1, **Label_Set)
                     .set_global_opts(title_opts=opts.TitleOpts(title=f'[{a}-{i}]训练数据散点图'), **global_Set,
                                      yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                      xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
                     )
                c.add_xaxis(x_2_new)

                if o_c == None:
                    o_c = c
                else:
                    o_c = o_c.overlap(c)
            o_cList.append(o_c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def Training_visualization_More(x_trainData,class_,y,center):#根据不同类别绘制x-x分类散点图(可以绘制更多的图)
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
    Cat = make_Cat(x_data)
    o_cList = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i: continue
            x1 = x_data[i]  # x坐标
            x1_con = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_con = is_continuous(x2)

            o_c = None  # 旧的C
            for class_num in range(len(class_)):
                n_class = class_[class_num]
                x_1 = x1[y == n_class].tolist()
                x_2 = x2[y == n_class]
                x_2_new = np.unique(x_2)
                x_2 = x2[y == n_class].tolist()
                #x与散点图不同，这里是纵坐标
                c = (Scatter()
                     .add_xaxis(x_2)
                     .add_yaxis(f'{n_class}', x_1, **Label_Set)
                     .set_global_opts(title_opts=opts.TitleOpts(title=f'[{a}-{i}]训练数据散点图'), **global_Set,
                                      yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                      xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
                     )
                c.add_xaxis(x_2_new)

                #添加簇中心
                try:
                    center_x_2 = [center[class_num][a]]
                except:
                    center_x_2 = [0]
                b = (Scatter()
                     .add_xaxis(center_x_2)
                     .add_yaxis(f'[{n_class}]中心',[center[class_num][i]], **Label_Set,symbol='triangle')
                     .set_global_opts(title_opts=opts.TitleOpts(title='簇中心'), **global_Set,
                                      yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                      xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
                     )
                c.overlap(b)

                if o_c == None:
                    o_c = c
                else:
                    o_c = o_c.overlap(c)
            o_cList.append(o_c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def Training_visualization_Center(x_trainData,class_,y,center):#根据不同类别绘制x-x分类散点图(可以绘制更多的图)
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
    Cat = make_Cat(x_data)
    o_cList = []
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        x1_con = is_continuous(x1)

        if i == 0:continue

        x2 = x_data[i - 1]  # y坐标
        x2_con = is_continuous(x2)

        o_c = None  # 旧的C
        for class_num in range(len(class_)):
            n_class = class_[class_num]
            x_1 = x1[y == n_class].tolist()
            x_2 = x2[y == n_class]
            x_2_new = np.unique(x_2)
            x_2 = x2[y == n_class].tolist()
            #x与散点图不同，这里是纵坐标
            c = (Scatter()
                 .add_xaxis(x_2)
                 .add_yaxis(f'{n_class}', x_1, **Label_Set)
                 .set_global_opts(title_opts=opts.TitleOpts(title=f'[{i-1}-{i}]训练数据散点图'), **global_Set,
                                  yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
                 )
            c.add_xaxis(x_2_new)

            #添加簇中心
            try:
                center_x_2 = [center[class_num][i-1]]
            except:
                center_x_2 = [0]
            b = (Scatter()
                 .add_xaxis(center_x_2)
                 .add_yaxis(f'[{n_class}]中心',[center[class_num][i]], **Label_Set,symbol='triangle')
                 .set_global_opts(title_opts=opts.TitleOpts(title='簇中心'), **global_Set,
                                  yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
                 )
            c.overlap(b)

            if o_c == None:
                o_c = c
            else:
                o_c = o_c.overlap(c)
        o_cList.append(o_c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def Training_visualization(x_trainData,class_,y):#根据不同类别绘制x-x分类散点图
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
    Cat = make_Cat(x_data)
    o_cList = []
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        x1_con = is_continuous(x1)

        if i == 0:continue

        x2 = x_data[i - 1]  # y坐标
        x2_con = is_continuous(x2)

        o_c = None  # 旧的C
        for n_class in class_:
            x_1 = x1[y == n_class].tolist()
            x_2 = x2[y == n_class]
            x_2_new = np.unique(x_2)
            x_2 = x2[y == n_class].tolist()
            #x与散点图不同，这里是纵坐标
            c = (Scatter()
                 .add_xaxis(x_2)
                 .add_yaxis(f'{n_class}', x_1, **Label_Set)
                 .set_global_opts(title_opts=opts.TitleOpts(title='训练数据散点图'), **global_Set,
                                  yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
                 )
            c.add_xaxis(x_2_new)
            if o_c == None:
                o_c = c
            else:
                o_c = o_c.overlap(c)
        o_cList.append(o_c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def Training_visualization_NoClass(x_trainData):#根据绘制x-x分类散点图(无类别)
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
    Cat = make_Cat(x_data)
    o_cList = []
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        x1_con = is_continuous(x1)

        if i == 0:continue

        x2 = x_data[i - 1]  # y坐标
        x2_con = is_continuous(x2)
        x2_new = np.unique(x2)
        #x与散点图不同，这里是纵坐标
        c = (Scatter()
             .add_xaxis(x2)
             .add_yaxis('', x1.tolist(), **Label_Set)
             .set_global_opts(title_opts=opts.TitleOpts(title='训练数据散点图'), **global_Leg,
                              yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                              xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
             )
        c.add_xaxis(x2_new)
        o_cList.append(c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def Training_W(x_trainData,class_,y,w_list,b_list,means:list):#针对分类问题绘制决策边界
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
    o_cList = []
    means.append(0)
    means = np.array(means)
    for i in range(len(x_data)):
        if i == 0:continue

        x1_con = is_continuous(x_data[i])
        x2 = x_data[i - 1]  # y坐标
        x2_con = is_continuous(x2)

        o_c = None  # 旧的C
        for class_num in range(len(class_)):
            n_class = class_[class_num]
            x2_new = np.unique(x2[y == n_class])
            #x与散点图不同，这里是纵坐标

            #加入这个判断是为了解决sklearn历史遗留问题
            if len(class_) == 2:#二分类问题
                if class_num == 0:continue
                w = w_list[0]
                b = b_list[0]
            else:#多分类问题
                w = w_list[class_num]
                b = b_list[class_num]

            if x2_con:
                x2_new = np.array(make_list(x2_new.min(), x2_new.max(), 5))

            w = np.append(w, 0)
            y_data = -(x2_new * w[i - 1]) / w[i] + b + (means[:i - 1] * w[:i - 1]).sum() + (means[i + 1:] * w[i + 1:]).sum()#假设除了两个特征意外，其余特征均为means列表的数值
            c = (
                Line()
                    .add_xaxis(x2_new)
                    .add_yaxis(f"决策边界:{n_class}=>[{i}]", y_data.tolist(), is_smooth=True, **Label_Set)
                    .set_global_opts(title_opts=opts.TitleOpts(title=f"系数w曲线"), **global_Set,
                              yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                              xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
            )
            if o_c == None:
                o_c = c
            else:
                o_c = o_c.overlap(c)
            #下面不要接任何代码，因为上面会continue
        o_cList.append(o_c)
    return o_cList

def Regress_W(x_trainData,y,w:np.array,b,means:list):#针对回归问题(y-x图)
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
    o_cList = []
    means.append(0)#确保mean[i+1]不会超出index
    means = np.array(means)
    w = np.append(w,0)
    for i in range(len(x_data)):
        x1 = x_data[i]
        x1_con = is_continuous(x1)
        if x1_con:
            x1 = np.array(make_list(x1.min(), x1.max(), 5))
        x1_new = np.unique(x1)
        y_data = x1_new * w[i] + b + (means[:i] * w[:i]).sum() + (means[i+1:] * w[i+1:]).sum()#假设除了两个特征意外，其余特征均为means列表的数值
        y_con = is_continuous(y_data)
        c = (
            Line()
                .add_xaxis(x1_new)
                .add_yaxis(f"拟合结果=>[{i}]", y_data.tolist(), is_smooth=True, **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title=f"系数w曲线"), **global_Set,
                          yaxis_opts=opts.AxisOpts(type_='value' if y_con else None,is_scale=True),
                          xaxis_opts=opts.AxisOpts(type_='value' if x1_con else None,is_scale=True))
        )
        o_cList.append(c)
    return o_cList

def regress_visualization(x_trainData,y):#y-x数据图
    x_data = x_trainData.T
    y_con = is_continuous(y)
    Cat = make_Cat(x_data)
    o_cList = []
    try:
        visualmap_opts = opts.VisualMapOpts(is_show=True, max_=int(y.max()) + 1, min_=int(y.min()),
                                            pos_right='3%')
    except:
        visualmap_opts = None
        y_con = False
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        x1_con = is_continuous(x1)
        #不转换成list因为保持dtype的精度，否则绘图会出现各种问题(数值重复)
        if not y_con and x1_con:#y不是连续的但x1连续,ry和ry_con是保护y的
            ry_con,x1_con = x1_con,y_con
            x1,ry = y,x1
        else:
            ry_con = y_con
            ry = y
        c = (
            Scatter()
            .add_xaxis(x1.tolist())#研究表明，这个是横轴
            .add_yaxis('数据',ry.tolist(),**Label_Set)
             .set_global_opts(title_opts=opts.TitleOpts(title="预测类型图"),**global_Set,
                              yaxis_opts=opts.AxisOpts(type_='value' if ry_con else 'category',is_scale=True),
                              xaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                              visualmap_opts=visualmap_opts
                              )
        )
        c.add_xaxis(np.unique(x1))
        o_cList.append(c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def Feature_visualization(x_trainData,data_name=''):#x-x数据图
    seeting = global_Set if data_name else global_Leg
    x_data = x_trainData.T
    only = False
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
        only = True
    o_cList = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i: continue#重复内容，跳过
            x1 = x_data[i]  # x坐标
            x1_con = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_con = is_continuous(x2)
            x2_new = np.unique(x2)
            if only:x2_con = False
            #x与散点图不同，这里是纵坐标
            c = (Scatter()
                 .add_xaxis(x2)
                 .add_yaxis(data_name, x1, **Label_Set)
                 .set_global_opts(title_opts=opts.TitleOpts(title=f'[{i}-{a}]数据散点图'), **seeting,
                                  yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True))
                 )
            c.add_xaxis(x2_new)
            o_cList.append(c)
    return o_cList

def Feature_visualization_Format(x_trainData,data_name=''):#x-x数据图
    seeting = global_Set if data_name else global_Leg
    x_data = x_trainData.T
    only = False
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
        only = True
    o_cList = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i: continue#重复内容，跳过（a读取的是i后面的）
            x1 = x_data[i]  # x坐标
            x1_con = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_con = is_continuous(x2)
            x2_new = np.unique(x2)
            x1_list = x1.astype(np.str).tolist()
            for i in range(len(x1_list)):
                x1_list[i] = [x1_list[i],f'特征{i}']
            if only:x2_con = False
            #x与散点图不同，这里是纵坐标
            c = (Scatter()
                 .add_xaxis(x2)
                 .add_yaxis(data_name, x1_list, **Label_Set)
                 .set_global_opts(title_opts=opts.TitleOpts(title=f'[{i}-{a}]数据散点图'), **seeting,
                                  yaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True),
                                  tooltip_opts=opts.TooltipOpts(is_show = True,axis_pointer_type = "cross",formatter="{c}"))
                 )
            c.add_xaxis(x2_new)
            o_cList.append(c)
    return o_cList

def Discrete_Feature_visualization(x_trainData,data_name=''):#必定离散x-x数据图
    seeting = global_Set if data_name else global_Leg
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data[0],np.zeros(len(x_data[0]))])
    o_cList = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i: continue#重复内容，跳过
            x1 = x_data[i]  # x坐标
            x2 = x_data[a]  # y坐标
            x2_new = np.unique(x2)

            #x与散点图不同，这里是纵坐标
            c = (Scatter()
                 .add_xaxis(x2)
                 .add_yaxis(data_name, x1, **Label_Set)
                 .set_global_opts(title_opts=opts.TitleOpts(title=f'[{i}-{a}]数据散点图'), **seeting,
                                  yaxis_opts=opts.AxisOpts(type_='category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='category',is_scale=True))
                 )
            c.add_xaxis(x2_new)
            o_cList.append(c)
    return o_cList

def Conversion_control(y_data,x_data,tab):#合并两x-x图
    if type(x_data) is np.ndarray and type(y_data) is np.ndarray:
        get_x = Feature_visualization(x_data,'原数据')#原来
        get_y = Feature_visualization(y_data,'转换数据')#转换
        for i in range(len(get_x)):
            tab.add(get_x[i].overlap(get_y[i]),f'[{i}]数据x-x散点图')
    return tab

def Conversion_Separate(y_data,x_data,tab):#并列显示两x-x图
    if type(x_data) is np.ndarray and type(y_data) is np.ndarray:
        get_x = Feature_visualization(x_data,'原数据')#原来
        get_y = Feature_visualization(y_data,'转换数据')#转换
        for i in range(len(get_x)):
            try:
                tab.add(get_x[i],f'[{i}]数据x-x散点图')
            except IndexError:pass
            try:
                tab.add(get_y[i],f'[{i}]变维数据x-x散点图')
            except IndexError:pass
    return tab

def Conversion_Separate_Format(y_data,tab):#并列显示两x-x图
    if type(y_data) is np.ndarray:
        get_y = Feature_visualization_Format(y_data,'转换数据')#转换
        for i in range(len(get_y)):
            tab.add(get_y[i],f'[{i}]变维数据x-x散点图')
    return tab

def Conversion_SeparateWH(w_data,h_data,tab):#并列显示两x-x图
    if type(w_data) is np.ndarray and type(w_data) is np.ndarray:
        get_x = Feature_visualization_Format(w_data,'W矩阵数据')#原来
        get_y = Feature_visualization(h_data.T,'H矩阵数据')#转换(先转T，再转T变回原样，W*H是横对列)
        print(h_data)
        print(w_data)
        print(h_data.T)
        for i in range(len(get_x)):
            try:
                tab.add(get_x[i],f'[{i}]W矩阵x-x散点图')
            except IndexError:pass
            try:
                tab.add(get_y[i],f'[{i}]H.T矩阵x-x散点图')
            except IndexError:pass
    return tab

def make_bar(name, value,tab):#绘制柱状图
    c = (
        Bar()
            .add_xaxis([f'[{i}]特征' for i in range(len(value))])
            .add_yaxis(name, value, **Label_Set)
            .set_global_opts(title_opts=opts.TitleOpts(title='系数w柱状图'), **global_Set)
    )
    tab.add(c, name)

def judging_Digits(num:(int,float)):#查看小数位数
    a = str(abs(num)).split('.')[0]
    if a == '':raise ValueError
    return len(a)

class Learner:
    def __init__(self,*args,**kwargs):
        self.numpy_Dic = {}#name:numpy
        self.Fucn_Add()#制作Func_Dic

    def Add_Form(self,data:np.array,name):
        name = f'{name}[{len(self.numpy_Dic)}]'
        self.numpy_Dic[name] = data

    def read_csv(self,Dic,name,encoding='utf-8',str_must=False,sep=','):
        type_ = np.str if str_must else np.float
        pf_data = read_csv(Dic,encoding=encoding,delimiter=sep,header=None)
        try:
            data = pf_data.to_numpy(dtype=type_)
        except ValueError:
            data = pf_data.to_numpy(dtype=np.str)
        if data.ndim == 1: data = np.expand_dims(data, axis=1)
        self.Add_Form(data,name)
        return data

    def Add_Python(self, Text, sheet_name):
        name = {}
        name.update(globals().copy())
        name.update(locals().copy())
        exec(Text, name)
        exec('get = Creat()', name)
        if isinstance(name['get'], np.array):  # 已经是DataFram
            get = name['get']
        else:
            try:
                get = np.array(name['get'])
            except:
                get = np.array([name['get']])
        self.Add_Form(get, sheet_name)
        return get

    def get_Form(self) -> dict:
        return self.numpy_Dic.copy()

    def get_Sheet(self,name) -> np.array:
        return self.numpy_Dic[name].copy()

    def to_CSV(self,Dic:str,name,sep) -> str:
        get = self.get_Sheet(name)
        np.savetxt(Dic, get, delimiter=sep)
        return Dic

    def to_Html_One(self,name,Dic=''):
        if Dic == '': Dic = f'{name}.html'
        get = self.get_Sheet(name)
        if get.ndim == 1: get = np.expand_dims(get, axis=1)
        get = get.tolist()
        for i in range(len(get)):
            get[i] = [i+1] + get[i]
        headers = [i for i in range(len(get[0]))]
        table = Table_Fisrt()
        table.add(headers, get).set_global_opts(
            title_opts=opts.ComponentTitleOpts(title=f"表格:{name}", subtitle="CoTan~机器学习:查看数据"))
        table.render(Dic)
        return Dic

    def to_Html(self, name, Dic='', type_=0):
        if Dic == '': Dic = f'{name}.html'
        # 把要画的sheet放到第一个
        Sheet_Dic = self.get_Form()
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

            tab = TAB(tab_First(page_title='CoTan:查看表格'))  # 一个Tab
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
            if get.ndim == 1: get = np.expand_dims(get, axis=1)
            get = get.tolist()
            for i in range(len(get)):
                get[i] = [i+1] + get[i]
            headers = [i for i in range(len(get[0]))]
            table = Table_Fisrt()
            table.add(headers, get).set_global_opts(
                title_opts=opts.ComponentTitleOpts(title=f"表格:{name}", subtitle="CoTan~机器学习:查看数据"))
            tab.add(table, f'表格:{name}')
        tab.render(Dic)
        return Dic

    def Merge(self,name,axis=0):#aiis:0-横向合并(hstack),1-纵向合并(vstack)，2-深度合并
        sheet_list = []
        for i in name:
            sheet_list.append(self.get_Sheet(i))
        get = {0:np.hstack,1:np.vstack,2:np.dstack}[axis](sheet_list)
        self.Add_Form(np.array(get),f'{name[0]}合成')

    def Split(self,name,split=2,axis=0):#aiis:0-横向分割(hsplit),1-纵向分割(vsplit)
        sheet = self.get_Sheet(name)
        get = {0:np.hsplit,1:np.vsplit,2:np.dsplit}[axis](sheet,split)
        for i in get:
            self.Add_Form(i,f'{name[0]}分割')

    def Two_Split(self,name,split,axis):#二分切割(0-横向，1-纵向)
        sheet = self.get_Sheet(name)
        try:
            split = float(eval(split))
            if split < 1:
                split = int(split * len(sheet) if axis == 1 else len(sheet[0]))
            else:
                raise Exception
        except:
            split = int(split)
        if axis == 0:
            self.Add_Form(sheet[:,split:], f'{name[0]}分割')
            self.Add_Form(sheet[:,:split], f'{name[0]}分割')

    def Deep(self,sheet:np.ndarray):
        return sheet.ravel()

    def Down_Ndim(self,sheet:np.ndarray):#横向
        down_list = []
        for i in sheet:
            down_list.append(i.ravel())
        return np.array(down_list)

    def LongitudinalDown_Ndim(self,sheet:np.ndarray):#纵向
        down_list = []
        for i in range(len(sheet[0])):
            down_list.append(sheet[:,i].ravel())
        return np.array(down_list).T

    def Reval(self,name,axis):#axis:0-横向，1-纵向(带.T)，2-深度
        sheet = self.get_Sheet(name)
        self.Add_Form({0:self.Down_Ndim,1:self.LongitudinalDown_Ndim,2:self.Deep}[axis](sheet).copy(),f'{name}伸展')

    def Del_Ndim(self,name):#删除无用维度
        sheet = self.get_Sheet(name)
        self.Add_Form(np.squeeze(sheet), f'{name}降维')

    def T(self,name,Func:list):
        sheet = self.get_Sheet(name)
        if sheet.ndim <= 2:
            self.Add_Form(sheet.T.copy(), f'{name}.T')
        else:
            self.Add_Form(np.transpose(sheet,Func).copy(), f'{name}.T')

    def reShape(self,name,shape:list):
        sheet = self.get_Sheet(name)
        self.Add_Form(sheet.reshape(shape).copy(), f'{name}.r')

    def Fucn_Add(self):
        self.Func_Dic = {
            'abs':lambda x,y:np.abs(x),
            'sqrt':lambda x,y:np.sqrt(x),
            'pow':lambda x,y:x**y,
            'loge':lambda x,y:np.log(x),
            'log10':lambda x,y:np.log10(x),
            'ceil':lambda x,y:np.ceil(x),
            'floor':lambda x,y:np.floor(x),
            'rint':lambda x,y:np.rint(x),
            'sin':lambda x,y:np.sin(x),
            'cos':lambda x,y:np.cos(x),
            'tan':lambda x,y:np.tan(x),
            'tanh':lambda x,y:np.tanh(x),
            'sinh':lambda x,y:np.sinh(x),
            'cosh':lambda x,y:np.cosh(x),
            'asin': lambda x, y: np.arcsin(x),
            'acos': lambda x, y: np.arccos(x),
            'atan': lambda x, y: np.arctan(x),
            'atanh': lambda x, y: np.arctanh(x),
            'asinh': lambda x, y: np.arcsinh(x),
            'acosh': lambda x, y: np.arccosh(x),
            'add': lambda x, y: x + y,#矩阵或元素
            'sub': lambda x, y: x - y,#矩阵或元素
            'mul': lambda x, y: np.multiply(x,y),#元素级别
            'matmul': lambda x, y: np.matmul(x,y),#矩阵
            'dot': lambda x, y: np.dot(x,y),#矩阵
            'div': lambda x, y: x / y,
            'div_floor': lambda x, y: np.floor_divide(x,y),
            'power': lambda x, y: np.power(x,y),#元素级
        }

    def Cul_Numpy(self,data,data_type,Func):
        if not 1 in data_type:raise Exception
        func = self.Func_Dic.get(Func,lambda x,y:x)
        args_data = []
        for i in range(len(data)):
            if data_type[i] == 0:
                args_data.append(data[i])
            else:
                args_data.append(self.get_Sheet(data[i]))
        get = func(*args_data)
        self.Add_Form(get,f'{Func}({data[0]},{data[1]})')
        return get

class Study_MachineBase:
    def __init__(self,*args,**kwargs):
        self.Model = None
        self.have_Fit = False
        self.have_Predict = False
        self.x_trainData = None
        self.y_trainData = None
        #有监督学习专有的testData
        self.x_testData = None
        self.y_testData = None
        #记录这两个是为了克隆

    def Fit(self,x_data,y_data,split=0.3,Increment=True,**kwargs):
        y_data = y_data.ravel()
        try:
            if self.x_trainData is None or not Increment:raise Exception
            self.x_trainData = np.vstack(x_data,self.x_trainData)
            self.y_trainData = np.vstack(y_data,self.y_trainData)
        except:
            self.x_trainData = x_data.copy()
            self.y_trainData = y_data.copy()
        x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=split)
        try:#增量式训练
            if not Increment:raise Exception
            self.Model.partial_fit(x_data,y_data)
        except:
            self.Model.fit(self.x_trainData, self.y_trainData)
        train_score = self.Model.score(x_train,y_train)
        test_score = self.Model.score(x_test,y_test)
        self.have_Fit = True
        return train_score,test_score

    def Score(self,x_data,y_data):
        Score = self.Model.score(x_data,y_data)
        return Score

    def Class_Score(self,Dic,x_data:np.ndarray,y_Really:np.ndarray):
        y_Really = y_Really.ravel()
        y_Predict = self.Predict(x_data)[0]

        Accuracy = self._Accuracy(y_Predict,y_Really)

        Recall,class_ = self._Macro(y_Predict,y_Really)
        Precision,class_ = self._Macro(y_Predict,y_Really,1)
        F1,class_ = self._Macro(y_Predict,y_Really,2)

        Confusion_matrix,class_ = self._Confusion_matrix(y_Predict,y_Really)
        kappa = self._Kappa_score(y_Predict,y_Really)

        tab = Tab()
        def gauge_base(name:str,value:float) -> Gauge:
            c = (
                Gauge()
                    .add("", [(name, round(value*100,2))],min_ = 0, max_ = 100)
                    .set_global_opts(title_opts=opts.TitleOpts(title=name))
            )
            return c
        tab.add(gauge_base('准确率',Accuracy),'准确率')
        tab.add(gauge_base('kappa',kappa),'kappa')

        def Bar_base(name,value) -> Bar:
            c = (
                Bar()
                    .add_xaxis(class_)
                    .add_yaxis(name, value, **Label_Set)
                    .set_global_opts(title_opts=opts.TitleOpts(title=name), **global_Set)
            )
            return c
        tab.add(Bar_base('精确率',Precision.tolist()),'精确率')
        tab.add(Bar_base('召回率',Recall.tolist()),'召回率')
        tab.add(Bar_base('F1',F1.tolist()),'F1')

        def heatmap_base(name,value,max_,min_,show) -> HeatMap:
            c = (
                HeatMap()
                    .add_xaxis(class_)
                    .add_yaxis(name, class_, value, label_opts=opts.LabelOpts(is_show=show,position='inside'))
                    .set_global_opts(title_opts=opts.TitleOpts(title=name), **global_Set,visualmap_opts=
                opts.VisualMapOpts(max_=max_,min_=min_,pos_right='3%'))
                )
            return c

        value = [[class_[i],class_[j],float(Confusion_matrix[i,j])] for i in range(len(class_)) for j in range(len(class_))]
        tab.add(heatmap_base('混淆矩阵',value,float(Confusion_matrix.max()),float(Confusion_matrix.min()),len(class_)<7), '混淆矩阵')

        desTo_CSV(Dic,'混淆矩阵',Confusion_matrix,class_,class_)
        desTo_CSV(Dic,'评分',[Precision,Recall,F1],class_,['精确率','召回率','F1'])
        save = Dic + r'/分类模型评估.HTML'
        tab.render(save)
        return save,

    def _Accuracy(self,y_Predict,y_Really):#准确率
        return accuracy_score(y_Really, y_Predict)

    def _Macro(self,y_Predict,y_Really,func=0):
        Func = [recall_score,precision_score,f1_score]#召回率，精确率和f1
        class_ = np.unique(y_Really).tolist()
        result = (Func[func](y_Really,y_Predict,class_,average=None))
        return result,class_

    def _Confusion_matrix(self,y_Predict,y_Really):#混淆矩阵
        class_ = np.unique(y_Really).tolist()
        return confusion_matrix(y_Really, y_Predict),class_

    def _Kappa_score(self,y_Predict,y_Really):
        return cohen_kappa_score(y_Really, y_Predict)

    def Regression_Score(self,Dic,x_data:np.ndarray,y_Really:np.ndarray):
        y_Really = y_Really.ravel()
        y_Predict = self.Predict(x_data)[0]
        tab = Tab()

        MSE = self._MSE(y_Predict,y_Really)
        MAE = self._MAE(y_Predict,y_Really)
        r2_Score = self._R2_Score(y_Predict,y_Really)
        RMSE = self._RMSE(y_Predict,y_Really)

        tab.add(make_Tab(['MSE','MAE','RMSE','r2_Score'],[[MSE,MAE,RMSE,r2_Score]]), '评估数据')

        save = Dic + r'/回归模型评估.HTML'
        tab.render(save)
        return save,

    def Clusters_Score(self,Dic,x_data:np.ndarray,*args):
        y_Predict = self.Predict(x_data)[0]
        tab = Tab()
        Coefficient,Coefficient_array = self._Coefficient_clustering(x_data,y_Predict)

        def gauge_base(name:str,value:float) -> Gauge:
            c = (
                Gauge()
                    .add("", [(name, round(value*100,2))],min_ = 0, max_ = 10**(judging_Digits(value*100)))
                    .set_global_opts(title_opts=opts.TitleOpts(title=name))
            )
            return c
        def Bar_base(name,value,xaxis) -> Bar:
            c = (
                Bar()
                    .add_xaxis(xaxis)
                    .add_yaxis(name, value, **Label_Set)
                    .set_global_opts(title_opts=opts.TitleOpts(title=name), **global_Set)
            )
            return c

        tab.add(gauge_base('平均轮廓系数', Coefficient),'平均轮廓系数')

        def Bar_(Coefficient_array,name='数据轮廓系数'):
            xaxis = [f'数据{i}' for i in range(len(Coefficient_array))]
            value = Coefficient_array.tolist()
            tab.add(Bar_base(name,value,xaxis),name)

        n = 20
        if len(Coefficient_array) <= n:
            Bar_(Coefficient_array)
        elif len(Coefficient_array) <= n**2:
            a = 0
            while a <= len(Coefficient_array):
                b = a + n
                if b >= len(Coefficient_array):b = len(Coefficient_array) + 1
                Cofe_array = Coefficient_array[a:b]
                Bar_(Cofe_array,f'{a}-{b}数据轮廓系数')
                a += n
        else:
            split = np.hsplit(Coefficient_array,n)
            a = 0
            for Cofe_array in split:
                Bar_(Cofe_array, f'{a}%-{a + n}%数据轮廓系数')
                a += n

        save = Dic + r'/聚类模型评估.HTML'
        tab.render(save)
        return save,

    def _MSE(self,y_Predict,y_Really):#均方误差
        return mean_squared_error(y_Really, y_Predict)

    def _MAE(self,y_Predict,y_Really):#中值绝对误差
        return median_absolute_error(y_Really, y_Predict)

    def _R2_Score(self,y_Predict,y_Really):#中值绝对误差
        return r2_score(y_Really, y_Predict)

    def _RMSE(self,y_Predict,y_Really):#中值绝对误差
        return self._MSE(y_Predict,y_Really) ** 0.5

    def _Coefficient_clustering(self,x_data,y_Predict):
        means_score = silhouette_score(x_data,y_Predict)
        outline_score = silhouette_samples(x_data,y_Predict)
        return means_score, outline_score

    def Predict(self,x_data,*args,**kwargs):
        self.x_testData = x_data.copy()
        y_Predict = self.Model.predict(x_data)
        self.y_testData = y_Predict.copy()
        self.have_Predict = True
        return y_Predict,'预测'

    def Des(self,Dic,*args,**kwargs):
        return (Dic,)

class prep_Base(Study_MachineBase):#不允许第二次训练
    def __init__(self,*args,**kwargs):
        super(prep_Base, self).__init__(*args,**kwargs)
        self.Model = None

    def Fit(self, x_data,y_data,Increment=True, *args, **kwargs):
        if not self.have_Predict:  # 不允许第二次训练
            y_data = y_data.ravel()
            try:
                if self.x_trainData is None or not Increment: raise Exception
                self.x_trainData = np.vstack(x_data, self.x_trainData)
                self.y_trainData = np.vstack(y_data, self.y_trainData)
            except:
                self.x_trainData = x_data.copy()
                self.y_trainData = y_data.copy()
            try:  # 增量式训练
                if not Increment: raise Exception
                self.Model.partial_fit(x_data, y_data)
            except:
                self.Model.fit(self.x_trainData, self.y_trainData)
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'特征工程'

    def Score(self, x_data, y_data):
        return 'None' # 没有score

class Unsupervised(prep_Base):#无监督，不允许第二次训练
    def Fit(self, x_data,Increment=True, *args, **kwargs):
        if not self.have_Predict:  # 不允许第二次训练
            self.y_trainData = None
            try:
                if self.x_trainData is None or not Increment: raise Exception
                self.x_trainData = np.vstack(x_data, self.x_trainData)
            except:
                self.x_trainData = x_data.copy()
            try:  # 增量式训练
                if not Increment: raise Exception
                self.Model.partial_fit(x_data)
            except:
                self.Model.fit(self.x_trainData, self.y_trainData)
        self.have_Fit = True
        return 'None', 'None'

class UnsupervisedModel(prep_Base):#无监督
    def Fit(self, x_data, Increment=True,*args, **kwargs):
        self.y_trainData = None
        try:
            if self.x_trainData is None or not Increment: raise Exception
            self.x_trainData = np.vstack(x_data, self.x_trainData)
        except:
            self.x_trainData = x_data.copy()
        try:  # 增量式训练
            if not Increment: raise Exception
            self.Model.partial_fit(x_data)
        except:
            self.Model.fit(self.x_trainData, self.y_trainData)
        self.have_Fit = True
        return 'None', 'None'

class To_PyeBase(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):
        super(To_PyeBase, self).__init__(*args,**kwargs)
        self.Model = None

        #记录这两个是为了克隆
        self.k = {}
        self.Model_Name = model

    def Fit(self, x_data,y_data, *args, **kwargs):
        self.x_trainData = x_data.copy()
        self.y_trainData = y_data.ravel().copy()
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        self.have_Predict = True
        return np.array([]),'请使用训练'

    def Score(self, x_data, y_data):
        return 'None' # 没有score

def num_str(num,f):
    num = str(round(float(num),f))
    if len(num.replace('.','')) == f:
        return num
    n = num.split('.')
    if len(n) == 0:#无小数
        return num + '.' + '0' * (f - len(num))
    else:
        return num + '0' * (f - len(num) + 1)#len(num)多算了一位小数点

def desTo_CSV(Dic,name,data,columns=None,row=None):
    Dic = Dic + '/' + name + '.csv'
    DataFrame(data,columns=columns,index=row).to_csv(Dic,header=False if columns is None else True,
                                                     index=False if row is None else True)
    return data

class Des(To_PyeBase):#数据分析
    def Des(self, Dic, *args, **kwargs):
        tab = Tab()

        data = self.x_trainData
        def Cumulative_calculation(data,func,name,tab):
            sum_list = []
            for i in range(len(data)):#按行迭代数据
                sum_list.append([])
                for a in range(len(data[i])):
                    s = num_str(func(data[:i+1,a]),8)
                    sum_list[-1].append(s)
            desTo_CSV(Dic,f'{name}',sum_list)
            tab.add(make_Tab([f'[{i}]' for i in range(len(sum_list[0]))],sum_list),f'{name}')

        Geometric_mean = lambda x:np.power(np.prod(x),1/len(x))#几何平均数
        Square_mean = lambda x:np.sqrt(np.sum(np.power(x,2)) / len(x))#平方平均数
        Harmonic_mean = lambda x:len(x)/np.sum(np.power(x,-1))#调和平均数

        Cumulative_calculation(data,np.sum,'累计求和',tab)
        Cumulative_calculation(data,np.var,'累计方差',tab)
        Cumulative_calculation(data,np.std,'累计标准差',tab)
        Cumulative_calculation(data,np.mean,'累计算术平均值',tab)
        Cumulative_calculation(data,Geometric_mean,'累计几何平均值',tab)
        Cumulative_calculation(data,Square_mean,'累计平方平均值',tab)
        Cumulative_calculation(data,Harmonic_mean,'累计调和平均值',tab)
        Cumulative_calculation(data,np.median,'累计中位数',tab)
        Cumulative_calculation(data,np.max,'累计最大值',tab)
        Cumulative_calculation(data,np.min,'累计最小值',tab)

        save = Dic + r'/数据分析.HTML'
        tab.render(save)  # 生成HTML
        return save,

class CORR(To_PyeBase):#相关性和协方差
    def Des(self, Dic, *args, **kwargs):
        tab = Tab()

        data = DataFrame(self.x_trainData)
        corr = data.corr().to_numpy()#相关性
        cov = data.cov().to_numpy()#协方差

        def HeatMAP(data,name:str,max_,min_):
            x = [f'特征[{i}]' for i in range(len(data))]
            y = [f'特征[{i}]' for i in range(len(data[0]))]
            value = [(f'特征[{i}]', f'特征[{j}]', float(data[i][j])) for i in range(len(data)) for j in range(len(data[i]))]
            c = (HeatMap()
                 .add_xaxis(x)
                 .add_yaxis(f'数据', y, value, label_opts=opts.LabelOpts(is_show= True if len(x) <= 10 else False,position='inside'))#如果特征太多则不显示标签
                 .set_global_opts(title_opts=opts.TitleOpts(title='矩阵热力图'), **global_Leg,
                                  yaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),  # 'category'
                                  xaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),
                                  visualmap_opts=opts.VisualMapOpts(is_show=True, max_=max_,min_=min_,pos_right='3%'))#显示
                 )
            tab.add(c,name)

        HeatMAP(corr,'相关性热力图',1,-1)
        HeatMAP(cov,'协方差热力图',float(cov.max()),float(cov.min()))

        desTo_CSV(Dic, f'相关性矩阵', corr)
        desTo_CSV(Dic, f'协方差矩阵', cov)
        save = Dic + r'/数据相关性.HTML'
        tab.render(save)  # 生成HTML
        return save,

class View_data(To_PyeBase):#绘制预测型热力图
    def __init__(self, args_use, Learner, *args, **kwargs):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(View_data, self).__init__(args_use,Learner,*args, **kwargs)

        self.Model = Learner.Model
        self.Select_Model = None
        self.have_Fit = Learner.have_Fit
        self.Model_Name = 'Select_Model'
        self.Learner = Learner
        self.Learner_name = Learner.Model_Name

    def Fit(self,*args,**kwargs):
        self.have_Fit = True
        return 'None','None'

    def Predict(self,x_data,Add_Func=None,*args, **kwargs):
        x_trainData = self.Learner.x_trainData
        y_trainData = self.Learner.y_trainData
        x_name = self.Learner_name
        if not x_trainData is None:
            Add_Func(x_trainData, f'{x_name}:x训练数据')

        try:
            x_testData = self.x_testData
            if not x_testData is None:
                Add_Func(x_testData, f'{x_name}:x测试数据')
        except:pass

        try:
            y_testData = self.y_testData.copy()
            if not y_testData is None:
                Add_Func(y_testData, f'{x_name}:y测试数据')
        except:pass

        self.have_Fit = True
        if y_trainData is None:
            return np.array([]), 'y训练数据'
        return y_trainData,'y训练数据'

    def Des(self,Dic,*args,**kwargs):
        return Dic,

class MatrixScatter(To_PyeBase):#矩阵散点图
    def Des(self, Dic, *args, **kwargs):
        tab = Tab()

        data = self.x_trainData
        if data.ndim <= 2:#维度为2
            c = (Scatter()
                 .add_xaxis([f'{i}' for i in range(data.shape[1])])
                 .set_global_opts(title_opts=opts.TitleOpts(title=f'矩阵散点图'), **global_Leg)
                 )
            if data.ndim == 2:
                for num in range(len(data)):
                    i = data[num]
                    c.add_yaxis(f'{num}',[[f'{num}',x] for x in i],color='#FFFFFF')
            else:
                c.add_yaxis(f'0', [[0,x]for x in data],color='#FFFFFF')
            c.set_series_opts(label_opts=opts.LabelOpts(is_show=True,color='#000000',position='inside',
            formatter=JsCode("function(params){return params.data[2];}"),
            ))
        elif data.ndim == 3:
            c = (Scatter3D()
                 .set_global_opts(title_opts=opts.TitleOpts(title=f'矩阵散点图'),**global_Leg)
                 )
            for num in range(len(data)):
                i = data[num]
                for s_num in range(len(i)):
                    s = i[s_num]
                    y_data = [[num,s_num,x,float(s[x])] for x in range(len(s))]
                    c.add(f'{num}',y_data,zaxis3d_opts = opts.Axis3DOpts(type_="category"))
            c.set_series_opts(label_opts=opts.LabelOpts(is_show=True,color='#000000',position='inside',
                        formatter=JsCode("function(params){return params.data[3];}")))
        else:
            c = Scatter()
        tab.add(c,'矩阵散点图')

        save = Dic + r'/矩阵散点图.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Cluster_Tree(To_PyeBase):#聚类树状图
    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        x_data = self.x_trainData
        linkage_array = ward(x_data)#self.y_trainData是结果
        dendrogram(linkage_array)
        plt.savefig(Dic + r'/Cluster_graph.png')

        image = Image()
        image.add(src=Dic + r'/Cluster_graph.png',).set_global_opts(title_opts=opts.ComponentTitleOpts(title="聚类树状图"))
        tab.add(image,'聚类树状图')

        save = Dic + r'/聚类树状图.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Class_To_Bar(To_PyeBase):#类型柱状图
    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        x_data = self.x_trainData.T
        y_data = self.y_trainData
        class_ = np.unique(y_data).tolist()#类型
        class_list = []
        for n_class in class_:  # 生成class_list(class是1,，也就是二维的，下面会压缩成一维)
            class_list.append(y_data == n_class)
        for num_i in range(len(x_data)):#迭代每一个特征
            i = x_data[num_i]
            i_con = is_continuous(i)
            if i_con and len(i) >= 11:
                c_list = [[0] * 10 for _ in class_list]  # 存放绘图数据，每一层列表是一个类(leg)，第二层是每个x_data
                start = i.min()
                end = i.max()
                n = (end - start) / 10#生成10条柱子
                x_axis = []#x轴
                num_startEND = 0#迭代到第n个
                while num_startEND <= 9:#把每个特征分为10类进行迭代
                    x_axis.append(f'({num_startEND})[{round(start, 2)}-{round((start + n) if (start + n) <= end or not num_startEND == 9 else end, 2)}]')#x_axis添加数据
                    try:
                        if num_startEND == 9:raise Exception#执行到第10次时，直接获取剩下的所有
                        s = (start <= i) == (i < end)#布尔索引
                    except:#因为start + n有超出end的风险
                        s = (start <= i) == (i <= end)#布尔索引
                    # n_data = i[s]  # 取得现在的特征数据

                    for num in range(len(class_list)):#根据类别进行迭代
                        now_class = class_list[num]#取得布尔数组：y_data == n_class也就是输出值为指定类型的bool矩阵，用于切片
                        bool_class = now_class[s].ravel()#切片成和n_data一样的位置一样的形状(now_class就是一个bool矩阵)
                        c_list[num][num_startEND] = (int(np.sum(bool_class))) #用len计数 c_list = [[class1的数据],[class2的数据],[]]
                    num_startEND += 1
                    start += n
            else :
                iter_np = np.unique(i)
                c_list = [[0] * len(iter_np) for _ in class_list]  # 存放绘图数据，每一层列表是一个类(leg)，第二层是每个x_data
                x_axis = []  # 添加x轴数据
                for i_num in range(len(iter_np)):#迭代每一个i(不重复)
                    i_data = iter_np[i_num]
                    # n_data= i[i == i_data]#取得现在特征数据
                    x_axis.append(f'[{i_data}]')
                    for num in range(len(class_list)):# 根据类别进行迭代
                        now_class = class_list[num]#取得class_list的布尔数组
                        bool_class = now_class[i == i_data]#切片成和n_data一样的位置一样的形状(now_class就是一个bool矩阵)
                        c_list[num][i_num] = (int(np.sum(bool_class).tolist())) #用len计数 c_list = [[class1的数据],[class2的数据],[]]
            c = (
                Bar()
                    .add_xaxis(x_axis)
                    .set_global_opts(title_opts=opts.TitleOpts(title='类型-特征统计柱状图'), **global_Set,xaxis_opts=opts.AxisOpts(type_='category'),
                                     yaxis_opts=opts.AxisOpts(type_='value')))
            y_axis = []
            for i in range(len(c_list)):
                y_axis.append(f'{class_[i]}')
                c.add_yaxis(f'{class_[i]}', c_list[i], **Label_Set)
            desTo_CSV(Dic, f'类型-[{num_i}]特征统计柱状图', c_list, x_axis, y_axis)
            tab.add(c, f'类型-[{num_i}]特征统计柱状图')

        #未完成
        save = Dic + r'/特征统计.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Numpy_To_HeatMap(To_PyeBase):#Numpy矩阵绘制热力图
    def Des(self,Dic,*args,**kwargs):
        tab = Tab()

        data = self.x_trainData
        x = [f'横[{i}]' for i in range(len(data))]
        y = [f'纵[{i}]' for i in range(len(data[0]))]
        value = [(f'横[{i}]', f'纵[{j}]', float(data[i][j])) for i in range(len(data)) for j in range(len(data[i]))]
        c = (HeatMap()
             .add_xaxis(x)
             .add_yaxis(f'数据', y, value, **Label_Set)  # value的第一个数值是x
             .set_global_opts(title_opts=opts.TitleOpts(title='矩阵热力图'), **global_Leg,
                              yaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),  # 'category'
                              xaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),
                              visualmap_opts=opts.VisualMapOpts(is_show=True, max_=float(data.max()),
                                                                min_=float(data.min()),
                                                                pos_right='3%'))#显示
             )
        tab.add(c,'矩阵热力图')
        tab.add(make_Tab(x,data.T.tolist()),f'矩阵热力图:表格')

        save = Dic + r'/矩阵热力图.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Predictive_HeatMap_Base(To_PyeBase):#绘制预测型热力图
    def __init__(self, args_use, Learner, *args, **kwargs):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(Predictive_HeatMap_Base, self).__init__(args_use,Learner,*args, **kwargs)

        self.Model = Learner.Model
        self.Select_Model = None
        self.have_Fit = Learner.have_Fit
        self.Model_Name = 'Select_Model'
        self.Learner = Learner
        self.x_trainData = Learner.x_trainData.copy()
        self.y_trainData = Learner.y_trainData.copy()
        self.means = []

    def Fit(self,x_data,*args,**kwargs):
        try:
            self.means = x_data.ravel()
        except:
            pass
        self.have_Fit = True
        return 'None','None'

    def Des(self,Dic,Decision_boundary,Prediction_boundary,*args,**kwargs):
        tab = Tab()
        y = self.y_trainData
        x_data = self.x_trainData
        try:#如果没有class
            class_ = self.Model.classes_.tolist()
            class_heard = [f'类别[{i}]' for i in range(len(class_))]

            #获取数据
            get,x_means,x_range,Type = Training_visualization(x_data,class_,y)
            #可使用自带的means，并且nan表示跳过
            for i in range(min([len(x_means),len(self.means)])):
                try:
                    g = self.means[i]
                    if g == np.nan:raise Exception
                    x_means[i] = g
                except:pass
            get = Decision_boundary(x_range,x_means,self.Learner.Predict,class_,Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            heard = class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))]
            data = class_ + [f'{i}' for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, '数据表')
        except:
            get, x_means, x_range,Type = regress_visualization(x_data, y)

            get = Prediction_boundary(x_range, x_means, self.Learner.Predict, Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            heard = [f'普适预测第{i}特征' for i in range(len(x_means))]
            data = [f'{i}' for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, '数据表')

        save = Dic + r'/预测热力图.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Predictive_HeatMap(Predictive_HeatMap_Base):#绘制预测型热力图
    def Des(self,Dic,*args,**kwargs):
        return super().Des(Dic,Decision_boundary,Prediction_boundary)

class Predictive_HeatMap_More(Predictive_HeatMap_Base):#绘制预测型热力图_More
    def Des(self,Dic,*args,**kwargs):
        return super().Des(Dic,Decision_boundary_More,Prediction_boundary_More)

class Near_feature_scatter_class_More(To_PyeBase):
    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        x_data = self.x_trainData
        y = self.y_trainData
        class_ = np.unique(y).ravel().tolist()
        class_heard = [f'簇[{i}]' for i in range(len(class_))]

        get, x_means, x_range, Type = Training_visualization_More_NoCenter(x_data, class_, y)
        for i in range(len(get)):
            tab.add(get[i], f'{i}训练数据散点图')

        heard = class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))]
        data = class_ + [f'{i}' for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, '数据表')

        save = Dic + r'/数据特征散点图(分类).HTML'
        tab.render(save)  # 生成HTML
        return save,

class Near_feature_scatter_More(To_PyeBase):
    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        x_data = self.x_trainData
        x_means = make_Cat(x_data).get()[0]
        get_y = Feature_visualization(x_data, '数据散点图')  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f'[{i}]数据x-x散点图')

        heard = [f'普适预测第{i}特征' for i in range(len(x_means))]
        data = [f'{i}' for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, '数据表')

        save = Dic + r'/数据特征散点图.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Near_feature_scatter_class(To_PyeBase):#临近特征散点图：分类数据
    def Des(self,Dic,*args,**kwargs):
        #获取数据
        class_ = np.unique(self.y_trainData).ravel().tolist()
        class_heard = [f'类别[{i}]' for i in range(len(class_))]
        tab = Tab()

        y = self.y_trainData
        x_data = self.x_trainData
        get, x_means, x_range, Type = Training_visualization(x_data, class_, y)
        for i in range(len(get)):
            tab.add(get[i], f'{i}临近特征散点图')

        heard = class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))]
        data = class_ + [f'{i}' for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, '数据表')

        save = Dic + r'/临近数据特征散点图(分类).HTML'
        tab.render(save)  # 生成HTML
        return save,

class Near_feature_scatter(To_PyeBase):#临近特征散点图：连续数据
    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        x_data = self.x_trainData.T
        y = self.y_trainData

        get, x_means, x_range,Type = Training_visualization_NoClass(x_data)
        for i in range(len(get)):
            tab.add(get[i], f'{i}临近特征散点图')

        columns = [f'普适预测第{i}特征' for i in range(len(x_means))]
        data = [f'{i}' for i in x_means]
        tab.add(make_Tab(columns,[data]), '数据表')

        save = Dic + r'/临近数据特征散点图.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Feature_scatter_YX(To_PyeBase):#y-x图
    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        x_data = self.x_trainData
        y = self.y_trainData

        get, x_means, x_range,Type = regress_visualization(x_data,y)
        for i in range(len(get)):
            tab.add(get[i], f'{i}特征x-y散点图')

        columns = [f'普适预测第{i}特征' for i in range(len(x_means))]
        data = [f'{i}' for i in x_means]
        tab.add(make_Tab(columns,[data]), '数据表')

        save = Dic + r'/特征y-x图像.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Line_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(Line_Model, self).__init__(*args,**kwargs)
        Model = {'Line':LinearRegression,'Ridge':Ridge,'Lasso':Lasso}[
            model]
        if model == 'Line':
            self.Model = Model()
            self.k = {}
        else:
            self.Model = Model(alpha=args_use['alpha'],max_iter=args_use['max_iter'])
            self.k = {'alpha':args_use['alpha'],'max_iter':args_use['max_iter']}
        #记录这两个是为了克隆
        self.Alpha = args_use['alpha']
        self.max_iter = args_use['max_iter']
        self.Model_Name = model

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        x_data = self.x_trainData
        y = self.y_trainData
        w_list = self.Model.coef_.tolist()
        w_heard = [f'系数w[{i}]' for i in range(len(w_list))]
        b = self.Model.intercept_.tolist()

        get, x_means, x_range,Type = regress_visualization(x_data, y)
        get_Line = Regress_W(x_data, y, w_list, b, x_means.copy())
        for i in range(len(get)):
            tab.add(get[i].overlap(get_Line[i]), f'{i}预测类型图')

        get = Prediction_boundary(x_range, x_means, self.Predict, Type)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测热力图')

        tab.add(scatter(w_heard,w_list),'系数w散点图')
        tab.add(bar(w_heard,self.Model.coef_),'系数柱状图')

        columns = [f'普适预测第{i}特征' for i in range(len(x_means))] + w_heard + ['截距b']
        data = [f'{i}' for i in x_means] + w_list + [b]
        if self.Model_Name != 'Line':
            columns += ['阿尔法','最大迭代次数']
            data += [self.Model.alpha,self.Model.max_iter]
        tab.add(make_Tab(columns,[data]), '数据表')

        desTo_CSV(Dic, '系数表', [w_list] + [b], [f'系数W[{i}]' for i in range(len(w_list))] + ['截距'])
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])

        save = Dic + r'/线性回归模型.HTML'
        tab.render(save)  # 生成HTML
        return save,

class LogisticRegression_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(LogisticRegression_Model, self).__init__(*args,**kwargs)
        self.Model = LogisticRegression(C=args_use['C'],max_iter=args_use['max_iter'])
        #记录这两个是为了克隆
        self.C = args_use['C']
        self.max_iter = args_use['max_iter']
        self.k = {'C':args_use['C'],'max_iter':args_use['max_iter']}
        self.Model_Name = model

    def Des(self,Dic='render.html',*args,**kwargs):
        #获取数据
        w_array = self.Model.coef_
        w_list = w_array.tolist()  # 变为表格
        b = self.Model.intercept_
        c = self.Model.C
        max_iter = self.Model.max_iter
        class_ = self.Model.classes_.tolist()
        class_heard = [f'类别[{i}]' for i in range(len(class_))]
        tab = Tab()

        y = self.y_trainData
        x_data = self.x_trainData
        get, x_means, x_range, Type = Training_visualization(x_data, class_, y)
        get_Line = Training_W(x_data, class_, y, w_list, b, x_means.copy())
        for i in range(len(get)):
            tab.add(get[i].overlap(get_Line[i]), f'{i}决策边界散点图')

        for i in range(len(w_list)):
            w = w_list[i]
            w_heard = [f'系数w[{i},{j}]' for j in range(len(w))]
            tab.add(scatter(w_heard, w), f'系数w[{i}]散点图')
            tab.add(bar(w_heard, w_array[i]), f'系数w[{i}]柱状图')

        columns = class_heard + [f'截距{i}' for i in range(len(b))] + ['C', '最大迭代数']
        data = class_ + b.tolist() + [c, max_iter]
        c = Table().add(headers=columns, rows=[data])
        tab.add(c, '数据表')
        c = Table().add(headers=[f'系数W[{i}]' for i in range(len(w_list[0]))], rows=w_list)
        tab.add(c, '系数数据表')

        c = Table().add(headers=[f'普适预测第{i}特征' for i in range(len(x_means))], rows=[[f'{i}' for i in x_means]])
        tab.add(c, '普适预测数据表')

        desTo_CSV(Dic, '系数表', w_list, [f'系数W[{i}]' for i in range(len(w_list[0]))])
        desTo_CSV(Dic, '截距表', [b], [f'截距{i}' for i in range(len(b))])
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])

        save = Dic + r'/逻辑回归.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Categorical_Data:#数据统计助手
    def __init__(self):
        self.x_means = []
        self.x_range = []
        self.Type = []

    def __call__(self,x1, *args, **kwargs):
        get = self.is_continuous(x1)
        return get

    def is_continuous(self,x1:np.array):
        try:
            x1_con = is_continuous(x1)
            if x1_con:
                self.x_means.append(np.mean(x1))
                self.add_Range(x1)
            else:
                raise Exception
            return x1_con
        except:#找出出现次数最多的元素
            new = np.unique(x1)#去除相同的元素
            count_list = []
            for i in new:
                count_list.append(np.sum(x1 == i))
            index = count_list.index(max(count_list))#找出最大值的索引
            self.x_means.append(x1[index])
            self.add_Range(x1,False)
            return False

    def add_Range(self,x1:np.array,range_=True):
        try:
            if not range_ : raise Exception
            min_ = int(x1.min()) - 1
            max_ = int(x1.max()) + 1
            #不需要复制列表
            self.x_range.append([min_,max_])
            self.Type.append(1)
        except:
            self.x_range.append(list(set(x1.tolist())))#去除多余元素
            self.Type.append(2)

    def get(self):
        return self.x_means,self.x_range,self.Type

class Knn_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(Knn_Model, self).__init__(*args,**kwargs)
        Model = {'Knn_class':KNeighborsClassifier,'Knn':KNeighborsRegressor}[model]
        self.Model = Model(p=args_use['p'],n_neighbors=args_use['n_neighbors'])
        #记录这两个是为了克隆
        self.n_neighbors = args_use['n_neighbors']
        self.p = args_use['p']
        self.k = {'n_neighbors':args_use['n_neighbors'],'p':args_use['p']}
        self.Model_Name = model

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y = self.y_trainData
        x_data = self.x_trainData
        y_test = self.y_testData
        x_test = self.x_testData
        if self.Model_Name == 'Knn_class':
            class_ = self.Model.classes_.tolist()
            class_heard = [f'类别[{i}]' for i in range(len(class_))]

            get,x_means,x_range,Type = Training_visualization(x_data,class_,y)
            for i in range(len(get)):
                tab.add(get[i],f'{i}训练数据散点图')

            if not y_test is None:
                get = Training_visualization(x_test,class_,y_test)[0]
                for i in range(len(get)):
                    tab.add(get[i],f'{i}测试数据散点图')

            get = Decision_boundary(x_range,x_means,self.Predict,class_,Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            heard = class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))]
            data = class_ + [f'{i}' for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, '数据表')
        else:
            get, x_means, x_range,Type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f'{i}训练数据散点图')

            get = regress_visualization(x_test, y_test)[0]
            for i in range(len(get)):
                tab.add(get[i], f'{i}测试数据类型图')

            get = Prediction_boundary(x_range, x_means, self.Predict, Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            heard = [f'普适预测第{i}特征' for i in range(len(x_means))]
            data = [f'{i}' for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, '数据表')
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])
        save = Dic + r'/K.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Tree_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(Tree_Model, self).__init__(*args,**kwargs)
        Model = {'Tree_class':DecisionTreeClassifier,'Tree':DecisionTreeRegressor}[model]
        self.Model = Model(criterion=args_use['criterion'],splitter=args_use['splitter'],max_features=args_use['max_features']
                           ,max_depth=args_use['max_depth'],min_samples_split=args_use['min_samples_split'])
        #记录这两个是为了克隆
        self.criterion = args_use['criterion']
        self.splitter = args_use['splitter']
        self.max_features = args_use['max_features']
        self.max_depth = args_use['max_depth']
        self.min_samples_split = args_use['min_samples_split']
        self.k = {'criterion':args_use['criterion'],'splitter':args_use['splitter'],'max_features':args_use['max_features'],
                  'max_depth':args_use['max_depth'],'min_samples_split':args_use['min_samples_split']}
        self.Model_Name = model

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        importance = self.Model.feature_importances_.tolist()

        with open(Dic + r"\Tree_Gra.dot", 'w') as f:
            export_graphviz(self.Model, out_file=f)

        make_bar('特征重要性',importance,tab)
        desTo_CSV(Dic, '特征重要性', [importance], [f'[{i}]特征' for i in range(len(importance))])
        tab.add(SeeTree(Dic + r"\Tree_Gra.dot"),'决策树可视化')

        y = self.y_trainData
        x_data = self.x_trainData
        y_test = self.y_testData
        x_test = self.x_testData
        if self.Model_Name == 'Tree_class':
            class_ = self.Model.classes_.tolist()
            class_heard = [f'类别[{i}]' for i in range(len(class_))]

            get,x_means,x_range,Type = Training_visualization(x_data,class_,y)
            for i in range(len(get)):
                tab.add(get[i],f'{i}训练数据散点图')

            get = Training_visualization(x_test, class_, y_test)[0]
            for i in range(len(get)):
                tab.add(get[i], f'{i}测试数据散点图')

            get = Decision_boundary(x_range,x_means,self.Predict,class_,Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            tab.add(make_Tab(class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))] + [f'特征{i}重要性' for i in range(len(importance))],
                             [class_ + [f'{i}' for i in x_means] + importance]), '数据表')
        else:
            get, x_means, x_range,Type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f'{i}训练数据散点图')

            get = regress_visualization(x_test, y_test)[0]
            for i in range(len(get)):
                tab.add(get[i], f'{i}测试数据类型图')

            get = Prediction_boundary(x_range, x_means, self.Predict, Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            tab.add(make_Tab([f'普适预测第{i}特征' for i in range(len(x_means))] + [f'特征{i}重要性' for i in range(len(importance))],
                             [[f'{i}' for i in x_means] + importance]), '数据表')
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])
        save = Dic + r'/决策树.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Forest_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(Forest_Model, self).__init__(*args,**kwargs)
        Model = {'Forest_class':RandomForestClassifier,'Forest':RandomForestRegressor}[model]
        self.Model = Model(n_estimators=args_use['n_Tree'],criterion=args_use['criterion'],max_features=args_use['max_features']
                           ,max_depth=args_use['max_depth'],min_samples_split=args_use['min_samples_split'])
        #记录这两个是为了克隆
        self.n_estimators = args_use['n_Tree']
        self.criterion = args_use['criterion']
        self.max_features = args_use['max_features']
        self.max_depth = args_use['max_depth']
        self.min_samples_split = args_use['min_samples_split']
        self.k = {'n_estimators':args_use['n_Tree'],'criterion':args_use['criterion'],'max_features':args_use['max_features'],
                  'max_depth':args_use['max_depth'],'min_samples_split':args_use['min_samples_split']}
        self.Model_Name = model

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        #多个决策树可视化
        for i in range(len(self.Model.estimators_)):
            with open(Dic + f"\Tree_Gra[{i}].dot", 'w') as f:
                export_graphviz(self.Model.estimators_[i], out_file=f)

            tab.add(SeeTree(Dic + f"\Tree_Gra[{i}].dot"),f'[{i}]决策树可视化')

        y = self.y_trainData
        x_data = self.x_trainData
        if self.Model_Name == 'Forest_class':
            class_ = self.Model.classes_.tolist()
            class_heard = [f'类别[{i}]' for i in range(len(class_))]

            get,x_means,x_range,Type = Training_visualization(x_data,class_,y)
            for i in range(len(get)):
                tab.add(get[i],f'{i}训练数据散点图')

            get = Decision_boundary(x_range,x_means,self.Predict,class_,Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            tab.add(make_Tab(class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))],
                             [class_ + [f'{i}' for i in x_means]]), '数据表')
        else:
            get, x_means, x_range,Type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测类型图')

            get = Prediction_boundary(x_range, x_means, self.Predict, Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            tab.add(make_Tab([f'普适预测第{i}特征' for i in range(len(x_means))],[[f'{i}' for i in x_means]]), '数据表')
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])
        save = Dic + r'/随机森林.HTML'
        tab.render(save)  # 生成HTML
        return save,

class GradientTree_Model(Study_MachineBase):#继承Tree_Model主要是继承Des
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(GradientTree_Model, self).__init__(*args,**kwargs)#不需要执行Tree_Model的初始化
        Model = {'GradientTree_class':GradientBoostingClassifier,'GradientTree':GradientBoostingRegressor}[model]
        self.Model = Model(n_estimators=args_use['n_Tree'],max_features=args_use['max_features']
                           ,max_depth=args_use['max_depth'],min_samples_split=args_use['min_samples_split'])
        #记录这两个是为了克隆
        self.criterion = args_use['criterion']
        self.splitter = args_use['splitter']
        self.max_features = args_use['max_features']
        self.max_depth = args_use['max_depth']
        self.min_samples_split = args_use['min_samples_split']
        self.k = {'criterion':args_use['criterion'],'splitter':args_use['splitter'],'max_features':args_use['max_features'],
                  'max_depth':args_use['max_depth'],'min_samples_split':args_use['min_samples_split']}
        self.Model_Name = model

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        #多个决策树可视化
        for a in range(len(self.Model.estimators_)):
            for i in range(len(self.Model.estimators_[a])):
                with open(Dic + f"\Tree_Gra[{a},{i}].dot", 'w') as f:
                    export_graphviz(self.Model.estimators_[a][i], out_file=f)

                tab.add(SeeTree(Dic + f"\Tree_Gra[{a},{i}].dot"),f'[{a},{i}]决策树可视化')

        y = self.y_trainData
        x_data = self.x_trainData
        if self.Model_Name == 'Tree_class':
            class_ = self.Model.classes_.tolist()
            class_heard = [f'类别[{i}]' for i in range(len(class_))]

            get,x_means,x_range,Type = Training_visualization(x_data,class_,y)
            for i in range(len(get)):
                tab.add(get[i],f'{i}训练数据散点图')

            get = Decision_boundary(x_range,x_means,self.Predict,class_,Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            tab.add(make_Tab(class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))],
                             [class_ + [f'{i}' for i in x_means]]), '数据表')
        else:
            get, x_means, x_range,Type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测类型图')

            get = Prediction_boundary(x_range, x_means, self.Predict, Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            tab.add(make_Tab([f'普适预测第{i}特征' for i in range(len(x_means))],[[f'{i}' for i in x_means]]), '数据表')
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])
        save = Dic + r'/梯度提升回归树.HTML'
        tab.render(save)  # 生成HTML
        return save,

class SVC_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SVC_Model, self).__init__(*args,**kwargs)
        self.Model = SVC(C=args_use['C'],gamma=args_use['gamma'],kernel=args_use['kernel'])
        #记录这两个是为了克隆
        self.C = args_use['C']
        self.gamma = args_use['gamma']
        self.kernel = args_use['kernel']
        self.k = {'C':args_use['C'],'gamma':args_use['gamma'],'kernel':args_use['kernel']}
        self.Model_Name = model

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        try:
            w_list = self.Model.coef_.tolist()  # 未必有这个属性
            b = self.Model.intercept_.tolist()
            U = True
        except:
            U = False
        class_ = self.Model.classes_.tolist()
        class_heard = [f'类别[{i}]' for i in range(len(class_))]

        y = self.y_trainData
        x_data = self.x_trainData
        get, x_means, x_range, Type = Training_visualization(x_data, class_, y)
        if U:get_Line = Training_W(x_data, class_, y, w_list, b, x_means.copy())
        for i in range(len(get)):
            if U:tab.add(get[i].overlap(get_Line[i]), f'{i}决策边界散点图')
            else:tab.add(get[i], f'{i}决策边界散点图')

        get = Decision_boundary(x_range, x_means, self.Predict, class_, Type)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测热力图')

        dic = {2:'离散',1:'连续'}
        tab.add(make_Tab(class_heard + [f'普适预测第{i}特征:{dic[Type[i]]}' for i in range(len(x_means))],
                         [class_ + [f'{i}' for i in x_means]]), '数据表')

        if U:desTo_CSV(Dic, '系数表', w_list, [f'系数W[{i}]' for i in range(len(w_list[0]))])
        if U:desTo_CSV(Dic, '截距表', [b], [f'截距{i}' for i in range(len(b))])
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])

        save = Dic + r'/支持向量机分类.HTML'
        tab.render(save)  # 生成HTML
        return save,

class SVR_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SVR_Model, self).__init__(*args,**kwargs)
        self.Model = SVR(C=args_use['C'],gamma=args_use['gamma'],kernel=args_use['kernel'])
        #记录这两个是为了克隆
        self.C = args_use['C']
        self.gamma = args_use['gamma']
        self.kernel = args_use['kernel']
        self.k = {'C':args_use['C'],'gamma':args_use['gamma'],'kernel':args_use['kernel']}
        self.Model_Name = model

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        x_data = self.x_trainData
        y = self.y_trainData
        try:
            w_list = self.Model.coef_.tolist()#未必有这个属性
            b = self.Model.intercept_.tolist()
            U = True
        except:
            U = False

        get, x_means, x_range,Type = regress_visualization(x_data, y)
        if U:get_Line = Regress_W(x_data, y, w_list, b, x_means.copy())
        for i in range(len(get)):
            if U:tab.add(get[i].overlap(get_Line[i]), f'{i}预测类型图')
            else:tab.add(get[i], f'{i}预测类型图')

        get = Prediction_boundary(x_range, x_means, self.Predict, Type)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测热力图')

        if U: desTo_CSV(Dic, '系数表', w_list, [f'系数W[{i}]' for i in range(len(w_list[0]))])
        if U: desTo_CSV(Dic, '截距表', [b], [f'截距{i}' for i in range(len(b))])
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])

        tab.add(make_Tab([f'普适预测第{i}特征' for i in range(len(x_means))],[[f'{i}' for i in x_means]]), '数据表')
        save = Dic + r'/支持向量机回归.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Variance_Model(Unsupervised):#无监督
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(Variance_Model, self).__init__(*args,**kwargs)
        self.Model = VarianceThreshold(threshold=(args_use['P'] * (1 - args_use['P'])))
        #记录这两个是为了克隆
        self.threshold = args_use['P']
        self.k = {'threshold':args_use['P']}
        self.Model_Name = model

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        var = self.Model.variances_#标准差
        y_data = self.y_testData
        if type(y_data) is np.ndarray:
            get = Feature_visualization(self.y_testData)
            for i in range(len(get)):
                tab.add(get[i],f'[{i}]数据x-x散点图')

        c = (
            Bar()
                .add_xaxis([f'[{i}]特征' for i in range(len(var))])
                .add_yaxis('标准差', var.tolist(), **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title='系数w柱状图'), **global_Set)
        )
        tab.add(c,'数据标准差')
        save = Dic + r'/方差特征选择.HTML'
        tab.render(save)  # 生成HTML
        return save,

class SelectKBest_Model(prep_Base):#有监督
    def __init__(self, args_use, model, *args, **kwargs):
        super(SelectKBest_Model, self).__init__(*args, **kwargs)
        self.Model = SelectKBest(k=args_use['k'],score_func=args_use['score_func'])
        # 记录这两个是为了克隆
        self.k_ = args_use['k']
        self.score_func=args_use['score_func']
        self.k = {'k':args_use['k'],'score_func':args_use['score_func']}
        self.Model_Name = model

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        score = self.Model.scores_.tolist()
        support = self.Model.get_support()
        y_data = self.y_trainData
        x_data = self.x_trainData
        if type(x_data) is np.ndarray:
            get = Feature_visualization(x_data)
            for i in range(len(get)):
                tab.add(get[i],f'[{i}]训练数据x-x散点图')

        if type(y_data) is np.ndarray:
            get = Feature_visualization(y_data)
            for i in range(len(get)):
                tab.add(get[i],f'[{i}]保留训练数据x-x散点图')

        y_data = self.y_testData
        x_data = self.x_testData
        if type(x_data) is np.ndarray:
            get = Feature_visualization(x_data)
            for i in range(len(get)):
                tab.add(get[i],f'[{i}]数据x-x散点图')

        if type(y_data) is np.ndarray:
            get = Feature_visualization(y_data)
            for i in range(len(get)):
                tab.add(get[i],f'[{i}]保留数据x-x散点图')

        Choose = []
        UnChoose = []
        for i in range(len(score)):
            if support[i]:
                Choose.append(score[i])
                UnChoose.append(0)#占位
            else:
                UnChoose.append(score[i])
                Choose.append(0)

        c = (
            Bar()
                .add_xaxis([f'[{i}]特征' for i in range(len(score))])
                .add_yaxis('选中特征', Choose, **Label_Set)
                .add_yaxis('抛弃特征', UnChoose, **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title='系数w柱状图'), **global_Set)
        )
        tab.add(c,'单变量重要程度')

        save = Dic + r'/单一变量特征选择.HTML'
        tab.render(save)  # 生成HTML
        return save,

class SelectFrom_Model(prep_Base):#有监督
    def __init__(self, args_use, Learner, *args, **kwargs):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SelectFrom_Model, self).__init__(*args, **kwargs)

        self.Model = Learner.Model
        self.Select_Model = SelectFromModel(estimator=Learner.Model,max_features=args_use['k'],prefit=Learner.have_Fit)
        self.max_features = args_use['k']
        self.estimator=Learner.Model
        self.k = {'max_features':args_use['k'],'estimator':Learner.Model,'have_Fit':Learner.have_Fit}
        self.have_Fit = Learner.have_Fit
        self.Model_Name = 'SelectFrom_Model'
        self.Learner = Learner

    def Fit(self, x_data,y_data,split=0.3, *args, **kwargs):
        y_data = y_data.ravel()
        if not self.have_Fit:  # 不允许第二次训练
            self.Select_Model.fit(x_data, y_data)
        self.have_Fit = True
        return 'None','None'

    def Predict(self, x_data, *args, **kwargs):
        try:
            self.x_testData = x_data.copy()
            x_Predict = self.Select_Model.transform(x_data)
            self.y_testData = x_Predict.copy()
            self.have_Predict = True
            return x_Predict,'模型特征工程'
        except:
            self.have_Predict = True
            return np.array([]),'无结果工程'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        support = self.Select_Model.get_support()
        y_data = self.y_testData
        x_data = self.x_testData
        if type(x_data) is np.ndarray:
            get = Feature_visualization(x_data)
            for i in range(len(get)):
                tab.add(get[i],f'[{i}]数据x-x散点图')

        if type(y_data) is np.ndarray:
            get = Feature_visualization(y_data)
            for i in range(len(get)):
                tab.add(get[i],f'[{i}]保留数据x-x散点图')

        def make_Bar(score):
            Choose = []
            UnChoose = []
            for i in range(len(score)):
                if support[i]:
                    Choose.append(abs(score[i]))
                    UnChoose.append(0)  # 占位
                else:
                    UnChoose.append(abs(score[i]))
                    Choose.append(0)
            c = (
                Bar()
                    .add_xaxis([f'[{i}]特征' for i in range(len(score))])
                    .add_yaxis('选中特征', Choose, **Label_Set)
                    .add_yaxis('抛弃特征', UnChoose, **Label_Set)
                    .set_global_opts(title_opts=opts.TitleOpts(title='系数w柱状图'), **global_Set)
            )
            tab.add(c,'单变量重要程度')

        try:
            make_Bar(self.Model.coef_)
        except:
            try:
                make_Bar(self.Model.feature_importances_)
            except:pass

        save = Dic + r'/模型特征选择.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Standardization_Model(Unsupervised):#z-score标准化 无监督
    def __init__(self, args_use, model, *args, **kwargs):
        super(Standardization_Model, self).__init__(*args, **kwargs)
        self.Model = StandardScaler()

        self.k = {}
        self.Model_Name = 'StandardScaler'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        var = self.Model.var_.tolist()
        means = self.Model.mean_.tolist()
        scale = self.Model.scale_.tolist()
        Conversion_control(y_data,x_data,tab)

        make_bar('标准差',var,tab)
        make_bar('方差',means,tab)
        make_bar('Scale',scale,tab)

        save = Dic + r'/z-score标准化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class MinMaxScaler_Model(Unsupervised):#离差标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(MinMaxScaler_Model, self).__init__(*args, **kwargs)
        self.Model = MinMaxScaler(feature_range=args_use['feature_range'])

        self.k = {}
        self.Model_Name = 'MinMaxScaler'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        scale = self.Model.scale_.tolist()
        max_ = self.Model.data_max_.tolist()
        min_ = self.Model.data_min_.tolist()
        Conversion_control(y_data,x_data,tab)
        make_bar('Scale',scale,tab)
        tab.add(make_Tab(heard= [f'[{i}]特征最大值' for i in range(len(max_))] + [f'[{i}]特征最小值' for i in range(len(min_))],
                         row=[max_ + min_]), '数据表格')

        save = Dic + r'/离差标准化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class LogScaler_Model(prep_Base):#对数标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(LogScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'LogScaler'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Predict:  # 不允许第二次训练
            self.max_logx = np.log(x_data.max())
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        try:
            max_logx = self.max_logx
        except:
            self.have_Fit = False
            self.Fit(x_data)
            max_logx = self.max_logx
        self.x_testData = x_data.copy()
        x_Predict = (np.log(x_data)/max_logx)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'对数变换'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab(heard=['最大对数值(自然对数)'],row=[[str(self.max_logx)]]),'数据表格')

        save = Dic + r'/对数标准化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class atanScaler_Model(prep_Base):#atan标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(atanScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'atanScaler'

    def Fit(self, x_data, *args, **kwargs):
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = (np.arctan(x_data)*(2/np.pi))
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'atan变换'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        Conversion_control(y_data,x_data,tab)

        save = Dic + r'/反正切函数标准化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class decimalScaler_Model(prep_Base):#小数定标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(decimalScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'Decimal_normalization'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Predict:  # 不允许第二次训练
            self.j = max([judging_Digits(x_data.max()),judging_Digits(x_data.min())])
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        try:
            j = self.j
        except:
            self.have_Fit = False
            self.Fit(x_data)
            j = self.j
        x_Predict = (x_data/(10**j))
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'小数定标标准化'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        j = self.j
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab(heard=['小数位数:j'], row=[[j]]), '数据表格')

        save = Dic + r'/小数定标标准化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Mapzoom_Model(prep_Base):#映射标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(Mapzoom_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.feature_range = args_use['feature_range']
        self.k = {}
        self.Model_Name = 'Decimal_normalization'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Predict:  # 不允许第二次训练
            self.max = x_data.max()
            self.min = x_data.min()
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        try:
            max = self.max
            min = self.min
        except:
            self.have_Fit = False
            self.Fit(x_data)
            max = self.max
            min = self.min
        x_Predict = (x_data * (self.feature_range[1] - self.feature_range[0])) / (max - min)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'映射标准化'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        max = self.max
        min = self.min
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab(heard=['最大值','最小值'], row=[[max,min]]), '数据表格')

        save = Dic + r'/映射标准化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class sigmodScaler_Model(prep_Base):#sigmod变换
    def __init__(self, args_use, model, *args, **kwargs):
        super(sigmodScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'sigmodScaler_Model'

    def Fit(self, x_data, *args, **kwargs):
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data:np.array,*args,**kwargs):
        self.x_testData = x_data.copy()
        x_Predict = (1/(1+np.exp(-x_data)))
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'Sigmod变换'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        Conversion_control(y_data,x_data,tab)

        save = Dic + r'/Sigmoid变换.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Fuzzy_quantization_Model(prep_Base):#模糊量化标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(Fuzzy_quantization_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.feature_range = args_use['feature_range']
        self.k = {}
        self.Model_Name = 'Fuzzy_quantization'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Predict:  # 不允许第二次训练
            self.max = x_data.max()
            self.min = x_data.min()
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data,*args,**kwargs):
        self.x_testData = x_data.copy()
        try:
            max = self.max
            min = self.min
        except:
            self.have_Fit = False
            self.Fit(x_data)
            max = self.max
            min = self.min
        x_Predict = 1 / 2 + (1 / 2) * np.sin(np.pi / (max - min) * (x_data - (max-min) / 2))
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'模糊量化标准化'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        max = self.max
        min = self.min
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab(heard=['最大值','最小值'], row=[[max,min]]), '数据表格')

        save = Dic + r'/模糊量化标准化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Regularization_Model(Unsupervised):#正则化
    def __init__(self, args_use, model, *args, **kwargs):
        super(Regularization_Model, self).__init__(*args, **kwargs)
        self.Model = Normalizer(norm=args_use['norm'])

        self.k = {'norm':args_use['norm']}
        self.Model_Name = 'Regularization'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData.copy()
        x_data = self.x_testData.copy()
        Conversion_control(y_data,x_data,tab)

        save = Dic + r'/正则化.HTML'
        tab.render(save)  # 生成HTML
        return save,

#离散数据
class Binarizer_Model(Unsupervised):#二值化
    def __init__(self, args_use, model, *args, **kwargs):
        super(Binarizer_Model, self).__init__(*args, **kwargs)
        self.Model = Binarizer(threshold=args_use['threshold'])

        self.k = {}
        self.Model_Name = 'Binarizer'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        get_y = Discrete_Feature_visualization(y_data,'转换数据')#转换
        for i in range(len(get_y)):
            tab.add(get_y[i],f'[{i}]数据x-x离散散点图')

        heard = [f'特征:{i}' for i in range(len(x_data[0]))]
        tab.add(make_Tab(heard,x_data.tolist()),f'原数据')
        tab.add(make_Tab(heard,y_data.tolist()), f'编码数据')
        tab.add(make_Tab(heard,np.dstack((x_data,y_data)).tolist()), f'合成[原数据,编码]数据')

        save = Dic + r'/二值离散化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Discretization_Model(prep_Base):#n值离散
    def __init__(self, args_use, model, *args, **kwargs):
        super(Discretization_Model, self).__init__(*args, **kwargs)
        self.Model = None

        range_ = args_use['split_range']
        if range_ == []:raise Exception
        elif len(range_) == 1:range_.append(range_[0])
        self.range = range_
        self.k = {}
        self.Model_Name = 'Discretization'

    def Fit(self,*args,**kwargs):
        #t值在模型创建时已经保存
        self.have_Fit = True
        return 'None','None'

    def Predict(self,x_data,*args,**kwargs):
        self.x_testData = x_data.copy()
        x_Predict = x_data.copy()#复制
        range_ = self.range
        bool_list = []
        max_ = len(range_) - 1
        o_t = None
        for i in range(len(range_)):
            try:
                t = float(range_[i])
            except:continue
            if o_t == None:#第一个参数
                bool_list.append(x_Predict <= t)
            else:
                bool_list.append((o_t <= x_Predict) == (x_Predict < t))
                if i == max_:
                    bool_list.append(t <= x_Predict)
            o_t = t
        for i in range(len(bool_list)):
            x_Predict[bool_list[i]] = i
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,f'{len(bool_list)}值离散化'

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        get_y = Discrete_Feature_visualization(y_data, '转换数据')  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f'[{i}]数据x-x离散散点图')

        heard = [f'特征:{i}' for i in range(len(x_data[0]))]
        tab.add(make_Tab(heard,x_data.tolist()),f'原数据')
        tab.add(make_Tab(heard,y_data.tolist()), f'编码数据')
        tab.add(make_Tab(heard,np.dstack((x_data,y_data)).tolist()), f'合成[原数据,编码]数据')

        save = Dic + r'/多值离散化.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Label_Model(prep_Base):#数字编码
    def __init__(self, args_use, model, *args, **kwargs):
        super(Label_Model, self).__init__(*args, **kwargs)
        self.Model = []
        self.k = {}
        self.Model_Name = 'LabelEncoder'

    def Fit(self,x_data,*args, **kwargs):
        if not self.have_Predict:  # 不允许第二次训练
            self.Model = []
            if x_data.ndim == 1:x_data = np.array([x_data])
            for i in range(x_data.shape[1]):
                self.Model.append(LabelEncoder().fit(np.ravel(x_data[:,i])))#训练机器(每个特征一个学习器)
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = x_data.copy()
        if x_data.ndim == 1: x_data = np.array([x_data])
        for i in range(x_data.shape[1]):
            x_Predict[:,i] = self.Model[i].transform(x_data[:,i])
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'数字编码'

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        x_data = self.x_testData
        y_data = self.y_testData
        get_y = Discrete_Feature_visualization(y_data, '转换数据')  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f'[{i}]数据x-x离散散点图')

        heard = [f'特征:{i}' for i in range(len(x_data[0]))]
        tab.add(make_Tab(heard,x_data.tolist()),f'原数据')
        tab.add(make_Tab(heard,y_data.tolist()), f'编码数据')
        tab.add(make_Tab(heard,np.dstack((x_data,y_data)).tolist()), f'合成[原数据,编码]数据')

        save = Dic + r'/数字编码.HTML'
        tab.render(save)  # 生成HTML
        return save,

class OneHotEncoder_Model(prep_Base):#独热编码
    def __init__(self, args_use, model, *args, **kwargs):
        super(OneHotEncoder_Model, self).__init__(*args, **kwargs)
        self.Model = []

        self.ndim_up = args_use['ndim_up']
        self.k = {}
        self.Model_Name = 'OneHotEncoder'
        self.OneHot_Data = None#三维独热编码

    def Fit(self,x_data,*args, **kwargs):
        if not self.have_Predict:  # 不允许第二次训练
            if x_data.ndim == 1:x_data = [x_data]
            for i in range(x_data.shape[1]):
                data = np.expand_dims(x_data[:,i], axis=1)#独热编码需要升维
                self.Model.append(OneHotEncoder().fit(data))#训练机器
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_new = []
        for i in range(x_data.shape[1]):
            data = np.expand_dims(x_data[:, i], axis=1)  # 独热编码需要升维
            oneHot = self.Model[i].transform(data).toarray().tolist()
            x_new.append(oneHot)#添加到列表中
        x_new = np.array(x_new)#新列表的行数据是原data列数据的独热码(只需要ndim=2，暂时没想到numpy的做法)
        x_Predict = []
        for i in range(x_new.shape[1]):
            x_Predict.append(x_new[:,i])
        x_Predict = np.array(x_Predict)#转换回array
        self.OneHot_Data = x_Predict.copy()  # 保存未降维数据
        if not self.ndim_up:#压缩操作
            new_xPredict = []
            for i in x_Predict:
                new_list = []
                list_ = i.tolist()
                for a in list_:
                    new_list += a
                new = np.array(new_list)
                new_xPredict.append(new)

            self.y_testData = np.array(new_xPredict)
            return self.y_testData.copy(),'独热编码'

        self.y_testData = self.OneHot_Data
        self.have_Predict = True
        return x_Predict,'独热编码'

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        oh_data = self.OneHot_Data
        if not self.ndim_up:
            get_y = Discrete_Feature_visualization(y_data, '转换数据')  # 转换
            for i in range(len(get_y)):
                tab.add(get_y[i], f'[{i}]数据x-x离散散点图')

        heard = [f'特征:{i}' for i in range(len(x_data[0]))]
        tab.add(make_Tab(heard,x_data.tolist()),f'原数据')
        tab.add(make_Tab(heard,oh_data.tolist()), f'编码数据')
        tab.add(make_Tab(heard,np.dstack((oh_data,x_data)).tolist()), f'合成[原数据,编码]数据')
        tab.add(make_Tab([f'编码:{i}' for i in range(len(y_data[0]))], y_data.tolist()), f'数据')
        save = Dic + r'/独热编码.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Missed_Model(Unsupervised):#缺失数据补充
    def __init__(self, args_use, model, *args, **kwargs):
        super(Missed_Model, self).__init__(*args, **kwargs)
        self.Model = SimpleImputer(missing_values=args_use['miss_value'], strategy=args_use['fill_method'],
                                   fill_value=args_use['fill_value'])

        self.k = {}
        self.Model_Name = 'Missed'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'填充缺失'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        statistics = self.Model.statistics_.tolist()
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab([f'特征[{i}]' for i in range(len(statistics))],[statistics]),'填充值')
        save = Dic + r'/缺失数据填充.HTML'
        tab.render(save)  # 生成HTML
        return save,

class PCA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(PCA_Model, self).__init__(*args, **kwargs)
        self.Model = PCA(n_components=args_use['n_components'],whiten=args_use['white_PCA'])

        self.whiten=args_use['white_PCA']
        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components'],'whiten':args_use['white_PCA']}
        self.Model_Name = 'PCA'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'PCA'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        importance = self.Model.components_.tolist()
        var = self.Model.explained_variance_.tolist()#方量差
        Conversion_Separate_Format(y_data,tab)

        x_data = [f'第{i+1}主成分' for i in range(len(importance))]#主成分
        y_data = [f'特征[{i}]' for i in range(len(importance[0]))]#主成分
        value = [(f'第{i+1}主成分',f'特征[{j}]',importance[i][j]) for i in range(len(importance)) for j in range(len(importance[i]))]
        c = (HeatMap()
             .add_xaxis(x_data)
             .add_yaxis(f'', y_data, value, **Label_Set)  # value的第一个数值是x
             .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Leg,
                              yaxis_opts=opts.AxisOpts(is_scale=True),  # 'category'
                              xaxis_opts=opts.AxisOpts(is_scale=True),
                              visualmap_opts=opts.VisualMapOpts(is_show=True, max_=int(self.Model.components_.max()) + 1,
                                                                min_=int(self.Model.components_.min()),
                                                                pos_right='3%'))  # 显示
             )
        tab.add(c,'成分热力图')
        c = (
            Bar()
                .add_xaxis([f'第[{i}]主成分' for i in range(len(var))])
                .add_yaxis('方量差', var, **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title='方量差柱状图'), **global_Set)
        )

        desTo_CSV(Dic, '成分重要性', importance, [x_data],[y_data])
        desTo_CSV(Dic, '方量差', [var], [f'第[{i}]主成分' for i in range(len(var))])

        tab.add(c, '方量差柱状图')
        save = Dic + r'/主成分分析.HTML'
        tab.render(save)  # 生成HTML
        return save,

class RPCA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(RPCA_Model, self).__init__(*args, **kwargs)
        self.Model = IncrementalPCA(n_components=args_use['n_components'],whiten=args_use['white_PCA'])

        self.n_components = args_use['n_components']
        self.whiten=args_use['white_PCA']
        self.k = {'n_components': args_use['n_components'],'whiten':args_use['white_PCA']}
        self.Model_Name = 'RPCA'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'RPCA'

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        y_data = self.y_trainData
        importance = self.Model.components_.tolist()
        var = self.Model.explained_variance_.tolist()  # 方量差
        Conversion_Separate_Format(y_data, tab)

        x_data = [f'第{i + 1}主成分' for i in range(len(importance))]  # 主成分
        y_data = [f'特征[{i}]' for i in range(len(importance[0]))]  # 主成分
        value = [(f'第{i + 1}主成分', f'特征[{j}]', importance[i][j]) for i in range(len(importance)) for j in
                 range(len(importance[i]))]
        c = (HeatMap()
             .add_xaxis(x_data)
             .add_yaxis(f'', y_data, value, **Label_Set)  # value的第一个数值是x
             .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Leg,
                              yaxis_opts=opts.AxisOpts(is_scale=True),  # 'category'
                              xaxis_opts=opts.AxisOpts(is_scale=True),
                              visualmap_opts=opts.VisualMapOpts(is_show=True,
                                                                max_=int(self.Model.components_.max()) + 1,
                                                                min_=int(self.Model.components_.min()),
                                                                pos_right='3%'))  # 显示
             )
        tab.add(c, '成分热力图')
        c = (
            Bar()
                .add_xaxis([f'第[{i}]主成分' for i in range(len(var))])
                .add_yaxis('放量差', var, **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title='方量差柱状图'), **global_Set)
        )
        tab.add(c, '方量差柱状图')
        desTo_CSV(Dic, '成分重要性', importance, [x_data],[y_data])
        desTo_CSV(Dic, '方量差', [var], [f'第[{i}]主成分' for i in range(len(var))])
        save = Dic + r'/RPCA(主成分分析).HTML'
        tab.render(save)  # 生成HTML
        return save,

class KPCA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(KPCA_Model, self).__init__(*args, **kwargs)
        self.Model = KernelPCA(n_components=args_use['n_components'], kernel=args_use['kernel'])
        self.n_components = args_use['n_components']
        self.kernel = args_use['kernel']
        self.k = {'n_components': args_use['n_components'],'kernel':args_use['kernel']}
        self.Model_Name = 'KPCA'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'KPCA'

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        y_data = self.y_testData
        Conversion_Separate_Format(y_data, tab)

        save = Dic + r'/KPCA(主成分分析).HTML'
        tab.render(save)  # 生成HTML
        return save,

class LDA_Model(prep_Base):#有监督学习
    def __init__(self, args_use, model, *args, **kwargs):
        super(LDA_Model, self).__init__(*args, **kwargs)
        self.Model = LDA(n_components=args_use['n_components'])
        self.n_components = args_use['n_components']
        self.k = {'n_components': args_use['n_components']}
        self.Model_Name = 'LDA'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'LDA'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()

        x_data = self.x_testData
        y_data = self.y_testData
        Conversion_Separate_Format(y_data,tab)

        w_list = self.Model.coef_.tolist()  # 变为表格
        b = self.Model.intercept_
        tab = Tab()

        x_means = make_Cat(x_data).get()[0]
        get = Regress_W(x_data, None, w_list, b, x_means.copy())#回归的y是历史遗留问题 不用分类回归：因为得不到分类数据（predict结果是降维数据不是预测数据）
        for i in range(len(get)):
            tab.add(get[i].overlap(get[i]), f'类别:{i}LDA映射曲线')

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class NMF_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(NMF_Model, self).__init__(*args, **kwargs)
        self.Model = NMF(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components']}
        self.Model_Name = 'NFM'
        self.h_testData = None
        #x_trainData保存的是W，h_trainData和y_trainData是后来数据

    def Predict(self, x_data,x_name='',Add_Func=None,*args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_testData = x_Predict.copy()
        self.h_testData = self.Model.components_
        if Add_Func != None and x_name != '':
            Add_Func(self.h_testData, f'{x_name}:V->NMF[H]')
        self.have_Predict = True
        return x_Predict,'V->NMF[W]'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        x_data = self.x_testData
        h_data = self.h_testData
        Conversion_SeparateWH(y_data,h_data,tab)

        wh_data = np.matmul(y_data, h_data)
        difference_data = x_data - wh_data

        def make_HeatMap(data,name,max_,min_):
            x = [f'数据[{i}]' for i in range(len(data))]  # 主成分
            y = [f'特征[{i}]' for i in range(len(data[0]))]  # 主成分
            value = [(f'数据[{i}]', f'特征[{j}]', float(data[i][j])) for i in range(len(data)) for j in range(len(data[i]))]

            c = (HeatMap()
                 .add_xaxis(x)
                 .add_yaxis(f'数据', y, value, **Label_Set)  # value的第一个数值是x
                 .set_global_opts(title_opts=opts.TitleOpts(title='原始数据热力图'), **global_Leg,
                                  yaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),  # 'category'
                                  xaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),
                                  visualmap_opts=opts.VisualMapOpts(is_show=True, max_=max_,
                                                                    min_=min_,
                                                                    pos_right='3%'))#显示
                 )
            tab.add(c,name)

        max_ = max(int(x_data.max()),int(wh_data.max()),int(difference_data.max())) + 1
        min_ = min(int(x_data.min()),int(wh_data.min()),int(difference_data.min()))

        make_HeatMap(x_data,'原始数据热力图',max_,min_)
        make_HeatMap(wh_data,'W * H数据热力图',max_,min_)
        make_HeatMap(difference_data,'数据差热力图',max_,min_)

        desTo_CSV(Dic, '权重矩阵', y_data)
        desTo_CSV(Dic, '系数矩阵', h_data)
        desTo_CSV(Dic, '系数*权重矩阵', wh_data)

        save = Dic + r'/非负矩阵分解.HTML'
        tab.render(save)  # 生成HTML
        return save,

class TSNE_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(TSNE_Model, self).__init__(*args, **kwargs)
        self.Model = TSNE(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components']}
        self.Model_Name = 't-SNE'

    def Fit(self,*args, **kwargs):
        self.have_Fit = True
        return 'None', 'None'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        x_Predict = self.Model.fit_transform(x_data)
        self.y_testData = x_Predict.copy()
        self.have_Predict = True
        return x_Predict,'SNE'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_testData
        Conversion_Separate_Format(y_data,tab)

        save = Dic + r'/T-SNE.HTML'
        tab.render(save)  # 生成HTML
        return save,

class MLP_Model(Study_MachineBase):#神经网络(多层感知机)，有监督学习
    def __init__(self,args_use,model,*args,**kwargs):
        super(MLP_Model, self).__init__(*args,**kwargs)
        Model = {'MLP':MLPRegressor,'MLP_class':MLPClassifier}[model]
        self.Model = Model(hidden_layer_sizes=args_use['hidden_size'],activation=args_use['activation'],
                           solver=args_use['solver'],alpha=args_use['alpha'],max_iter=args_use['max_iter'])
        #记录这两个是为了克隆
        self.hidden_layer_sizes = args_use['hidden_size']
        self.activation = args_use['activation']
        self.max_iter = args_use['max_iter']
        self.solver = args_use['solver']
        self.alpha = args_use['alpha']
        self.k = {'hidden_layer_sizes':args_use['hidden_size'],'activation':args_use['activation'],'max_iter':args_use['max_iter'],
                  'solver':args_use['solver'],'alpha':args_use['alpha']}
        self.Model_Name = model

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()

        x_data = self.x_testData
        y_data = self.y_testData
        coefs = self.Model.coefs_
        class_ = self.Model.classes_
        n_layers_ = self.Model.n_layers_
        def make_HeatMap(data,name):
            x = [f'特征(节点)[{i}]' for i in range(len(data))]
            y = [f'节点[{i}]' for i in range(len(data[0]))]
            value = [(f'特征(节点)[{i}]', f'节点[{j}]', float(data[i][j])) for i in range(len(data)) for j in range(len(data[i]))]

            c = (HeatMap()
                 .add_xaxis(x)
                 .add_yaxis(f'数据', y, value, **Label_Set)  # value的第一个数值是x
                 .set_global_opts(title_opts=opts.TitleOpts(title=name), **global_Leg,
                                  yaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),  # 'category'
                                  xaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),
                                  visualmap_opts=opts.VisualMapOpts(is_show=True, max_=float(data.max()),
                                                                    min_=float(data.min()),
                                                                    pos_right='3%'))#显示
                 )
            tab.add(c,name)
            tab.add(make_Tab(x,data.T.tolist()),f'{name}:表格')
            desTo_CSV(Dic,f'{name}:表格',data.T.tolist(),x,y)

        get, x_means, x_range, Type = regress_visualization(x_data, y_data)
        for i in range(len(get)):
            tab.add(get[i], f'{i}训练数据散点图')

        get = Prediction_boundary(x_range, x_means, self.Predict, Type)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测热力图')

        heard = ['神经网络层数']
        data = [n_layers_]
        for i in range(len(coefs)):
            make_HeatMap(coefs[i],f'{i}层权重矩阵')
            heard.append(f'第{i}层节点数')
            data.append(len(coefs[i][0]))

        if self.Model_Name == 'MLP_class':
            heard += [f'[{i}]类型' for i in range(len(class_))]
            data += class_.tolist()

        tab.add(make_Tab(heard,[data]),'数据表')

        save = Dic + r'/多层感知机.HTML'
        tab.render(save)  # 生成HTML
        return save,

class kmeans_Model(UnsupervisedModel):
    def __init__(self, args_use, model, *args, **kwargs):
        super(kmeans_Model, self).__init__(*args, **kwargs)
        self.Model = KMeans(n_clusters=args_use['n_clusters'])

        self.class_ = []
        self.n_clusters = args_use['n_clusters']
        self.k = {'n_clusters':args_use['n_clusters']}
        self.Model_Name = 'k-means'

    def Fit(self, x_data, *args, **kwargs):
        re = super().Fit(x_data,*args,**kwargs)
        self.class_ = list(set(self.Model.labels_.tolist()))
        self.have_Fit = True
        return re

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        y_Predict = self.Model.predict(x_data)
        self.y_testData = y_Predict.copy()
        self.have_Predict = True
        return y_Predict,'k-means'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y = self.y_testData
        x_data = self.x_testData
        class_ = self.class_
        center = self.Model.cluster_centers_
        class_heard = [f'簇[{i}]' for i in range(len(class_))]

        Func = Training_visualization_More if More_Global else Training_visualization_Center
        get,x_means,x_range,Type = Func(x_data,class_,y,center)
        for i in range(len(get)):
            tab.add(get[i],f'{i}数据散点图')

        get = Decision_boundary(x_range, x_means, self.Predict, class_, Type)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测热力图')

        heard = class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))]
        data = class_ + [f'{i}' for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, '数据表')
        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])
        save = Dic + r'/k-means聚类.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Agglomerative_Model(UnsupervisedModel):
    def __init__(self, args_use, model, *args, **kwargs):
        super(Agglomerative_Model, self).__init__(*args, **kwargs)
        self.Model = AgglomerativeClustering(n_clusters=args_use['n_clusters'])#默认为2，不同于k-means

        self.class_ = []
        self.n_clusters = args_use['n_clusters']
        self.k = {'n_clusters':args_use['n_clusters']}
        self.Model_Name = 'Agglomerative'

    def Fit(self, x_data, *args, **kwargs):
        re = super().Fit(x_data,*args,**kwargs)
        self.class_ = list(set(self.Model.labels_.tolist()))
        self.have_Fit = True
        return re

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        y_Predict = self.Model.fit_predict(x_data)
        self.y_trainData = y_Predict.copy()
        self.have_Predict = True
        return y_Predict,'Agglomerative'

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        y = self.y_testData
        x_data = self.x_testData
        class_ = self.class_
        class_heard = [f'簇[{i}]' for i in range(len(class_))]

        Func = Training_visualization_More_NoCenter if More_Global else Training_visualization
        get, x_means, x_range, Type = Func(x_data, class_, y)
        for i in range(len(get)):
            tab.add(get[i], f'{i}训练数据散点图')

        get = Decision_boundary(x_range, x_means, self.Predict, class_, Type)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测热力图')

        linkage_array = ward(self.x_trainData)#self.y_trainData是结果
        dendrogram(linkage_array)
        plt.savefig(Dic + r'/Cluster_graph.png')

        image = Image()
        image.add(
            src=Dic + r'/Cluster_graph.png',
        ).set_global_opts(
            title_opts=opts.ComponentTitleOpts(title="聚类树状图")
        )

        tab.add(image,'聚类树状图')

        heard = class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))]
        data = class_ + [f'{i}' for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, '数据表')

        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])
        save = Dic + r'/层次聚类.HTML'
        tab.render(save)  # 生成HTML
        return save,

class DBSCAN_Model(UnsupervisedModel):
    def __init__(self, args_use, model, *args, **kwargs):
        super(DBSCAN_Model, self).__init__(*args, **kwargs)
        self.Model = DBSCAN(eps = args_use['eps'], min_samples = args_use['min_samples'])
        #eps是距离(0.5)，min_samples(5)是簇与噪音分界线(每个簇最小元素数)
        # min_samples
        self.eps = args_use['eps']
        self.min_samples = args_use['min_samples']
        self.k = {'min_samples':args_use['min_samples'],'eps':args_use['eps']}
        self.class_ = []
        self.Model_Name = 'DBSCAN'

    def Fit(self, x_data, *args, **kwargs):
        re = super().Fit(x_data,*args,**kwargs)
        self.class_ = list(set(self.Model.labels_.tolist()))
        self.have_Fit = True
        return re

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        y_Predict = self.Model.fit_predict(x_data)
        self.y_testData = y_Predict.copy()
        self.have_Predict = True
        return y_Predict,'DBSCAN'

    def Des(self, Dic, *args, **kwargs):
        #DBSCAN没有预测的必要
        tab = Tab()
        y = self.y_testData.copy()
        x_data = self.x_testData.copy()
        class_ = self.class_
        class_heard = [f'簇[{i}]' for i in range(len(class_))]

        Func = Training_visualization_More_NoCenter if More_Global else Training_visualization
        get, x_means, x_range, Type = Func(x_data, class_, y)
        for i in range(len(get)):
            tab.add(get[i], f'{i}训练数据散点图')

        heard = class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))]
        data = class_ + [f'{i}' for i in x_means]
        c = Table().add(headers=heard, rows=[data])
        tab.add(c, '数据表')

        desTo_CSV(Dic, '预测表', [[f'{i}' for i in x_means]], [f'普适预测第{i}特征' for i in range(len(x_means))])
        save = Dic + r'/密度聚类.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Fast_Fourier(Study_MachineBase):#快速傅里叶变换
    def __init__(self, args_use, model, *args, **kwargs):
        super(Fast_Fourier, self).__init__(*args, **kwargs)
        self.Model = None
        self.Fourier = None#fft复数
        self.Frequency = None#频率range
        self.angular_Frequency = None#角频率range
        self.Phase = None#相位range
        self.Breadth = None#震幅range
        self.N = None#样本数

    def Fit(self, y_data, *args, **kwargs):
        y_data = y_data.ravel()  # 扯平为一维数组
        try:
            if self.y_trainData is None:raise Exception
            self.y_trainData = np.hstack(y_data,self.x_trainData)
        except:
            self.y_trainData = y_data.copy()
        Fourier = fft(y_data)
        self.N = len(y_data)
        self.Frequency = np.linspace(0,1,self.N)#频率N_range
        self.angular_Frequency = self.Frequency / ( np.pi * 2 )#角频率w
        self.Phase = np.angle(Fourier)
        self.Breadth = np.abs(Fourier)
        self.Fourier = Fourier
        self.have_Fit = True
        return 'None','None'

    def Predict(self, x_data, *args, **kwargs):
        return np.array([]),''

    def Des(self, Dic, *args, **kwargs):
        #DBSCAN没有预测的必要
        tab = Tab()
        y = self.y_trainData.copy()
        N = self.N
        Phase = self.Phase#相位range
        Breadth = self.Breadth#震幅range
        normalization_Breadth = Breadth/N
        def line(name,value,s=slice(0,None)) -> Line:
            c = (
                Line()
                    .add_xaxis(self.Frequency[s].tolist())
                    .add_yaxis('', value,**Label_Set,symbol='none' if self.N >= 500 else None)
                    .set_global_opts(title_opts=opts.TitleOpts(title=name),**global_Leg,
                                     xaxis_opts=opts.AxisOpts(type_='value'),
                                     yaxis_opts=opts.AxisOpts(type_='value'))
            )
            return c

        tab.add(line('原始数据',y.tolist()),'原始数据')
        tab.add(line('双边振幅谱',Breadth.tolist()),'双边振幅谱')
        tab.add(line('双边振幅谱(归一化)',normalization_Breadth.tolist()),'双边振幅谱(归一化)')
        tab.add(line('单边相位谱',Breadth[:int(N/2)].tolist(),slice(0,int(N/2))),'单边相位谱')
        tab.add(line('单边相位谱(归一化)',normalization_Breadth[:int(N/2)].tolist(),slice(0,int(N/2))),'单边相位谱(归一化)')
        tab.add(line('双边相位谱', Phase.tolist()), '双边相位谱')
        tab.add(line('单边相位谱', Phase[:int(N/2)].tolist(),slice(0,int(N/2))), '单边相位谱')

        tab.add(make_Tab(self.Frequency.tolist(),[Breadth.tolist()]),'双边振幅谱')
        tab.add(make_Tab(self.Frequency.tolist(),[Phase.tolist()]),'双边相位谱')
        tab.add(make_Tab(self.Frequency.tolist(),[self.Fourier.tolist()]),'快速傅里叶变换')

        save = Dic + r'/快速傅里叶.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Reverse_Fast_Fourier(Study_MachineBase):#快速傅里叶变换
    def __init__(self, args_use, model, *args, **kwargs):
        super(Reverse_Fast_Fourier, self).__init__(*args, **kwargs)
        self.Model = None
        self.N = None
        self.y_testData_real = None
        self.Phase = None
        self.Breadth = None

    def Fit(self, y_data, *args, **kwargs):
        return 'None','None'

    def Predict(self, x_data,x_name='', Add_Func=None, *args, **kwargs):
        self.x_testData = x_data.ravel().astype(np.complex_)
        Fourier = ifft(self.x_testData)
        self.y_testData = Fourier.copy()
        self.y_testData_real = np.real(Fourier)
        self.N = len(self.y_testData_real)
        self.Phase = np.angle(self.x_testData)
        self.Breadth = np.abs(self.x_testData)
        Add_Func(self.y_testData_real.copy(), f'{x_name}:逆向快速傅里叶变换[实数]')
        return Fourier,'逆向快速傅里叶变换'

    def Des(self, Dic, *args, **kwargs):
        #DBSCAN没有预测的必要
        tab = Tab()
        y = self.y_testData_real.copy()
        y_data = self.y_testData.copy()
        N = self.N
        range_N = np.linspace(0,1,N).tolist()
        Phase = self.Phase#相位range
        Breadth = self.Breadth#震幅range

        def line(name,value,s=slice(0,None)) -> Line:
            c = (
                Line()
                    .add_xaxis(range_N[s])
                    .add_yaxis('', value,**Label_Set,symbol='none' if N >= 500 else None)
                    .set_global_opts(title_opts=opts.TitleOpts(title=name),**global_Leg,
                                     xaxis_opts=opts.AxisOpts(type_='value'),
                                     yaxis_opts=opts.AxisOpts(type_='value'))
            )
            return c

        tab.add(line('逆向傅里叶变换', y.tolist()), '逆向傅里叶变换[实数]')
        tab.add(make_Tab(range_N,[y_data.tolist()]),'逆向傅里叶变换数据')
        tab.add(make_Tab(range_N,[y.tolist()]),'逆向傅里叶变换数据[实数]')
        tab.add(line('双边振幅谱',Breadth.tolist()),'双边振幅谱')
        tab.add(line('单边相位谱',Breadth[:int(N/2)].tolist(),slice(0,int(N/2))),'单边相位谱')
        tab.add(line('双边相位谱', Phase.tolist()), '双边相位谱')
        tab.add(line('单边相位谱', Phase[:int(N/2)].tolist(),slice(0,int(N/2))), '单边相位谱')

        save = Dic + r'/快速傅里叶.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Reverse_Fast_Fourier_TwoNumpy(Reverse_Fast_Fourier):#2快速傅里叶变换
    def Fit(self, x_data,y_data=None,x_name='', Add_Func=None, *args, **kwargs):
        r = np.multiply(np.cos(x_data),y_data)
        j = np.multiply(np.sin(x_data),y_data) * 1j
        super(Reverse_Fast_Fourier_TwoNumpy, self).Predict(r + j,x_name=x_name, Add_Func=Add_Func, *args, **kwargs)
        return 'None','None'

class Curve_fitting(Study_MachineBase):#曲线拟合
    def __init__(self,Name, str_, model, *args, **kwargs):
        super(Curve_fitting, self).__init__(*args, **kwargs)
        def ndimDown(data:np.ndarray):
            if data.ndim == 1:return data
            new_data = []
            for i in data:
                new_data.append(np.sum(i))
            return np.array(new_data)
        NAME = {'np':np,'Func':model,'ndimDown':ndimDown}
        DEF = f'''
def FUNC({",".join(model.__code__.co_varnames)}):
    answer = Func({",".join(model.__code__.co_varnames)})
    return ndimDown(answer)
'''
        exec(DEF,NAME)
        self.Func = NAME['FUNC']
        self.Fit_data = None
        self.Name = Name
        self.Func_Str = str_

    def Fit(self, x_data:np.ndarray,y_data:np.ndarray, *args, **kwargs):
        y_data = y_data.ravel()
        x_data = x_data.astype(np.float64)
        try:
            if self.x_trainData is None:raise Exception
            self.x_trainData = np.vstack(x_data,self.x_trainData)
            self.y_trainData = np.vstack(y_data,self.y_trainData)
        except:
            self.x_trainData = x_data.copy()
            self.y_trainData = y_data.copy()
        self.Fit_data = optimize.curve_fit(self.Func,self.x_trainData,self.y_trainData)
        self.Model = self.Fit_data[0].copy()
        return 'None','None'

    def Predict(self, x_data, *args, **kwargs):
        self.x_testData = x_data.copy()
        Predict = self.Func(x_data,*self.Model)
        y_Predict = []
        for i in Predict:
            y_Predict.append(np.sum(i))
        y_Predict = np.array(y_Predict)
        self.y_testData = y_Predict.copy()
        self.have_Predict = True
        return y_Predict,self.Name

    def Des(self, Dic, *args, **kwargs):
        #DBSCAN没有预测的必要
        tab = Tab()
        y = self.y_testData.copy()
        x_data = self.x_testData.copy()

        get, x_means, x_range,Type = regress_visualization(x_data, y)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测类型图')

        get = Prediction_boundary(x_range, x_means, self.Predict, Type)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测热力图')

        tab.add(make_Tab([f'普适预测第{i}特征' for i in range(len(x_means))], [[f'{i}' for i in x_means]]),'普适预测特征数据')
        tab.add(make_Tab([f'参数[{i}]' for i in range(len(self.Model))], [[f'{i}' for i in self.Model]]), '拟合参数')

        save = Dic + r'/曲线拟合.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Machine_Learner(Learner):#数据处理者
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Learner = {}#记录机器
        self.Learn_Dic = {'Line':Line_Model,
                          'Ridge':Line_Model,
                          'Lasso':Line_Model,
                          'LogisticRegression':LogisticRegression_Model,
                          'Knn_class':Knn_Model,
                          'Knn': Knn_Model,
                          'Tree_class': Tree_Model,
                          'Tree': Tree_Model,
                          'Forest':Forest_Model,
                          'Forest_class': Forest_Model,
                          'GradientTree_class':GradientTree_Model,
                          'GradientTree': GradientTree_Model,
                          'Variance':Variance_Model,
                          'SelectKBest':SelectKBest_Model,
                          'Z-Score':Standardization_Model,
                          'MinMaxScaler':MinMaxScaler_Model,
                          'LogScaler':LogScaler_Model,
                          'atanScaler':atanScaler_Model,
                          'decimalScaler':decimalScaler_Model,
                          'sigmodScaler':sigmodScaler_Model,
                          'Mapzoom':Mapzoom_Model,
                          'Fuzzy_quantization':Fuzzy_quantization_Model,
                          'Regularization':Regularization_Model,
                          'Binarizer':Binarizer_Model,
                          'Discretization':Discretization_Model,
                          'Label':Label_Model,
                          'OneHotEncoder':OneHotEncoder_Model,
                          'Missed':Missed_Model,
                          'PCA':PCA_Model,
                          'RPCA':RPCA_Model,
                          'KPCA':KPCA_Model,
                          'LDA':LDA_Model,
                          'SVC':SVC_Model,
                          'SVR':SVR_Model,
                          'MLP':MLP_Model,
                          'MLP_class': MLP_Model,
                          'NMF':NMF_Model,
                          't-SNE':TSNE_Model,
                          'k-means':kmeans_Model,
                          'Agglomerative':Agglomerative_Model,
                          'DBSCAN':DBSCAN_Model,
                          'ClassBar':Class_To_Bar,
                          'FeatureScatter':Near_feature_scatter,
                          'FeatureScatterClass': Near_feature_scatter_class,
                          'FeatureScatter_all':Near_feature_scatter_More,
                          'FeatureScatterClass_all':Near_feature_scatter_class_More,
                          'HeatMap':Numpy_To_HeatMap,
                          'FeatureY-X':Feature_scatter_YX,
                          'ClusterTree':Cluster_Tree,
                          'MatrixScatter':MatrixScatter,
                          'Correlation':CORR,
                          'Statistics':Des,
                          'Fast_Fourier':Fast_Fourier,
                          'Reverse_Fast_Fourier':Reverse_Fast_Fourier,
                          '[2]Reverse_Fast_Fourier':Reverse_Fast_Fourier_TwoNumpy,
                          }
        self.Learner_Type = {}#记录机器的类型

    def p_Args(self,Text,Type):#解析参数
        args = {}
        args_use = {}
        #输入数据
        exec(Text,args)
        #处理数据
        if Type in ('MLP','MLP_class'):
            args_use['alpha'] = float(args.get('alpha', 0.0001))  # MLP正则化用
        else:
            args_use['alpha'] = float(args.get('alpha',1.0))#L1和L2正则化用
        args_use['C'] = float(args.get('C', 1.0))  # L1和L2正则化用
        if Type in ('MLP','MLP_class'):
            args_use['max_iter'] = int(args.get('max_iter', 200))  # L1和L2正则化用
        else:
            args_use['max_iter'] = int(args.get('max_iter', 1000))  # L1和L2正则化用
        args_use['n_neighbors'] = int(args.get('K_knn', 5))#knn邻居数 (命名不同)
        args_use['p'] = int(args.get('p', 2))  # 距离计算方式
        args_use['nDim_2'] = bool(args.get('nDim_2', True))  # 数据是否降维

        if Type in ('Tree','Forest','GradientTree'):
            args_use['criterion'] = 'mse' if bool(args.get('is_MSE', True)) else 'mae'  # 是否使用基尼不纯度
        else:
            args_use['criterion'] = 'gini' if bool(args.get('is_Gini', True)) else 'entropy'  # 是否使用基尼不纯度
        args_use['splitter'] = 'random' if bool(args.get('is_random', False)) else 'best' # 决策树节点是否随机选用最优
        args_use['max_features'] = args.get('max_features', None) # 选用最多特征数
        args_use['max_depth'] = args.get('max_depth', None)  # 最大深度
        args_use['min_samples_split'] = int(args.get('min_samples_split', 2))  # 是否继续划分（容易造成过拟合）

        args_use['P'] = float(args.get('min_samples_split', 0.8))
        args_use['k'] = args.get('k',1)
        args_use['score_func'] = ({'chi2':chi2,'f_classif':f_classif,'mutual_info_classif':mutual_info_classif,
                                   'f_regression':f_regression,'mutual_info_regression':mutual_info_regression}.
                                  get(args.get('score_func','f_classif'),f_classif))

        args_use['feature_range'] = tuple(args.get('feature_range',(0,1)))
        args_use['norm'] = args.get('norm','l2')#正则化的方式L1或者L2

        args_use['threshold'] = float(args.get('threshold', 0.0))  # 二值化特征

        args_use['split_range'] = list(args.get('split_range', [0]))  # 二值化特征

        args_use['ndim_up'] = bool(args.get('ndim_up', False))
        args_use['miss_value'] = args.get('miss_value',np.nan)
        args_use['fill_method'] = args.get('fill_method','mean')
        args_use['fill_value'] = args.get('fill_value',None)

        args_use['n_components'] = args.get('n_components',1)
        args_use['kernel'] = args.get('kernel','rbf' if Type in ('SVR','SVC') else 'linear')

        args_use['n_Tree'] = args.get('n_Tree',100)
        args_use['gamma'] = args.get('gamma',1)
        args_use['hidden_size'] = tuple(args.get('hidden_size',(100,)))
        args_use['activation'] = str(args.get('activation','relu'))
        args_use['solver'] = str(args.get('solver','adam'))
        if Type in ('k-means',):
            args_use['n_clusters'] = int(args.get('n_clusters',8))
        else:
            args_use['n_clusters'] = int(args.get('n_clusters', 2))
        args_use['eps'] = float(args.get('n_clusters', 0.5))
        args_use['min_samples'] = int(args.get('n_clusters', 5))
        args_use['white_PCA'] = bool(args.get('white_PCA', False))
        return args_use

    def Add_Learner(self,Learner,Text=''):
        get = self.Learn_Dic[Learner]
        name = f'Le[{len(self.Learner)}]{Learner}'
        #参数调节
        args_use = self.p_Args(Text,Learner)
        #生成学习器
        self.Learner[name] = get(model=Learner,args_use=args_use)
        self.Learner_Type[name] = Learner

    def Add_Curve_Fitting(self,Learner_text,Text=''):
        NAME = {}
        exec(Learner_text,NAME)
        name = f'Le[{len(self.Learner)}]{NAME.get("name","SELF")}'
        func = NAME.get('f',lambda x,k,b:k * x + b)
        self.Learner[name] = Curve_fitting(name,Learner_text,func)
        self.Learner_Type[name] = 'Curve_fitting'

    def Add_SelectFrom_Model(self,Learner,Text=''):#Learner代表选中的学习器
        model = self.get_Learner(Learner)
        name = f'Le[{len(self.Learner)}]SelectFrom_Model:{Learner}'
        #参数调节
        args_use = self.p_Args(Text,'SelectFrom_Model')
        #生成学习器
        self.Learner[name] = SelectFrom_Model(Learner=model,args_use=args_use,Dic=self.Learn_Dic)
        self.Learner_Type[name] = 'SelectFrom_Model'

    def Add_Predictive_HeatMap(self,Learner,Text=''):#Learner代表选中的学习器
        model = self.get_Learner(Learner)
        name = f'Le[{len(self.Learner)}]Predictive_HeatMap:{Learner}'
        #生成学习器
        args_use = self.p_Args(Text, 'Predictive_HeatMap')
        self.Learner[name] = Predictive_HeatMap(Learner=model,args_use=args_use)
        self.Learner_Type[name] = 'Predictive_HeatMap'

    def Add_Predictive_HeatMap_More(self,Learner,Text=''):#Learner代表选中的学习器
        model = self.get_Learner(Learner)
        name = f'Le[{len(self.Learner)}]Predictive_HeatMap_More:{Learner}'
        #生成学习器
        args_use = self.p_Args(Text, 'Predictive_HeatMap_More')
        self.Learner[name] = Predictive_HeatMap_More(Learner=model,args_use=args_use)
        self.Learner_Type[name] = 'Predictive_HeatMap_More'

    def Add_View_data(self,Learner,Text=''):#Learner代表选中的学习器
        model = self.get_Learner(Learner)
        name = f'Le[{len(self.Learner)}]View_data:{Learner}'
        #生成学习器
        args_use = self.p_Args(Text, 'View_data')
        self.Learner[name] = View_data(Learner=model,args_use=args_use)
        self.Learner_Type[name] = 'View_data'

    def Return_Learner(self):
        return self.Learner.copy()

    def get_Learner(self,name):
        return self.Learner[name]

    def get_Learner_Type(self,name):
        return self.Learner_Type[name]

    def Fit(self,x_name,y_name,Learner,split=0.3,*args,**kwargs):
        x_data = self.get_Sheet(x_name)
        y_data = self.get_Sheet(y_name)
        model = self.get_Learner(Learner)
        return model.Fit(x_data,y_data,split = split, x_name=x_name, Add_Func=self.Add_Form)

    def Predict(self,x_name,Learner,Text='',**kwargs):
        x_data = self.get_Sheet(x_name)
        model = self.get_Learner(Learner)
        y_data,name = model.Predict(x_data, x_name=x_name, Add_Func=self.Add_Form)
        self.Add_Form(y_data,f'{x_name}:{name}')
        return y_data

    def Score(self,name_x,name_y,Learner):#Score_Only表示仅评分 Fit_Simp 是普遍类操作
        model = self.get_Learner(Learner)
        x = self.get_Sheet(name_x)
        y = self.get_Sheet(name_y)
        return model.Score(x,y)

    def Show_Score(self,Learner,Dic,name_x,name_y,Func=0):#显示参数
        x = self.get_Sheet(name_x)
        y = self.get_Sheet(name_y)
        if NEW_Global:
            dic = Dic + f'/{Learner}分类评分[CoTan]'
            new_dic = dic
            a = 0
            while exists(new_dic):#直到他不存在 —— False
                new_dic = dic + f'[{a}]'
                a += 1
            mkdir(new_dic)
        else:
            new_dic = Dic
        model = self.get_Learner(Learner)
        #打包
        func = [model.Class_Score, model.Regression_Score, model.Clusters_Score][Func]
        save = func(new_dic,x,y)[0]
        if TAR_Global:make_targz(f'{new_dic}.tar.gz',new_dic)
        return save,new_dic

    def Show_Args(self,Learner,Dic):#显示参数
        if NEW_Global:
            dic = Dic + f'/{Learner}数据[CoTan]'
            new_dic = dic
            a = 0
            while exists(new_dic):#直到他不存在 —— False
                new_dic = dic + f'[{a}]'
                a += 1
            mkdir(new_dic)
        else:
            new_dic = Dic
        model = self.get_Learner(Learner)
        if (not(model.Model is None) or not(model.Model is list)) and CLF_Global:
            joblib.dump(model.Model,new_dic + '/MODEL.model')#保存模型
        # pickle.dump(model,new_dic + f'/{Learner}.pkl')#保存学习器
        #打包
        save = model.Des(new_dic)[0]
        if TAR_Global:make_targz(f'{new_dic}.tar.gz',new_dic)
        return save,new_dic

    def Del_Leaner(self,Leaner):
        del self.Learner[Leaner]
        del self.Learner_Type[Leaner]

def make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=basename(source_dir))
    return output_filename

def set_Global(More=More_Global,All=All_Global,CSV=CSV_Global,CLF=CLF_Global,TAR=TAR_Global,NEW=NEW_Global):
    global More_Global,All_Global,CSV_Global,CLF_Global,TAR_Global,NEW_Global
    More_Global = More  # 是否使用全部特征绘图
    All_Global = All  # 是否导出charts
    CSV_Global = CSV  # 是否导出CSV
    CLF_Global = CLF  # 是否导出模型
    TAR_Global = TAR  # 是否打包tar
    NEW_Global = NEW  # 是否新建目录