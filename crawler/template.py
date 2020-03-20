import bs4
import hashlib
import os
import re as regular
import threading
import time
from abc import ABCMeta, abstractmethod
from time import sleep
import logging

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
import requests

from system import plugin_class_loading, get_path, basicConfig

logging.basicConfig(**basicConfig)

keys_name_dict = {
    "ctrl": Keys.CONTROL,
    "shift": Keys.SHIFT,
    "tab": Keys.TAB,
    "left_ctrl": Keys.LEFT_CONTROL,
    "left_shift": Keys.LEFT_SHIFT,
    "left_alt": Keys.LEFT_ALT,
    "ALT": Keys.ALT,
    "enter": Keys.ENTER,
    "return": Keys.RETURN,
    "backspace": Keys.BACKSPACE,
    "del": Keys.DELETE,
    "pgup": Keys.PAGE_UP,
    "pgdn": Keys.PAGE_DOWN,
    "home": Keys.HOME,
    "end": Keys.END,
    "esc": Keys.CANCEL,
    "insert": Keys.INSERT,
    "meta": Keys.META,
    "up": Keys.UP,
    "down": Keys.DOWN,
    "right": Keys.RIGHT,
    "left": Keys.LEFT,
}  # 键-值映射


class PageParserError(Exception):
    pass


class UrlError(Exception):
    pass


class CookiesError(Exception):
    pass


class Database(metaclass=ABCMeta):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def add_new(self, data):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def out_file(self, out_dir):
        pass


class CoTanDB(Database):
    def __init__(self, name):
        self.dir = rf"{os.getcwd()}{os.sep}Database_dir{os.sep}{name}.cotanDB"  # 创建DB文件
        self.file = open(self.dir, "r+" if os.path.exists(self.dir) else "w+")
        self.id = 0
        self.name = name
        for _ in self.file.readlines():
            self.id += 1

    def __str__(self):
        return self.name

    def close(self):
        try:
            self.file.close()
        except IOError:
            pass

    def add_new(self, data):
        data_str = str(self.id)
        for i in data:
            data_str += "," + str(i)
        data_str += "\n"
        self.file.write(data_str)
        self.file.flush()
        self.id += 1

    def remove(self):
        self.file.close()
        os.remove(self.dir)

    def out_file(self, out_dir):
        with open(out_dir + fr"{os.sep}{self.name}.contanDB", "w") as f:
            with open(self.dir) as g:
                f.write(g.read())


class DatabaseControllerBase:
    def __init__(self):
        self.database = {}


class AddDatabase(DatabaseControllerBase):
    def add_database(self, name):  # 添加数据表
        self.database[name] = CoTanDB(name)


class DatabaseControllerCustom(metaclass=ABCMeta):
    @abstractmethod
    def close(self, name):
        pass

    @abstractmethod
    def close_all(self):
        pass

    @abstractmethod
    def rm_database(self, name):
        pass

    @abstractmethod
    def out(self, name, save_dir):
        pass

    @abstractmethod
    def return_database(self):
        pass


class DatabaseController(AddDatabase, DatabaseControllerCustom):  # data base控制器

    def add_new(self, name, data):  # 添加新内容
        database = self.database.get(name)
        if database is None:
            self.add_database(name)
            database = self.database.get(name)
        database.add_new(data)

    def close(self, name):  # 关闭数据表
        try:
            self.database[name].close()
            del self.database[name]
        except IndexError:
            pass

    def close_all(self):  # 关闭所有数据表
        for i in self.database:
            self.database[i].close()
        self.database = {}

    def rm_database(self, name):  # 删除数据表
        self.database[name].remove()
        del self.database[name]

    def out(self, name, save_dir):  # 输出数据表
        self.database[name].out_file(save_dir)

    def return_database(self):
        return list(self.database.keys())


class LogBase(metaclass=ABCMeta):
    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def close(self):
        pass


class Log(LogBase):
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.log_file = open(
            log_dir + f"{os.sep}log.coTanLog",
            "r+" if os.path.exists(log_dir + "log.coTanLog") else "w+",
        )

    def write(self, data):
        self.log_file.write(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}] "
            + data
            + "\n"
        )
        self.log_file.flush()

    def close(self):
        self.log_file.close()


class PageBase:
    def __init__(self, time_out):
        self.url = ""
        self.user_agent = ""
        self.mode = "PAGE"
        self.time_out = time_out

    def __str__(self):
        return f"[{self.time_out}s]{self.mode}-{self.url}:UA>{self.user_agent}"

    @abstractmethod
    def init(self, *args, **kwargs):
        pass


class __RequestsBase(PageBase):
    def init(self, user_agent, url, cookies):
        if user_agent == "":
            user_agent = (
                f'--user-agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                f'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66"'
            )
        self.user_agent = user_agent
        self.headers = {
            "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
            "Accept - Encoding": "gzip, deflate",
            "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.5",
            "Connection": "Keep-Alive",
            "User-Agent": user_agent,
        }
        self.url = url
        self.cookies = cookies
        self.new = True


@plugin_class_loading(get_path(r'template/crawler'))
class UrlGet(__RequestsBase):  # 通过requests的post请求
    def __init__(self, url, time_out, user_agent="", cookies=None, **kwargs):
        super(UrlGet, self).__init__(time_out)
        self.mode = "simplify_get"
        self.requests = requests.get
        self.init(user_agent, url, cookies)


