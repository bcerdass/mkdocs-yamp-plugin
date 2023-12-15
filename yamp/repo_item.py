import os
import git
from mkdocs.exceptions import PluginError

class RepoItem:
    def __init__(self, repo_dict):
        self.url = repo_dict['url']
        self.branch = repo_dict.get('branch', 'main')
        self.auth_required = repo_dict.get('auth_required', False)

    def clone_repo(self, base_dir):
        repo_name = self.url.split("/")[-1].replace('.git', '')
        repo_path = os.path.join(base_dir, 'repos', repo_name)

        if self.auth_required:
            git_username = os.environ.get('GIT_USERNAME')
            git_password = os.environ.get('GIT_PASSWORD')
            if not git_username or not git_password:
                raise PluginError("Authentication required but no credentials provided")
            self.url = self.url.replace("https://", f"https://{git_username}:{git_password}@")

        if not os.path.exists(repo_path):
            git.Repo.clone_from(self.url, repo_path, branch=self.branch)
