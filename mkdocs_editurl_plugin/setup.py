# setup.py

from setuptools import setup, find_packages

setup(
    name='mkdocs-editurl-plugin',
    version='0.1.0',
    description='A MkDocs plugin to customize edit URLs',
    long_description='A longer description of your plugin',
    keywords='mkdocs python markdown',
    url='https://example.com/your-plugin-homepage',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=1.0'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'editurl = mkdocs_editurl_plugin.plugin:EditUrlPlugin'
        ]
    }
)
