import os
import random
import subprocess
from abc import ABCMeta, abstractmethod
from git import Repo
from os.path import exists, split
from time import time

from system import plugin_class_loading, get_path

sys_seeting = dict(
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
)
git_path = "git"  # git的地址，如果配置了环境变量则不需要修改
stop_key = "【操作完成】"  # 存储stopKey的global变量
passwd = (
    "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"  # stopKey的候选词库
)


class GitBase(metaclass=ABCMeta):
    def __init__(self, repo_dir, *args, **kwargs):
        self.repo_dir = ''
        self.repo = None
        self.init(repo_dir)

    @abstractmethod
    def init(self, repo_dir):
        pass

    @staticmethod
    def make_stop_key():  # 生成一个随机stopKey
        code = ""
        for _ in range(8):  # 八位随机数
            code += passwd[random.randint(0, len(passwd) - 1)]  # 时间戳+8位随机数
        stop_key = (str(time()) + code).replace(".", "")
        return stop_key

    def get_flie_list(self, file_list, is_file=True, pat=" "):
        if file_list == ".":
            file = ".."
        else:
            file_ = []
            for i in file_list:
                if i[: len(self.repo_dir)] == self.repo_dir:
                    file_.append(i[len(self.repo_dir) + 1:])  # +1是为了去除/
            if not is_file:
                return file_
            file = pat.join(file_)
        return file


