from selenium import webdriver

class url:
    num = 0#url处理器个数
    def __init__(self,dic=f'',dic_run=f'',add_func=lambda url:True,change_url=lambda url:url):
        url.num += 1
        if dic == '':dic = f'url[{url.num}].cot_url'
        if dic_run == '':dic = f'url_run[{url.num}].cot_url'
        self.dir = dic
        self.dir_run = dic_run
        self.file = open(dic,'a')#写入url_history的文件
        self.file_run = open(dic_run,'a')#写入已读url文件
        self.url_list = []#待读url
        self.add_func = add_func#url添加过滤方法
        self.change_url = change_url#url更正方法
        self.url_history = []#url历史

    def add_url(self,url):
        url = self.change_url(url)#url更正，比如http替换https
        if url not in self.url_history and self.add_func(url):#1.url不存在历史，2.url满足筛选条件
            self.url_list.append(url)
            self.url_history.append(url)
            self.__out_url(url)
            return True#写入成功
        return False#写入失败

    def get_url(self):
        url = self.url_list[0]
        self.__out_url_run(url)
        del self.url_list[0]
        return url

    def __out_url(self,url):#输出url
        self.file.write(f'{url}\n')
        self.file.flush()

    def __out_url_run(self,url):#输出url
        self.file_run.write(f'{url}\n')
        self.file_run.flush()

    def return_url(self):
        return self.url_list.copy()

    def return_url_history(self):
        return self.url_history.copy()