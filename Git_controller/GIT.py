import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askdirectory, askopenfilenames
import os
from Git_controller import GitController
from tkinter.scrolledtext import ScrolledText
import time
import threading


def git_main():
    global SCREEN, git, PATH, bg_color, buttom_color, word_color, repo_list, last_name, file_list
    file_list = []
    PATH = os.getcwd()
    git = GitController.git_Ctrol()
    repo_list = []
    SCREEN = tkinter.Tk()
    last_name = None
    bg_color = '#FFFAFA'  # 主颜色
    buttom_color = '#FFFAFA'  # 按钮颜色
    word_color = '#000000'  # 文字颜色
    SCREEN["bg"] = bg_color
    FONT = ('黑体', 11)  # 设置字体
    SCREEN.title('CoTan仓库管理器')
    SCREEN.resizable(width=False, height=False)
    SCREEN.geometry('+10+10')  # 设置所在位置

    width_B = 13  # 标准宽度
    height_B = 2
    a_y = 0
    a_x = 0

    global clone_repo, repo_box, repo_dir
    global commit_message, head, master, no_fast_forward
    global tag_name, tag_message, tag_commit, show_search_key
    global remote_ssh, remote_name, remote_branch, local_branch, push_bind, allow_history
    global branch_name, stash_name, commit, origin_branch

    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='克隆仓库',
        command=clone_git,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='打开仓库',
        command=repo_init,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='查看文件',
        command=update_git_file_select,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='克隆URL:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    clone_repo = tkinter.Entry(SCREEN, width=width_B * 2)
    clone_repo.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    repo_box = tkinter.Listbox(SCREEN, width=width_B * 3, height=height_B * 4)
    repo_box.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=4,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.S +
        tkinter.N)

    a_y += 4
    tkinter.Label(
        SCREEN,
        text='【仓库文件列表】',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B *
        3,
        height=height_B).grid(
        column=a_x,
        columnspan=3,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.W +
        tkinter.S +
        tkinter.N)  # 设置说明

    a_y += 1
    repo_dir = tkinter.Listbox(SCREEN, width=width_B * 3, height=height_B * 4)
    repo_dir.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=4,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.S +
        tkinter.N)

    a_y += 4
    tkinter.Label(
        SCREEN,
        text='【添加文件列表】',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B *
        3,
        height=height_B).grid(
        column=a_x,
        columnspan=3,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.W +
        tkinter.S +
        tkinter.N)  # 设置说明

    global file_dir, file_box

    a_y += 1
    file_dir = tkinter.Entry(SCREEN, width=width_B * 2)
    file_dir.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.N +
        tkinter.S)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='填充路径并添加',
        command=add_file_by_git,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='直接添加',
        command=add_file_input,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='选择文件',
        command=add_file_list,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='把文件移除出列表',
        command=del_file,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='清空列表',
        command=clean_file,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    file_box = tkinter.Listbox(SCREEN, width=width_B * 3, height=height_B * 4)
    file_box.grid(
        column=a_x,
        row=a_y,
        columnspan=3,
        rowspan=4,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.S +
        tkinter.N)

    a_y += 4
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='添加暂存区文件',
        command=add,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='移除暂存区文件',
        command=remove_the_staging,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='提交到git',
        command=commit,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='查看执行日志',
        command=lambda: not_parameters_call(
            git.do_log),
        font=FONT,
        width=width_B,
        height=height_B).grid(
            column=a_x,
            row=a_y,
            sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='查看文件日志',
        command=log,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='查看状态',
        command=lambda: not_parameters_call(
            git.status),
        font=FONT,
        width=width_B,
        height=height_B).grid(
            column=a_x +
            2,
            row=a_y,
            sticky=tkinter.E +
        tkinter.W)

    global log_type, reset_type
    a_y += 1
    log_type = []
    lable = ['显示轴', 'commit完全显示', '简化显示']  # 复选框
    for i in range(3):
        log_type.append(tkinter.IntVar())
        tkinter.Checkbutton(SCREEN,
                            bg=bg_color,
                            fg=word_color,
                            activebackground=bg_color,
                            activeforeground=word_color,
                            selectcolor=bg_color,
                            text=lable[i],
                            variable=log_type[-1]).grid(column=a_x + i,
                                                        row=a_y,
                                                        sticky=tkinter.W)
        log_type[-1].set(1)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='版本回退',
        command=reset_head,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='放弃修改',
        command=checkout_file,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='删除文件',
        command=remove_file,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    reset_type = tkinter.IntVar()  # 正，负，0
    lable = ['回退到工作区', '回退到暂存区', '无痕回退']  # 复选框
    for i in range(3):
        tkinter.Radiobutton(
            SCREEN,
            bg=bg_color,
            fg=word_color,
            activebackground=bg_color,
            activeforeground=word_color,
            selectcolor=bg_color,
            text=lable[i],
            variable=reset_type,
            value=i).grid(
            column=a_x + i,
            row=a_y,
            sticky=tkinter.W)

    a_x += 3
    tkinter.Label(
        SCREEN,
        text='',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=1).grid(
        column=a_x,
        row=a_y)  # 设置说明
    a_x += 1
    a_y = 0

    tkinter.Label(
        SCREEN,
        text='【参数操作】',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B *
        3,
        height=height_B).grid(
        column=a_x,
        columnspan=3,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.W +
        tkinter.S +
        tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='提交描述:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    commit_message = tkinter.Entry(SCREEN, width=width_B * 2)
    commit_message.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='diff分支:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    master = tkinter.Entry(SCREEN, width=width_B * 2)
    master.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='回退版本号:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    head = tkinter.Entry(SCREEN, width=width_B * 2)
    head.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='本地分支:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    branch_name = tkinter.Entry(SCREEN, width=width_B * 2)
    branch_name.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='远程分支:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    origin_branch = tkinter.Entry(SCREEN, width=width_B * 2)
    origin_branch.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='远程仓库链接:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    remote_ssh = tkinter.Entry(SCREEN, width=width_B)
    remote_ssh.grid(
        column=a_x +
        1,
        columnspan=2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='远程仓库名:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    remote_name = tkinter.Entry(SCREEN, width=width_B)
    remote_name.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='commit:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    commit = tkinter.Entry(SCREEN, width=width_B)
    commit.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='标签名字:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    tag_name = tkinter.Entry(SCREEN, width=width_B)
    tag_name.grid(
        column=a_x +
        1,
        columnspan=2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='查询关键字:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    show_search_key = tkinter.Entry(SCREEN, width=width_B)
    show_search_key.grid(
        column=a_x +
        1,
        columnspan=2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='工作区序号:',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y)
    stash_name = tkinter.Entry(SCREEN, width=width_B)
    stash_name.grid(
        column=a_x +
        1,
        row=a_y,
        columnspan=2,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Label(
        SCREEN,
        text='【高级操作】',
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=width_B *
        3,
        height=height_B).grid(
        column=a_x,
        columnspan=3,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.W +
        tkinter.S +
        tkinter.N)  # 设置说明

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='查看分支',
        command=lambda: not_parameters_call(
            git.branch_view),
        font=FONT,
        width=width_B,
        height=height_B).grid(
            column=a_x,
            row=a_y,
            sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='新建分支',
        command=add_new_branch,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='切换分支',
        command=switch_branch,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='删除分支',
        command=lambda: del_branch(1),
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='丢弃分支',
        command=lambda: del_branch(0),
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='合并分支',
        command=switch_branch,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    no_fast_forward = tkinter.IntVar()
    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='合并分支',
        command=branch_merge,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='退出冲突处理',
        command=lambda: not_parameters_call(
            git.merge_abort),
        font=FONT,
        width=width_B,
        height=height_B).grid(
            column=a_x +
            2,
            row=a_y,
            sticky=tkinter.E +
        tkinter.W)
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text='使用快速合并',
        variable=no_fast_forward).grid(
        column=a_x + 1,
        row=a_y,
        sticky=tkinter.W)
    no_fast_forward.set(0)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='连接远程仓库',
        command=add_remote,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='推送到远程仓库',
        command=lambda: pull_push_remote(1),
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='从远程仓库抓取',
        command=lambda: pull_push_remote(0),
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    push_bind = tkinter.IntVar()
    allow_history = tkinter.IntVar()
    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='分支绑定',
        command=bind_remote_branch,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text='无视历史记录',
        variable=allow_history).grid(
        column=a_x + 1,
        row=a_y,
        sticky=tkinter.W)
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text='推送时绑定',
        variable=push_bind).grid(
        column=a_x + 2,
        row=a_y,
        sticky=tkinter.W)
    allow_history.set(0)
    push_bind.set(0)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='应用标签',
        command=add_tag,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='查看已有标签',
        command=lambda: show_tag(1),
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='查询commit记录',
        command=lambda: show_tag(0),
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='推送标签',
        command=push_tag,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='推送所有标签',
        command=push_all_tag,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='删除本地标签',
        command=del_tag,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='删除远程标签',
        command=del_remote_tag,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='删除远程分支',
        command=del_remote_branch,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='刷新远程分支',
        command=fetch_remote,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='commit补丁',
        command=cherry_pick,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='删除远程仓库',
        command=del_remote,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='工作区列表',
        command=lambda: not_parameters_call(
            git.stash_list),
        font=FONT,
        width=width_B,
        height=height_B).grid(
            column=a_x +
            2,
            row=a_y,
            sticky=tkinter.E +
        tkinter.W)

    global branch_new_name
    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='文件回退',
        command=reset_file,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='分支重命名',
        command=branch_new,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    branch_new_name = tkinter.Entry(SCREEN, width=width_B)
    branch_new_name.grid(column=a_x + 2, row=a_y, sticky=tkinter.E + tkinter.W)

    a_y += 1
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='保存工作区',
        command=lambda: not_parameters_call(
            git.save_stash),
        font=FONT,
        width=width_B,
        height=height_B).grid(
            column=a_x,
            row=a_y,
            sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='恢复工作区',
        command=lambda: open_stash(1),
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        1,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='删除工作区',
        command=lambda: open_stash(0),
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)

    global customize_input, threaded_refresh, asynchronous_display
    a_y += 1
    threaded_refresh = tkinter.IntVar()
    asynchronous_display = tkinter.IntVar()
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text='多进程刷新',
        variable=threaded_refresh).grid(
        column=0,
        row=a_y,
        sticky=tkinter.W)
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text='异步显示',
        variable=asynchronous_display).grid(
        column=1,
        row=a_y,
        sticky=tkinter.W)
    customize_input = tkinter.Entry(SCREEN, width=width_B * 3)
    customize_input.grid(
        column=2,
        row=a_y,
        columnspan=4,
        sticky=tkinter.E +
        tkinter.W +
        tkinter.N +
        tkinter.S)

    tkinter.Button(
        SCREEN,
        bg=buttom_color,
        fg=word_color,
        text='执行操作',
        command=customize,
        font=FONT,
        width=width_B,
        height=height_B).grid(
        column=a_x +
        2,
        row=a_y,
        sticky=tkinter.E +
        tkinter.W)
    threaded_refresh.set(0)
    asynchronous_display.set(1)
    tag_message = commit_message
    tag_commit = commit
    remote_branch = origin_branch
    local_branch = branch_name

    SCREEN.mainloop()


