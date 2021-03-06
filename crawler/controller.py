from crawler.template import UrlAdd, UrlReturn, PageDownloaderRequests, PageDownloaderSelenium, PageDownloaderCookies, \
     PageParserAutomation, PageParserBrowser, PageParserData, PageParserChains, UrlFile


class Url(UrlAdd, UrlReturn, UrlFile):  # url管理器

    def return_url(self):
        return self.url_list.copy()

    def return_url_history(self):
        return self.url_history.copy()


class PageDownloader(PageDownloaderRequests, PageDownloaderSelenium, PageDownloaderCookies):

    def requests_mode(self, func_cookie, url):
        if self.last_mode == "get":
            self.selenium_quit()
        return super(PageDownloader, self).requests_mode(func_cookie, url)

    def set_page_parser(self, parser):
        super(PageDownloader, self).set_page_parser(parser)
        self.parser.browser = self.browser
        self.parser.url = self.url
        self.parser.dir = self.dir
        self.parser.log = self.log


class PageParser(PageParserAutomation, PageParserBrowser, PageParserData, PageParserChains):

    def element_interaction(self, update_func=lambda *args: None):  # 元素交互
        func_list = self.func_list
        status = None
        self.log.write(f'{"*"*5}url:{self.url_text}{"*" * 5}')

        def update_log(func_name):
            nonlocal status, self
            if status:
                success_code = "Success to run"
            elif status is None:
                success_code = "No status"
            else:
                success_code = f"Wrong to run: {e} "
            self.log.write(
                f"last:[{success_code}];now:[{func_name}];url:{self.url_text} [END]"
            )
            value_box = []
            for i in self.element_dict:
                try:
                    value_box.append(f"{i}[{len(i)}] = {self.element_dict[i]}")
                except TypeError:
                    value_box.append(f"{i} = {self.element_dict[i]}")
            update_func(func_name, success_code, value_box)  # 信息更新系统

        update_log("开始解析")
        for func_num in range(len(func_list)):
            func_name = func_list[func_num]
            update_log(func_name)
            status, e = self.func_dict[func_name](num=f"{func_num}", name="var")
        update_log("运行完成")
