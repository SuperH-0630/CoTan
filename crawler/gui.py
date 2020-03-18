import os
import re
import tkinter
import threading

import crawler.controller
import crawler.template
from newtkinter import askdirectory
from system import exception_catch

SCREEN = tkinter.Tk()
database_list = []
attributes_dict = {}
PATH = os.getcwd()
cookies_list = []
bg_color = "#FFFAFA"  # 主颜色
buttom_bg_color = "#FFFAFA"  # 按钮颜色
word_color = "#000000"  # 文字颜色
SCREEN["bg"] = bg_color
FONT = ("黑体", 11)  # 设置字体
start_loader_stop = False
user_agent_input = None
requests_data = None
mode_input = None
time_out = None
applied_cookies = None
url_box = None
filter_func_box = None
cookies_fixed = None
cookies_BOX = None
new_cookies = None
search_all = None
search_key = None
parser_func_box = None
operation_object = None
object_index = None
send_text = None
password = None
select_object = None
wait_time = None
js_code = None
now_running = None
status_output = None
variable_box = None
cookies_name_input = None
element_name = None
attributes_name = None
attribute_regex = None
attributes_value = None
attributes_box = None
find_text = None
is_recursive = None
text_regex = None
limit = None
find_path = None
data_format = None
database_name = None
database_box = None
url_tag = None
chains = None
drag_element = None
drag_element_index = None
type_value = None
run_time = None
is_special_keys = None
save_dir = None
url = None
loader = None
page_parser = None
database = None


