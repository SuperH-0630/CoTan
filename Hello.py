from multiprocessing import Process


def painting_board():
    from CGB import draw_main
    draw_main()


def Draw():
    global top, HTB
    HTB = Process(target=painting_board)
    HTB.start()


def Data_Science():
    from Data_Science import machine_learning
    machine_learning()


def SJKX():
    global top, SJ
    SJ = Process(target=Data_Science)
    SJ.start()


def Function_mapping():
    from HSCH import Func_Control
    Func_Control()


def Hsch():
    global top, CH
    CH = Process(target=Function_mapping)
    CH.start()


def Function_factory():
    from HSCH import Advanced_Control
    Advanced_Control()


def HSGC():
    global top, HsGC
    HsGC = Process(target=Function_factory)
    HsGC.start()


def Algebraic_factory():
    from DSGC import algebraic_factory_main
    algebraic_factory_main()


def Dsgc():
    global top, DsGC
    DsGC = Process(target=Algebraic_factory)
    DsGC.start()


def Machine_Learning():
    from Machine_learning_analysis import Main
    Main()


def MLA():
    global top, Mla
    Mla = Process(target=Machine_Learning)
    Mla.start()


def Git_Ctrl():
    from Git_controller import git_main
    git_main()


def GIT_Ctrl():
    global top, Git_Ctrl
    Git = Process(target=Git_Ctrl)
    Git.start()


def Crawler_Main():
    from Crawler import Main
    Main()


def Crawlef_Run():
    global top, crawlef
    crawlef = Process(target=Crawler_Main)
    crawlef.start()


def Main():
    global top
    import tkinter
    import tkinter.font as tkFont
    from PIL import ImageTk, Image
    from New_TK import DragWindow
    print('加载完毕')
    top = DragWindow(alpha=0.97, width=1200, height=800)
    ft = tkFont.Font(family='Comic Sans MS', size=20, weight=tkFont.BOLD)
    ft1 = tkFont.Font(family='Comic Sans MS', size=16, weight=tkFont.BOLD)
    ft2 = tkFont.Font(family='Comic Sans MS', size=10)
    ft3 = tkFont.Font(family='Comic Sans MS', size=50, weight=tkFont.BOLD)
    top.title('')
    top.resizable(width=False, height=False)
    top.geometry(f'1200x800+30+30')

    # 渲染白色
    F1 = tkinter.Frame(top, width=1200, height=800, bg='#FFFFFF')
    F1.pack()

    # 图片
    canvas = tkinter.Canvas(
        F1,
        bd=0,
        width=1000,
        height=800,
        highlightthickness=0)
    photo = ImageTk.PhotoImage(Image.open('Pic/Night2.jpg'))
    canvas.create_image(500, 400, image=photo)
    canvas.grid(column=1, row=0, sticky=tkinter.S + tkinter.N, rowspan=20)
    abg = '#F0FFFF'
    bg = '#FFFFFF'
    bc = 'tcross'
    # 标题
    tkinter.Label(
        F1,
        text='CoTan~科学计算',
        width=20,
        bg='#FFFFFF',
        font=ft).grid(
        column=0,
        row=0,
        sticky=tkinter.N)  # 设置说明
    tkinter.Label(
        F1,
        text='寄忆学术',
        bg=abg,
        font=ft1).grid(
        column=0,
        row=1,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        F1,
        text='我的寄忆',
        cursor=bc,
        height=2,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=2,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='寄忆草稿版',
        cursor=bc,
        command=Draw,
        height=2,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=3,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='自动化网页',
        cursor=bc,
        command=Crawlef_Run,
        height=1,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=4,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='Git仓库控制器',
        cursor=bc,
        command=GIT_Ctrl,
        height=1,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=5,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    abg = '#FFFAFA'
    tkinter.Label(
        F1,
        text='数学系统',
        bg=abg,
        font=ft1).grid(
        column=0,
        row=6,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        F1,
        text='函数测绘',
        cursor=bc,
        command=Hsch,
        height=2,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=7,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='函数工厂',
        cursor=bc,
        command=HSGC,
        height=2,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=8,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='代数工厂',
        cursor=bc,
        command=Dsgc,
        height=2,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=9,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='数据科学',
        cursor=bc,
        command=SJKX,
        height=1,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=10,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='机器学习',
        cursor=bc,
        command=MLA,
        height=1,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=11,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)

    abg = '#F5FFFA'
    tkinter.Label(
        F1,
        text='物化系统',
        bg=abg,
        font=ft1).grid(
        column=0,
        row=12,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        F1,
        text='几何车间',
        cursor=bc,
        height=2,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=13,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='物理车间',
        cursor=bc,
        height=2,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=14,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='化学车间',
        cursor=bc,
        height=1,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=15,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='实验室管理',
        cursor=bc,
        height=1,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=16,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    abg = '#F8F8FF'
    tkinter.Label(
        F1,
        text='其他工具',
        bg=abg,
        font=ft1).grid(
        column=0,
        row=17,
        sticky=tkinter.W +
        tkinter.E)
    tkinter.Button(
        F1,
        text='系统扩展',
        cursor=bc,
        height=1,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=18,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Button(
        F1,
        text='Tensorflew深度学习',
        cursor=bc,
        height=1,
        font=ft2,
        bg=bg,
        activebackground=abg,
        bd=0,
        justify=tkinter.LEFT).grid(
        column=0,
        row=19,
        sticky=tkinter.N +
        tkinter.E +
        tkinter.W)
    tkinter.Label(
        F1,
        text='',
        bg='#FFFFFF',
        font=ft1,
        height=5).grid(
        column=0,
        row=20,
        sticky=tkinter.W +
        tkinter.E)
    canvas.create_text(500, 750, text='CoTan~别来无恙', font=ft3, fill='#FFFFE0')
    top.mainloop()


if __name__ == "__main__":
    Main()
