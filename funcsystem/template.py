from __future__ import division  # 让/恢复为除法
import tkinter
import tkinter.messagebox
from abc import ABCMeta, abstractmethod
import tkinter.messagebox

import pandas
import sympy

from system import plugin_class_loading, get_path, plugin_func_loading


@plugin_func_loading(get_path(r'template/funcsystem'))
def to_bool(str_object, hope=False):
    false_list = ["0", "n", "no", "NO", "NOT", "No", "Not", "不"]
    true_list = ["y", "yes", "Yes", "YES", "不"]
    if hope:
        true_list.append("")
    else:
        false_list.append("")
    try:
        str_object = str(str_object)
        if str_object in false_list:
            return False
        elif str_object in true_list:
            return True
        else:
            raise Exception
    except BaseException:
        return bool(str_object)


@plugin_func_loading(get_path(r'template/funcsystem'))
def find_x_by_y(x_list, y_list, y):  # 输入x和y照除In_Y的所有对应x值
    m = []
    while True:
        try:
            num = y_list.index(y)
            m.append(x_list[num])
            del x_list[num]
            del y_list[num]
        except ValueError:
            break
    return m


class FuncBase(metaclass=ABCMeta):
    @abstractmethod
    def best_value_core(self):
        pass

    @abstractmethod
    def data_packet(self, number_type=float):
        pass

    @abstractmethod
    def gradient_calculation(self, y_value, start, end, max_iter, accuracy):
        pass

    @abstractmethod
    def dichotomy(self, y_value, **kwargs):
        pass

    @abstractmethod
    def parity(self, precision):
        pass

    @abstractmethod
    def monotonic(self):
        pass

    @abstractmethod
    def property_prediction(self, output_prompt, return_all, accuracy):
        pass

    @abstractmethod
    def hide_or_show(self):
        pass

    @abstractmethod
    def save_csv(self, file_dir):
        pass

    @abstractmethod
    def return_list(self):
        pass

    @abstractmethod
    def best_value(self):
        pass

    @abstractmethod
    def get_memory(self):
        pass

    @abstractmethod
    def clean_memory(self):
        pass

    @abstractmethod
    def get_plot_data(self):
        pass

    @abstractmethod
    def calculation(self, x_in):
        pass

    @abstractmethod
    def periodic(self, output_prompt, accuracy):
        pass

    @abstractmethod
    def symmetry_axis(self, output_prompt, accuracy):
        pass

    @abstractmethod
    def symmetry_center(self, output_prompt, accuracy):
        pass


class SheetFuncBase(FuncBase, metaclass=ABCMeta):
    @abstractmethod
    def dichotomy(self, y_in, *args, **kwargs):
        pass

    @abstractmethod
    def data_packet(self, *args, **kwargs):
        pass

    @abstractmethod
    def property_prediction(self, output_prompt, **kwargs):
        pass

    @abstractmethod
    def periodic(self, output_prompt, **kwargs):
        pass

    @abstractmethod
    def symmetry_axis(self, output_prompt, **kwargs):
        pass

    @abstractmethod
    def symmetry_center(self, output_prompt, **kwargs):
        pass


class ExpFuncBase(FuncBase, metaclass=ABCMeta):
    @abstractmethod
    def return_son(self):
        pass

    @abstractmethod
    def check_monotonic(self, parameters, output_prompt, accuracy):
        pass

    @abstractmethod
    def check_periodic(self, parameters, output_prompt, accuracy):
        pass

    @abstractmethod
    def check_symmetry_axis(self, parameters, output_prompt, accuracy):
        pass

    @abstractmethod
    def check_symmetry_center(self, parameters_input, output_prompt, accuracy):
        pass

    @abstractmethod
    def sympy_calculation(self, y_value):
        pass

    @abstractmethod
    def derivative(self, x_value, delta_x, must):
        pass


class SheetFuncInit(SheetFuncBase):
    def __init__(self, func, name, style):
        # 筛查可以数字化的结果
        float_x_list = []
        float_y_list = []
        for i in range(len(func[0])):  # 检查
            try:
                float_x = float(func[0][i])
                float_y = float(func[1][i])
                float_x_list.append(float_x)
                float_y_list.append(float_y)
            except BaseException:
                pass
        # 筛查重复
        x = []
        y = []
        for x_index in range(len(float_x_list)):
            now_x = float_x_list[x_index]
            if now_x in x:
                continue
            y.append(float_y_list[x_index])
            x.append(now_x)

        # 函数基本信息
        self.func_name = name  # 这个是函数名字
        self.style = style  # 绘制样式

        # 函数基本数据，相当于Lambda的Cul
        self.x = x
        self.y = y
        self.y_real = y
        self.classification_x = []
        self.classification_y = []
        self.xy_sheet = []
        for i in range(len(self.x)):
            self.xy_sheet.append(f"x:{self.x[i]},y:{self.y[i]}")
        self.dataframe = pandas.DataFrame((self.x, self.y), index=("x", "y"))

        self.span = (max(x) - min(x)) / len(x)

        # 函数记忆数据
        self.memore_x = []
        self.memore_y = []
        self.memory_answer = []

        self.have_prediction = False
        self.best_r = None
        self.have_data_packet = False

        self.max_y = None
        self.max_x = []
        self.min_y = None
        self.min_x = []

    def __call__(self, x):
        return self.y[self.x.index(x)]

    def __str__(self):
        return f"{self.func_name}"

    @abstractmethod
    def best_value_core(self):
        pass


@plugin_class_loading(get_path(r'template/funcsystem'))
class SheetDataPacket(SheetFuncInit, metaclass=ABCMeta):
    def data_packet(self, *args, **kwargs):
        if self.have_data_packet:
            return self.x, self.y, self.func_name, self.style
        self.classification_x = [[]]
        self.classification_y = [[]]
        last_y = None
        last_monotonic = None  # 单调性 0-增，1-减
        now_monotonic = 1
        classification_reason = [100]  # 第一断组原因为100
        try:
            for now_x in self.x:
                group_score = 0
                balance = 1
                try:
                    y = self(now_x)
                    if last_y is not None and last_y > y:
                        now_monotonic = 1
                    elif last_y is not None and last_y < y:
                        now_monotonic = 0
                    elif last_y is not None and last_y == y:
                        try:
                            if last_y == y:  # 真实平衡
                                balance = 2
                            elif abs(y - last_y) >= 10 * self.span:
                                balance = 3
                                group_score += 5
                        except BaseException:
                            balance = 4
                            group_score += 9
                        now_monotonic = 2
                    if last_y is not None and last_monotonic != now_monotonic:
                        if (last_y * y) < 0:
                            group_score += 5
                        elif abs(last_y - y) >= (10 * self.span):
                            group_score += 5
                        if group_score >= 5 and (now_monotonic != 2 or balance != 2):
                            classification_reason.append(group_score)
                            self.classification_x.append([])
                            self.classification_y.append([])
                    last_monotonic = now_monotonic
                    self.classification_x[-1].append(now_x)
                    self.classification_y[-1].append(y)
                    last_y = y
                except BaseException:
                    pass
        except (TypeError, IndexError, ValueError):
            pass
        classification_reason.append(99)
        new_classification_x = []
        new_classification_y = []
        must_forward = False
        for i in range(len(self.classification_x)):  # 去除只有单个的组群
            if len(self.classification_x[i]) == 1 and not must_forward:  # 检测到有单个群组
                front_reason = classification_reason[i]  # 前原因
                back_reason = classification_reason[i + 1]  # 后原因
                if front_reason < back_reason:  # 前原因小于后原因，连接到前面
                    try:
                        new_classification_x[-1] += self.classification_x[i]
                        new_classification_y[-1] += self.classification_y[i]
                    except BaseException:  # 按道理不应该出现这个情况
                        new_classification_x.append(self.classification_x[i])
                        new_classification_y.append(self.classification_y[i])
                else:
                    new_classification_x.append(self.classification_x[i])
                    new_classification_y.append(self.classification_y[i])
                    must_forward = True
            else:
                if not must_forward:
                    new_classification_x.append(self.classification_x[i])
                    new_classification_y.append(self.classification_y[i])
                else:
                    new_classification_x[-1] += self.classification_x[i]
                    new_classification_y[-1] += self.classification_y[i]
                    must_forward = False
        self.classification_x = new_classification_x
        self.classification_y = new_classification_y
        self.have_data_packet = True
        self.dataframe = pandas.DataFrame((self.x, self.y), index=("x", "y"))
        self.best_value_core()
        return self.x, self.y, self.func_name, self.style


