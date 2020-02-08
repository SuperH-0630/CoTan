from sympy import *
from sympy.plotting import plot3d,plot

class Algebra_base:
    def __init__(self,new=lambda x:x):
        self.Name = {'self':self}#命名空间
        self.Name.update(globals())
        self.Name.update(locals())
        self.Algebra_dict = {}
        self.Algebra_dict_View = {}#门面
        self.Symbol_MS = {}#描述文件
        self.Take_News = new

    def Draw_Core(self,f):
        print(f'alg = {f}')
        re = []
        try:
            name = f.func.__name__
            args = f.args
            if name == 'Pow':
                try:
                    if args[1] < 0:
                        a = [['A', '1']]
                        b = self.Draw_Core(f.func(args[0], -args[1]))
                        print(b)
                        re.append(['D', a, b])
                        print(f'Qre = {re}')
                    else:
                        raise Exception
                except:
                    a = self.Draw_Core(args[0])
                    b = self.Draw_Core(args[1])
                    re.append(['B', a, b])
            elif name == 'log':
                # a = [['A', '']]
                b = self.Draw_Core(args[0])
                re.append(['C', [['A', 'ln ']], b])
            elif name == 'Add':
                a = 0
                for i in args:
                    get = self.Draw_Core(i)
                    if a != 0:re.append(['A', ' + '])
                    re += get
                    a += 1
            elif name == 'Mul':
                a = 0
                for i in args:
                    get = self.Draw_Core(i)
                    if a != 0:re.append(['A', ' × '])
                    re += get
                    a += 1
            elif name == 'Rational':
                q = str(f).split('/')
                a = [['A', q[0]]]
                b = [['A', q[1]]]
                re.append(['D', a, b])
            # elif name in ['Symbol', 'One', 'Zero', 'NegativeOne', 'Float', 'Rational', 'Half']:
            #     raise Exception
            elif len(args)<1:
                raise Exception
            else:#增添逗号
                re.append(['A', f'{str(name)}( '])
                a = 0
                for i in args:
                    get = self.Draw_Core(i)
                    if a != 0:re.append(['A', ' , '])
                    re += get
                    a += 1
                re.append(['A', ' )'])
            print(f'bRe={re}')
            return re
        except:
            a = str(f)
            try:
                if a[0] == '-':
                    a = f'({a})'
            except:pass
            re.append(['A', a])
            return re

    def Simplify(self,alg,radio=1.7,func=None,rat=True,inv=False):#函数简化
        if func == None:func = count_ops
        try:
            self.Take_News('正在标准化')
            return simplify(alg,ratio=radio,func=func,rational=rat,inverse=inv)
        except:
            return None

    def rprint_expression(self,e, level=0, First=True):#直接打印
        e = simplify(e)#转换为sympy可以执行的对象
        return self.print_expression_core(e,level,First)

    def print_expression_core(self,e, level=0, First=True,q = 1):#递归
        str_print = ' ' * level
        if First: str_print = f'[{e}]\n' + str_print
        try:
            name = e.func.__name__
            args = e.args
            if args == (): raise Exception
            if name == 'log':name = 'ln'
            str_print += f'({q}){name}\n'
            n = len(name)
            for i in args:
                self.Take_News('正在迭代运算中')
                str_print += self.print_expression_core(i, level + n, First=False,q = q + 1)
            return str_print
        except:
            return str_print + f'({q}){str(e)}\n'

    def Split_Func_core(self,e,deep,f,first=True):#递归
        try:
            name = e.func.__name__
            args = e.args
            if name not in f or args == ():
                if f != ['All']:
                    raise Exception
                else:
                    deep = 1
            if deep == 1:
                if f == ['All'] and not first:
                    re = [e]
                else:
                    re = []
                for i in args:
                    self.Take_News('正在迭代运算中')
                    get = self.Split_Func_core(i, deep, f,False)
                    re += get
                return re
            else:
                return args
        except:
            return [e]

    def Merge_Func_Core(self,name_list,Func):
        if len(name_list) < 2:
            return None
        st = name_list[0]
        for n in name_list[1:]:
            st = Func(st,n)
        return st

    def Creat_Num(self,num,num_type):
        try:
            if num_type == 0:#浮点数
                return Float(num)
            elif num_type == 1:#整数
                return Integer(num)
            elif num_type == 2:#有理数
                n = num.split('/')
                return Rational(n[0],n[1])
            else:
                return sympify(num,locals=self.Name)
        except:
            return Integer(1)

