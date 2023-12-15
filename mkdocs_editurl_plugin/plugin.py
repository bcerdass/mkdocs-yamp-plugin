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
        
    # @event_priority(-100)  # Wishing to run this after all other plugins' `on_files` events.
    # def on_page_context(self, context, page, config, nav):
    #     # Logic to set the edit_url
    #     edit_url = f"https://example.com/edit/{page.file.src_path}"
    #     page.edit_url = edit_url
    #     logger.info(f"Set edit URL for page {page.file.src_path} to {edit_url}")
    #     return context

    @event_priority(-100)  # Wishing to run this after all other plugins' `on_files` events.
    def on_page_context(self, context, page, config, nav):
        # edit_url = 'https://example.com'
        # for repo in self.repo_config['repositories']:
        #     repo_name = repo['name']
        #     if page.file.src_path.startswith(os.path.join('repos', repo_name)):
                
        #         edit_url = f"https://example.com/edit/{page.file.src_path}"
        #         logger.info(f"1. Set edit URL for page {page.file.src_path} to {edit_url}") 
        #         break
        #     #     return context
        #     #     logger.info(f"this should not be printed")
        #     # else:
        #     #     return context
        # logger.info(f"2. Set edit URL for page {page.file.src_path} to {edit_url}")  
        #test = self.build_edit_url(page)
        #logger.info(f"current page {page.edit_url} to {test}")
        page.edit_url = self.build_edit_url(page)
        #repo_url = config.get('repo_url')+"this is a test"
        config['repo_url'] = self.get_repo_url(page)
        #logger.info(f"this is the repo url {repo_url}")
        # with open('output.txt', 'w') as file:
        #     #pprint.pprint(my_object, stream=file)
        #     pprint.pprint(context, stream=file)

        return context
        # logger.info(f"2 Set edit åURL for page {page.file.src_path} to {edit_url}")
        # page.edit_url = edit_url
        
    def get_repo_url(self, page):
        #logger.info(f"current page {page.edit_url} source {page.file.src_path}")
        filtered = [
            repo for repo in self.repo_config['repositories']
                if page.file.src_path.startswith(os.path.join('repos', repo['name'])) or page.file.src_path.startswith(os.path.join(repo['name']))
        ]
        if len(filtered) > 0:
            repo = filtered[0]
            return repo['url']       

    def build_edit_url(self, page):
        #logger.info(f"current page {page.edit_url} source {page.file.src_path}")
        filtered = [
            repo for repo in self.repo_config['repositories']
                if page.file.src_path.startswith(os.path.join('repos', repo['name'])) or page.file.src_path.startswith(os.path.join(repo['name']))
        ]
        if len(filtered) > 0:
            #base_url = ''
            repo= filtered[0]
            #filtered[0].set_edit_url(page, self.config.temp_dir)
            base_url = repo['url']
            branch = repo.get('branch', 'main')
            file_path = page.file.src_path.replace(repo['name'] + '/', 'docs/')
            edit_url = f"{base_url}/edit/{branch}/{file_path}"
            #logger.info(f"Set edit URL for page {page.file.src_path} to {edit_url}")
            #edit_url = 'https://example.com'
            #logger.info(f"base_url {base_url}")
            return edit_url
            

        # for repo in self.repo_config['repositories']:
        #     repo_name = repo['name']
        #     if page.file.src_path.startswith(os.path.join('repos', repo_name)):
        #         base_url = repo['url']
        #         branch = repo.get('branch', 'main')
        #         file_path = page.file.src_path.replace(os.path.join('docs', 'repos', repo['name']) + '/', '')
        #         edit_url = f"{base_url}/edit/{branch}/{file_path}"
        #         logger.info(f"Set edit URL for page {page.file.src_path} to {edit_url}")
        #         edit_url = 'https://example.com'
        #         logger.info(f"should return {page.file.src_path} to {edit_url}")
        #         return edit_url        
        