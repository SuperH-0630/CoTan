import time
import threading
import tkinter
import os

import tkinter.messagebox
from tkinter import ttk
from newtkinter import asksaveasfilename, askdirectory, askopenfilenames
from tkinter.scrolledtext import ScrolledText

import gitrepo.template
from gitrepo import controller
from system import exception_catch


class UIAPI:
    @staticmethod
    @exception_catch()
    def cli_gui(
            func,
            args,
            name="CoTan Git",
            break_time=0,
            show_screen=True,
            tip_text="",
            is_threaded_refresh=False,
            is_asynchronous_display=False,
    ):
        command_thread = func(*args)
        format_flat = True
        stop_key = gitrepo.template.stop_key

        def save_to_txt():
            nonlocal data
            dic = asksaveasfilename(title="选择文件保存位置", filetypes=[("TXT", ".txt")])
            if not dic.endswith(".txt"):
                dic += ".txt"
            with open(dic, "w", encoding="utf-8") as f:
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
            start = float("inf")
            keep_button = False
            update_button()

        def pipe():
            pass

        def format_information():
            nonlocal text, out_data, data, format_flat
            text.clear()
            if format_flat:
                text.insert(tkinter.END, data)
            else:
                text.insert(tkinter.END, out_data)
            format_flat = not format_flat

        start = time.time()
        data = ""
        out_data = ""  # 包含out的data

        if show_screen:
            text, cli_screen, button_list = API.show_cli_gui(
                save_to_txt, stop, keep, format_information, pipe, name=name
            )  # [close,keep]
            update_button()
            if tip_text != "":
                text.insert("0.0", f"载入前提示>>> {tip_text}\n")
                out_data += f"载入前提示>>> {tip_text}\n"
                data += f"{tip_text}\n"
            cli_screen.update()
        else:
            class TkNone:
                def title(self, *args, **kwargs):
                    return

                def insert(self, *args, **kwargs):
                    return

                def update(self, *args, **kwargs):
                    return

                def config(self, *args, **kwargs):
                    return

            text = TkNone()
            cli_screen = TkNone()
            button_list = [TkNone(), TkNone()]
            u = threading.Thread(target=API.progress_bar_gui)
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
                        finally:
                            pass
                    assert time.time() - start >= break_time != 0
                    assert break_time == 0 and start == 0
                except AssertionError:
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

            threaded_update = threading.Thread(
                target=wait_command_thread
            )  # 这么做不是多此一举，如果没有wait，进程并不会退出
            threaded_update.start()
            update_screen()  # 遇到sleep等主线程阻塞，top.update等会阻塞子线程，因此，必须保证主线程不会被wait所阻塞
            out = command_thread.stdout.read().split("\n")
            for i in out:
                if not show_screen:
                    break
                try:  # 如果界面被关掉了，会报错
                    cli_screen.title(f"{name} : 运行中")
                except tkinter.TclError:
                    text, cli_screen, button_list = API.show_cli_gui(
                        save_to_txt, stop, keep, format_information, pipe, name=f"{name} : 运行中"
                    )
                    update_button()
                    text.insert(tkinter.END, out_data)
                if stop and i.replace(" ", "").replace("\n", "") != stop_key:
                    text.insert(tkinter.END, f"[out]> {i}\n")
                    data += i + "\n"
                    out_data += f"[out]> {i}\n"
            else:
                text.insert(tkinter.END, "[END]")
                out_data += f"[END]"
                data += f"[END]"
            start = 0
        else:  # 即时显示
            while True:
                # 界面设置
                try:  # 如果界面被关掉了，会报错
                    cli_screen.title(f"{name} : 运行中")
                except tkinter.TclError:
                    text, cli_screen, button_list = API.show_cli_gui(
                        save_to_txt, stop, keep, format_information, pipe, name=f"{name} : 运行中"
                    )
                    update_button()
                    text.insert(tkinter.END, out_data)
                # 界面刷新
                try:
                    if not is_threaded_refresh:
                        SCREEN.update()
                        cli_screen.update()
                except tkinter.TclError:
                    break
                # 输出字符
                try:
                    # .decode(str_code)#不需要decode,因为Popen已经设置了universal_newlines=True
                    i = command_thread.stdout.readline()
                    bool_text = i.replace(" ", "").replace("\n", "")
                    if bool_text != "":
                        if stop and bool_text == stop_key:
                            start = 0
                        else:
                            text.insert(tkinter.END, f"[out]> {i}")
                            data += i
                            out_data += f"[out]> {i}"
                    if (
                            command_thread.returncode == 0
                            or (time.time() - start >= break_time != 0)
                            or (break_time == 0 and start == 0)
                    ):
                        text.insert(tkinter.END, "[END]")
                        out_data += f"[END]"
                        data += f"[END]"
                        break
                    elif command_thread.returncode is not None:
                        assert True
                except (tkinter.TclError, AssertionError):
                    if show_screen:
                        text.insert(tkinter.END, "[ERROR]")
                        out_data += f"[ERROR]"
                        data += f"[ERROR]"
                    break
            try:  # 如果界面被关掉了，会报错
                if show_screen:
                    cli_screen.title(f"{name} : 运行完毕")
            except tkinter.TclError:
                pass
            command_thread.kill()
        try:
            button_list[0].config(state=tkinter.DISABLED)
            button_list[1].config(state=tkinter.DISABLED)
        except (AttributeError, NameError):
            pass
        return data

    @staticmethod
    @exception_catch()
    def progress_bar_gui(*args, name="CoTan_Git >>> 运行中...", **kwargs):
        progress_screen = tkinter.Toplevel(bg=bg_color)
        progress_screen.title(name)
        progress_screen.geometry("+10+10")  # 设置所在位置
        mpb = ttk.Progressbar(
            progress_screen, orient="horizontal", length=300, mode="determinate"
        )
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

    @staticmethod
    @exception_catch()
    def get_commit_id_gui():
        global commit
        the_commit = commit.get()
        return the_commit

    @staticmethod
    @exception_catch()
    def show_cli_gui(
            out_func, close_func, keep_func, not_out, pipe_func, name="CoTan_Git >>> 命令行"
    ):
        global bg_color
        cli_screen = tkinter.Toplevel(bg=bg_color)
        cli_screen.title(name)
        cli_screen.geometry("+10+10")  # 设置所在位置
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
                self.delete("0.0", tkinter.END)
                text.config(state=tkinter.DISABLED)

        text = ScrolledCli(cli_screen, font=("黑体", 11), height=30, width=100)
        text.grid(column=0, row=0, columnspan=5, sticky=tkinter.E + tkinter.W)
        text.config(state=tkinter.DISABLED)
        tkinter.Button(
            cli_screen,
            bg=bg_color,
            fg=word_color,
            text="输出文档",
            font=("黑体", 11),
            width=20,
            height=2,
            command=out_func,
        ).grid(column=4, row=1, sticky=tkinter.E + tkinter.W)
        close = tkinter.Button(
            cli_screen,
            bg=bg_color,
            fg=word_color,
            text="关闭子线程连接",
            font=("黑体", 11),
            width=20,
            height=2,
            command=close_func,
        )
        close.grid(column=0, row=1, sticky=tkinter.E + tkinter.W)
        keep = tkinter.Button(
            cli_screen,
            bg=bg_color,
            fg=word_color,
            text="保持线程连接",
            font=("黑体", 11),
            width=20,
            height=2,
            command=keep_func,
        )
        keep.grid(column=1, row=1, sticky=tkinter.E + tkinter.W)
        tkinter.Button(
            cli_screen,
            bg=bg_color,
            fg=word_color,
            text="格式化输出",
            font=("黑体", 11),
            width=20,
            height=2,
            command=not_out,
        ).grid(column=2, row=1, sticky=tkinter.E + tkinter.W)
        tkinter.Button(
            cli_screen,
            bg=bg_color,
            fg=word_color,
            text="启动CoTan命令行",
            font=("黑体", 11),
            width=20,
            height=2,
            command=pipe_func,
            state=tkinter.DISABLED,
        ).grid(column=3, row=1, sticky=tkinter.E + tkinter.W)
        cli_screen.update()
        return text, cli_screen, [close, keep]

    @staticmethod
    @exception_catch()
    def repo_init_gui():
        new_dir = askdirectory(title="选择仓库地址")
        if new_dir == "":
            raise Exception
        return new_dir

    @staticmethod
    @exception_catch()
    def get_repo_name_gui():  # 获得名字统一接口
        global git, repo_list, repo_box
        try:
            return repo_list[repo_box.curselection()[0]]
        except IndexError:
            try:
                return repo_list[0]
            except IndexError:
                return None

    @staticmethod
    @exception_catch()
    def update_repo_box_gui():
        global git, repo_list, repo_box
        repo_list = list(git.get_git_dict().keys())
        repo_box.delete(0, tkinter.END)
        repo_box.insert(tkinter.END, *repo_list)

    @staticmethod
    @exception_catch()
    def update_file_box_gui():
        global file_list, file_box
        file_box.delete(0, tkinter.END)
        file_box.insert(tkinter.END, *file_list)

    @staticmethod
    @exception_catch()
    def update_git_file_last_gui():
        global last_name
        if last_name is None:
            return False
        API.update_git_file_gui(last_name)

    @staticmethod
    @exception_catch()
    def update_git_file_select_gui():
        name = API.get_repo_name_gui()
        API.update_git_file_gui(name)

    @staticmethod
    @exception_catch()
    def update_git_file_gui(name):
        global git, repo_dir, last_name
        dir_list = git.get_dir(name)
        try:  # 窗口可能已经关闭
            repo_dir.delete(0, tkinter.END)
            repo_dir.insert(tkinter.END, *dir_list)
        finally:
            pass
        last_name = name

    @staticmethod
    @exception_catch()
    def add_file_list_gui():
        global file_list, file_box
        new_file = set(askopenfilenames(title=f"选择文件"))
        have_file = set(file_list)
        file_list += list(new_file - (new_file & have_file))  # 筛选出重复
        API.update_file_box_gui()

    @staticmethod
    @exception_catch()
    def add_file_input_dir_gui():
        global file_dir
        new_dir = file_dir.get()
        if new_dir.replace(" ", "") != "" and new_dir not in file_list:
            file_list.append(new_dir)
        API.update_file_box_gui()

    @staticmethod
    @exception_catch()
    def add_file_by_git_gui():
        global file_dir
        new_dir = file_dir.get()
        if new_dir.replace(" ", "") != "":
            name = API.get_repo_name_gui()
            new_dir = git.make_dir(name, new_dir)
            if new_dir not in file_list:
                file_list.append(new_dir)
        API.update_file_box_gui()

    @staticmethod
    @exception_catch()
    def diff_gui():
        branch = master.get()
        if branch == "":
            branch = "HEAD"
        return branch

    @staticmethod
    @exception_catch()
    def commit_file_gui():
        m = commit_message.get()
        if m.replace(" ", "") == "":
            tkinter.messagebox.showinfo("警告!", "非常遗憾，我不同意你commit而不添加任何描述！\n描述是很重要的！")
            raise Exception
        return m

    @staticmethod
    @exception_catch()
    def log_gui(log_type_):
        graph = bool(log_type_[0].get())
        abbrev = bool(log_type_[1].get())
        pretty = bool(log_type_[2].get())
        return abbrev, graph, pretty

    @staticmethod
    @exception_catch()
    def reset_head_gui():
        repo_head = head.get()
        if repo_head == "":
            repo_head = "HEAD~1"
        the_reset_type = reset_type.get()
        return repo_head, the_reset_type

    @staticmethod
    @exception_catch()
    def reset_file_gui():
        repo_head = head.get()
        if repo_head == "":
            repo_head = "HEAD~1"
        return repo_head

    @staticmethod
    @exception_catch()
    def add_new_branch_gui():
        name = API.get_branch_name_gui()
        origin = origin_branch.get()
        return name, origin

    @staticmethod
    @exception_catch()
    def branch_merge_gui():
        message = commit_message.get()
        parameters_no_ff = not bool(no_fast_forward.get())  # 对于no_ff来说，True - 使用快速合并，所以要翻转
        if message.replace(" ", "") == "" and parameters_no_ff:
            tkinter.messagebox.showinfo(
                "警告!", "非常遗憾，我不同意你commit而不添加任何描述！\n描述是很重要的！" "(如果你不想添加描述，请使用快速合并，但我并不建议！)"
            )
            raise Exception
        name = API.get_branch_name_gui()
        return message, name, parameters_no_ff

    @staticmethod
    @exception_catch()
    def get_branch_name_gui():
        return branch_name.get()

    @staticmethod
    @exception_catch()
    def get_stash_gui():
        stash_num = stash_name.get()
        return stash_num

    @staticmethod
    @exception_catch()
    def add_remote_gui():
        ssh = remote_ssh.get()
        name = remote_name.get()
        return name, ssh

    @staticmethod
    @exception_catch()
    def del_remote_gui():
        name = remote_name.get()
        return name

    @staticmethod
    @exception_catch()
    def bind_remote_branch_gui():
        remote = remote_branch.get()
        local = local_branch.get()
        return local, remote

    @staticmethod
    @exception_catch()
    def pull_push_gui():
        branch = remote_branch.get()
        remote = remote_name.get()
        local = local_branch.get()
        allow = bool(allow_history.get())
        parameters_u = bool(push_bind.get())
        parameters_f = tkinter.messagebox.askokcancel("提示", f"是否需要强制推送？(强制推送不被建议)")
        return allow, branch, local, parameters_f, parameters_u, remote

    @staticmethod
    @exception_catch()
    def get_search_key_gui():
        return show_search_key.get()

    @staticmethod
    @exception_catch()
    def add_tag_gui():
        global tag_name, commit, tag_message
        the_tag_name = tag_name.get()
        the_commit = tag_commit.get()
        the_tag_message = tag_message.get()
        return the_tag_name, the_commit, the_tag_message

    @staticmethod
    @exception_catch()
    def push_tag_gui():
        global tag_name
        the_tag_name = tag_name.get()
        remoto = remote_name.get()
        return remoto, the_tag_name

    @staticmethod
    @exception_catch()
    def get_remote_name_gui():
        remoto = remote_name.get()
        return remoto

    @staticmethod
    @exception_catch()
    def del_remote_tag_gui():
        remoto = remote_name.get()
        tag = tag_name.get()
        return remoto, tag

    @staticmethod
    @exception_catch()
    def del_remote_branch_gui():
        remote = remote_name.get()
        branch = remote_branch.get()
        return branch, remote

    @staticmethod
    @exception_catch()
    def del_tag_gui():
        tag = tag_name.get()
        return tag

    @staticmethod
    @exception_catch()
    def featch_remote_gui():
        branch = remote_branch.get()
        remote = remote_name.get()
        local = local_branch.get()
        return branch, local, remote

    @staticmethod
    @exception_catch()
    def get_customize_gui():
        command = customize_input.get()
        is_threaded_refresh = bool(threaded_refresh.get())
        is_asynchronous_display = bool(asynchronous_display.get())
        return command, is_asynchronous_display, is_threaded_refresh

    @staticmethod
    @exception_catch()
    def clone_git_gui():
        new_dir = askdirectory(title="选择仓库地址")
        name = git.clone_repo(new_dir)
        return name

    @staticmethod
    @exception_catch()
    def branch_new_gui():
        new_name = branch_new_name.get()
        old_name = API.get_branch_name_gui()
        return new_name, old_name


