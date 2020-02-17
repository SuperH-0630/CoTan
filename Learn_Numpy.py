from pyecharts.components import Table #绘制表格
from pyecharts import options as opts
from random import randint
from pyecharts.charts import *
from pandas import DataFrame,read_csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
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
Label_Set = dict(label_opts=opts.LabelOpts(is_show=False))

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
        self.x_trainData = x_data
        self.y_train = y_data
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data,y_data)
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'特征工程'

    def Score(self, x_data, y_data):
        return 'None' # 没有score

class Unsupervised(prep_Base):
    def Fit(self, x_data, *args, **kwargs):
        self.x_trainData = x_data
        self.y_train = None
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data)
        return 'None', 'None'

class UnsupervisedModel(prep_Base):
    def Fit(self, x_data, *args, **kwargs):
        self.x_trainData = x_data
        self.y_train = None
        self.Model.fit(x_data)
        return 'None', 'None'

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
        y = x * w[i] + (w[i] / w_sum) * b
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
        b = (
            Scatter()
                .add_xaxis(x.tolist())
                .add_yaxis(f'{i}特征', y, **Label_Set)
                .set_global_opts(title_opts=opts.TitleOpts(title='类型划分图'), **global_Set)
        )
        b.overlap(c)
        re.append(b)
    return re

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

    def Des(self,Dic='render.html',*args,**kwargs):
        #获取数据
        w = self.Model.coef_.tolist()#变为表格
        w_sum = self.Model.coef_.sum()
        w_heard = [f'系数w[{i}]' for i in range(len(w))]
        b = self.Model.intercept_
        tab = Tab()

        tab.add(scatter(w_heard,w),'系数w散点图')
        tab.add(bar(w_heard,self.Model.coef_),'系数柱状图')
        tab.add(line(w_sum,w,b), '系数w曲线')

        re = see_Line(self.x_trainData,self.y_trainData,w,w_sum,b)
        for i in range(len(re)):
            tab.add(re[i], f'{i}预测分类类表')

        columns = w_heard + ['截距b']
        data = w + [b]
        if self.Model_Name != 'Line':
            columns += ['阿尔法','最大迭代次数']
            data += [self.Model.alpha,self.Model.max_iter]
        c = Table().add(headers=columns,rows=[data])
        tab.add(c, '数据表')

        save = Dic + r'/render.HTML'
        tab.render(save)#生成HTML
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

        for i in range(len(w_list)):
            w = w_list[i]
            w_sum = self.Model.coef_.sum()
            w_heard = [f'系数w[{i},{j}]' for j in range(len(w))]
            tab.add(scatter(w_heard, w), '系数w散点图')
            tab.add(bar(w_heard, w_array[i]), '系数柱状图')
            tab.add(line(w_sum, w, b), '系数w曲线')

        columns = class_heard + ['截距b','C','最大迭代数']
        data = class_ + [b,c,max_iter]
        c = Table().add(headers=columns, rows=[data])
        tab.add(c, '数据表')
        c = Table().add(headers=[f'系数W[{i}]' for i in range(len(w_list[0]))], rows=w_list)
        tab.add(c, '系数数据表')

        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

def get_Color():
    # 随机颜色，雷达图默认非随机颜色
    rgb = [randint(0, 255), randint(0, 255), randint(0, 255)]
    color = '#'
    for a in rgb:
        color += str(hex(a))[-2:].replace('x', '0').upper()  # 转换为16进制,upper表示小写(规范化)
    return color

def is_continuous(data:np.array,f:float=0.1):
    data = data.tolist()
    l = list(set(data))
    re = len(l)/len(data)>=f or len(data) <= 3
    return re

class Categorical_Data:
    def __init__(self):
        self.x_means = []
        self.x_range = []
        self.Type = []
        # self.min_max = [0,None]

    def __call__(self,x1, *args, **kwargs):
        return self.is_continuous(x1)

    def is_continuous(self,x1:np.array):
        try:
            x1_con = is_continuous(x1)
            if x1_con:
                self.x_means.append(np.mean(x1))
                self.add_Range(x1)
            else:
                self.x_means.append(np.median(x1))
                self.add_Range(x1,False)
            return x1_con
        except:
            self.add_Range(x1,False)
            return False

    def add_Range(self,x1:np.array,range_=True):
        try:
            if not range_ : raise Exception
            min_ = int(x1.min())
            max_ = int(x1.max())
            #不需要复制列表
            # if self.min_max[0] > min_:self.min_max[0] = min_
            # if self.min_max[1] < max_:self.min_max[1] = max_
            # self.x_range.append(self.min_max)
            self.x_range.append([min(min_,0),max_])
            self.Type.append(1)
        except:
            self.x_range.append(np.array.tolist())
            self.Type.append(2)

    def get(self):
        return self.x_means,self.x_range,self.Type

