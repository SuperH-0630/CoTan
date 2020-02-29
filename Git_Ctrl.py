# -*- coding: <encoding name> -*-
from git import Repo
from os.path import split,exists
import os
import subprocess

sys_seeting = dict(shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
git_path = 'git'

class git_Repo:#git的基类
    def __init__(self,Dic,name,*args,**kwargs):
        self.Repo_Dic = Dic  # 仓库地址
        self.url = None
        if not exists(Dic + r'/.git'):  # 是否为git 仓库
            subprocess.Popen(f'{git_path} init',cwd=self.Repo_Dic,**sys_seeting).wait()
        self.repo = Repo(Dic)
        self.name = name

    def Flie_List(self,file_list,is_file=True,pat=' '):
        if file_list == '*':
            file = '*'
        else:
            file_ = []
            for i in file_list:
                if i[:len(self.Repo_Dic)] == self.Repo_Dic:
                    file_.append(i[len(self.Repo_Dic) + 1:])  # +1是为了去除/
            if not is_file:return file_
            file = pat.join(file_)
        return file

    def dir_list(self,all=True):
        listfile = []
        if all:
            listfile += [f'[当前分支] {self.repo.active_branch} 工作区{"不" if self.repo.is_dirty() else ""}干净 -> {self.name}']
        listfile += [f'{"[配置文件]" if i == ".git" else "[未跟踪]"if i in self.repo.untracked_files else "[已跟踪]"} {i}'
                     for i in os.listdir(self.Repo_Dic)]
        return listfile

    def Add_File(self,file_list):
        file = self.Flie_List(file_list)
        return subprocess.Popen(f'{git_path} add {file}',cwd=self.Repo_Dic,**sys_seeting)

    def Commit_File(self,m):
        return subprocess.Popen(f'{git_path} commit -m "{m}"',cwd=self.Repo_Dic,**sys_seeting)

    def Status(self):#执行status
        return subprocess.Popen(f'{git_path} status',cwd=self.Repo_Dic,**sys_seeting)

    def Log(self):#执行log
        return subprocess.Popen(f'{git_path} log',cwd=self.Repo_Dic,**sys_seeting)

    def refLog(self):#执行reflog
        return subprocess.Popen(f'{git_path} reflog',cwd=self.Repo_Dic,**sys_seeting)

    def Diff_File(self,MASTER='HEAD'):#执行diff
        return subprocess.Popen(f'{git_path} diff {MASTER}',cwd=self.Repo_Dic,**sys_seeting)

    def reset(self,HEAD='HEAD~1'):
        return subprocess.Popen(f'{git_path} reset --hard {HEAD}',cwd=self.Repo_Dic,**sys_seeting)

    def checkout(self,file_list):
        if len(file_list) >= 1:#多于一个文件，不用--，空格
            file = self.Flie_List(file_list,pat=' ')
            return subprocess.Popen(f'{git_path} checkout {file}',cwd=self.Repo_Dic,**sys_seeting)
        elif len(file_list) == 1:
            return subprocess.Popen(f'{git_path} checkout -- {file_list[0]}', cwd=self.Repo_Dic, **sys_seeting)
        else:
            return subprocess.Popen(f'{git_path} checkout *', cwd=self.Repo_Dic, **sys_seeting)

    def rm(self,file_list):#删除版本库中的文件
        file = self.Flie_List(file_list)
        return subprocess.Popen(f'{git_path} rm {file}', cwd=self.Repo_Dic,**sys_seeting)

class Clone_git(git_Repo):#Clone一个git
    def __init__(self,Dic,url,name,*args,**kwargs):
        super(Clone_git, self).__init__(Dic,name, *args, **kwargs)
        self.url = url
        Repo.clone_from(url=url,to_path=Dic)
        self.git = self.repo.git
        self.index = self.repo.index

class git_Ctrol:
    def __init__(self):
        self.git_Dic = {}#名字-文件位置
        self.gitType_Dic = {}#名字-类型

    def Add_init(self,Dic,**kwargs):
        name = split(Dic)[-1]
        git = git_Repo(Dic,name)
        self.git_Dic[name] = git
        self.gitType_Dic[name] = 'init'

    def Clone_init(self,Dic,url,**kwargs):
        name = split(Dic)[-1]
        git = Clone_git(Dic,url,name)
        self.git_Dic[name] = git
        self.gitType_Dic[name] = 'clone'

    def get_git(self,name):
        return self.git_Dic[name]

    def get_git_Dic(self):
        return self.git_Dic.copy()

    def get_Dir(self,name):
        return self.get_git(name).dir_list()

    def add_File(self,name,dic_list):
        return self.get_git(name).Add_File(dic_list)

    def commit_File(self,name,m):
        return self.get_git(name).Commit_File(m)

    def log(self,name):
        return self.get_git(name).Log()

    def reflog(self,name):
        return self.get_git(name).refLog()

    def status(self,name):
        return self.get_git(name).Status()

    def diff_File(self,name,MASTER):
        return self.get_git(name).Diff_File(MASTER)

    def back_version(self,name,HEAD):
        return self.get_git(name).reset(HEAD)

    def checkout_version(self,name,file):
        return self.get_git(name).checkout(file)

    def rm(self,name,file):
        return self.get_git(name).rm(file)