class API(UIAPI):
    @staticmethod
    @exception_catch()
    def branch_new():  # 克隆仓库
        new_name, old_name = API.branch_new_gui()
        API.cli_gui(git.rename_branch, (API.get_repo_name_gui(), old_name, new_name), show_screen=False)
        API.update_repo_box_gui()

    @staticmethod
    @exception_catch()
    def clone_git():  # 克隆仓库
        name = API.clone_git_gui()
        API.clone_core(name, clone_repo.get())
        API.update_repo_box_gui()

    @staticmethod
    @exception_catch()
    def clone_core(name, url):
        try:
            API.cli_gui(
                git.clone,
                (name, url),
                break_time=0,
                tip_text=f"{url}:正在执行克隆操作",
                is_threaded_refresh=True,
                is_asynchronous_display=True,
            )
            git.after_clone(name)
        except BaseException:
            raise
        finally:
            API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def customize():
        command, is_asynchronous_display, is_threaded_refresh = API.get_customize_gui()
        API.cli_gui(
            git.customize_command,
            (API.get_repo_name_gui(), command),
            break_time=0,
            tip_text=f"{command}:操作进行中",
            is_threaded_refresh=is_threaded_refresh,
            is_asynchronous_display=is_asynchronous_display,
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def fetch_remote():
        branch, local, remote = API.featch_remote_gui()
        API.cli_gui(
            git.fetch,
            (API.get_repo_name_gui(), local, remote, branch),
            break_time=0,
            tip_text=f"此操作需要连接远程仓库，请稍等...",
            is_threaded_refresh=True,
            is_asynchronous_display=True,
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def del_tag():
        tag = API.del_tag_gui()
        API.cli_gui(git.del_tag, (API.get_repo_name_gui(), tag))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def del_remote_branch():
        branch, remote = API.del_remote_branch_gui()
        API.cli_gui(
            git.del_branch_remote,
            (API.get_repo_name_gui(), remote, branch),
            break_time=0,
            tip_text=f"此操作需要连接远程仓库，请稍等...",
            is_threaded_refresh=True,
            is_asynchronous_display=True,
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def del_remote_tag():
        remoto, tag = API.del_remote_tag_gui()
        API.cli_gui(
            git.del_tag_remote,
            (API.get_repo_name_gui(), remoto, tag),
            break_time=0,
            tip_text=f"此操作需要连接远程仓库，请稍等...",
            is_threaded_refresh=True,
            is_asynchronous_display=True,
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def push_all_tag():
        remoto = API.get_remote_name_gui()
        API.cli_gui(
            git.push_all_tag,
            (API.get_repo_name_gui(), remoto),
            break_time=0,
            tip_text=f"此操作需要连接远程仓库，请稍等...",
            is_threaded_refresh=True,
            is_asynchronous_display=True,
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def push_tag():
        remoto, the_tag_name = API.push_tag_gui()
        API.cli_gui(
            git.push_tag,
            (API.get_repo_name_gui(), the_tag_name, remoto),
            break_time=0,
            tip_text=f"此操作需要连接远程仓库，请稍等...",
            is_threaded_refresh=True,
            is_asynchronous_display=True,
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def add_tag():
        the_tag_name, the_commit, the_tag_message = API.add_tag_gui()
        API.cli_gui(
            git.add_tag, (API.get_repo_name_gui(), the_tag_name, the_commit, the_tag_message), show_screen=False
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def show_tag(type_):
        global git
        key = API.get_search_key_gui()
        API.cli_gui(
            {1: git.get_tag_list, 0: git.search_commit}.get(type_, git.search_commit),
            (API.get_repo_name_gui(), key),
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def pull_push_remote(type_):
        allow, branch, local, parameters_f, parameters_u, remote = API.pull_push_gui()
        API.cli_gui(
            {0: git.pull_from_remote, 1: git.push_to_remote}.get(
                type_, git.pull_from_remote
            ),
            (API.get_repo_name_gui(), local, remote, branch, allow, parameters_u, parameters_f),
            break_time=0,
            tip_text=f"此操作需要连接远程仓库，请稍等...",
            is_threaded_refresh=True,
            is_asynchronous_display=True,
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def bind_remote_branch():
        local, remote = API.bind_remote_branch_gui()
        API.cli_gui(git.bind_branch, (API.get_repo_name_gui(), local, remote))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def del_remote():
        name = API.del_remote_gui()
        API.cli_gui(git.del_remote, (API.get_repo_name_gui(), name))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def add_remote():
        name, ssh = API.add_remote_gui()
        API.cli_gui(git.remote_add, (API.get_repo_name_gui(), ssh, name))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def cherry_pick():
        the_commit = API.get_commit_id_gui()
        API.cli_gui(git.cherry_pick, (API.get_repo_name_gui(), the_commit))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def open_stash(type_):
        stash_num = API.get_stash_gui()
        if stash_num == "":
            stash_num = "0"
        API.cli_gui([git.drop_stash, git.apply_stash][type_], (API.get_repo_name_gui(), stash_num))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def branch_merge():
        message, name, parameters_no_ff = API.branch_merge_gui()
        API.cli_gui(git.merge_branch, (API.get_repo_name_gui(), name, parameters_no_ff, message))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def del_branch(type_):
        name = API.get_branch_name_gui()
        API.cli_gui(git.del_branch, (API.get_repo_name_gui(), name, type_))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def switch_branch():
        name = API.get_branch_name_gui()
        API.cli_gui(git.switch_branch, (API.get_repo_name_gui(), name), break_time=1, show_screen=False)
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def add_new_branch():
        name, origin = API.add_new_branch_gui()
        API.cli_gui(
            git.new_branch, (API.get_repo_name_gui(), name, origin), break_time=1, show_screen=False
        )
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def remove_file():
        if not file_list:
            return False
        API.cli_gui(git.rm, (API.get_repo_name_gui(), file_list))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def checkout_file():  # 从暂存区、仓库返回文件
        if not file_list:
            return False
        API.cli_gui(git.checkout_version, (API.get_repo_name_gui(), file_list))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def reset_file():  # 使用reset回退文件
        repo_head = API.reset_file_gui()
        API.cli_gui(git.back_version_file, (API.get_repo_name_gui(), repo_head, file_list))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def reset_head():
        repo_head, the_reset_type = API.reset_head_gui()
        API.cli_gui(git.back_version, (API.get_repo_name_gui(), repo_head, the_reset_type))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def log():
        global git, log_type
        name = API.get_repo_name_gui()
        abbrev, graph, pretty = API.log_gui(log_type)
        API.cli_gui(git.log, (name, graph, pretty, abbrev))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def not_parameters_call(func):
        global git
        name = API.get_repo_name_gui()
        API.cli_gui(func, (name,))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def commit_file():
        name = API.get_repo_name_gui()
        API.cli_gui(git.commit_file, (name, API.commit_file_gui()))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def diff():
        branch = API.diff_gui()
        API.cli_gui(git.diff_file, (API.get_repo_name_gui(), branch))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def remove_the_staging():
        global git
        dic = file_list
        if not dic:
            dic = "."
        API.cli_gui(git.reset_file, (API.get_repo_name_gui(), dic))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def add():
        dic = file_list
        if not dic:
            dic = "."  # 查一下取消的dic
        API.cli_gui(git.add_file, (API.get_repo_name_gui(), dic))
        API.update_git_file_last_gui()

    @staticmethod
    @exception_catch()
    def get_file_box_index():
        return file_box.curselection()

    @staticmethod
    @exception_catch()
    def del_file():
        try:
            del file_list[API.get_file_box_index()]
            API.update_file_box_gui()
        finally:
            pass

    @staticmethod
    @exception_catch()
    def clean_file():
        global file_list
        file_list = []
        API.update_file_box_gui()

    @staticmethod
    @exception_catch()
    def repo_init():  # 创建仓库
        global git
        new_dir = API.repo_init_gui()
        git.open_repo(new_dir)
        API.update_repo_box_gui()


def git_main():
    global SCREEN, git, PATH, bg_color, buttom_color, word_color, repo_list, last_name, file_list, FONT
    SCREEN.mainloop()


file_list = []
PATH = os.getcwd()
git = controller.GitCtrol()
repo_list = []
SCREEN = tkinter.Tk()
last_name = None
bg_color = "#FFFAFA"  # 主颜色
buttom_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
SCREEN["bg"] = bg_color
FONT = ("黑体", 11)  # 设置字体
SCREEN.title("CoTan仓库管理器")
SCREEN.resizable(width=False, height=False)
SCREEN.geometry("+10+10")  # 设置所在位置

gui_width = 13  # 标准宽度
gui_height = 2
row = 0
column = 0

tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="克隆仓库",
    command=API.clone_git,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="打开仓库",
    command=API.repo_init,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="查看文件",
    command=API.update_git_file_select_gui,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="克隆URL:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
clone_repo = tkinter.Entry(SCREEN, width=gui_width * 2)
clone_repo.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
repo_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 4)
repo_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 4
tkinter.Label(
    SCREEN,
    text="【仓库文件列表】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column,
    columnspan=3,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)  # 设置说明

row += 1
repo_dir = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 4)
repo_dir.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 4
tkinter.Label(
    SCREEN,
    text="【添加文件列表】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column,
    columnspan=3,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)  # 设置说明

row += 1
file_dir = tkinter.Entry(SCREEN, width=gui_width * 2)
file_dir.grid(
    column=column,
    row=row,
    columnspan=3,
    sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="填充路径并添加",
    command=API.add_file_by_git_gui,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="直接添加",
    command=API.add_file_input_dir_gui,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="选择文件",
    command=API.add_file_list_gui,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="把文件移除出列表",
    command=API.del_file,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="清空列表",
    command=API.clean_file,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
file_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 4)
file_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)

row += 4
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="添加暂存区文件",
    command=API.add,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="移除暂存区文件",
    command=API.remove_the_staging,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="提交到git",
    command=API.commit_file,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="查看执行日志",
    command=lambda: API.not_parameters_call(git.do_log),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="查看文件日志",
    command=API.log,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="查看状态",
    command=lambda: API.not_parameters_call(git.status),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
log_type = []
lable = ["显示轴", "commit完全显示", "简化显示"]  # 复选框
for i in range(3):
    log_type.append(tkinter.IntVar())
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=log_type[-1],
    ).grid(column=column + i, row=row, sticky=tkinter.W)
    log_type[-1].set(1)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="版本回退",
    command=API.reset_head,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="放弃修改",
    command=API.checkout_file,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除文件",
    command=API.remove_file,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
reset_type = tkinter.IntVar()  # 正，负，0
lable = ["回退到工作区", "回退到暂存区", "无痕回退"]  # 复选框
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
        value=i,
    ).grid(column=column + i, row=row, sticky=tkinter.W)

column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=row
)  # 设置说明
column += 1
row = 0

tkinter.Label(
    SCREEN,
    text="【参数操作】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column,
    columnspan=3,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)  # 设置说明

row += 1
tkinter.Label(
    SCREEN,
    text="提交描述:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
commit_message = tkinter.Entry(SCREEN, width=gui_width * 2)
commit_message.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="diff分支:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
master = tkinter.Entry(SCREEN, width=gui_width * 2)
master.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="回退版本号:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
head = tkinter.Entry(SCREEN, width=gui_width * 2)
head.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="本地分支:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
branch_name = tkinter.Entry(SCREEN, width=gui_width * 2)
branch_name.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="远程分支:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
origin_branch = tkinter.Entry(SCREEN, width=gui_width * 2)
origin_branch.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="远程仓库链接:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
remote_ssh = tkinter.Entry(SCREEN, width=gui_width)
remote_ssh.grid(column=column + 1, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="远程仓库名:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
remote_name = tkinter.Entry(SCREEN, width=gui_width)
remote_name.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="commit:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
commit = tkinter.Entry(SCREEN, width=gui_width)
commit.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="标签名字:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
tag_name = tkinter.Entry(SCREEN, width=gui_width)
tag_name.grid(column=column + 1, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="查询关键字:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
show_search_key = tkinter.Entry(SCREEN, width=gui_width)
show_search_key.grid(
    column=column + 1, columnspan=2, row=row, sticky=tkinter.E + tkinter.W
)

row += 1
tkinter.Label(
    SCREEN,
    text="工作区序号:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
stash_name = tkinter.Entry(SCREEN, width=gui_width)
stash_name.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Label(
    SCREEN,
    text="【高级操作】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width * 3,
    height=gui_height,
).grid(
    column=column,
    columnspan=3,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)  # 设置说明

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="查看分支",
    command=lambda: API.not_parameters_call(git.branch_view),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="新建分支",
    command=API.add_new_branch,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="切换分支",
    command=API.switch_branch,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除分支",
    command=lambda: API.del_branch(1),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="丢弃分支",
    command=lambda: API.del_branch(0),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="合并分支",
    command=API.switch_branch,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

no_fast_forward = tkinter.IntVar()
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="合并分支",
    command=API.branch_merge,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="退出冲突处理",
    command=lambda: API.not_parameters_call(git.merge_abort),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="使用快速合并",
    variable=no_fast_forward,
).grid(column=column + 1, row=row, sticky=tkinter.W)
no_fast_forward.set(0)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="连接远程仓库",
    command=API.add_remote,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="推送到远程仓库",
    command=lambda: API.pull_push_remote(1),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="从远程仓库抓取",
    command=lambda: API.pull_push_remote(0),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

push_bind = tkinter.IntVar()
allow_history = tkinter.IntVar()
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="分支绑定",
    command=API.bind_remote_branch,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="无视历史记录",
    variable=allow_history,
).grid(column=column + 1, row=row, sticky=tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="推送时绑定",
    variable=push_bind,
).grid(column=column + 2, row=row, sticky=tkinter.W)
allow_history.set(0)
push_bind.set(0)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="应用标签",
    command=API.add_tag,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="查看已有标签",
    command=lambda: API.show_tag(1),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="查询commit记录",
    command=lambda: API.show_tag(0),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="推送标签",
    command=API.push_tag,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="推送所有标签",
    command=API.push_all_tag,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除本地标签",
    command=API.del_tag,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除远程标签",
    command=API.del_remote_tag,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除远程分支",
    command=API.del_remote_branch,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="刷新远程分支",
    command=API.fetch_remote,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="commit补丁",
    command=API.cherry_pick,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除远程仓库",
    command=API.del_remote,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="工作区列表",
    command=lambda: API.not_parameters_call(git.stash_list),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="文件回退",
    command=API.reset_file,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="分支重命名",
    command=API.branch_new,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
branch_new_name = tkinter.Entry(SCREEN, width=gui_width)
branch_new_name.grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="保存工作区",
    command=lambda: API.not_parameters_call(git.save_stash),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="恢复工作区",
    command=lambda: API.open_stash(1),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="删除工作区",
    command=lambda: API.open_stash(0),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)

row += 1
threaded_refresh = tkinter.IntVar()
asynchronous_display = tkinter.IntVar()
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="多进程刷新",
    variable=threaded_refresh,
).grid(column=0, row=row, sticky=tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="异步显示",
    variable=asynchronous_display,
).grid(column=1, row=row, sticky=tkinter.W)
customize_input = tkinter.Entry(SCREEN, width=gui_width * 3)
customize_input.grid(
    column=2,
    row=row,
    columnspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,
)

tkinter.Button(
    SCREEN,
    bg=buttom_color,
    fg=word_color,
    text="执行操作",
    command=API.customize,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
threaded_refresh.set(0)
asynchronous_display.set(1)
tag_message = commit_message
tag_commit = commit
remote_branch = origin_branch
local_branch = branch_name
