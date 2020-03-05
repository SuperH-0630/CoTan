from selenium import webdriver
import threading
import time
from os.path import exists
from os import mkdir
import hashlib


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
            self.url_list.append(url)#添加到待取得url
            self.url_history.append(url)#添加到历史url
            self.__out_url(url)#输出历史url
            return True#写入成功
        return False#写入失败

    def del_url(self,index):#删除url
        self.__out_url_run(f'DELETE {self.url_list[index]}')
        del self.url_list[index]

    def get_url(self):#取得url
        url = self.url_list[0]
        self.__out_url_run(url)
        del self.url_list[0]
        return url

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
        self.wait = {}#等待函数
        self.wait_list = []#等待函数的函数名字(执行顺序)
        self.cookie_Thread = None#子进程

    def Add_func(self,func,name):#添加等待函数
        name = f'[{len(self.wait)}]{name}'
        def f(*args,**kwargs):
            get = func(*args,**kwargs)
            print(get)
            try:
                if get[1] == '':raise Exception
                return get#save和name
            except:
                return False,''
        self.wait_list.append(name)
        self.wait[name] = f

    def Del_func(self,index):#删除等待函数
        del self.wait[list(self.wait.keys())[index]]

    def return_func(self):
        return list(self.wait.keys())

    def __seeting(self,*args):#设置参数，请求头
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')# 不显示提示语句
        for i in args:
            if i == '':continue
            options.add_argument(i)
        return options

    def strat_urlGet(self,*args):#用get请求url ->得到一个页面信息
        self.break_ = False
        self.page_source_dict = {}
        self.nowurl = self.url.get_url()#获取一个url
        url = self.nowurl
        self.browser = webdriver.Chrome(chrome_options=self.__seeting(*args))
        self.browser.get(url)
        return self.browser

    def Logical_operation(self,func_cookie=lambda x:None,func_page=lambda x:None):#执行等待策略
        browser = self.browser
        self.page_source_dict['FIRST_PAGE'] = browser.page_source#记录最先的PAGE源代码
        func_page(list(self.page_source_dict.keys()))
        self.break_ = True
        def update_cookie():
            nonlocal self
            while self.break_:
                try:
                    func_cookie(self.browser.get_cookies())  # 与GUI通信显示cookie
                    time.sleep(1)
                except:pass
        self.cookie_Thread = threading.Thread(target=update_cookie)
        self.cookie_Thread.start()
        for i in self.wait_list:
            save,name = self.wait[i](browser)
            if save:
                print(save)
                self.page_source_dict[name] = browser.page_source
            else:
                print(save)
            func_page(list(self.page_source_dict.keys()))
        self.page_source_dict['LAST_PAGE'] = browser.page_source#记录最后的PAGE源代码
        func_page(list(self.page_source_dict.keys()))

    def save_Page(self):#保存网页
        dic = self.dir + f'/Page_{hashlib.md5(self.nowurl.encode("utf8")).hexdigest()}'#通过计算哈希保存页面
        a = 0
        new_dir = ''
        while exists(dic):
            new_dir = dic + f'[{a}]'
            a += 1
        if new_dir == '':new_dir = dic
        mkdir(new_dir)
        with open(f'{new_dir}/url', 'w') as f:
            f.write(self.nowurl)
        for i in self.page_source_dict:
            with open(f'{new_dir}/{i}.html','w') as f:
                f.write(str(self.page_source_dict[i]))
        return None

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