@plugin_class_loading(get_path(r'template/crawler'))
class UrlPost(__RequestsBase):  # 通过requests的post请求
    def __init__(self, url, data, time_out, user_agent="", cookies=None, **kwargs):
        super(UrlPost, self).__init__(time_out)
        self.mode = "post"
        self.data = data
        self.requests = requests.post
        self.init(user_agent, url, cookies)

    def __str__(self):
        return super(UrlPost, self).__str__() + f";data>{self.data}"


@plugin_class_loading(get_path(r'template/crawler'))
class UrlPage(PageBase):
    def __init__(
        self,
        url,
        time_out,
        first_run=False,
        head=False,
        no_plugins=True,
        no_js=False,
        no_java=False,
        no_img=False,
        user_agent="",
        cookies=None,
        new=False,
        down_load_dir="",
        **kwargs,
    ):
        super(UrlPage, self).__init__(time_out)
        self.url = url
        self.mode = "get"
        self.options = webdriver.ChromeOptions()
        self.cookies = cookies  # cookies存储位置
        self.new = new  # 新键页面or新键浏览器
        self.down_load_dir = down_load_dir
        self.init(first_run, head, no_plugins, no_js, no_java, no_img, user_agent)

    def init(self, first_run, head, no_plugins, no_js, no_java, no_img, user_agent):
        self.options.add_argument("disable-infobars")  # 不显示
        prefs = {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": self.down_load_dir,
        }
        self.options.add_experimental_option("prefs", prefs)  # 下载设置
        if first_run:
            self.options.add_argument("-first run")
        if head:  # 无头设置
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
        if no_plugins:
            self.options.add_argument("--disable-plugins")
        if no_js:
            self.options.add_argument("--disable-javascript")
        if no_java:
            self.options.add_argument("--disable-java")
        if no_img:
            self.options.add_argument("blink-settings=imagesEnabled=false")
        if user_agent == "":
            user_agent = (
                f'user-agent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                f'Chrome/80.0.3987.132 Safari/537.36"'
            )
        # self.options.add_argument(f'--user-agent ="{UA}"')
        self.user_agent = user_agent

    def __str__(self):
        return f"{self.mode}-{self.url}:UA>{self.user_agent}"


