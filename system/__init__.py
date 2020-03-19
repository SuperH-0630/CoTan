import os
import logging
from multiprocessing import Queue
import time
import threading
from sys import exit


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
        except NoPluginError:
            # logging.info(str(e) + 'no plugin')
            return base
        except BaseException as e:
            logging.info(f'{base.__name__} plugin wrong {e}')
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
                assert not func.__name__.endswith('_gui'), str(e)
        return adorner
    return catch


class QueueController:
    def __init__(self):
        self.in_queue = None
        self.out_queue = None
        self.run = True
        self.var_dict = {}
        self.stop = None
        self.before_stop = lambda: None

    def set_queue(self, in_queue: Queue, out_queue: Queue):
        self.in_queue = in_queue
        self.out_queue = out_queue
        return self

    def set_before_stop(self, func):
        self.before_stop = func

    def stop_process(self):
        self.run = False
        self.out_queue.put("__--$$stop_process$$--__")
        self.before_stop()
        time.sleep(0.5)

    def __call__(self, *args, **kwargs):
        self.run = True

        def done():
            while self.run:
                if self.in_queue.empty():
                    continue
                get = self.in_queue.get()
                try:
                    assert isinstance(get, str)
                    name_space = self.var_dict.copy()
                    name_space.update(globals())
                    if get.startswith('done '):
                        exec(get[5:], name_space)
                    elif get == 'get var_*':
                        self.out_queue.put(list(name_space.keys()))
                    elif get == 'get *':
                        self.out_queue.put(list(self.var_dict.keys()))
                    elif get.startswith('get_var '):
                        result = name_space.get(get[8:])
                        if result == '__--$$stop_process$$--__':
                            result += '_'
                        self.out_queue.put(result)
                        self.var_dict[f'var_{len(self.var_dict)}'] = result
                    elif get.startswith('get_eval '):
                        result = eval(get[9:], name_space)
                        if result == '__--$$stop_process$$--__':
                            result += '_'
                        self.out_queue.put(result)
                        self.var_dict[f'var_{len(self.var_dict)}'] = result
                    elif get.startswith('file ') and get.startswith('.py'):
                        with open(get[4:], 'r') as f:
                            code_file = f.read()
                        new_name_space = name_space
                        exec(code_file, new_name_space)
                        self.var_dict[f'var_{len(self.var_dict)}'] = new_name_space.copy()
                except AssertionError:
                    self.var_dict[f'var_{len(self.var_dict)}'] = get
                except BaseException as e:
                    self.out_queue.put(str(e))

        t = threading.Thread(target=done)
        t.setDaemon(True)
        t.start()
