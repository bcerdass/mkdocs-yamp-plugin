# mkdocs_editurl_plugin/plugin.py

from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
import logging
import json
import os
import pprint

logger = logging.getLogger('mkdocs.plugins')

class EditUrlPlugin(BasePlugin):
    
    def on_config(self, config):
        config_file_path = config['extra']['repo_config_path']
        with open(config_file_path, 'r') as file:
            self.repo_config = json.load(file)
        return config
        

    @event_priority(-100)  # Wishing to run this after all other plugins' `on_files` events.
    def on_page_context(self, context, page, config, nav):
        page.edit_url = self.build_edit_url(page)
        config['repo_url'] = self.get_repo_url(page)


        return context

        
    def get_repo_url(self, page):
        filtered = [
            repo for repo in self.repo_config['repositories']
                if page.file.src_path.startswith(os.path.join('repos', repo['name'])) or page.file.src_path.startswith(os.path.join(repo['name']))
        ]
        if len(filtered) > 0:
            repo = filtered[0]
            return repo['url']       

    def build_edit_url(self, page):
        filtered = [
            repo for repo in self.repo_config['repositories']
                if page.file.src_path.startswith(os.path.join('repos', repo['name'])) or page.file.src_path.startswith(os.path.join(repo['name']))
        ]
        if len(filtered) > 0:
            repo= filtered[0]
            base_url = repo['url']
            branch = repo.get('branch', 'main')
            file_path = page.file.src_path.replace(repo['name'] + '/', 'docs/')
            edit_url = f"{base_url}/edit/{branch}/{file_path}"

            return edit_url
            
