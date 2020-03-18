import os
import shutil
from system import LOG_DIR

PATH = os.getcwd() + rf'{os.sep}template'


class NamingError(BaseException):
    pass


class ConflictError(BaseException):
    pass


class Systemctl:
    def __init__(self):
        self.dir_list = []
        self.plugin_list = []

    def get_dir(self):
        self.dir_list = os.listdir(PATH)
        return self.dir_list.copy()

    def get_all_plugin(self):
        self.get_dir()
        self.plugin_list = []
        for name in self.dir_list:
            try:
                plugin = os.listdir(f'{PATH}{os.sep}{name}')
                self.plugin_list += [f'{name}{os.sep}{i}' for i in plugin]
            finally:
                pass
        return self.plugin_list.copy()

    def get_plugin(self, index):
        dir_name = self.dir_list[index]
        return [f'{dir_name}{os.sep}{i}' for i in os.listdir(f'{PATH}{os.sep}{dir_name}')]

    def add_plugin(self, index, plugin_dir):
        plugin_name = os.path.split(plugin_dir)[1]
        if plugin_name.startswith('template_') and plugin_name.endswith('.py'):
            dir_name = self.dir_list[index]
            targets_name = f'{PATH}{os.sep}{dir_name}{os.sep}{plugin_name}'
            if os.path.isfile(targets_name):
                raise ConflictError
            shutil.copyfile(plugin_dir, targets_name)
            return self.get_all_plugin()
        else:
            print(plugin_name)
            raise NamingError

    def del_plugin(self, index):
        targets_name = f'{PATH}{os.sep}{self.plugin_list[index]}'
        os.remove(targets_name)
        return self.get_all_plugin()

    def merge_plugin(self, index, plugin_dir):
        plugin_name = os.path.split(plugin_dir)[1]
        targets_name = f'{PATH}{os.sep}{self.dir_list[index]}{os.sep}{plugin_name}'
        name = plugin_name[9:-3]
        with open(targets_name, 'a+') as f:
            with open(plugin_dir, 'r') as g:
                f.write('\n' + g.read().replace('base = None', f'base = {name}'))

    def show_plugin(self, index):
        with open(f'{PATH}{os.sep}{self.plugin_list[index]}') as f:
            code = f.read() + '\n[END]'
        return code, self.plugin_list[index]

    def show_log(self):
        with open(LOG_DIR) as f:
            log = f.read()
        return log
