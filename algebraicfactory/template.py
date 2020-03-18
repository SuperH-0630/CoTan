from abc import ABCMeta, abstractmethod
from sympy import simplify, count_ops, Float, Integer, Rational, sympify, factor, factor_list, expand, collect, Add, \
    Mul, ratsimp, cancel, apart, together, radsimp, trigsimp, expand_trig, expand_mul, expand_multinomial, powdenest, \
    powsimp, expand_power_base, expand_power_exp, logcombine, expand_log, ceiling, expand_complex, expand_func, Eq, \
    Symbol, solve, true, false, plot
from sympy.plotting import plot3d

from system import plugin_class_loading, get_path, plugin_func_loading


class AlgebraInit:
    def __init__(self, new=lambda x: x):
        self.symbol_dict = {"self": self}  # 命名空间
        self.symbol_dict.update(globals())
        self.symbol_dict.update(locals())
        exec('from sympy import *', self.symbol_dict)
        self.algebra_dict = {}
        self.algebra_dict_view = {}  # 门面(str)
        self.symbol_describe = {}  # 描述文件
        self.out_status = new

    def get_expression(self, name, exp_str=False):
        if exp_str:
            return self.algebra_dict_view[name]
        else:
            return self.algebra_dict[name]


class AlgebraSymbolBase(AlgebraInit, metaclass=ABCMeta):
    @abstractmethod
    def del_symbol(self, x):
        pass

    @abstractmethod
    def add_symbol(self, name, is_generation, is_rational, is_prime, is_even, is_finite, is_complex, is_natural,
                   is_integer, no_constraint, describe):
        pass

    @abstractmethod
    def variable_prediction(self, n):
        pass


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraSymbol(AlgebraSymbolBase):
    def del_symbol(self, x):
        del self.symbol_describe[x]
        del self.symbol_dict[x]

    def add_symbol(
        self,
        name,
        is_generation=0,
        is_rational=0,
        is_prime=0,
        is_even=0,
        is_finite=0,
        is_complex=None,
        is_natural=None,
        is_integer=0,
        no_constraint=0,
        describe="自定义符号",
    ):
        k = {}
        try:
            name = name.replace(" ", "")
            exec(f"{name} = 5", {})  # 测试name有没有做符号名字的资质
            if no_constraint == 1:
                raise Exception
            if is_generation == 1:  # 代数
                k["algebraic"] = True
            elif is_generation == 2:  # 超越数
                k["transcendental"] = True
            if is_rational == 1:  # 有理数
                k["rational"] = True
            elif is_rational == 2:  # 无理数
                k["irrational"] = True
            if is_prime == 1:  # 质数
                k["prime"] = True
            elif is_prime == 2:  # 合数
                k["composite"] = True
            if is_even == 1:  # 偶数
                k["even"] = True
            elif is_even == 2:  # 奇数
                k["odd"] = True
            if is_finite == 1:  # 有限实数
                k["finite"] = True
            elif is_finite == 2:  # 无穷
                k["infinite"] = True
            elif is_finite == 3:  # 广义实数
                k["extended_real"] = True
            if is_integer == 1:
                k["integer"] = True
            try:  # 避免CIR不是list而是None
                k[is_complex[0]] = is_complex[1]
            except BaseException:
                pass
            try:  # 避免NZ不是list而是None
                k[is_natural[0]] = is_natural[1]
            except BaseException:
                pass
        except BaseException:
            pass
        new_name = self.symbol_dict.copy()
        new_name.update({"k": k})
        exec(f"self.symbol_dict['{name}'] = Symbol('{name}', **k)", new_name)  # 创建一个Symbols
        self.symbol_describe[name] = describe
        return True

    def variable_prediction(self, n):
        value = self.symbol_dict[n]
        get = value.assumptions0
        establish_forecast = []  # 成立的预测
        no_prediction = []  # 不成立的预测
        for i in get:
            if get[i]:
                establish_forecast.append(f"{interpreter(i)} >>> {get[i]}")
            else:
                no_prediction.append(f"{interpreter(i)} >>> {get[i]}")
        return establish_forecast + no_prediction


