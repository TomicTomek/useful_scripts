#!/usr/bin/python3
from git import Repo
import xml.etree.ElementTree as ET
from sys import exit


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
    def __init__(self, path, revision):
        self.path = path
        self.revision = revision
    def __str__(self):
        return "patch: " + self.path + "\trevision: " + self.revision

# parse projects from manifest
manifest_path = ".repo/manifests/enplug.xml"
root = ET.parse(manifest_path).getroot()


projects_list = []
projects_list.append(Project(".repo/manifests", "default"))

for type_tag in root.findall('project'):
    path = type_tag.get('path')
    revision = type_tag.get('revision')
    projects_list.append(Project(path, revision))

#for aaaa in projects_list:
#    print(aaaa)
#exit()

def is_repo_dirty(repo_path):
    repo = Repo(repo_path)
    return repo.is_dirty(index=True, working_tree=True, untracked_files=True)

    
def print_untracked_files(repo_path):
    repo = Repo(repo_path)
    has_untracked = repo.is_dirty(index=False, working_tree=False, untracked_files=True)
    if has_untracked:
        for untracked_file_path in repo.untracked_files:
            print(bcolors.YELLOW + "\t" +untracked_file_path + bcolors.ENDC)


def print_modified_files(repo_path):
    repo = Repo(repo_path)
    has_modified = repo.is_dirty(index=False, working_tree=True, untracked_files=False)
    if has_modified:
        for modified_file_path in repo.index.diff(None):
            print(bcolors.RED, "\t", modified_file_path.a_path, bcolors.ENDC)


def print_stagged_files(repo_path):
    repo = Repo(repo_path)
    has_indexed = repo.is_dirty(index=True, working_tree=False, untracked_files=False)
    if has_indexed:
        for indexed_file_path in repo.index.diff(repo.head.commit):
            print(bcolors.BLUE, "\t", indexed_file_path.a_path, bcolors.ENDC)


clean_repo_paths = []
dirty_repo_paths = []
for project in projects_list:
    if is_repo_dirty(project.path):
        dirty_repo_paths.append(project.path)
    else:
        clean_repo_paths.append(project.path)


print(bcolors.GREEN + "CLEAN repos" + bcolors.ENDC)
for repository_path in clean_repo_paths:
    print(repository_path + "/")

    
print(bcolors.DARK_PURPLE + "\nDIRTY repos" + bcolors.ENDC)
for repository_path in dirty_repo_paths:
    print(repository_path + "/")
    print_untracked_files(repository_path)
    print_modified_files(repository_path)
    print_stagged_files(repository_path)
    