def Training_visualization(x_trainData,class_,y):
    x_data = x_trainData.T
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
            x_2 = x2[y == n_class].tolist()
            c = (Scatter()
                 .add_xaxis(x_1)
                 .add_yaxis(f'{n_class}', x_2, **Label_Set)
                 .set_global_opts(title_opts=opts.TitleOpts(title='系数w散点图'), **global_Set,
                                  yaxis_opts=opts.AxisOpts(type_='value' if x2_con else None,axisline_opts=opts.AxisLineOpts(is_on_zero=False)),
                                  xaxis_opts=opts.AxisOpts(type_='value' if x1_con else None,axisline_opts=opts.AxisLineOpts(is_on_zero=False))))
            if o_c == None:
                o_c = c
            else:
                o_c = o_c.overlap(c)
        o_cList.append(o_c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

def regress_visualization(x_trainData,y):
    x_data = x_trainData.T
    Cat = Categorical_Data()
    o_cList = []
    for i in range(len(x_data)):
        x1 = x_data[i]  # x坐标
        x1_con = Cat(x1)

        if i == 0:continue

        print(f'类型{i}:\n{x1_con}x1=\n{x1}')
        x2 = x_data[i - 1]  # y坐标
        x2_con = is_continuous(x2)
        print(f'\n{x2_con}x2=\n{x2}')
        value = [[x1[i],x2[i],y[i]] for i in range(len(x1))]
        value = sorted(value,key=lambda y:y[1])
        value = sorted(value,key=lambda y:y[0])#两次排序
        c = (
            HeatMap()
            .add_xaxis(x1)
            .add_yaxis('数据',x2,value)
             .set_global_opts(title_opts=opts.TitleOpts(title="预测热点图"),visualmap_opts=opts.VisualMapOpts(max_=y.max(),min_=y.min()),
                                      **global_Set,yaxis_opts=opts.AxisOpts(type_='category'),
                                      xaxis_opts=opts.AxisOpts(type_='category'))
        )
        o_cList.append(c)
    means,x_range,Type = Cat.get()
    return o_cList,means,x_range,Type

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
                tab.add(get[i],f'{i}类型图')

            get = Decision_boundary(x_range,x_means,self.Predict,class_,Type,get)
            for i in range(len(get)):
                tab.add(get[i], f'{i}预测类型图')

            # c = Table().add(headers=class_heard, rows=class_)
            # tab.add(c, '数据表')
        else:
            get, x_means, x_range,Type = regress_visualization(x_data, y)
            for i in range(len(get)):
                tab.add(get[i], f'{i}类型图')
        save = Dic + r'/render.HTML'
        tab.render(save)  # 生成HTML
        return save,

def Prediction_boundary(r,x_means,Predict_Func):
    #r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调,class_是分类
    # a-特征x，b-特征x-1，c-其他特征
    a = np.array([i for i in r for _ in r]).T
    b = np.array([i for _ in r for i in r]).T
    data_c = np.array([x_means for _ in r for i in r])
    o_cList = []
    for i in range(data_c.shape[1]):
        if i == 0:
            continue
        data = data_c.copy()
        data[:, i - 1] = a
        data[:, i] = b
        y_data = Predict_Func(data)[0]
        value = [[a[i], b[i], y_data[i]] for i in range(len(a))]
        a_con = is_continuous(a)
        b_con = is_continuous(b)
        c = (
            HeatMap()
                .add_xaxis(a)
                .add_yaxis('数据', b, value)
                .set_global_opts(title_opts=opts.TitleOpts(title="预测热点图"), visualmap_opts=opts.VisualMapOpts(max_=y_data.max(),min_=y_data.min()),
                                 **global_Set, yaxis_opts=opts.AxisOpts(type_='value' if b_con else None),
                                 xaxis_opts=opts.AxisOpts(type_='value' if a_con else None))
        )
        o_cList.append(c)
    return o_cList

def Decision_boundary(x_range,x_means,Predict_Func,class_,Type,add_o):
    #r是绘图大小列表,x_means是其余值,Predict_Func是预测方法回调,class_是分类,add_o是可以合成的图
    # a-特征x，b-特征x-1，c-其他特征
    #规定，i-1是x轴，a是x轴，x_1是x轴
    class_dict = dict(zip(class_,[i for i in range(len(class_))]))
    o_cList = []
    for i in range(len(x_means)):
        if i == 0:
            continue

        n_ra = x_range[i-1]
        Type_ra = Type[i-1]
        n_rb = x_range[i]
        Type_rb = Type[i]
        print(f'{n_ra},{n_rb}')
        if Type_ra == 1:
            n = int(35 / (n_ra[1] - n_ra[0]))
            ra = [i / n for i in range(n_ra[0] * n, n_ra[1] * n)]
        else:
            ra = n_ra

        if Type_rb == 1:
            n = int(35 / (n_rb[1] - n_rb[0]))
            rb = [i / n for i in range(n_rb[0] * n, n_rb[1] * n)]
        else:
            rb = n_rb
        a = np.array([i for i in ra for _ in rb]).T
        b = np.array([i for _ in ra for i in rb]).T
        data_c = np.array([x_means for _ in ra for i in rb])
        data = data_c.copy()
        data[:, i - 1] = a
        data[:, i] = b
        y_data = Predict_Func(data)[0].tolist()
        value = [[a[i], b[i], class_dict.get(y_data[i],-1)] for i in range(len(a))]
        c = (HeatMap()
             .add_xaxis(a)
             .add_yaxis(f'数据', b, value, **Label_Set)#value的第一个数值是x
             .set_global_opts(title_opts=opts.TitleOpts(title='预测热力图'), **global_Set,
                              yaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_on_zero=False),type_='category'),
                              xaxis_opts=opts.AxisOpts(axisline_opts=opts.AxisLineOpts(is_on_zero=False),type_='category')
                              ,visualmap_opts=opts.VisualMapOpts(is_show=False,max_=max(class_dict.values()),min_=-1))
             )
        try:
            c.overlap(add_o[i])
        except:pass
        o_cList.append(c)
    return o_cList

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

