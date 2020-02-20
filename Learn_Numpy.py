from pyecharts.components import Table as Table_Fisrt#绘制表格
from pyecharts import options as opts
from random import randint
from pyecharts.charts import *
from pyecharts.options.series_options import JsCode
from pandas import DataFrame,read_csv
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor,export_graphviz
from sklearn.ensemble import (RandomForestClassifier,RandomForestRegressor,GradientBoostingClassifier,
                              GradientBoostingRegressor)
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import *
from sklearn.preprocessing import *
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA, IncrementalPCA,KernelPCA,NMF
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC,SVR#SVC是svm分类，SVR是svm回归
from sklearn.neural_network import MLPClassifier,MLPRegressor
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN
from pyecharts.charts import *
# import sklearn as sk

#设置
np.set_printoptions(threshold=np.inf)
global_Set = dict(toolbox_opts=opts.ToolboxOpts(is_show=True),legend_opts=opts.LegendOpts(pos_bottom='3%',type_='scroll'))
global_Leg = dict(toolbox_opts=opts.ToolboxOpts(is_show=True),legend_opts=opts.LegendOpts(is_show=False))
Label_Set = dict(label_opts=opts.LabelOpts(is_show=False))

class Table(Table_Fisrt):
    def add(self, headers, rows, attributes = None):
        if len(rows) == 1:
            new_headers = ['数据类型','数据']
            new_rows = list(zip(headers,rows[0]))
            return super().add(new_headers,new_rows,attributes)
        else:
            return super().add(headers, rows, attributes)

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
        n_ra = x_range[0]
        if Type[0] == 1:
            ra = make_list(n_ra[0], n_ra[1], 70)
        else:
            ra = n_ra

        a = np.array([i for i in ra]).reshape(-1,1)
        y_data = Predict_Func(a)[0].tolist()
        value = [[0 , float(a[i]), y_data[i]] for i in range(len(a))]
        c = (HeatMap()
             .add_xaxis(['None'])
             .add_yaxis(f'数据', np.unique(a), value, **Label_Set)  # value的第一个数值是x
             .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Leg,
                              yaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),  # 'category'
                              xaxis_opts=opts.AxisOpts(is_scale=True, type_='category'),
                              visualmap_opts=opts.VisualMapOpts(is_show=True, max_=int(max(y_data)) + 1,
                                                                min_=int(min(y_data)),
                                                                pos_right='3%'))  # 显示
             )
        o_cList.append(c)
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

def Decision_boundary(x_range,x_means,Predict_Func,class_,Type):#绘制分类型预测图x-x热力图
    #r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调,class_是分类,add_o是可以合成的图
    # a-特征x，b-特征x-1，c-其他特征
    #规定，i-1是x轴，a是x轴，x_1是x轴
    class_dict = dict(zip(class_,[i for i in range(len(class_))]))
    v_dict = [{'min':-1.5,'max':-0.5,'label':'未知'}]#分段显示
    for i in class_dict:
        v_dict.append({'min':class_dict[i]-0.5,'max':class_dict[i]+0.5,'label':i})
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
    for i in range(len(x_means)):
        if i == 0:
            continue

        n_ra = x_range[i-1]
        Type_ra = Type[i-1]
        n_rb = x_range[i]
        Type_rb = Type[i]
        print(f'{n_ra},{n_rb}')
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

def line(w_sum,w,b):
    x = np.arange(-5, 5, 1)
    c = (
        Line()
            .add_xaxis(x.tolist())
            .set_global_opts(title_opts=opts.TitleOpts(title=f"系数w曲线"), **global_Set)
    )
    for i in range(len(w)):
        y = x * w[i] + b
        c.add_yaxis(f"系数w[{i}]", y.tolist(), is_smooth=True, **Label_Set)
    return c

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