class Urlbase(metaclass=ABCMeta):
    url_count = 0  # url处理器个数

    def __init__(self, dic=f"", dic_run=f""):
        Urlbase.url_count += 1
        self.save_dir = dic
        dic += f"{os.sep}url[{Urlbase.url_count}].cot_url"
        dic_run += f"{os.sep}url_run[{Urlbase.url_count}].cot_url"
        self.dir = dic
        self.dir_run = dic_run
        self.file = open(dic, "a")  # 写入url_history的文件
        self.file_run = open(dic_run, "a")  # 写入已读url文件
        self.url_list = []  # 待读url
        self.url_history = []  # url历史
        self.filter = {}  # 过滤函数

    @abstractmethod
    def filter_func(self, url, **kwargs):
        pass

    @abstractmethod
    def add_filter_func(self, func, name):
        pass

    @abstractmethod
    def del_filter_func(self, index):
        pass

    @abstractmethod
    def return_filter_func(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def out_url_history(self, url):
        pass

    @abstractmethod
    def out_url_run(self, url):
        pass


@plugin_class_loading(get_path(r'template/crawler'))
class UrlFile(Urlbase, metaclass=ABCMeta):
    def close(self):
        self.file.close()
        self.file_run.close()

    def out_url_history(self, url):  # 输出url历史
        self.file.write(f"{url}\n")
        self.file.flush()

    def out_url_run(self, url):  # 输出已经运行的url
        self.file_run.write(f"{url}\n")
        self.file_run.flush()


@plugin_class_loading(get_path(r'template/crawler'))
class UrlAdd(Urlbase, metaclass=ABCMeta):
    def filter_func(self, url, **kwargs):  # url过滤系统
        for i in self.filter:
            if not self.filter[i](url):
                return False
        return True

    def add_filter_func(self, func, name):  # 添加过滤函数
        self.filter[name] = func

    def del_filter_func(self, index):  # 删除过滤函数
        del self.filter[list(self.filter.keys())[index]]

    def clean_filter_func(self):
        self.filter = {}

    def return_filter_func(self):
        return list(self.filter.keys())


@plugin_class_loading(get_path(r'template/crawler'))
class UrlReturn(Urlbase, metaclass=ABCMeta):
    def del_url(self, index):  # 删除url
        self.out_url_run(f"DELETE {self.url_list[index]}")
        del self.url_list[index]

    def get_url(self):  # 取得url
        url_page = self.url_list[0]
        self.out_url_run(url_page.url)
        del self.url_list[0]
        return url_page

    def is_finish(self):
        return len(self.url_list) == 0

    def add_url(self, url, func, data=None, must=False, **kwargs):  # 添加url
        if func == "":
            func = "get"
        if func == "get":
            url_ = url
        else:
            url_ = url + str(data)
        if must or (url_ not in self.url_history and self.filter_func(url, func=func)):  # 1.url不存在历史，2.url满足筛选条件
            if func == "get":
                self.url_list.append(
                    UrlPage(url=url, **kwargs, down_load_dir=self.dir)
                )  # 添加到待取得url
            elif func == "simplify_get":
                self.url_list.append(
                    UrlGet(url=url, **kwargs, down_load_dir=self.dir)
                )  # 添加到待取得url
            else:
                self.url_list.append(UrlPost(url=url, data=data, **kwargs))  # 添加到待取得url

            self.url_history.append(url_)  # 添加到历史url
            self.out_url_history(url_)  # 输出历史url
            return True  # 写入成功
        return False  # 写入失败


class SeleniumBase(metaclass=ABCMeta):
    @abstractmethod
    def selenium_mode(self, func_cookie, url):
        pass


class RequestsBase(metaclass=ABCMeta):
    @abstractmethod
    def requests_mode(self, func_cookie, url):
        pass


class PagedownloaderBase(SeleniumBase, RequestsBase, metaclass=ABCMeta):
    downloader_count = 0

    def __init__(self, url, dic=""):
        self.url = url
        self.dir = dic
        self.log = Log(dic)
        PagedownloaderBase.downloader_count += 1
        self.page_source_dict = {}  # 页面保存信息
        self.cookie_Thread = None  # 子进程
        self.browser = None
        self.cookie_dict = {}
        self.cookie_dict_list = {}  # sele的cookies
        self.last_mode = None

    def set_page_parser(self, parser):
        self.parser = parser

    @abstractmethod
    def monitoring_add_cookies(self, cookies):
        pass

    @abstractmethod
    def monitoring_clear_cookier(self):
        pass


@plugin_class_loading(get_path(r'template/crawler'))
class PageDownloaderRun(PagedownloaderBase, metaclass=ABCMeta):
    def close(self):
        self.log.close()

    def stop(self):
        self.break_ = False
        if self.last_mode is not None:
            try:
                self.browser.quit()
            except InvalidSessionIdException:
                pass
        self.last_mode = None

    def start_to_run(self, *args, func_cookie):  # 用get请求url ->得到一个页面信息
        self.break_ = False
        self.page_source_dict = {}
        self.url_text = self.url.get_url()  # 获取一个url
        url = self.url_text.url
        try:
            if self.url_text.mode == "get":
                self.selenium_mode(func_cookie, url)
            else:  # requests模式
                self.requests_mode(func_cookie, url)
        except BaseException:
            raise CookiesError
        finally:
            self.last_mode = self.url_text.mode
        self.parser.browser = self.browser
        self.parser.init(url)
        return self.browser


@plugin_class_loading(get_path(r'template/crawler'))
class PageDownloaderCookies(PagedownloaderBase, metaclass=ABCMeta):
    def monitoring_del_cookies(self, name):  # 删除指定cookies
        self.browser.delete_cookie(name)

    def monitoring_clear_cookier(self):  # 清空cookies
        self.browser.delete_all_cookies()

    def monitoring_add_cookies(self, cookies: dict):  # 新增cookies
        self.browser.add_cookie(cookies)

    def monitoring_update_cookies(self, name, cookies: dict):
        cookies_list = self.browser.get_cookies()
        for i in cookies_list:
            if i.get("name", None) == name:
                self.browser.delete_cookie(name)  # 删除原来cookies
                i.update(cookies)
                self.browser.add_cookie(i)
                return
        raise Exception


@plugin_class_loading(get_path(r'template/crawler'))
class PageDownloaderRequests(PageDownloaderRun, metaclass=ABCMeta):
    def requests_start_cookies(self, func_cookie, url):
        self.cookie_dict[url] = requests.utils.dict_from_cookiejar(
            self.browser.cookies
        )  # 保存cookies
        func_cookie([self.cookie_dict[url]])

    def requests_run(self, parameters, url):
        self.browser = self.url_text.requests(
            url,
            headers=self.url_text.headers,
            timeout=self.url_text.time_out,
            **parameters,
        )

    def requests_data(self, parameters):
        if self.url_text.mode == "post":
            parameters["data"] = self.url_text.data
        return parameters

    def requests_cookies(self, func_cookie):
        try:
            parameters = {"cookies": self.cookie_dict[self.url_text.cookies]}
        except KeyError:
            parameters = {}
            func_cookie([])
        else:
            func_cookie([parameters["cookies"]])
        return parameters

    def requests_mode(self, func_cookie, url):
        parameters = self.requests_cookies(func_cookie)
        parameters = self.requests_data(parameters)
        self.requests_run(parameters, url)
        self.requests_start_cookies(func_cookie, url)


@plugin_class_loading(get_path(r'template/crawler'))
class PageDownloaderSelenium(PageDownloaderRun, metaclass=ABCMeta):

    def selenium_quit(self):
        try:
            self.browser.quit()
        except InvalidSessionIdException:
            pass

    def selenium_cookies(self):
        try:
            if not self.url_text.new:
                raise UrlError
            cookies_list = self.cookie_dict_list[self.url_text.cookies]
        except (UrlError, KeyError):
            pass
        else:
            self.monitoring_clear_cookier()
            try:
                for i in cookies_list:
                    self.monitoring_add_cookies(i)
            except WebDriverException:
                pass

    def start_selenium(self, quit_=True):
        if quit_:
            self.selenium_quit()
        self.browser = webdriver.Chrome(chrome_options=self.url_text.options)

    def selenium_run(self, url):
        self.browser.set_page_load_timeout(self.url_text.time_out)  # 设置页面加载超时
        self.browser.set_script_timeout(self.url_text.time_out)  # 设置页面异步js执行超时
        self.browser.get(url)

    def selenium_start_cookies(self, func_cookie, url):
        self.break_ = True

        def update_cookie():
            nonlocal self
            while self.break_:
                try:
                    cookies = self.browser.get_cookies()
                    func_cookie(cookies)  # 与GUI通信显示cookie
                    self.cookie_dict[url] = cookies
                    time.sleep(0.5)
                except WebDriverException:
                    pass

        self.cookie_Thread = threading.Thread(target=update_cookie)
        self.cookie_Thread.start()

    def selenium_mode(self, func_cookie, url):
        if self.url_text.new and self.last_mode == "get":  # 重新启动
            self.start_selenium()
        elif self.last_mode is None:
            self.start_selenium(False)
        try:
            self.selenium_run(url)
        except WebDriverException:
            self.start_selenium()
            self.selenium_run(url)
        self.selenium_cookies()
        self.selenium_start_cookies(func_cookie, url)


class PageParserBase:
    def __init__(self, downloader):
        self.downloader = downloader
        self.downloader.set_page_parser(self)
        self.func_list = []
        self.func_dict = {}
        self.n = 0
        self.init()

    def init(self, url=""):
        self.element_dict = {}  # 记录属性的名字
        self.url_text = url

    @staticmethod
    def add_base(func):  # 装饰器
        def wrap(num=None, name=None, *args, **kwargs):
            try:
                func(num=num, name=name, *args, **kwargs)
                return True, ''
            except BaseException as e:
                return False, str(e)

        return wrap


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserFunc(PageParserBase):
    def tra_func(self):
        self.func_list = []
        self.func_dict = {}
        self.n = 0

    def add_func(self, name, func):
        self.func_list.append(f"{name}[{self.n}]")
        self.func_dict[f"{name}[{self.n}]"] = func
        self.n += 1

    def del_func(self, index, end=False):
        if end:
            index = len(self.func_list) - index - 1
        del self.func_dict[self.func_list[index]]
        self.func_list[index] = "Func_have_been_del"
        self.func_dict["Func_have_been_del"] = lambda *args, **kwargs: None

    def return_func(self, only=True):
        if only:
            return self.func_list.copy()
        else:
            return [
                f"var[{index}]@ {i}" for index, i in enumerate(self.func_list.copy())
            ]


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserFind(PageParserFunc):
    def find_id(self, id_, not_all=False, **kwargs):
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, id_
            if not_all:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_id(id_)
                ]  # 返回必须是list
            else:
                self.element_dict[f"{name}[{num}]"] = self.browser.find_elements_by_id(id_)

        self.add_func(f"find_ID:{id_}", find)  # 添加func

    def find_class(self, class_name, not_all=False, **kwargs):
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, class_name
            self.browser = self.browser
            if not_all:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_class_name(class_name)
                ]  # 返回必须是list
            else:
                self.element_dict[
                    f"{name}[{num}]"
                ] = self.browser.find_elements_by_class_name(
                    class_name
                )  # 返回必须是list

        self.add_func(f"find_class:{class_name}", find)  # 添加func

    def find_name(self, name_, not_all=False, **kwargs):
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, name_
            if not_all:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_name(name_)
                ]  # 返回必须是list
            else:
                self.element_dict[f"{name}[{num}]"] = self.browser.find_elements_by_name(
                    name_
                )  # 返回必须是list

        self.add_func(f"find_name:{name_}", find)  # 添加func

    def find_xpath(self, xpath, not_all=False, **kwargs):
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, xpath
            if not_all:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_xpath(xpath)
                ]  # 返回必须是list
            else:
                self.element_dict[f"{name}[{num}]"] = self.browser.find_elements_by_xpath(
                    xpath
                )  # 返回必须是list

        self.add_func(f"find_xpath:{xpath}", find)  # 添加func

    def find_css(self, css_selector, not_all=False, **kwargs):
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, css_selector
            if not_all:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_css_selector(css_selector)
                ]  # 返回必须是list
            else:
                self.element_dict[
                    f"{name}[{num}]"
                ] = self.browser.find_elements_by_css_selector(
                    css_selector
                )  # 返回必须是list

        self.add_func(f"find_css:{css_selector}", find)  # 添加func

    def find_tag_name(self, tag_name, not_all=False, **kwargs):
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, tag_name
            if not_all:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_tag_name(tag_name)
                ]  # 返回必须是list
            else:
                self.element_dict[f"{name}[{num}]"] = self.browser.find_elements_by_tag_name(
                    tag_name
                )  # 返回必须是list

        self.add_func(f"find_tagName:{tag_name}", find)  # 添加func\

    def find_link_text(self, link_text, not_all=False, **kwargs):  # 匹配link
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, link_text
            if not_all:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_link_text(link_text)
                ]  # 返回必须是list
            else:
                self.element_dict[
                    f"{name}[{num}]"
                ] = self.browser.find_elements_by_link_text(
                    link_text
                )  # 返回必须是list

        self.add_func(f"find_link_text:{link_text}", find)  # 添加func

    def find_partial_link_text(
        self, partial_link_text, not_all=False, **kwargs
    ):  # 模糊匹配
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, partial_link_text
            if not_all:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_partial_link_text(partial_link_text)
                ]  # 返回必须是list
            else:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.find_element_by_partial_link_text(partial_link_text)
                ]  # 返回必须是list

        self.add_func(f"find_partial_link_text:{partial_link_text}", find)  # 添加func

    def find_switch_to_alert(self, *args, **kwargs):  # 定位弹出框
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self
            self.element_dict[f"{name}[{num}]"] = [self.browser.switch_to.alert()]

        self.add_func(f"find_alert", find)  # 添加func

    def find_switch_to_active_element(self, *args, **kwargs):  # 定位焦点元素
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self
            self.element_dict[f"{name}[{num}]"] = [self.browser.switch_to.active_element()]

        self.add_func(f"active_element", find)  # 添加func

    def find_switch_to_frame(self, reference, is_id=False, *args, **kwargs):  # 定位Frame
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self, reference, is_id
            if reference is None:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.default_content()
                ]  # 回到主文档
            elif reference == "":
                self.element_dict[f"{name}[{num}]"] = [self.browser.parent_frame()]  # 回到父文档
            else:
                if is_id:
                    reference = int(reference)
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.switch_to.frame(str(reference))
                ]  # 定位进入文档

        func_name = {None: "主文档", "": "父文档"}.get(reference, reference)
        self.add_func(f"find_frame：{func_name}", find)  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserActionListBox(PageParserFunc):
    def deselect_by_index(
        self, element_value, deselect, index=0, **kwargs
    ):  # 根据index取消选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].deselect_by_index(int(deselect))

        self.add_func(
            f"deselect_by_index:{deselect}>{element_value}[{index}]", action
        )  # 添加func

    def deselect_by_text(
        self, element_value, deselect, index=0, **kwargs
    ):  # 根据text取消选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].deselect_by_visible_text(deselect)

        self.add_func(
            f"deselect_by_text:{deselect}>{element_value}[{index}]", action
        )  # 添加func

    def deselect_by_value(
        self, element_value, deselect, index=0, **kwargs
    ):  # 根据value取消选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].deselect_by_value(deselect)

        self.add_func(
            f"deselect_by_value:{deselect}>{element_value}[{index}]", action
        )  # 添加func

    def select_by_index(self, element_value, deselect, index=0, **kwargs):  # 根据index选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].select_by_index(int(deselect))

        self.add_func(
            f"select_by_index:{deselect}>{element_value}[{index}]", action
        )  # 添加func

    def select_by_text(self, element_value, deselect, index=0, **kwargs):  # 根据text选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].select_by_visible_text(deselect)

        self.add_func(
            f"select_by_text:{deselect}>{element_value}[{index}]", action
        )  # 添加func

    def select_by_value(self, element_value, deselect, index=0, **kwargs):  # 根据value选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].select_by_value(deselect)

        self.add_func(
            f"select_by_value:{deselect}>{element_value}[{index}]", action
        )  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserAction(PageParserFunc):
    def send_keys(self, text, element_value, index=0, **kwargs):  # 输入文字
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].send_keys(text)

        self.add_func(f"sent_text:{text}>{element_value}[{index}]", action)  # 添加func

    def authentication(
        self, user, passwd, element_value, index=0, **kwargs
    ):  # 输入验证(User&Password)
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].authenticate(user, passwd)

        self.add_func(
            f"Authentication:{user};{passwd}>{element_value}[{index}]", action
        )  # 添加func

    def clear(self, element_value, index=0, **kwargs):  # 清空文本
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].clear()

        self.add_func(f"clear_text>{element_value}[{index}]", action)  # 添加func

    def click(self, element_value, index=0, **kwargs):  # 点击按钮
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].click()

        self.add_func(f"click>{element_value}[{index}]", action)  # 添加func

    def accept(self, element_value, index=0, **kwargs):  # 点击确定(弹出框)
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].accept()

        self.add_func(f"accept>{element_value}[{index}]", action)  # 添加func

    def dismiss(self, element_value, index=0, **kwargs):  # 点击取消(弹出框)
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].dismiss()

        self.add_func(f"dismiss>{element_value}[{index}]", action)  # 添加func

    def submit(self, element_value, index=0, **kwargs):  # 提交表单
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].submit()

        self.add_func(f"submit>{element_value}[{index}]", action)  # 添加func

    def run_js(self, js, **kwargs):
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            get = self.browser.execute_script(js)
            if hasattr(get, "__getitem__"):  # 可切片
                self.element_dict[f"{name}[{num}]"] = get  # 返回必须是list
            else:
                self.element_dict[f"{name}[{num}]"] = [get]

        self.add_func(f"run_js:{js}", action)


