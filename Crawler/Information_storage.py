import os
import time


class Database:
    def __init__(self, name):
        self.dir = rf'{os.getcwd()}/Database_dir/{name}.cotanDB'  # 创建DB文件
        self.file = open(self.dir, 'r+' if os.path.exists(self.dir) else 'w+')
        self.id = 0
        self.name = name
        for _ in self.file.readlines():
            self.id += 1

    def __str__(self):
        return self.name

    def close(self):
        try:
            self.file.close()
        except BaseException:
            pass

    def add_new(self, data):
        data_str = str(self.id)
        for i in data:
            data_str += ',' + str(i)
        data_str += '\n'
        self.file.write(data_str)
        self.file.flush()
        self.id += 1

    def remove(self):
        self.file.close()
        os.remove(self.dir)

    def out_file(self, out_dir):
        with open(out_dir + fr'/{self.name}.contanDB', 'w') as f:
            with open(self.dir) as g:
                f.write(g.read())


class DatabaseController:  # data base控制器
    def __init__(self):
        self.database = {}

    def add_database(self, name):  # 添加数据表
        self.database[name] = Database(name)

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
        except BaseException:
            pass

    def close_all(self):  # 关闭所有数据表
        for i in self.database:
            self.database[i].close()
        self.database = {}

    def rm_database(self, name):  # 删除数据表
        self.database[name].remove()
        del self.database[name]

    def out(self, name, dir):  # 输出数据表
        self.database[name].out_file(dir)

    def return_database(self):
        return list(self.database.keys())


class log:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.log_file = open(log_dir +
                             '/log.coTanLog', 'r+' if os.path.exists(log_dir +
                                                                     'log.coTanLog') else 'w+')

    def write(self, data):
        self.log_file.write(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}] " +
            data +
            '\n')
        self.log_file.flush()

    def close(self):
        self.log_file.close()