def Training_visualization(x_trainData,class_,y):#根据不同类别绘制x-x分类散点图
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data,np.zeros(len(x_data[0]))])
    Cat = Categorical_Data()
    o_cList = []
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        x1_con = Cat(x1)

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
                                  yaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True))
                 )
            c.add_xaxis(x_2_new)
            if o_c == None:
                o_c = c
            else:
                o_c = o_c.overlap(c)
        o_cList.append(o_c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def Training_W(x_trainData,class_,y,w_list,b_list,means:list):#针对分类问题绘制决策边界
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data,np.zeros(len(x_data[0]))])
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
                              yaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True),
                              xaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True))
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
        x_data = np.array([x_data,np.zeros(len(x_data[0]))])
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
    Cat = Categorical_Data()
    o_cList = []
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        x1_con = Cat(x1)
        #不转换成list因为保持dtype的精度，否则绘图会出现各种问题(数值重复)
        c = (
            Scatter()
            .add_xaxis(x1)#研究表明，这个是横轴
            .add_yaxis('数据',y,**Label_Set)
             .set_global_opts(title_opts=opts.TitleOpts(title="预测类型图"),**global_Set,
                              yaxis_opts=opts.AxisOpts(type_='value' if y_con else None,is_scale=True),
                              xaxis_opts=opts.AxisOpts(type_='value' if x1_con else None,is_scale=True),
                              visualmap_opts=opts.VisualMapOpts(is_show=True, max_=int(y.max())+1, min_=int(y.min()),
                                                                pos_right='3%'))
        )
        o_cList.append(c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def Feature_visualization(x_trainData,data_name=''):#x-x数据图
    seeting = global_Set if data_name else global_Leg
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data,np.zeros(len(x_data[0]))])
    o_cList = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i: continue#重复内容，跳过
            x1 = x_data[i]  # x坐标
            x1_con = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_con = is_continuous(x2)
            x2_new = np.unique(x2)

            #x与散点图不同，这里是纵坐标
            c = (Scatter()
                 .add_xaxis(x2)
                 .add_yaxis(data_name, x1, **Label_Set)
                 .set_global_opts(title_opts=opts.TitleOpts(title=f'[{i}-{a}]数据散点图'), **seeting,
                                  yaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True))
                 )
            c.add_xaxis(x2_new)
            o_cList.append(c)
    return o_cList

def Feature_visualization_Format(x_trainData,data_name=''):#x-x数据图
    seeting = global_Set if data_name else global_Leg
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data,np.zeros(len(x_data[0]))])
    o_cList = []
    for i in range(len(x_data)):
        for a in range(len(x_data)):
            if a <= i: continue#重复内容，跳过
            x1 = x_data[i]  # x坐标
            x1_con = is_continuous(x1)
            x2 = x_data[a]  # y坐标
            x2_con = is_continuous(x2)
            x2_new = np.unique(x2)
            x1_list = x1.astype(np.str).tolist()
            for i in range(len(x1_list)):
                x1_list[i] = [x1_list[i],f'特征{i}']
            #x与散点图不同，这里是纵坐标
            c = (Scatter()
                 .add_xaxis(x2)
                 .add_yaxis(data_name, x1, **Label_Set)
                 .set_global_opts(title_opts=opts.TitleOpts(title=f'[{i}-{a}]数据散点图'), **seeting,
                                  yaxis_opts=opts.AxisOpts(type_='value' if x2_con else 'category',is_scale=True),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x1_con else 'category',is_scale=True),
                                  tooltip_opts=opts.TooltipOpts(is_show = True,axis_pointer_type = "cross",
                formatter=JsCode("function (params) {params.data[2];}")),)
                 )
            c.add_xaxis(x2_new)
            o_cList.append(c)
    return o_cList

def Discrete_Feature_visualization(x_trainData,data_name=''):#必定离散x-x数据图
    seeting = global_Set if data_name else global_Leg
    x_data = x_trainData.T
    if len(x_data) == 1:
        x_data = np.array([x_data,np.zeros(len(x_data[0]))])
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
        table = Table()
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
            if get.ndim == 1: get = np.expand_dims(get, axis=1)
            get = get.tolist()
            for i in range(len(get)):
                get[i] = [i+1] + get[i]
            headers = [i for i in range(len(get[0]))]
            table = Table()
            table.add(headers, get).set_global_opts(
                title_opts=opts.ComponentTitleOpts(title=f"表格:{name}", subtitle="CoTan~机器学习:查看数据"))
            tab.add(table, f'表格:{name}')
        tab.render(Dic)
        return Dic

