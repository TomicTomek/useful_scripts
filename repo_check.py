#!/usr/bin/python3
from git import Repo
import xml.etree.ElementTree as ET
import sys


class bcolors:
    DARK_PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Project:
    def __init__(self, project_path, project_revision):
        self.path = project_path
        self.revision = project_revision

    def __str__(self):
        return "patch: " + self.path + "\trevision: " + self.revision


# parse projects from manifest
manifest_path = ".repo/manifests/enplug.xml"
root = ET.parse(manifest_path).getroot()

projects_list = [Project(".repo/manifests", "default")]

for type_tag in root.findall('project'):
    path = type_tag.get('path')
    revision = type_tag.get('revision')
    projects_list.append(Project(path, revision))


def is_repo_dirty(repo_path):
    repo = Repo(repo_path)
    return repo.is_dirty(index=True, working_tree=True, untracked_files=True)


def print_untracked_files(repo_path):
    repo = Repo(repo_path)
    has_untracked = repo.is_dirty(index=False, working_tree=False, untracked_files=True)
    if has_untracked:
        for untracked_file_path in repo.untracked_files:
            print(bcolors.YELLOW + "\t[u] " + untracked_file_path + bcolors.ENDC)


def print_modified_files(repo_path):
    repo = Repo(repo_path)
    has_modified = repo.is_dirty(index=False, working_tree=True, untracked_files=False)
    if has_modified:
        for modified_file_path in repo.index.diff(None):
            print(bcolors.RED + "\t[m] " + modified_file_path.a_path + bcolors.ENDC)


def print_stagged_files(repo_path):
    repo = Repo(repo_path)
    has_indexed = repo.is_dirty(index=True, working_tree=False, untracked_files=False)
    if has_indexed:
        for indexed_file_path in repo.index.diff(repo.head.commit):
            print(bcolors.BLUE + "\t[i] " + indexed_file_path.a_path + bcolors.ENDC)


def check_repositories_local_state():
    global project
    clean_repo_paths = []
    dirty_repo_paths = []
    for project in projects_list:
        if is_repo_dirty(project.path):
            dirty_repo_paths.append(project.path)
        else:
            clean_repo_paths.append(project.path)
    print(bcolors.GREEN + "\nCLEAN repos" + bcolors.ENDC)
    for repository_path in clean_repo_paths:
        print(repository_path + "/")
    print(bcolors.DARK_PURPLE + "\nDIRTY repos" + bcolors.ENDC)
    for repository_path in dirty_repo_paths:
        print(repository_path + "/")
        print_untracked_files(repository_path)
        print_modified_files(repository_path)
        print_stagged_files(repository_path)


def print_help():
    print("Mini help:")
    print("\t" + sys.argv[0] + " r\n\tRun script with remote mode - will compare to remotes.")
    print("\t" + sys.argv[0] + " rf\n\tRun script with remote mode force - will fetch changes from server "
                               "and compare to remote branches.")


# remote compare START
def is_branch_present_on_remote(remote, branch_name):
    is_present = False
    try:
        remote.refs[branch_name]
        is_present = True
    except (AttributeError, IndexError):
        is_present = False
    return is_present


def local_and_remote_are_at_same_commit(repo, remote_name, branch_name, local_hexsha=None):
    if branch_name is None and local_hexsha is None:
        raise InputError("branch_name and commit_hexsha are None")

    remote = repo.remotes[remote_name]

    if branch_name is None:
        # iterate by all branches
        for remote_branch_ref in remote.refs:
            if local_hexsha == remote_branch_ref.commit.hexsha:
                return True
        return False

    if local_hexsha is None:
        local_commit = repo.heads[branch_name].commit
        local_hexsha = local_commit.hexsha

    remote_commit = remote.refs[branch_name].commit
    return local_hexsha == remote_commit.hexsha


def is_remote_and_local_same(repo_project, force_fetch=False):
    repo = Repo(repo_project.path)
    if force_fetch:
        print("Fetching remote for project ", repo_project.path, "...")
    remote_name = 'enplug'

    try:
        repo.remotes[remote_name]  # just to check if raise error
    except (AttributeError, IndexError):
        remote_name = 'origin'

    if force_fetch:
        repo.remotes[remote_name].fetch()

    if repo.head.is_detached:
        return local_and_remote_are_at_same_commit(repo, remote_name, None, repo.head.commit.hexsha)
    else:
        local_head_name = repo.head.reference.name
        remote = repo.remotes[remote_name]
        if is_branch_present_on_remote(remote, local_head_name):
            return local_and_remote_are_at_same_commit(repo, remote_name, local_head_name)
    return False


# remote compare END
############################################################################################
mode = "default"
if len(sys.argv) > 1:
    mode = str(sys.argv[1])

if len(sys.argv) > 1 and not (mode in ["r", "rf"]):
    print_help()
    sys.exit()

check_repositories_local_state()

if mode in ["r", "rf"]:
    print(bcolors.DARK_PURPLE + "\nRemote mode - compare local to remote" + bcolors.ENDC)
    for project in projects_list:
        if is_remote_and_local_same(project, mode == "rf"):
            print(bcolors.GREEN + project.path + "/" + bcolors.ENDC)
        else:
            print(bcolors.RED + project.path + "/" + bcolors.ENDC)

print("\n")
