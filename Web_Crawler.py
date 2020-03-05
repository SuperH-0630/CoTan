import Crawler_controller
import os
import tkinter
from tkinter.filedialog import askdirectory
import re
import threading
import time

def Main():
    global top,Git,PATH,bg,bbg,fg,cookies_list
    PATH = os.getcwd()
    top = tkinter.Tk()
    cookies_list = []
    bg = '#FFFAFA'  # 主颜色
    bbg = '#FFFAFA'  # 按钮颜色
    fg = '#000000'  # 文字颜色
    top["bg"] = bg
    FONT = ('黑体', 11)  # 设置字体
    top.title('CoTan仓库管理器')
    top.resizable(width=False, height=False)
    top.geometry('+10+10')  # 设置所在位置

    width_B = 13  # 标准宽度
    height_B = 2
    a_y = 0
    a_x = 0

    tkinter.Button(top, bg=bbg, fg=fg, text='添加url',command=add_url , font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除url',command=del_url , font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='应用过滤机制', font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global URL_BOX,URL_Input,Func_BOX
    a_y += 1
    tkinter.Label(top, text='添加url:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    URL_Input = tkinter.Entry(top, width=width_B * 2)
    URL_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    URL_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 3)
    URL_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=3, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 3
    tkinter.Button(top, bg=bbg, fg=fg, text='HTTPS过滤',command=add_filter_func_HTTPS, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='WWW过滤',command=add_filter_func_WWW, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除过滤',command=del_func, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='自定义过滤',command=add_filter_func_HTTPS, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空过滤', font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Func_BOX,cookies_fixed
    a_y += 1
    Func_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)
    Func_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    global wait_Func_BOX,Wait_Input,cookies_BOX

    a_y += 2
    tkinter.Button(top, bg=bbg, fg=fg, text='执行网页下载',command=startDownloader, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='显式等待',command=add_time_wait, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    Wait_Input = tkinter.Entry(top, width=width_B)
    Wait_Input.grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 3
    tkinter.Button(top, bg=bbg, fg=fg, text='自定义等待策略',command=add_filter_func_HTTPS, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除等待策略',command=del_waitfunc, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空等待策略',command=del_func, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    wait_Func_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)
    wait_Func_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 2
    cookies_fixed = tkinter.Variable()
    tkinter.Label(top, text='【曲奇监视】', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='固定曲奇',
                        variable=cookies_fixed).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)
    cookies_fixed.set('0')

    a_y += 1
    cookies_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)
    cookies_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 2
    tkinter.Button(top, bg=bbg, fg=fg, text='清空曲奇',command=Tra_cookies, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='更新曲奇',command=Update_cookies, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除曲奇',command=Del_cookies, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global cookies_Input,PAGE_BOX
    a_y += 1
    cookies_Input = tkinter.Entry(top, width=width_B * 2)
    cookies_Input.grid(column=a_x, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='添加曲奇',command=Add_cookies, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    cookies_fixed = tkinter.Variable()
    tkinter.Label(top, text='【已存储页面】', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(
        column=a_x,row=a_y,columnspan=3,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)

    a_y += 1
    PAGE_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 2)
    PAGE_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=2, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    top.update()#要预先update一下，否则会卡住
    global url,loader
    save_dir = askdirectory(title='选择项目位置')#项目位置
    url = Crawler_controller.url(save_dir,save_dir)
    loader = Crawler_controller.Page_Downloader(url,save_dir)
    top.mainloop()

def PAGE_BOX_Update(PAGE_list):
    global PAGE_BOX
    PAGE_BOX.delete(0,tkinter.END)
    PAGE_BOX.insert(0,*PAGE_list)

def Update_cookies():
    global cookies_BOX,cookies_list,cookies_Input
    cookies = eval(cookies_Input.get(),{})
    if cookies_fixed.get() == '0':return False
    try:
        name = cookies_list[cookies_BOX.curselection()[0]].get('name')
        loader.update_cookies(name,cookies)
        cookies_fixed.set('0')
    except:
        pass

def Add_cookies():
    global cookies_BOX,cookies_list,cookies_Input
    cookies = eval(cookies_Input.get(),{})
    if cookies_fixed.get() == '0':return False
    try:
        loader.Add_cookies(cookies)
        cookies_fixed.set('0')
    except:
        raise

def Tra_cookies():
    global cookies_BOX,cookies_list
    if cookies_fixed.get() == '0':return False
    try:
        loader.Tra_cookies()
        cookies_fixed.set('0')
    except:
        pass

def Del_cookies():
    global cookies_BOX,cookies_list
    if cookies_fixed.get() == '0':return False
    try:
        name = cookies_list[cookies_BOX.curselection()[0]].get('name')
        print(name)
        loader.Del_cookies(name)
        cookies_fixed.set('0')
    except:
        pass

def cookies_BOX_Update(cookies):
    global cookies_BOX,cookies_list
    if cookies_fixed.get() == '0':
        cookies_list = cookies
        cookies_BOX.delete(0,tkinter.END)
        cookies_BOX.insert(0,*cookies)

def add_time_wait():#显式等待一定s
    global url,Wait_Input
    times = float(Wait_Input.get())
    def wait_time(*args):
        time.sleep(times)
        return True,f'After_{time}s'
    loader.Add_func(wait_time,f'wait {times}s')
    update_Wait_Input()

def del_waitfunc():#删除策略
    global wait_Func_BOX
    index = wait_Func_BOX.curselection()[0]
    loader.Del_func(index)
    update_Wait_Input()

def update_Wait_Input():
    global loader,wait_Func_BOX
    wait_Func_BOX.delete(0,tkinter.END)
    wait_Func_BOX.insert(tkinter.END,*loader.return_func())

def startDownloader():
    def startLoader():
        global loader
        loader.strat_urlGet()
        loader.Logical_operation(cookies_BOX_Update,PAGE_BOX_Update)
        loader.save_Page()
    new = threading.Thread(target=startLoader)
    new.start()
    update_URLBOX()

def add_filter_func_HTTPS():
    global url
    url.Add_func(lambda url:re.match(re.compile('^https://'),url),'HTTPS过滤')
    update_Func_BOX()

def add_filter_func_WWW():
    global url
    url.Add_func(lambda url:re.match(re.compile('.*www\.'),url),'www过滤')
    update_Func_BOX()

def del_func():
    global URL_BOX
    index = Func_BOX.curselection()[0]
    url.Del_func(index)
    update_Func_BOX()

def update_Func_BOX():
    global url,Func_BOX
    Func_BOX.delete(0,tkinter.END)
    Func_BOX.insert(tkinter.END,*url.return_func())

def del_url():
    global URL_BOX
    index = URL_BOX.curselection()[0]
    url.del_url(index)
    update_URLBOX()

def add_url():
    global URL_Input,url
    new_url = URL_Input.get()
    if new_url == '':return
    url.add_url(new_url)
    update_URLBOX()

def update_URLBOX():
    global url,URL_BOX
    URL_BOX.delete(0,tkinter.END)
    URL_BOX.insert(tkinter.END,*url.return_url())


if __name__ == "__main__":
    Main()