def branch_new():  # 克隆仓库
    global branch_name, branch_new_name
    new_name = branch_new_name.get()
    old_name = branch_name.get()
    cli(git.rename_branch, (get_repo_name(), old_name, new_name), show_screen=False)
    update_repo_box()


def clone_git():  # 克隆仓库
    global clone_repo
    new_dir = askdirectory(title='选择仓库地址')
    if new_dir == '':
        return False
    name = git.clone_repo(new_dir)
    clone_core(name, clone_repo.get())
    update_repo_box()


def clone_core(name, url):
    cli(git.clone, (name, url), break_time=0, tip_text=f'{url}:正在执行克隆操作', is_threaded_refresh=True, is_asynchronous_display=True)
    git.after_clone(name)
    update_git_file_last()


def customize():
    global git, customize_input, threaded_refresh, asynchronous_display
    command = customize_input.get()
    cli(git.customize_command, (get_repo_name(), command), break_time=0, tip_text=f'{command}:操作进行中',
        is_threaded_refresh=bool(threaded_refresh.get()), is_asynchronous_display=bool(asynchronous_display.get()))
    update_git_file_last()


def fetch_remote():
    global remote_branch, local_branch, git, remote_name
    branch = remote_branch.get()
    remote = remote_name.get()
    local = local_branch.get()
    cli(git.fetch, (get_repo_name(), local, remote, branch), break_time=0, tip_text=f'此操作需要连接远程仓库，请稍等...', is_threaded_refresh=True,
        is_asynchronous_display=True)
    update_git_file_last()