class AlgebraExpBase(AlgebraInit, metaclass=ABCMeta):
    @abstractmethod
    def formula_export(self, f):
        pass

    @abstractmethod
    def format_func(self, args, name, result_str):
        pass

    @abstractmethod
    def format_rational(self, f, result_str):
        pass

    @abstractmethod
    def format_mul(self, args, result_str):
        pass

    @abstractmethod
    def format_add(self, args, result_str):
        pass

    @abstractmethod
    def format_log(self, args, result_str):
        pass

    @abstractmethod
    def format_pow(self, args, f, result_str):
        pass

    @abstractmethod
    def print_expression_core(self, e, level, first, q):
        pass

    @abstractmethod
    def print_expression_str(self, e, level, first):
        pass

    @abstractmethod
    def split_func_core(self, exp, deep, name_list, first):
        pass

    @abstractmethod
    def merge_func_core(self, name_list, func):
        pass


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraFormat(AlgebraExpBase, metaclass=ABCMeta):
    def formula_export(self, f):
        result_str = []
        try:
            name = f.func.__name__
            args = f.args
            if name == "Pow":
                self.format_pow(args, f, result_str)
            elif name == "log":
                self.format_log(args, result_str)
            elif name == "Add":
                result_str = self.format_add(args, result_str)
            elif name == "Mul":
                result_str = self.format_mul(args, result_str)
            elif name == "Rational":
                self.format_rational(f, result_str)
            elif len(args) < 1:
                raise Exception
            else:  # 增添逗号
                result_str = self.format_func(args, name, result_str)
            return result_str
        except BaseException:
            a = str(f)
            try:
                if a[0] == "-":
                    a = f"({a})"
            except BaseException:
                pass
            result_str.append(["A", a])
            return result_str

    def format_func(self, args, name, result_str):
        result_str.append(["A", f"{str(name)}( "])
        a = 0
        for i in args:
            get = self.formula_export(i)
            if a != 0:
                result_str.append(["A", " , "])
            result_str += get
            a += 1
        result_str.append(["A", " )"])
        return result_str

    def format_rational(self, f, result_str):
        q = str(f).split("/")
        a = [["A", q[0]]]
        b = [["A", q[1]]]
        result_str.append(["D", a, b])

    def format_mul(self, args, result_str):
        a = 0
        for i in args:
            get = self.formula_export(i)
            if a != 0:
                result_str.append(["A", " × "])
            result_str += get
            a += 1
        return result_str

    def format_add(self, args, result_str):
        a = 0
        for i in args:
            get = self.formula_export(i)
            if a != 0:
                result_str.append(["A", " + "])
            result_str += get
            a += 1
        return result_str

    def format_log(self, args, result_str):
        b = self.formula_export(args[0])
        result_str.append(["C", [["A", "ln "]], b])

    def format_pow(self, args, f, result_str):
        try:
            if args[1] < 0:
                a = [["A", "1"]]
                b = self.formula_export(f.func(args[0], -args[1]))
                result_str.append(["D", a, b])
            else:
                raise Exception
        except BaseException:
            a = self.formula_export(args[0])
            b = self.formula_export(args[1])
            result_str.append(["B", a, b])


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraPrint(AlgebraExpBase, metaclass=ABCMeta):
    def print_expression_core(self, e, level=0, first=True, q=1):  # 递归
        str_print = " " * level
        if first:
            str_print = f"[{e}]\n" + str_print
        try:
            name = e.func.__name__
            args = e.args
            if args == ():
                raise Exception
            if name == "log":
                name = "ln"
            str_print += f"({q}){name}\n"
            n = len(name)
            for i in args:
                self.out_status("正在迭代运算中")
                str_print += self.print_expression_core(
                    i, level + n, first=False, q=q + 1
                )
            return str_print
        except BaseException:
            return str_print + f"({q}){str(e)}\n"

    def print_expression_str(self, e, level=0, first=True):  # 直接打印
        e = simplify(e)  # 转换为sympy可以执行的对象
        return self.print_expression_core(e, level, first)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraSplit(AlgebraExpBase, metaclass=ABCMeta):
    def split_func_core(self, exp, deep, name_list, first=True):  # 递归
        try:
            name = exp.func.__name__
            args = exp.args
            if name not in name_list or args == ():
                if name_list != ["All"]:
                    raise Exception
                else:
                    deep = 1
            if deep == 1:
                if name_list == ["All"] and not first:
                    re = [exp]
                else:
                    re = []
                for i in args:
                    self.out_status("正在迭代运算中")
                    get = self.split_func_core(i, deep, name_list, False)
                    re += get
                return re
            else:
                return args
        except BaseException:
            return [exp]


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraMerge(AlgebraExpBase, metaclass=ABCMeta):
    def merge_func_core(self, name_list, func):
        if len(name_list) < 2:
            return None
        st = name_list[0]
        for n in name_list[1:]:
            st = func(st, n)
        return st


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraBase(AlgebraSymbol, AlgebraFormat, AlgebraPrint, AlgebraSplit, AlgebraMerge):

    def simplify(self, alg, radio=1.7, func=None, rat=True, inv=False):  # 函数简化
        if func is None:
            func = count_ops
        try:
            self.out_status("正在标准化")
            return simplify(alg, ratio=radio, func=func, rational=rat, inverse=inv)
        except BaseException:
            return None

    def creat_num(self, num, num_type):
        try:
            if num_type == 0:  # 浮点数
                return Float(num)
            elif num_type == 1:  # 整数
                return Integer(num)
            elif num_type == 2:  # 有理数
                n = num.split("/")
                return Rational(n[0], n[1])
            else:
                return sympify(num, locals=self.symbol_dict)
        except BaseException:
            return Integer(1)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraVisualization(AlgebraBase):
    def add_expression(self, name, alg):  # 添加表达式
        try:
            name = name.replace(" ", "")
            try:
                exec(f"{name}=5", {})  # 检查name是否符合标准
            except BaseException:
                name = f"F{str(len(self.algebra_dict))}"
            eval(f"{alg}", self.symbol_dict)  # 检查
            self.algebra_dict[name] = sympify(alg, locals=self.symbol_dict)
            self.algebra_dict_view[name] = str(alg)
            return True
        except BaseException:
            return False

    def del_expression(self, name):
        del self.algebra_dict[name]
        del self.algebra_dict_view[name]

    def clean_expression(self):
        self.algebra_dict = {}
        self.algebra_dict_view = {}

    def print_expression(self, name, level=0, first=True):  # 根据名字打印
        return self.print_expression_core(self.get_expression(name), level, first)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraPolynomialSplit(AlgebraBase):
    def split_mul(self, name, return_num=False, return_one=False):
        exp = self.get_expression(name)
        factor_exp = factor(exp)  # 因式分解
        split_list = list(factor_list(exp))
        useful_exp = []
        for i in split_list:
            if type(i) in (list, tuple):
                split_list += list(i)
            else:
                try:
                    if return_num:
                        if return_one:
                            raise Exception
                        else:
                            if i == 1:
                                continue
                    else:
                        Float(i)
                        continue  # 排除数字
                except BaseException:
                    pass
                useful_exp.append(i)
        return useful_exp, factor_exp

    def split_add(self, name, collect_exp, return_type):
        exp = self.get_expression(name)
        exp = expand(exp)
        coll = collect(exp, collect_exp)
        coll_dict = collect(exp, collect_exp, evaluate=False)
        if return_type == 0:
            return list(coll_dict.keys()), coll
        elif return_type == 1:
            return list(coll_dict.values()), coll
        else:
            re = []
            for i in coll_dict:
                re.append(i * coll_dict[i])
            return re, coll

    def split_func(self, name, deep, func_name, return_all=True):
        alg = self.get_expression(name)
        if func_name == [""]:
            try:
                return alg.args, alg
            except BaseException:
                return None, alg
        get = self.split_func_core(alg, deep, func_name)
        re = []
        if not return_all:
            for i in get:
                try:
                    if i.args != ():
                        re.append(i)
                except BaseException:
                    pass
            return re, alg
        return get, alg


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraPolynomialMerge(AlgebraBase):
    def merge_add(self, name_list):
        exp = []
        for n in name_list:
            try:
                exp.append(self.get_expression(n))
            except BaseException:
                pass
        return self.merge_func_core(exp, Add)

    def merge_mul(self, name_list):
        exp = []
        for n in name_list:
            try:
                exp.append(self.get_expression(n))
            except BaseException:
                pass
        return self.merge_func_core(exp, Mul)

    def merge_func(self, name_list, f):
        name = []
        func = self.symbol_dict[f]
        for n in name_list:
            try:
                name.append(self.get_expression(n))
            except BaseException:
                pass
        return self.merge_func_core(name, func)


