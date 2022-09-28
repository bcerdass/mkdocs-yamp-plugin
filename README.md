# Yet Another Multirepo Plugin

This plugin allows users to define external repositories for integration into the MkDocs site.

Declared repositories are added to a subdirectory within your docs directory.

Users can then reference files within those repositories from their own navigation.

## Config

```yaml
plugins:
  - yamp:
    # directory within docs dir to add content
    temp_dir: "repos"
    # delete docs/{temp_dir} after build||serve?
    #  default: true
    cleanup: true
    # delete docs/{temp_dir} at the beginning of the
    # mkdocs invocation.
    start_fresh: true
    # declare a list of repositories or directories to add
    # to docs/{temp_dir}
    #   default: []
    repos:
      # the git repository URL to clone
    - url: "https://github.com/some-user/some-repo"
      # a list of globs to checkout
      # if empty or not provided, the entire repository is cloned
      # default: [ ]
      include: [ "README.md", "docs/index.md"]
      # the branch of the repository to clone
      branch: "main"

      # alternatively, you can provide a path.
      # a symlink will be created within docs/{temp_dir}
    - path: "../some-other-directory"
```
