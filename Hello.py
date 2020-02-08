print('启动')
from time import time
print('开始加载')
start = time()
import tkinter
print(f'图形加载完毕...')
import tkinter.font as tkFont
print(f'字体加载完毕...')
from PIL import ImageTk, Image
print(f'图片加载完毕...')
import CGB,HSCH,DSGC
from New_TK import DragWindow
from multiprocessing import Process
print(f'加载完毕...{round(time() - start,3)}s')

def Draw():
    global top,HTB
    HTB = Process(target=CGB.Draw)
    HTB.start()
    # top.destroy()
    # CGB.Draw()
    # Main()

def Hsch():
    global top,CH
    CH = Process(target=HSCH.Func_Control)
    CH.start()
    # top.destroy()
    # HSCH.Func_Control()
    # Main()

def HSGC():
    global top,HsGC
    HsGC = Process(target=HSCH.Advanced_Control)
    HsGC.start()
    # top.destroy()
    # HSCH.Advanced_Control()
    # Main()

def Dsgc():
    global top,DsGC
    DsGC = Process(target=DSGC.Alg)
    DsGC.start()
    # top.destroy()
    # DSGC.Alg()
    # Main()

def Main():
    global top
    # top = tkinter.Tk()  # 设置屏幕
    top = DragWindow(alpha=0.97,width=1200,height=800)
    ft = tkFont.Font(family='Comic Sans MS', size=20, weight=tkFont.BOLD)
    ft1 = tkFont.Font(family='Comic Sans MS', size=16, weight=tkFont.BOLD)
    ft2 = tkFont.Font(family='Comic Sans MS', size=10)
    ft3 = tkFont.Font(family='Comic Sans MS', size=50, weight=tkFont.BOLD)
    top.title('')
    top.resizable(width=False, height=False)
    top.geometry(f'1200x800+30+30')

    #渲染白色
    F1 = tkinter.Frame(top, width=1200, height=800, bg='#FFFFFF')
    F1.pack()

    #图片
    canvas = tkinter.Canvas(F1,bd=0, width=1000, height=800,highlightthickness=0)
    photo = ImageTk.PhotoImage(Image.open('Pic/Night2.jpg'))
    canvas.create_image(500, 400, image=photo)
    canvas.grid(column=1, row=0,sticky=tkinter.S + tkinter.N,rowspan =20)
    abg = '#F0FFFF'
    bg = '#FFFFFF'
    bc = 'tcross'
    #标题
    tkinter.Label(F1, text='CoTan~NOTE', width=20,bg='#FFFFFF', font=ft).grid(column=0, row=0,sticky=tkinter.N)  # 设置说明
    tkinter.Label(F1, text='私人笔记',bg=abg,font=ft1).grid(column=0, row=1,sticky=tkinter.W + tkinter.E)
    tkinter.Button(F1,text='Markdown笔记',cursor=bc,height=2,font=ft2,bg=bg,activebackground=abg,bd=0,justify=tkinter.LEFT).grid(column =0,row = 2,sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='画图板',cursor=bc,command=Draw, height=2, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=3,sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='爬虫系统',cursor=bc, height=1, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=4,sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='我的寄忆',cursor=bc, height=1, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=5,sticky=tkinter.N + tkinter.E + tkinter.W)

    abg = '#FFFAFA'
    tkinter.Label(F1, text='数学系统', bg=abg, font=ft1).grid(column=0, row=6,sticky=tkinter.W + tkinter.E)
    tkinter.Button(F1,text='函数测绘',cursor=bc,command=Hsch,height=2,font=ft2,bg=bg,activebackground=abg,bd=0,justify=tkinter.LEFT).grid(column =0,row = 7,sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='函数工厂',cursor=bc,command=HSGC, height=2, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=8,sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='代数工厂',cursor=bc,command=Dsgc, height=2, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=9,sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='机器学习',cursor=bc, height=1, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=10,sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='几何分析',cursor=bc, height=1, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=11,sticky=tkinter.N + tkinter.E + tkinter.W)

    abg='#F5FFFA'
    tkinter.Label(F1, text='物化系统', bg=abg, font=ft1).grid(column=0, row=12, sticky=tkinter.W + tkinter.E)
    tkinter.Button(F1, text='平面物体分析',cursor=bc, height=2, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=13,
                                                                                                       sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='平面受力分析',cursor=bc, height=2, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=14,
                                                                                                       sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='实验数据拟合',cursor=bc, height=1, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0,
                                                                                                           row=15,
                                                                                                           sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='化学反应预测',cursor=bc, height=1, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0,
                                                                                                       row=16,
                                                                                                       sticky=tkinter.N + tkinter.E + tkinter.W)
    abg = '#F8F8FF'
    tkinter.Label(F1, text='其他工具', bg=abg, font=ft1).grid(column=0, row=17, sticky=tkinter.W + tkinter.E)
    tkinter.Button(F1, text='系统扩展',cursor=bc, height=1, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=18,
                                                                                                       sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Button(F1, text='Tensorflew深度学习',cursor=bc, height=1, font=ft2, bg=bg,activebackground=abg, bd=0, justify=tkinter.LEFT).grid(column=0, row=19,
                                                                                                       sticky=tkinter.N + tkinter.E + tkinter.W)
    tkinter.Label(F1, text='', bg='#FFFFFF', font=ft1,height=5).grid(column=0, row=20, sticky=tkinter.W + tkinter.E)
    canvas.create_text(500,750,text='CoTan~别来无恙',font=ft3,fill='#FFFFE0')
    top.mainloop()

if __name__ == "__main__":
    HTB = Process(target=CGB.Draw)
    CH = Process(target=HSCH.Func_Control)
    HsGC = Process(target=HSCH.Advanced_Control)
    DsGC = Process(target=DSGC.Alg)
    Main()
    # HTB.join()
    # CH.join()
    # HsGC.join()
    # DsGC.join()