class Algebra_Polynomial(Algebra_base):
    def __call__(self):
        alg_view = []
        alg = []
        for name in self.Algebra_dict:
            alg.append(name)
            alg_view.append(f'{name} --> {self.Algebra_dict[name]}')
        value = []
        value_view = []
        for name in self.Symbol_MS:
            value.append(name)
            value_view.append(f'符号:{name} --> {self.Symbol_MS[name]}')
        return (value_view,value),(alg_view,alg)

    def del_Symbol(self,x):
        del self.Symbol_MS[x]
        del self.Name[x]

    def addSymbol(self,name,AT=0,RI=0,PC=0,EO=0,FI=0,CIR=None,NZ=None,INT=0,NONE=0,ms='自定义符号'):#创建符号(ms=描述)
        k = {}
        try:
            name = name.replace(' ','')
            exec(f'{name} = 5',{})#测试name有没有做符号名字的资质
            if NONE == 1:raise Exception
            if AT == 1:#代数
                k['algebraic'] = True
            elif AT == 2:#超越数
                k['transcendental'] = True
            if RI == 1:#有理数
                k['rational'] = True
            elif RI == 2:#无理数
                k['irrational'] = True
            if PC == 1:#质数
                k['prime'] = True
            elif PC == 2:#合数
                k['composite'] = True
            if EO == 1:#偶数
                k['even'] = True
            elif EO == 2:#奇数
                k['odd'] = True
            if FI == 1:#有限实数
                k['finite'] = True
            elif FI == 2:#无穷
                k['infinite'] = True
            elif FI == 3:#广义实数
                k['extended_real'] = True
            if INT == 1:
                k['integer'] = True
            try:#避免CIR不是list而是None
                k[CIR[0]] = CIR[1]
            except:pass
            try:#避免NZ不是list而是None
                k[NZ[0]] = NZ[1]
            except:pass
        except:
            pass
        new_Name = self.Name.copy()
        new_Name.update({'k':k})
        try:
            exec(f"self.Name['{name}'] = Symbol('{name}',**k)",new_Name)#创建一个Symbols
            self.Symbol_MS[name] = ms
            return True
        except:
            return False
            # raise
    def Value_assumptions0(self,n):
        value = self.Name[n]
        get = value.assumptions0
        R_T = []
        R_F = []
        for i in get:
            if get[i]:
                R_T.append(f'{FY(i)} >>> {get[i]}')
            else:
                R_F.append(f'{FY(i)} >>> {get[i]}')
        return R_T + R_F

    def addAlgebra(self,name,alg):#设置代数式
        try:
            name = name.replace(' ','')
            try:
                exec(f'{name}=5',{})#检查name是否符合标准
            except:
                name = f'F{str(len(self.Algebra_dict))}'
            eval(f'{alg}',self.Name)#检查
            self.Algebra_dict[name] = sympify(alg,locals=self.Name)
            self.Algebra_dict_View[name] = str(alg)
            return True
        except:
            return False

    def del_Alg(self,name):
        del self.Algebra_dict[name]
        del self.Algebra_dict_View[name]

    def Tra_Alg(self):
        self.Algebra_dict = {}
        self.Algebra_dict_View = {}

    def get_Algebra(self,name,str = False):
        if str:
            return self.Algebra_dict_View[name]
        else:
            return self.Algebra_dict[name]

    def print_expression(self,name, level=0, First=True):#根据名字打印
        print(name)
        return self.print_expression_core(self.get_Algebra(name),level,First)

    def Split_Mul(self,name,renum=False,reone=False):
        alg = self.get_Algebra(name)
        r = factor(alg)
        b = list(factor_list(alg))
        c = []
        for i in b:
            if type(i) in (list, tuple):
                b += list(i)
            else:
                try:
                    if renum:
                        if reone:
                            raise Exception
                        else:
                            if i == 1:continue
                    else:
                        Float(i)
                        continue  # 排除数字
                except:
                    pass
                c.append(i)
        return c,r

    def Split_Add(self,name,Object,f):
        alg = self.get_Algebra(name)
        alg = expand(alg)
        coll = collect(alg,Object)
        coll_Dic = collect(alg,Object,evaluate=False)
        if f == 0:
            return list(coll_Dic.keys()),coll
        elif f == 1:
            return list(coll_Dic.values()),coll
        else:
            re = []
            for i in coll_Dic:
                re.append(i*coll_Dic[i])
            return re,coll

    def Split_Func(self,name,deep,f,must = True):
        alg = self.get_Algebra(name)
        if f == ['']:
            try:
                return alg.args,alg
            except:
                return None,alg
        get = self.Split_Func_core(alg, deep, f)
        re = []
        if not must:
            for i in get:
                try:
                    if i.args != ():re.append(i)
                except:
                    pass
            return re,alg
        return get, alg

    def Merge_Add(self, name_list):
        name = []
        for n in name_list:
            try:
                name.append(self.get_Algebra(n))
            except:pass
        return self.Merge_Func_Core(name,Add)

    def Merge_Mul(self, name_list):
        name = []
        for n in name_list:
            try:
                name.append(self.get_Algebra(n))
            except:pass
        return self.Merge_Func_Core(name,Mul)

    def Merge_Func(self, name_list,f):
        name = []
        func = self.Name[f]
        for n in name_list:
            try:
                name.append(self.get_Algebra(n))
            except:pass
        return self.Merge_Func_Core(name,func)

    def Fractional_merge(self,name):#最小公分母合并
        alg = self.get_Algebra(name)
        return ratsimp(alg)

    def Fraction_reduction(self,name):#分式化简
        alg = self.get_Algebra(name)
        return cancel(alg)

    def Fractional_fission(self,name,x):#分式裂项
        x = self.Name[x]
        alg = self.get_Algebra(name)
        return apart(alg,x)

    def as_Fraction(self,name,deep):#合成分式
        alg = self.get_Algebra(name)
        return together(alg,deep)

    def Fractional_rat(self,name,s,Max):#分母有理化
        alg = self.get_Algebra(name)
        return radsimp(alg,s,Max)

    def Trig_Simp(self,name):#三角化简
        alg = self.get_Algebra(name)
        return trigsimp(alg)

    def Trig_Expansion(self,name,deep):#三角化简
        alg = self.get_Algebra(name)
        return expand_trig(alg,deep)

    def Mul_Expansion(self,name):
        alg = self.get_Algebra(name)
        return expand_mul(alg)

    def Multinomial_Expansion(self,name):
        alg = self.get_Algebra(name)
        return expand_multinomial(alg)

    def Pow_Simp_Multinomial(self,name):
        alg = self.get_Algebra(name)
        return powdenest(alg)

    def Pow_Simp_base(self,name,JS):#处理底数
        return self.Pow_Simp(name,JS,'base')

    def Pow_Simp_exp(self,name,JS):#处理指数
        return self.Pow_Simp(name,JS,'exp')

    def Pow_Simp(self,name,JS,combine='all'):#均处理
        alg = self.get_Algebra(name)
        return powsimp(alg,force=JS,combine=combine)

    def Pow_Expansion_base(self,name,deep):
        alg = self.get_Algebra(name)
        return expand_power_base(alg,deep)

    def Pow_Expansion_exp(self,name,deep):
        alg = self.get_Algebra(name)
        return expand_power_exp(alg,deep)

    def Pow_Expansion(self,name,deep):
        alg = self.get_Algebra(name)
        return expand(alg,deep=deep, log=False, mul=False,
        power_exp=True, power_base=True, multinomial=True,
        basic=False)

    def log_Simp(self,name,fo):
        alg = self.get_Algebra(name)
        return logcombine(alg,fo)

    def log_Expansion(self,name,deep,fo):
        alg = self.get_Algebra(name)
        return expand_log(alg,deep,fo)

    def simplify(self,name,ratdio=1.7,func=None,rat=True,inv=False):
        alg = self.get_Algebra(name)
        self.Simplify(alg,ratdio,func,rat,inv)

    def expansion(self,name,IM):
        alg = self.get_Algebra(name)
        return expand(alg,complex=IM)

    def factor(self,name,M,GS,Deep,Rat):
        k = {}
        if M != None:k['modulus']=M
        if GS:k['gaussian']=True
        alg = self.get_Algebra(name)
        return factor(alg,deep = Deep,fraction=Rat,**k)

    def Collect(self,name,x):
        alg = self.get_Algebra(name)
        try:
            return collect(alg,x)
        except:
            return ceiling(alg)

    def complex_Ex(self,name):
        alg = self.get_Algebra(name)
        return expand_complex(alg)

    def func_Ex(self,name):
        alg = self.get_Algebra(name)
        return expand_func(alg)

    def to_num(self,name,n):
        alg = self.get_Algebra(name)
        return alg.evalf(n)

    def Sub_Value(self,name,Dic):
        alg = self.get_Algebra(name)
        sympy_Dic = {}#
        for i in Dic:#i是符号，Dic[i]是代数式名字
            try:
                v_alg = self.get_Algebra(Dic[i])#获得代数式
                get = self.Name[i]#处理符号
                sympy_Dic[get] = v_alg
            except:pass
        return alg.subs(sympy_Dic)

    def RSub_Value(self,name,Dic):
        alg = self.get_Algebra(name)
        sympy_Dic = {}
        for i in Dic:#i是代数式名字，Dic[i]是符号
            try:
                v_alg = self.get_Algebra(i)#获得代数式
                get = self.Name[Dic[i]]#处理符号
                sympy_Dic[v_alg] = get
            except:pass
        return alg.subs(sympy_Dic)

    def SubNum_Value(self,name,Dic):
        alg = self.get_Algebra(name)
        sympy_Dic = {}
        for i in Dic:#i是符号，Dic[i]是数字
            try:
                get = self.Name[i]#处理符号
                sympy_Dic[get] = Dic[i]
            except:pass
        return alg.subs(sympy_Dic)

    def Solve(self,alg_list):
        alg = []
        x_list = set()
        for i in alg_list:
            z = self.get_Algebra(i[0])
            y = self.get_Algebra(i[1])
            alg.append(Eq(z,y))
            x_list = x_list|alg[-1].atoms(Symbol)
        x_list = list(x_list)
        re = []
        for x in x_list:#遍历原子
            get = solve(alg,x,dict=True)
            for i in get:#遍历答案
                for a in i:
                    re.append((a,i[a]))
        return re

    def Solve_Inequality(self,alg_list,Type_Num):
        Type = ['>','<','>=','<='][Type_Num]
        z = self.get_Algebra(alg_list[0])
        y = self.get_Algebra(alg_list[1])
        f = sympify(f'{z} {Type} {y}',locals=self.Name)
        print(f)
        answer = solve(f)
        if answer == True:
            return ['恒成立']
        elif answer == False:
            return ['恒不成立']
        get = self.Split_Func_core(answer,1,('Or'))
        return get

    def Rewrite(self,name,Func,DX,deep=False):
        alg = self.get_Algebra(name)
        f = sympify(Func,locals=self.Name)#重新函数
        if DX != []:
            ff = []  # 重写对象
            for i in DX:
                ff.append(sympify(i,locals=self.Name))
            return alg.rewrite(ff, f, deep=deep)
        else:
            return alg.rewrite(f, deep=deep)

    def Plot(self,name,list_2D,list_3D = None):
        list_2D = list_2D.copy()
        alg = self.get_Algebra(name)
        list_2D[0] = self.Name[list_2D[0]]
        if list_3D == None:
            self.Take_News('正在绘制图像')
            plot(alg, tuple(list_2D),xlabel=f'{list_2D[0]}',ylabel=f'{alg}',title='CoTan Algebra')
        else:
            list_3D = list_3D.copy()
            list_3D[0] = self.Name[list_3D[0]]
            self.Take_News('正在绘制图像')
            plot3d(alg, tuple(list_2D),tuple(list_3D), xlabel=f'{list_2D[0]}', ylabel=f'{list_3D[0]}',zlable=f'{alg}',title='CoTan Algebra')

    def Draw(self,name):
        alg = self.get_Algebra(name)
        return self.Draw_Core(alg)

#提供翻译服务
def FY(word):
    book = {'algebraic':'代数','transcendental':'超越数','rational':'有理数','irrational':'无理数',
            'odd':'奇数','even':'偶数','negative':'负数','positive':'正数','zero':'零',
            'complex':'复数','imaginary':'虚数','real':'实数','integer':'整数','prime':'质数',
            'composite':'合数','finite':'有限数字','infinite':'无穷','extended_real':'广义实数',
            'commutative':'满足交换律','hermitian':'厄米特矩阵','nonnegative':'非负数',
            'nonpositive':'非正数','nonzero':'非零实数','noninteger':'非整数','extended_nonzero':'广义非零数',
            'extended_negative':'广义负数','extended_nonpositive':'广义非正数','extended_nonnegative':'广义非负数',
            'extended_positive':'广义正数'}
    try:
        CN = book[word]
        return f'{CN}({word})'
    except:
        return word