def del_tag():
    global git, remote_name, tag_name
    tag = tag_name.get()
    cli(git.del_tag, (get_repo_name(), tag))
    update_git_file_last()


def del_remote_branch():
    global git, remote_name, tag_name
    remote = remote_name.get()
    branch = remote_branch.get()
    cli(git.del_branch_remote, (get_repo_name(), remote, branch), break_time=0, tip_text=f'此操作需要连接远程仓库，请稍等...', is_threaded_refresh=True,
        is_asynchronous_display=True)
    update_git_file_last()


def del_remote_tag():
    global git, remote_name, tag_name
    remoto = remote_name.get()
    tag = tag_name.get()
    cli(git.del_tag_remote, (get_repo_name(), remoto, tag), break_time=0, tip_text=f'此操作需要连接远程仓库，请稍等...', is_threaded_refresh=True,
        is_asynchronous_display=True)
    update_git_file_last()


def push_all_tag():
    global git, remote_name
    remoto = remote_name.get()
    cli(git.push_all_tag, (get_repo_name(), remoto), break_time=0, tip_text=f'此操作需要连接远程仓库，请稍等...', is_threaded_refresh=True, is_asynchronous_display=True)
    update_git_file_last()


def push_tag():
    global tag_name, git, remote_name
    tag_name = tag_name.get()
    remoto = remote_name.get()
    cli(git.push_tag, (get_repo_name(), tag_name, remoto), break_time=0, tip_text=f'此操作需要连接远程仓库，请稍等...', is_threaded_refresh=True,
        is_asynchronous_display=True)
    update_git_file_last()


