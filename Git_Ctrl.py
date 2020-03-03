# -*- coding: <encoding name> -*-
from git import Repo
from os.path import split,exists
import os
import subprocess
from time import time
import random

sys_seeting = dict(shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
git_path = 'git'# git的地址，如果配置了环境变量则不需要修改
stopKey = '【操作完成】'#存储stopKey的global变量
passwd = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'#stopKey的候选词库

class git_Repo:#git的基类
    def __init__(self,Dic,*args,**kwargs):
        self.url = None
        try:
            if exists(Dic + r'/.git'):  # 是否为git 仓库
                pass
            elif Dic[-4:] =='.git':
                Dic = Dic[:-5]  # -5,得把/去掉
            else:raise Exception
        except:
            subprocess.Popen(f'{git_path} init',cwd=self.Repo_Dic,**sys_seeting).wait()
        self.Repo_Dic = Dic  # 仓库地址(末尾不带/)
        self.repo = Repo(Dic)
        self.name = split(Dic)[-1]
        self.have_clone = True

    def make_stopKey(self):#生成一个随机stopKey
        global stopKey,passwd
        code = ''
        for _ in range(8):#八位随机数
            code += passwd[random.randint(0, len(passwd) - 1)]#时间戳+8位随机数
        stopKey = (str(time()) + code).replace('.','')
        return stopKey

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
        return subprocess.Popen(f'echo 添加文件... && {git_path} add {file} && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)

    def Reset_File(self,file_list):
        file = self.Flie_List(file_list)
        return subprocess.Popen(f'echo 撤销文件... && {git_path} reset {file} && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)

    def Commit_File(self,m):
        return subprocess.Popen(f'echo 提交文件: && {git_path} commit -m "{m}" && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)

    def Status(self):#执行status
        return subprocess.Popen(f'echo 仓库状态: && {git_path} status && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)

    def Log(self,graph,pretty,abbrev):#执行log
        args = ''
        if graph:
            args += ' --graph'
        if pretty:
            args += ' --pretty=oneline'
        if abbrev:
            args += ' --abbrev-commit'
        return subprocess.Popen(f'echo 仓库日志: && {git_path} log{args} && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)

    def refLog(self):#执行reflog
        return subprocess.Popen(f'echo 操作记录: && {git_path} reflog && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)

    def Diff_File(self,MASTER='HEAD'):#执行diff
        return subprocess.Popen(f'echo 文件日志: && {git_path} diff {MASTER} && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)

    def reset(self,HEAD='HEAD~1'):
        return subprocess.Popen(f'echo 回退... && {git_path} reset --hard {HEAD} && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)

    def checkout(self,file_list):
        if len(file_list) >= 1:#多于一个文件，不用--，空格
            file = self.Flie_List(file_list,pat=' ')
            return subprocess.Popen(f'echo 丢弃修改: && {git_path} checkout {file} && echo {self.make_stopKey()}',cwd=self.Repo_Dic,**sys_seeting)
        elif len(file_list) == 1:
            return subprocess.Popen(f'echo 丢弃修改: && {git_path} checkout -- {file_list[0]} && echo {self.make_stopKey()}', cwd=self.Repo_Dic, **sys_seeting)
        else:
            return subprocess.Popen(f'echo 丢弃修改: && {git_path} checkout * && echo {self.make_stopKey()}', cwd=self.Repo_Dic, **sys_seeting)

    def rm(self,file_list):#删除版本库中的文件
        file = self.Flie_List(file_list)
        return subprocess.Popen(f'echo 删除... && {git_path} rm {file}', cwd=self.Repo_Dic,**sys_seeting)

    def check_Branch(self):#查看本地分支和远程分支
        return subprocess.Popen(f'echo 仓库分支: && {git_path} branch -a && echo 远程仓库信息: && {git_path} remote -v && '
                                f'echo 分支详情: && {git_path} branch -vv && echo {self.make_stopKey()}',
                                cwd=self.Repo_Dic,**sys_seeting)

    def new_Branch(self,branch_name, origin):#新建分支
        return subprocess.Popen(f'echo 新建分支... && {git_path} branch {branch_name} {origin} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def switch_Branch(self,branch_name):#切换分支
        return subprocess.Popen(f'echo 切换分支... && {git_path} switch {branch_name} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def del_Branch(self,branch_name,del_type):#删除分支
        return subprocess.Popen(f'echo 删除分支... && {git_path} branch -{del_type} {branch_name} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def merge_Branch(self,branch_name,no_ff,m=''):#合并分支
        if no_ff:no_ff = f' --no-ff -m "{m}"'#--no-ff前有空格
        else:no_ff = ''
        return subprocess.Popen(f'echo 合并分支... && {git_path} merge{no_ff} {branch_name} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def merge_abort(self):#退出冲突处理
        return subprocess.Popen(f'echo 冲突处理退出... && {git_path} merge --abort && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def Save_stash(self):#保存工作区
        return subprocess.Popen(f'echo 保存工作区... && {git_path} stash && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def Stash_List(self):#工作区列表
        return subprocess.Popen(f'echo 工作区列表: && {git_path} stash list && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def Apply_stash(self,stash_num = '0'):#恢复工作区
        return subprocess.Popen(f'echo 恢复工作区... && {git_path} stash apply stash@{{{stash_num}}} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def Drop_stash(self,stash_num = '0'):#删除工作区
        return subprocess.Popen(f'echo 删除工作区... && {git_path} stash drop stash@{{{stash_num}}} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def cherry_pick(self,commit):#补丁
        return subprocess.Popen(f'echo 补丁... && {git_path} cherry-pick {commit} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def Del_remote(self,remote_name):
        return subprocess.Popen(f'echo 删除远程仓库... && {git_path} remote remove {remote_name} && echo {self.make_stopKey()}', cwd=self.Repo_Dic, **sys_seeting)

    def Add_remote(self,remote,remote_name):
        return subprocess.Popen(f'echo 添加远程仓库... && {git_path} remote add {remote_name} {remote} && echo {self.make_stopKey()}', cwd=self.Repo_Dic, **sys_seeting)

    def Bind_remote(self,local_name,remote_name):
        return subprocess.Popen(f'echo 分支绑定... && {git_path} branch --set-upstream-to={remote_name} {local_name} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,
                                **sys_seeting)

    def push_Tag(self,tag,remote_name):
        return subprocess.Popen(f'echo 推送标签... && {git_path} push {remote_name} {tag} && echo {self.make_stopKey()}', cwd=self.Repo_Dic, **sys_seeting)

    def del_tag(self,tag):
        return subprocess.Popen(f'echo 删除本地标签... && {git_path} tag -d {tag} && echo {self.make_stopKey()}', cwd=self.Repo_Dic, **sys_seeting)

    def Add_Tag(self,tag,commit,message=''):
        a = ' -a'
        if message != '':
            message = f' -m "{message}"'#自带空格
        else:
            a = ''
        if commit != '':
            commit = f' {commit}'#自带空格
        return subprocess.Popen(f'echo 添加标签... && {git_path} tag{a} {tag}{commit}{message} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,
                                **sys_seeting)

    def Tag(self,condition=''):
        if condition != '':
            condition = f' -l {condition}'
        return subprocess.Popen(f'echo 标签列表: && {git_path} tag{condition} && echo {self.make_stopKey()}', cwd=self.Repo_Dic,**sys_seeting)

    def show_new(self,condition):
        return subprocess.Popen(f'echo 查询结果: && {git_path} show {condition} && echo {self.make_stopKey()}', cwd=self.Repo_Dic, **sys_seeting)

    def Pull_Push_remote(self,Pull_Push=0,remote='',remote_branch='',local='',allow=False,u=False,f=False):
        #处理逻辑
        # 1）remote去斜杠第一个作为主机名字
        # 2) 从remote分离主机名(如果没指定)
        # 3) 如果local为空，用HEAD填充
        # 4) 如果以上后，主机名仍为空，则local和分支均为空

        split = remote.split('/')
        try:
            remote_name = split[0]#获取主机名 1）
        except:
            remote_name = ''#没有主机名 1）

        branch_split = remote_branch.split('/')
        if len(branch_split) >= 2 and remote_name == '':
            remote_name = branch_split[0]# 2)
            remote_branch = '/'.join(branch_split[1:])# 2)
        if local.replace(' ','') == '':local = 'HEAD'# 3)
        if remote_name == '':# 4)
            branch = ''
        else:
            if Pull_Push == 1:
                # 注意，local不可以为空，也不会为空
                if remote_branch != '':branch = f'{local}:{remote_branch}'# git push <远程主机名> <本地分支名>:<远程分支名>
                else:branch = f'{local}'#要去掉冒号
            else:
                if remote_branch != 'HEAD':branch = f'{remote_branch}:{local}'  # git push <远程主机名> <本地分支名>:<远程分支名>
                else:branch = f'{remote_branch}'

        if allow:
            history = ' --allow-unrelated-histories'
        else:
            history = ''
        push_pull = {0:"pull",1:f"push{' -u' if u else ''}{' -f' if f else ''}"}
        return subprocess.Popen(f'''echo 与服务器连接... && {git_path} {push_pull.get(Pull_Push,"pull")}{history} {remote_name} {branch} && echo {self.make_stopKey()}''',
                                cwd=self.Repo_Dic, **sys_seeting)

    def del_Branch_remote(self,remote,remote_branch):
        split = remote.split('/')
        try:
            remote_name = split[0]  # 获取主机名 1）
        except:
            remote_name = ''  # 没有主机名 1）
        branch_split = remote_branch.split('/')
        if len(branch_split) >= 2 and remote_name == '':
            remote_name = branch_split[0]  # 2)
            remote_branch = '/'.join(branch_split[1:])  # 2)
        return subprocess.Popen(f'echo 删除远程分支... && {git_path} push {remote_name} :{remote_branch} && echo {self.make_stopKey()}',cwd=self.Repo_Dic, **sys_seeting)

    def del_Tag_remote(self,remote,tag):
        return subprocess.Popen(f'echo 删除远程标签... && {git_path} push {remote} :refs/tags/{tag} && echo {self.make_stopKey()}',cwd=self.Repo_Dic, **sys_seeting)

    def fetch(self,remote,remote_branch,local):
        # 处理逻辑
        # 1）remote去斜杠第一个作为主机名字
        # 2) 从remote分离主机名(如果没指定)
        # 3) 如果local为空，用HEAD填充
        # 4) 如果以上后，主机名仍为空，则local和分支均为空

        split = remote.split('/')
        try:
            remote_name = split[0]  # 获取主机名 1）
        except:
            remote_name = ''  # 没有主机名 1）

        branch_split = remote_branch.split('/')
        if len(branch_split) >= 2 and remote_name == '':
            remote_name = branch_split[0]  # 2)
            remote_branch = '/'.join(branch_split[1:])  # 2)
        if local.replace(' ', '') == '': local = 'HEAD'  # 3)
        if remote_name == '':  # 4)
            branch = ''
        else:
            if remote_branch != 'HEAD':
                branch = f'{remote_branch}:{local}'  # git push <远程主机名> <本地分支名>:<远程分支名>
            else:
                branch = f'{remote_branch}'

        return subprocess.Popen(f'''echo 更新远程仓库... && {git_path} fetch {remote_name} {branch} && echo {self.make_stopKey()}''', cwd=self.Repo_Dic, **sys_seeting)

    def Customize(self,command:str):
        return subprocess.Popen(command,cwd=self.Repo_Dic, **sys_seeting)

    def Clone(self,url):
        return subprocess.Popen(f'echo 克隆操作不被允许', cwd=self.Repo_Dic, **sys_seeting)

class Clone_git(git_Repo):#Clone一个git
    def __init__(self, Dic, *args, **kwargs):
        self.Repo_Dic = Dic  # 仓库地址
        self.url = None
        self.name = split(Dic)[-1]
        self.have_clone = False

    def Clone(self,url):
        if self.have_clone:super(Clone_git, self).Clone(url)
        self.have_clone = True
        return subprocess.Popen(f'echo 正在克隆... && {git_path} clone {url} {self.Repo_Dic}', cwd=split(self.Repo_Dic)[0], **sys_seeting)

    def after_Clone(self):
        self.repo = Repo(self.Repo_Dic)

class git_Ctrol:
    def __init__(self):
        self.git_Dic = {}#名字-文件位置
        self.gitType_Dic = {}#名字-类型

    def Add_init(self,Dic,**kwargs):
        git = git_Repo(Dic)
        self.git_Dic[git.name] = git
        self.gitType_Dic[git.name] = 'init'
        return git.name

    def Clone_init(self,Dic,**kwargs):
        git = Clone_git(Dic)
        self.git_Dic[git.name] = git
        self.gitType_Dic[git.name] = 'clone'
        return git.name

    def get_git(self,name):
        return self.git_Dic[name]

    def get_git_Dic(self):
        return self.git_Dic.copy()

    def get_Dir(self,name):
        return self.get_git(name).dir_list()

    def add_File(self,name,dic_list):
        return self.get_git(name).Add_File(dic_list)

    def reset_File(self,name,dic_list):
        return self.get_git(name).Reset_File(dic_list)

    def commit_File(self,name,m):
        return self.get_git(name).Commit_File(m)

    def log(self,name,graph,pretty,abbrev):
        return self.get_git(name).Log(graph,pretty,abbrev)

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

    def Del_remote(self,name,remote_name):
        return self.get_git(name).Del_remote(remote_name)

    def Add_remote(self,name,remote,remote_name):
        return self.get_git(name).Add_remote(remote,remote_name)

    def Bind_remote(self,name,local_name,remote_name):
        return self.get_git(name).Bind_remote(local_name,remote_name)

    def Pull_remote(self,name,local_name,remote_name,remote_branch,allow=False,u=False,f=False):
        return self.get_git(name).Pull_Push_remote(0,remote_name,remote_branch,local_name,allow,u,False)

    def Push_remote(self,name,local_name,remote_name,remote_branch,allow=False,u=False,f=False):
        return self.get_git(name).Pull_Push_remote(1,remote_name,remote_branch,local_name,False,u,f)#push没有allow选项

    def Tag(self,name, condition=''):
        return self.get_git(name).Tag(condition)  # push没有allow选项

    def show_new(self,name, condition):
        return self.get_git(name).show_new(condition)  # push没有allow选项

    def Add_Tag(self,name,tag,commit,message=''):
        return self.get_git(name).Add_Tag(tag,commit,message)  # push没有allow选项

    def push_Tag(self,name, tag, remoto):
        return self.get_git(name).push_Tag(tag, remoto)

    def push_allTag(self,name, remoto):
        return self.get_git(name).push_Tag('--tags', remoto)

    def del_Tag_remote(self,name , remote, tag):
        return self.get_git(name).del_Tag_remote(remote, tag)

    def del_Branch_remote(self,name , remote, remote_Branch):
        return self.get_git(name).del_Branch_remote(remote, remote_Branch)

    def del_tag(self,name,tag):
        return self.get_git(name).del_tag(tag)

    def Fetch(self,name,local_name,remote_name,remote_branch):
        return self.get_git(name).fetch(remote_name,remote_branch,local_name)

    def Customize(self,name,command:str):
        return self.get_git(name).Customize(command)

    def Clone(self,name,url):
        return self.get_git(name).Clone(url)

    def After_Clone(self,name):
        try:
            return self.get_git(name).after_Clone()
        except:
            return None