import tkinter
from newtkinter import askopenfilename
from tkinter.messagebox import showwarning, askokcancel, showinfo
from tkinter.scrolledtext import ScrolledText
import webbrowser
import os

from system.controller import Systemctl, NamingError, ConflictError
from system import QueueController

queue_controller = QueueController()
SCREEN = tkinter.Tk()
systemctl = Systemctl()
SCREEN.title("系统管理")
SCREEN.resizable(width=False, height=False)
SCREEN.geometry(f"+10+10")
SCREEN.iconbitmap(bitmap=f'Pic{os.sep}favicon.ico', default=f'Pic{os.sep}favicon.ico')
bg_color = "#FFFAFA"  # 主颜色
SCREEN["bg"] = bg_color
botton_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
FONT = ("黑体", 11)  # 设置字体
gui_width = 13  # 标准宽度
gui_height = 2
row = 0
column = 0


def code_window(name):
    global bg_color
    cli_screen = tkinter.Toplevel(bg=bg_color)
    cli_screen.title(f"插件查看器:{name}")
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
    cli_screen.update()
    return text, cli_screen


def get_dir():
    plugin_dir_box.delete(0, tkinter.END)
    plugin_dir_box.insert(0, *systemctl.get_dir())


def get_all_plugin():
    plugin_box.delete(0, tkinter.END)
    plugin_box.insert(0, *systemctl.get_all_plugin())


def get_plugin():
    try:
        index = plugin_dir_box.curselection()[0]
    except IndexError:
        return False
    plugin_box.delete(0, tkinter.END)
    plugin_box.insert(0, *systemctl.get_plugin(index))


def add_plugin():
    index = plugin_dir_box.curselection()[0]
    plugin_dir = askopenfilename(title="选择插件文件", filetypes=[("Python", ".py")])
    try:
        plugin_list = systemctl.add_plugin(index, plugin_dir)
    except NamingError:
        showwarning("文件错误", "插件命名错误，命名规则:\ntemplate_[类\\方法名].py")
    except ConflictError:
        if askokcancel("提示", f"已经存在插件，是否需要尝试合并插件?\n[合并失败将产生不可逆的后果]"):
            systemctl.merge_plugin(index, plugin_dir)
    except BaseException as e:
        showwarning("文件错误", f"插件导入遇到了未知错误:\n{e}")
    else:
        plugin_box.delete(0, tkinter.END)
        plugin_box.insert(0, *plugin_list)


def del_plugin():
    index = plugin_box.curselection()[0]
    try:
        plugin_list = systemctl.del_plugin(index)
        plugin_box.delete(0, tkinter.END)
        plugin_box.insert(0, *plugin_list)
    finally:
        pass


def show_plugin():
    index = plugin_box.curselection()[0]
    try:
        code, name = systemctl.show_plugin(index)
        code_window(name)[0].insert(tkinter.END, code)
    finally:
        pass


def show_log():
    try:
        log = systemctl.show_log()
        code_window('日志信息')[0].insert(tkinter.END, log)
    finally:
        pass


def system_main(in_queue, out_queue):
    global SCREEN
    queue_controller.set_queue(in_queue, out_queue)
    queue_controller()
    SCREEN.mainloop()
    queue_controller.stop_process()


def show_about():
    showinfo("关于", '''
关于CoTan:
CoTan是由SuperHuan于2020年开始开发的开源科学计算系统。
关于CoTan的更多信息请访问CoTan社区
''')


(
    tkinter.Label(
        SCREEN,
        text="【插件管理】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(column=column, row=row, columnspan=3)
)
row += 1
(
    tkinter.Button(
        SCREEN,
        bg=botton_color,
        fg=word_color,
        command=get_dir,
        text="查看插件列表",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
)
(
    tkinter.Button(
        SCREEN,
        bg=botton_color,
        fg=word_color,
        command=get_all_plugin,
        text="查看所有插件",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
)
(
    tkinter.Button(
        SCREEN,
        bg=botton_color,
        fg=word_color,
        command=get_plugin,
        text="查看仓库插件",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
)
row += 1
plugin_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 5)
plugin_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=5,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 5
(
    tkinter.Label(
        SCREEN,
        text="【插件仓库】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(column=column, row=row, columnspan=3)
)
row += 1
plugin_dir_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 5)
plugin_dir_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=5,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 5
(
    tkinter.Button(
        SCREEN,
        bg=botton_color,
        fg=word_color,
        command=add_plugin,
        text="新增插件",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
)
(
    tkinter.Button(
        SCREEN,
        bg=botton_color,
        fg=word_color,
        command=del_plugin,
        text="删除插件",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
)
(
    tkinter.Button(
        SCREEN,
        bg=botton_color,
        fg=word_color,
        command=show_plugin,
        text="查看插件",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
)
(
    tkinter.Label(
        SCREEN,
        text="【日志管理】",
        bg=bg_color,
        fg=word_color,
        font=FONT,
        width=gui_width * 3,
        height=gui_height,
    ).grid(column=column, row=row, columnspan=3)
)
row += 1
(
    tkinter.Button(
        SCREEN,
        bg=botton_color,
        fg=word_color,
        command=lambda: webbrowser.open(r'E:\SongZihuan\PyProject\CoTan\Log\log_system.log'),
        text="查看日志",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
)
(
    tkinter.Button(
        SCREEN,
        bg=botton_color,
        fg=word_color,
        command=show_about,
        text="关于CoTan",
        font=FONT,
        width=gui_width,
        height=gui_height,
    ).grid(column=column+2, row=row, sticky=tkinter.E + tkinter.W)
)
