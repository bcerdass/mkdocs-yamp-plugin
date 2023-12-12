"""
Copyright 2022 Booz Allen Hamilton
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import shutil
import logging
import git
import yaml
import os

from mkdocs.plugins import BasePlugin
from mkdocs.config.base import Config
from mkdocs.config import config_options as c
from mkdocs.utils import warning_filter
from pprint import pprint

from .repo_item import RepoItem

log = logging.getLogger("mkdocs.plugins." + __name__)
log.addFilter(warning_filter)

class YAMPConfig(Config):
    """defines the plugin configuration"""
    # determines whether the generated `temp_dir` should be
    # deleted after the mkdocs invocation
    cleanup = c.Type(bool, default=True)

    # determines whether the `temp_dir` should be deleted
    # if it exists as the start of the mkdocs invocation
    start_fresh = c.Type(bool, default=True)

    # the local path within the docs directory where
    # repositories should be cloned
    temp_dir = c.Type(str, default="repos")

    # the list of repositories to clone
    repos = c.ListOfItems(c.SubConfig(RepoItem), default = [])


class YAMP(BasePlugin[YAMPConfig]):
    """Aggregates repositories defined by users in the mkdocs.yaml"""

    first_build = True
    # the actual Directory defined by self.config.temp_dir
    _temp_dir = None

    def __init__(self):
        self.enabled = True

    # registers the plugin to persist a common
    # instance across builds during mkdocs serve
    def on_startup(self, command, dirty):
        """
        registers this plugin instance to persist across builds during mkdocs serve
        """

    # validates the repo configurations


    def update_nav_paths(self, nav, repo_name):
        """Update nav paths and integrate into a designated category."""
        def update_path(item):
            if isinstance(item, dict):
                return {key: update_path(value) for key, value in item.items()}
            elif isinstance(item, list):
                return [update_path(subitem) for subitem in item]
            else:
                return f'repos/{repo_name}/docs/{item}'

        return [update_path(item) for item in nav]


    def on_config(self, config):
        """Validates the repo configurations and merges nav sections from external mkdocs.yml."""

        new_nav_section = "Repositories"
        new_nav_content = []

        for repo in self.config.repos:
            try:
                repo.do_validation()
                # Logic to fetch and parse external mkdocs.yml
                # Assume external_config is the parsed external mkdocs.yml
                
                external_mkdocs_path = os.path.join('docs/repos',repo.repo_name, 'mkdocs.yml') # Update repo_path accordingly
                if os.path.exists(external_mkdocs_path):
                    with open(external_mkdocs_path, 'r') as file:
                        external_config = yaml.safe_load(file)

                    if 'nav' in external_config:
                        updated_nav = self.update_nav_paths(external_config['nav'], repo.repo_name)
                        new_nav_content.append({repo.repo_name: updated_nav})

            except Exception as e:
                log.warning('Misconfigured repo: %s, Error: %s', repo, str(e))
                raise

        if new_nav_content:
            config['nav'].append({new_nav_section: new_nav_content})
        with open('output.txt', 'w') as file:
            pprint(vars(config), stream=file)
        return config


    def on_pre_build(self, config):
        """aggregates documentation"""
        # the actual directory where we'll add the repositories
        self._temp_dir = os.path.join(config.docs_dir, self.config.temp_dir)

        # wipe temp_dir on first build
        if self.first_build and self.config.start_fresh:
            self.cleanup()

        # create repos directory if it doesn't exist
        if not os.path.exists(self._temp_dir):
            os.makedirs(self._temp_dir)
        for repo in self.config.repos:
            repo.fetch(self._temp_dir, self.first_build)

        self.first_build = False

    def on_pre_page(self, page, config, files):
        """
        Change the page's edit URL if the page came from one of the defined repositories
        """
        path = page.file.src_path
        filtered = [
            repo for repo in self.config.repos
                if path.startswith(f'{self.config.temp_dir}/{repo.repo_name}')
        ]
        if len(filtered) > 0:
            filtered[0].set_edit_url(page, self.config.temp_dir)

    def cleanup(self):
        """deletes the temporary directory where repos are aggregated"""
        if self.config.cleanup and os.path.exists(self._temp_dir):
            git.rmtree(self._temp_dir)

    def on_shutdown(self):
        """cleanup at the end of the mkdocs invocation"""
        self.cleanup()
