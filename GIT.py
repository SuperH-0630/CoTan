import tkinter
import tkinter.messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename,askdirectory,askopenfilenames
import os
import Git_Ctrl
from tkinter.scrolledtext import ScrolledText
import time
import threading

str_code = 'utf-8'
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
    Git_Box = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)
    Git_Box.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 4
    tkinter.Label(top, text='【仓库文件列表】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x,columnspan=3,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    Git_Dir = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)
    Git_Dir.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 4
    tkinter.Button(top, bg=bbg, fg=fg, text='添加暂存区文件', command=Add_File, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='移除暂存区文件', command=init_git, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='提交到git', command=Commit_File, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global commit_m,head,master,no_ff
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

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='查看分支', command=lambda :not_Args(Git.check_Branch), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='新建分支', command=make_Branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='切换分支', command=switch_Branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='删除分支', command=lambda :Delete_Branch(1), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='丢弃分支', command=lambda :Delete_Branch(0), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='合并分支', command=switch_Branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    no_ff = tkinter.Variable()
    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='合并分支', command=merge_Branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='退出冲突处理', command=lambda :not_Args(Git.merge_abort), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='使用快速合并',
                        variable=no_ff).grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    no_ff.set(0)

    global BranchName,StashName,CommitName,BranchNOrigin
    a_y += 1
    tkinter.Label(top, text='分支名字:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    BranchName = tkinter.Entry(top, width=width_B * 2)
    BranchName.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='关联远程分支:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    BranchNOrigin = tkinter.Entry(top, width=width_B * 2)
    BranchNOrigin.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='保存工作区', command=lambda :not_Args(Git.Save_stash), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='恢复工作区', command=lambda :Open_Stash(1), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除工作区', command=lambda :Open_Stash(0), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='工作区序号:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    StashName = tkinter.Entry(top, width=width_B)
    StashName.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='工作区列表', command=lambda :not_Args(Git.Stash_List), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='commit:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    CommitName = tkinter.Entry(top, width=width_B)
    CommitName.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='复制commit', command=cherry_pick, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【远程仓库】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x,columnspan=3,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='连接远程仓库', command=Add_remote, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='推送到远程仓库', command=lambda :Pull_Push_remote(1), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='从远程仓库抓取', command=lambda :Pull_Push_remote(0), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global RemoteSSH,RemoteName,RemoteBranch,LocalBranch,push_bind,allow_history

    a_y += 1
    tkinter.Label(top, text='远程仓库链接:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    RemoteSSH = tkinter.Entry(top, width=width_B)
    RemoteSSH.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='远程仓库名:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    RemoteName = tkinter.Entry(top, width=width_B)
    RemoteName.grid(column=a_x + 1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除关联', command=cherry_pick, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='远程分支:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    RemoteBranch = tkinter.Entry(top, width=width_B)
    RemoteBranch.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='本地分支:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    LocalBranch = tkinter.Entry(top, width=width_B)
    LocalBranch.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    push_bind = tkinter.Variable()
    allow_history = tkinter.Variable()
    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='分支绑定', command=Bind_remote, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='无视历史记录',
                        variable=allow_history).grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='推送时绑定',
                        variable=push_bind).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)
    allow_history.set(0)
    push_bind.set(0)

    tkinter.Label(top, text='【标签管理】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x,columnspan=3,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    global TagName,TagMessage,TagCommit,Show_Key
    a_y += 1
    tkinter.Label(top, text='标签名字:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    TagName = tkinter.Entry(top, width=width_B)
    TagName.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='标签描述:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    TagMessage = tkinter.Entry(top, width=width_B)
    TagMessage.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='commit记录:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    TagCommit = tkinter.Entry(top, width=width_B)
    TagCommit.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='查询关键字:',command=lambda :show_tag(0), bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Show_Key = tkinter.Entry(top, width=width_B)
    Show_Key.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='应用标签', command=Bind_remote, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看已有标签', command=lambda :show_tag(0), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查询数据', command=Bind_remote, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    top.mainloop()

def add_tag():
    global TagName, Git
    tag_name = TagName.get()
    commit = TagCommit.get()
    tag_message = TagMessage.get()
    do_Sys(Git.Add_Tag, (get_Name(), tag_name,commit,tag_message))
    update_Git_Dir()

def show_tag(type_):
    global Show_Key, Git
    key = Show_Key.get()
    do_Sys({1:Git.Tag,0:Git.show_new}.get(type_,Git.show_new), (get_Name(), key))
    update_Git_Dir()

def Pull_Push_remote(type_):
    global RemoteBranch, LocalBranch, Git, allow_history
    Remote = RemoteBranch.get()
    Local = LocalBranch.get()
    allow = bool(allow_history.get())
    u = bool(push_bind.get())
    do_Sys({0:Git.Pull_remote,1:Git.Push_remote}.get(type_,Git.Pull_remote), (get_Name(), Local, Remote, allow, u),
           break_time=10,text_n=f'此操作需要连接远程仓库，请稍等...',th=True)
    update_Git_Dir()

def Bind_remote():
    global RemoteBranch, LocalBranch, Git
    Remote = RemoteBranch.get()
    Local = LocalBranch.get()
    do_Sys(Git.Bind_remote, (get_Name(), Local, Remote))
    update_Git_Dir()

def Add_remote():
    global RemoteSSH, RemoteName, Git
    SSH = RemoteSSH.get()
    name = RemoteName.get()
    do_Sys(Git.Add_remote, (get_Name(), SSH, name))
    update_Git_Dir()

def cherry_pick():
    global CommitName, Git
    commit = CommitName.get()
    do_Sys(Git.cherry_pick, (get_Name(), commit))
    update_Git_Dir()

def Open_Stash(type_):
    global StashName, Git
    stash_num = StashName.get()
    if stash_num == '':stash_num = '0'
    do_Sys([Git.Drop_stash,Git.Apply_stash][type_], (get_Name(), stash_num))
    update_Git_Dir()

def merge_Branch():
    global BranchName, Git, no_ff,commit_m
    m = commit_m.get()
    no = not bool(no_ff.get())  # 对于no_ff来说，True - 使用快速合并，所以要翻转
    if m.replace(' ','') == '' and no:
        tkinter.messagebox.showinfo('警告!', '非常遗憾，我不同意你commit而不添加任何描述！\n描述是很重要的！'
                                           '(如果你不想添加描述，请使用快速合并，但我并不建议！)')
        return False
    name = BranchName.get()
    do_Sys(Git.merge_Branch, (get_Name(), name, no, m))
    update_Git_Dir()

def Delete_Branch(type_):
    global BranchName, Git
    name = BranchName.get()
    do_Sys(Git.Del_Branch, (get_Name(), name, type_))
    update_Git_Dir()

def switch_Branch():
    global BranchName,Git
    name = BranchName.get()
    do_Sys(Git.switch_Branch, (get_Name(), name),break_time=1,show=False)
    update_Git_Dir()

def make_Branch():
    global BranchName,Git,BranchNOrigin
    name = BranchName.get()
    origin = BranchNOrigin.get()
    do_Sys(Git.new_Branch, (get_Name(), name, origin),break_time=1,show=False)
    update_Git_Dir()

def check_Branch():
    global Git,head
    dic = askopenfilenames(title=f'选择要删除的文件(取消为全选)')
    if dic == '': return False
    do_Sys(Git.rm,(get_Name(),dic))
    update_Git_Dir()

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

def do_Sys(func,args,name='CoTan Git',break_time=2,show=True,text_n='',th=False):
    p = func(*args)
    def Out_Txt():
        nonlocal data
        dic = asksaveasfilename(title='选择文件保存位置',filetypes=[("TXT", ".txt")])
        try:
            if dic == '':return False
            if dic[-4] == '.txt':pass
            else:raise Exception
        except:
            dic += '.txt'
        with open(dic,'w',encoding='utf-8') as f:
            f.write(data)
    def Stop():nonlocal start;start = 0
    def keep():nonlocal start;start = float('inf')
    def pipe():pass
    def not_out():
        nonlocal text,data
        text.clear()
        text.insert(tkinter.END,data)
    start = time.time()
    data = ''
    if show:
        text, new_top = show_Now(Out_Txt,Stop,keep,not_out,pipe,name=name)
        if text_n != '':
            text.insert('0.0',f'载入前提示>>> {text_n}\n')
        new_top.update()
    top.update()
    def Update():
        nonlocal start
        while True:
            try:
                top.update()
                if show: new_top.update()
                if time.time() - start >= break_time:raise Exception
            except:
                start = 0
                break
    if th:
        j = threading.Thread(target=Update())
        j.start()
    while True:
        try:
            if not th:
                top.update()
                if show: new_top.update()
        except:
            break
        try:
            i = p.stdout.readline()#.decode(str_code)#不需要decode,因为Popen已经设置了universal_newlines=True
            if i.replace(' ','').replace('\n','') != '':
                if show:text.insert(tkinter.END,f'[out]> {i}')
                data += i
            if p.returncode == 0 or time.time() - start >= break_time:
                if show:text.insert(tkinter.END,'[END]')
                break
            elif p.returncode != None:
                raise Exception
        except:
            try:
                if show:text.insert(tkinter.END, '[ERROR]')
                raise Exception
            except:break
    p.kill()
    return data

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
    if dic == '':dic = '.'
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
    try:#窗口可能已经关闭
        Git_Dir.delete(0,tkinter.END)
        Git_Dir.insert(tkinter.END,*dir_list)
    except:
        pass
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

def show(data='',name='CoTan_Git'):
    global bg, ft1
    new_top = tkinter.Toplevel(bg=bg)
    new_top.title(name)
    new_top.geometry('+10+10')  # 设置所在位置
    text = ScrolledText(new_top, font=('黑体', 11), height=50)
    text.pack(fill=tkinter.BOTH)
    text.insert('0.0', data)
    text.config(state=tkinter.DISABLED)
    new_top.resizable(width=False, height=False)

def show_Now(out_func,close_func,keepFunc,not_out,pipeFunc,name='CoTan_Git >>> 高级命令行'):
    global bg
    new_top = tkinter.Toplevel(bg=bg)
    new_top.title(name)
    new_top.geometry('+10+10')  # 设置所在位置
    new_top.resizable(width=False, height=False)

    class ScrolledText_new(ScrolledText):
        def __init__(self,*args,**kwargs):
            super(ScrolledText_new, self).__init__(*args,**kwargs)

        def insert(self, index, chars, *args):
            text.config(state=tkinter.NORMAL)
            super(ScrolledText_new, self).insert(index, chars, *args)
            text.config(state=tkinter.DISABLED)

        def clear(self):
            text.config(state=tkinter.NORMAL)
            self.delete('0.0',tkinter.END)
            text.config(state=tkinter.DISABLED)

    text = ScrolledText_new(new_top, font=('黑体', 11), height=30,width=100)
    text.grid(column=0, row=0,columnspan=5, sticky=tkinter.E + tkinter.W)
    text.config(state=tkinter.DISABLED)
    tkinter.Button(new_top, bg=bg, fg=fg, text='输出文档', font=('黑体', 11),width=20, height=2, command=out_func).grid(
        column=4, row=1, sticky=tkinter.E + tkinter.W)
    tkinter.Button(new_top, bg=bg, fg=fg, text='关闭子线程连接', font=('黑体', 11),width=20, height=2, command=close_func).grid(
        column=0, row=1, sticky=tkinter.E + tkinter.W)
    tkinter.Button(new_top, bg=bg, fg=fg, text='保持线程连接', font=('黑体', 11),width=20, height=2, command=keepFunc).grid(
        column=1, row=1, sticky=tkinter.E + tkinter.W)
    tkinter.Button(new_top, bg=bg, fg=fg, text='格式化输出', font=('黑体', 11),width=20, height=2, command=not_out).grid(
        column=2, row=1, sticky=tkinter.E + tkinter.W)
    tkinter.Button(new_top, bg=bg, fg=fg, text='文件管道输入', font=('黑体', 11),width=20, height=2, command=pipeFunc).grid(
        column=3, row=1, sticky=tkinter.E + tkinter.W)
    return text,new_top

if __name__ == '__main__':
    Main()
    # show_Now()