class AlgebraMath(AlgebraBase, metaclass=ABCMeta):
    @abstractmethod
    def fractional_merge(self, name):
        pass

    @abstractmethod
    def fraction_reduction(self, name):
        pass

    @abstractmethod
    def fractional_fission(self, name, x):
        pass

    @abstractmethod
    def as_fraction(self, name, deep):
        pass

    @abstractmethod
    def fractional_rat(self, name, rationalized_unknown, maximum_irrational_term):
        pass

    @abstractmethod
    def trig_simp(self, name):
        pass

    @abstractmethod
    def trig_expansion(self, name, deep):
        pass

    @abstractmethod
    def mul_expansion(self, name):
        pass

    @abstractmethod
    def multinomial_expansion(self, name):
        pass

    @abstractmethod
    def pow_simp_multinomial(self, name):
        pass

    @abstractmethod
    def pow_simp_core(self, name, keep_assumptions, combine):
        pass

    @abstractmethod
    def pow_simp_base(self, name, keep_assumptions):
        pass

    @abstractmethod
    def pow_simp_exp(self, name, keep_assumptions):
        pass

    @abstractmethod
    def pow_expansion_base(self, name, deep):
        pass

    @abstractmethod
    def pow_expansion_exp(self, name, deep):
        pass

    @abstractmethod
    def pow_expansion_core(self, name, deep):
        pass

    @abstractmethod
    def log_simp(self, name, keep_assumptions):
        pass

    @abstractmethod
    def log_expansion(self, name, deep, keep_assumptions):
        pass

    @abstractmethod
    def expansion(self, name, is_expand_complex):
        pass

    @abstractmethod
    def factor(self, name, modulus, is_gaussian, deep, rat):
        pass

    @abstractmethod
    def merger_of_similar_items(self, name, x):
        pass

    @abstractmethod
    def expand_complex(self, name):
        pass

    @abstractmethod
    def expand_special(self, name):
        pass


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class Fractional(AlgebraMath, metaclass=ABCMeta):
    def fractional_merge(self, name):  # 最小公分母合并
        alg = self.get_expression(name)
        return ratsimp(alg)

    def fraction_reduction(self, name):  # 分式化简
        alg = self.get_expression(name)
        return cancel(alg)

    def fractional_fission(self, name, x):  # 分式裂项
        x = self.symbol_dict[x]
        alg = self.get_expression(name)
        return apart(alg, x)

    def as_fraction(self, name, deep):  # 合成分式
        alg = self.get_expression(name)
        return together(alg, deep)

    def fractional_rat(
        self, name, rationalized_unknown, maximum_irrational_term
    ):  # 分母有理化
        alg = self.get_expression(name)
        return radsimp(alg, rationalized_unknown, maximum_irrational_term)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class Trig(AlgebraMath, metaclass=ABCMeta):
    def trig_simp(self, name):  # 三角化简
        alg = self.get_expression(name)
        return trigsimp(alg)

    def trig_expansion(self, name, deep):  # 三角化简
        alg = self.get_expression(name)
        return expand_trig(alg, deep)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraMul(AlgebraMath, metaclass=ABCMeta):
    def mul_expansion(self, name):
        alg = self.get_expression(name)
        return expand_mul(alg)

    def multinomial_expansion(self, name):
        alg = self.get_expression(name)
        return expand_multinomial(alg)

    def pow_simp_multinomial(self, name):
        alg = self.get_expression(name)
        return powdenest(alg)

    def pow_simp_core(self, name, keep_assumptions, combine="all"):  # 均处理
        alg = self.get_expression(name)
        return powsimp(alg, force=keep_assumptions, combine=combine)

    def pow_simp_base(self, name, keep_assumptions):  # 处理底数
        return self.pow_simp_core(name, keep_assumptions, "base")

    def pow_simp_exp(self, name, keep_assumptions):  # 处理指数
        return self.pow_simp_core(name, keep_assumptions, "exp")

    def pow_expansion_base(self, name, deep):
        alg = self.get_expression(name)
        return expand_power_base(alg, deep)

    def pow_expansion_exp(self, name, deep):
        alg = self.get_expression(name)
        return expand_power_exp(alg, deep)

    def pow_expansion_core(self, name, deep):
        alg = self.get_expression(name)
        return expand(
            alg,
            deep=deep,
            log=False,
            mul=False,
            power_exp=True,
            power_base=True,
            multinomial=True,
            basic=False,
        )

    def log_simp(self, name, keep_assumptions):
        alg = self.get_expression(name)
        return logcombine(alg, keep_assumptions)

    def log_expansion(self, name, deep, keep_assumptions):
        alg = self.get_expression(name)
        return expand_log(alg, deep, keep_assumptions)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class General(AlgebraMath, metaclass=ABCMeta):
    def expansion(self, name, is_expand_complex):
        alg = self.get_expression(name)
        return expand(alg, complex=is_expand_complex)

    def factor(self, name, modulus, is_gaussian, deep, rat):
        k = {}
        if modulus is not None:
            k["modulus"] = modulus
        if is_gaussian:
            k["gaussian"] = True
        alg = self.get_expression(name)
        return factor(alg, deep=deep, fraction=rat, **k)

    def merger_of_similar_items(self, name, x):
        alg = self.get_expression(name)
        try:
            return collect(alg, x)
        except BaseException:
            return ceiling(alg)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraComplex(AlgebraMath, metaclass=ABCMeta):
    def expand_complex(self, name):
        alg = self.get_expression(name)
        return expand_complex(alg)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraSpecialFunc(AlgebraMath, metaclass=ABCMeta):
    def expand_special(self, name):
        alg = self.get_expression(name)
        return expand_func(alg)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class Simultaneous(AlgebraBase):
    def value_algebraic_simultaneous(self, name, simultaneous_dict):
        alg = self.get_expression(name)
        sympy_dict = {}
        for i in simultaneous_dict:  # i是符号，Dic[i]是代数式名字
            try:
                v_alg = self.get_expression(simultaneous_dict[i])  # 获得代数式
                get = self.symbol_dict[i]  # 处理符号
                sympy_dict[get] = v_alg
            except BaseException:
                pass
        return alg.subs(sympy_dict)

    def algebragic_value_simultaneous(self, name, simultaneous_dict):
        alg = self.get_expression(name)
        sympy_dict = {}
        for i in simultaneous_dict:  # i是代数式名字，Dic[i]是符号
            try:
                v_alg = self.get_expression(i)  # 获得代数式
                get = self.symbol_dict[simultaneous_dict[i]]  # 处理符号
                sympy_dict[v_alg] = get
            except BaseException:
                pass
        return alg.subs(sympy_dict)

    def algebraic_assignment(self, name, simultaneous_dict):
        alg = self.get_expression(name)
        sympy_dict = {}
        for i in simultaneous_dict:  # i是符号，Dic[i]是数字
            try:
                get = self.symbol_dict[i]  # 处理符号
                sympy_dict[get] = simultaneous_dict[i]
            except BaseException:
                pass
        return alg.subs(sympy_dict)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class Sloving(AlgebraBase):
    def solving_equations(self, equation_set):
        alg = []
        x_list = set()
        for i in equation_set:
            z = self.get_expression(i[0])
            y = self.get_expression(i[1])
            alg.append(Eq(z, y))
            x_list = x_list | alg[-1].atoms(Symbol)
        x_list = list(x_list)
        result = []
        for x in x_list:  # 遍历原子
            get = solve(alg, x, dict=True)
            for i in get:  # 遍历答案
                for a in i:
                    result.append((a, i[a]))
        return result

    def solving_inequality(self, inequalities, inequality_symbol):
        inequality_symbol = [">", "<", ">=", "<="][inequality_symbol]
        z = self.get_expression(inequalities[0])
        y = self.get_expression(inequalities[1])
        f = sympify(f"{z} {inequality_symbol} {y}", locals=self.symbol_dict)
        answer = solve(f)
        if answer is true:
            return ["恒成立"]
        elif answer is false:
            return ["恒不成立"]
        get = self.split_func_core(answer, 1, ["Or"])
        return get


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class Digitization(AlgebraBase):
    def algebraic_digitization(self, name, n):
        alg = self.get_expression(name)
        return alg.evalf(n)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraSimplify(AlgebraBase):
    def simplify(self, name, ratdio=1.7, func=None, rat=True, inv=False):
        alg = self.get_expression(name)
        self.simplify(alg, ratdio, func, rat, inv)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class Rewrite(AlgebraBase):
    def rewrite_exp(self, name, rewrite_func, rewrite_object, deep=False):
        alg = self.get_expression(name)
        initial_object = sympify(rewrite_func, locals=self.symbol_dict)
        if rewrite_object:
            sympify_rewrite_object = []  # 重写对象
            for i in rewrite_object:
                sympify_rewrite_object.append(sympify(i, locals=self.symbol_dict))
            return alg.rewrite(sympify_rewrite_object, initial_object, deep=deep)
        else:
            return alg.rewrite(initial_object, deep=deep)