class UIAPI:
    @staticmethod
    @exception_catch()
    def get_db_index_gui():
        try:
            index = eval(object_index.get(), {})
        except BaseException:
            index = slice(None, None)
        return index

    @staticmethod
    @exception_catch()
    def get_datadase_name_gui():
        global database_box, database_list
        try:
            return database_list[database_box.curselection()[0]]
        except IndexError:
            try:
                return database_list[0]
            except IndexError:
                return None

    @staticmethod
    @exception_catch()
    def update_database_box_gui():
        global database_box, database_list
        database_list = database.return_database()
        database_box.delete(0, tkinter.END)
        database_box.insert(tkinter.END, *database_list)

    @staticmethod
    @exception_catch()
    def update_run_status_gui(now_func, status, value_box):
        global now_running, status_output, variable_box
        now_running.set(now_func)
        status_output.set(status)
        variable_box.delete(0, tkinter.END)
        variable_box.insert(0, *value_box)

    @staticmethod
    @exception_catch()
    def get_attributes_box_index_gui():
        return attributes_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def add_attributes_gui():
        name = attributes_name.get()
        value = attributes_value.get()
        if name == "" or value == "":
            raise Exception
        value = re.compile(value) if bool(attribute_regex.get()) else value
        return name, value

    @staticmethod
    @exception_catch()
    def update_attributes_box_gui():
        global attributes_box, attributes_dict
        show = []
        for i in attributes_dict:
            show.append(f"{i} -> {attributes_dict[i]}")
        attributes_box.delete(0, tkinter.END)
        attributes_box.insert(tkinter.END, *show)

    @staticmethod
    @exception_catch()
    def third_func_args_gui():  # 方法args统一转换(第三栏目)
        global is_special_keys, chains, drag_element, drag_element_index, run_time, operation_object, object_index
        global type_value
        try:
            index = int(object_index.get())
        except ValueError:
            index = 0
        try:
            index2 = int(drag_element_index.get())
        except ValueError:
            index2 = 0
        try:
            time = int(run_time.get())
        except ValueError:
            time = 1
        return dict(
            Chains=chains.get(),
            element_value=operation_object.get(),
            index=index,
            element_value2=drag_element.get(),
            index2=index2,
            run_time=time,
            is_special_keys=bool(is_special_keys.get()),
            key=type_value.get(),
        )

    @staticmethod
    @exception_catch()
    def second_func_args_gui():  # 方法args统一转换(第二栏目)
        global cookies_name_input, new_cookies, element_name, attributes_dict, operation_object, object_index
        global find_text, text_regex, limit, is_recursive, find_path
        try:
            index = eval(object_index.get(), {})
        except BaseException:
            index = slice(None, None)
        try:
            cookies = eval(new_cookies.get(), {})
        except BaseException:
            cookies = {}
        return dict(
            element_value=operation_object.get(),
            index=index,
            cookies_name=cookies_name_input.get(),
            cookies=cookies,
            tag=element_name.get().split(","),
            attribute=attributes_dict,
            text=re.compile(find_text.get()) if bool(text_regex.get()) else find_text.get(),
            limit=limit.get(),
            recursive=bool(is_recursive.get()),
            path=find_path.get(),
        )

    @staticmethod
    @exception_catch()
    def first_func_args_gui():  # 方法args统一转换(不支持Frame)
        global operation_object, object_index, send_text, password, select_object, js_code, wait_time
        try:
            time = int(wait_time.get())
        except ValueError:
            time = 2
        try:
            index = int(object_index.get())
        except ValueError:
            index = 0
        return dict(
            element_value=operation_object.get(),
            index=index,
            text=send_text.get(),
            User=password.get(),
            Passwd=password.get(),
            deselect=select_object.get(),
            JS=js_code.get(),
            time=time,
        )

    @staticmethod
    @exception_catch()
    def get_parser_func_box_index_gui():
        return parser_func_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def update_parser_func_box_gui():
        global parser_func_box, page_parser
        parser_func_box.delete(0, tkinter.END)
        parser_func_box.insert(tkinter.END, *page_parser.return_func(False)[::-1])

    @staticmethod
    @exception_catch()
    def get_new_cookies_gui():
        return eval(new_cookies.get(), {})

    @staticmethod
    @exception_catch()
    def get_cookies_fix_gui():
        return bool(cookies_fixed.get())

    @staticmethod
    @exception_catch()
    def get_cookies_box_index_gui():
        return cookies_BOX.curselection()[0]

    @staticmethod
    @exception_catch()
    def update_cookies_box_gui(cookies):
        global cookies_BOX, cookies_list
        if API.get_cookies_fix_gui():
            cookies_list = cookies
            cookies_BOX.delete(0, tkinter.END)
            cookies_BOX.insert(0, *cookies)

    @staticmethod
    @exception_catch()
    def get_filter_func_box_index_gui():
        return filter_func_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def update_filter_func_box_gui():
        global url, filter_func_box
        filter_func_box.delete(0, tkinter.END)
        filter_func_box.insert(tkinter.END, *url.return_filter_func())

    @staticmethod
    @exception_catch()
    def get_url_box_index_gui():
        return url_box.curselection()[0]

    @staticmethod
    @exception_catch()
    def get_url_parameter_gui():
        try:
            data = eval(requests_data.get(), {})
        except BaseException:
            data = {}
        try:
            the_time_out = int(time_out.get())
        except ValueError:
            the_time_out = 5
        return_ = dict(
            func=mode_input.get(),
            UA=user_agent_input.get(),
            cookies=applied_cookies.get(),
            data=data,
            time_out=the_time_out,
        )
        name = ["no_js", "no_java", "no_plugins", "first_run", "head", "no_img", "new"]
        for i in range(len(name)):
            return_[name[i]] = bool(url_parameter[i].get())
        return return_

    @staticmethod
    @exception_catch()
    def get_new_url_name_gui():
        return url_input.get()

    @staticmethod
    @exception_catch()
    def add_url_from_tag_gui():
        try:
            index = eval(object_index.get(), {})
        except BaseException:
            index = slice(None, None)
        return dict(
            element_value=operation_object.get(),
            index=index,
            url_name=url_tag.get(),
            update_func=API.update_url_box_gui,
            url_args=API.get_url_parameter_gui(),
        )

    @staticmethod
    @exception_catch()
    def update_url_box_gui():
        global url, url_box
        url_box.delete(0, tkinter.END)
        url_box.insert(tkinter.END, *url.return_url())

    @staticmethod
    @exception_catch()
    def to_database_gui():
        index = API.get_db_index_gui()
        return dict(element_value=operation_object.get(),
                    index=index,
                    data=data_format.get(),
                    dataBase_name=API.get_datadase_name_gui(),)