@plugin_class_loading(get_path(r'template/funcsystem'))
class SheetBestValue(SheetFuncInit, metaclass=ABCMeta):
    def best_value_core(self):  # 计算最值和极值点
        if not self.have_data_packet:
            self.data_packet()  # 检查Cul的计算
        y = self.y + self.memore_y
        x = self.x + self.memore_x
        max_y = max(y)
        min_y = min(y)
        max_x = find_x_by_y(x.copy(), y.copy(), max_y)
        self.max_y = max_y
        self.max_x = max_x
        min_x = find_x_by_y(x.copy(), y.copy(), min_y)
        self.min_y = min_y
        self.min_x = min_x
        return self.max_x, self.max_y, self.min_x, self.min_y

    def best_value(self):
        if not self.have_data_packet:
            self.data_packet()  # 检查Cul的计算
        return self.max_x, self.max_y, self.min_x, self.min_y


@plugin_class_loading(get_path(r'template/funcsystem'))
class SheetComputing(SheetFuncInit, metaclass=ABCMeta):
    def gradient_calculation(self, y_in, *args, **kwargs):  # 保持和下一个对象相同参数
        result = self.dichotomy(y_in)
        return result[0], result[0][0]

    def dichotomy(self, y_in, *args, **kwargs):  # 保持和下一个对象相同参数
        y_list = sorted(self.y.copy())
        last_y = None  # o_y是比较小的，i是比较大的
        result = None
        for i in y_list:
            try:
                if (last_y < y_in < i) and (
                    abs(((i + last_y) / 2) - y_in) < 0.1
                ):
                    result = [last_y, i]
                    break
            except BaseException:
                pass
            last_y = i
        if result is None:
            for i in y_list:
                try:
                    if abs(((i + last_y) / 2) - y_in) < 0.1:
                        result = [last_y, i]
                        break
                except BaseException:
                    pass
                last_y = i
        if result is None:
            return [], []
        last_x = find_x_by_y(self.x.copy(), self.y.copy(), result[0])  # last_y的x
        now_x = find_x_by_y(self.x.copy(), self.y.copy(), result[1])
        x_len = min([len(now_x), len(last_x)])
        answer = []
        result = []
        for i in range(x_len):
            r = (now_x[i] + last_x[i]) / 2
            self.memore_x.append(r)
            self.memore_y.append(y_in)
            result.append(r)
            answer.append(f"y={y_in} -> x={r}")
        self.memory_answer += answer
        return answer, result

    def calculation(self, x_list):
        answer = []
        for i in x_list:
            try:
                i = float(i)
                y = self(i)
                answer.append(f"x={i} -> y={y}")
                if i not in self.memore_x:
                    self.memore_x.append(i)
                    self.memore_y.append(y)
            except BaseException:  # 捕捉运算错误
                continue
        self.memory_answer += answer
        self.best_value_core()
        return answer


@plugin_class_loading(get_path(r'template/funcsystem'))
class SheetProperty(SheetFuncInit, metaclass=ABCMeta):
    def parity(self, *args, **kwargs):  # 奇偶性
        if not self.have_data_packet:
            self.data_packet()  # 检查Cul的计算
        x = self.x.copy()
        left_x = sorted(x)[0]
        right_x = sorted(x)[1]
        left_x = -min([abs(left_x), abs(right_x)])
        right_x = -left_x
        flat = None  # 0-偶函数，1-奇函数
        for i in range(len(x)):
            now_x = x[i]  # 正项x
            if now_x < left_x or now_x > right_x:
                continue  # x不在区间内
            try:
                now_y = self(now_x)
                symmetry_y = self(-now_x)

                if symmetry_y == now_y == 0:
                    continue
                elif symmetry_y == now_y:
                    if flat is None:
                        flat = 0
                    elif flat == 1:
                        raise Exception
                elif symmetry_y == -now_y:
                    if flat is None:
                        flat = 1
                    elif flat == 0:
                        raise Exception
                else:
                    raise Exception
            except BaseException:
                flat = None
                break
        return flat, [left_x, right_x]

    def monotonic(self):  # 单调性
        if not self.have_data_packet:
            self.data_packet()  # 运行Cul计算
        classification_x = self.classification_x.copy()
        increase_interval = []  # 增区间
        minus_interval = []  # 减区间
        interval = []  # 不增不减
        for i in range(len(classification_x)):
            x_list = classification_x[i]
            y_list = classification_x[i]
            last_x = None
            last_y = None
            start_x = None
            flat = None  # 当前研究反围:0-增区间,1-减区间,2-不增不减
            for a in range(len(x_list)):
                now_x = x_list[a]  # 正项x
                now_y = y_list[a]  # 正项y
                if start_x is None:
                    start_x = now_x
                else:
                    if last_y > now_y:  # 减区间
                        if flat is None or flat == 1:  # 减区间
                            pass
                        elif flat == 0:  # 增区间
                            increase_interval.append((start_x, last_x))
                            start_x = last_x
                        elif flat == 2:
                            interval.append((start_x, last_x))
                            start_x = last_x
                        flat = 1
                    elif last_y < now_y:  # 增区间
                        if flat is None or flat == 0:  # 增区间
                            pass
                        elif flat == 1:  # 减区间
                            minus_interval.append((start_x, last_x))
                            start_x = last_x
                        elif flat == 2:
                            interval.append((start_x, last_x))
                            start_x = last_x
                        flat = 0
                    else:  # 水平区间
                        if flat is None or flat == 2:
                            pass
                        elif flat == 1:  # 减区间
                            minus_interval.append((start_x, last_x))
                            start_x = last_x
                        elif flat == 0:  # 增区间
                            increase_interval.append((start_x, last_x))
                            start_x = last_x
                        flat = 2
                last_x = now_x
                last_y = now_y
            if flat == 2:
                interval.append((start_x, last_x))
            elif flat == 1:  # 减区间
                minus_interval.append((start_x, last_x))
            elif flat == 0:  # 增区间
                increase_interval.append((start_x, last_x))
        return increase_interval, minus_interval, interval

    def property_prediction(self, output_prompt=lambda x: x, **kwargs):
        answer = []
        parity = self.parity()
        monotonic = self.monotonic()
        cycles = self.periodic(output_prompt)[0]
        symmetry_axis = self.symmetry_axis(output_prompt)[0]
        center_of_symmetry = self.symmetry_center(output_prompt)[0]
        if parity[0] == 1:
            answer.append(f"奇函数 区间:[{parity[1][0]},{parity[1][0]}]")
        elif parity[0] == 0:
            answer.append(f"偶函数 区间:[{parity[1][0]},{parity[1][0]}]")
        for i in monotonic[0]:
            answer.append(f"增区间:[{i[0]},{i[1]}]")
        for i in monotonic[1]:
            answer.append(f"减区间:[{i[0]},{i[1]}]")
        for i in monotonic[2]:
            answer.append(f"水平区间:[{i[0]},{i[1]}]")
        if cycles is not None:
            answer.append(f"最小正周期：{cycles}")
        if symmetry_axis is not None:
            answer.append(f"对称轴：x={symmetry_axis}")
        if center_of_symmetry is not None:
            answer.append(f"对称中心：{center_of_symmetry}")
        return answer

    def periodic(self, output_prompt=lambda x: x, **kwargs):  # 计算周期
        if not tkinter.messagebox.askokcancel("提示", f"计算周期需要一定时间，是否执行？(计算过程程序可能无响应)"):
            return None, []  # 无结果
        if not self.have_data_packet:
            self.data_packet()
        possible_cycle_list = []  # 可能的周期
        iteration_length = len(self.x)
        iteration_interval = int(iteration_length / 20)
        output_prompt("正在预测可能的周期")
        for i in range(0, iteration_length, iteration_interval):
            start = self.x[i]
            try:
                y = self(start)
                x_list = self.dichotomy(y)[1]
                possible_cycle = []
                for x in x_list:
                    a = abs(x - start)
                    if a == 0:
                        continue
                    possible_cycle.append(a)
                possible_cycle_list.extend(
                    list(set(possible_cycle))
                )  # 这里是extend不是append，相当于 +=
            except BaseException:
                pass

        possible_cycle = []  # a的可能列表
        max_count = 0
        output_prompt("正在筛选结果")
        for i in list(set(possible_cycle_list)):
            count = possible_cycle_list.count(i)
            if count > max_count:
                possible_cycle = [i]
                max_count = count
            elif count == max_count:
                possible_cycle.append(i)
        try:
            possible_cycle.sort()
            output_prompt("计算完毕")
            return possible_cycle[0], possible_cycle
        except BaseException:
            output_prompt("无周期")
            return None, []  # 无结果

    def symmetry_axis(self, output_prompt=lambda x: x, **kwargs):  # 计算对称轴
        if not tkinter.messagebox.askokcancel("提示", f"计算对称轴需要一定时间，是否执行？(计算过程程序可能无响应)"):
            return None, []  # 无结果
        if not self.have_data_packet:
            self.data_packet()
        possible_symmetry_axis_list = []  # 可能的对称轴
        iteration_length = len(self.x)
        iteration_interval = int(iteration_length / 20)
        output_prompt("正在预测可能的对称轴")
        for i in range(0, iteration_length, iteration_interval):
            start = self.x[i]
            try:
                y = self(start)
                x_list = self.dichotomy(y)[1]
                possible_symmetry_axis = []
                for x in x_list:
                    a = (x + start) / 2
                    if possible_symmetry_axis:
                        possible_symmetry_axis.append(a)
                possible_symmetry_axis_list.extend(list(set(possible_symmetry_axis)))
            except BaseException:
                pass

        possible_symmetry_axis = []  # a的可能列表
        max_count = 0
        output_prompt("正在筛选结果")
        for i in list(set(possible_symmetry_axis_list)):
            count = possible_symmetry_axis_list.count(i)
            if count > max_count:
                possible_symmetry_axis = [i]
                max_count = count
            elif count == max_count:
                possible_symmetry_axis.append(i)
        try:
            possible_symmetry_axis.sort()  #
            output_prompt("计算完毕")
            return possible_symmetry_axis[0], possible_symmetry_axis
        except BaseException:
            output_prompt("无对称轴")
            return None, []  # 无结果

    def symmetry_center(self, output_prompt=lambda x: x, **kwargs):  # 计算对称中心
        if not tkinter.messagebox.askokcancel("提示", f"计算对称中心需要一定时间，是否执行？(计算过程程序可能无响应)"):
            return None, []  # 无结果
        if not self.have_data_packet:
            self.data_packet()
        coordinate_points = []
        iteration_length = len(self.x)
        iteration_interval = int(iteration_length / 20)
        output_prompt("正在计算坐标点")
        for i in range(0, iteration_length, iteration_interval):
            start = self.x[i]
            try:
                y = self(start)
                x = start
                coordinate_points.append((x, y))
            except BaseException:
                pass

        possible_center_list = []
        output_prompt("正在预测对称中心")
        for i in coordinate_points:
            for o in coordinate_points:
                x = i[0] + o[0] / 2
                y = i[1] + o[1] / 2
                if i == o:
                    continue
                possible_center_list.append((x, y))

        possible_center = []  # a的可能列表
        max_count = 0
        output_prompt("正在筛选结果")
        for i in list(set(possible_center_list)):
            count = possible_center_list.count(i)
            if count > max_count:
                possible_center = [i]
                max_count = count
            elif count == max_count:
                possible_center.append(i)
        try:
            if max_count < 5:
                raise Exception
            output_prompt("计算完毕")
            possible_center.sort()
            return possible_center[int(len(possible_center) / 2)], possible_center
        except BaseException:
            output_prompt("无对称中心")
            return None, []  # 无结果


