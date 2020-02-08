from __future__ import division#让/恢复为除法
import pandas
import tkinter,tkinter.messagebox
from tkinter.filedialog import asksaveasfile
import tkinter.messagebox
import sympy

def Bool(n,p=False):
    f = ['0','n','no','NO','NOT','No','Not','不']
    t = ['y', 'yes', 'Yes','YES', '不']
    if p:
        t.append('')
    else:
        f.append('')
    try:
        _n = str(n)
        if _n in f:
            return False
        elif _n in t:
            return True
    except:
        pass
    return bool(n)

class HS_CSV:
    def __init__(self,HS,name,view):
        if len(HS[0]) != len(HS[1]):raise Exception#个数不相等报错
        print(HS)
        #筛查可以数字化的结果
        _x = []
        _y = []
        for i in range(len(HS[0])):#检查
            try:
                a_x = float(HS[0][i])
                a_y = float(HS[1][i])
                _x.append(a_x)
                _y.append(a_y)
            except:
                pass
        print(_x)
        print(_y)
        Iter_X = _x
        Iter_X = sorted(list(set(Iter_X)))#排序并且去除重复
        #筛查重复
        x = []
        y = []
        for n_x in Iter_X:
            try:
                y.append(_y[_x.index(n_x)])
                x.append(n_x)
            except:
                pass
        print(x)
        print(y)
        #函数基本信息
        self.Func_Name = name#这个是函数名字
        self.View = view#绘制样式

        #函数基本数据，相当于Lambda的Cul
        self.__x = x
        self.__y = y
        self.__ya = y
        self.__xy = []
        self.__fx = []
        self.__fy = []
        for i in range(len(self.__x)):
            self.__xy.append(f'x:{self.__x[i]},y:{self.__y[i]}')
        self.__xyCSV = pandas.DataFrame((self.__x,self.__y),index=('x','y'))

        #函数记忆数据
        self.Memore_x = []
        self.Memore_y = []
        self.__MemoryAnswer = []

        self.YC = False
        self.Best_R = None
        self.HaveDone = False

        self.max_y = None
        self.max_x = []
        self.min_y = None
        self.min_x = []

    def __call__(self,x):
        return self.__y[self.__x.index(x)]

    def __str__(self):
        return f'{self.Func_Name}'

    def __Best_value(self):  # 计算最值和极值点
        if not self.HaveDone: self.Cul()  # 检查Cul的计算
        y = self.__y + self.Memore_y
        x = self.__x + self.Memore_x
        max_y = max(y)
        min_y = min(y)
        max_x = Find(x.copy(),y.copy(),max_y)
        self.max_y = max_y
        self.max_x = max_x
        min_x = Find(x.copy(),y.copy(),min_y)
        self.min_y = min_y
        self.min_x = min_x
        return self.max_x, self.max_y, self.min_x, self.min_y

    def Cul(self):
        if self.HaveDone:return self.__x,self.__y,self.Func_Name,self.View
        self.__fx = [[]]
        self.__fy = [[]]
        o_y = None
        p = None#单调性 0-增，1-减
        _p = 1
        try:
            for a_x in self.__x:
                c = 0
                p2 = 1
                try:
                    y = self(a_x)
                    if o_y != None and o_y > y:
                        _p = 1
                    elif o_y != None and o_y < y:
                        _p = 0
                    elif o_y != None and o_y == y:
                        try:
                            z_x = round(a_x - 0.5 * self.kd)
                            z_y = self(z_x)
                            if z_y == o_y == y:  # 真实平衡
                                p2 = 2
                            elif abs(z_y - o_y) >= 10 * self.kd or abs(z_y - y) >= 10 * self.kd:
                                p2 = 3
                                c += 5
                        except:
                            p2 = 4
                            c += 9
                        _p = 2
                    if o_y != None and p != _p:
                        if (o_y * y) < 0:
                            c += 5
                        elif abs(o_y - y) >= (10 * self.kd):
                            c += 5
                        if c >= 5 and (_p != 2 or p2 != 2):
                            reason.append(c)
                            self.__fx.append([])
                            self.__fy.append([])
                    p = _p
                    self.__fx[-1].append(a_x)
                    self.__fy[-1].append(y)
                    o_y = y
                except:
                    pass
        except (TypeError, IndexError, ValueError):
            pass
        newfx = []
        newfy = []
        must = False
        for i in range(len(self.__fx)):  # 去除只有单个的组群
            if len(self.__fx[i]) == 1:  # 检测到有单个群组
                q_r = reason[i]  # 前原因
                b_r = reason[i]  # 后原因
                if q_r < b_r:  # 前原因小于后原因，连接到前面
                    try:
                        newfx[-1] += self.__fx[i]
                        newfy[-1] += self.__fy[i]
                    except:  # 按道理不应该出现这个情况
                        newfx.append(self.__fx[i])
                        newfy.append(self.__fy[i])
                else:
                    newfx.append(self.__fx[i])
                    newfy.append(self.__fy[i])
                    must = True
            else:
                if not must:
                    newfx.append(self.__fx[i])
                    newfy.append(self.__fy[i])
                else:
                    newfx[-1] += self.__fx[i]
                    newfy[-1] += self.__fy[i]
                    must = False
        self.__fx = newfx
        self.__fy = newfy
        self.HaveDone = True
        self.__xyCSV = pandas.DataFrame((self.__x,self.__y),index=('x','y'))
        self.__Best_value()
        return self.__x,self.__y,self.Func_Name,self.View

    def Iterative_method_Of_Huan(self, y_in, *args,**kwargs):#保持和下一个对象相同参数
        r = self.Cul_dichotomy(y_in)
        return r[0],r[0][0]#

    def Cul_dichotomy(self, y_in, *args,**kwargs):#保持和下一个对象相同参数
        y = sorted(self.__y.copy())
        o_y = None#o_y是比较小的，i是比较大的
        q = None
        for i in y:
            try:
                if (o_y < y_in and i > y_in) and (abs(((i + o_y)/2) - y_in) < 0.1):
                    q = [o_y,i]
                    break
            except:
                pass
            o_y = i
        if q == None:
            for i in y:
                try:
                    if abs(((i + o_y) / 2) - y_in) < 0.1:
                        q = [o_y, i]
                        break
                except:
                    pass
                o_y = i
        if q == None:return [],[]
        X_o_y = Find(self.__x.copy(),self.__y.copy(),q[0])
        X_y = Find(self.__x.copy(),self.__y.copy(),q[1])
        l = min([len(X_y),len(X_o_y)])
        answer = []
        X_out = []
        for i in range(l):
            print(X_y[i],X_o_y[i])
            r = (X_y[i] + X_o_y[i])/2
            print(r)
            self.Memore_x.append(r)
            self.Memore_y.append(y_in)
            X_out.append(r)
            answer.append(f'y={y_in} -> x={r}')
        self.__MemoryAnswer += answer
        return answer,X_out

    def __Parity(self,ro=False):
        if not self.HaveDone: self.Cul()  # 检查Cul的计算
        y = self.__y.copy()
        x = self.__x.copy()
        a = sorted(x)[0]
        b = sorted(x)[1]
        a = -min([abs(a),abs(b)])
        b = -a
        flat = None#0-偶函数，1-奇函数
        for i in range(len(x)):
            _x = x[i]#正项x
            if _x < a or _x > b:continue#x不在区间内
            try:
                _y = self(_x)
                o_y = self(-_x)

                if o_y == _y == 0:
                    continue
                elif o_y == _y:
                    if flat == None:
                        flat = 0
                    elif flat == 1:
                        raise Exception
                elif o_y == -_y:
                    if flat == None:
                        flat = 1
                    elif flat == 0:
                        raise Exception
                else:
                    raise Exception
            except:
                flat = None
                break
        return flat,[a,b]

    def __Monotonic(self):
        if not self.HaveDone: self.Cul()  # 运行Cul计算
        fy = self.__fy.copy()
        fx = self.__fx.copy()
        Increase_interval = []#增区间
        Minus_interval = []#减区间
        Interval = []#不增不减
        for i in range(len(fx)):
            x = fx[i]
            y = fx[i]
            o_x = None
            o_y = None
            start_x = None
            flat = None#当前研究反围:0-增区间,1-减区间,2-不增不减
            for i in range(len(x)):
                _x = x[i]#正项x
                _y = y[i]#正项y
                if start_x == None:
                    start_x = _x
                else:
                    if o_y > _y:#减区间
                        if flat == None or flat == 1:#减区间
                            pass
                        elif flat == 0:#增区间
                            Increase_interval.append((start_x,o_x))
                            start_x = o_x
                        elif flat == 2:
                            Interval.append((start_x, o_x))
                            start_x = o_x
                        flat = 1
                    elif o_y < _y:#增区间
                        if flat == None or flat == 0:  # 增区间
                            pass
                        elif flat == 1:  # 减区间
                            Minus_interval.append((start_x, o_x))
                            start_x = o_x
                        elif flat == 2:
                            Interval.append((start_x, o_x))
                            start_x = o_x
                        flat = 0
                    else:#水平区间
                        if flat == None or flat == 2:
                            pass
                        elif flat == 1:  # 减区间
                            Minus_interval.append((start_x, o_x))
                            start_x = o_x
                        elif flat == 0:  # 增区间
                            Increase_interval.append((start_x, o_x))
                            start_x = o_x
                        flat = 2
                o_x = _x
                o_y = _y
            if flat == 2:
                Interval.append((start_x, o_x))
            elif flat == 1:  # 减区间
                Minus_interval.append((start_x, o_x))
            elif flat == 0:  # 增区间
                Increase_interval.append((start_x, o_x))
        return Increase_interval,Minus_interval,Interval

    def Nature(self,addNews=lambda x:x):
        answer = []
        P = self.__Parity()
        M = self.__Monotonic()
        ZQ = self.Periodic(addNews)[0]
        DCZ = self.Symmetry_axis(addNews)[0]
        DCZX = self.Center_of_symmetry(addNews)[0]
        if P[0] == 1:
            answer.append(f'奇函数 区间:[{P[1][0]},{P[1][0]}]')
        elif P[0] == 0:
            answer.append(f'偶函数 区间:[{P[1][0]},{P[1][0]}]')
        for i in M[0]:
            answer.append(f'增区间:[{i[0]},{i[1]}]')
        for i in M[1]:
            answer.append(f'减区间:[{i[0]},{i[1]}]')
        for i in M[2]:
            answer.append(f'水平区间:[{i[0]},{i[1]}]')
        if ZQ != None:
            answer.append(f'最小正周期：{ZQ}')
        if DCZ != None:
            answer.append(f'对称轴：x={DCZ}')
        if DCZX != None:
            answer.append(f'对称中心：{DCZX}')
        return answer

    def YC_On_Off(self):
        if self.YC:
            if tkinter.messagebox.askokcancel('提示', f'是否显示{self}的记忆数据？'):
                # addNews('记忆显示完毕')
                self.YC = False
        else:
            if tkinter.messagebox.askokcancel('提示', f'是否隐藏{self}的记忆数据？'):
                # addNews('记忆隐藏完毕')
                self.YC = True

    def Out(self):
        if not self.HaveDone: self.Cul()  # 检查Cul的计算
        if tkinter.messagebox.askokcancel('提示', f'是否确认导出函数:\n{str(self)}'):
            try:
                Dic = tkinter.filedialog.asksaveasfilename(title='选择导出位置', filetypes=[("CSV", ".csv")]) + '.csv'
                if Dic == '.csv':raise Exception
                self.__xyCSV.to_csv(Dic)
                return True
            except:
                pass
        return False

    def returnList(self):
        # 最值和极值点设计
        # if not self.HaveDone: self.Cul()  # 检查Cul的计算
        a = []
        for i in self.min_x:
            a.append(f'极值点：{i}>最小值{self.min_y}')
        for i in self.max_x:
            a.append(f'极值点：{i}>最大值{self.max_y}')
        return a + self.__MemoryAnswer +self.__xy

    def Best_value(self):
        if not self.HaveDone: self.Cul()  # 检查Cul的计算
        return self.max_x, self.max_y, self.min_x, self.min_y

    def getMemory(self):
        if self.YC: return [], []
        return self.Memore_x, self.Memore_y

    def Clear_Memory(self):
        self.Memore_x = []
        self.Memore_y = []
        self.__MemoryAnswer = []

    def Draw_Cul(self):
        if not self.HaveDone:self.Cul()
        return self.__fx,self.__fy,self.Func_Name,self.View

    def Cul_Y(self,x_in):
        answer = []
        for i in x_in:
            try:
                i = float(i)
                y = self(i)
                answer.append(f'x={i} -> y={y}')
                if i not in self.Memore_x:
                    self.Memore_x.append(i)
                    self.Memore_y.append(y)
            except:#捕捉运算错误
                continue
        self.__MemoryAnswer += answer
        self.__Best_value()
        return answer

    def Periodic(self,addNews=lambda x:x):#计算周期
        if not tkinter.messagebox.askokcancel('提示', f'计算周期需要一定时间，是否执行？(计算过程程序可能无响应)'):
            return None,[]#无结果
        if not self.HaveDone: self.Cul()
        p = []#可能的周期
        ran = len(self.__x)
        k = int(ran/20)
        addNews('正在预测可能的周期')
        for i in range(0,ran,k):
            start = self.__x[i]
            try:
                y = self(start)
                x_list = self.Cul_dichotomy(y)[1]
                # print(x_list)
                q = []
                for o_x in x_list:
                    a = abs(o_x - start)
                    if a == 0:continue
                    if a:q.append(a)
                p.extend(list(set(q)))
            except:
                pass
        p_c = list(set(p))
        a = []#a的可能列表
        c = 0
        addNews('正在筛选结果')
        for i in p_c:
            n_c = p.count(i)
            if n_c > c:
                a = [i]
                c = n_c
            elif n_c == c:
                a.append(i)
        try:
            a.sort()#
            addNews('计算完毕')
            return a[0],a
        except:
            addNews('无周期')
            return None,[]#无结果

    def Symmetry_axis(self,addNews=lambda x:x):#计算对称轴
        if not tkinter.messagebox.askokcancel('提示', f'计算对称轴需要一定时间，是否执行？(计算过程程序可能无响应)'):
            return None,[]#无结果
        if not self.HaveDone: self.Cul()
        p = []#可能的对称轴
        ran = len(self.__x)
        k = int(ran / 20)
        addNews('正在预测可能的对称轴')
        for i in range(0, ran, k):
            start = self.__x[i]
            try:
                y = self(start)
                x_list = self.Cul_dichotomy(y)[1]
                print(x_list)
                q = []
                for o_x in x_list:
                    a = (o_x + start)/2
                    if a:q.append(a)
                p.extend(list(set(q)))
            except:
                pass
        p_c = list(set(p))
        a = []#a的可能列表
        c = 0
        addNews('正在筛选结果')
        for i in p_c:
            n_c = p.count(i)
            if n_c > c:
                a = [i]
                c = n_c
            elif n_c == c:
                a.append(i)
        try:
            a.sort()  #
            addNews('计算完毕')
            return a[0], a
        except:
            addNews('无对称轴')
            return None, []  # 无结果

    def Center_of_symmetry(self,addNews=lambda x:x):  # 计算对称中心
        if not tkinter.messagebox.askokcancel('提示', f'计算对称中心需要一定时间，是否执行？(计算过程程序可能无响应)'):
            return None, []  # 无结果
        if not self.HaveDone: self.Cul()
        point = []  # 可能的对称轴
        ran = len(self.__x)
        k = int(ran / 20)
        addNews('正在计算坐标点')
        for i in range(0, ran, k):
            start = self.__x[i]
            try:
                y = self(start)
                x = start
                point.append((x,y))
            except:
                pass

        p = []
        addNews('正在预测对称中心')
        for i in point:
            for o in point:
                x = i[0] + o[0] / 2
                y = i[1] + o[1] / 2
                if i == o:continue
                # print(f'i={i},o={o},x={x},y={y}')
                p.append((x,y))
        p_c = list(set(p))
        a = []  # a的可能列表
        c = 0
        addNews('正在筛选结果')
        for i in p_c:
            n_c = p.count(i)
            if n_c > c:
                a = [i]
                c = n_c
            elif n_c == c:
                a.append(i)
        try:
            if c < 5:raise Exception
            addNews('计算完毕')
            a.sort()  #
            return a[int(len(a)/2)], a
        except:
            addNews('无对称中心')
            return None, []  # 无结果