class GradientTree_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(GradientTree_Model, self).__init__(*args,**kwargs)
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

class Variance_Model(Unsupervised):#无监督
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(Variance_Model, self).__init__(*args,**kwargs)
        self.Model = VarianceThreshold(threshold=(args_use['P'] * (1 - args_use['P'])))
        #记录这两个是为了克隆
        self.threshold = args_use['P']
        self.k = {'threshold':args_use['P']}
        self.Model_Name = model

class SelectKBest_Model(prep_Base):#有监督
    def __init__(self, args_use, model, *args, **kwargs):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SelectKBest_Model, self).__init__(*args, **kwargs)
        self.Model = SelectKBest(k=args_use['k'],score_func=args_use['score_func'])
        # 记录这两个是为了克隆
        self.k_ = args_use['k']
        self.score_func=args_use['score_func']
        self.k = {'k':args_use['k'],'score_func':args_use['score_func']}
        self.Model_Name = model

class SelectFrom_Model(prep_Base):#有监督
    def __init__(self, args_use, Learner, *args, **kwargs):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SelectFrom_Model, self).__init__(*args, **kwargs)

        self.Model = Learner.Model
        self.Select_Model = SelectFromModel(estimator=Learner.Model,max_features=args_use['k'],prefit=Learner.have_Fit)

        self.max_features = args_use['k']
        self.estimator=Learner.Model
        self.k = {'max_features':args_use['k'],'estimator':Learner.Model}
        self.Model_Name = 'SelectFrom_Model'

    def Predict(self, x_data):
        try:
            x_Predict = self.Select_Model.transform(x_data)
            return x_Predict,'模型特征工程'
        except:
            return np.array([]),'无结果工程'

class Standardization_Model(Unsupervised):#z-score标准化 无监督
    def __init__(self, args_use, model, *args, **kwargs):
        super(Standardization_Model, self).__init__(*args, **kwargs)
        self.Model = StandardScaler()

        self.k = {}
        self.Model_Name = 'StandardScaler'

class MinMaxScaler_Model(Unsupervised):#离差标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(MinMaxScaler_Model, self).__init__(*args, **kwargs)
        self.Model = MinMaxScaler(feature_range=args_use['feature_range'])

        self.k = {}
        self.Model_Name = 'MinMaxScaler'

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
        x_Predict = (np.log(x_data)/max_logx)
        return x_Predict,'对数变换'

class atanScaler_Model(prep_Base):#atan标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(atanScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'atanScaler'

    def Fit(self, x_data, *args, **kwargs):
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = (np.arctan(x_data)*(2/np.pi))
        return x_Predict,'atan变换'

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
        try:
            j = self.j
        except:
            self.have_Fit = False
            self.Fit(x_data)
            j = self.j
        x_Predict = (x_data/(10**j))
        return x_Predict,'小数定标标准化'

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
        try:
            max = self.max
            min = self.min
        except:
            self.have_Fit = False
            self.Fit(x_data)
            max = self.max
            min = self.min
        x_Predict = (x_data * (self.feature_range[1] - self.feature_range[0])) / (max - min)
        return x_Predict,'映射标准化'

