# -*- coding: <encoding name> -*-

from gitrepo.template import GitRepo, CloneGit


class GitCtrol:
    def __init__(self):
        self.git_dict = {}  # 名字-文件位置
        self.git_type_dict = {}  # 名字-类型

    def open_repo(self, repo_dir, **kwargs):
        git = GitRepo(repo_dir)
        self.git_dict[git.name] = git
        self.git_type_dict[git.name] = "init"
        return git.name

    def clone_repo(self, repo_dir, **kwargs):
        git = CloneGit(repo_dir)
        self.git_dict[git.name] = git
        self.git_type_dict[git.name] = "clone"
        return git.name

    def get_git(self, name):
        return self.git_dict[name]

    def get_git_dict(self):
        return self.git_dict.copy()

    def get_dir(self, name):
        return self.get_git(name).dir_list()

    def add_file(self, name, file_list):
        return self.get_git(name).add(file_list)

    def del_cached_file(self, name, file_list):
        return self.get_git(name).del_cached_file(file_list)  # 移除出去暂存区

    def commit_file(self, name, message):
        return self.get_git(name).commit_file(message)

    def log(self, name, graph, pretty, abbrev):
        return self.get_git(name).log(graph, pretty, abbrev)

    def do_log(self, name):
        return self.get_git(name).do_log()

    def status(self, name):
        return self.get_git(name).status()

    def diff_file(self, name, brach):
        return self.get_git(name).diff(brach)

    def back_version(self, name, head, reset_type=0):
        return self.get_git(name).reset(head, reset_type)  # 版本回退HEAD

    def back_version_file(self, name, head, file_list):
        return self.get_git(name).reset_file(head, file_list)  # 文件回退

    def checkout_version(self, name, file):
        return self.get_git(name).checkout(file)  # 弹出

    def rm(self, name, file):
        return self.get_git(name).rm(file)

    def branch_view(self, name):
        return self.get_git(name).branch_view()

    def new_branch(self, name, new_branch, origin):
        return self.get_git(name).new_branch(new_branch, origin)

    def switch_branch(self, name, branch_name):
        return self.get_git(name).switch_branch(branch_name)

    def del_branch(self, name, branch_name, type_):
        d = {1: "d", 0: "D"}.get(type_, "d")
        return self.get_git(name).del_branch(branch_name, d)

    def merge_branch(self, name, branch_name, no_ff, m):
        return self.get_git(name).merge_branch(branch_name, no_ff, m)

    def merge_abort(self, name):
        return self.get_git(name).merge_abort()

    def save_stash(self, name):
        return self.get_git(name).save_stash()

    def stash_list(self, name):
        return self.get_git(name).get_stash_list()

    def apply_stash(self, name, stash_num="0"):
        return self.get_git(name).apply_stash(stash_num)

    def drop_stash(self, name, stash_num="0"):
        return self.get_git(name).drop_stash(stash_num)

    def cherry_pick(self, name, commit):
        return self.get_git(name).cherry_pick(commit)

    def del_remote(self, name, remote_name):
        return self.get_git(name).del_remote(remote_name)

    def remote_add(self, name, remote, remote_name):
        return self.get_git(name).remote_add(remote, remote_name)

    def bind_branch(self, name, local_name, remote_name):
        return self.get_git(name).bind_branch(local_name, remote_name)

    def pull_from_remote(
        self, name, local_name, remote_name, remote_branch, allow=False, u=False
    ):
        return self.get_git(name).pull_push(
            0, remote_name, remote_branch, local_name, allow, u, False
        )

    def push_to_remote(
        self, name, local_name, remote_name, remote_branch, u=False, f=False
    ):
        return self.get_git(name).pull_push(
            1, remote_name, remote_branch, local_name, False, u, f
        )  # push没有allow选项

    def tag(self, name, condition=""):
        return self.get_git(name).get_tag_list(condition)  # push没有allow选项

    def show_new(self, name, condition):
        return self.get_git(name).search_commit(condition)  # push没有allow选项

    def add_tag(self, name, tag, commit, message=""):
        return self.get_git(name).add_tag(tag, commit, message)  # push没有allow选项

    def push_tag(self, name, tag, remoto):
        return self.get_git(name).push_tag(tag, remoto)

    def push_all_tag(self, name, remoto):
        return self.get_git(name).push_tag("--tags", remoto)

    def del_tag_remote(self, name, remote, tag):
        return self.get_git(name).del_tag_remote(remote, tag)

    def del_branch_remote(self, name, remote, remote_branch):
        return self.get_git(name).del_branch_remote(remote, remote_branch)

    def del_tag(self, name, tag):
        return self.get_git(name).del_tag(tag)

    def fetch(self, name, local_name, remote_name, remote_branch):
        return self.get_git(name).fetch(remote_name, remote_branch, local_name)

    def customize_command(self, name, command: str):
        return self.get_git(name).customize_command(command)

    def clone(self, name, url):
        return self.get_git(name).clone(url)

    def after_clone(self, name):
        try:
            return self.get_git(name).after_clone()
        except BaseException:
            return None

    def make_dir(self, name, dir):
        return self.get_git(name).make_dir(dir)

    def rename_branch(self, name, old_name, new_name):
        return self.get_git(name).rename_branch(old_name, new_name)
