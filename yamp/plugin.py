import os
import yaml
from mkdocs.plugins import BasePlugin
from .repo_item import RepoItem

class YAMP(BasePlugin):
    def __init__(self):
        self.repos = []

    def on_config(self, config):
        # Load repository information from repos.yaml
        repos_config_path = os.path.join(config['docs_dir'], 'repos.yaml')
        if os.path.exists(repos_config_path):
            with open(repos_config_path, 'r') as file:
                repos_config = yaml.safe_load(file)
                self.repos = [RepoItem(repo) for repo in repos_config.get('repos', [])]

        for repo in self.repos:
            repo.clone_repo(config['docs_dir'])

        return config