class API(UIAPI):
    @staticmethod
    @exception_catch()
    def to_database(is_tag=True):
        global object_index, operation_object, data_format, page_parser
        if is_tag:
            func = page_parser.to_database
        else:
            func = page_parser.to_database_by_re
        func(**API.to_database_gui())
        API.update_parser_func_box_gui()

    @staticmethod
    @exception_catch()
    def close():
        name = API.get_datadase_name_gui()
        database.close(name)
        API.update_database_box_gui()

    @staticmethod
    @exception_catch()
    def out():
        name = API.get_datadase_name_gui()
        database.out(name, save_dir)
        API.update_database_box_gui()

    @staticmethod
    @exception_catch()
    def remove_database():
        name = API.get_datadase_name_gui()
        database.rm_database(name)
        API.update_database_box_gui()

    @staticmethod
    @exception_catch()
    def add_database():
        name = database_name.get()
        database.add_database(name)
        API.update_database_box_gui()

    @staticmethod
    @exception_catch()
    def clean_attributes():
        global attributes_dict
        attributes_dict = {}
        API.update_attributes_box_gui()

    @staticmethod
    @exception_catch()
    def del_attributes():
        del attributes_dict[list(attributes_dict.keys())[API.get_attributes_box_index_gui()]]
        API.update_attributes_box_gui()

    @staticmethod
    @exception_catch()
    def add_attributes():
        try:
            name, value = API.add_attributes_gui()
        except BaseException:
            raise
        attributes_dict[name] = value
        API.update_attributes_box_gui()

    @staticmethod
    @exception_catch()
    def third_add_action_func(func):
        args = API.third_func_args_gui()
        func = {
            "make_ActionChains": page_parser.make_action_chains,
            "click": page_parser.action_click,
            "double_click": page_parser.action_double_click,
            "click_right": page_parser.action_click_right,
            "click_and_hold": page_parser.action_click_and_hold,
            "release": page_parser.action_release,
            "drag_and_drop": page_parser.action_drag_and_drop,
            "move": page_parser.action_move,
            "key_down": page_parser.action_key_down,
            "key_up": page_parser.action_key_up,
            "send_keys_to_element": page_parser.action_send_keys_to_element,
            "send_keys": page_parser.action_send_keys,
            "ActionChains_run": page_parser.action_run,
        }.get(func, page_parser.make_action_chains)
        func(**args)
        API.update_parser_func_box_gui()

    @staticmethod
    @exception_catch()
    def second_add_action_func(func):
        args = API.second_func_args_gui()
        func = {
            "del_all_cookies": page_parser.del_all_cookies,
            "del_cookies": page_parser.del_cookies,
            "add_cookies": page_parser.add_cookies,
            "update_cookies": page_parser.update_cookies,
            "get_cookies": page_parser.get_cookies,
            "get_all_cookies": page_parser.get_all_cookies,
            "make_bs": page_parser.make_bs,
            "findAll": page_parser.findall,
            "findAll_by_text": page_parser.findall_by_text,
            "get_children": page_parser.get_children,
            "get_offspring": page_parser.get_offspring,
            "get_up": page_parser.get_up,
            "get_down": page_parser.get_down,
            "get_by_path": page_parser.get_by_path,
            "brothers": page_parser.get_brothers,
            "png": page_parser.webpage_snapshot,
            "to_json": page_parser.to_json,
        }.get(func, page_parser.make_bs)
        func(**args)
        API.update_parser_func_box_gui()

    @staticmethod
    @exception_catch()
    def first_add_action_func(func):
        args = API.first_func_args_gui()
        func = {
            "send_keys": page_parser.send_keys,
            "clear": page_parser.clear,
            "click": page_parser.click,
            "User_Passwd": page_parser.authentication,
            "accept": page_parser.accept,
            "dismiss": page_parser.dismiss,
            "submit": page_parser.submit,
            "deselect_by_index": page_parser.deselect_by_index,
            "deselect_by_value": page_parser.deselect_by_value,
            "deselect_by_text": page_parser.deselect_by_text,
            "select_by_index": page_parser.select_by_index,
            "select_by_value": page_parser.select_by_value,
            "select_by_text": page_parser.select_by_text,
            "back": page_parser.back,
            "forward": page_parser.forward,
            "refresh": page_parser.refresh,
            "wait_sleep": page_parser.wait_sleep,
            "set_wait": page_parser.set_wait,
            "run_JS": page_parser.run_js,
            "out": page_parser.out_html,
            "get_Page": page_parser.to_text,
            "get_all_windows": page_parser.get_all_windows,
            "get_now_windows": page_parser.get_now_windows,
            "switch_to_windwos": page_parser.switch_to_windwos,
        }.get(func, page_parser.send_keys)
        func(**args)
        API.update_parser_func_box_gui()

    @staticmethod
    @exception_catch()
    def add_frame_func_father(is_main=True):
        search = None if is_main else ""
        page_parser.find_switch_to_frame(search, True)
        API.update_parser_func_box_gui()

    @staticmethod
    @exception_catch()
    def add_frame_func_id():
        search = API.get_search_key()
        page_parser.find_switch_to_frame(search, True)
        API.update_parser_func_box_gui()

    @staticmethod
    @exception_catch()
    def add_find_func(func):
        not_all = not (bool(search_all.get()))
        search = API.get_search_key()
        func = {
            "id": page_parser.find_id,
            "name": page_parser.find_name,
            "class": page_parser.find_class,
            "xpath": page_parser.find_xpath,
            "css": page_parser.find_css,
            "tag": page_parser.find_tag_name,
            "link": page_parser.find_link_text,
            "partial_link": page_parser.find_partial_link_text,
            "alert": page_parser.find_switch_to_alert,
            "active_element": page_parser.find_switch_to_active_element,
            "frame": page_parser.find_switch_to_frame,
        }.get(func, page_parser.find_id)
        func(search, not_all=not_all)
        API.update_parser_func_box_gui()

    @staticmethod
    @exception_catch()
    def get_search_key():
        search = search_key.get()
        return search

    @staticmethod
    @exception_catch()
    def del_parser_func():
        try:
            index = API.get_parser_func_box_index_gui()
            page_parser.del_func(index, True)
            API.update_parser_func_box_gui()
        except BaseException:
            raise

    @staticmethod
    @exception_catch()
    def clean_parser_func():
        try:
            page_parser.tra_func()
            API.update_parser_func_box_gui()
        except BaseException:
            raise

    @staticmethod
    @exception_catch()
    def update_cookies():
        cookies = API.get_new_cookies_gui()
        if API.get_cookies_fix_gui():
            return False
        try:
            name = cookies_list[API.get_cookies_box_index_gui()].get("name")
            loader.monitoring_update_cookies(name, cookies)
            API.set_cookies_fix()
        except BaseException:
            raise

    @staticmethod
    @exception_catch()
    def add_cookies():
        cookies = API.get_new_cookies_gui()
        if API.get_cookies_fix_gui():
            return False
        try:
            loader.monitoring_add_cookies(cookies)
            API.set_cookies_fix()
        except BaseException:
            raise

    @staticmethod
    @exception_catch()
    def clean_cookies():
        if API.get_cookies_fix_gui():
            return False
        try:
            loader.monitoring_clear_cookier()
            API.set_cookies_fix()
        except BaseException:
            raise

    @staticmethod
    @exception_catch()
    def set_cookies_fix(fix=0):
        cookies_fixed.set(fix)

    @staticmethod
    @exception_catch()
    def del_cookies():
        if API.get_cookies_fix_gui():
            return False
        try:
            name = cookies_list[API.get_cookies_box_index_gui()].get("name")
            loader.monitoring_del_cookies(name)
            API.set_cookies_fix()
        except BaseException:
            raise

    @staticmethod
    @exception_catch()
    def crawler_stop():
        global start_loader_stop
        start_loader_stop = False
        loader.stop()

    @staticmethod
    @exception_catch()
    def crawler_run():
        def start_loader():
            global start_loader_stop
            start_loader_stop = True
            loader.stop()  # 把之前的停止
            while start_loader_stop:
                if url.is_finish():
                    API.update_run_status_gui('暂无URL', 'No status', [])
                    break
                API.update_run_status_gui('呼叫浏览器...', 'No status', [])
                loader.start_to_run(func_cookie=API.update_cookies_box_gui)
                API.update_url_box_gui()
                page_parser.element_interaction(API.update_run_status_gui)
            loader.stop()

        new = threading.Thread(target=start_loader)
        new.start()
        API.update_url_box_gui()

    @staticmethod
    @exception_catch()
    def crawler_run_one():
        def start_loader():
            global loader, page_parser
            if url.is_finish():
                return
            loader.start_to_run(func_cookie=API.update_cookies_box_gui)
            API.update_url_box_gui()
            page_parser.element_interaction(API.update_run_status_gui)
            loader.stop()

        new = threading.Thread(target=start_loader)
        new.start()

    @staticmethod
    @exception_catch()
    def add_filter_func_https():
        url.add_filter_func(lambda the_url: re.match(re.compile("^https://"), the_url), "HTTPS过滤")
        API.update_filter_func_box_gui()

    @staticmethod
    @exception_catch()
    def add_filter_func_www():
        url.add_filter_func(lambda the_url: re.match(re.compile(r".*www\."), the_url), "www过滤")
        API.update_filter_func_box_gui()

    @staticmethod
    @exception_catch()
    def del_filter_func():
        index = API.get_filter_func_box_index_gui()
        url.del_filter_func(index)
        API.update_filter_func_box_gui()

    @staticmethod
    @exception_catch()
    def del_url():
        index = API.get_url_box_index_gui()
        url.del_url(index)
        API.update_url_box_gui()

    @staticmethod
    @exception_catch()
    def add_url():
        args = API.get_url_parameter_gui()
        new_url = API.get_new_url_name_gui()
        if new_url == "":
            return
        url.add_url(new_url, **args)
        API.update_url_box_gui()

    @staticmethod
    @exception_catch()
    def add_url_from_tag():
        page_parser.add_url(**API.add_url_from_tag_gui())
        API.update_parser_func_box_gui()


