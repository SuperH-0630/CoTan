from selenium import webdriver
import threading
import time
from os.path import exists
from os import mkdir
import hashlib


class URL_PAGE():
    def __init__(self,url,func='get'):
        self.url = url
        self.func = func

    def __str__(self):
        return self.url

class url:#url管理器
    num = 0#url处理器个数
    def __init__(self,dic=f'',dic_run=f''):
        url.num += 1
        dic += f'/url[{url.num}].cot_url'
        dic_run += f'/url_run[{url.num}].cot_url'
        self.dir = dic
        self.dir_run = dic_run
        self.file = open(dic,'a')#写入url_history的文件
        self.file_run = open(dic_run,'a')#写入已读url文件
        self.url_list = []#待读url
        self.url_history = []#url历史
        self.filter = {}#过滤函数

    def filter_func(self,url):#url过滤系统
        for i in self.filter:
            if not self.filter[i](url): return False
        return True

    def Add_func(self,func,name):#添加过滤函数
        self.filter[name] = func

    def Del_func(self,index):#删除过滤函数
        del self.filter[list(self.filter.keys())[index]]

    def return_func(self):
        return list(self.filter.keys())

    def add_url(self,url):#添加url
        if url not in self.url_history and self.filter_func(url):#1.url不存在历史，2.url满足筛选条件
            self.url_list.append(URL_PAGE(url,'get'))#添加到待取得url
            self.url_history.append(url)#添加到历史url
            self.__out_url(url)#输出历史url
            return True#写入成功
        return False#写入失败

    def del_url(self,index):#删除url
        self.__out_url_run(f'DELETE {self.url_list[index]}')
        del self.url_list[index]

    def get_url(self) -> URL_PAGE:#取得url
        url_page = self.url_list[0]
        self.__out_url_run(url_page.url)
        del self.url_list[0]
        return url_page

    def __out_url(self,url):#输出url历史
        self.file.write(f'{url}\n')
        self.file.flush()

    def __out_url_run(self,url):#输出已经运行的url
        self.file_run.write(f'{url}\n')
        self.file_run.flush()

    def return_url(self):
        return self.url_list.copy()

    def return_url_history(self):
        return self.url_history.copy()

class Page_Downloader:
    num = 0
    def __init__(self,url:url,dic=''):
        self.url = url
        self.dir = dic
        Page_Downloader.num += 1
        self.page_source_dict = {}#页面保存信息
        self.cookie_Thread = None#子进程
        self.browser = None

    def __seeting(self,*args):#设置参数，请求头
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')# 不显示提示语句
        for i in args:
            if i == '':continue
            options.add_argument(i)
        return options

    def strat_urlGet(self,*args,func_cookie):#用get请求url ->得到一个页面信息
        self.break_ = False
        self.page_source_dict = {}
        self.nowurl = self.url.get_url()#获取一个url
        url = self.nowurl.url
        self.browser = webdriver.Chrome(chrome_options=self.__seeting(*args))
        self.browser.get(url)
        self.break_ = True
        def update_cookie():
            nonlocal self
            while self.break_:
                try:
                    func_cookie(self.browser.get_cookies())  # 与GUI通信显示cookie
                    time.sleep(.5)
                except:pass
        self.cookie_Thread = threading.Thread(target=update_cookie)
        self.cookie_Thread.start()
        self.Parser.browser = self.browser
        self.Parser.init()
        return self.browser

    def Del_cookies(self,name):#删除指定cookies
        browser = self.browser
        browser.delete_cookie(name)

    def Tra_cookies(self):#清空cookies
        browser = self.browser
        browser.delete_all_cookies()

    def Add_cookies(self,cookies:dict):#清空cookies
        browser = self.browser
        browser.add_cookie(cookies)

    def update_cookies(self,name,cookies:dict,):
        browser = self.browser
        cookies_list = browser.get_cookies()
        for i in cookies_list:
            if i.get('name',None) == name:
                browser.delete_cookie(name)#删除原来cookies
                i.update(cookies)
                browser.add_cookie(i)
                return
        raise Exception

    def set_Page_Parser(self,Parser):
        self.Parser = Parser
        self.Parser.browser = self.browser
        self.Parser.url = self.url