def add_tag():
    global tag_name, git, commit, tag_message
    tag_name = tag_name.get()
    commit = tag_commit.get()
    tag_message = tag_message.get()
    cli(git.add_tag, (get_repo_name(), tag_name, commit, tag_message), show_screen=False)
    update_git_file_last()


def show_tag(type_):
    global show_search_key, git
    key = show_search_key.get()
    cli({1: git.get_tag_list, 0: git.search_commit}.get(
        type_, git.search_commit), (get_repo_name(), key))
    update_git_file_last()


def pull_push_remote(type_):
    global remote_branch, local_branch, git, allow_history, remote_name
    branch = remote_branch.get()
    remote = remote_name.get()
    local = local_branch.get()
    allow = bool(allow_history.get())
    parameters_u = bool(push_bind.get())
    parameters_f = tkinter.messagebox.askokcancel('提示', f'是否需要强制推送？(强制推送不被建议)')
    cli({0: git.pull_from_remote,
         1: git.push_to_remote}.get(type_,
                                    git.pull_from_remote), (get_repo_name(),
                                                            local,
                                                            remote,
                                                            branch,
                                                            allow,
                                                            parameters_u,
                                                            parameters_f), break_time=0, tip_text=f'此操作需要连接远程仓库，请稍等...', is_threaded_refresh=True,
        is_asynchronous_display=True)
    update_git_file_last()


