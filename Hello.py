from multiprocessing import Process, Queue, freeze_support
import threading
import time
import os
import webbrowser
import random
import flask
import json

from newtkinter import DragWindow, center_windows

app = flask.Flask(__name__, static_url_path='')

pic_list = os.listdir(f'{os.getcwd()}{os.sep}static{os.sep}Pic')
del pic_list[pic_list.index('favicon.ico')]
pic_list = random.sample(pic_list, 10)
queue_box = []
var_box = []
new_queue_box = True
new_var_box = True


@app.route('/img', methods=['get'])
def get_img():
    pic = pic_list[int(str(time.time())[-1])]
    print(pic)
    return pic


@app.route('/sent', methods=['get'])
def sent():
    value = flask.request.args.get("message", '')
    index = queue_box.index(flask.request.args.get("index", queue_box[0]))
    queue_controller.put(value, index)
    return 'success'


@app.route('/update')
def update():
    global new_queue_box, new_var_box
    must = flask.request.args.get("must", 'NO')
    if must == 'must':
        new_queue_box = True
        new_var_box = True
    repo = {'queue': queue_box, 'var': var_box}
    if new_queue_box or new_var_box:
        repo['status'] = 'YES'
    else:
        repo['status'] = "NO"
    new_queue_box = False
    new_var_box = False
    return repo


def update_queue_box(queue_list):
    global queue_box, new_queue_box
    queue_box = queue_list
    new_queue_box = True


def update_var_box(var_dict, var_from):
    global var_box, new_var_box
    var = []
    for name in var_dict:
        var.append(f'{name}[{var_from[name]}] : {var_dict[name]}')
    var_box = var
    new_var_box = True


class QueueController:
    def __init__(self):
        self.in_dict = {}
        self.out_dict = {}
        self.var_dict = {}
        self.queue_list = []
        self.var_from = {}
        self.update_var = lambda x, y: None
        self.update_queue = lambda x: None
        self.run = False
        self.stop_str = "__--$$stop_process$$--__"

    def can_stop(self):
        return len(self.out_dict) == 0

    def __call__(self, *args, **kwargs):
        self.run = True

        def done():
            while self.run:
                stop_pid = []
                old_var = list(self.var_dict.keys())
                for out in self.out_dict:
                    output: Queue = self.out_dict[out]
                    if output.empty():
                        continue
                    dict_index = f'var_{len(self.var_dict)}'
                    get_out = output.get()
                    if get_out == self.stop_str:
                        stop_pid.append(out)
                    else:
                        self.var_dict[dict_index] = get_out
                        self.var_from[dict_index] = out
                if old_var != list(self.var_dict.keys()):
                    self.update_var(self.var_dict, self.var_from)
                if stop_pid:
                    for i in stop_pid:
                        del self.in_dict[i]
                        del self.out_dict[i]
                    self.queue_list = list(self.in_dict.keys())
                    self.update_queue(self.queue_list.copy())

        t = threading.Thread(target=done)
        t.setDaemon(True)
        t.start()
        return self

    def stop(self):
        self.run = False

    def add_queue(self, inqueue, outqueue, name):
        self.stop()
        time.sleep(0.5)
        self.in_dict[name] = inqueue
        self.out_dict[name] = outqueue
        self.queue_list = list(self.in_dict.keys())
        self.update_queue(self.queue_list.copy())
        self.update_var(self.var_dict, self.var_from)

    def init(self, update_var, update_queue):
        self.update_var = update_var
        self.update_queue = update_queue
        self.update_queue(list(self.in_dict.keys()))
        self.update_var(self.var_dict, self.var_from)

    def put(self, value: str, index):
        name_space = self.var_dict.copy()
        name_space.update(globals())
        in_queue = self.in_dict[self.queue_list[index]]
        if value.startswith('put_var '):
            var_name = value[7:]
            in_queue.put(self.var_dict.get(var_name))
        elif value.startswith('put_eval '):
            in_queue.put(eval(value[8:]), name_space)
        elif value.startswith('put_file ') and value.startswith('.py'):
            try:
                with open(value[4:], 'r') as f:
                    code_file = f.read()
                new_name_space = name_space
                exec(code_file, new_name_space)
                dict_index = f'var_{len(self.var_dict)}'
                in_queue.put(list(new_name_space.keys()))
                self.var_dict[dict_index] = new_name_space.copy()
                self.var_from[dict_index] = 'self'
            except BaseException as e:
                in_queue.put(str(e))
        else:
            in_queue.put(value)


