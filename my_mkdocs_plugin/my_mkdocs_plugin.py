from mkdocs.plugins import BasePlugin
import git
import os
import json

class MyCustomPlugin(BasePlugin):

    def on_config(self, config):
        try:
            config_file_path = config['extra']['repo_config_path']
        except KeyError:
            raise KeyError("The 'repo_config_path' was not found in the 'extra' section of your mkdocs.yml file.")

        with open(config_file_path, 'r') as file:
            repo_config = json.load(file)

        for repo in repo_config['repositories']:
            url = repo['url']
            branch = repo.get('branch', 'main')
            requires_auth = repo.get('requires_auth', False)
            #target_dir = os.path.join('docs', 'repos', repo['name'])
            target_dir = os.path.join('docs', 'repos', repo['name'])

            # Modify the URL for repositories requiring authentication
            if requires_auth:
                git_username = os.environ.get('GIT_USERNAME')
                git_password = os.environ.get('GIT_PASSWORD')
                if git_username and git_password:
                    # Update the URL to include credentials
                    url = url.replace('https://', f'https://{git_username}:{git_password}@')
                else:
                    raise EnvironmentError("Git username/password not set in environment variables.")

            # Clone or pull the repository
            try:
                if not os.path.isdir(target_dir):
                    git.Repo.clone_from(url, target_dir, branch=branch)
                else:
                    repo = git.Repo(target_dir)
                    repo.git.pull('origin', branch)
            except Exception as e:
                print(f"Error processing repository {url}: {e}")

        return config
