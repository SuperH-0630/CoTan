import Crawler_controller
import os
import tkinter
from tkinter.filedialog import askdirectory
import re
import threading
import time

def Main():
    global top,Git,PATH,bg,bbg,fg,cookies_list,Attributes_Dict,DataBase_list
    DataBase_list = []
    Attributes_Dict = {}
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

    global URL_ARGS,UA_Input,use_Cookies_Input,FUNC_Input,DATA_Input
    a_y += 1
    URL_ARGS = []
    lable = ['不加载js','不加载java','不加载插件']#复选框
    for i in range(3):
        URL_ARGS.append(tkinter.IntVar())
        tkinter.Checkbutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i],
                            variable=URL_ARGS[-1]).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    lable = ['第一次启动','隐藏网页','不加载图片']#复选框
    for i in range(3):
        URL_ARGS.append(tkinter.IntVar())
        tkinter.Checkbutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i],
                            variable=URL_ARGS[-1]).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_y += 1
    tkinter.Label(top, text='UA设置:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    UA_Input = tkinter.Entry(top, width=width_B * 2)
    UA_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='DATA:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    DATA_Input = tkinter.Entry(top, width=width_B * 2)
    DATA_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='请求方式:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    FUNC_Input = tkinter.Entry(top, width=width_B * 2)
    FUNC_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='Cookies:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    use_Cookies_Input = tkinter.Entry(top, width=width_B)
    use_Cookies_Input.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    URL_ARGS.append(tkinter.IntVar())
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='新启动网页',
                        variable=URL_ARGS[-1]).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)

    a_y += 1
    URL_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)
    URL_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 4
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
    Func_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 3)
    Func_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=3, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    global wait_Func_BOX,Wait_Input,cookies_BOX
    a_y += 3
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
    cookies_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)
    cookies_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 4
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

    global Var_Input,VarIndex_Input,Send_Input,UserPW_Input,SELE_Input,JS_Input,Time_Input
    a_y += 4
    tkinter.Label(top, text='操作元素:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Var_Input = tkinter.Entry(top, width=width_B * 2)
    Var_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='操作索引:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    VarIndex_Input = tkinter.Entry(top, width=width_B * 2)
    VarIndex_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='发送信息:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Send_Input = tkinter.Entry(top, width=width_B * 2)
    Send_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='认证用户名:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    UserName_Input = tkinter.Entry(top, width=width_B * 2)
    UserName_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='认证密码:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    UserPW_Input = tkinter.Entry(top, width=width_B * 2)
    UserPW_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='选择参数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    SELE_Input = tkinter.Entry(top, width=width_B * 2)
    SELE_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='等待时间:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Time_Input = tkinter.Entry(top, width=width_B * 2)
    Time_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='JavaScript:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    JS_Input = tkinter.Entry(top, width=width_B * 2)
    JS_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='发送字符',command=lambda :Page_Parser_addActionFunc('send_keys'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空字符',command=lambda :Page_Parser_addActionFunc('clear'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='提交表单',command=lambda :Page_Parser_addActionFunc('submit'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='点击按钮',command=lambda :Page_Parser_addActionFunc('click'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='取得源代码',command=lambda :Page_Parser_addActionFunc('get_Page'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='输出HTML',command=lambda :Page_Parser_addActionFunc('out'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='切换Frame(id)',command=Page_Parser_addFrameFunc_id, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='切换Frame',command=lambda :Page_Parser_addFindFunc('frame'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='定位焦点元素',command=lambda :Page_Parser_addFindFunc('active_element'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='捕获弹窗',command=lambda :Page_Parser_addFindFunc('alert'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='回到主Frame',command=lambda :Page_Parser_addFrameFunc_FP(False), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='回到父Frame',command=lambda :Page_Parser_addFrameFunc_FP(True), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='弹出框认证',command=lambda :Page_Parser_addActionFunc('User_Passwd'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='弹出框确定',command=lambda :Page_Parser_addActionFunc('accept'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='弹出框取消',command=lambda :Page_Parser_addActionFunc('dismiss'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='取消选择index',command=lambda :Page_Parser_addActionFunc('deselect_by_index'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='取消选择text',command=lambda :Page_Parser_addActionFunc('deselect_by_text'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='取消选择value',command=lambda :Page_Parser_addActionFunc('deselect_by_value'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='选择index',command=lambda :Page_Parser_addActionFunc('select_by_index'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='选择text',command=lambda :Page_Parser_addActionFunc('select_by_text'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='选择value',command=lambda :Page_Parser_addActionFunc('select_by_value'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='页面后退',command=lambda :Page_Parser_addActionFunc('back'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='页面刷新',command=lambda :Page_Parser_addActionFunc('refresh'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='页面前进',command=lambda :Page_Parser_addActionFunc('forward'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='暴力等待',command=lambda :Page_Parser_addActionFunc('wait_sleep'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='元素检查等待',command=lambda :Page_Parser_addActionFunc('set_wait'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='运行js',command=lambda :Page_Parser_addActionFunc('run_JS'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    global Func_Output,Status_Output,FuncValue_BOX
    Func_Output = tkinter.StringVar()
    Status_Output = tkinter.StringVar()
    tkinter.Label(top, text='正在执行:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    tkinter.Entry(top, width=width_B * 2, state=tkinter.DISABLED,textvariable=Func_Output).grid(
        column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='上一次状态:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    tkinter.Entry(top, width=width_B * 2, state=tkinter.DISABLED,textvariable=Status_Output).grid(
        column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    FuncValue_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 5)
    FuncValue_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    global CookiesName_Input,Cookies_Input,Tag_Input,AttributesName_Input,AttributesValue_Input
    global FindAllText_Input,text_re,attribute_re,limit_Input,recursive_Input,FindAllPATH_Input,Attributes_BOX

    a_y += 5
    tkinter.Label(top, text='cookies名:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    CookiesName_Input = tkinter.Entry(top, width=width_B * 2)
    CookiesName_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='cookies:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Cookies_Input = tkinter.Entry(top, width=width_B * 2)
    Cookies_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='定位标签:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y)
    Tag_Input = tkinter.Entry(top, width=width_B * 2)
    Tag_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='定位属性名:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y)
    AttributesName_Input = tkinter.Entry(top, width=width_B * 2)
    AttributesName_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    attribute_re = tkinter.IntVar()
    a_y += 1
    tkinter.Label(top, text='定位属性值:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y)
    AttributesValue_Input = tkinter.Entry(top, width=width_B)
    AttributesValue_Input.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='添加属性',command=add_Attributes, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除属性',command=del_Attributes, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空属性',command=tra_Attributes, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    Attributes_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 3)
    Attributes_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=3, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 3
    tkinter.Label(top, text='定位文本:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y)
    FindAllText_Input = tkinter.Entry(top, width=width_B)
    FindAllText_Input.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    recursive_Input = tkinter.IntVar()
    text_re = tkinter.IntVar()
    a_y += 1
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='递归查找',
                        variable=recursive_Input).grid(column=a_x, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='文本使用正则',
                        variable=text_re).grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='属性值使用正则',
                        variable=attribute_re).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)
    attribute_re.set(1)
    text_re.set('1')
    recursive_Input.set('1')

    a_y += 1
    tkinter.Label(top, text='查找个数:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y)
    limit_Input = tkinter.Entry(top, width=width_B * 2)
    limit_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='定位路径:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,
                                                                                                      row=a_y)
    FindAllPATH_Input = tkinter.Entry(top, width=width_B * 2)
    FindAllPATH_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='删除所有曲奇',command=lambda :Page_Parser_addActionFunc2('del_all_cookies'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除指定曲奇',command=lambda :Page_Parser_addActionFunc2('del_cookies'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='添加新的曲奇',command=lambda :Page_Parser_addActionFunc2('add_cookies'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='更新指定曲奇',command=lambda :Page_Parser_addActionFunc2('update_cookies'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='获得所有曲奇',command=lambda :Page_Parser_addActionFunc2('get_cookies'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='获得指定曲奇',command=lambda :Page_Parser_addActionFunc2('get_all_cookies'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='解析网页',command=lambda :Page_Parser_addActionFunc2('make_bs'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='根据标签定位',command=lambda :Page_Parser_addActionFunc2('findAll'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='根据文本定位',command=lambda :Page_Parser_addActionFunc2('findAll_by_text'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='获得子标签',command=lambda :Page_Parser_addActionFunc2('get_children'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='获得后代标签',command=lambda :Page_Parser_addActionFunc2('get_offspring'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='获得弟标签',command=lambda :Page_Parser_addActionFunc2('get_down'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='获得兄标签',command=lambda :Page_Parser_addActionFunc2('get_up'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='获得兄弟标签',command=lambda :Page_Parser_addActionFunc2('brothers'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='路径定位',command=lambda :Page_Parser_addActionFunc2('get_by_path'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【数据库操作】', bg=bg, fg=fg, font=FONT).grid(column=a_x, row=a_y,columnspan=3)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='元素式存入',command=lambda :to_Database(True), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='正则式存入',command=lambda :to_Database(False), font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='新增数据表',command=add_DataBase, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='删除数据表',command=remove_DataBase, font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='导出数据表',command=out, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='关闭数据表', command=close, font=FONT,
                   width=width_B, height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Data_Input,DataBase_BOX,DataName_Input
    a_y += 1
    tkinter.Label(top, text='数据存入格式:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Data_Input = tkinter.Entry(top, width=width_B * 2)
    Data_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='数据表名字:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    DataName_Input = tkinter.Entry(top, width=width_B * 2)
    DataName_Input.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    DataBase_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 3)
    DataBase_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=3, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 3
    tkinter.Button(top, bg=bbg, fg=fg, text='导出页面快照',command=lambda :Page_Parser_addActionFunc2('png'), font=FONT, width=width_B,height=height_B).grid(
        column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='NONE',command=out, font=FONT, width=width_B,height=height_B).grid(
        column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='NONE', command=close, font=FONT,
                   width=width_B, height=height_B).grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    top.update()#要预先update一下，否则会卡住
    global url,loader,Page_Parser,DataBase,save_dir
    save_dir = askdirectory(title='选择项目位置')#项目位置
    url = Crawler_controller.url(save_dir,save_dir)
    loader = Crawler_controller.Page_Downloader(url,save_dir)
    Page_Parser = Crawler_controller.Page_Parser(loader)
    DataBase = Crawler_controller.data_base
    top.mainloop()

def to_Database(is_tag=True):
    global VarIndex_Input,Var_Input,Data_Input,Page_Parser
    try:
        index = eval(VarIndex_Input.get(),{})
    except:
        index = slice(None,None)
    if is_tag:
        func = Page_Parser.to_Database
    else:
        func = Page_Parser.to_Database_by_re
    func(element_value=Var_Input.get(),index=index,data = Data_Input.get(),dataBase_name=get_DataBase_Name())
    Update_Parser_Func_BOX()

def close():
    global DataBase
    name = get_DataBase_Name()
    DataBase.close(name)
    update_DataBase_BOX()

def out():
    global save_dir,DataBase
    name = get_DataBase_Name()
    DataBase.out(name,save_dir)
    update_DataBase_BOX()

def remove_DataBase():
    global DataBase
    name = get_DataBase_Name()
    DataBase.rm_dataBase(name)
    update_DataBase_BOX()

def add_DataBase():
    global DataName_Input,DataBase
    name = DataName_Input.get()
    DataBase.add_DataBase(name)
    update_DataBase_BOX()

def get_DataBase_Name():
    global DataBase_BOX,DataBase_list
    try:
        return DataBase_list[DataBase_BOX.curselection()[0]]
    except:
        try:
            return DataBase_list[0]
        except:
            return None

def update_DataBase_BOX():
    global DataBase_BOX,DataBase_list
    DataBase_list = DataBase.return_database()
    DataBase_BOX.delete(0,tkinter.END)
    DataBase_BOX.insert(tkinter.END,*DataBase_list)

def update_Status(now_func,status,Value_BOX):
    global Func_Output,Status_Output,FuncValue_BOX
    Func_Output.set(now_func)
    Status_Output.set(status)
    FuncValue_BOX.delete(0,tkinter.END)
    FuncValue_BOX.insert(0,*Value_BOX)

def tra_Attributes():
    global Attributes_Dict
    Attributes_Dict = {}
    update_Attributes_BOX()

def del_Attributes():
    global Attributes_BOX, Attributes_Dict
    del Attributes_Dict[list(Attributes_Dict.keys())[Attributes_BOX.curselection()[0]]]
    update_Attributes_BOX()

def add_Attributes():
    global AttributesName_Input,AttributesValue_Input,attribute_re,Attributes_Dict
    name = AttributesName_Input.get()
    value = AttributesValue_Input.get()
    if name == '' or value == '': return False
    value = re.compile(value) if bool(attribute_re.get()) else value
    Attributes_Dict[name] = value
    update_Attributes_BOX()

def update_Attributes_BOX():
    global Attributes_BOX,Attributes_Dict
    show = []
    for i in Attributes_Dict:
        show.append(f'{i} -> {Attributes_Dict[i]}')
    Attributes_BOX.delete(0, tkinter.END)
    Attributes_BOX.insert(tkinter.END,*show)

def Func_Args2():#方法args统一转换(第二栏目)
    global CookiesName_Input,Cookies_Input,Tag_Input,Attributes_Dict,Var_Input,VarIndex_Input
    global FindAllText_Input,text_re,limit_Input,recursive_Input,FindAllPATH_Input
    try:
        index = eval(VarIndex_Input.get(),{})
    except:
        index = slice(None,None)
    try:
        cookies = eval(Cookies_Input.get(),{})
    except:
        cookies = {}
    return dict(element_value=Var_Input.get(),index=index,cookies_name=CookiesName_Input.get(),cookies=cookies,tag=Tag_Input.get().split(','),
             attribute=Attributes_Dict,text=re.compile(FindAllText_Input.get()) if bool(text_re.get()) else FindAllText_Input.get(),
             limit=limit_Input.get(),recursive=bool(recursive_Input.get()),path=FindAllPATH_Input.get())

def Func_Args():#方法args统一转换(不支持Frame)
    global Var_Input, VarIndex_Input, Send_Input, UserPW_Input, SELE_Input, JS_Input, Time_Input
    try:
        time = int(Time_Input.get())
    except:
        time = 2
    try:
        index = int(VarIndex_Input.get())
    except:
        index = 0
    return dict(
    element_value = Var_Input.get(),
    index = index,
    text = Send_Input.get(),
    User = UserPW_Input.get(),
    Passwd = UserPW_Input.get(),
    deselect = SELE_Input.get(),
    JS = JS_Input.get(),
    time=time
    )

def Page_Parser_addActionFunc2(func):
    global Page_Parser
    args = Func_Args2()
    FUNC = {'del_all_cookies':Page_Parser.del_all_cookies,'del_cookies':Page_Parser.del_cookies,'add_cookies':Page_Parser.add_cookies,
            'update_cookies':Page_Parser.update_cookies,'get_cookies':Page_Parser.get_cookies,'get_all_cookies':Page_Parser.get_all_cookies,
            'make_bs':Page_Parser.make_bs,'findAll':Page_Parser.findAll,'findAll_by_text':Page_Parser.findAll_by_text,
            'get_children':Page_Parser.get_children,'get_offspring':Page_Parser.get_offspring,'get_up':Page_Parser.get_up,
            'get_down':Page_Parser.get_down,'get_by_path':Page_Parser.get_by_path,'brothers':Page_Parser.get_brothers,
            'png':Page_Parser.Webpage_snapshot}.get(func,Page_Parser.make_bs)
    FUNC(**args)
    Update_Parser_Func_BOX()

def Page_Parser_addActionFunc(func):
    global Page_Parser
    args = Func_Args()
    FUNC = {'send_keys':Page_Parser.send_keys,'clear':Page_Parser.clear,'click':Page_Parser.click,'User_Passwd':Page_Parser.User_Passwd,
            'accept':Page_Parser.accept,'dismiss':Page_Parser.dismiss,'submit':Page_Parser.submit,'deselect_by_index':Page_Parser.deselect_by_index,
            'deselect_by_value':Page_Parser.deselect_by_value,'deselect_by_text':Page_Parser.deselect_by_text,'select_by_index':Page_Parser.select_by_index,
            'select_by_value':Page_Parser.select_by_value,'select_by_text':Page_Parser.select_by_text,'back':Page_Parser.back,'forward':Page_Parser.forward,
            'refresh':Page_Parser.refresh,'wait_sleep':Page_Parser.wait_sleep,'set_wait':Page_Parser.set_wait,'run_JS':Page_Parser.run_JS,
            'out':Page_Parser.out_html,'get_Page':Page_Parser.to_text}.get(func,Page_Parser.send_keys)
    FUNC(**args)
    Update_Parser_Func_BOX()

def Page_Parser_addFrameFunc_FP(F=True):
    global Page_Parser, search_Input
    search = None if F else ''
    Page_Parser.find_switch_to_frame(search,True)
    Update_Parser_Func_BOX()

def Page_Parser_addFrameFunc_id():
    global Page_Parser, search_Input
    search = search_Input.get()
    Page_Parser.find_switch_to_frame(search,True)
    Update_Parser_Func_BOX()

def Page_Parser_addFindFunc(func):
    global search_all, search_Input,Page_Parser
    not_all = not(bool(search_all.get()))
    search = search_Input.get()
    FUNC = {'id':Page_Parser.find_ID,'name':Page_Parser.find_name,'class':Page_Parser.find_class,
            'xpath':Page_Parser.find_xpath,'css':Page_Parser.find_css,'tag':Page_Parser.find_tag_name,
            'link':Page_Parser.find_link_text,'partial_link':Page_Parser.find_partial_link_text,
            'alert':Page_Parser.find_switch_to_alert,'active_element':Page_Parser.find_switch_to_active_element,
            'frame':Page_Parser.find_switch_to_frame}.get(func,Page_Parser.find_ID)
    FUNC(search,not_all=not_all)
    Update_Parser_Func_BOX()

def Update_Parser_Func_BOX():
    global Parser_Func_BOX,Page_Parser
    Parser_Func_BOX.delete(0,tkinter.END)
    Parser_Func_BOX.insert(tkinter.END, *Page_Parser.return_func(False)[::-1])

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
        Page_Parser.Element_interaction(update_Status)

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

def add_args():
    global URL_ARGS, UA_Input, use_Cookies_Input,FUNC_Input,DATA_Input
    try:
        data = eval(DATA_Input.get(),{})
    except:
        data = {}
    re = dict(
        func = FUNC_Input.get(),
        UA = UA_Input.get(),
        cookies = use_Cookies_Input.get(),
        data=data
        )
    name = ['no_js','no_java','no_plugins','first_run','head','no_img','new']
    for i in range(len(name)):
        re[name[i]] = bool(URL_ARGS[i].get())
    return re

def add_url():
    global URL_Input,url
    args = add_args()
    new_url = URL_Input.get()
    if new_url == '':return
    url.add_url(new_url,**args)
    update_URLBOX()

def update_URLBOX():
    global url,URL_BOX
    URL_BOX.delete(0,tkinter.END)
    URL_BOX.insert(tkinter.END,*url.return_url())


if __name__ == "__main__":
    Main()