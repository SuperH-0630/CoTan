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
    top.title('CoTan自动化网页')
    top.resizable(width=False, height=False)
    top.geometry('+10+10')  # 设置所在位置

    width_B = 13  # 标准宽度
    height_B = 2
    a_y = 0
    a_x = 0

    tkinter.Button(top, bg=bbg, fg=fg, text='添加url对象',command=add_url , font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除url对象',command=del_url , font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='应用过滤机制', font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global URL_BOX,URL_Input,Func_BOX
    a_y += 1
    tkinter.Label(top, text='添加url:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    URL_Input = tkinter.Entry(top, width=width_B * 2)
    URL_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    URL_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 5)
    URL_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 5
    tkinter.Button(top, bg=bbg, fg=fg, text='HTTPS过滤器',command=add_filter_func_HTTPS, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='WWW过滤器',command=add_filter_func_WWW, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除过滤器',command=del_func, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='自定义过滤器',command=add_filter_func_HTTPS, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空过滤器', font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Func_BOX,cookies_fixed
    a_y += 1
    Func_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)
    Func_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    global wait_Func_BOX,Wait_Input,cookies_BOX
    a_y += 4
    tkinter.Button(top, bg=bbg, fg=fg, text='单点爬虫运行',command=startDownloader, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='爬虫运行',command=startDownloader, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='单点爬虫停止',command=startDownloader, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    cookies_fixed = tkinter.Variable()
    tkinter.Label(top, text='【曲奇监视】', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(
        column=a_x+1,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='固定曲奇',
                        variable=cookies_fixed).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)
    cookies_fixed.set('0')

    a_y += 1
    cookies_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 7)
    cookies_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=7, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 7
    tkinter.Button(top, bg=bbg, fg=fg, text='清空曲奇',command=Tra_cookies, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='更新曲奇',command=Update_cookies, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除曲奇',command=Del_cookies, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global cookies_Input,PAGE_BOX
    a_y += 1
    cookies_Input = tkinter.Entry(top, width=width_B * 3)
    cookies_Input.grid(column=a_x, row=a_y, columnspan=3, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='添加曲奇',command=Add_cookies, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Button(top, bg=bbg, fg=fg, text='根据id搜查',command=lambda :Page_Parser_addFindFunc('id'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='根据name搜查',command=lambda :Page_Parser_addFindFunc('name'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='根据class搜查',command=lambda :Page_Parser_addFindFunc('class'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='根据xpath搜查',command=lambda :Page_Parser_addFindFunc('xpath'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='根据css搜查',command=lambda :Page_Parser_addFindFunc('css'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='根据元素名搜查',command=lambda :Page_Parser_addFindFunc('tag'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global search_all,search_Input,Parser_Func_BOX
    a_y += 1
    search_all = tkinter.Variable()
    tkinter.Button(top, bg=bbg, fg=fg, text='根据link搜查',command=lambda :Page_Parser_addFindFunc('link'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='link模糊搜查',command=lambda :Page_Parser_addFindFunc('partial_link'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='匹配全部',
                        variable=search_all).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)
    search_all.set('0')

    a_y += 1
    tkinter.Label(top, text='搜查参数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    search_Input = tkinter.Entry(top, width=width_B * 2)
    search_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    Parser_Func_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)
    Parser_Func_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    top.update()#要预先update一下，否则会卡住
    global url,loader,Page_Parser
    save_dir = askdirectory(title='选择项目位置')#项目位置
    url = Crawler_controller.url(save_dir,save_dir)
    loader = Crawler_controller.Page_Downloader(url,save_dir)
    Page_Parser = Crawler_controller.Page_Parser(loader)
    top.mainloop()

def Page_Parser_addFindFunc(func):
    global search_all, search_Input,Page_Parser
    not_all = not(bool(search_all.get()))
    search = search_Input.get()
    FUNC = {'id':Page_Parser.find_ID,'name':Page_Parser.find_name,'class':Page_Parser.find_class,
            'xpath':Page_Parser.find_xpath,'css':Page_Parser.find_css,'tag':Page_Parser.find_tag_name,
            'link':Page_Parser.find_link_text,'partial_link':Page_Parser.find_partial_link_text}.get(
        func,Page_Parser.find_ID)
    FUNC(search,not_all)
    Update_Parser_Func_BOX()

def Update_Parser_Func_BOX():
    global Parser_Func_BOX,Page_Parser
    Parser_Func_BOX.delete(0,tkinter.END)
    Parser_Func_BOX.insert(tkinter.END, *Page_Parser.return_func())

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

def startDownloader():
    def startLoader():
        global loader,Page_Parser
        loader.strat_urlGet(func_cookie=cookies_BOX_Update)
        Page_Parser = Crawler_controller.Page_Parser(loader)

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