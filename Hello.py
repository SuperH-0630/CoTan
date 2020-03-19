from multiprocessing import Process, Queue, freeze_support
import threading
from _tkinter import TclError
import tkinter
from tkinter import ttk
import tkinter.font as tkfont
from PIL import ImageTk, Image
import time
import os
import tkinter.messagebox
import webbrowser

from newtkinter import DragWindow

SCREEN = None
draftboard_start = None
datascience_start = None
functionmapping_start = None
functionfactory_start = None
algebraicfactory_start = None
machinelearner_start = None
git_start = None
crawlef_start = None
title_color = '#F0FFFF'
button_color = '#FFFFFF'
button_cursor = 'tcross'


class QueueController:
    def __init__(self):
        self.in_dict = {}
        self.out_dict = {}
        self.var_dict = {}
        self.queue_list = []
        self.var_from = {}
        self.update_var = lambda x, y: None
        self.update_queue = lambda x: None
        self.run = False
        self.stop_str = "__--$$stop_process$$--__"

    def can_stop(self):
        return len(self.out_dict) == 0

    def __call__(self, *args, **kwargs):
        self.run = True

        def done():
            while self.run:
                stop_pid = []
                old_var = list(self.var_dict.keys())
                for out in self.out_dict:
                    output: Queue = self.out_dict[out]
                    if output.empty():
                        continue
                    dict_index = f'var_{len(self.var_dict)}'
                    get_out = output.get()
                    if get_out == self.stop_str:
                        stop_pid.append(out)
                    else:
                        self.var_dict[dict_index] = get_out
                        self.var_from[dict_index] = out
                if old_var != list(self.var_dict.keys()):
                    self.update_var(self.var_dict, self.var_from)
                if stop_pid:
                    for i in stop_pid:
                        del self.in_dict[i]
                        del self.out_dict[i]
                    self.queue_list = list(self.in_dict.keys())
                    self.update_queue(self.queue_list.copy())

        t = threading.Thread(target=done)
        t.setDaemon(True)
        t.start()
        return self

    def stop(self):
        self.run = False

    def add_queue(self, inqueue, outqueue, name):
        self.stop()
        self.in_dict[name] = inqueue
        self.out_dict[name] = outqueue
        self.queue_list = list(self.in_dict.keys())
        self.update_queue(self.queue_list.copy())
        self.update_var(self.var_dict, self.var_from)

    def init(self, update_var, update_queue):
        self.update_var = update_var
        self.update_queue = update_queue
        self.update_queue(list(self.in_dict.keys()))
        self.update_var(self.var_dict, self.var_from)

    def put(self, value: str, index):
        name_space = self.var_dict.copy()
        name_space.update(globals())
        in_queue = self.in_dict[self.queue_list[index]]
        if value.startswith('put_var '):
            var_name = value[7:]
            in_queue.put(self.var_dict.get(var_name))
        elif value.startswith('put_eval '):
            in_queue.put(eval(value[8:]), name_space)
        elif value.startswith('file ') and value.startswith('.py'):
            try:
                with open(value[4:], 'r') as f:
                    code_file = f.read()
                new_name_space = name_space
                exec(code_file, new_name_space)
                in_queue.put(new_name_space.copy())
            except BaseException as e:
                in_queue.put(str(e))
        else:
            in_queue.put(value)


queue_controller = QueueController()


def progress_bar(func):
    def make_bar(*agrs, **kwargs):
        SCREEN.update()
        in_queue: Queue
        out_queue: Queue
        in_queue, out_queue = func(*agrs, **kwargs)
        pid = out_queue.get()
        name = func.__name__
        queue_controller.add_queue(in_queue, out_queue, f'{name}_{pid}')
        progress_screen = tkinter.Toplevel()
        progress_screen.title('系统持续加载中...')
        progress_screen.geometry("+10+10")  # 设置所在位置
        progress = ttk.Progressbar(
            progress_screen, orient="horizontal", length=300, mode="determinate"
        )
        progress.pack()
        progress_screen.resizable(width=False, height=False)
        progress["maximum"] = 10
        progress["value"] = 0
        i = 0
        a = 10
        while out_queue.empty():
            i += 1
            a += 1
            try:
                progress["value"] = i
                progress["maximum"] = a
                progress_screen.update()
            except TclError:
                pass
            SCREEN.update()
            time.sleep(0.015)
        try:
            progress_screen.title(out_queue.get())
            progress["value"] = a
            progress_screen.update()
            time.sleep(0.5)
            progress_screen.destroy()
        except TclError:
            pass
        queue_controller()

    return make_bar


