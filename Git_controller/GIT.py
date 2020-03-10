import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename,askdirectory,askopenfilenames
import os
from Git_controller import Git_Ctrl
from tkinter.scrolledtext import ScrolledText
import time
import threading

def git_main():
    global top,Git,PATH,bg,bbg,fg,Git_List,Last_Name,FileList
    FileList = []
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

    global clone_url,Git_Box,Git_Dir
    global commit_m,head,master,no_ff
    global TagName,TagMessage,TagCommit,Show_Key
    global RemoteSSH,RemoteName,RemoteBranch,LocalBranch,push_bind,allow_history
    global BranchName, StashName, CommitName, BranchNOrigin

    tkinter.Button(top, bg=bbg, fg=fg, text='克隆仓库', command=clone_git, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='打开仓库', command=repo_init, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看文件', command=update_git_file_select, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='克隆URL:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Dic_Var = tkinter.StringVar()#当前的Dic
    clone_url = tkinter.Entry(top, width=width_B * 2, textvariable=Dic_Var)
    clone_url.grid(column=a_x+1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

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
    tkinter.Label(top, text='【添加文件列表】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x,columnspan=3,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    global File_Input,File_BOX

    a_y += 1
    File_Input = tkinter.Entry(top, width=width_B * 2)
    File_Input.grid(column=a_x, row=a_y, columnspan=3, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='填充路径并添加', command=add_file_by_git, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='直接添加', command=add_file_input, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='选择文件', command=add_file_list, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='把文件移除出列表', command=del_file, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='清空列表', command=clean_file, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    File_BOX = tkinter.Listbox(top, width=width_B * 3, height=height_B * 4)
    File_BOX.grid(column=a_x, row=a_y, columnspan=3, rowspan=4, sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N)

    a_y += 4
    tkinter.Button(top, bg=bbg, fg=fg, text='添加暂存区文件', command=add, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='移除暂存区文件', command=remove_the_staging, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='提交到git', command=commit, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='查看执行日志', command=lambda :not_parameters_call(Git.reflog), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看文件日志', command=log, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看状态', command=lambda :not_parameters_call(Git.status), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global log_Type,reset_Type
    a_y += 1
    log_Type = []
    lable = ['显示轴','commit完全显示','简化显示']#复选框
    for i in range(3):
        log_Type.append(tkinter.IntVar())
        tkinter.Checkbutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg, text=lable[i],
                            variable=log_Type[-1]).grid(column=a_x+i, row=a_y, sticky=tkinter.W)
        log_Type[-1].set(1)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='版本回退', command=reset_head, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='放弃修改', command=checkout_file, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除文件', command=remove_file, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    reset_Type = tkinter.IntVar()#正，负，0
    lable = ['回退到工作区','回退到暂存区','无痕回退']#复选框
    for i in range(3):
        tkinter.Radiobutton(top,bg = bg,fg = fg,activebackground=bg,activeforeground=fg,selectcolor=bg,text=lable[i],
                            variable=reset_Type, value=i).grid(column=a_x+i, row=a_y, sticky=tkinter.W)

    a_x += 3
    tkinter.Label(top, text='', bg=bg, fg=fg, font=FONT, width=1).grid(column=a_x, row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(top, text='【参数操作】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x,columnspan=3,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Label(top, text='提交描述:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    commit_m = tkinter.Entry(top, width=width_B * 2)
    commit_m.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='diff分支:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    master = tkinter.Entry(top, width=width_B * 2)
    master.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='回退版本号:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    head = tkinter.Entry(top, width=width_B * 2)
    head.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='本地分支:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    BranchName = tkinter.Entry(top, width=width_B * 2)
    BranchName.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='远程分支:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    BranchNOrigin = tkinter.Entry(top, width=width_B * 2)
    BranchNOrigin.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='远程仓库链接:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    RemoteSSH = tkinter.Entry(top, width=width_B)
    RemoteSSH.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='远程仓库名:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    RemoteName = tkinter.Entry(top, width=width_B)
    RemoteName.grid(column=a_x + 1, row=a_y, columnspan=2,sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='commit:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    CommitName = tkinter.Entry(top, width=width_B)
    CommitName.grid(column=a_x + 1, row=a_y, columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='标签名字:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    TagName = tkinter.Entry(top, width=width_B)
    TagName.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='查询关键字:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    Show_Key = tkinter.Entry(top, width=width_B)
    Show_Key.grid(column=a_x + 1,columnspan=2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='工作区序号:', bg=bg, fg=fg, font=FONT, width=width_B, height=height_B).grid(column=a_x,row=a_y)
    StashName = tkinter.Entry(top, width=width_B)
    StashName.grid(column=a_x + 1, row=a_y,columnspan=2, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Label(top, text='【高级操作】', bg=bg, fg=fg, font=FONT, width=width_B * 3, height=height_B).grid(
        column=a_x,columnspan=3,row=a_y,sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='查看分支', command=lambda :not_parameters_call(Git.check_Branch), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='新建分支', command=add_new_Branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='切换分支', command=switch_branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='删除分支', command=lambda :del_branch(1), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='丢弃分支', command=lambda :del_branch(0), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='合并分支', command=switch_branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    no_ff = tkinter.IntVar()
    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='合并分支', command=branch_merge, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='退出冲突处理', command=lambda :not_parameters_call(Git.merge_abort), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='使用快速合并',
                        variable=no_ff).grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    no_ff.set(0)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='连接远程仓库', command=add_remote, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='推送到远程仓库', command=lambda :pull_push_remote(1), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='从远程仓库抓取', command=lambda :pull_push_remote(0), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    push_bind = tkinter.IntVar()
    allow_history = tkinter.IntVar()
    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='分支绑定', command=bind_remote_branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='无视历史记录',
                        variable=allow_history).grid(column=a_x + 1, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='推送时绑定',
                        variable=push_bind).grid(column=a_x + 2, row=a_y, sticky=tkinter.W)
    allow_history.set(0)
    push_bind.set(0)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='应用标签', command=add_tag, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查看已有标签', command=lambda :show_tag(1), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='查询commit记录',command=lambda :show_tag(0), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='推送标签', command=push_tag, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='推送所有标签', command=push_all_tag, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除本地标签', command=del_tag, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='删除远程标签', command=del_remote_tag, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除远程分支', command=del_remote_branch, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='刷新远程分支', command=fetch_remote, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='commit补丁', command=cherry_pick, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除远程仓库', command=del_remote, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='工作区列表', command=lambda :not_parameters_call(Git.Stash_List), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global newName_Input
    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='文件回退', command=reset_file, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='分支重命名', command=branch_new, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    newName_Input = tkinter.Entry(top, width=width_B)
    newName_Input.grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(top, bg=bbg, fg=fg, text='保存工作区', command=lambda :not_parameters_call(Git.Save_stash), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='恢复工作区', command=lambda :open_stash(1), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+1, row=a_y, sticky=tkinter.E + tkinter.W)
    tkinter.Button(top, bg=bbg, fg=fg, text='删除工作区', command=lambda :open_stash(0), font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)

    global Customize_Input, th_do, wait_do
    a_y += 1
    th_do = tkinter.IntVar()
    wait_do = tkinter.IntVar()
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='多进程刷新',
                        variable=th_do).grid(column=0, row=a_y, sticky=tkinter.W)
    tkinter.Checkbutton(top, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, selectcolor=bg, text='异步显示',
                        variable=wait_do).grid(column=1, row=a_y, sticky=tkinter.W)
    Customize_Input = tkinter.Entry(top, width=width_B * 3)
    Customize_Input.grid(column=2, row=a_y, columnspan=4, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)

    tkinter.Button(top, bg=bbg, fg=fg, text='执行操作', command=customize, font=FONT, width=width_B,
                   height=height_B).grid(column=a_x+2, row=a_y, sticky=tkinter.E + tkinter.W)
    th_do.set(0)
    wait_do.set(1)
    TagMessage = commit_m
    TagCommit = CommitName
    RemoteBranch = BranchNOrigin
    LocalBranch = BranchName

    top.mainloop()

def branch_new():#克隆仓库
    global BranchName, newName_Input
    new_name = newName_Input.get()
    old_name = BranchName.get()
    cli(Git.Branch_new, (get_repo_name(), old_name, new_name), show=False)
    update_repo_box()

def clone_git():#克隆仓库
    global clone_url
    new_Dic = askdirectory(title = '选择仓库地址')
    if new_Dic == '':return False
    name = Git.Clone_init(new_Dic)
    clone_core(name, clone_url.get())
    update_repo_box()

def clone_core(name, url):
    cli(Git.Clone, (name, url),
        break_time=0, text_n=f'{url}:正在执行克隆操作', th=True, wait=True)
    Git.After_Clone(name)
    update_git_file_last()

def customize():
    global Git, Customize_Input, th_do, wait_do
    command = Customize_Input.get()
    cli(Git.Customize, (get_repo_name(), command),
        break_time=0, text_n=f'{command}:操作进行中', th=bool(th_do.get()), wait=bool(wait_do.get()))
    update_git_file_last()

def fetch_remote():
    global RemoteBranch, LocalBranch, Git, RemoteName
    Branch = RemoteBranch.get()
    Remote = RemoteName.get()
    Local = LocalBranch.get()
    cli(Git.Fetch, (get_repo_name(), Local, Remote, Branch),
        break_time=0, text_n=f'此操作需要连接远程仓库，请稍等...', th=True, wait=True)
    update_git_file_last()

def del_tag():
    global Git, RemoteName, TagName
    Tag = TagName.get()
    cli(Git.del_tag, (get_repo_name(), Tag))
    update_git_file_last()

def del_remote_branch():
    global Git, RemoteName, TagName
    Remoto = RemoteName.get()
    Remoto_Branch = RemoteBranch.get()
    cli(Git.del_Branch_remote, (get_repo_name(), Remoto, Remoto_Branch), break_time=0, text_n=f'此操作需要连接远程仓库，请稍等...',
        th=True, wait=True)
    update_git_file_last()

def del_remote_tag():
    global Git, RemoteName, TagName
    Remoto = RemoteName.get()
    Tag = TagName.get()
    cli(Git.del_Tag_remote, (get_repo_name(), Remoto, Tag), break_time=0, text_n=f'此操作需要连接远程仓库，请稍等...',
        th=True, wait=True)
    update_git_file_last()

def push_all_tag():
    global Git, RemoteName
    Remoto = RemoteName.get()
    cli(Git.push_allTag, (get_repo_name(), Remoto), break_time=0, text_n=f'此操作需要连接远程仓库，请稍等...',
        th=True, wait=True)
    update_git_file_last()

def push_tag():
    global TagName, Git, RemoteName
    tag_name = TagName.get()
    Remoto = RemoteName.get()
    cli(Git.push_Tag, (get_repo_name(), tag_name, Remoto), break_time=0, text_n=f'此操作需要连接远程仓库，请稍等...',
        th=True, wait=True)
    update_git_file_last()

def add_tag():
    global TagName, Git, commit, tag_message
    tag_name = TagName.get()
    commit = TagCommit.get()
    tag_message = TagMessage.get()
    cli(Git.Add_Tag, (get_repo_name(), tag_name, commit, tag_message), show=False)
    update_git_file_last()

def show_tag(type_):
    global Show_Key, Git
    key = Show_Key.get()
    cli({1:Git.Tag, 0:Git.show_new}.get(type_, Git.show_new), (get_repo_name(), key))
    update_git_file_last()

def pull_push_remote(type_):
    global RemoteBranch, LocalBranch, Git, allow_history, RemoteName
    Branch = RemoteBranch.get()
    Remote = RemoteName.get()
    Local = LocalBranch.get()
    allow = bool(allow_history.get())
    u = bool(push_bind.get())
    f = tkinter.messagebox.askokcancel('提示', f'是否需要强制推送？(强制推送不被建议)')
    cli({0:Git.Pull_remote, 1:Git.Push_remote}.get(type_, Git.Pull_remote), (get_repo_name(), Local, Remote, Branch, allow, u, f),
        break_time=0, text_n=f'此操作需要连接远程仓库，请稍等...', th=True, wait=True)
    update_git_file_last()

def bind_remote_branch():
    global RemoteBranch, LocalBranch, Git
    Remote = RemoteBranch.get()
    Local = LocalBranch.get()
    cli(Git.Bind_remote, (get_repo_name(), Local, Remote))
    update_git_file_last()

def del_remote():
    global RemoteSSH, RemoteName, Git
    name = RemoteName.get()
    cli(Git.Del_remote, (get_repo_name(), name))
    update_git_file_last()

def add_remote():
    global RemoteSSH, RemoteName, Git
    SSH = RemoteSSH.get()
    name = RemoteName.get()
    cli(Git.Add_remote, (get_repo_name(), SSH, name))
    update_git_file_last()

def cherry_pick():
    global CommitName, Git
    commit = CommitName.get()
    cli(Git.cherry_pick, (get_repo_name(), commit))
    update_git_file_last()

def open_stash(type_):
    global StashName, Git
    stash_num = StashName.get()
    if stash_num == '':stash_num = '0'
    cli([Git.Drop_stash, Git.Apply_stash][type_], (get_repo_name(), stash_num))
    update_git_file_last()

def branch_merge():
    global BranchName, Git, no_ff,commit_m
    m = commit_m.get()
    no = not bool(no_ff.get())  # 对于no_ff来说，True - 使用快速合并，所以要翻转
    if m.replace(' ','') == '' and no:
        tkinter.messagebox.showinfo('警告!', '非常遗憾，我不同意你commit而不添加任何描述！\n描述是很重要的！'
                                           '(如果你不想添加描述，请使用快速合并，但我并不建议！)')
        return False
    name = BranchName.get()
    cli(Git.merge_Branch, (get_repo_name(), name, no, m))
    update_git_file_last()

def del_branch(type_):
    global BranchName, Git
    name = BranchName.get()
    cli(Git.Del_Branch, (get_repo_name(), name, type_))
    update_git_file_last()

def switch_branch():
    global BranchName,Git
    name = BranchName.get()
    cli(Git.switch_Branch, (get_repo_name(), name), break_time=1, show=False)
    update_git_file_last()

def add_new_Branch():
    global BranchName,Git,BranchNOrigin
    name = BranchName.get()
    origin = BranchNOrigin.get()
    cli(Git.new_Branch, (get_repo_name(), name, origin), break_time=1, show=False)
    update_git_file_last()

def remove_file():
    global Git,head
    dic = FileList
    if dic == []: return False
    cli(Git.rm, (get_repo_name(), dic))
    update_git_file_last()

def checkout_file():#从暂存区、仓库返回文件
    global Git,head
    dic = FileList
    if dic == []: return False
    cli(Git.checkout_version, (get_repo_name(), dic))
    update_git_file_last()

def reset_file():#使用reset回退文件
    global Git,head,reset_Type
    HEAD = head.get()
    if HEAD == '': HEAD = 'HEAD~1'
    File = FileList
    cli(Git.back_version_file, (get_repo_name(), HEAD, File))
    update_git_file_last()

def reset_head():
    global Git,head,reset_Type
    HEAD = head.get()
    if HEAD == '': HEAD = 'HEAD~1'
    Type = reset_Type.get()
    cli(Git.back_version, (get_repo_name(), HEAD, Type))
    update_git_file_last()

def cli(func, args, name='CoTan Git', break_time=0, show=True, text_n='', th=False, wait=False, stop=True):
    p = func(*args)
    flat = True
    stop_key = Git_Ctrl.stopKey
    def out_txt():
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
    kb = True
    sb = True
    def update_b():
        if not kb:
            b_list[1].config(state=tkinter.DISABLED)
        if not sb:
            b_list[0].config(state=tkinter.DISABLED)
    def stop():
        nonlocal start,kb,sb
        start = 0
        sb = False
        kb = False
        update_b()
    def keep():
        nonlocal start,kb
        start = float('inf')
        kb = False
        update_b()

    def pipe():pass
    def not_out():
        nonlocal text,out_data,data,flat
        text.clear()
        if flat:
            text.insert(tkinter.END,data)
        else:
            text.insert(tkinter.END, out_data)
        flat = not flat
    start = time.time()
    data = ''
    out_data = ''#包含out的data
    if show:
        text, new_top, b_list = show_cli(out_txt, stop, keep, not_out, pipe, name=name)#[close,keep]
        update_b()
        if text_n != '':
            text.insert('0.0',f'载入前提示>>> {text_n}\n')
            out_data += f'载入前提示>>> {text_n}\n'
            data += f'{text_n}\n'
        new_top.update()
    else:
        u = threading.Thread(target=progress_bar)
        u.start()
    top.update()
    def Update():
        nonlocal start
        while True:
            try:
                top.update()
                if show:
                    try:
                        new_top.update()
                    except:pass
                if time.time() - start >= break_time and break_time != 0:
                    raise Exception
                elif break_time == 0 and start == 0:
                    raise Exception
            except:
                start = 0
                break

    if th or not wait:
        j = threading.Thread(target=Update)#如果没有启动到多进程的效果，请检查Update是不是加了()，这里需要回调
        j.start()

    if wait:#等待后显示
        if break_time == 0:break_ti = None# 此处break_ti是为了别面覆盖break_time，因为Update进程需要用
        else:break_ti = break_time
        def wait_p():
            nonlocal start
            p.wait(break_ti)
            start = 0
        j = threading.Thread(target=wait_p)  # 这么做不是多此一举，如果没有wait，进程并不会退出
        j.start()
        Update()#遇到sleep等主线程阻塞，top.update等会阻塞子线程，因此，必须保证主线程不会被wait所阻塞
        out = p.stdout.read().split('\n')
        for i in out:
            if show:
                try:  # 如果界面被关掉了，会报错
                    new_top.title(f'{name} : 运行中')
                except:
                    text, new_top, b_list = show_cli(out_txt, stop, keep, not_out, pipe,
                                                     name=f'{name} : 运行中')
                    update_b()
                    text.insert(tkinter.END, out_data)
                if stop and i.replace(' ', '').replace('\n', '') != stop_key:
                    text.insert(tkinter.END, f'[out]> {i}\n')
                    data += i + '\n'
                    out_data += f'[out]> {i}\n'
        if show:
            text.insert(tkinter.END, '[END]')
            out_data += f'[END]'
            data += f'[END]'
        start = 0
    else:#即时显示
        while True:
            #界面设置
            try:#如果界面被关掉了，会报错
                if show: new_top.title(f'{name} : 运行中')
            except:
                text, new_top, b_list = show_cli(out_txt, stop, keep, not_out, pipe,
                                                 name=f'{name} : 运行中')
                update_b()
                text.insert(tkinter.END,out_data)
            #界面刷新
            try:
                if not th:
                    top.update()
                    if show: new_top.update()
            except:
                break
            #输出字符
            try:
                i = p.stdout.readline()#.decode(str_code)#不需要decode,因为Popen已经设置了universal_newlines=True
                bool_text = i.replace(' ','').replace('\n','')
                if bool_text != '':
                    if stop and bool_text == stop_key:
                        start = 0
                    else:
                        if show: text.insert(tkinter.END, f'[out]> {i}')
                        data += i
                        out_data += f'[out]> {i}'
                if p.returncode == 0 or (time.time() - start >= break_time and break_time != 0) or (break_time == 0 and start == 0):
                    if show:
                        text.insert(tkinter.END,'[END]')
                        out_data += f'[END]'
                        data += f'[END]'
                    break
                elif p.returncode != None:
                    raise Exception
            except:
                try:
                    if show:
                        text.insert(tkinter.END, '[ERROR]')
                        out_data += f'[ERROR]'
                        data += f'[ERROR]'
                    raise Exception
                except:break
        try:  # 如果界面被关掉了，会报错
            if show: new_top.title(f'{name} : 运行完毕')
        except:pass
        p.kill()
    try:
        if show:
            b_list[0].config(state=tkinter.DISABLED)
            b_list[1].config(state=tkinter.DISABLED)
    except:pass
    return data

def log():
    global Git,log_Type
    name = get_repo_name()
    graph = bool(log_Type[0].get())
    abbrev = bool(log_Type[1].get())
    pretty = bool(log_Type[2].get())
    cli(Git.log, (name, graph, pretty, abbrev))
    update_git_file_last()

def not_parameters_call(func):
    global Git
    name = get_repo_name()
    cli(func, (name,))
    update_git_file_last()

def commit():
    global Git,commit_m
    m = commit_m.get()
    if m.replace(' ','') == '':
        tkinter.messagebox.showinfo('警告!', '非常遗憾，我不同意你commit而不添加任何描述！\n描述是很重要的！')
        return False
    name = get_repo_name()
    cli(Git.commit_File, (name, m))
    update_git_file_last()

def diff():
    global Git,master
    MASTER = master.get()
    if MASTER == '':MASTER = 'HEAD'
    cli(Git.diff_File, (get_repo_name(), MASTER))
    update_git_file_last()

def remove_the_staging():
    global Git,Last_Name,FileList
    dic = FileList
    if dic == []:dic = '.'
    cli(Git.reset_File, (get_repo_name(), dic))
    update_git_file_last()

def add():
    global Git,Last_Name,FileList
    dic = FileList
    if dic == []:dic = '.'#查一下取消的dic
    cli(Git.add_File, (get_repo_name(), dic))
    update_git_file_last()

def add_file_list():
    global FileList, File_BOX
    a = set(askopenfilenames(title=f'选择要add的文件(取消为全选)'))
    b = set(FileList)
    dic = list(a - (a & b))#筛选出重复
    FileList += dic
    update_file_box()

def add_file_input():
    global File_Input
    dic = File_Input.get()
    if dic.replace(' ','') != '' and dic not in FileList:
        FileList.append(dic)
    update_file_box()

def add_file_by_git():
    global File_Input
    dic = File_Input.get()
    if dic.replace(' ', '') != '':
        name = get_repo_name()
        new_dir = Git.make_Dir(name,dic)
        if new_dir not in FileList:
            FileList.append(new_dir)
    update_file_box()

def del_file():
    global FileList, File_BOX
    try:
        del FileList[File_BOX.curselection()]
        update_file_box()
    except:pass

def clean_file():
    global FileList
    FileList = []
    update_file_box()

def update_file_box():
    global FileList, File_BOX
    File_BOX.delete(0, tkinter.END)
    File_BOX.insert(tkinter.END, *FileList)

def update_git_file_last():
    global Last_Name
    if Last_Name == None:return False
    update_git_file_core(Last_Name)

def update_git_file_select():
    name = get_repo_name()
    update_git_file_core(name)

def update_git_file_core(name):
    global Git, Git_Dir,Last_Name
    dir_list = Git.get_Dir(name)
    try:#窗口可能已经关闭
        Git_Dir.delete(0,tkinter.END)
        Git_Dir.insert(tkinter.END,*dir_list)
    except:
        pass
    Last_Name = name

def repo_init():#创建仓库
    global Git
    new_Dic = askdirectory(title = '选择仓库地址')
    if new_Dic == '':return False
    Git.Add_init(new_Dic,)
    update_repo_box()

def get_repo_name():  # 获得名字统一接口
    global Git,Git_List,Git_Box
    try:
        return Git_List[Git_Box.curselection()[0]]
    except:
        try:
            return Git_List[0]
        except:
            return None

def update_repo_box():
    global Git,Git_List,Git_Box
    Git_List = list(Git.get_git_Dic().keys())
    Git_Box.delete(0,tkinter.END)
    Git_Box.insert(tkinter.END,*Git_List)

def show_cli(out_func, close_func, keepFunc, not_out, pipeFunc, name='CoTan_Git >>> 命令行'):
    global bg
    new_top = tkinter.Toplevel(bg=bg)
    new_top.title(name)
    new_top.geometry('+10+10')  # 设置所在位置
    new_top.resizable(width=False, height=False)

    class ScrolledCli(ScrolledText):
        def __init__(self,*args,**kwargs):
            super(ScrolledCli, self).__init__(*args,**kwargs)

        def insert(self, index, chars, *args):
            text.config(state=tkinter.NORMAL)
            super(ScrolledCli, self).insert(index, chars, *args)
            text.config(state=tkinter.DISABLED)

        def clear(self):
            text.config(state=tkinter.NORMAL)
            self.delete('0.0',tkinter.END)
            text.config(state=tkinter.DISABLED)

    text = ScrolledCli(new_top, font=('黑体', 11), height=30,width=100)
    text.grid(column=0, row=0,columnspan=5, sticky=tkinter.E + tkinter.W)
    text.config(state=tkinter.DISABLED)
    tkinter.Button(new_top, bg=bg, fg=fg, text='输出文档', font=('黑体', 11),width=20, height=2, command=out_func).grid(
        column=4, row=1, sticky=tkinter.E + tkinter.W)
    close = tkinter.Button(new_top, bg=bg, fg=fg, text='关闭子线程连接', font=('黑体', 11),width=20, height=2, command=close_func)
    close.grid(column=0, row=1, sticky=tkinter.E + tkinter.W)
    keep = tkinter.Button(new_top, bg=bg, fg=fg, text='保持线程连接', font=('黑体', 11),width=20, height=2, command=keepFunc)
    keep.grid(column=1, row=1, sticky=tkinter.E + tkinter.W)
    tkinter.Button(new_top, bg=bg, fg=fg, text='格式化输出', font=('黑体', 11),width=20, height=2, command=not_out).grid(
        column=2, row=1, sticky=tkinter.E + tkinter.W)
    tkinter.Button(new_top, bg=bg, fg=fg, text='启动CoTan命令行', font=('黑体', 11),width=20, height=2,
                   command=pipeFunc,state=tkinter.DISABLED).grid(column=3, row=1, sticky=tkinter.E + tkinter.W)
    new_top.update()
    return text,new_top,[close,keep]

def progress_bar(*args, name='CoTan_Git >>> 运行中...', **kwargs):
    new_top = tkinter.Toplevel(bg=bg)
    new_top.title(name)
    new_top.geometry('+10+10')  # 设置所在位置
    mpb = ttk.Progressbar(new_top, orient="horizontal", length=300, mode="determinate")
    mpb.pack()
    new_top.resizable(width=False, height=False)
    mpb["maximum"] = 50
    mpb["value"] = 0
    for i in range(50):
        mpb["value"] = i + 1
        new_top.update()
        top.update()
        time.sleep(0.001)
    new_top.destroy()