class PageParserAutomation(PageParserFind, PageParserActionListBox, PageParserAction):
    pass


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserCookies(PageParserFunc):
    def del_all_cookies(self, **kwargs):  # 删除所有曲奇
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.browser.delete_all_cookies()

        self.add_func(f"del_all_cookies", action)

    def del_cookies(self, cookies_name, **kwargs):  # 删除指定曲奇
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.browser.delete_cookie(cookies_name)

        self.add_func(f"del_cookies:{cookies_name}", action)

    def add_cookies(self, cookies, **kwargs):  # 添加指定曲奇
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.browser.add_cookie(cookies)

        self.add_func(f"add_cookies:{cookies}", action)

    def update_cookies(self, cookies_name, cookies, **kwargs):  # 更新曲奇
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            now_cookies = self.browser.get_cookie(cookies_name)
            self.browser.delete_cookie(cookies_name)
            now_cookies.update(cookies)
            self.browser.add_cookie(now_cookies)

        self.add_func(f"add_cookies:{cookies}", action)

    def get_cookies(self, cookies_name, **kwargs):  # 获取指定曲奇
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            self.element_dict[f"{name}[{num}]"] = [
                self.browser.get_cookie(cookies_name)
            ]

        self.add_func(f"get_cookies:{cookies_name}", action)

    def get_all_cookies(self, **kwargs):  # 获取所有曲奇
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            self.element_dict[f"{name}[{num}]"] = self.browser.get_cookie()

        self.add_func(f"get_all_cookies", action)


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserBrowserActions(PageParserFunc):
    def back(self, **kwargs):  # 返回
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.browser.back()

        self.add_func(f"BACK", action)

    def forward(self, **kwargs):  # 前进
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.browser.forward()

        self.add_func(f"FORWARD", action)

    def refresh(self, **kwargs):  # 刷新
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.browser.refresh()

        self.add_func(f"REFRESH", action)

    def wait_sleep(self, time: int = 2, **kwargs):  # 暴力等待
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            sleep(time)

        self.add_func(f"WAIT:{time}s", action)

    def set_wait(self, time: int = 2, **kwargs):  # 隐式等待
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            sleep(time)

        self.add_func(f"Loading_wait:{time}s", action)