class Page_Parser:
    def __init__(self,Downloader:Page_Downloader):
        self.Downloader = Downloader
        self.Downloader.set_Page_Parser(self)
        self.func_list = []
        self.func_dict = {}
        self.init()

    def init(self):
        self.element_dict = {}#记录属性的名字

    def add_base(self,func):  # 装饰器
        def wrap(browser=None,num=None,name=None, *args, **kwargs):
            try:
                func(browser,num, name, *args, **kwargs)
                return False
            except:
                return True
        return wrap

    def add_func(self,name,func):
        n = len(self.func_list)
        self.func_list.append(f'{name}[{n}]')
        self.func_dict[f'{name}[{n}]'] = func

    def return_func(self):
        return self.func_list.copy()

    def find_ID(self,id,not_all=False):
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,id
            if browser == None:browser = self.browser
            if not_all:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_id(id)]#返回必须是list
            else:self.element_dict[f'{name}[{num}]'] = browser.find_elements_by_id(id)
        self.add_func(f'find_ID:{id}',find)#添加func

    def find_class(self,class_name,not_all=False):
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,class_name
            if browser == None:browser = self.browser
            if not_all:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_class_name(class_name)]#返回必须是list
            else:self.element_dict[f'{name}[{num}]'] = browser.find_elements_by_class_name(class_name)#返回必须是list
        self.add_func(f'find_class:{class_name}',find)#添加func

    def find_name(self,name_,not_all=False):
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,name_
            if browser == None:browser = self.browser
            if not_all:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_name(name_)]#返回必须是list
            else:self.element_dict[f'{name}[{num}]'] = browser.find_elements_by_name(name_)#返回必须是list
        self.add_func(f'find_name:{name_}',find)#添加func

    def find_xpath(self,xpath,not_all=False):
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,xpath
            if browser == None:browser = self.browser
            if not_all:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_xpath(xpath)]#返回必须是list
            else:self.element_dict[f'{name}[{num}]'] = browser.find_elements_by_xpath(xpath)#返回必须是list
        self.add_func(f'find_xpath:{xpath}',find)#添加func

    def find_css(self,css_selector,not_all=False):
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,css_selector
            if browser == None:browser = self.browser
            if not_all:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_css_selector(css_selector)]#返回必须是list
            else:self.element_dict[f'{name}[{num}]'] = browser.find_elements_by_css_selector(css_selector)#返回必须是list
        self.add_func(f'find_css:{css_selector}',find)#添加func

    def find_tag_name(self,tag_name,not_all=False):
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,tag_name
            if browser == None:browser = self.browser
            if not_all:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_tag_name(tag_name)]#返回必须是list
            else:self.element_dict[f'{name}[{num}]'] = browser.find_elements_by_tag_name(tag_name)#返回必须是list
        self.add_func(f'find_tagName:{tag_name}',find)#添加func\

    def find_link_text(self,link_text,not_all=False):#匹配link
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,link_text
            if browser == None:browser = self.browser
            if not_all:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_link_text(link_text)]#返回必须是list
            else:self.element_dict[f'{name}[{num}]'] = browser.find_elements_by_link_text(link_text)#返回必须是list
        self.add_func(f'find_link_text:{link_text}',find)#添加func

    def find_partial_link_text(self,partial_link_text,not_all=False):#模糊匹配
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,partial_link_text
            if browser == None:browser = self.browser
            if not_all:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_partial_link_text(partial_link_text)]#返回必须是list
            else:self.element_dict[f'{name}[{num}]'] = [browser.find_element_by_partial_link_text(partial_link_text)]#返回必须是list
        self.add_func(f'find_partial_link_text:{partial_link_text}',find)#添加func

    def find_switch_to_alert(self,*args,**kwargs):#定位弹出框
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self
            if browser == None:browser = self.browser
            self.element_dict[f'{name}[{num}]'] = [browser.switch_to.alert()]
        self.add_func(f'find_alert',find)#添加func

    def find_switch_to_active_element(self,*args,**kwargs):#定位焦点元素
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self
            if browser == None:browser = self.browser
            self.element_dict[f'{name}[{num}]'] = [browser.switch_to.active_element()]
        self.add_func(f'active_element',find)#添加func

    def find_switch_to_frame(self,reference,is_id=False,*args,**kwargs):#定位弹出框
        @self.add_base
        def find(browser, num, name, *args, **kwargs):
            nonlocal self,reference,is_id
            if browser == None:browser = self.browser
            if reference == None:
                self.element_dict[f'{name}[{num}]'] = [browser.default_content()]# 回到主文档
            elif reference == '':
                self.element_dict[f'{name}[{num}]'] = [browser.parent_frame()]# 回到父文档
            else:
                if is_id:reference = int(reference)
                self.element_dict[f'{name}[{num}]'] = [browser.switch_to.frame(str(reference))]# 定位进入文档
        self.add_func(f'find_frame：{reference}',find)#添加func

    def send_keys(self,text,element_value,index=0):#输入文字
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].send_keys(text)
        self.add_func(f'sent_text:{text}>{element_value}[{index}]', action)  # 添加func

    def User_Passwd(self,User,Passwd,element_value,index=0):#输入验证(User&Password)
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].authenticate(User,Passwd)
        self.add_func(f'sent_text:{User};{Passwd}>{element_value}[{index}]', action)  # 添加func

    def clear(self,element_value,index=0):#清空文本
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].clear()
        self.add_func(f'clear_text>{element_value}[{index}]', action)  # 添加func

    def click(self,element_value,index=0):#点击按钮
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].click()
        self.add_func(f'click>{element_value}[{index}]', action)  # 添加func

    def accept(self,element_value,index=0):#点击确定(弹出框)
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].accept()
        self.add_func(f'accept>{element_value}[{index}]', action)  # 添加func

    def dismiss(self,element_value,index=0):#点击取消(弹出框)
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].dismiss()
        self.add_func(f'dismiss>{element_value}[{index}]', action)  # 添加func

    def submit(self,element_value,index=0):#点击按钮
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].submit()
        self.add_func(f'submit>{element_value}[{index}]', action)  # 添加func

    def deselect_by_index(self,element_value,deselect_index,index=0):#根据index取消选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].deselect_by_index(int(deselect_index))
        self.add_func(f'deselect_by_index:{deselect_index}>{element_value}[{index}]', action)  # 添加func

    def deselect_by_text(self,element_value,deselect_text,index=0):#根据text取消选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].deselect_by_visible_text(deselect_text)
        self.add_func(f'deselect_by_text:{deselect_text}>{element_value}[{index}]', action)  # 添加func

    def select_by_index(self,element_value,deselect_index,index=0):#根据index选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].select_by_index(int(deselect_index))
        self.add_func(f'select_by_index:{deselect_index}>{element_value}[{index}]', action)  # 添加func

    def select_by_text(self,element_value,deselect_text,index=0):#根据text选择
        @self.add_base
        def action(*args, **kwargs):
            nonlocal self
            self.element_dict[element_value][index].select_by_visible_text(deselect_text)
        self.add_func(f'select_by_text:{deselect_text}>{element_value}[{index}]', action)  # 添加func

    def Element_interaction(self):#元素交互
        func_list = self.func_list
        for func_num in range(len(func_list)):
            self.func_dict[func_list[func_num]](num=f'{func_num}',name='var')