def bind_remote_branch():
    global remote_branch, local_branch, git
    remote = remote_branch.get()
    local = local_branch.get()
    cli(git.bind_branch, (get_repo_name(), local, remote))
    update_git_file_last()


def del_remote():
    global remote_ssh, remote_name, git
    name = remote_name.get()
    cli(git.del_remote, (get_repo_name(), name))
    update_git_file_last()


def add_remote():
    global remote_ssh, remote_name, git
    ssh = remote_ssh.get()
    name = remote_name.get()
    cli(git.remote_add, (get_repo_name(), ssh, name))
    update_git_file_last()


def cherry_pick():
    global commit, git
    commit = commit.get()
    cli(git.cherry_pick, (get_repo_name(), commit))
    update_git_file_last()


def open_stash(type_):
    global stash_name, git
    stash_num = stash_name.get()
    if stash_num == '':
        stash_num = '0'
    cli([git.drop_stash, git.apply_stash][type_], (get_repo_name(), stash_num))
    update_git_file_last()


def branch_merge():
    global branch_name, git, no_fast_forward, commit_message
    message = commit_message.get()
    parameters_no_ff = not bool(no_fast_forward.get())  # 对于no_ff来说，True - 使用快速合并，所以要翻转
    if message.replace(' ', '') == '' and parameters_no_ff:
        tkinter.messagebox.showinfo(
            '警告!', '非常遗憾，我不同意你commit而不添加任何描述！\n描述是很重要的！'
            '(如果你不想添加描述，请使用快速合并，但我并不建议！)')
        return False
    name = branch_name.get()
    cli(git.merge_branch, (get_repo_name(), name, parameters_no_ff, message))
    update_git_file_last()


def del_branch(type_):
    global branch_name, git
    name = branch_name.get()
    cli(git.del_branch, (get_repo_name(), name, type_))
    update_git_file_last()


def switch_branch():
    global branch_name, git
    name = branch_name.get()
    cli(git.switch_branch, (get_repo_name(), name), break_time=1, show_screen=False)
    update_git_file_last()


def add_new_branch():
    global branch_name, git, origin_branch
    name = branch_name.get()
    origin = origin_branch.get()
    cli(git.new_branch, (get_repo_name(), name, origin), break_time=1, show_screen=False)
    update_git_file_last()


def remove_file():
    global git, head, file_list
    if file_list == []:
        return False
    cli(git.rm, (get_repo_name(), file_list))
    update_git_file_last()


def checkout_file():  # 从暂存区、仓库返回文件
    global git, head, file_list
    if file_list == []:
        return False
    cli(git.checkout_version, (get_repo_name(), file_list))
    update_git_file_last()


def reset_file():  # 使用reset回退文件
    global git, head, reset_type, file_list
    repo_head = head.get()
    if repo_head == '':
        repo_head = 'HEAD~1'
    cli(git.back_version_file, (get_repo_name(), repo_head, file_list))
    update_git_file_last()


def reset_head():
    global git, head, reset_type
    repo_head = head.get()
    if repo_head == '':
        repo_head = 'HEAD~1'
    Type = reset_type.get()
    cli(git.back_version, (get_repo_name(), repo_head, Type))
    update_git_file_last()


