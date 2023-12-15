from setuptools import setup, find_packages

setup(
    name='my_mkdocs_plugin',
    version='0.1.0',
    description='A custom MKDocs plugin to clone repositories.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'mkdocs',
        'gitpython'
    ],
    entry_points={
        'mkdocs.plugins': [
            'my_mkdocs_plugin = my_mkdocs_plugin:MyCustomPlugin',
        ]
    }
)