class HS_lambda:
    def __init__(self,HS,name,view,start = -10,end = 10,kd = 0.1,JD = 2,a = 1,a_start=-10,a_end=10,a_kd=1,c_Son = False):
        self.x = sympy.Symbol('x')
        Name = {'a':a,'x': self.x, 'Pi': sympy.pi, 'e': sympy.E, 'log': sympy.log,
                'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
                'cot': lambda x: 1 / sympy.tan(x), 'csc': lambda x: 1 / sympy.sin(x),
                'sec': lambda x: 1 / sympy.cos(x), 'sinh': sympy.sinh, 'cosh': sympy.cosh,
                'tanh': sympy.tanh, 'asin': sympy.asin, 'acos': sympy.acos,
                'atan': sympy.atan,'abs':abs}  # 这个是函数命名域
        self.HS = eval(HS.replace(' ', ''), Name)#函数解析式
        self.str_HS = HS.replace(' ', '')
        #函数基本信息
        self.View = view#绘制样式
        #数据辨析
        try:
            start = float(start)
            end = float(end)
            if start > end:#使用float确保输入是数字，否则诱发ValueError
                start, end = end, start
            kd = abs(float(kd))
            start = (start//kd)*kd#确保start可以恰好被kd整除
            end = (end//kd+1)*kd
            JD = abs(int(JD))
            if JD >= 3:JD = 3
        except ValueError:
            start,end,kd,JD = -10,10,0.1,2#保底设置
        #基本数据存储
        self.JD = JD
        self.start = start
        self.end = end
        self.kd = kd

        #x和y数据存储
        self.__x = []
        self.__y = []
        self.__ya = []
        self.__fx = [[]]
        self.__fy = [[]]

        #记忆数据存储
        self.Memore_x = []
        self.Memore_y = []
        self.__MemoryAnswer = []

        #最值和极值点
        self.max_y = None
        self.max_x = []
        self.min_y = None
        self.min_x = []

        self.YC = False
        self.Best_R = None#是否计算最值
        self.HaveDone = False#是否已经计算过xy

        #函数求导
        try:
            self.DHS = sympy.diff(self.HS, self.x)
        except:
            self.DHS = None

        #儿子函数
        try:
            a_start = float(a_start)
            a_end = float(a_end)
            if a_start > a_end:#使用float确保输入是数字，否则诱发ValueError
                a_start, a_end = a_end, a_start
            a_kd = abs(float(a_kd))
        except ValueError:
            a_start,a_end,a_kd = -10,10,1#保底设置
        if c_Son:
            self.Son_List = []
            while a_start <= a_end:
                try:
                    self.Son_List.append(HS_lambda_Son(HS,name,view,start,end,kd,JD,a_start))
                except:pass#不应该出现
                a_start += a_kd
            self.Func_Name = f'{name}:y={HS} a={a}({a_start},{a_end},{a_kd})'  # 这个是函数名字
        else:
            self.Son_List = []
            self.Func_Name = f'{name}:y={HS} a={a})'  # 这个是函数名字

    def Return_Son(self):
        return self.Son_List

    def __call__(self,x):
        return self.HS.subs({self.x:x})

    def __str__(self):
        return f'{self.Func_Name} {self.start,self.end,self.kd}'

    def __Best_value(self):#计算最值和极值点
        #使用ya解决了因计算器误差而没计算到的最值，但是同时本不是最值的与最值相近的数字也被当为了最值，所以使用群组击破
        if not self.HaveDone: self.Cul()#检查Cul的计算
        if len(self.__fx) != 1:#没有计算的必要
            if self.Best_R == None:
                self.Best_R = not tkinter.messagebox.askokcancel('建议不计算最值', f'{self}的最值计算不精确，函数可能无最值，是否不计算最值')
            if not self.Best_R:
                pass
                return self.max_x,self.max_y,self.min_x,self.min_y
        y = self.__ya + self.Memore_y#x和y数据对齐(因为是加法，所以y的修改不影响self.__ya)
        _y = self.__y + self.Memore_y
        x = self.__x + self.Memore_x
        max_y = max(y)
        min_y = min(y)
        max_x = Find(x.copy(),y,max_y)
        min_x = Find(x.copy(),y,min_y)
        #处理最大值极值点重复
        max_x = sorted(list(set(max_x)))#处理重复
        n = []
        o_a = None
        flat = False
        b = max_x.copy()  #可处理列表
        for i in range(len(max_x)):  #迭代选择
            g_a = max_x[i]
            if o_a == None or abs(g_a - o_a) >= 1:#1-连续系数
                flat = False
            else:
                if flat:#加入群组
                    n[-1].append(g_a)
                else:#新键群组
                    n.append([o_a, g_a])
                    del b[b.index(o_a)]
                    flat = True
                del b[b.index(g_a)]#删除可处理列表
            o_a = g_a
        for i in n:#逐个攻破群组
            y_For_X = []#群组中x的y值
            for Qx in i:
                num = x.index(Qx)
                y_For_X.append(_y[num])#找到对应y值
            n_max = max(y_For_X)#求解最大y值
            n_x = Find(i,y_For_X,n_max)
            n_max_x = n_x[int(len(n_x)/2)]
            b.append(n_max_x)#取中间个
        self.max_y = max_y
        self.max_x = b
        # 处理最小值极值点重复
        min_x = sorted(list(set(min_x)))  # 处理重复
        n = []
        o_a = None
        flat = False
        b = min_x.copy()  # 可处理列表
        for i in range(len(min_x)):  # 迭代选择
            g_a = min_x[i]
            if o_a == None or abs(g_a - o_a) >= 1:  # 1-连续系数
                flat = False
            else:
                if flat:  # 加入群组
                    n[-1].append(g_a)
                else:  # 新键群组
                    n.append([o_a, g_a])
                    del b[b.index(o_a)]
                    flat = True
                del b[b.index(g_a)]  # 删除可处理列表
            o_a = g_a
        for i in n:  # 逐个攻破群组
            y_For_X = []  # 群组中x的y值
            for Qx in i:
                num = x.index(Qx)
                y_For_X.append(_y[num])  # 找到对应y值
            n_min = min(y_For_X)  # 求解最大y值
            n_x = Find(i,y_For_X,n_min)
            n_min_x = n_x[int(len(n_x) / 2)]
            b.append(n_min_x)  # 取中间个

        self.min_y = min_y
        self.min_x = b
        return self.max_x,self.max_y,self.min_x,self.min_y

    def Cul(self,it=float):
        if self.HaveDone:
            return self.__x,self.__y,self.Func_Name,self.View
        #混合存储
        self.__y = []
        self.__ya = []
        self.__x = []
        self.__xy = []
        self.__fx = [[]]
        self.__fy = [[]]
        reason = [30]
        o_y = None
        p = None#单调性 0-增，1-减
        _p = 1
        try:
            a = int(self.start)
            while a <= int(self.end):  # 因为range不接受小数
                p2 = 1
                try:
                    c = 0
                    a_x = round(a, self.JD)
                    y = self(a_x)
                    y = it(y)#数字处理方案
                    a_y=round(y,self.JD)
                    if o_y != None and o_y > y:
                        _p = 1
                    elif o_y != None and o_y < y:
                        _p = 0
                    elif o_y != None and o_y == y:
                        try:
                            z_x = round(a_x - 0.5 * self.kd)
                            z_y = self(z_x)
                            if z_y == o_y == y:  # 真实平衡
                                p2 = 2
                            elif abs(z_y - o_y) >= 10 * self.kd or abs(z_y - y) >= 10 * self.kd:
                                p2 = 3
                                c += 5
                        except:
                            p2 = 4
                            c += 9
                        _p = 2
                    if o_y != None and p != _p:
                        if (o_y * y) < 0:
                            c += 5
                        elif abs(o_y - y) >= (10 * self.kd):
                            c += 5
                        if c >= 5 and (_p != 2 or p2 != 2):
                            reason.append(c)
                            self.__fx.append([])
                            self.__fy.append([])
                    p = _p
                    self.__x.append(a_x)#四舍五入减少计算量
                    self.__y.append(y)#不四舍五入
                    self.__ya.append(a_y)  # 四舍五入(用于求解最值)
                    self.__xy.append(f'x:{a_x},y:{a_y}')
                    self.__fx[-1].append(a_x)
                    self.__fy[-1].append(y)
                    o_y = y
                except:
                    reason.append(0)
                    self.__fx.append([])
                    self.__fy.append([])
                a += self.kd
        except (TypeError, IndexError, ValueError):
            pass
        newfx = []
        newfy = []
        must = False
        for i in range(len(self.__fx)):#去除只有单个的组群
            if len(self.__fx[i]) <= 1:#检测到有单个群组
                q_r = reason[i]#前原因
                b_r = reason[i]#后原因
                if q_r < b_r:#前原因小于后原因，连接到前面
                    try:
                        newfx[-1] += self.__fx[i]
                        newfy[-1] += self.__fy[i]
                    except:#按道理不应该出现这个情况
                        newfx.append(self.__fx[i])
                        newfy.append(self.__fy[i])
                else:
                    newfx.append(self.__fx[i])
                    newfy.append(self.__fy[i])
                    must = True
            else:
                if not must:
                    newfx.append(self.__fx[i])
                    newfy.append(self.__fy[i])
                else:
                    newfx[-1] += self.__fx[i]
                    newfy[-1] += self.__fy[i]
                    must = False
        self.__fx = newfx
        self.__fy = newfy
        self.HaveDone = True
        self.__xyCSV = pandas.DataFrame((self.__x,self.__y),index=('x','y'))
        self.__Best_value()
        return self.__x,self.__y,self.Func_Name,self.View

    def Iterative_method_Of_Huan(self,y_in,start,end,k=100,kx=0.00001):#梯度计算(kx表示精度)
        try:
            y_in = float(y_in)
            start = float(start)
            end = float(end)
        except:
            return '',None
        try:
            k = int(k)
            kx = float(kx)
        except:
            k = 100
            kx = 0.00001
        a = start
        b = end
        o_a = []
        o_b = []
        c = 0
        o_c = None
        _a = 0
        _b = 0
        _c = 0
        flat = 0#收缩方向1=a往b，2=b往a，0=未知
        p = 0#增or减
        q = 0#增减预测1增，0减
        for i in range(k):
            #a,b,c确定
            if a > b: a, b = b, a  # a是小的数字，b是大的数字，c是中间
            o_a.append(a)#赋值a的回退值
            o_b.append(b)
            c = (a + b) / 2
            _a = self(a)
            _b = self(b)
            _c = self(c)
            #增减预测
            if abs(_c - y_in)<kx:#数据计算完成
                break
            elif _c < y_in:#预测增还是减：_c移动到y_in需要增还是间
                q = 1#增
            else:
                q = 0#减
            try:#当前是增还是减
                if o_c == _c:#恰好关于了原点对称
                    pass#保持不变
                elif o_c < _c:
                    p = 1#增
                else:
                    p = 0#减
            except:
                flat = 1
                p = q
            o_c = _c
            #开始行动
            if q == p:#实际和预测一样，保持相同执行方案
                if flat == 1:#a往b方向收缩
                    a = c
                else:
                    b = c
            else:
                if flat == 1:#收缩方向相反
                    a = o_a[-2]
                    b = c
                    flat = 0
                else:
                    a = c
                    b = o_b[-2]
                    flat = 1
        else:
            return '', None
        self.Memore_x.append(c)
        self.Memore_y.append(y_in)
        self.__MemoryAnswer.append(f'y={y_in} -> x={c}')
        print(f'y={y_in} -> x={c}',c)
        return f'y={y_in} -> x={c}',c

    def Cul_dichotomy(self, y_in, k=100, d=0.0001, ky=0.1, dx=0.5, r_Cul=False,H_Cul=True, deep=1000, cx=0.1, kx=0.1,f_On=False,f=None,all=False):
        #y_in输入的参数,k最大迭代数,r_Cul允许使用原来的数值,d精度,ky最值允许偏移量,kx新区间偏移量,cx扩张限制,dx两零点的最小范围,deep扩张深度
        #H_Cul允许扩展计算,f_On开启二级验证,f二级验证效果
        if f == None:f = d
        try:#参数处理
            r_Cul = Bool(r_Cul)
            H_Cul = Bool(H_Cul,True)
            f_On = Bool(f_On)
            k = abs(int(k))
            d = abs(float(d))
            ky = abs(float(ky))
            kx = abs(float(kx))
            cx = abs(float(cx))
            dx = abs(float(dx))
            deep = abs(int(deep))
            f = abs(float(f))
        except:
            r_Cul = False
            H_Cul = True
            f_On = False
            k = 100
            d = 0.0001
            ky = 0.1
            kx = 0.1
            cx = 0.5
            dx = 0.5
            deep = 100
            f = d
        if not self.HaveDone: self.Cul()
        x = self.__x + self.Memore_x
        y = self.__y + self.Memore_x
        try:#y_in是否为数字
            y_in = float(y_in)
        except:
            return [], []
        try:
            if y_in < self.min_y-ky or y_in > self.max_y+ky: return [],[]  # 返回空值
            if r_Cul and y_in in y:  # 如果已经计算过
                num = y.index(y_in)
                return x[num]
        except:
            pass
        iter_list = [[self.start, self.end]]  # 准备迭代的列表
        c_list = []
        c_o_list = []
        c = 0
        for ab in iter_list:
            a = ab[0]
            b = ab[1]
            c = None
            br = False
            for i in range(k):  # 限定次数的迭代
                try:
                    if a > b:a,b=b,a#a是小的数字，b是大的数字，c是中间
                    if a == b:#如果相等，作废
                        c=None
                        break
                    _a = self(a) - y_in#计算a
                    _b = self(b) - y_in#计算b
                    c = (a + b) / 2#计算c
                    try:
                        _c = self(c) - y_in#计算c
                    except:
                        if deep > 0:  # 尝试向两边扩张，前提是有deep余额（扩张限制）而且新去见大于cx
                            if abs(a - (c - kx)) > cx:
                                iter_list.append([a, c - kx])  # 增加区间（新区间不包括c，增加了一个偏移kx）
                                deep -= 1  # 余额减一
                            if abs((c + kx) - b) > cx:
                                iter_list.append([c + kx, b])  # 增加区间
                                deep -= 1
                            c = None
                        break
                    # print(f'a={a},b={b},c={c},_a={_a},_b={_b}')
                    q = _a * _c#a,c之间零点
                    p = _b * _c#b,c之间零点
                    if _c == 0:#如果c就是零点
                        if deep > 0:#尝试向两边扩张，前提是有deep余额（扩张限制）而且新去见大于cx
                            if abs(a - (c-kx)) > cx:
                                iter_list.append([a, c-kx])#增加区间（新区间不包括c，增加了一个偏移kx）
                                deep -= 1#余额减一
                            if abs((c+kx) - b) > cx:
                                iter_list.append([c+kx, b])#增加区间
                                deep -= 1
                        break#这个区间迭代完成，跳出返回c
                    elif q * p == 0:#a或者b之间有一个是零点
                        if q == 0:#a是零点
                            c = a
                            if deep > 0 and abs((a+kx) - b) > cx:#尝试往b方向扩张
                                iter_list.append([a+kx, b])
                                deep -= 1
                            break
                        else:
                            c = b#同上
                            if deep > 0 and abs(a - (b-kx)) > cx:
                                iter_list.append([a, b-kx])
                                deep -= 1
                            break
                    elif q * p > 0:#q和p都有或都没用零点
                        if q > 0 and abs(a - b) < dx:#如果ab足够小反围，则认为a和b之间不存在零点
                            if H_Cul:
                                # addNews('进入梯度运算')
                                c = self.Iterative_method_Of_Huan(y_in, a, b)[1]
                                if c != None:
                                    break
                            c = None
                            break
                        iter_list.append([b, c])#其中一个方向继续迭代，另一个方向加入候选
                        b = c
                        _b = self(b) - y_in
                    elif q < 0:#往一个方向收缩，同时另一个方向增加新的区间
                        if deep > 0 and abs(c - b) > cx:
                            iter_list.append([c,b])
                            deep -= 1
                        b = c
                        _b = self(b) - y_in
                    elif p < 0:#同上
                        if deep > 0 and abs(a - c) > cx:
                            iter_list.append([a,c])
                            deep -= 1
                        a = c
                        _a = self(a) - y_in
                    if abs(a - b) < d:#a和b足够小，认为找到零点
                        c = (a + b) / 2
                        _c = self(c)
                        if f_On and abs(y_in - _c) > f:#_c不是目标输出
                            print("A")
                            c = None
                        break
                except:
                    break
            else:#证明没有break
                br = True
            if c == None:
                continue#去除c不存在的选项
            if not br:
                c_list.append(c)
            else:
                c_o_list.append(c)
        answer = []
        for i in c_list:
            self.Memore_x.append(i)
            self.Memore_y.append(y_in)
            answer.append(f'y={y_in} -> x={i}')
        if all:
            for i in c_o_list:
                answer.append(f'(误差)y={y_in} -> x={i}')
        self.__MemoryAnswer += answer
        return answer, c_list

    def __Parity(self,ro=False):#启动round处理
        if not self.HaveDone: self.Cul()#运行Cul计算
        if len(self.__fx) != 1:
            m = True#通过self计算y
        else:
            m = False
        y = self.__y.copy()
        x = self.__x.copy()
        a = self.start
        b = self.end
        a = -min([abs(a),abs(b)])
        b = -a
        flat = None#0-偶函数，1-奇函数
        for i in range(len(x)):
            _x = x[i]#正项x
            if _x < a or _x > b:continue#x不在区间内
            try:
                if m:
                    _y = self(_x)
                else:
                    _y = y[i]  # 求得x的y
                if m:
                    o_y = self(-_x)
                else:
                    o_y = y[x.index(-_x)]#求得-x的y
                if ro:
                    _y = round(_y,self.JD)
                    o_y = round(o_y, self.JD)
                if o_y == _y == 0:
                    continue
                elif o_y == _y:
                    if flat == None:
                        flat = 0
                    elif flat == 1:
                        raise Exception
                elif o_y == -_y:
                    if flat == None:
                        flat = 1
                    elif flat == 0:
                        raise Exception
                else:
                    raise Exception
            except:
                flat = None
                break
        return flat,[a,b]

    def __Monotonic(self):
        if not self.HaveDone: self.Cul()  # 运行Cul计算
        fy = self.__fy.copy()
        fx = self.__fx.copy()
        Increase_interval = []#增区间
        Minus_interval = []#减区间
        Interval = []#不增不减
        for i in range(len(fx)):
            x = fx[i]
            y = fx[i]
            o_x = None
            o_y = None
            start_x = None
            flat = None#当前研究反围:0-增区间,1-减区间,2-不增不减
            for i in range(len(x)):
                _x = x[i]#正项x
                _y = y[i]#正项y
                if start_x == None:
                    start_x = _x
                else:
                    if o_y > _y:#减区间
                        if flat == None or flat == 1:#减区间
                            pass
                        elif flat == 0:#增区间
                            Increase_interval.append((start_x,o_x))
                            start_x = o_x
                        elif flat == 2:
                            Interval.append((start_x, o_x))
                            start_x = o_x
                        flat = 1
                    elif o_y < _y:#增区间
                        if flat == None or flat == 0:  # 增区间
                            pass
                        elif flat == 1:  # 减区间
                            Minus_interval.append((start_x, o_x))
                            start_x = o_x
                        elif flat == 2:
                            Interval.append((start_x, o_x))
                            start_x = o_x
                        flat = 0
                    else:#水平区间
                        if flat == None or flat == 2:
                            pass
                        elif flat == 1:  # 减区间
                            Minus_interval.append((start_x, o_x))
                            start_x = o_x
                        elif flat == 0:  # 增区间
                            Increase_interval.append((start_x, o_x))
                            start_x = o_x
                        flat = 2
                o_x = _x
                o_y = _y
            if flat == 2:
                Interval.append((start_x, o_x))
            elif flat == 1:  # 减区间
                Minus_interval.append((start_x, o_x))
            elif flat == 0:  # 增区间
                Increase_interval.append((start_x, o_x))
        return Increase_interval,Minus_interval,Interval

    def Nature(self,addNews=lambda x:x,all=False,JD=None,must=False):
        try:
            if not must:JD = float(JD)
        except:
            JD = None
        answer = []
        P = self.__Parity()
        M = self.__Monotonic()
        ZQ = self.Periodic(addNews,JD)
        DCZ = self.Symmetry_axis(addNews,JD)
        DCZX = self.Center_of_symmetry(addNews,JD)
        if P[0] == 1:
            answer.append(f'奇函数 区间:[{P[1][0]},{P[1][0]}]')
        elif P[0] == 0:
            answer.append(f'偶函数 区间:[{P[1][0]},{P[1][0]}]')
        for i in M[0]:
            answer.append(f'增区间:[{i[0]},{i[1]}]')
        for i in M[1]:
            answer.append(f'减区间:[{i[0]},{i[1]}]')
        for i in M[2]:
            answer.append(f'水平区间:[{i[0]},{i[1]}]')
        if self.DHS:
            answer.append(f'导函数：{self.DHS}')
        if ZQ[0] != None:
            answer.append(f'最小正周期：{ZQ[0]}')
        if DCZ[0] != None:
            answer.append(f'对称轴：x={DCZ[0]}')
        if DCZX[0] != None:
            answer.append(f'对称中心：{DCZX[0]}')
        if all:
            try:
                for i in ZQ[1][1:]:
                    answer.append(f'可能的最小正周期：{i}')
            except:
                pass
            try:
                for i in DCZ[1][1:]:
                    answer.append(f'可能的对称轴：{i}')
            except:
                pass
            try:
                for i in DCZX[1][1:]:
                    answer.append(f'可能的对称中心：{i}')
            except:
                pass

        return answer

    def YC_On_Off(self):#记忆数据显示和隐藏
        if self.YC:
            if tkinter.messagebox.askokcancel('提示', f'是否显示{self}的记忆数据？'):
                # addNews('记忆显示完毕')
                self.YC = False
        else:
            if tkinter.messagebox.askokcancel('提示', f'是否隐藏{self}的记忆数据？'):
                # addNews('记忆隐藏完毕')
                self.YC = True

    def Out(self):
        if not self.HaveDone: self.Cul()
        if tkinter.messagebox.askokcancel('提示', f'是否确认导出函数:\n{str(self)}'):
            try:
                Dic = tkinter.filedialog.asksaveasfilename(title='选择导出位置', filetypes=[("CSV", ".csv")]) + '.csv'
                if Dic == '.csv':raise Exception
                self.__xyCSV.to_csv(Dic)
                return True
            except:
                pass
        return False

    def returnList(self):#导出列表
        if not self.HaveDone:self.Cul()
        #最值和极值点设计
        a = []
        for i in self.min_x:
            a.append(f'极值点：{i}>最小值{self.min_y}')
        for i in self.max_x:
            a.append(f'极值点：{i}>最大值{self.max_y}')
        return a + self.__MemoryAnswer +self.__xy

    def Best_value(self):
        return self.max_x, self.max_y, self.min_x, self.min_y

    def getMemory(self):
        if self.YC:return [],[]
        return self.Memore_x,self.Memore_y

    def Clear_Memory(self):
        self.Memore_x = []
        self.Memore_y = []
        self.__MemoryAnswer = []

    def Draw_Cul(self):
        if not self.HaveDone:self.Cul()
        return self.__fx,self.__fy,self.Func_Name,self.View

    def Cul_Y(self,x_in):
        answer = []
        for i in x_in:
            try:
                i = float(i)
                y = self(i)
                answer.append(f'x={i} -> y={y}={float(y)}')
                if i not in self.Memore_x:
                    self.Memore_x.append(i)
                    self.Memore_y.append(y)
            except:#捕捉运算错误
                continue
        self.__Best_value()
        self.__xyCSV = pandas.DataFrame((self.__x+self.Memore_x, self.__y+self.Memore_y), index=('x', 'y'))
        self.__MemoryAnswer += answer
        return answer

    def Periodic(self,addNews=lambda x:x,JD=None):#计算周期
        if not tkinter.messagebox.askokcancel('提示', f'计算周期需要一定时间，是否执行？(计算过程程序可能无响应)'):
            return None,[]#无结果
        if not self.HaveDone: self.Cul()
        p = []#可能的周期
        start = self.start
        end = self.end
        if JD != None:
            k = JD
        else:
            k = abs(start - end) / 20
        addNews('正在预测可能的周期')
        print(start,end,k)
        while start <= end:
            try:
                y = self(start)
                x_list = self.Cul_dichotomy(y)[1]
                addNews('迭代运算...')
                # print(x_list)
                q = []
                for o_x in x_list:
                    a = round(abs(o_x - start),self.JD)
                    if a == 0:
                        start += k
                        continue
                    if a:q.append(round(a,self.JD))
                p.extend(list(set(q)))
            except:
                pass
            start += k
            print(start)
        p_c = list(set(p))
        a = []#a的可能列表
        c = 0
        addNews('正在筛选结果')
        for i in p_c:
            n_c = p.count(i)
            if n_c > c:
                a = [i]
                c = n_c
            elif n_c == c:
                a.append(i)
        try:
            a.sort()#
            addNews('计算完毕')
            return a[0],a
        except:
            addNews('无周期')
            return None,[]#无结果

    def Symmetry_axis(self,addNews=lambda x:x,JD=None):#计算对称轴
        if not tkinter.messagebox.askokcancel('提示', f'计算对称轴需要一定时间，是否执行？(计算过程程序可能无响应)'):
            return None,[]#无结果
        if not self.HaveDone: self.Cul()
        p = []#可能的对称轴
        start = self.start
        end = self.end
        if JD != None:
            k = JD
        else:
            k = abs(start - end) / 20
        addNews('正在预测对称轴')
        while start <= end:
            try:
                y = self(start)
                x_list = self.Cul_dichotomy(y)[1]
                addNews('迭代运算...')
                # print(x_list)
                q = []
                for o_x in x_list:
                    a = (o_x + start)/2
                    if a:q.append(round(a,self.JD))
                p.extend(list(set(q)))
            except:
                pass
            start += k
        p_c = list(set(p))
        a = []#a的可能列表
        c = 0
        addNews('正在筛选结果')
        for i in p_c:
            n_c = p.count(i)
            if n_c > c:
                a = [i]
                c = n_c
            elif n_c == c:
                a.append(i)
        try:
            a.sort()  #
            addNews('计算完毕')
            return a[0], a
        except:
            addNews('无对称轴')
            return None, []  # 无结果

    def Center_of_symmetry(self,addNews=lambda x:x,JD=None):  # 计算对称中心
        if not tkinter.messagebox.askokcancel('提示', f'计算对称中心需要一定时间，是否执行？(计算过程程序可能无响应)'):
            return None, []  # 无结果
        if not self.HaveDone: self.Cul()
        point = []  # 可能的对称轴
        start = self.start
        end = self.end
        addNews('正在计算坐标点')
        if JD != None:
            k = JD
        else:
            k = 1
        while start <= end:
            try:
                y = self(start)
                x = start
                point.append((x,y))
            except:
                pass
            start += k
        p = []

        addNews('正在预测对称中心')
        for i in point:
            for o in point:
                x = round((i[0] + o[0])/2,self.JD)
                y = round((i[1] + o[1]) / 2, self.JD)
                if i == o:continue
                # print(f'i={i},o={o},x={x},y={y}')
                p.append((x,y))
        p_c = list(set(p))
        a = []  # a的可能列表
        c = 0
        addNews('正在筛选结果')
        for i in p_c:
            n_c = p.count(i)
            if n_c > c:
                a = [i]
                c = n_c
            elif n_c == c:
                a.append(i)
        try:
            if c < 5:raise Exception
            addNews('计算完毕')
            a.sort()  #
            return a[int(len(a)/2)], a
        except:
            addNews('无对称中心')
            return None, []  # 无结果

    def Check_Monotonic(self,cs,addNews=lambda x:x,JD = None):#检查单调性
        test = True#预测结果
        try:
            cd = cs.split(',')
            start = float(cd[0])
            end = float(cd[1])
            flat = float(cd[2]) # 当前研究反围:0-增区间,1-减区间,2-不增不减
        except:
            return False,''
        if start > end:
            start,end = end,start
        o_y = None
        if JD != None:
            k = JD
        else:
            k = self.kd
        while start<= end:
            try:
                addNews('迭代运算...')
                y = round(self(start),self.JD)
            except:
                start += k
                continue
            start += k
            if o_y == None:continue
            if flat == 0 and o_y > y:#增区间，o_y不小于y
                test = False
                break
            elif flat == 1 and o_y < y:#减小区间，o_y不小于y
                test = False
                break
            elif flat == 2 and o_y != y:
                test = False
                break
            o_y = y
        #Start+=k在上面

        key = {0:'单调递增',1:'单调递减',2:'平行'}
        keys = {True: '成立', False: '不成立'}
        return test,f'{self}在[{cd[0]},{cd[1]}]{key[flat]}{keys[test]}'

    def Check_Periodic(self,cs,addNews=lambda x:x,JD = None):#检查周期性
        test = True
        try:
            cs = float(cs)
        except:
            return False,''
        start = self.start
        end = self.end
        if JD != None:
            k = JD
        else:
            k = self.kd
        while start <= end:
            try:
                addNews('迭代运算...')
                y = round(self(start),self.JD)
                o_y = round(self(start + cs),self.JD)
                if y != o_y:
                    test = False
            except:
                pass
            start += k
        key = {True:'是',False:'不是'}
        return test,f'{self}的周期{key[test]}{cs}'

    def Check_Symmetry_axis(self,cs,addNews=lambda x:x,JD=None):#检查对称轴
        test = True
        try:
            cs = 2 * float(cs)
        except:
            return False,''
        start = self.start
        end = self.end
        if JD != None:
            k = JD
        else:
            k = self.kd
        while start <= end:
            try:
                addNews('迭代运算...')
                y = round(self(start),self.JD)
                o_y = round(self(cs-start),self.JD)#(a+b)/2=c >>> b = 2c-a
                if y != o_y:
                    test = False
            except:
                pass
            start += k
        key = {True:'是',False:'不是'}
        return test,f'{self}的对称轴{key[test]}{cs}'

    def Check_Center_of_symmetry(self,in_cs,addNews=lambda x:x,JD=None):#检查对称中心
        test = True
        try:
            cs = []
            for i in in_cs.split(','):
                cs.append(float(i))
        except:
            return False,''
        start = self.start
        end = self.end
        if JD != None:
            k = JD
        else:
            k = self.kd
        while start <= end:
            try:
                addNews('迭代运算...')
                y = round(self(start),self.JD)
                o_y = round(self(2*cs[0]-start),self.JD)#(a+b)/2=c >>> b = 2c-a
                if round((y+o_y)/2,self.JD) != cs[1]:
                    test = False
            except:
                pass
            start += k
        key = {True:'是',False:'不是'}
        return test,f'{self}的对称中心{key[test]}{cs}'

    def Sympy_Cul(self,y_in):#利用Sympy解方程
        try:
            f = self.HS - float(y_in)
            x_list = sympy.solve(f,self.x)
            answer = []
            for x in x_list:
                self.Memore_x.append(x)#可能需要修复成float(x)
                self.Memore_y.append(y_in)
                answer.append(f'y={y_in} -> x={x}')
            return answer,x_list
        except:
            return [],[]

    def Sympy_DHS(self,x_in,dx=0.1,must=False):#可导函数求导，不可导函数逼近
        DHS = self.DHS
        try:
            dx = abs(float(dx))
        except:
            dx = 0.1
        try:
            x_in = float(x_in)
            if DHS != None and not must:#导函数法
                get = DHS.evalf(subs ={self.x:x_in})
                a = '导函数求值'
            else:
                x1 = x_in - dx/2
                x2 = x_in + dx/2
                y1 = self(x1)
                y2 = self(x2)
                dy = y2 - y1
                get = dy/dx
                a = '逼近法求值'
        except:
            return None,None
        answer = f'({a})x:{x_in} -> {get}'
        return answer, get

def Find(x,y,in_y):#输入x和y照除In_Y的所有对应x值
    m = []
    while True:
        try:
            num = y.index(in_y)
            m.append(x[num])
            del x[num]
            del y[num]
        except ValueError:
            break
    return m

class HS_lambda_Son:
    def __init__(self,HS,name,view,start = -10,end = 10,kd = 0.1,JD = 2,a=1):
        self.x = sympy.Symbol('x')
        Name = {'a':a,'x': self.x, 'Pi': sympy.pi, 'e': sympy.E, 'log': sympy.log,
                'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
                'cot': lambda x: 1 / sympy.tan(x), 'csc': lambda x: 1 / sympy.sin(x),
                'sec': lambda x: 1 / sympy.cos(x), 'sinh': sympy.sinh, 'cosh': sympy.cosh,
                'tanh': sympy.tanh, 'asin': sympy.asin, 'acos': sympy.acos,
                'atan': sympy.atan,'abs':abs}  # 这个是函数命名域
        self.HS = eval(HS.replace(' ', ''), Name)#函数解析式
        self.str_HS = HS.replace(' ', '')
        #函数基本信息
        self.Func_Name = f'y={HS} a={a}'#这个是函数名字
        self.View = view#绘制样式
        #数据辨析
        try:
            start = float(start)
            end = float(end)
            if start > end:#使用float确保输入是数字，否则诱发ValueError
                start, end = end, start
            kd = abs(float(kd))
            start = (start//kd)*kd#确保start可以恰好被kd整除
            end = (end//kd+1)*kd
            JD = abs(int(JD))
            if JD >= 3:JD = 3
        except ValueError:
            start,end,kd,JD = -10,10,0.1,2#保底设置
        #基本数据存储
        self.JD = JD
        self.start = start
        self.end = end
        self.kd = kd

        #x和y数据存储
        self.__x = []
        self.__y = []
        self.__ya = []
        self.__fx = [[]]
        self.__fy = [[]]

        #最值和极值点
        self.HaveDone = False#是否已经计算过xy

        #函数求导
        try:
            self.DHS = sympy.diff(self.HS, self.x)
        except:
            self.DHS = None

    def __call__(self,x):
        return self.HS.evalf(subs={self.x:x})

    def __str__(self):
        return f'{self.Func_Name} {self.start,self.end,self.kd}'

    def Creat_Son(self,a_start = -10,a_end = 10,a_kd = 0.1):
        self.Son_List = []
        while a_start <= a_end:
            self.Son_List.append(HS_lambda_Son())

    def Cul(self,it=float):
        if self.HaveDone:
            return self.__x, self.__y, self.Func_Name, self.View
        # 混合存储
        self.__y = []
        self.__ya = []
        self.__x = []
        self.__xy = []
        self.__fx = [[]]
        self.__fy = [[]]
        reason = [30]
        o_y = None
        p = None  # 单调性 0-增，1-减
        _p = 1
        try:
            a = int(self.start)
            while a <= int(self.end):  # 因为range不接受小数
                p2 = 1
                try:
                    c = 0
                    a_x = round(a, self.JD)
                    y = self(a_x)
                    y = it(y)  # 数字处理方案
                    a_y = round(y, self.JD)
                    if o_y != None and o_y > y:
                        _p = 1
                    elif o_y != None and o_y < y:
                        _p = 0
                    elif o_y != None and o_y == y:
                        try:
                            z_x = round(a_x - 0.5 * self.kd)
                            z_y = self(z_x)
                            if z_y == o_y == y:  # 真实平衡
                                p2 = 2
                            elif abs(z_y - o_y) >= 10 * self.kd or abs(z_y - y) >= 10 * self.kd:
                                p2 = 3
                                c += 5
                        except:
                            p2 = 4
                            c += 9
                        _p = 2
                    if o_y != None and p != _p:
                        if (o_y * y) < 0:
                            c += 5
                        elif abs(o_y - y) >= (10 * self.kd):
                            c += 5
                        if c >= 5 and (_p != 2 or p2 != 2):
                            reason.append(c)
                            self.__fx.append([])
                            self.__fy.append([])
                    p = _p
                    self.__x.append(a_x)  # 四舍五入减少计算量
                    self.__y.append(y)  # 不四舍五入
                    self.__ya.append(a_y)  # 四舍五入(用于求解最值)
                    self.__xy.append(f'x:{a_x},y:{a_y}')
                    self.__fx[-1].append(a_x)
                    self.__fy[-1].append(y)
                    o_y = y
                except:
                    reason.append(0)
                    self.__fx.append([])
                    self.__fy.append([])
                a += self.kd
        except (TypeError, IndexError, ValueError):
            pass
        newfx = []
        newfy = []
        must = False
        for i in range(len(self.__fx)):  # 去除只有单个的组群
            if len(self.__fx[i]) <= 1:  # 检测到有单个群组
                q_r = reason[i]  # 前原因
                b_r = reason[i]  # 后原因
                if q_r < b_r:  # 前原因小于后原因，连接到前面
                    try:
                        newfx[-1] += self.__fx[i]
                        newfy[-1] += self.__fy[i]
                    except:  # 按道理不应该出现这个情况
                        newfx.append(self.__fx[i])
                        newfy.append(self.__fy[i])
                else:
                    newfx.append(self.__fx[i])
                    newfy.append(self.__fy[i])
                    must = True
            else:
                if not must:
                    newfx.append(self.__fx[i])
                    newfy.append(self.__fy[i])
                else:
                    newfx[-1] += self.__fx[i]
                    newfy[-1] += self.__fy[i]
                    must = False
        self.__fx = newfx
        self.__fy = newfy
        self.HaveDone = True
        return self.__x, self.__y, self.Func_Name, self.View
    def Draw_Cul(self):
        if not self.HaveDone:self.Cul()
        return self.__fx,self.__fy,self.Func_Name,self.View