def draftboard_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from draftboard import draw_main
    out_queue.put('start')
    time.sleep(0.5)
    draw_main(in_queue, out_queue)


@progress_bar
def draftboard_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=draftboard_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def datascience_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from datascience import machine_learning
    out_queue.put('start')
    time.sleep(0.5)
    machine_learning(in_queue, out_queue)


@progress_bar
def datascience_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=datascience_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def functionmapping_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from funcsystem.map import function_mapping
    out_queue.put('start')
    time.sleep(0.5)
    function_mapping(in_queue, out_queue)


@progress_bar
def functionmapping_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=functionmapping_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def functionfactory_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from funcsystem.factory import function_factory_main
    out_queue.put('start')
    time.sleep(0.5)
    function_factory_main(in_queue, out_queue)


@progress_bar
def functionfactory_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=functionfactory_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def algebraicfactory_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from algebraicfactory import algebraic_factory_main
    out_queue.put('start')
    time.sleep(0.5)
    algebraic_factory_main(in_queue, out_queue)


@progress_bar
def algebraicfactory_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=algebraicfactory_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def machinelearner_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from machinelearning import machine_learning
    out_queue.put('start')
    time.sleep(0.5)
    machine_learning(in_queue, out_queue)


@progress_bar
def machinelearner_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=machinelearner_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def git_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from gitrepo import git_main
    out_queue.put('start')
    time.sleep(0.5)
    git_main(in_queue, out_queue)


@progress_bar
def git_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=git_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def crawler_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from crawler import crawler_main
    out_queue.put('start')
    time.sleep(0.5)
    crawler_main(in_queue, out_queue)


@progress_bar
def crawlef_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=crawler_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def system_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from system.gui import system_main
    out_queue.put('start')
    time.sleep(0.5)
    system_main(in_queue, out_queue)