def cli(func, args, name='CoTan Git', break_time=0, show_screen=True, tip_text='',
        is_threaded_refresh=False, is_asynchronous_display=False):
    command_thread = func(*args)
    format_flat = True
    stop_key = GitController.stop_key

    def save_to_txt():
        nonlocal data
        dic = asksaveasfilename(title='选择文件保存位置', filetypes=[("TXT", ".txt")])
        try:
            if dic == '':
                return False
            if dic[-4] == '.txt':
                pass
            else:
                raise Exception
        except BaseException:
            dic += '.txt'
        with open(dic, 'w', encoding='utf-8') as f:
            f.write(data)
    keep_button = True
    stop_button = True

    def update_button():
        if not keep_button:
            button_list[1].config(state=tkinter.DISABLED)
        if not stop_button:
            button_list[0].config(state=tkinter.DISABLED)

    def stop():
        nonlocal start, keep_button, stop_button
        start = 0
        stop_button = False
        keep_button = False
        update_button()

    def keep():
        nonlocal start, keep_button
        start = float('inf')
        keep_button = False
        update_button()

    def pipe(): pass

    def format():
        nonlocal text, out_data, data, format_flat
        text.clear()
        if format_flat:
            text.insert(tkinter.END, data)
        else:
            text.insert(tkinter.END, out_data)
        format_flat = not format_flat
    start = time.time()
    data = ''
    out_data = ''  # 包含out的data
    if show_screen:
        text, cli_screen, button_list = show_cli(
            save_to_txt, stop, keep, format, pipe, name=name)  # [close,keep]
        update_button()
        if tip_text != '':
            text.insert('0.0', f'载入前提示>>> {tip_text}\n')
            out_data += f'载入前提示>>> {tip_text}\n'
            data += f'{tip_text}\n'
        cli_screen.update()
    else:
        u = threading.Thread(target=progress_bar)
        u.start()
    SCREEN.update()

    def update_screen():
        nonlocal start
        while True:
            try:
                SCREEN.update()
                if show_screen:
                    try:
                        cli_screen.update()
                    except BaseException:
                        pass
                if time.time() - start >= break_time and break_time != 0:
                    raise Exception
                elif break_time == 0 and start == 0:
                    raise Exception
            except BaseException:
                start = 0
                break

    if is_threaded_refresh or not is_asynchronous_display:
        # 如果没有启动到多进程的效果，请检查Update是不是加了()，这里需要回调
        threaded_update = threading.Thread(target=update_screen)
        threaded_update.start()

    if is_asynchronous_display:  # 等待后显示
        if break_time == 0:
            break_ti = None  # 此处break_ti是为了别面覆盖break_time，因为Update进程需要用
        else:
            break_ti = break_time

        def wait_command_thread():
            nonlocal start
            command_thread.wait(break_ti)
            start = 0
        threaded_update = threading.Thread(target=wait_command_thread)  # 这么做不是多此一举，如果没有wait，进程并不会退出
        threaded_update.start()
        update_screen()  # 遇到sleep等主线程阻塞，top.update等会阻塞子线程，因此，必须保证主线程不会被wait所阻塞
        out = command_thread.stdout.read().split('\n')
        for i in out:
            if show_screen:
                try:  # 如果界面被关掉了，会报错
                    cli_screen.title(f'{name} : 运行中')
                except BaseException:
                    text, cli_screen, button_list = show_cli(
                        save_to_txt, stop, keep, format, pipe, name=f'{name} : 运行中')
                    update_button()
                    text.insert(tkinter.END, out_data)
                if stop and i.replace(' ', '').replace('\n', '') != stop_key:
                    text.insert(tkinter.END, f'[out]> {i}\n')
                    data += i + '\n'
                    out_data += f'[out]> {i}\n'
            else:
                break
        else:
            text.insert(tkinter.END, '[END]')
            out_data += f'[END]'
            data += f'[END]'
        start = 0
    else:  # 即时显示
        while True:
            # 界面设置
            try:  # 如果界面被关掉了，会报错
                if show_screen:
                    cli_screen.title(f'{name} : 运行中')
            except BaseException:
                text, cli_screen, button_list = show_cli(
                    save_to_txt, stop, keep, format, pipe, name=f'{name} : 运行中')
                update_button()
                text.insert(tkinter.END, out_data)
            # 界面刷新
            try:
                if not is_threaded_refresh:
                    SCREEN.update()
                    if show_screen:
                        cli_screen.update()
            except BaseException:
                break
            # 输出字符
            try:
                # .decode(str_code)#不需要decode,因为Popen已经设置了universal_newlines=True
                i = command_thread.stdout.readline()
                bool_text = i.replace(' ', '').replace('\n', '')
                if bool_text != '':
                    if stop and bool_text == stop_key:
                        start = 0
                    else:
                        if show_screen:
                            text.insert(tkinter.END, f'[out]> {i}')
                        data += i
                        out_data += f'[out]> {i}'
                if command_thread.returncode == 0 or (
                        time.time() -
                        start >= break_time and break_time != 0) or (
                        break_time == 0 and start == 0):
                    if show_screen:
                        text.insert(tkinter.END, '[END]')
                        out_data += f'[END]'
                        data += f'[END]'
                    break
                elif command_thread.returncode is not None:
                    raise Exception
            except BaseException:
                try:
                    if show_screen:
                        text.insert(tkinter.END, '[ERROR]')
                        out_data += f'[ERROR]'
                        data += f'[ERROR]'
                    raise Exception
                except BaseException:
                    break
        try:  # 如果界面被关掉了，会报错
            if show_screen:
                cli_screen.title(f'{name} : 运行完毕')
        except BaseException:
            pass
        command_thread.kill()
    try:
        if show_screen:
            button_list[0].config(state=tkinter.DISABLED)
            button_list[1].config(state=tkinter.DISABLED)
    except BaseException:
        pass
    return data