class PageParserBrowser(PageParserBrowserActions, PageParserCookies):
    pass


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserNeighbor(PageParserFunc):
    def __get_other_base(
        self, element_value, index: (slice, int), who="children", **kwargs
    ):  # 获得子、后代、兄弟标签的基类
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            iter_list = self.list_slicing(index, element_value)
            paser_list = []
            for bs in iter_list:
                if who != "brothers":
                    paser_list += {
                        "children": bs.children,
                        "offspring": bs.descendants,
                        "down": bs.next_siblings,
                        "up": bs.previous_siblings,
                    }.get(who, bs.children)
                else:
                    paser_list += bs.previous_siblings
                    paser_list += bs.next_siblings
            self.element_dict[f"{name}[{num}]"] = list(set(paser_list))

        self.add_func(f"get_{who}:{element_value}[{index}]", action)  # 添加func

    def get_children(self, element_value, index: (slice, int), **kwargs):
        return self.__get_other_base(element_value, index)

    def get_offspring(self, element_value, index: (slice, int), **kwargs):
        return self.__get_other_base(element_value, index, "offspring")

    def get_up(self, element_value, index: (slice, int), **kwargs):
        return self.__get_other_base(element_value, index, "up")

    def get_down(self, element_value, index: (slice, int), **kwargs):
        return self.__get_other_base(element_value, index, "down")

    def get_brothers(self, element_value, index: (slice, int), **kwargs):
        return self.__get_other_base(element_value, index, "brothers")


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserDataFindall(PageParserFunc):
    def findall(
        self,
        element_value,
        tag: (str, list),
        attribute: dict,
        limit,
        recursive,
        index: (slice, int),
        **kwargs,
    ):  # 根据标签定位
        if isinstance(tag, str):
            tag = str(tag).split(",")
        try:
            limit = int(limit)
        except ValueError:
            limit = None

        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            iter_list = self.list_slicing(index, element_value)
            paser_list = []
            for bs in iter_list:
                try:
                    re = bs.find_all(tag, attribute, limit=limit, recursive=recursive)
                except AttributeError:
                    try:
                        if str(bs.name) not in tag:
                            raise PageParserError
                        for agrs_name in attribute:
                            text = attribute[agrs_name]
                            if isinstance(text, str):
                                if bs.attrs[agrs_name] != text:
                                    raise PageParserError
                            else:  # 正则匹配
                                if not regular.match(text, bs.attrs[agrs_name]):
                                    raise PageParserError
                        re = [bs]
                    except PageParserError:
                        re = []
                paser_list += re
            self.element_dict[f"{name}[{num}]"] = paser_list

        self.add_func(f"findAll:{element_value}[{index}]", action)  # 添加func

    def findall_by_text(
        self,
        element_value,
        text: (regular.compile, str),
        limit,
        recursive,
        index: (slice, int),
        **kwargs,
    ):  # 根据text定位
        try:
            limit = int(limit)
        except ValueError:
            limit = None

        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            iter_list = self.list_slicing(index, element_value)
            paser_list = []
            for bs in iter_list:
                try:
                    re = bs.find_all(text=text, limit=limit, recursive=recursive)
                except AttributeError:
                    try:
                        if isinstance(text, str):
                            if str(bs.string) != text:
                                raise PageParserError
                        else:
                            if not regular.match(text, str(bs.string)):
                                raise PageParserError
                        re = [bs]
                    except PageParserError:
                        re = []
                paser_list += re
            self.element_dict[f"{name}[{num}]"] = paser_list

        self.add_func(f"findAll_by_text:{element_value}[{index}]", action)  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserDatabase(PageParserFunc):
    def to_database(
        self, element_value, index, data: (str, list), database_name: str, **kwargs
    ):  # 传入data Base
        @self.add_base
        def action(*args, **kwargs):
            global data_base
            nonlocal self
            iter_list = self.list_slicing(index, element_value)
            for bs in iter_list:
                new = []
                for i in data:
                    if i == "$name&":
                        new.append(bs.name)
                    elif i == "$self&":
                        new.append(str(bs).replace("\n", ""))
                    elif i == "$string$":
                        new.append(str(bs.string).replace("\n", ""))
                    else:
                        new.append(bs.attrs.get(i, ""))
                data_base.add_database(database_name, new)

        self.add_func(
            f"DataBase:{data}<{element_value}[{index}]>{database_name}", action
        )  # 添加func

    def to_database_by_re(
        self, element_value, index, data: str, database_name: str, **kwargs
    ):  # 通过正则，传入dataBase
        data = regular.compile(data)

        @self.add_base
        def action(*args, **kwargs):
            global data_base
            nonlocal self
            iter_list = self.list_slicing(index, element_value)
            for bs in iter_list:
                new = regular.findall(data, str(bs))
                data_base.add_database(database_name, new)

        self.add_func(
            f"DataBase:{data}<{element_value}[{index}]>{database_name}", action
        )  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserDataSource(PageParserFunc):
    def to_text(self, **kwargs):  # 获取网页源码
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            try:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.page_source,
                    self.url_text,
                ]
            except AttributeError:
                self.element_dict[f"{name}[{num}]"] = [
                    self.browser.text,
                    self.url_text,
                ]  # request

        self.add_func(f"get_page_source", action)

    def out_html(self, element_value, **kwargs):  # 输出网页源码
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            md5 = hashlib.md5()  # 应用MD5算法
            md5.update(f"{time.time()}_{self.url_text}".encode("utf-8"))
            name = md5.hexdigest()
            save_dir = self.dir + f"{os.sep}" + name + ".cotan_source"
            print(save_dir)
            with open(save_dir, "w") as f:
                f.write(self.element_dict[element_value][0])
            with open(save_dir + ".CoTanURL", "w") as f:
                f.write(self.element_dict[element_value][1])

        self.add_func(f"write_html<{element_value}", action)

    def make_bs(self, element_value, **kwargs):  # 解析成bs4对象
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            self.element_dict[f"{name}[{num}]"] = [
                bs4.BeautifulSoup(self.element_dict[element_value][0], "html.parser")
            ]

        self.add_func(f"Parsing:{element_value}", action)  # 添加func

    def add_url(
        self,
        element_value,
        index: (slice, int),
        url_name,
        update_func,
        url_args: dict,
        **kwargs,
    ):  # 自动添加url
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            iter_list = self.list_slicing(index, element_value)
            for bs in iter_list:
                try:
                    if url_name == "$name&":
                        new_url = bs.name
                    elif url_name == "$self&":
                        new_url = str(bs).replace("\n", "")
                    elif url_name == "$string$":
                        new_url = str(bs.string).replace("\n", "")
                    else:
                        new_url = bs.attrs.get(url_name, "")
                    self.downloader.url.add_url(new_url, **url_args)
                except AttributeError:
                    pass
            update_func()  # 更新tkinter

        self.add_func(f"add_URL<{element_value}[{index}]:{url_name}", action)  # 添加func

    def to_json(self, **kwargs):
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            self.element_dict[f"{name}[{num}]"] = [
                self.browser.json()
            ]  # request 解析为 json

        self.add_func(f"to_json", action)  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserTool(PageParserFunc):

    def list_slicing(self, index: (slice, int), element_value):
        if isinstance(index, int):
            return [self.element_dict[element_value][index]]
        else:
            return self.element_dict[element_value][index]

    def get_by_path(
        self, element_value, index: (slice, int), path, **kwargs
    ):  # 根据bs4的目录选择
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            iter_list = self.list_slicing(index, element_value)
            paser_list = []
            for bs in iter_list:
                try:
                    re = eval(str(path), {"self": bs})
                    if re is None:
                        raise PageParserError
                    paser_list.append(re)
                except BaseException as e:
                    logging.warning(str(e))
            self.element_dict[f"{name}[{num}]"] = paser_list

        self.add_func(f"get>{path}:{element_value}[{index}]", action)  # 添加func

    def webpage_snapshot(self, **kwargs):
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            md5 = hashlib.md5()  # 应用MD5算法
            md5.update(f"{time.time()}_{self.url_text}".encode("utf-8"))
            name = md5.hexdigest()
            with open(self.dir + f"{os.sep}" + name + ".png.CoTanURL", "w") as f:
                f.write(self.url_text)
            self.browser.save_screenshot(self.dir + f"{os.sep}" + name + ".png")
            sleep(1)

        self.add_func(f"Webpage_snapshot", action)  # 添加func


