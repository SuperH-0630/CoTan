import tkinter
import tkinter.messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename,askdirectory,askopenfilenames
import os
import Git_Ctrl
from tkinter.scrolledtext import ScrolledText

Git = Git_Ctrl.git_Ctrol()#需要去掉

def Main():
    global top,Git,PATH,bg,bbg,fg,Git_List,Last_Name
    PATH = os.getcwd()
    Git = Git_Ctrl.git_Ctrol()
    Git_List = []
    top = tkinter.Tk()
    Last_Name = None
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

    global clone_url
    a_y += 1
    tkinter.Label(top, text='克隆URL:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Dic_Var = tkinter.StringVar()#当前的Dic
    clone_url = tkinter.Entry(top, width=width_B * 2, textvariable=Dic_Var)
    clone_url.grid(column=a_x+1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='克隆仓库', command=clone_git, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='打开仓库', command=init_git, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看文件', command=get_Git_Dir, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Git_Box,Git_Dir
    a_y += 1
    Git_Box = tkinter.Listbox(top, width=width_B * 3, height=height_B * 5)
    Git_Box.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 5
    tkinter.Label(top, text='【仓库文件列表】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x,columnspan=3,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    Git_Dir = tkinter.Listbox(top, width=width_B * 3, height=height_B * 5)
    Git_Dir.grid(column=a_x, row=a_y, columnspan=3, rowspan=5, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 5
    tkinter.Button(top, bg=bbg, fg=fg, text='添加暂存区文件', command=Add_File, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='移除暂存区文件', command=init_git, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='提交到git', command=Commit_File, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global commit_m,head,master
    a_y += 1
    tkinter.Label(top, text='提交描述:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    commit_m = tkinter.Entry(top, width=width_B * 2)
    commit_m.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='查看执行日志', command=lambda :not_Args(Git.reflog), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看文件日志', command=lambda :not_Args(Git.log), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看状态', command=lambda :not_Args(Git.status), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='版本回退', command=Back_version, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='文件回退', command=Back_File, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除文件', command=rm_file, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='diff分支:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    master = tkinter.Entry(top, width=width_B * 2)
    master.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='回退版本号:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    head = tkinter.Entry(top, width=width_B * 2)
    head.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    top.mainloop()

def rm_file():
    global Git,head
    dic = askopenfilenames(title=f'选择要删除的文件(取消为全选)')
    if dic == '': return False
    do_Sys(Git.rm,(get_Name(),dic))
    update_Git_Dir()

def Back_File():
    global Git,head
    dic = askopenfilenames(title=f'选择要add的文件(取消为全选)')
    if dic == '': return False
    do_Sys(Git.checkout_version,(get_Name(),dic))
    update_Git_Dir()

def Back_version():
    global Git,head
    HEAD = head.get()
    if HEAD == '': HEAD = 'HEAD~1'
    do_Sys(Git.back_version,(get_Name(),HEAD))
    update_Git_Dir()

def do_Sys(func,args,name='CoTan Git'):
    p = func(*args)
    p.wait()
    if p.returncode != 0: print(p.returncode)
    else:
        print('success')
    data = ''
    while True:
        i = p.stdout.readline().decode('utf-8')
        if i == '': break
        data += i
    if data.replace('\n','').replace(' ','') != '':show(data,name)


def not_Args(func):
    global Git
    name = get_Name()
    do_Sys(func,(name,))
    update_Git_Dir()

def Commit_File():
    global Git,commit_m
    m = commit_m.get()
    if m.replace(' ','') == '':
        tkinter.messagebox.showinfo('警告!', '非常遗憾，我不同意你commit而不添加任何描述！\n描述是很重要的！')
        return False
    name = get_Name()
    do_Sys(Git.commit_File,(name,m))
    update_Git_Dir()

def Diff_File():
    global Git,master
    MASTER = master.get()
    if MASTER == '':MASTER = 'HEAD'
    do_Sys(Git.diff_File,(get_Name(),MASTER))
    update_Git_Dir()

def Add_File():
    global Git,Last_Name
    dic = askopenfilenames(title=f'选择要add的文件(取消为全选)')
    if dic == '':dic = '*'
    do_Sys(Git.add_File,(get_Name(),dic))
    update_Git_Dir()

def update_Git_Dir():
    global Last_Name
    if Last_Name == None:return False
    Git_dir(Last_Name)

def get_Git_Dir():
    name = get_Name()
    Git_dir(name)

def Git_dir(name):
    global Git, Git_Dir,Last_Name
    dir_list = Git.get_Dir(name)
    Git_Dir.delete(0,tkinter.END)
    Git_Dir.insert(tkinter.END,*dir_list)
    Last_Name = name

def clone_git():#克隆仓库
    global clone_url
    new_Dic = askdirectory(title = '选择仓库地址')
    if new_Dic == '':return False
    Git.Clone_init(new_Dic, clone_url.get())
    Updata_GitBox()

def init_git():#创建仓库
    global Git
    new_Dic = askdirectory(title = '选择仓库地址')
    if new_Dic == '':return False
    Git.Add_init(new_Dic,)
    Updata_GitBox()

def get_Name():  # 获得名字统一接口
    global Git,Git_List,Git_Box
    try:
        return Git_List[Git_Box.curselection()[0]]
    except:
        try:
            return Git_List[0]
        except:
            return None

def Updata_GitBox():
    global Git,Git_List,Git_Box
    Git_List = list(Git.get_git_Dic().keys())
    Git_Box.delete(0,tkinter.END)
    Git_Box.insert(tkinter.END,*Git_List)

def show(data,name):
    global bg, ft1
    new_top = tkinter.Toplevel(bg=bg)
    new_top.title(name)
    new_top.geometry('+10+10')  # 设置所在位置
    text = ScrolledText(new_top, font=('黑体', 11), height=50)
    text.pack(fill=tkinter.BOTH)
    text.insert('0.0', data)
    text.config(state=tkinter.DISABLED)
    new_top.resizable(width=False, height=False)

if __name__ == '__main__':
    Main()