from multiprocessing import Process
from _tkinter import TclError
import tkinter
from tkinter import ttk
import tkinter.font as tkfont
from PIL import ImageTk, Image
import time

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


def progress_bar(func):
    def make_bar(*agrs, **kwargs):
        func(*agrs, **kwargs)
        progress_screen = tkinter.Toplevel()
        progress_screen.title('系统持续加载中...')
        progress_screen.geometry("+10+10")  # 设置所在位置
        progress = ttk.Progressbar(
            progress_screen, orient="horizontal", length=300, mode="determinate"
        )
        progress.pack()
        progress_screen.resizable(width=False, height=False)
        progress["maximum"] = 50
        progress["value"] = 0
        for i in range(50):
            try:
                progress["value"] = i + 1
                progress_screen.update()
            except TclError:
                pass
            SCREEN.update()
            time.sleep(0.015)
        progress_screen.destroy()
    return make_bar


def draftboard_main():
    from draftboard import draw_main
    draw_main()


@progress_bar
def draftboard_run():
    Process(target=draftboard_main).start()


def datascience_main():
    from datascience import machine_learning
    machine_learning()


@progress_bar
def datascience_run():
    Process(target=datascience_main).start()


def functionmapping_main():
    from funcsystem.map import function_mapping
    print('函数测绘加载完毕...')
    function_mapping()


@progress_bar
def functionmapping_run():
    Process(target=functionmapping_main).start()


def functionfactory_main():
    from funcsystem.factory import function_factory_main
    print('函数工厂加载完毕...')
    function_factory_main()


@progress_bar
def functionfactory_run():
    Process(target=functionfactory_main).start()


def algebraicfactory_main():
    from algebraicfactory import algebraic_factory_main
    algebraic_factory_main()


@progress_bar
def algebraicfactory_run():
    Process(target=algebraicfactory_main).start()


def machinelearner_main():
    from machinelearning import machine_learning
    machine_learning()


@progress_bar
def machinelearner_run():
    Process(target=machinelearner_main).start()


def git_main():
    from gitrepo import git_main
    git_main()


@progress_bar
def git_run():
    Process(target=git_main).start()


def crawler_main():
    from crawler import crawler_main
    crawler_main()


@progress_bar
def crawlef_run():
    Process(target=crawler_main).start()


def system_main():
    from system.gui import system_main
    system_main()


def system_run():  # 不需要进度条
    Process(target=system_main).start()


def cotan_main():
    global SCREEN
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
    title_color = '#F0FFFF'
    button_color = '#FFFFFF'
    button_cursor = 'tcross'
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
        text='寄忆学术',
        bg=title_color,
        font=font2).grid(
        column=0,
        row=1,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        frame,
        text='我的寄忆',
        cursor=button_cursor,
        height=2,
        font=font3,
        bg=button_color,
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
        text='系统扩展',
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
        text='Tensorflew深度学习',
        cursor=button_cursor,
        height=1,
        font=font3,
        bg=button_color,
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
    SCREEN.mainloop()


if __name__ == "__main__":
    cotan_main()
