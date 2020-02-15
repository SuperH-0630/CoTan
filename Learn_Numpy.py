from pyecharts.components import Table #绘制表格
from pyecharts import options as opts
from pyecharts.charts import Tab,Page
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
# import sklearn as sk


#设置
np.set_printoptions(threshold=np.inf)

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
        #记录这两个是为了克隆

    def Accuracy(self,y_Predict,y_Really):
        return accuracy_score(y_Predict, y_Really)

    def Fit(self,x_data,y_data,split=0.3,**kwargs):
        self.have_Fit = True
        y_data = y_data.ravel()
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

class prep_Base(Study_MachineBase):
    def __init__(self,*args,**kwargs):
        super(prep_Base, self).__init__(*args,**kwargs)
        self.Model = None

    def Fit(self, x_data,y_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data,y_data)
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'特征工程'

    def Score(self, x_data, y_data):
        return 'None'  # 没有score

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

class LogisticRegression_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(LogisticRegression_Model, self).__init__(*args,**kwargs)
        self.Model = LogisticRegression(C=args_use['C'],max_iter=args_use['max_iter'])
        #记录这两个是为了克隆
        self.C = args_use['C']
        self.max_iter = args_use['max_iter']
        self.k = {'C':args_use['C'],'max_iter':args_use['max_iter']}
        self.Model_Name = model

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

class Variance_Model(prep_Base):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
        super(Variance_Model, self).__init__(*args,**kwargs)
        self.Model = VarianceThreshold(threshold=(args_use['P'] * (1 - args_use['P'])))
        #记录这两个是为了克隆
        self.threshold = args_use['P']
        self.k = {'threshold':args_use['P']}
        self.Model_Name = model

class SelectKBest_Model(prep_Base):
    def __init__(self, args_use, model, *args, **kwargs):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SelectKBest_Model, self).__init__(*args, **kwargs)
        self.Model = SelectKBest(k=args_use['k'],score_func=args_use['score_func'])
        # 记录这两个是为了克隆
        self.k_ = args_use['k']
        self.score_func=args_use['score_func']
        self.k = {'k':args_use['k'],'score_func':args_use['score_func']}
        self.Model_Name = model

class SelectFrom_Model(prep_Base):
    def __init__(self, args_use, Learner, *args, **kwargs):  # model表示当前选用的模型类型,Alpha针对正则化的参数
        super(SelectFrom_Model, self).__init__(*args, **kwargs)

        self.Model = Learner.Model
        self.Select_Model = SelectFromModel(estimator=Learner.Model,max_features=args_use['k'],prefit=Learner.have_Fit)

        self.max_features = args_use['k']
        self.estimator=Learner.Model
        self.k = {'max_features':args_use['k'],'estimator':Learner.Model}
        self.Model_Name = 'SelectFrom_Model'

    def Fit(self, x_data,y_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Select_Model.fit(x_data,y_data)
        return 'None', 'None'

    def Predict(self, x_data):
        try:
            x_Predict = self.Select_Model.transform(x_data)
            return x_Predict,'模型特征工程'
        except:
            return np.array([]),'无结果工程'

class Standardization_Model(prep_Base):#z-score标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(Standardization_Model, self).__init__(*args, **kwargs)
        self.Model = StandardScaler()

        self.k = {}
        self.Model_Name = 'StandardScaler'

class MinMaxScaler_Model(prep_Base):#离差标准化
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

class atanScaler_Model(prep_Base):#对数标准化
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

class Regularization_Model(prep_Base):#离差标准化
    def __init__(self, args_use, model, *args, **kwargs):
        super(Regularization_Model, self).__init__(*args, **kwargs)
        self.Model = Normalizer(norm=args_use['norm'])

        self.k = {'norm':args_use['norm']}
        self.Model_Name = 'Regularization'

class Binarizer_Model(prep_Base):#二值化
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

class Missed_Model(prep_Base):#缺失数据补充
    def __init__(self, args_use, model, *args, **kwargs):
        super(Missed_Model, self).__init__(*args, **kwargs)
        self.Model = SimpleImputer(missing_values=args_use['miss_value'], strategy=args_use['fill_method'],
                                   fill_value=args_use['fill_value'])

        self.k = {}
        self.Model_Name = 'Missed'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data)
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'填充缺失'

class PCA_Model(prep_Base):
    def __init__(self, args_use, model, *args, **kwargs):
        super(PCA_Model, self).__init__(*args, **kwargs)
        self.Model = PCA(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components']}
        self.Model_Name = 'PCA'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data)
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'PCA'

class RPCA_Model(prep_Base):
    def __init__(self, args_use, model, *args, **kwargs):
        super(RPCA_Model, self).__init__(*args, **kwargs)
        self.Model = IncrementalPCA(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components': args_use['n_components']}
        self.Model_Name = 'RPCA'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data)
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'RPCA'

class KPCA_Model(prep_Base):
    def __init__(self, args_use, model, *args, **kwargs):
        super(KPCA_Model, self).__init__(*args, **kwargs)
        self.Model = KernelPCA(n_components=args_use['n_components'], kernel=args_use['kernel'])
        self.n_components = args_use['n_components']
        self.kernel = args_use['kernel']
        self.k = {'n_components': args_use['n_components'],'kernel':args_use['kernel']}
        self.Model_Name = 'KPCA'

    def Fit(self, x_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data)
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'KPCA'

class LDA_Model(prep_Base):
    def __init__(self, args_use, model, *args, **kwargs):
        super(LDA_Model, self).__init__(*args, **kwargs)
        self.Model = LDA(n_components=args_use['n_components'])
        self.n_components = args_use['n_components']
        self.k = {'n_components': args_use['n_components']}
        self.Model_Name = 'LDA'

    def Fit(self, x_data,y_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data,y_data)
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'LDA'

class NMF_Model(prep_Base):
    def __init__(self, args_use, model, *args, **kwargs):
        super(NMF_Model, self).__init__(*args, **kwargs)
        self.Model = NMF(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components']}
        self.Model_Name = 'NFM'

    def Fit(self, x_data,y_data, *args, **kwargs):
        if not self.have_Fit:  # 不允许第二次训练
            self.Model.fit(x_data,y_data)
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.transform(x_data)
        return x_Predict,'NMF'

class TSNE_Model(prep_Base):
    def __init__(self, args_use, model, *args, **kwargs):
        super(TSNE_Model, self).__init__(*args, **kwargs)
        self.Model = TSNE(n_components=args_use['n_components'])

        self.n_components = args_use['n_components']
        self.k = {'n_components':args_use['n_components']}
        self.Model_Name = 't-SNE'

    def Fit(self, x_data,y_data, *args, **kwargs):
        return 'None', 'None'

    def Predict(self, x_data):
        x_Predict = self.Model.fit_transform(x_data)
        return x_Predict,'SNE'

class MLP_Model(Study_MachineBase):
    def __init__(self,args_use,model,*args,**kwargs):#model表示当前选用的模型类型,Alpha针对正则化的参数
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
        pass

    def Del_Leaner(self,Leaner):
        del self.Learner[Leaner]
        del self.Learner_Type[Leaner]

def judging_Digits(num:(int,float)):
    a = str(abs(num)).split('.')[0]
    if a == '':raise ValueError
    return len(a)