queue_controller = QueueController()
queue_controller.init(update_var_box, update_queue_box)


def progress_bar(func):
    def run(*agrs, **kwargs):
        in_queue, out_queue = func(*agrs, **kwargs)
        pid = out_queue.get()
        name = func.__name__
        queue_controller.add_queue(in_queue, out_queue, f'{name}_{pid}')
        queue_controller()
        time.sleep(1)
        return 'run success'
    return run


def draftboard_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from draftboard import draw_main
    out_queue.put('start')
    # 不需要等待
    draw_main(in_queue, out_queue)


@app.route('/communication')
def communication():
    return app.send_static_file(r'Communication.html')


@app.route('/')
def hello():
    return app.send_static_file('Hello.html')


@app.route('/draftboard')
def draftboard():
    return draftboard_run()


@progress_bar
def draftboard_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=draftboard_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def datascience_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from datascience import machine_learning
    out_queue.put('start')
    time.sleep(0.5)
    machine_learning(in_queue, out_queue)


@app.route('/datascience')
def datascience():
    return datascience_run()


@progress_bar
def datascience_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=datascience_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def functionmapping_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from funcsystem.map import function_mapping
    out_queue.put('start')
    time.sleep(0.5)
    function_mapping(in_queue, out_queue)


@app.route('/functionmapping')
def functionmapping():
    return functionmapping_run()


@progress_bar
def functionmapping_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=functionmapping_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def functionfactory_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from funcsystem.factory import function_factory_main
    out_queue.put('start')
    time.sleep(0.5)
    function_factory_main(in_queue, out_queue)


@app.route('/functionfactory')
def functionfactory():
    return functionfactory_run()


@progress_bar
def functionfactory_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=functionfactory_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def algebraicfactory_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from algebraicfactory import algebraic_factory_main
    out_queue.put('start')
    time.sleep(0.5)
    algebraic_factory_main(in_queue, out_queue)


@app.route('/algebraicfactory')
def algebraicfactory():
    return algebraicfactory_run()


@progress_bar
def algebraicfactory_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=algebraicfactory_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def machinelearner_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from machinelearning import machine_learning
    out_queue.put('start')
    time.sleep(0.5)
    machine_learning(in_queue, out_queue)


@app.route('/machinelearner')
def machinelearner():
    return machinelearner_run()


@progress_bar
def machinelearner_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=machinelearner_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def git_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from gitrepo import git_main
    out_queue.put('start')
    time.sleep(0.5)
    git_main(in_queue, out_queue)


@app.route('/git')
def git():
    return git_run()


@progress_bar
def git_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=git_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def crawler_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from crawler import crawler_main
    out_queue.put('start')
    time.sleep(0.5)
    crawler_main(in_queue, out_queue)


@app.route('/crawler')
def crawler():
    return crawler_run()


@progress_bar
def crawler_run():
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=crawler_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def system_main(in_queue, out_queue):
    out_queue.put(str(os.getpid()))
    from system.gui import system_main
    out_queue.put('start')
    time.sleep(0.5)
    system_main(in_queue, out_queue)


@app.route('/system')
def system():
    return system_run()


@progress_bar
def system_run():  # 不需要进度条
    in_queue = Queue(10)
    out_queue = Queue(10)
    Process(target=system_main, args=(in_queue, out_queue)).start()
    return in_queue, out_queue


def to_website():
    t = threading.Thread(target=webbrowser.open, args=('https://cotan.songzh.website/',))
    t.start()


if __name__ == "__main__":
    freeze_support()
    app.run()