def crawler_main():
    global SCREEN
    SCREEN.mainloop()
    loader.stop()
    database.close_all()
    url.close()
    loader.close()


SCREEN.title("CoTan自动化网页")
SCREEN.resizable(width=False, height=False)
SCREEN.geometry("+10+10")  # 设置所在位置
gui_width = 13  # 标准宽度
gui_height = 2
row = 0
column = 0
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="添加url对象",
    command=API.add_url,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除url对象",
    command=API.del_url,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="应用过滤机制",
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="添加url:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
url_input = tkinter.Entry(SCREEN, width=gui_width * 2)
url_input.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
url_parameter = []
lable = ["不加载js", "不加载java", "不加载插件"]  # 复选框
for i in range(3):
    url_parameter.append(tkinter.IntVar())
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=url_parameter[-1],
    ).grid(column=column + i, row=row, sticky=tkinter.W)
row += 1
lable = ["第一次启动", "隐藏网页", "不加载图片"]  # 复选框
for i in range(3):
    url_parameter.append(tkinter.IntVar())
    tkinter.Checkbutton(
        SCREEN,
        bg=bg_color,
        fg=word_color,
        activebackground=bg_color,
        activeforeground=word_color,
        selectcolor=bg_color,
        text=lable[i],
        variable=url_parameter[-1],
    ).grid(column=column + i, row=row, sticky=tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="UA设置:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
user_agent_input = tkinter.Entry(SCREEN, width=gui_width * 2)
user_agent_input.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="DATA:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
requests_data = tkinter.Entry(SCREEN, width=gui_width * 2)
requests_data.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="请求方式:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
mode_input = tkinter.Entry(SCREEN, width=gui_width * 2)
mode_input.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="请求超时:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
time_out = tkinter.Entry(SCREEN, width=gui_width * 2)
time_out.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="Cookies:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
applied_cookies = tkinter.Entry(SCREEN, width=gui_width)
applied_cookies.grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
url_parameter.append(tkinter.IntVar())
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="新启动网页",
    variable=url_parameter[-1],
).grid(column=column + 2, row=row, sticky=tkinter.W)
row += 1
url_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 4)
url_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=4,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 4
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="HTTPS过滤器",
    command=API.add_filter_func_https,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="WWW过滤器",
    command=API.add_filter_func_www,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除过滤器",
    command=API.del_filter_func,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="自定义过滤器",
    command=API.add_filter_func_https,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="清空过滤器",
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
filter_func_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 3)
filter_func_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=3,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 3
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="单点爬虫运行",
    command=API.crawler_run_one,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="爬虫运行",
    command=API.crawler_run,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="单点爬虫停止",
    command=API.crawler_stop,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