@plugin_class_loading(get_path(r"template/algebraicfactory"))
class AlgebraPlot(AlgebraBase):
    def plot(self, name, list_2d, list_3d=None):
        list_2d = list_2d.copy()
        alg = self.get_expression(name)
        list_2d[0] = self.symbol_dict[list_2d[0]]
        if list_3d is None:
            self.out_status("正在绘制图像")
            plot(
                alg,
                tuple(list_2d),
                xlabel=f"{list_2d[0]}",
                ylabel=f"{alg}",
                title="CoTan Algebra",
            )
        else:
            list_3d = list_3d.copy()
            list_3d[0] = self.symbol_dict[list_3d[0]]
            self.out_status("正在绘制图像")
            plot3d(
                alg,
                tuple(list_2d),
                tuple(list_3d),
                xlabel=f"{list_2d[0]}",
                ylabel=f"{list_3d[0]}",
                zlable=f"{alg}",
                title="CoTan Algebra",
            )


@plugin_func_loading(get_path(r"template/algebraicfactory"))
def interpreter(word: str):
    book = {
        "algebraic": "代数",
        "transcendental": "超越数",
        "rational": "有理数",
        "irrational": "无理数",
        "odd": "奇数",
        "even": "偶数",
        "negative": "负数",
        "positive": "正数",
        "zero": "零",
        "complex": "复数",
        "imaginary": "虚数",
        "real": "实数",
        "integer": "整数",
        "prime": "质数",
        "composite": "合数",
        "finite": "有限数字",
        "infinite": "无穷",
        "extended_real": "广义实数",
        "commutative": "满足交换律",
        "hermitian": "厄米特矩阵",
        "nonnegative": "非负数",
        "nonpositive": "非正数",
        "nonzero": "非零实数",
        "noninteger": "非整数",
        "extended_nonzero": "广义非零数",
        "extended_negative": "广义负数",
        "extended_nonpositive": "广义非正数",
        "extended_nonnegative": "广义非负数",
        "extended_positive": "广义正数",
    }
    try:
        results = book[word]
        return f"{results}({word})"
    except BaseException:
        return word