def log():
    global git, log_type
    name = get_repo_name()
    graph = bool(log_type[0].get())
    abbrev = bool(log_type[1].get())
    pretty = bool(log_type[2].get())
    cli(git.log, (name, graph, pretty, abbrev))
    update_git_file_last()


def not_parameters_call(func):
    global git
    name = get_repo_name()
    cli(func, (name,))
    update_git_file_last()


def commit():
    global git, commit_message
    m = commit_message.get()
    if m.replace(' ', '') == '':
        tkinter.messagebox.showinfo(
            '警告!', '非常遗憾，我不同意你commit而不添加任何描述！\n描述是很重要的！')
        return False
    name = get_repo_name()
    cli(git.commit_file, (name, m))
    update_git_file_last()


def diff():
    global git, master
    branch = master.get()
    if branch == '':
        branch = 'HEAD'
    cli(git.diff_file, (get_repo_name(), branch))
    update_git_file_last()


def remove_the_staging():
    global git, last_name, file_list
    dic = file_list
    if dic == []:
        dic = '.'
    cli(git.reset_file, (get_repo_name(), dic))
    update_git_file_last()


def add():
    global git, last_name, file_list
    dic = file_list
    if dic == []:
        dic = '.'  # 查一下取消的dic
    cli(git.add_file, (get_repo_name(), dic))
    update_git_file_last()


def add_file_list():
    global file_list, file_box
    new_file = set(askopenfilenames(title=f'选择文件'))
    have_file = set(file_list)
    file_list += list(new_file - (new_file & have_file))  # 筛选出重复
    update_file_box()


def add_file_input():
    global file_dir
    new_dir = file_dir.get()
    if new_dir.replace(' ', '') != '' and new_dir not in file_list:
        file_list.append(new_dir)
    update_file_box()


def add_file_by_git():
    global file_dir
    new_dir = file_dir.get()
    if new_dir.replace(' ', '') != '':
        name = get_repo_name()
        new_dir = git.make_dir(name, new_dir)
        if new_dir not in file_list:
            file_list.append(new_dir)
    update_file_box()


def del_file():
    global file_list, file_box
    try:
        del file_list[file_box.curselection()]
        update_file_box()
    except BaseException:
        pass


def clean_file():
    global file_list
    file_list = []
    update_file_box()


def update_file_box():
    global file_list, file_box
    file_box.delete(0, tkinter.END)
    file_box.insert(tkinter.END, *file_list)


def update_git_file_last():
    global last_name
    if last_name is None:
        return False
    update_git_file_core(last_name)


def update_git_file_select():
    name = get_repo_name()
    update_git_file_core(name)


def update_git_file_core(name):
    global git, repo_dir, last_name
    dir_list = git.get_dir(name)
    try:  # 窗口可能已经关闭
        repo_dir.delete(0, tkinter.END)
        repo_dir.insert(tkinter.END, *dir_list)
    except BaseException:
        pass
    last_name = name


def repo_init():  # 创建仓库
    global git
    new_dir = askdirectory(title='选择仓库地址')
    if new_dir == '':
        return False
    git.open_repo(new_dir)
    update_repo_box()