@plugin_class_loading(get_path(r'template/gitrepo'))
class ViewClasses(GitBase, metaclass=ABCMeta):

    def status(self):  # 执行status
        return subprocess.Popen(
            f"echo 仓库状态: && {git_path} status && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def rm(self, file_list):  # 删除版本库中的文件
        file = self.get_flie_list(file_list)
        return subprocess.Popen(
            f"echo 删除... && {git_path} rm {file}", cwd=self.repo_dir, **sys_seeting
        )

    def dir_list(self, all=True):
        listfile = []
        if all:
            listfile += [
                f'[当前分支] {self.repo.active_branch} 工作区{"不" if self.repo.is_dirty() else ""}干净 -> {self.name}'
            ]
        listfile += [
            f'{"[配置文件]" if i == ".git" else "[未跟踪]"if i in self.repo.untracked_files else "[已跟踪]"} {i}'
            for i in os.listdir(self.repo_dir)
        ]
        return listfile

    def log(self, graph, pretty, abbrev):  # 执行log
        args = ""
        if graph:
            args += " --graph"
        if pretty:
            args += " --pretty=oneline"
        if abbrev:
            args += " --abbrev-commit"
        return subprocess.Popen(
            f"echo 仓库日志: && {git_path} log{args} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def do_log(self):  # 执行reflog
        return subprocess.Popen(
            f"echo 操作记录: && {git_path} reflog && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def diff(self, master="HEAD"):  # 执行diff
        return subprocess.Popen(
            f"echo 文件日志: && {git_path} diff {master} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def branch_view(self):  # 查看本地分支和远程分支
        return subprocess.Popen(
            f"echo 仓库分支: && {git_path} branch -a && echo 远程仓库信息: && {git_path} remote -v && "
            f"echo 分支详情: && {git_path} branch -vv && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def get_stash_list(self):  # 工作区列表
        return subprocess.Popen(
            f"echo 工作区列表: && {git_path} stash list && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def get_tag_list(self, condition=""):
        if condition != "":
            condition = f" -l {condition}"
        return subprocess.Popen(
            f"echo 标签列表: && {git_path} tag{condition} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def search_commit(self, condition):
        return subprocess.Popen(
            f"echo 查询结果: && {git_path} show {condition} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )


@plugin_class_loading(get_path(r'template/gitrepo'))
class NewClasses(GitBase, metaclass=ABCMeta):
    def add(self, file_list):
        file = self.get_flie_list(file_list)
        return subprocess.Popen(
            f"echo 添加文件... && {git_path} add {file} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def commit_file(self, m):
        return subprocess.Popen(
            f'echo 提交文件: && {git_path} commit -m "{m}" && echo {self.make_stop_key()}',
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def new_branch(self, branch_name, origin):  # 新建分支
        return subprocess.Popen(
            f"echo 新建分支... && {git_path} branch {branch_name} {origin} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def save_stash(self):  # 保存工作区
        return subprocess.Popen(
            f"echo 保存工作区... && {git_path} stash && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def cherry_pick(self, commit):  # 补丁
        return subprocess.Popen(
            f"echo 补丁... && {git_path} cherry-pick {commit} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def remote_add(self, remote, remote_name):
        return subprocess.Popen(
            f"echo 添加远程仓库... && {git_path} remote add {remote_name} {remote} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def bind_branch(self, local_name, remote_name):
        return subprocess.Popen(
            f"echo 分支绑定... && {git_path} branch --set-upstream-to={remote_name} {local_name} && echo "
            f"{self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def add_tag(self, tag, commit, message=""):
        a = " -a"
        if message != "":
            message = f' -m "{message}"'  # 自带空格
        else:
            a = ""
        if commit != "":
            commit = f" {commit}"  # 自带空格
        return subprocess.Popen(
            f"echo 添加标签... && {git_path} tag{a} {tag}{commit}{message} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )


@plugin_class_loading(get_path(r'template/gitrepo'))
class RemoveClass(GitBase, metaclass=ABCMeta):
    def del_cached_file(self, file_list):
        file = self.get_flie_list(file_list)
        return subprocess.Popen(
            f"echo 撤销文件... && {git_path} rm --cached {file} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def del_branch(self, branch_name, del_type):  # 删除分支
        return subprocess.Popen(
            f"echo 删除分支... && {git_path} branch -{del_type} {branch_name} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def drop_stash(self, stash_num="0"):  # 删除工作区
        return subprocess.Popen(
            f"echo 删除工作区... && {git_path} stash drop stash@{{{stash_num}}} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def del_remote(self, remote_name):
        return subprocess.Popen(
            f"echo 删除远程仓库... && {git_path} remote remove {remote_name} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def del_tag(self, tag):
        return subprocess.Popen(
            f"echo 删除本地标签... && {git_path} tag -d {tag} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def del_branch_remote(self, remote, remote_branch):
        remote_split = remote.split("/")
        try:
            remote_name = remote_split[0]  # 获取主机名 1）
        except BaseException:
            remote_name = ""  # 没有主机名 1）
        branch_split = remote_branch.split("/")
        if len(branch_split) >= 2 and remote_name == "":
            remote_name = branch_split[0]  # 2)
            remote_branch = "/".join(branch_split[1:])  # 2)
        return subprocess.Popen(
            f"echo 删除远程分支... && {git_path} push {remote_name} :{remote_branch} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def del_tag_remote(self, remote, tag):
        return subprocess.Popen(
            f"echo 删除远程标签... && {git_path} push {remote} :refs/tags/{tag} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )


@plugin_class_loading(get_path(r'template/gitrepo'))
class BackClasses(GitBase, metaclass=ABCMeta):
    def reset(self, head="HEAD~1", reset_type=0):
        if reset_type == 0:
            type_ = "--mixed"  # 退回到工作区
        elif reset_type == 1:
            type_ = "--soft"  # 退回到暂存区
        else:
            type_ = "--hard"  # 退回到暂存区
        return subprocess.Popen(
            f"echo 回退... && {git_path} reset {type_} {head} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def checkout(self, file_list):
        if len(file_list) >= 1:  # 多于一个文件，不用--，空格
            file = self.get_flie_list(file_list, pat=" ")
            return subprocess.Popen(
                f"echo 丢弃修改: && {git_path} checkout {file} && echo {self.make_stop_key()}",
                cwd=self.repo_dir,
                **sys_seeting,
            )
        elif len(file_list) == 1:
            return subprocess.Popen(
                f"echo 丢弃修改: && {git_path} checkout -- {file_list[0]} && echo {self.make_stop_key()}",
                cwd=self.repo_dir,
                **sys_seeting,
            )
        else:
            return subprocess.Popen(
                f"echo 丢弃修改: && {git_path} checkout * && echo {self.make_stop_key()}",
                cwd=self.repo_dir,
                **sys_seeting,
            )

    def apply_stash(self, stash_num="0"):  # 恢复工作区
        return subprocess.Popen(
            f"echo 恢复工作区... && {git_path} stash apply stash@{{{stash_num}}} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def reset_file(self, hard, file_list):  # 注意版本回退是:Reset_File
        file = self.get_flie_list(file_list)
        return subprocess.Popen(
            f"""echo 回退文件... && {git_path} reset {hard} {file} && echo {self.make_stop_key()}""",
            cwd=self.repo_dir,
            **sys_seeting,
        )


@plugin_class_loading(get_path(r'template/gitrepo'))
class ParallelClasses(GitBase, metaclass=ABCMeta):
    def switch_branch(self, branch_name):  # 切换分支
        return subprocess.Popen(
            f"echo 切换分支... && {git_path} switch {branch_name} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def merge_branch(self, branch_name, no_ff, m=""):  # 合并分支
        if no_ff:
            no_ff = f' --no-ff -m "{m}"'  # --no-ff前有空格
        else:
            no_ff = ""
        return subprocess.Popen(
            f"echo 合并分支... && {git_path} merge{no_ff} {branch_name} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def merge_abort(self):  # 退出冲突处理
        return subprocess.Popen(
            f"echo 冲突处理退出... && {git_path} merge --abort && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def rename_branch(self, old_name, new_name):
        return subprocess.Popen(
            f"""echo 回退文件... && {git_path} branch -m {old_name} {new_name} && echo {self.make_stop_key()}""",
            cwd=self.repo_dir,
            **sys_seeting,
        )


@plugin_class_loading(get_path(r'template/gitrepo'))
class RemoteClasses(GitBase, metaclass=ABCMeta):
    def push_tag(self, tag, remote_name):
        return subprocess.Popen(
            f"echo 推送标签... && {git_path} push {remote_name} {tag} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def pull_push(
        self,
        pull_or_push=0,
        remote="",
        remote_branch="",
        local="",
        allow=False,
        u=False,
        f=False,
    ):
        # 处理逻辑
        # 1）remote去斜杠第一个作为主机名字
        # 2) 从remote分离主机名(如果没指定)
        # 3) 如果local为空，用HEAD填充
        # 4) 如果以上后，主机名仍为空，则local和分支均为空

        split = remote.split("/")
        try:
            remote_name = split[0]  # 获取主机名 1）
        except BaseException:
            remote_name = ""  # 没有主机名 1）

        branch_split = remote_branch.split("/")
        if len(branch_split) >= 2 and remote_name == "":
            remote_name = branch_split[0]  # 2)
            remote_branch = "/".join(branch_split[1:])  # 2)
        if local.replace(" ", "") == "":
            local = "HEAD"  # 3)
        if remote_name == "":  # 4)
            branch = ""
        else:
            if pull_or_push == 1:
                # 注意，local不可以为空，也不会为空
                if remote_branch != "":
                    # git push <远程主机名> <本地分支名>:<远程分支名>
                    branch = f"{local}:{remote_branch}"
                else:
                    branch = f"{local}"  # 要去掉冒号
            else:
                if remote_branch != "HEAD":
                    # git push <远程主机名> <本地分支名>:<远程分支名>
                    branch = f"{remote_branch}:{local}"
                else:
                    branch = f"{remote_branch}"

        if allow:
            history = " --allow-unrelated-histories"
        else:
            history = ""
        push_pull = {0: "pull", 1: f"push{' -u' if u else ''}{' -f' if f else ''}"}
        return subprocess.Popen(
            f"""echo 与服务器连接... && {git_path} {push_pull.get(pull_or_push, "pull")}{history} {remote_name} {branch} 
&& echo {self.make_stop_key()}""",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def fetch(self, remote, remote_branch, local):
        # 处理逻辑
        # 1）remote去斜杠第一个作为主机名字
        # 2) 从remote分离主机名(如果没指定)
        # 3) 如果local为空，用HEAD填充
        # 4) 如果以上后，主机名仍为空，则local和分支均为空

        split = remote.split("/")
        try:
            remote_name = split[0]  # 获取主机名 1）
        except BaseException:
            remote_name = ""  # 没有主机名 1）

        branch_split = remote_branch.split("/")
        if len(branch_split) >= 2 and remote_name == "":
            remote_name = branch_split[0]  # 2)
            remote_branch = "/".join(branch_split[1:])  # 2)
        if local.replace(" ", "") == "":
            local = "HEAD"  # 3)
        if remote_name == "":  # 4)
            branch = ""
        else:
            if remote_branch != "HEAD":
                # git push <远程主机名> <本地分支名>:<远程分支名>
                branch = f"{remote_branch}:{local}"
            else:
                branch = f"{remote_branch}"

        return subprocess.Popen(
            f"""echo 更新远程仓库... && {git_path} fetch {remote_name} {branch} && echo {self.make_stop_key()}""",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def clone(self, url):
        return subprocess.Popen(
            f"echo 克隆操作不被允许 && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )


@plugin_class_loading(get_path(r'template/gitrepo'))
class GitRepo(ViewClasses, NewClasses, RemoveClass, BackClasses, ParallelClasses, RemoteClasses):  # git的基类

    def init(self, repo_dir):
        self.url = None
        try:
            if exists(repo_dir + r"/.git"):  # 是否为git 仓库
                pass
            elif repo_dir[-4:] == ".git":
                repo_dir = repo_dir[:-5]  # -5,得把/去掉
            else:
                raise Exception
        except BaseException:
            subprocess.Popen(
                f"{git_path} init", cwd=self.repo_dir, **sys_seeting
            ).wait()
        self.repo_dir = repo_dir  # 仓库地址(末尾不带/)
        self.repo = Repo(repo_dir)  # 读取一个仓库
        self.name = split(repo_dir)[-1]
        self.have_clone = True

    def customize_command(self, command: str):
        return subprocess.Popen(
            f"{command} && echo {self.make_stop_key()}",
            cwd=self.repo_dir,
            **sys_seeting,
        )

    def make_dir(self, dir):
        if len(dir) == "":
            return dir
        if dir[0].startswith(os.sep):
            inside = ""
        else:
            inside = os.sep
        return self.repo_dir + inside + dir


@plugin_class_loading(get_path(r'template/gitrepo'))
class CloneGit(GitRepo):  # Clone一个git
    def init(self, repo_dir, *args, **kwargs):
        self.Repo_Dic = repo_dir  # 仓库地址
        self.url = None
        self.name = split(repo_dir)[-1]
        self.have_clone = False

    def clone(self, url):
        if self.have_clone:
            super(CloneGit, self).clone(url)
        self.have_clone = True
        return subprocess.Popen(
            f"echo 正在克隆... && {git_path} clone {url} {self.Repo_Dic}",
            cwd=split(self.Repo_Dic)[0],
            **sys_seeting,
        )

    def after_clone(self):
        self.repo = Repo(self.Repo_Dic)