cookies_fixed = tkinter.IntVar()
tkinter.Label(
    SCREEN,
    text="【曲奇监视】",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(
    column=column + 1,
    row=row,
    sticky=tkinter.E + tkinter.W + tkinter.W + tkinter.S + tkinter.N,
)  # 设置说明
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="固定曲奇",
    variable=cookies_fixed,
).grid(column=column + 2, row=row, sticky=tkinter.W)
cookies_fixed.set("0")
row += 1
cookies_BOX = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 3)
cookies_BOX.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=3,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 3
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="清空曲奇",
    command=API.clean_cookies,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="更新曲奇",
    command=API.update_cookies,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除曲奇",
    command=API.del_cookies,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
new_cookies = tkinter.Entry(SCREEN, width=gui_width * 3)
new_cookies.grid(column=column, row=row, columnspan=3, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="添加曲奇",
    command=API.add_cookies,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=row
)  # 设置说明
column += 1
row = 0
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据id搜查",
    command=lambda: API.add_find_func("id"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据name搜查",
    command=lambda: API.add_find_func("name"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据class搜查",
    command=lambda: API.add_find_func("class"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据xpath搜查",
    command=lambda: API.add_find_func("xpath"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据css搜查",
    command=lambda: API.add_find_func("css"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据元素名搜查",
    command=lambda: API.add_find_func("tag"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
search_all = tkinter.Variable()
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据link搜查",
    command=lambda: API.add_find_func("link"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="link模糊搜查",
    command=lambda: API.add_find_func("partial_link"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="匹配全部",
    variable=search_all,
).grid(column=column + 2, row=row, sticky=tkinter.W)
search_all.set("0")
row += 1
tkinter.Label(
    SCREEN,
    text="搜查参数:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
search_key = tkinter.Entry(SCREEN, width=gui_width * 2)
search_key.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除方法",
    command=API.del_parser_func,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="清空方法",
    command=API.clean_parser_func,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
parser_func_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 5)
parser_func_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=5,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 5
tkinter.Label(
    SCREEN,
    text="操作元素:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
operation_object = tkinter.Entry(SCREEN, width=gui_width * 2)
operation_object.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="操作索引:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
object_index = tkinter.Entry(SCREEN, width=gui_width * 2)
object_index.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="发送信息:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
send_text = tkinter.Entry(SCREEN, width=gui_width * 2)
send_text.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="认证用户名:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
username_input = tkinter.Entry(SCREEN, width=gui_width * 2)
username_input.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="认证密码:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
password = tkinter.Entry(SCREEN, width=gui_width * 2)
password.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="选择参数:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
select_object = tkinter.Entry(SCREEN, width=gui_width * 2)
select_object.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="等待时间:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
wait_time = tkinter.Entry(SCREEN, width=gui_width * 2)
wait_time.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="JavaScript:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
js_code = tkinter.Entry(SCREEN, width=gui_width * 2)
js_code.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="发送字符",
    command=lambda: API.first_add_action_func("send_keys"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="清空字符",
    command=lambda: API.first_add_action_func("clear"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="提交表单",
    command=lambda: API.first_add_action_func("submit"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="点击按钮",
    command=lambda: API.first_add_action_func("click"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="取得源代码",
    command=lambda: API.first_add_action_func("get_Page"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="输出HTML",
    command=lambda: API.first_add_action_func("out"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="切换Frame(id)",
    command=API.add_frame_func_id,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="切换Frame",
    command=lambda: API.add_find_func("frame"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="定位焦点元素",
    command=lambda: API.add_find_func("active_element"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="捕获弹窗",
    command=lambda: API.add_find_func("alert"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="回到主Frame",
    command=lambda: API.add_frame_func_father(False),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="回到父Frame",
    command=lambda: API.add_frame_func_father(True),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="弹出框认证",
    command=lambda: API.first_add_action_func("User_Passwd"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="弹出框确定",
    command=lambda: API.first_add_action_func("accept"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="弹出框取消",
    command=lambda: API.first_add_action_func("dismiss"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="取消选择index",
    command=lambda: API.first_add_action_func("deselect_by_index"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="取消选择text",
    command=lambda: API.first_add_action_func("deselect_by_text"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="取消选择value",
    command=lambda: API.first_add_action_func("deselect_by_value"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="选择index",
    command=lambda: API.first_add_action_func("select_by_index"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="选择text",
    command=lambda: API.first_add_action_func("select_by_text"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="选择value",
    command=lambda: API.first_add_action_func("select_by_value"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=row
)  # 设置说明
column += 1
row = 0
now_running = tkinter.StringVar()
status_output = tkinter.StringVar()
tkinter.Label(
    SCREEN,
    text="正在执行:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
tkinter.Entry(
    SCREEN, width=gui_width * 2, state=tkinter.DISABLED, textvariable=now_running
).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="上一次状态:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
tkinter.Entry(
    SCREEN, width=gui_width * 2, state=tkinter.DISABLED, textvariable=status_output
).grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
variable_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 5)
variable_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=5,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 5
tkinter.Label(
    SCREEN,
    text="cookies名:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
cookies_name_input = tkinter.Entry(SCREEN, width=gui_width * 2)
cookies_name_input.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="cookies:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
new_cookies = tkinter.Entry(SCREEN, width=gui_width * 2)
new_cookies.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="定位标签:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
element_name = tkinter.Entry(SCREEN, width=gui_width * 2)
element_name.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="定位属性名:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
attributes_name = tkinter.Entry(SCREEN, width=gui_width * 2)
attributes_name.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
attribute_regex = tkinter.IntVar()
row += 1
tkinter.Label(
    SCREEN,
    text="定位属性值:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
attributes_value = tkinter.Entry(SCREEN, width=gui_width)
attributes_value.grid(
    column=column + 1, columnspan=2, row=row, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="添加属性",
    command=API.add_attributes,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除属性",
    command=API.del_attributes,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="清空属性",
    command=API.clean_attributes,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
attributes_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 3)
attributes_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=3,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 3
tkinter.Label(
    SCREEN,
    text="定位文本:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
find_text = tkinter.Entry(SCREEN, width=gui_width)
find_text.grid(column=column + 1, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
is_recursive = tkinter.IntVar()
text_regex = tkinter.IntVar()
row += 1
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="递归查找",
    variable=is_recursive,
).grid(column=column, row=row, sticky=tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="文本使用正则",
    variable=text_regex,
).grid(column=column + 1, row=row, sticky=tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="属性值使用正则",
    variable=attribute_regex,
).grid(column=column + 2, row=row, sticky=tkinter.W)
attribute_regex.set(1)
text_regex.set("1")
is_recursive.set("1")
row += 1
tkinter.Label(
    SCREEN,
    text="查找个数:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
limit = tkinter.Entry(SCREEN, width=gui_width * 2)
limit.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="定位路径:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
find_path = tkinter.Entry(SCREEN, width=gui_width * 2)
find_path.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除所有曲奇",
    command=lambda: API.second_add_action_func("del_all_cookies"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除指定曲奇",
    command=lambda: API.second_add_action_func("del_cookies"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="添加新的曲奇",
    command=lambda: API.second_add_action_func("add_cookies"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="更新指定曲奇",
    command=lambda: API.second_add_action_func("update_cookies"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获得所有曲奇",
    command=lambda: API.second_add_action_func("get_cookies"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获得指定曲奇",
    command=lambda: API.second_add_action_func("get_all_cookies"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="解析网页",
    command=lambda: API.second_add_action_func("make_bs"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据标签定位",
    command=lambda: API.second_add_action_func("findAll"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="根据文本定位",
    command=lambda: API.second_add_action_func("findAll_by_text"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获得子标签",
    command=lambda: API.second_add_action_func("get_children"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获得后代标签",
    command=lambda: API.second_add_action_func("get_offspring"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获得弟标签",
    command=lambda: API.second_add_action_func("get_down"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获得兄标签",
    command=lambda: API.second_add_action_func("get_up"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获得兄弟标签",
    command=lambda: API.second_add_action_func("brothers"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="路径定位",
    command=lambda: API.second_add_action_func("get_by_path"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
column += 3
tkinter.Label(SCREEN, text="", bg=bg_color, fg=word_color, font=FONT, width=1).grid(
    column=column, row=row
)  # 设置说明
column += 1
row = 0
tkinter.Label(SCREEN, text="【数据库操作】", bg=bg_color, fg=word_color, font=FONT).grid(
    column=column, row=row, columnspan=3
)  # 设置说明
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="元素式存入",
    command=lambda: API.to_database(True),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="正则式存入",
    command=lambda: API.to_database(False),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="新增数据表",
    command=API.add_database,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="删除数据表",
    command=API.remove_database,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="导出数据表",
    command=API.out,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="关闭数据表",
    command=API.close,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="数据存入格式:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
data_format = tkinter.Entry(SCREEN, width=gui_width * 2)
data_format.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="数据表名字:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
database_name = tkinter.Entry(SCREEN, width=gui_width * 2)
database_name.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
database_box = tkinter.Listbox(SCREEN, width=gui_width * 3, height=gui_height * 5)
database_box.grid(
    column=column,
    row=row,
    columnspan=3,
    rowspan=5,
    sticky=tkinter.E + tkinter.W + tkinter.S + tkinter.N,
)
row += 5
tkinter.Label(
    SCREEN,
    text="URL标签:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
url_tag = tkinter.Entry(SCREEN, width=gui_width * 2)
url_tag.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="导出页面快照",
    command=lambda: API.second_add_action_func("png"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="回调添加URL",
    command=API.add_url_from_tag,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="解析为json",
    command=lambda: API.second_add_action_func("to_json"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="操作动作链:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
chains = tkinter.Entry(SCREEN, width=gui_width * 2)
chains.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="拽拖至元素:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
drag_element = tkinter.Entry(SCREEN, width=gui_width * 2)
drag_element.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="拽拖索引:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
drag_element_index = tkinter.Entry(SCREEN, width=gui_width * 2)
drag_element_index.grid(
    column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W
)
row += 1
tkinter.Label(
    SCREEN,
    text="键入值:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
type_value = tkinter.Entry(SCREEN, width=gui_width * 2)
type_value.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Label(
    SCREEN,
    text="运行时长:",
    bg=bg_color,
    fg=word_color,
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row)
run_time = tkinter.Entry(SCREEN, width=gui_width * 2)
run_time.grid(column=column + 1, row=row, columnspan=2, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="点击左键",
    command=lambda: API.third_add_action_func("click"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="双击左键",
    command=lambda: API.third_add_action_func("double_click"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="点击右键",
    command=lambda: API.third_add_action_func("click_right"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="按住左键",
    command=lambda: API.third_add_action_func("click_and_hold"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="松开左键",
    command=lambda: API.third_add_action_func("release"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="拽托元素",
    command=lambda: API.second_add_action_func("drag_and_drop"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="移动鼠标",
    command=lambda: API.third_add_action_func("move"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="按下按键",
    command=lambda: API.third_add_action_func("key_down"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="抬起按键",
    command=lambda: API.third_add_action_func("key_up"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
is_special_keys = tkinter.IntVar()
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="发送文本到焦点",
    command=lambda: API.third_add_action_func("send_keys"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="发送文本",
    command=lambda: API.third_add_action_func("send_keys_to_element"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Checkbutton(
    SCREEN,
    bg=bg_color,
    fg=word_color,
    activebackground=bg_color,
    activeforeground=word_color,
    selectcolor=bg_color,
    text="转换为特殊按钮",
    variable=is_special_keys,
).grid(column=column + 2, row=row, sticky=tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="生成动作链",
    command=lambda: API.third_add_action_func("make_ActionChains"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="运行动作链",
    command=lambda: API.third_add_action_func("ActionChains_run"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, columnspan=2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获取当前窗口",
    command=lambda: API.first_add_action_func("get_now_windows"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="获取所有窗口",
    command=lambda: API.first_add_action_func("get_all_windows"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="切换窗口",
    command=lambda: API.first_add_action_func("switch_to_windwos"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="暴力等待",
    command=lambda: API.first_add_action_func("wait_sleep"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="元素检查等待",
    command=lambda: API.first_add_action_func("set_wait"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="运行js",
    command=lambda: API.first_add_action_func("run_JS"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
row += 1
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="页面后退",
    command=lambda: API.first_add_action_func("back"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="页面刷新",
    command=lambda: API.first_add_action_func("refresh"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 1, row=row, sticky=tkinter.E + tkinter.W)
tkinter.Button(
    SCREEN,
    bg=buttom_bg_color,
    fg=word_color,
    text="页面前进",
    command=lambda: API.first_add_action_func("forward"),
    font=FONT,
    width=gui_width,
    height=gui_height,
).grid(column=column + 2, row=row, sticky=tkinter.E + tkinter.W)
SCREEN.update()  # 要预先update一下，否则会卡住
save_dir = askdirectory(title="选择项目位置", must=True)  # 项目位置
url = crawler.controller.Url(save_dir, save_dir)  # url管理器
loader = crawler.controller.PageDownloader(url, save_dir)  # 页面下载器
page_parser = crawler.controller.PageParser(loader)  # 页面解析器
database = crawler.template.data_base  # 数据库