class PageParserData(PageParserDatabase, PageParserDataSource, PageParserDataFindall, PageParserTool):
    pass


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserChainsWindow(PageParserFunc):
    def get_all_windows(self, *args, **kwargs):  # 获取所有句柄
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self
            # 获得窗口句柄
            self.element_dict[f"{name}[{num}]"] = self.browser.window_handles

        self.add_func(f"get_all_windows", find)  # 添加func

    def get_now_windows(self, *args, **kwargs):  # 获取当前窗口句柄
        @self.add_base
        def find(num, name, *args, **kwargs):
            nonlocal self
            self.element_dict[f"{name}[{num}]"] = [
                self.browser.current_window_handle
            ]  # 获得当前窗口句柄

        self.add_func(f"get_now_window", find)  # 添加func

    def switch_to_windwos(self, element_value, index=0, **kwargs):  # 切换窗口
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.browser.switch_to.window(self.element_dict[element_value][index])

        self.add_func(f"switch_to_window>{element_value}[{index}]", action)  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserClick(PageParserFunc):
    def action_click(self, chains, element_value, index, **kwargs):  # 单击左
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].click(self.element_dict[element_value][index])

        self.add_func(f"[{chains}]click>[{element_value}][{index}]", action)  # 添加func

    def action_double_click(self, chains, element_value, index, **kwargs):  # 双击左
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].double_click(
                self.element_dict[element_value][index]
            )

        self.add_func(
            f"[{chains}]double_click>[{element_value}][{index}]", action
        )  # 添加func

    def action_click_right(self, chains, element_value, index, **kwargs):  # 点击右
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].context_click(
                self.element_dict[element_value][index]
            )

        self.add_func(
            f"[{chains}]right_click>[{element_value}][{index}]", action
        )  # 添加func

    def action_click_and_hold(self, chains, element_value, index, **kwargs):  # 按住左
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].click_and_hold(
                self.element_dict[element_value][index]
            )

        self.add_func(
            f"[{chains}]click_and_hold>[{element_value}][{index}]", action
        )  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserChainsMouse(PageParserFunc):
    def action_release(self, chains, element_value, index, **kwargs):  # 松开左键
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].release(
                self.element_dict[element_value][index]
            )

        self.add_func(f"[{chains}]release>[{element_value}][{index}]", action)  # 添加func

    def action_drag_and_drop(
        self, chains, element_value, index, element_value2, index2, **kwargs
    ):  # 拽托、松开
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].drag_and_drop(
                self.element_dict[element_value][index],
                self.element_dict[element_value2][index2],
            )

        self.add_func(
            f"[{chains}]drag_and_drop>[{element_value}][{index}]", action
        )  # 添加func

    def action_move(self, chains, element_value, index, **kwargs):  # 移动鼠标
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].move_to_element(
                self.element_dict[element_value][index]
            )

        self.add_func(
            f"[{chains}]drag_and_drop>[{element_value}][{index}]", action
        )  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserChainsKeys(PageParserFunc):
    @staticmethod
    def special_keys(key: str, is_special_keys):
        if is_special_keys:
            return keys_name_dict.get(key.lower(), key), f"[{key.upper()}]"
        else:
            return key, key

    def action_key_down(
        self, chains, key, element_value, index, is_special_keys, **kwargs
    ):  # down
        new_key, key = self.special_keys(key, is_special_keys)

        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].key_down(
                new_key, self.element_dict[element_value][index]
            )

        self.add_func(
            f"[{chains}]key_down>{key}:[{element_value}][{index}]", action
        )  # 添加func

    def action_key_up(
        self, chains, key, element_value, index, is_special_keys, **kwargs
    ):  # down
        new_key, key = self.special_keys(key, is_special_keys)

        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].key_up(
                new_key, self.element_dict[element_value][index]
            )

        self.add_func(
            f"[{chains}]key_up>{key}:[{element_value}][{index}]", action
        )  # 添加func

    def action_send_keys_to_element(
        self, chains, key, element_value, index, is_special_keys, **kwargs
    ):
        new_key, key = self.special_keys(key, is_special_keys)

        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].send_keys_to_element(
                self.element_dict[element_value][index], new_key
            )

        self.add_func(
            f"[{chains}]sent>{key}:[{element_value}][{index}]", action
        )  # 添加func

    def action_send_keys(self, chains, key, is_special_keys, **kwargs):  # 发送到焦点元素
        new_key, key = self.special_keys(key, is_special_keys)

        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].send_keys(new_key)

        self.add_func(f"[{chains}].sent>{key}", action)  # 添加func


@plugin_class_loading(get_path(r'template/crawler'))
class PageParserChains(PageParserChainsWindow, PageParserClick, PageParserChainsMouse,
                       PageParserChainsKeys):
    def make_action_chains(self, **kwargs):  # 创建动作链
        @self.add_base
        def action(num, name, *args, **kwargs):
            nonlocal self
            self.element_dict[f"{name}[{num}]"] = [ActionChains(self.browser)]

        self.add_func(f"make_ActionChains", action)  # 添加func

    def action_run(self, chains, run_time=1, **kwargs):  # 执行
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[chains][0].perform()
            sleep(run_time)

        self.add_func(f"[{chains}].run<{run_time}s", action)  # 添加func


for i in range(1, 13):  # F1 - F12按键
    keys_name_dict[f"f{i}"] = eval(f"Keys.F{i}", {'Keys': Keys})


data_base = DatabaseController()