@progress_bar
def system_run():  # 不需要进度条
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=system_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def queuer():
    global title_color, button_color, button_cursor
    queue_screen = tkinter.Toplevel()
    queue_screen.title('通信管理器')
    queue_screen.resizable(width=False, height=False)
    queue_screen.geometry(f'+30+30')
    font = ("黑体", 11)  # 设置字体

    def sent():
        nonlocal sent_text, queue_box
        value = sent_text.get()
        try:
            index = queue_box.curselection()[0]
        except IndexError:
            return
        queue_controller.put(value, index)

    width_b = 20
    height_b = 2
    a_x = 0
    a_y = 0
    sent_text = tkinter.Entry(queue_screen, width=width_b * 2)
    sent_text.grid(column=a_x, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    tkinter.Button(queue_screen, bg=button_color, text='发送', command=sent, font=font, width=10, height=height_b)\
        .grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    a_y += 1
    queue_box = tkinter.Listbox(queue_screen, height=height_b * 8)
    queue_box.grid(column=a_x, row=a_y, columnspan=3, rowspan=8, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)
    a_x += 3
    a_y = 0
    var_box = tkinter.Listbox(queue_screen, width=width_b * 3, height=height_b * 9)
    var_box.grid(column=a_x, row=a_y, columnspan=3, rowspan=9, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    def update_queue_box(queue_list):
        try:
            queue_box.delete(0, tkinter.END)
            queue_box.insert(0, *queue_list)
        except TclError:
            pass

    def update_var_box(var_dict, var_from):
        var = []
        for name in var_dict:
            var.append(f'{name}[{var_from[name]}] : {var_dict[name]}')
        try:
            var_box.delete(0, tkinter.END)
            var_box.insert(0, *var)
        except TclError:
            pass

    queue_controller.init(update_var_box, update_queue_box)


def to_website():
    SCREEN.update()
    webbrowser.open('https://cotan.songzh.website/')


def close():
    global SCREEN
    if not queue_controller.can_stop():
        tkinter.messagebox.showinfo('操作不被允许', '请先关闭其他模块。')
    else:
        SCREEN.destroy()


def cotan_main():
    global SCREEN, title_color, button_color, button_cursor
    SCREEN = DragWindow(alpha=0.97, width=1200, height=800)
    font1 = tkfont.Font(family='Comic Sans MS', size=20, weight=tkfont.BOLD)
    font2 = tkfont.Font(family='Comic Sans MS', size=16, weight=tkfont.BOLD)
    font3 = tkfont.Font(family='Comic Sans MS', size=10)
    font4 = tkfont.Font(family='Comic Sans MS', size=50, weight=tkfont.BOLD)
    SCREEN.title('')
    SCREEN.resizable(width=False, height=False)
    SCREEN.geometry(f'1200x800+30+30')
    # 渲染白色
    frame = tkinter.Frame(SCREEN, width=1200, height=800, bg='#FFFFFF')
    frame.pack()

    # 图片
    canvas = tkinter.Canvas(
        frame,
        bd=0,
        width=1000,
        height=800,
        highlightthickness=0)
    bg_image = ImageTk.PhotoImage(Image.open('Pic/Night2.jpg'))
    canvas.create_image(500, 400, image=bg_image)
    canvas.grid(column=1, row=0, sticky=tkinter.S + tkinter.N, rowspan=20)
    # 标题
    tkinter.Label(
        frame,
        text='CoTan~科学计算',
        width=20,
        bg='#FFFFFF',
        font=font1).grid(
        column=0,
        row=0,
        sticky=tkinter.N)  # 设置说明
    tkinter.Label(
        frame,
        text='CoTan学术',
        bg=title_color,
        font=font2).grid(
        column=0,
        row=1,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        frame,
        text='CoTan社区',
        cursor=button_cursor,
        height=2,
        font=font3,
        bg=button_color,
        command=to_website,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=2,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='寄忆草稿板',
        cursor=button_cursor,
        command=draftboard_run,
        height=2,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=3,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='自动化网页',
        cursor=button_cursor,
        command=crawlef_run,
        height=1,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=4,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='Git仓库控制器',
        cursor=button_cursor,
        command=git_run,
        height=1,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=5,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    title_color = '#FFFAFA'
    tkinter.Label(
        frame,
        text='数学系统',
        bg=title_color,
        font=font2).grid(
        column=0,
        row=6,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        frame,
        text='函数测绘',
        cursor=button_cursor,
        command=functionmapping_run,
        height=2,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=7,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='函数工厂',
        cursor=button_cursor,
        command=functionfactory_run,
        height=2,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=8,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='代数工厂',
        cursor=button_cursor,
        command=algebraicfactory_run,
        height=2,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=9,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='数据科学',
        cursor=button_cursor,
        command=datascience_run,
        height=1,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=10,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='机器学习',
        cursor=button_cursor,
        command=machinelearner_run,
        height=1,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=11,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    title_color = '#F5FFFA'
    tkinter.Label(
        frame,
        text='物化系统',
        bg=title_color,
        font=font2).grid(
        column=0,
        row=12,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        frame,
        text='几何车间',
        cursor=button_cursor,
        height=2,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=13,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='物理车间',
        cursor=button_cursor,
        height=2,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=14,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='化学车间',
        cursor=button_cursor,
        height=1,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=15,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='实验室管理',
        cursor=button_cursor,
        height=1,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=16,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    title_color = '#F8F8FF'
    tkinter.Label(
        frame,
        text='其他工具',
        bg=title_color,
        font=font2).grid(
        column=0,
        row=17,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        frame,
        text='系统管理',
        cursor=button_cursor,
        command=system_run,
        height=1,
        font=font3,
        bg=button_color,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=18,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        frame,
        text='通信管理器',
        cursor=button_cursor,
        height=1,
        font=font3,
        bg=button_color,
        command=queuer,
        activebackground=title_color,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=19,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Label(
        frame,
        text='',
        bg='#FFFFFF',
        font=font2,
        height=5).grid(
        column=0,
        row=20,
        sticky=tkinter.W +
        tkinter.E)
    canvas.create_text(500, 750, text='CoTan~别来无恙', font=font4, fill='#FFFFE0')
    SCREEN.protocol("WM_DELETE_WINDOW", close)
    SCREEN.mainloop()


if __name__ == "__main__":
    freeze_support()
    cotan_main()