@plugin_class_loading(get_path(r'template/funcsystem'))
class SheetMemory(SheetFuncInit, metaclass=ABCMeta):
    def hide_or_show(self):
        if self.have_prediction:
            if tkinter.messagebox.askokcancel("提示", f"是否显示{self}的记忆数据？"):
                self.have_prediction = False
        else:
            if tkinter.messagebox.askokcancel("提示", f"是否隐藏{self}的记忆数据？"):
                self.have_prediction = True

    def clean_memory(self):
        self.memore_x = []
        self.memore_y = []
        self.memory_answer = []

    def get_memory(self):
        if self.have_prediction:
            return [], []
        return self.memore_x, self.memore_y


class ExpFuncInit(ExpFuncBase):
    def __init__(
        self,
        func,
        name,
        style,
        start=-10,
        end=10,
        span=0.1,
        accuracy=2,
        a_default=1,
        a_start=-10,
        a_end=10,
        a_span=1,
        have_son=False,
    ):
        self.symbol_x = sympy.Symbol("x")
        named_domain = {
            "a": a_default,
            "x": self.symbol_x,
            "Pi": sympy.pi,
            "e": sympy.E,
            "log": sympy.log,
            "sin": sympy.sin,
            "cos": sympy.cos,
            "tan": sympy.tan,
            "cot": lambda x: 1 / sympy.tan(x),
            "csc": lambda x: 1 / sympy.sin(x),
            "sec": lambda x: 1 / sympy.cos(x),
            "sinh": sympy.sinh,
            "cosh": sympy.cosh,
            "tanh": sympy.tanh,
            "asin": sympy.asin,
            "acos": sympy.acos,
            "atan": sympy.atan,
            "abs": abs,
        }  # 这个是函数命名域
        self.func = eval(func.replace(" ", ""), named_domain)  # 函数解析式
        self.func_str = func.replace(" ", "")
        # 函数基本信息
        self.style = style  # 绘制样式
        # 数据辨析
        try:
            start = float(start)
            end = float(end)
            if start > end:  # 使用float确保输入是数字，否则诱发ValueError
                start, end = end, start
            span = abs(float(span))
            start = (start // span) * span  # 确保start可以恰好被kd整除
            end = (end // span + 1) * span
            accuracy = abs(int(accuracy))
            if accuracy >= 3:
                accuracy = 3
        except ValueError:
            start, end, span, accuracy = -10, 10, 0.1, 2  # 保底设置
        # 基本数据存储
        self.accuracy = accuracy
        self.start = start
        self.end = end
        self.span = span

        # x和y数据存储
        self.x = []
        self.y = []
        self.y_real = []
        self.classification_x = [[]]
        self.classification_y = [[]]

        # 记忆数据存储
        self.memore_x = []
        self.memore_y = []
        self.memory_answer = []

        # 最值和极值点
        self.max_y = None
        self.max_x = []
        self.min_y = None
        self.min_x = []

        self.have_prediction = False
        self.best_r = None  # 是否计算最值
        self.have_data_packet = False  # 是否已经计算过xy

        # 函数求导
        try:
            self.derivatives = sympy.diff(self.func, self.symbol_x)
        except BaseException:
            self.derivatives = None

        # 儿子函数
        try:
            a_start = float(a_start)
            a_end = float(a_end)
            if a_start > a_end:  # 使用float确保输入是数字，否则诱发ValueError
                a_start, a_end = a_end, a_start
            a_span = abs(float(a_span))
        except ValueError:
            a_start, a_end, a_span = -10, 10, 1  # 保底设置
        if have_son:
            self.son_list = []
            while a_start <= a_end:
                try:
                    self.son_list.append(
                        ExpFuncSon(func, style, start, end, span, accuracy, a_start)
                    )
                except BaseException:
                    pass  # 不应该出现
                a_start += a_span
            # 这个是函数名字
            self.func_name = (
                f"{name}:y={func} a={a_default}({a_start},{a_end},{a_span})"
            )
        else:
            self.son_list = []
            self.func_name = f"{name}:y={func} a={a_default})"  # 这个是函数名字

    def __call__(self, x):
        return self.func.subs({self.symbol_x: x})

    def __str__(self):
        return f"{self.func_name} {self.start, self.end, self.span}"

    @abstractmethod
    def best_value_core(self):
        pass


@plugin_class_loading(get_path(r'template/funcsystem'))
class ExpDataPacket(ExpFuncInit, metaclass=ABCMeta):

    def data_packet(self, number_type=float):
        if self.have_data_packet:
            return self.x, self.y, self.func_name, self.style
        # 混合存储
        self.y = []
        self.y_real = []
        self.x = []
        self.xy_sheet = []
        self.classification_x = [[]]
        self.classification_y = [[]]
        classification_reason = [100]
        last_y = None
        last_monotonic = None  # 单调性 0-增，1-减
        now_monotonic = 1
        try:
            now_x = int(self.start)
            while now_x <= int(self.end):  # 因为range不接受小数
                group_score = 0
                balance = 1
                try:
                    accuracy_x = round(now_x, self.accuracy)
                    now_y = number_type(self(accuracy_x))  # 数字处理方案
                    accuracy_y = round(now_y, self.accuracy)
                    if last_y is not None and last_y > now_y:
                        now_monotonic = 1
                    elif last_y is not None and last_y < now_y:
                        now_monotonic = 0
                    elif last_y is not None and last_y == now_y:
                        try:
                            middle_y = self(round(accuracy_x - 0.5 * self.span))
                            if middle_y == last_y == now_y:  # 真实平衡
                                balance = 2
                            elif (
                                abs(middle_y - last_y) >= 10 * self.span
                                or abs(middle_y - now_y) >= 10 * self.span
                            ):
                                balance = 3
                                group_score += 5
                        except BaseException:
                            balance = 4
                            group_score += 9
                        now_monotonic = 2
                    if last_y is not None and last_monotonic != now_monotonic:
                        if (last_y * now_y) < 0:
                            group_score += 5
                        elif abs(last_y - now_y) >= (10 * self.span):
                            group_score += 5
                        if group_score >= 5 and (now_monotonic != 2 or balance != 2):
                            classification_reason.append(group_score)
                            self.classification_x.append([])
                            self.classification_y.append([])
                    last_monotonic = now_monotonic
                    self.x.append(accuracy_x)  # 四舍五入减少计算量
                    self.y.append(now_y)  # 不四舍五入
                    self.y_real.append(accuracy_y)  # 四舍五入(用于求解最值)
                    self.xy_sheet.append(f"x:{accuracy_x},y:{accuracy_y}")
                    self.classification_x[-1].append(accuracy_x)
                    self.classification_y[-1].append(now_y)
                    last_y = now_y
                except BaseException:
                    classification_reason.append(0)
                    self.classification_x.append([])
                    self.classification_y.append([])
                now_x += self.span
        except (TypeError, IndexError, ValueError):
            pass
        new_classification_x = []
        new_classification_y = []
        classification_reason.append(99)
        must_forward = False
        for i in range(len(self.classification_x)):  # 去除只有单个的组群
            if len(self.classification_x[i]) <= 1 and not must_forward:  # 检测到有单个群组
                front_reason = classification_reason[i]  # 前原因
                back_reason = classification_reason[i + 1]  # 后原因
                if front_reason < back_reason:  # 前原因小于后原因，连接到前面
                    try:
                        new_classification_x[-1] += self.classification_x[i]
                        new_classification_y[-1] += self.classification_y[i]
                    except BaseException:  # 按道理不应该出现这个情况
                        new_classification_x.append(self.classification_x[i])
                        new_classification_y.append(self.classification_y[i])
                else:
                    new_classification_x.append(self.classification_x[i])
                    new_classification_y.append(self.classification_y[i])
                    must_forward = True
            else:
                if not must_forward:
                    new_classification_x.append(self.classification_x[i])
                    new_classification_y.append(self.classification_y[i])
                else:
                    new_classification_x[-1] += self.classification_x[i]
                    new_classification_y[-1] += self.classification_y[i]
                    must_forward = False
        self.classification_x = new_classification_x
        self.classification_y = new_classification_y
        self.have_data_packet = True
        self.dataframe = pandas.DataFrame((self.x, self.y), index=("x", "y"))
        self.best_value_core()
        return self.x, self.y, self.func_name, self.style


@plugin_class_loading(get_path(r'template/funcsystem'))
class ExpBestValue(ExpFuncInit, metaclass=ABCMeta):
    def best_value_core(self):  # 计算最值和极值点
        # 使用ya解决了因计算器误差而没计算到的最值，但是同时本不是最值的与最值相近的数字也被当为了最值，所以使用群组击破
        if not self.have_data_packet:
            self.data_packet()  # 检查Cul的计算
        if len(self.classification_x) != 1:  # 没有计算的必要
            if self.best_r is None:
                self.best_r = not tkinter.messagebox.askokcancel(
                    "建议不计算最值", f"{self}的最值计算不精确，函数可能无最值，是否不计算最值"
                )
            if not self.best_r:
                pass
                return self.max_x, self.max_y, self.min_x, self.min_y
        y = self.y_real + self.memore_y  # x和y数据对齐(因为是加法，所以y的修改不影响self.__ya)
        _y = self.y + self.memore_y
        x = self.x + self.memore_x
        max_y = max(y)
        min_y = min(y)
        max_x = find_x_by_y(x.copy(), y, max_y)
        min_x = find_x_by_y(x.copy(), y, min_y)
        # 处理最大值极值点重复
        max_x = sorted(list(set(max_x)))  # 处理重复
        groups_list = []
        last_x = None
        flat = False
        can_handle = max_x.copy()  # 可处理列表
        for i in range(len(max_x)):  # 迭代选择
            now_x = max_x[i]
            if last_x is None or abs(now_x - last_x) >= 1:  # 1-连续系数
                flat = False
            else:
                if flat:  # 加入群组
                    groups_list[-1].append(now_x)
                else:  # 新键群组
                    groups_list.append([last_x, now_x])
                    del can_handle[can_handle.index(last_x)]
                    flat = True
                del can_handle[can_handle.index(now_x)]  # 删除可处理列表
            last_x = now_x
        for i in groups_list:  # 逐个攻破群组
            groups_y = []  # 群组中x的y值
            for x_in_groups in i:
                num = x.index(x_in_groups)
                groups_y.append(_y[num])  # 找到对应y值
            groups_x = find_x_by_y(i, groups_y, max(groups_y))
            groups_max_x = groups_x[int(len(groups_x) / 2)]
            can_handle.append(groups_max_x)  # 取中间个
        self.max_y = max_y
        self.max_x = can_handle
        # 处理最小值极值点重复
        min_x = sorted(list(set(min_x)))  # 处理重复
        groups_list = []
        last_x = None
        flat = False
        can_handle = min_x.copy()  # 可处理列表
        for i in range(len(min_x)):  # 迭代选择
            now_x = min_x[i]
            if last_x is None or abs(now_x - last_x) >= 1:  # 1-连续系数
                flat = False
            else:
                if flat:  # 加入群组
                    groups_list[-1].append(now_x)
                else:  # 新键群组
                    groups_list.append([last_x, now_x])
                    del can_handle[can_handle.index(last_x)]
                    flat = True
                del can_handle[can_handle.index(now_x)]  # 删除可处理列表
            last_x = now_x
        for i in groups_list:  # 逐个攻破群组
            groups_y = []  # 群组中x的y值
            for x_in_groups in i:
                num = x.index(x_in_groups)
                groups_y.append(_y[num])  # 找到对应y值

            groups_x = find_x_by_y(i, groups_y, min(groups_y))
            groups_max_x = groups_x[int(len(groups_x) / 2)]
            can_handle.append(groups_max_x)  # 取中间个

        self.min_y = min_y
        self.min_x = can_handle
        return self.max_x, self.max_y, self.min_x, self.min_y

    def best_value(self):
        return self.max_x, self.max_y, self.min_x, self.min_y


@plugin_class_loading(get_path(r'template/funcsystem'))
class ExpComputing(ExpFuncInit, metaclass=ABCMeta):

    def sympy_calculation(self, y_value):  # 利用Sympy解方程
        try:
            equation = self.func - float(y_value)
            result_list = sympy.solve(equation, self.symbol_x)
            answer = []
            for x in result_list:
                self.memore_x.append(x)  # 可能需要修复成float(x)
                self.memore_y.append(y_value)
                answer.append(f"y={y_value} -> x={x}")
            return answer, result_list
        except BaseException:
            return [], []

    def gradient_calculation(self, y_value, start, end, max_iter=100, accuracy=0.00001):
        try:
            y_value = float(y_value)
            start = float(start)
            end = float(end)
        except BaseException:
            return "", None
        try:
            max_iter = int(max_iter)
            accuracy = float(accuracy)
        except BaseException:
            max_iter = 100
            accuracy = 0.00001
        left = start
        right = end
        left_history = []
        right_history = []
        middle_history = None
        contraction_direction = 0  # 收缩方向1=a往b，2=b往a，0=未知
        actual_monotony = 0  # 增or减
        for i in range(max_iter):
            if left > right:
                left, right = right, left  # a是小的数字，b是大的数字，c是中间
            left_history.append(left)  # 赋值a的回退值
            right_history.append(right)
            middle = (left + right) / 2
            middle_y = self(middle)
            # 增减预测
            if abs(middle_y - y_value) < accuracy:  # 数据计算完成
                break
            elif middle_y < y_value:  # 预测增还是减：_c移动到y_in需要增还是间
                future_monotony = 1  # 增
            else:
                future_monotony = 0  # 减
            try:  # 当前是增还是减
                if middle_history == middle_y:  # 恰好关于了原点对称
                    pass  # 保持不变
                elif middle_history < middle_y:
                    actual_monotony = 1  # 增
                else:
                    actual_monotony = 0  # 减
            except BaseException:
                contraction_direction = 1
                actual_monotony = future_monotony
            middle_history = middle_y
            # 开始行动
            if future_monotony == actual_monotony:  # 实际和预测一样，保持相同执行方案
                if contraction_direction == 1:  # a往b方向收缩
                    left = middle
                else:
                    right = middle
            else:
                if contraction_direction == 1:  # 收缩方向相反
                    left = left_history[-2]
                    right = middle
                    contraction_direction = 0
                else:
                    left = middle
                    right = right_history[-2]
                    contraction_direction = 1
        else:
            return "", None
        self.memore_x.append(middle)
        self.memore_y.append(y_value)
        self.memory_answer.append(f"y={y_value} -> x={middle}")
        print(f"y={y_value} -> x={middle}", middle)
        return f"y={y_value} -> x={middle}", middle

    def dichotomy(
        self,
        y_value,
        max_iter=100,
        accuracy=0.0001,
        best_value_starting_offset=0.1,
        zero_minimum_distance=0.5,
        allow_original_value=False,
        allow_extended_calculations=True,
        expansion_depth=1000,
        expansion_limit=0.1,
        new_area_offset=0.1,
        secondary_verification=False,
        secondary_verification_effect=None,
        return_all=False,
    ):
        # y_in输入的参数,k最大迭代数,r_Cul允许使用原来的数值,d精度,ky最值允许偏移量,kx新区间偏移量,cx扩张限制,dx两零点的最小范围,deep扩张深度
        # H_Cul允许扩展计算,f_On开启二级验证,f二级验证效果
        if secondary_verification_effect is None:
            secondary_verification_effect = accuracy
        try:  # 参数处理
            allow_original_value = to_bool(allow_original_value)
            allow_extended_calculations = to_bool(allow_extended_calculations, True)
            secondary_verification = to_bool(secondary_verification)
            max_iter = abs(int(max_iter))
            accuracy = abs(float(accuracy))
            best_value_starting_offset = abs(float(best_value_starting_offset))
            new_area_offset = abs(float(new_area_offset))
            expansion_limit = abs(float(expansion_limit))
            zero_minimum_distance = abs(float(zero_minimum_distance))
            expansion_depth = abs(int(expansion_depth))
            secondary_verification_effect = abs(float(secondary_verification_effect))
        except BaseException:
            allow_original_value = False
            allow_extended_calculations = True
            secondary_verification = False
            max_iter = 100
            accuracy = 0.0001
            best_value_starting_offset = 0.1
            new_area_offset = 0.1
            expansion_limit = 0.5
            zero_minimum_distance = 0.5
            expansion_depth = 100
            secondary_verification_effect = accuracy
        if not self.have_data_packet:
            self.data_packet(float)
        x = self.x + self.memore_x
        y = self.y + self.memore_x
        try:
            y_value = float(y_value)
        except BaseException:
            return [], []
        try:
            if (
                y_value < self.min_y - best_value_starting_offset
                or y_value > self.max_y + best_value_starting_offset
            ):
                return [], []  # 返回空值
            if allow_original_value and y_value in y:  # 如果已经计算过
                num = y.index(y_value)
                return x[num]
        except BaseException:
            pass
        iter_interval = [[self.start, self.end]]  # 准备迭代的列表
        middle_list = []
        middle_list_deviation = []
        for interval in iter_interval:
            left = interval[0]
            right = interval[1]
            middle = None
            no_break = False
            for i in range(max_iter):  # 限定次数的迭代
                try:
                    if left > right:
                        left, right = right, left  # a是小的数字，b是大的数字，c是中间
                    if left == right:  # 如果相等，作废
                        middle = None
                        break
                    left_y = self(left) - y_value  # 计算a
                    right_y = self(right) - y_value  # 计算b
                    middle = (left + right) / 2  # 计算c
                    try:
                        middle_y = self(middle) - y_value  # 计算c
                    except BaseException:
                        if expansion_depth > 0:  # 尝试向两边扩张，前提是有deep余额（扩张限制）而且新去见大于cx
                            if abs(left - (middle - new_area_offset)) > expansion_limit:
                                # 增加区间（新区间不包括c，增加了一个偏移kx）
                                iter_interval.append([left, middle - new_area_offset])
                                expansion_depth -= 1  # 余额减一
                            if (
                                abs((middle + new_area_offset) - right)
                                > expansion_limit
                            ):
                                iter_interval.append(
                                    [middle + new_area_offset, right]
                                )  # 增加区间
                                expansion_depth -= 1
                            middle = None
                        break
                    left_zero_c = left_y * middle_y  # a,c之间零点
                    right_zero_c = right_y * middle_y  # b,c之间零点
                    if middle_y == 0:  # 如果c就是零点
                        if expansion_depth > 0:  # 尝试向两边扩张，前提是有deep余额（扩张限制）而且新去见大于cx
                            if abs(left - (middle - new_area_offset)) > expansion_limit:
                                # 增加区间（新区间不包括c，增加了一个偏移kx）
                                iter_interval.append([left, middle - new_area_offset])
                                expansion_depth -= 1  # 余额减一
                            if (
                                abs((middle + new_area_offset) - right)
                                > expansion_limit
                            ):
                                iter_interval.append(
                                    [middle + new_area_offset, right]
                                )  # 增加区间
                                expansion_depth -= 1
                        break  # 这个区间迭代完成，跳出返回c
                    elif left_zero_c * right_zero_c == 0:  # a或者b之间有一个是零点
                        if left_zero_c == 0:  # a是零点
                            middle = left
                            if (
                                expansion_depth > 0
                                and abs((left + new_area_offset) - right)
                                > expansion_limit
                            ):
                                iter_interval.append([left + new_area_offset, right])
                                expansion_depth -= 1
                            break
                        else:
                            middle = right  # 同上
                            if (
                                expansion_depth > 0
                                and abs(left - (right - new_area_offset))
                                > expansion_limit
                            ):
                                iter_interval.append([left, right - new_area_offset])
                                expansion_depth -= 1
                            break
                    elif left_zero_c * right_zero_c > 0:  # q和p都有或都没用零点
                        if (
                            left_zero_c > 0
                            and abs(left - right) < zero_minimum_distance
                        ):  # 如果ab足够小反围，则认为a和b之间不存在零点
                            if allow_extended_calculations:
                                # addNews('进入梯度运算')
                                middle = self.gradient_calculation(
                                    y_value, left, right
                                )[1]
                                if middle is not None:
                                    break
                            middle = None
                            break
                        iter_interval.append([right, middle])  # 其中一个方向继续迭代，另一个方向加入候选
                        right = middle
                    elif left_zero_c < 0:  # 往一个方向收缩，同时另一个方向增加新的区间
                        if (
                            expansion_depth > 0
                            and abs(middle - right) > expansion_limit
                        ):
                            iter_interval.append([middle, right])
                            expansion_depth -= 1
                        right = middle
                    elif right_zero_c < 0:  # 同上
                        if expansion_depth > 0 and abs(left - middle) > expansion_limit:
                            iter_interval.append([left, middle])
                            expansion_depth -= 1
                        left = middle
                    if abs(left - right) < accuracy:  # a和b足够小，认为找到零点
                        middle = (left + right) / 2
                        middle_y = self(middle)
                        if (
                            secondary_verification
                            and abs(y_value - middle_y) > secondary_verification_effect
                        ):
                            middle = None
                        break
                except BaseException:
                    break
            else:  # 证明没有break
                no_break = True
            if middle is None:
                continue  # 去除c不存在的选项
            if not no_break:
                middle_list.append(middle)
            else:
                middle_list_deviation.append(middle)
        answer = []
        for i in middle_list:
            self.memore_x.append(i)
            self.memore_y.append(y_value)
            answer.append(f"y={y_value} -> x={i}")
        if return_all:
            for i in middle_list_deviation:
                answer.append(f"(误差)y={y_value} -> x={i}")
        self.memory_answer += answer
        return answer, middle_list

    def calculation(self, x_in):
        answer = []
        for i in x_in:
            try:
                i = float(i)
                y = self(i)
                answer.append(f"x={i} -> y={y}={float(y)}")
                if i not in self.memore_x:
                    self.memore_x.append(i)
                    self.memore_y.append(y)
            except BaseException:  # 捕捉运算错误
                continue
        self.best_value_core()
        self.dataframe = pandas.DataFrame(
            (self.x + self.memore_x, self.y + self.memore_y), index=("x", "y")
        )
        self.memory_answer += answer
        return answer

    def derivative(self, x_value, delta_x=0.1, must=False):  # 可导函数求导，不可导函数逼近
        derivatives = self.derivatives
        try:
            delta_x = abs(float(delta_x))
        except BaseException:
            delta_x = 0.1
        try:
            x_value = float(x_value)
            if derivatives is not None and not must:  # 导函数法
                derivative_num = derivatives.evalf(subs={self.symbol_x: x_value})
                derivative_method = "导函数求值"
            else:
                x1 = x_value - delta_x / 2
                x2 = x_value + delta_x / 2
                y1 = self(x1)
                y2 = self(x2)
                delta_x = y2 - y1
                derivative_num = delta_x / delta_x
                derivative_method = "逼近法求值"
        except BaseException:
            return None, None
        answer = f"({derivative_method})x:{x_value} -> {derivative_num}"
        return answer, derivative_num


@plugin_class_loading(get_path(r'template/funcsystem'))
class ExpProperty(ExpFuncInit, metaclass=ABCMeta):
    def parity(self, precision=False):  # 启动round处理
        if not self.have_data_packet:
            self.data_packet(float)  # 运行Cul计算
        if len(self.classification_x) != 1:
            need_computing = True  # 通过self计算y
        else:
            need_computing = False
        y = self.y.copy()
        x = self.x.copy()
        a = self.start
        b = self.end
        a = -min([abs(a), abs(b)])
        b = -a
        flat = None  # 0-偶函数，1-奇函数
        for i in range(len(x)):
            now_x = x[i]  # 正项x
            if now_x < a or now_x > b:
                continue  # x不在区间内
            try:
                if need_computing:
                    now_y = self(now_x)
                else:
                    now_y = y[i]  # 求得x的y
                if need_computing:
                    symmetry_y = self(-now_x)
                else:
                    symmetry_y = y[x.index(-now_x)]  # 求得-x的y
                if precision:
                    now_y = round(now_y, self.accuracy)
                    symmetry_y = round(symmetry_y, self.accuracy)
                if symmetry_y == now_y == 0:
                    continue
                elif symmetry_y == now_y:
                    if flat is None:
                        flat = 0
                    elif flat == 1:
                        raise Exception
                elif symmetry_y == -now_y:
                    if flat is None:
                        flat = 1
                    elif flat == 0:
                        raise Exception
                else:
                    raise Exception
            except BaseException:
                flat = None
                break
        return flat, [a, b]

    def monotonic(self):
        if not self.have_data_packet:
            self.data_packet(float)  # 运行Cul计算
        classification_x = self.classification_x.copy()
        increase_interval = []  # 增区间
        minus_interval = []  # 减区间
        interval = []  # 不增不减
        for i in range(len(classification_x)):
            x_list = classification_x[i]
            y_list = classification_x[i]
            last_x = None
            last_y = None
            start_x = None
            flat = None  # 当前研究反围:0-增区间,1-减区间,2-不增不减
            for a in range(len(x_list)):
                now_x = x_list[a]  # 正项x
                now_y = y_list[a]  # 正项y
                if start_x is None:
                    start_x = now_x
                else:
                    if last_y > now_y:  # 减区间
                        if flat is None or flat == 1:  # 减区间
                            pass
                        elif flat == 0:  # 增区间
                            increase_interval.append((start_x, last_x))
                            start_x = last_x
                        elif flat == 2:
                            interval.append((start_x, last_x))
                            start_x = last_x
                        flat = 1
                    elif last_y < now_y:  # 增区间
                        if flat is None or flat == 0:  # 增区间
                            pass
                        elif flat == 1:  # 减区间
                            minus_interval.append((start_x, last_x))
                            start_x = last_x
                        elif flat == 2:
                            interval.append((start_x, last_x))
                            start_x = last_x
                        flat = 0
                    else:  # 水平区间
                        if flat is None or flat == 2:
                            pass
                        elif flat == 1:  # 减区间
                            minus_interval.append((start_x, last_x))
                            start_x = last_x
                        elif flat == 0:  # 增区间
                            increase_interval.append((start_x, last_x))
                            start_x = last_x
                        flat = 2
                last_x = now_x
                last_y = now_y
            if flat == 2:
                interval.append((start_x, last_x))
            elif flat == 1:  # 减区间
                minus_interval.append((start_x, last_x))
            elif flat == 0:  # 增区间
                increase_interval.append((start_x, last_x))
        return increase_interval, minus_interval, interval

    def property_prediction(
        self, output_prompt=lambda x: x, return_all=False, accuracy=None
    ):
        try:
            accuracy = float(accuracy)
        except BaseException:
            accuracy = None
        answer = []
        parity = self.parity()
        monotonic = self.monotonic()
        periodic = self.periodic(output_prompt, accuracy)
        symmetry_axis = self.symmetry_axis(output_prompt, accuracy)
        symmetry_center = self.symmetry_center(output_prompt, accuracy)
        if parity[0] == 1:
            answer.append(f"奇函数 区间:[{parity[1][0]},{parity[1][0]}]")
        elif parity[0] == 0:
            answer.append(f"偶函数 区间:[{parity[1][0]},{parity[1][0]}]")
        for i in monotonic[0]:
            answer.append(f"增区间:[{i[0]},{i[1]}]")
        for i in monotonic[1]:
            answer.append(f"减区间:[{i[0]},{i[1]}]")
        for i in monotonic[2]:
            answer.append(f"水平区间:[{i[0]},{i[1]}]")
        if self.derivatives:
            answer.append(f"导函数：{self.derivatives}")
        if periodic[0] is not None:
            answer.append(f"最小正周期：{periodic[0]}")
        if symmetry_axis[0] is not None:
            answer.append(f"对称轴：x={symmetry_axis[0]}")
        if symmetry_center[0] is not None:
            answer.append(f"对称中心：{symmetry_center[0]}")
        if return_all:
            try:
                for i in periodic[1][1:]:
                    answer.append(f"可能的最小正周期：{i}")
            except BaseException:
                pass
            try:
                for i in symmetry_axis[1][1:]:
                    answer.append(f"可能的对称轴：{i}")
            except BaseException:
                pass
            try:
                for i in symmetry_center[1][1:]:
                    answer.append(f"可能的对称中心：{i}")
            except BaseException:
                pass

        return answer

    def periodic(self, output_prompt=lambda x: x, accuracy=None):  # 计算周期
        if not tkinter.messagebox.askokcancel("提示", f"计算周期需要一定时间，是否执行？(计算过程程序可能无响应)"):
            return None, []  # 无结果
        if not self.have_data_packet:
            self.data_packet(float)
        possible_cycle_list = []  # 可能的周期
        start = self.start
        end = self.end
        if accuracy is not None:
            span = accuracy
        else:
            span = abs(start - end) / 20
        output_prompt("正在预测可能的周期")
        while start <= end:
            try:
                y = self(start)
                x_list = self.dichotomy(y)[1]
                output_prompt("迭代运算...")
                # print(x_list)
                possible_cycle = []
                for o_x in x_list:
                    a = round(abs(o_x - start), self.accuracy)
                    if a == 0:
                        start += span
                        continue
                    if a:
                        possible_cycle.append(round(a, self.accuracy))
                possible_cycle_list.extend(list(set(possible_cycle)))  # 不是append
            except BaseException:
                pass
            start += span

        possible_cycle = []  # a的可能列表
        max_count = 0
        output_prompt("正在筛选结果")
        for i in list(set(possible_cycle_list)):
            count = possible_cycle_list.count(i)
            if count > max_count:
                possible_cycle = [i]
                max_count = count
            elif count == max_count:
                possible_cycle.append(i)
        try:
            possible_cycle.sort()
            output_prompt("计算完毕")
            return possible_cycle[0], possible_cycle
        except BaseException:
            output_prompt("无周期")
            return None, []  # 无结果

    def symmetry_axis(self, output_prompt=lambda x: x, accuracy=None):  # 计算对称轴
        if not tkinter.messagebox.askokcancel("提示", f"计算对称轴需要一定时间，是否执行？(计算过程程序可能无响应)"):
            return None, []  # 无结果
        if not self.have_data_packet:
            self.data_packet()
        possible_symmetry_axis_list = []  # 可能的对称轴
        start = self.start
        end = self.end
        if accuracy is not None:
            span = accuracy
        else:
            span = abs(start - end) / 20
        output_prompt("正在预测对称轴")
        while start <= end:
            try:
                y = self(start)
                x_list = self.dichotomy(y)[1]
                output_prompt("迭代运算...")
                # print(x_list)
                possible_symmetry_axis = []
                for o_x in x_list:
                    a = (o_x + start) / 2
                    if a:
                        possible_symmetry_axis.append(round(a, self.accuracy))
                possible_symmetry_axis_list.extend(list(set(possible_symmetry_axis)))
            except BaseException:
                pass
            start += span

        possible_symmetry_axis = []  # a的可能列表
        c = 0
        output_prompt("正在筛选结果")
        for i in list(set(possible_symmetry_axis_list)):
            n_c = possible_symmetry_axis_list.count(i)
            if n_c > c:
                possible_symmetry_axis = [i]
                c = n_c
            elif n_c == c:
                possible_symmetry_axis.append(i)
        try:
            possible_symmetry_axis.sort()  #
            output_prompt("计算完毕")
            return possible_symmetry_axis[0], possible_symmetry_axis
        except BaseException:
            output_prompt("无对称轴")
            return None, []  # 无结果

    def symmetry_center(self, output_prompt=lambda x: x, accuracy=None):  # 计算对称中心
        if not tkinter.messagebox.askokcancel("提示", f"计算对称中心需要一定时间，是否执行？(计算过程程序可能无响应)"):
            return None, []  # 无结果
        if not self.have_data_packet:
            self.data_packet(float)
        coordinate_points = []  # 可能的对称轴
        start = self.start
        end = self.end
        output_prompt("正在计算坐标点")
        if accuracy is not None:
            span = accuracy
        else:
            span = 1
        while start <= end:
            try:
                y = self(start)
                x = start
                coordinate_points.append((x, y))
            except BaseException:
                pass
            start += span
        possible_center_list = []

        output_prompt("正在预测对称中心")
        for i in coordinate_points:
            for o in coordinate_points:
                x = round((i[0] + o[0]) / 2, self.accuracy)
                y = round((i[1] + o[1]) / 2, self.accuracy)
                if i == o:
                    continue
                possible_center_list.append((x, y))
        possible_center = []  # a的可能列表
        max_count = 0
        output_prompt("正在筛选结果")
        for i in list(set(possible_center_list)):
            count = possible_center_list.count(i)
            if count > max_count:
                possible_center = [i]
                max_count = count
            elif count == max_count:
                possible_center.append(i)
        try:
            if max_count < 5:
                raise Exception
            output_prompt("计算完毕")
            possible_center.sort()  #
            return possible_center[int(len(possible_center) / 2)], possible_center
        except BaseException:
            output_prompt("无对称中心")
            return None, []  # 无结果


@plugin_class_loading(get_path(r'template/funcsystem'))
class ExpCheck(ExpFuncInit, metaclass=ABCMeta):
    def check_monotonic(
        self, parameters, output_prompt=lambda x: x, accuracy=None
    ):  # 检查单调性
        result = True  # 预测结果
        try:
            parameters = parameters.split(",")
            start = float(parameters[0])
            end = float(parameters[1])
            flat = int(parameters[2])  # 当前研究反围:0-增区间,1-减区间,2-不增不减
        except BaseException:
            return False, ""
        if start > end:
            start, end = end, start
        last_y = None
        if accuracy is not None:
            span = accuracy
        else:
            span = self.span
        while start <= end:
            try:
                output_prompt("迭代运算...")
                now_y = round(self(start), self.accuracy)
            except BaseException:
                start += span
                continue
            if last_y is None:
                continue
            if flat == 0 and last_y > now_y:  # 增区间，o_y不小于y
                result = False
                break
            elif flat == 1 and last_y < now_y:  # 减小区间，o_y不小于y
                result = False
                break
            elif flat == 2 and last_y != now_y:
                result = False
                break
            last_y = now_y
            start += span

        monotonic_key = {0: "单调递增", 1: "单调递减", 2: "平行"}
        result_key = {True: "成立", False: "不成立"}
        return (
            result,
            f"{self}在[{parameters[0]},{parameters[1]}]{monotonic_key[flat]}{result_key[result]}",
        )

    def check_periodic(
        self, parameters, output_prompt=lambda x: x, accuracy=None
    ):  # 检查周期性
        result = True
        try:
            parameters = float(parameters)
        except BaseException:
            return False, ""
        start = self.start
        end = self.end
        if accuracy is not None:
            span = accuracy
        else:
            span = self.span
        while start <= end:
            try:
                output_prompt("迭代运算...")
                now_y = round(self(start), self.accuracy)
                last_y = round(self(start + parameters), self.accuracy)
                if now_y != last_y:
                    result = False
            except BaseException:
                pass
            start += span
        result_key = {True: "是", False: "不是"}
        return result, f"{self}的周期{result_key[result]}{parameters}"

    def check_symmetry_axis(
        self, parameters, output_prompt=lambda x: x, accuracy=None
    ):  # 检查对称轴
        result = True
        try:
            parameters = 2 * float(parameters)
        except BaseException:
            return False, ""
        start = self.start
        end = self.end
        if accuracy is not None:
            span = accuracy
        else:
            span = self.span
        while start <= end:
            try:
                output_prompt("迭代运算...")
                now_y = round(self(start), self.accuracy)
                last_y = round(self(parameters - start), self.accuracy)
                if now_y != last_y:
                    result = False
            except BaseException:
                pass
            start += span
        result_key = {True: "是", False: "不是"}
        return result, f"{self}的对称轴{result_key[result]}{parameters}"

    def check_symmetry_center(
        self, parameters_input, output_prompt=lambda x: x, accuracy=None
    ):  # 检查对称中心
        result = True
        try:
            parameters = []
            for i in parameters_input.split(","):
                parameters.append(float(i))
        except BaseException:
            return False, ""
        start = self.start
        end = self.end
        if accuracy is not None:
            span = accuracy
        else:
            span = self.span
        while start <= end:
            try:
                output_prompt("迭代运算...")
                now_y = round(self(start), self.accuracy)
                last_y = round(self(2 * parameters[0] - start), self.accuracy)
                if round((now_y + last_y) / 2, self.accuracy) != parameters[1]:
                    result = False
            except BaseException:
                pass
            start += span
        result_key = {True: "是", False: "不是"}
        return result, f"{self}的对称中心{result_key[result]}{parameters}"


@plugin_class_loading(get_path(r'template/funcsystem'))
class ExpMemory(ExpFuncInit, metaclass=ABCMeta):
    def hide_or_show(self):  # 记忆数据显示和隐藏
        if self.have_prediction:
            if tkinter.messagebox.askokcancel("提示", f"是否显示{self}的记忆数据？"):
                # addNews('记忆显示完毕')
                self.have_prediction = False
        else:
            if tkinter.messagebox.askokcancel("提示", f"是否隐藏{self}的记忆数据？"):
                # addNews('记忆隐藏完毕')
                self.have_prediction = True

    def clean_memory(self):
        self.memore_x = []
        self.memore_y = []
        self.memory_answer = []

    def get_memory(self):
        if self.have_prediction:
            return [], []
        return self.memore_x, self.memore_y


@plugin_class_loading(get_path(r'template/funcsystem'))
class ExpFuncSon:
    def __init__(
        self, func, style, start=-10, end=10, span=0.1, accuracy=2, a_default=1
    ):
        self.symbol_x = sympy.Symbol("x")
        named_domain = {
            "a": a_default,
            "x": self.symbol_x,
            "Pi": sympy.pi,
            "e": sympy.E,
            "log": sympy.log,
            "sin": sympy.sin,
            "cos": sympy.cos,
            "tan": sympy.tan,
            "cot": lambda x: 1 / sympy.tan(x),
            "csc": lambda x: 1 / sympy.sin(x),
            "sec": lambda x: 1 / sympy.cos(x),
            "sinh": sympy.sinh,
            "cosh": sympy.cosh,
            "tanh": sympy.tanh,
            "asin": sympy.asin,
            "acos": sympy.acos,
            "atan": sympy.atan,
            "abs": abs,
        }  # 这个是函数命名域
        self.func = eval(func.replace(" ", ""), named_domain)  # 函数解析式
        self.func_str = func.replace(" ", "")
        # 函数基本信息
        self.func_name = f"y={func} a={a_default}"  # 这个是函数名字
        self.style = style  # 绘制样式
        # 数据辨析
        try:
            start = float(start)
            end = float(end)
            if start > end:  # 使用float确保输入是数字，否则诱发ValueError
                start, end = end, start
            span = abs(float(span))
            start = (start // span) * span  # 确保start可以恰好被kd整除
            end = (end // span + 1) * span
            accuracy = abs(int(accuracy))
            if accuracy >= 3:
                accuracy = 3
        except ValueError:
            start, end, span, accuracy = -10, 10, 0.1, 2  # 保底设置
        # 基本数据存储
        self.accuracy = accuracy
        self.start = start
        self.end = end
        self.span = span

        # x和y数据存储
        self.x = []
        self.y = []
        self.y_real = []
        self.classification_x = [[]]
        self.classification_y = [[]]

        self.have_data_packet = False

    def __call__(self, x):
        return self.func.evalf(subs={self.symbol_x: x})

    def __str__(self):
        return f"{self.func_name} {self.start, self.end, self.span}"

    def data_packet(self, number_type=float):
        if self.have_data_packet:
            return self.x, self.y, self.func_name, self.style
        # 混合存储
        self.y = []
        self.y_real = []
        self.x = []
        self.classification_x = [[]]
        self.classification_y = [[]]
        classification_reason = [100]
        last_y = None
        last_monotonic = None  # 单调性 0-增，1-减
        now_monotonic = 1
        try:
            now_x = int(self.start)
            while now_x <= int(self.end):  # 因为range不接受小数
                group_score = 0
                balance = 1
                try:
                    accuracy_x = round(now_x, self.accuracy)
                    now_y = number_type(self(accuracy_x))  # 数字处理方案
                    accuracy_y = round(now_y, self.accuracy)
                    if last_y is not None and last_y > now_y:
                        now_monotonic = 1
                    elif last_y is not None and last_y < now_y:
                        now_monotonic = 0
                    elif last_y is not None and last_y == now_y:
                        try:
                            middle_y = self(round(accuracy_x - 0.5 * self.span))
                            if middle_y == last_y == now_y:  # 真实平衡
                                balance = 2
                            elif (
                                abs(middle_y - last_y) >= 10 * self.span
                                or abs(middle_y - now_y) >= 10 * self.span
                            ):
                                balance = 3
                                group_score += 5
                        except BaseException:
                            balance = 4
                            group_score += 9
                        now_monotonic = 2
                    if last_y is not None and last_monotonic != now_monotonic:
                        if (last_y * now_y) < 0:
                            group_score += 5
                        elif abs(last_y - now_y) >= (10 * self.span):
                            group_score += 5
                        if group_score >= 5 and (now_monotonic != 2 or balance != 2):
                            classification_reason.append(group_score)
                            self.classification_x.append([])
                            self.classification_y.append([])
                    last_monotonic = now_monotonic
                    self.x.append(accuracy_x)  # 四舍五入减少计算量
                    self.y.append(now_y)  # 不四舍五入
                    self.y_real.append(accuracy_y)  # 四舍五入(用于求解最值)
                    self.classification_x[-1].append(accuracy_x)
                    self.classification_y[-1].append(now_y)
                    last_y = now_y
                except BaseException:
                    classification_reason.append(0)
                    self.classification_x.append([])
                    self.classification_y.append([])
                now_x += self.span
        except (TypeError, IndexError, ValueError):
            pass
        new_classification_x = []
        new_classification_y = []
        classification_reason.append(99)
        must_forward = False
        for i in range(len(self.classification_x)):  # 去除只有单个的组群
            if len(self.classification_x[i]) <= 1 and not must_forward:  # 检测到有单个群组
                front_reason = classification_reason[i]  # 前原因
                back_reason = classification_reason[i + 1]  # 后原因
                if front_reason < back_reason:  # 前原因小于后原因，连接到前面
                    try:
                        new_classification_x[-1] += self.classification_x[i]
                        new_classification_y[-1] += self.classification_y[i]
                    except BaseException:  # 按道理不应该出现这个情况
                        new_classification_x.append(self.classification_x[i])
                        new_classification_y.append(self.classification_y[i])
                else:
                    new_classification_x.append(self.classification_x[i])
                    new_classification_y.append(self.classification_y[i])
                    must_forward = True
            else:
                if not must_forward:
                    new_classification_x.append(self.classification_x[i])
                    new_classification_y.append(self.classification_y[i])
                else:
                    new_classification_x[-1] += self.classification_x[i]
                    new_classification_y[-1] += self.classification_y[i]
                    must_forward = False
        self.classification_x = new_classification_x
        self.classification_y = new_classification_y
        self.have_data_packet = True
        return self.x, self.y, self.func_name, self.style

    def get_plot_data(self):
        if not self.have_data_packet:
            self.data_packet()
        return (
            self.classification_x,
            self.classification_y,
            self.func_name,
            self.style,
        )