def get_repo_name():  # 获得名字统一接口
    global git, repo_list, repo_box
    try:
        return repo_list[repo_box.curselection()[0]]
    except BaseException:
        try:
            return repo_list[0]
        except BaseException:
            return None


def update_repo_box():
    global git, repo_list, repo_box
    repo_list = list(git.get_git_dict().keys())
    repo_box.delete(0, tkinter.END)
    repo_box.insert(tkinter.END, *repo_list)


def show_cli(
        out_func,
        close_func,
        keepFunc,
        not_out,
        pipeFunc,
        name='CoTan_Git >>> 命令行'):
    global bg_color
    cli_screen = tkinter.Toplevel(bg=bg_color)
    cli_screen.title(name)
    cli_screen.geometry('+10+10')  # 设置所在位置
    cli_screen.resizable(width=False, height=False)

    class ScrolledCli(ScrolledText):
        def __init__(self, *args, **kwargs):
            super(ScrolledCli, self).__init__(*args, **kwargs)

        def insert(self, index, chars, *args):
            text.config(state=tkinter.NORMAL)
            super(ScrolledCli, self).insert(index, chars, *args)
            text.config(state=tkinter.DISABLED)

        def clear(self):
            text.config(state=tkinter.NORMAL)
            self.delete('0.0', tkinter.END)
            text.config(state=tkinter.DISABLED)

    text = ScrolledCli(cli_screen, font=('黑体', 11), height=30, width=100)
    text.grid(column=0, row=0, columnspan=5, sticky=tkinter.E + tkinter.W)
    text.config(state=tkinter.DISABLED)
    tkinter.Button(
        cli_screen,
        bg=bg_color,
        fg=word_color,
        text='输出文档',
        font=(
            '黑体',
            11),
        width=20,
        height=2,
        command=out_func).grid(
            column=4,
            row=1,
            sticky=tkinter.E +
        tkinter.W)
    close = tkinter.Button(
        cli_screen,
        bg=bg_color,
        fg=word_color,
        text='关闭子线程连接',
        font=(
            '黑体',
            11),
        width=20,
        height=2,
        command=close_func)
    close.grid(column=0, row=1, sticky=tkinter.E + tkinter.W)
    keep = tkinter.Button(
        cli_screen,
        bg=bg_color,
        fg=word_color,
        text='保持线程连接',
        font=(
            '黑体',
            11),
        width=20,
        height=2,
        command=keepFunc)
    keep.grid(column=1, row=1, sticky=tkinter.E + tkinter.W)
    tkinter.Button(
        cli_screen,
        bg=bg_color,
        fg=word_color,
        text='格式化输出',
        font=(
            '黑体',
            11),
        width=20,
        height=2,
        command=not_out).grid(
            column=2,
            row=1,
            sticky=tkinter.E +
        tkinter.W)
    tkinter.Button(
        cli_screen,
        bg=bg_color,
        fg=word_color,
        text='启动CoTan命令行',
        font=(
            '黑体',
            11),
        width=20,
        height=2,
        command=pipeFunc,
        state=tkinter.DISABLED).grid(
            column=3,
            row=1,
            sticky=tkinter.E +
        tkinter.W)
    cli_screen.update()
    return text, cli_screen, [close, keep]


def progress_bar(*args, name='CoTan_Git >>> 运行中...', **kwargs):
    progress_screen = tkinter.Toplevel(bg=bg_color)
    progress_screen.title(name)
    progress_screen.geometry('+10+10')  # 设置所在位置
    mpb = ttk.Progressbar(
        progress_screen,
        orient="horizontal",
        length=300,
        mode="determinate")
    mpb.pack()
    progress_screen.resizable(width=False, height=False)
    mpb["maximum"] = 50
    mpb["value"] = 0
    for i in range(50):
        mpb["value"] = i + 1
        progress_screen.update()
        SCREEN.update()
        time.sleep(0.001)
    progress_screen.destroy()
