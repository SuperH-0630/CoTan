import os
import logging

PATH = os.getcwd()
LOG_DIR = rf'{PATH}{os.sep}Log{os.sep}log_system.log'
LOG_FORMAT = '%(asctime)s - %(pathname)s - %(levelname)s  [%(lineno)d]%(funcName)s  %(message)s'
basicConfig = dict(filename=LOG_DIR, level=logging.DEBUG, format=LOG_FORMAT)
logging.basicConfig(**basicConfig)


class NoPluginError(Exception):
    pass


def get_path(name):
    return f'{PATH}{os.sep}{name}'


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
                logging.info(f'{base.__name__} use plugin success')
                return namespace[name]
            else:
                raise NoPluginError
        except NoPluginError as e:
            logging.info(str(e) + 'no plugin')
            return base
        except BaseException as e:
            logging.warning(str(e))
            return base
    return plugin_read


plugin_func_loading = plugin_class_loading


def exception_catch(*args_catch, **kwargs_catch):
    def catch(func):
        def adorner(*args, **kwargs):
            try:
                return_ = func(*args, **kwargs)
                logging.debug(f'run  {func.__name__} args:{args}  kwargs:{kwargs} return:{return_}')
                return return_
            except BaseException as e:
                logging.error(f'{e}  {func.__name__} args:{args}  kwargs:{kwargs}')
                assert func.__name__.endswith('_gui'), str(e)
        return adorner
    return catch
