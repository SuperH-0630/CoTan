from multiprocessing import Process
import tkinter
from tkinter import ttk
import tkinter.font as tkfont
from PIL import ImageTk, Image
import time

from drag import DragWindow

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
    def progress_bar(*agrs, **kwargs):
        func(*agrs, **kwargs)
        progress_screen = tkinter.Toplevel()
        progress_screen.title('系统持续加载中...')
        progress_screen.geometry("+10+10")  # 设置所在位置
        mpb = ttk.Progressbar(
            progress_screen, orient="horizontal", length=300, mode="determinate"
        )
        mpb.pack()
        progress_screen.resizable(width=False, height=False)
        mpb["maximum"] = 50
        mpb["value"] = 0
        for i in range(50):
            try:
                mpb["value"] = i + 1
                progress_screen.update()
            except BaseException:
                pass
            SCREEN.update()
            time.sleep(0.015)
        progress_screen.destroy()
    return progress_bar


def draftboard_main():
    from draftboard import draw_main
    draw_main()


@progress_bar
def draftboard_run():
    global SCREEN, draftboard_start
    draftboard_start = Process(target=draftboard_main)
    draftboard_start.start()


def datascience_main():
    from datascience import machine_learning
    machine_learning()


@progress_bar
def datascience_run():
    global SCREEN, datascience_start
    datascience_start = Process(target=datascience_main)
    datascience_start.start()


def functionmapping_main():
    from funcsystem.map import function_mapping
    function_mapping()


@progress_bar
def functionmapping_run():
    global SCREEN, functionmapping_start
    functionmapping_start = Process(target=functionmapping_main)
    functionmapping_start.start()


def functionfactory_main():
    from funcsystem.factory import function_factory_main
    function_factory_main()


@progress_bar
def functionfactory_run():
    global SCREEN, functionfactory_start
    functionfactory_start = Process(target=functionfactory_main)
    functionfactory_start.start()


def algebraicfactory_main():
    from algebraicfactory import algebraic_factory_main
    algebraic_factory_main()


@progress_bar
def algebraicfactory_run():
    global SCREEN, algebraicfactory_start
    algebraicfactory_start = Process(target=algebraicfactory_main)
    algebraicfactory_start.start()


def machinelearner_main():
    from machinelearning import machine_learning
    machine_learning()


@progress_bar
def machinelearner_run():
    global SCREEN, machinelearner_start
    machinelearner_start = Process(target=machinelearner_main)
    machinelearner_start.start()


def git_main():
    from gitrepo import git_main
    git_main()


@progress_bar
def git_run():
    global SCREEN, git_start
    git_start = Process(target=git_main)
    git_start.start()


def crawler_main():
    from crawler import crawler_main
    crawler_main()


@progress_bar
def crawlef_run():
    crawlef_start = Process(target=crawler_main)
    crawlef_start.start()


def system_main():
    from system.gui import system_main
    system_main()


def system_run():  # 不需要进度条
    system_start = Process(target=system_main)
    system_start.start()


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
        text='寄忆草稿版',
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
