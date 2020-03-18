import os

PATH = os.getcwd()


def get_path(name):
    return f'{PATH}/{name}'


def plugin_class_loading(template_path):
    # 装饰器，装饰类的，允许使用自定义插件
    def plugin_read(base):
        name = base.__name__
        template = f'{template_path}/template_{name}.py'.replace('/', os.sep)
        try:
            if os.path.exists(template):
                with open(template, 'r') as f:
                    namespace = {'base': base}
                    exec(f.read().replace('base = None', ''), namespace)
                return namespace[name]
            else:
                raise Exception
        except BaseException:
            return base
    return plugin_read


plugin_func_loading = plugin_class_loading