class Study_MachineBase:
    def __init__(self,*args,**kwargs):
        self.Model = None
        self.have_Fit = False
        self.x_trainData = None
        self.y_trainData = None
        #记录这两个是为了克隆

    def Accuracy(self,y_Predict,y_Really):
        return accuracy_score(y_Predict, y_Really)

    def Fit(self,x_data,y_data,split=0.3,**kwargs):
        self.have_Fit = True
        y_data = y_data.ravel()
        self.x_trainData = x_data
        self.y_trainData = y_data
        x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=split)
        self.Model.fit(x_data,y_data)
        train_score = self.Model.score(x_train,y_train)
        test_score = self.Model.score(x_test,y_test)
        return train_score,test_score

    def Score(self,x_data,y_data):
        Score = self.Model.score(x_data,y_data)
        return Score

    def Predict(self,x_data):
        y_Predict = self.Model.predict(x_data)
        return y_Predict,'预测'

    def Des(self,*args,**kwargs):
        return ()

class prep_Base(Study_MachineBase):
    def __init__(self,*args,**kwargs):
        super(prep_Base, self).__init__(*args,**kwargs)
        self.Model = None

    def Fit(self, x_data,y_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.x_trainData = x_data
            self.y_trainData = y_data
            self.Model.fit(x_data,y_data)
        return 'None', 'None'

    def Predict(self, x_data):
        self.x_trainData = x_data
        x_Predict = self.Model.transform(x_data)
        self.y_trainData = x_Predict
        return x_Predict,'特征工程'

    def Score(self, x_data, y_data):
        return 'None' # 没有score

class Unsupervised(prep_Base):
    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.x_trainData = x_data
            self.y_trainData = None
            self.Model.fit(x_data)
        return 'None', 'None'

class UnsupervisedModel(prep_Base):
    def Fit(self, x_data, *args, **kwargs):
        self.x_trainData = x_data
        self.y_trainData = None
        self.Model.fit(x_data)
        return 'None', 'None'

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
        save = Dic + r'/render.HTML'
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

        columns = class_heard + ['截距b','C','最大迭代数']
        data = class_ + [b,c,max_iter]
        c = Table().add(headers=columns, rows=[data])
        tab.add(c, '数据表')
        c = Table().add(headers=[f'系数W[{i}]' for i in range(len(w_list[0]))], rows=w_list)
        tab.add(c, '系数数据表')

        save = Dic + r'/render.HTML'
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
        if self.Model_Name == 'Knn_class':
            class_ = self.Model.classes_.tolist()
            class_heard = [f'类别[{i}]' for i in range(len(class_))]

            get,x_means,x_range,Type = Training_visualization(x_data,class_,y)
            for i in range(len(get)):
                tab.add(get[i],f'{i}训练数据散点图')

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
                tab.add(get[i], f'{i}预测类型图')

            get = Prediction_boundary(x_range, x_means, self.Predict, Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')
            heard = [f'普适预测第{i}特征' for i in range(len(x_means))]
            data = [f'{i}' for i in x_means]
            c = Table().add(headers=heard, rows=[data])
            tab.add(c, '数据表')
        save = Dic + r'/render.HTML'
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
        tab.add(SeeTree(Dic + r"\Tree_Gra.dot"),'决策树可视化')

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

            tab.add(make_Tab(class_heard + [f'普适预测第{i}特征' for i in range(len(x_means))] + [f'特征{i}重要性' for i in range(len(importance))],
                             [class_ + [f'{i}' for i in x_means] + importance]), '数据表')
        else:
            get, x_means, x_range,Type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测类型图')

            get = Prediction_boundary(x_range, x_means, self.Predict, Type)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测热力图')

            tab.add(make_Tab([f'普适预测第{i}特征' for i in range(len(x_means))] + [f'特征{i}重要性' for i in range(len(importance))],
                             [[f'{i}' for i in x_means] + importance]), '数据表')
        save = Dic + r'/render.HTML'
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
        save = Dic + r'/render.HTML'
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
        save = Dic + r'/render.HTML'
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
        w_list = self.Model.coef_.tolist()
        b = self.Model.intercept_.tolist()
        class_ = self.Model.classes_.tolist()
        class_heard = [f'类别[{i}]' for i in range(len(class_))]

        y = self.y_trainData
        x_data = self.x_trainData
        get, x_means, x_range, Type = Training_visualization(x_data, class_, y)
        get_Line = Training_W(x_data, class_, y, w_list, b, x_means.copy())
        for i in range(len(get)):
            tab.add(get[i].overlap(get_Line[i]), f'{i}决策边界散点图')

        get = Decision_boundary(x_range, x_means, self.Predict, class_, Type)
        for i in range(len(get)):
            tab.add(get[i], f'{i}预测热力图')

        dic = {2:'离散',1:'连续'}
        tab.add(make_Tab(class_heard + [f'普适预测第{i}特征:{dic[Type[i]]}' for i in range(len(x_means))],
                         [class_ + [f'{i}' for i in x_means]]), '数据表')

        save = Dic + r'/render.HTML'
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

        tab.add(make_Tab([f'普适预测第{i}特征' for i in range(len(x_means))],[[f'{i}' for i in x_means]]), '数据表')
        save = Dic + r'/render.HTML'
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
        y_data = self.y_trainData
        if type(y_data) is np.ndarray:
            get = Feature_visualization(self.y_trainData)
            for i in range(len(get)):
                tab.add(get[i],f'[{i}]数据x-x散点图')

        c = (
            Bar()
                .add_xaxis([f'[{i}]特征' for i in range(len(var))])
                .add_yaxis('标准差', var.tolist(), **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title='系数w柱状图'), **global_Set)
        )
        tab.add(c,'数据标准差')
        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class SelectKBest_Model(prep_Base):#无监督
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

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class SelectFrom_Model(prep_Base):#无监督
    def __init__(self, args_use, Learner, *args, **kwargs):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SelectFrom_Model, self).__init__(*args, **kwargs)

        self.Model = Learner.Model
        self.Select_Model = SelectFromModel(estimator=Learner.Model,max_features=args_use['k'],prefit=Learner.have_Fit)
        self.max_features = args_use['k']
        self.estimator=Learner.Model
        self.k = {'max_features':args_use['k'],'estimator':Learner.Model,'have_Fit':Learner.have_Fit}
        self.have_Fit = Learner.have_Fit
        self.Model_Name = 'SelectFrom_Model'

    def Fit(self, x_data,y_data,split=0.3, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Select_Model.fit(x_data, y_data)
            return 'None', 'None'
        return 'NONE','NONE'

    def Predict(self, x_data):
        try:
            self.x_trainData = x_data
            x_Predict = self.Select_Model.transform(x_data)
            self.y_trainData = x_Predict
            print(self.y_trainData)
            print(self.x_trainData)
            return x_Predict,'模型特征工程'
        except:
            return np.array([]),'无结果工程'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        support = self.Select_Model.get_support()
        y_data = self.y_trainData
        x_data = self.x_trainData
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

        save = Dic + r'/render.HTML'
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
        y_data = self.y_trainData
        x_data = self.x_trainData
        var = self.Model.var_.tolist()
        means = self.Model.mean_.tolist()
        scale = self.Model.scale_.tolist()
        Conversion_control(y_data,x_data,tab)

        make_bar('标准差',var,tab)
        make_bar('方差',means,tab)
        make_bar('Scale',scale,tab)

        save = Dic + r'/render.HTML'
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
        y_data = self.y_trainData
        x_data = self.x_trainData
        scale = self.Model.scale_.tolist()
        max_ = self.Model.data_max_.tolist()
        min_ = self.Model.data_min_.tolist()
        Conversion_control(y_data,x_data,tab)
        make_bar('Scale',scale,tab)
        tab.add(make_Tab(heard= [f'[{i}]特征最大值' for i in range(len(max_))] + [f'[{i}]特征最小值' for i in range(len(min_))],
                         row=[max_ + min_]), '数据表格')

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class LogScaler_Model(prep_Base):#对数标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(LogScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'LogScaler'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.max_logx = np.log(x_data.max())
        return 'None', 'None'

    def Predict(self, x_data):
        try:
            max_logx = self.max_logx
        except:
            self.have_Fit = False
            self.Fit(x_data)
            max_logx = self.max_logx
        self.x_trainData = x_data.copy()
        x_Predict = (np.log(x_data)/max_logx)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'对数变换'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab(heard=['最大对数值(自然对数)'],row=[[str(self.max_logx)]]),'数据表格')

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class atanScaler_Model(prep_Base):#atan标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(atanScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'atanScaler'

    def Fit(self, x_data, *args, **kwargs):
        return 'None', 'None'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_Predict = (np.arctan(x_data)*(2/np.pi))
        self.y_trainData = x_Predict.copy()
        return x_Predict,'atan变换'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_control(y_data,x_data,tab)

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class decimalScaler_Model(prep_Base):#小数定标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(decimalScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'Decimal_normalization'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.j = max([judging_Digits(x_data.max()),judging_Digits(x_data.min())])
        return 'None', 'None'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        try:
            j = self.j
        except:
            self.have_Fit = False
            self.Fit(x_data)
            j = self.j
        x_Predict = (x_data/(10**j))
        self.y_trainData = x_Predict.copy()
        return x_Predict,'小数定标标准化'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        j = self.j
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab(heard=['小数位数:j'], row=[[j]]), '数据表格')

        save = Dic + r'/render.HTML'
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
        if not self.have_Fit:  # 不允许第二次训练
            self.max = x_data.max()
            self.min = x_data.min()
        return 'None', 'None'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        try:
            max = self.max
            min = self.min
        except:
            self.have_Fit = False
            self.Fit(x_data)
            max = self.max
            min = self.min
        x_Predict = (x_data * (self.feature_range[1] - self.feature_range[0])) / (max - min)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'映射标准化'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        max = self.max
        min = self.min
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab(heard=['最大值','最小值'], row=[[max,min]]), '数据表格')

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class sigmodScaler_Model(prep_Base):#sigmod变换
    def __init__(self, args_use, model, *args, **kwargs):
        super(sigmodScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'sigmodScaler_Model'

    def Fit(self, x_data, *args, **kwargs):
        return 'None', 'None'

    def Predict(self, x_data:np.array):
        self.x_trainData = x_data.copy()
        x_Predict = (1/(1+np.exp(-x_data)))
        self.y_trainData = x_Predict.copy()
        return x_Predict,'Sigmod变换'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_control(y_data,x_data,tab)

        save = Dic + r'/render.HTML'
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
        if not self.have_Fit:  # 不允许第二次训练
            self.max = x_data.max()
            self.min = x_data.min()
        return 'None', 'None'

    def Predict(self, x_data,*args,**kwargs):
        self.y_trainData = x_data.copy()
        try:
            max = self.max
            min = self.min
        except:
            self.have_Fit = False
            self.Fit(x_data)
            max = self.max
            min = self.min
        x_Predict = 1 / 2 + (1 / 2) * np.sin(np.pi / (max - min) * (x_data - (max-min) / 2))
        self.y_trainData = x_Predict.copy()
        return x_Predict,'映射标准化'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        max = self.max
        min = self.min
        Conversion_control(y_data,x_data,tab)
        tab.add(make_Tab(heard=['最大值','最小值'], row=[[max,min]]), '数据表格')

        save = Dic + r'/render.HTML'
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
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_control(y_data,x_data,tab)

        save = Dic + r'/render.HTML'
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
        y_data = self.y_trainData
        get_y = Discrete_Feature_visualization(y_data,'转换数据')#转换
        for i in range(len(get_y)):
            tab.add(get_y[i],f'[{i}]数据x-x离散散点图')
        save = Dic + r'/render.HTML'
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
        return 'None','None'

    def Predict(self,x_data):
        self.x_trainData = x_data.copy()
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
        self.y_trainData = x_Predict.copy()
        return x_Predict,f'{len(bool_list)}值离散化'

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        y_data = self.y_trainData
        get_y = Discrete_Feature_visualization(y_data, '转换数据')  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f'[{i}]数据x-x离散散点图')
        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Label_Model(prep_Base):#数字编码
    def __init__(self, args_use, model, *args, **kwargs):
        super(Label_Model, self).__init__(*args, **kwargs)
        self.Model = []
        self.k = {}
        self.Model_Name = 'LabelEncoder'

    def Fit(self,x_data,*args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            if x_data.ndim == 1:x_data = np.array([x_data])
            for i in range(x_data.shape[1]):
                self.Model.append(LabelEncoder().fit(np.ravel(x_data[:,i])))#训练机器
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = x_data.copy()
        if x_data.ndim == 1: x_data = np.array([x_data])
        for i in range(x_data.shape[1]):
            x_Predict[:,i] = self.Model[i].transform(x_data[:,i])
        self.y_trainData = x_Predict.copy()
        return x_Predict,'数字编码'

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        y_data = self.y_trainData
        get_y = Discrete_Feature_visualization(y_data, '转换数据')  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f'[{i}]数据x-x离散散点图')
        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class OneHotEncoder_Model(prep_Base):#独热编码
    def __init__(self, args_use, model, *args, **kwargs):
        super(OneHotEncoder_Model, self).__init__(*args, **kwargs)
        self.Model = []

        self.ndim_up = args_use['ndim_up']
        self.k = {}
        self.Model_Name = 'OneHotEncoder'

    def Fit(self,x_data,*args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            if x_data.ndim == 1:x_data = [x_data]
            for i in range(x_data.shape[1]):
                data = np.expand_dims(x_data[:,i], axis=1)#独热编码需要升维
                self.Model.append(OneHotEncoder().fit(data))#训练机器
        return 'None', 'None'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_new = []
        for i in range(x_data.shape[1]):
            data = np.expand_dims(x_data[:, i], axis=1)  # 独热编码需要升维
            oneHot = self.Model[i].transform(data).toarray().tolist()
            x_new.append(oneHot)#添加到列表中
        x_new = DataFrame(x_new).to_numpy()#新列表的行数据是原data列数据的独热码(只需要ndim=2，暂时没想到numpy的做法)
        x_Predict = []
        for i in range(x_new.shape[1]):
            x_Predict.append(x_new[:,i])
        x_Predict = np.array(x_Predict)#转换回array
        if not self.ndim_up:#压缩操作
            new_xPredict = []
            for i in x_Predict:
                new_list = []
                list_ = i.tolist()
                for a in list_:
                    new_list += a
                new = np.array(new_list)
                new_xPredict.append(new)
            self.y_trainData = x_Predict.copy()
            return np.array(new_xPredict),'独热编码'
        #不保存y_trainData
        return x_Predict,'独热编码'#不需要降维

    def Des(self, Dic, *args, **kwargs):
        tab = Tab()
        y_data = self.y_trainData
        get_y = Discrete_Feature_visualization(y_data, '转换数据')  # 转换
        for i in range(len(get_y)):
            tab.add(get_y[i], f'[{i}]数据x-x离散散点图')
        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class Missed_Model(Unsupervised):#缺失数据补充
    def __init__(self, args_use, model, *args, **kwargs):
        super(Missed_Model, self).__init__(*args, **kwargs)
        self.Model = SimpleImputer(missing_values=args_use['miss_value'], strategy=args_use['fill_method'],
                                   fill_value=args_use['fill_value'])

        self.k = {}
        self.Model_Name = 'Missed'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'填充缺失'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_control(y_data,x_data,tab)

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class PCA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(PCA_Model, self).__init__(*args, **kwargs)
        self.Model = PCA(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components']}
        self.Model_Name = 'PCA'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'PCA'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_Separate_Format(y_data,tab)

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class RPCA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(RPCA_Model, self).__init__(*args, **kwargs)
        self.Model = IncrementalPCA(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components': args_use['n_components']}
        self.Model_Name = 'RPCA'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'RPCA'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_Separate_Format(y_data,tab)

        save = Dic + r'/render.HTML'
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

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'KPCA'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_Separate_Format(y_data,tab)

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

class LDA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(LDA_Model, self).__init__(*args, **kwargs)
        self.Model = LDA(n_components=args_use['n_components'])
        self.n_components = args_use['n_components']
        self.k = {'n_components': args_use['n_components']}
        self.Model_Name = 'LDA'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'LDA'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_Separate_Format(y_data,tab)

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

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_Predict = self.Model.transform(x_data)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'NMF'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_Separate_Format(y_data,tab)

        save = Dic + r'/render.HTML'
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
        return 'None', 'None'

    def Predict(self, x_data):
        self.x_trainData = x_data.copy()
        x_Predict = self.Model.fit_transform(x_data)
        self.y_trainData = x_Predict.copy()
        return x_Predict,'SNE'

    def Des(self,Dic,*args,**kwargs):
        tab = Tab()
        y_data = self.y_trainData
        x_data = self.x_trainData
        Conversion_Separate_Format(y_data,tab)

        save = Dic + r'/render.HTML'
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

class kmeans_Model(UnsupervisedModel):
    def __init__(self, args_use, model, *args, **kwargs):
        super(kmeans_Model, self).__init__(*args, **kwargs)
        self.Model = KMeans(n_clusters=args_use['n_clusters'])

        self.n_clusters = args_use['n_clusters']
        self.k = {'n_clusters':args_use['n_clusters']}
        self.Model_Name = 'k-means'

    def Predict(self, x_data):
        y_Predict = self.Model.predict(x_data)
        return y_Predict,'k-means'

class Agglomerative_Model(UnsupervisedModel):
    def __init__(self, args_use, model, *args, **kwargs):
        super(Agglomerative_Model, self).__init__(*args, **kwargs)
        self.Model = AgglomerativeClustering(n_clusters=args_use['n_clusters'])#默认为2，不同于k-means

        self.n_clusters = args_use['n_clusters']
        self.k = {'n_clusters':args_use['n_clusters']}
        self.Model_Name = 'Agglomerative'

    def Predict(self, x_data):
        y_Predict = self.Model.fit_predict(x_data)
        return y_Predict,'Agglomerative'

class DBSCAN_Model(UnsupervisedModel):
    def __init__(self, args_use, model, *args, **kwargs):
        super(DBSCAN_Model, self).__init__(*args, **kwargs)
        self.Model = DBSCAN(eps = args_use['eps'], min_samples = args_use['min_samples'])
        #eps是距离(0.5)，min_samples(5)是簇与噪音分界线(每个簇最小元素数)
        # min_samples
        self.eps = args_use['eps']
        self.min_samples = args_use['min_samples']
        self.k = {'min_samples':args_use['min_samples'],'eps':args_use['eps']}
        self.Model_Name = 'DBSCAN'

    def Predict(self, x_data):
        y_Predict = self.Model.fit_predict(x_data)
        return y_Predict,'DBSCAN'

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

        args_use['ndim_up'] = bool(args.get('ndim_up', True))
        args_use['miss_value'] = args.get('miss_value',np.nan)
        args_use['fill_method'] = args.get('fill_method','mean')
        args_use['fill_value'] = args.get('fill_value',None)

        args_use['n_components'] = args.get('n_components',1)
        args_use['kernel'] = args.get('kernel','rbf' if Type in ('SVR','SVR') else 'linear')

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
        return args_use

    def Add_Learner(self,Learner,Text=''):
        get = self.Learn_Dic[Learner]
        name = f'Le[{len(self.Learner)}]{Learner}'
        #参数调节
        args_use = self.p_Args(Text,Learner)
        #生成学习器
        self.Learner[name] = get(model=Learner,args_use=args_use)
        self.Learner_Type[name] = Learner

    def Add_SelectFrom_Model(self,Learner,Text=''):#Learner代表选中的学习器
        model = self.get_Learner(Learner)
        name = f'Le[{len(self.Learner)}]SelectFrom_Model:{Learner}'
        #参数调节
        args_use = self.p_Args(Text,'SelectFrom_Model')
        #生成学习器
        self.Learner[name] = SelectFrom_Model(Learner=model,args_use=args_use,Dic=self.Learn_Dic)
        self.Learner_Type[name] = 'SelectFrom_Model'

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
        return model.Fit(x_data,y_data,split)

    def Predict(self,x_name,Learner,Text='',**kwargs):
        x_data = self.get_Sheet(x_name)
        model = self.get_Learner(Learner)
        y_data,name = model.Predict(x_data)
        self.Add_Form(y_data,f'{x_name}:{name}')
        return y_data

    def Score(self,name_x,name_y,Learner):#Score_Only表示仅评分 Fit_Simp 是普遍类操作
        model = self.get_Learner(Learner)
        x = self.get_Sheet(name_x)
        y = self.get_Sheet(name_y)
        return model.Score(x,y)

    def Show_Args(self,Learner,Dic):#显示参数
        model = self.get_Learner(Learner)
        return model.Des(Dic)

    def Del_Leaner(self,Leaner):
        del self.Learner[Leaner]
        del self.Learner_Type[Leaner]
