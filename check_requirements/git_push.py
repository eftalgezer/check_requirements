"""
Git Push Utility

This module provides a function to create and push changes to a Git repository.

Functions:
    push_reqs_file(file_path, git_repo, push_type, git_remote_url=None): Pushes changes to a Git repository
    after creating or updating a requirements file.
"""

import os
import git


def push_reqs_file(file_path, git_repo, push_type, git_remote_url=None):
    """
    Pushes changes to a Git repository after creating or updating a requirements file.

    This function creates a new branch named "check_requirements" or switches to an existing one.
    It then adds and commits the provided requirements file changes to the branch and pushes it to the Git repository.

    Args:
        file_path (str): Path to the requirements file.
        git_repo (str): URL of the Git repository.
        push_type (str): The type of push operation. Should be 'create' or 'update'.
        git_remote_url (str, optional): URL of the Git remote repository. Defaults to None.

    Returns:
        None

    Raises:
        AttributeError: If an invalid push_type is provided.
    """
    if push_type not in ["create", "update"]:
        raise AttributeError("Wrong push_type. It should be 'create or 'update'")
    repo = git.Repo(os.getcwd())
    repo.create_remote('origin', git_repo)
    if git_remote_url:
        repo.remotes.origin.set_url(git_remote_url)
    try:
        repo.git.checkout("check_requirements")
    except git.exc.GitCommandError:
        repo.git.checkout(b="check_requirements")
    repo.index.add([file_path])
    repo.index.commit(
        f"{push_type.capitalize()} {file_path}",
        author=git.Actor("check_requirements[bot]", "mail@check_requirements.bot")
    )
    origin = repo.remote("origin")
    origin.push(refspec="HEAD:check_requirements")
