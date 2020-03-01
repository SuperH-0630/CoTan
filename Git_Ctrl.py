# -*- coding: <encoding name> -*-
from git import Repo
from os.path import split,exists
import os
import subprocess

sys_seeting = dict(shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
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
        if file_list == '.':
            file = '.'
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

    def check_Branch(self):#查看本地分支和远程分支
        return subprocess.Popen(f'echo 仓库分支:&&{git_path} branch -a&&echo 远程仓库信息:&&{git_path} remote -v',
                                cwd=self.Repo_Dic,**sys_seeting)

    def new_Branch(self,branch_name, origin):#新建分支
        return subprocess.Popen(f'{git_path} branch {branch_name} {origin}', cwd=self.Repo_Dic,**sys_seeting)

    def switch_Branch(self,branch_name):#切换分支
        return subprocess.Popen(f'{git_path} switch {branch_name}', cwd=self.Repo_Dic,**sys_seeting)

    def del_Branch(self,branch_name,del_type):#删除分支
        return subprocess.Popen(f'{git_path} branch -{del_type} {branch_name}', cwd=self.Repo_Dic,**sys_seeting)

    def merge_Branch(self,branch_name,no_ff,m=''):#合并分支
        if no_ff:no_ff = f' --no-ff -m "{m}"'#--no-ff前有空格
        else:no_ff = ''
        return subprocess.Popen(f'{git_path} merge{no_ff} {branch_name}', cwd=self.Repo_Dic,**sys_seeting)

    def merge_abort(self):#退出冲突处理
        return subprocess.Popen(f'{git_path} merge --abort', cwd=self.Repo_Dic,**sys_seeting)

    def Save_stash(self):#保存工作区
        return subprocess.Popen(f'{git_path} stash', cwd=self.Repo_Dic,**sys_seeting)

    def Stash_List(self):#保存工作区
        return subprocess.Popen(f'{git_path} stash list', cwd=self.Repo_Dic,**sys_seeting)

    def Apply_stash(self,stash_num = '0'):#保存工作区
        return subprocess.Popen(f'{git_path} stash apply stash@{{{stash_num}}}', cwd=self.Repo_Dic,**sys_seeting)

    def Drop_stash(self,stash_num = '0'):#保存工作区
        return subprocess.Popen(f'{git_path} stash drop stash@{{{stash_num}}}', cwd=self.Repo_Dic,**sys_seeting)

    def cherry_pick(self,commit):#保存工作区
        return subprocess.Popen(f'{git_path} cherry-pick {commit}', cwd=self.Repo_Dic,**sys_seeting)

    def Add_remote(self,remote,remote_name):
        return subprocess.Popen(f'{git_path} remote add {remote_name} {remote}', cwd=self.Repo_Dic, **sys_seeting)

    def Bind_remote(self,local_name,remote_name):
        return subprocess.Popen(f'{git_path} branch --set-upstream-to={remote_name} {local_name}', cwd=self.Repo_Dic,
                                **sys_seeting)

    def Add_Tag(self,tag,commit,message=''):
        if message != '':
            message = f' -m "{message}"'#自带空格
        if commit != '':
            commit = f' {commit}'#自带空格
        return subprocess.Popen(f'{git_path} tag -a {tag}{commit}{message}', cwd=self.Repo_Dic,
                                **sys_seeting)

    def Tag(self,condition=''):
        if condition != '':
            condition = f' -l {condition}'
        return subprocess.Popen(f'{git_path} tag{condition}', cwd=self.Repo_Dic,**sys_seeting)

    def show_new(self,condition):
        return subprocess.Popen(f'{git_path} show {condition}', cwd=self.Repo_Dic, **sys_seeting)

    def Pull_Push_remote(self,Pull_Push=0,remote='',local='',allow=False,u=False):
        split = remote.split('/')
        try:
            remote_name = ' '.join(split[0:2])
        except:
            remote_name = remote
            local = ''
        if allow:
            history = ' --allow-unrelated-histories'
        else:
            history = ''
        return subprocess.Popen(f'''{git_path} { {0:"pull",1:f"push{' -u' if u else ''}"}.get(Pull_Push,"pull") }{history} {remote_name} {local}''',
                                cwd=self.Repo_Dic, **sys_seeting)

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

    def check_Branch(self,name):
        return self.get_git(name).check_Branch()

    def new_Branch(self,name, new_branch, origin):
        return self.get_git(name).new_Branch(new_branch, origin)

    def switch_Branch(self,name,branch_name):
        return self.get_git(name).switch_Branch(branch_name)

    def Del_Branch(self,name,branch_name,type_):
        d = {1:'d',0:'D'}.get(type_,'d')
        return self.get_git(name).del_Branch(branch_name,d)

    def merge_Branch(self,name,branch_name,no_ff,m):
        return self.get_git(name).merge_Branch(branch_name,no_ff,m)

    def merge_abort(self,name):
        return self.get_git(name).merge_abort()

    def Save_stash(self,name):
        return self.get_git(name).Save_stash()

    def Stash_List(self,name):
        return self.get_git(name).Stash_List()

    def Apply_stash(self,name,stash_num='0'):
        return self.get_git(name).Apply_stash(stash_num)

    def Drop_stash(self,name,stash_num='0'):
        return self.get_git(name).Drop_stash(stash_num)

    def cherry_pick(self,name,commit):
        return self.get_git(name).cherry_pick(commit)

    def Add_remote(self,name,remote,remote_name):
        return self.get_git(name).Add_remote(remote,remote_name)

    def Bind_remote(self,name,local_name,remote_name):
        return self.get_git(name).Bind_remote(local_name,remote_name)

    def Pull_remote(self,name,local_name,remote_name,allow=False,u=False):
        return self.get_git(name).Pull_Push_remote(0,remote_name,local_name,allow,u)

    def Push_remote(self,name,local_name,remote_name,allow=False,u=False):
        return self.get_git(name).Pull_Push_remote(1,remote_name,local_name,False,u)#push没有allow选项

    def Tag(self,name, condition=''):
        return self.get_git(name).Tag(condition)  # push没有allow选项

    def show_new(self,name, condition):
        return self.get_git(name).show_new(condition)  # push没有allow选项

    def Add_Tag(self,name,tag,commit,message=''):
        return self.get_git(name).Add_Tag(tag,commit,message)  # push没有allow选项