class sigmodScaler_Model(prep_Base):#sigmod变换
    def __init__(self, args_use, model, *args, **kwargs):
        super(sigmodScaler_Model, self).__init__(*args, **kwargs)
        self.Model = None

        self.k = {}
        self.Model_Name = 'sigmodScaler_Model'

    def Fit(self, x_data, *args, **kwargs):
        return 'None', 'None'

    def Predict(self, x_data:np.array):
        x_Predict = (1/(1+np.exp(-x_data)))
        return x_Predict,'Sigmod变换'

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
        try:
            max = self.max
            min = self.min
        except:
            self.have_Fit = False
            self.Fit(x_data)
            max = self.max
            min = self.min
        x_Predict = 1 / 2 + (1 / 2) * np.sin(np.pi / (max - min) * (x_data - (max-min) / 2))
        return x_Predict,'映射标准化'

class Regularization_Model(Unsupervised):#正则化
    def __init__(self, args_use, model, *args, **kwargs):
        super(Regularization_Model, self).__init__(*args, **kwargs)
        self.Model = Normalizer(norm=args_use['norm'])

        self.k = {'norm':args_use['norm']}
        self.Model_Name = 'Regularization'

class Binarizer_Model(Unsupervised):#二值化
    def __init__(self, args_use, model, *args, **kwargs):
        super(Binarizer_Model, self).__init__(*args, **kwargs)
        self.Model = Binarizer(threshold=args_use['threshold'])

        self.k = {}
        self.Model_Name = 'Binarizer'

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
        return x_Predict,f'{len(bool_list)}值离散化'

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
        return x_Predict,'数字编码'

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
        x_new = []
        for i in range(x_data.shape[1]):
            data = np.expand_dims(x_data[:, i], axis=1)  # 独热编码需要升维
            oneHot = self.Model[i].transform(data).toarray().tolist()
            print(len(oneHot),oneHot)
            x_new.append(oneHot)#添加到列表中
        x_new = DataFrame(x_new).to_numpy()#新列表的行数据是原data列数据的独热码(只需要ndim=2，暂时没想到numpy的做法)
        x_Predict = []
        for i in range(x_new.shape[1]):
            x_Predict.append(x_new[:,i])
        x_Predict = np.array(x_Predict)#转换回array
        if not self.ndim_up:#需要降维操作
            print('Q')
            new_xPredict = []
            for i in x_Predict:
                new_list = []
                list_ = i.tolist()
                for a in list_:
                    new_list += a
                new = np.array(new_list)
                new_xPredict.append(new)
            return np.array(new_xPredict),'独热编码'
        return x_Predict,'独热编码'#不需要降维

class Missed_Model(Unsupervised):#缺失数据补充
    def __init__(self, args_use, model, *args, **kwargs):
        super(Missed_Model, self).__init__(*args, **kwargs)
        self.Model = SimpleImputer(missing_values=args_use['miss_value'], strategy=args_use['fill_method'],
                                   fill_value=args_use['fill_value'])

        self.k = {}
        self.Model_Name = 'Missed'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'填充缺失'

class PCA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(PCA_Model, self).__init__(*args, **kwargs)
        self.Model = PCA(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components']}
        self.Model_Name = 'PCA'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'PCA'

class RPCA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(RPCA_Model, self).__init__(*args, **kwargs)
        self.Model = IncrementalPCA(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components': args_use['n_components']}
        self.Model_Name = 'RPCA'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'RPCA'

class KPCA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(KPCA_Model, self).__init__(*args, **kwargs)
        self.Model = KernelPCA(n_components=args_use['n_components'], kernel=args_use['kernel'])
        self.n_components = args_use['n_components']
        self.kernel = args_use['kernel']
        self.k = {'n_components': args_use['n_components'],'kernel':args_use['kernel']}
        self.Model_Name = 'KPCA'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'KPCA'

class LDA_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(LDA_Model, self).__init__(*args, **kwargs)
        self.Model = LDA(n_components=args_use['n_components'])
        self.n_components = args_use['n_components']
        self.k = {'n_components': args_use['n_components']}
        self.Model_Name = 'LDA'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'LDA'

class NMF_Model(Unsupervised):
    def __init__(self, args_use, model, *args, **kwargs):
        super(NMF_Model, self).__init__(*args, **kwargs)
        self.Model = NMF(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components']}
        self.Model_Name = 'NFM'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'NMF'

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
        x_Predict = self.Model.fit_transform(x_data)
        return x_Predict,'SNE'

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
        name = f'Le[{len(self.Learner)}]SelectFrom_Model'
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

def judging_Digits(num:(int,float)):
    a = str(abs(num)).split('.')[0]
    if a == '':raise ValueError
    return len(a)