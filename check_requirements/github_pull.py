"""
GitHub Pull Request Utility

This module provides a function to create a pull request on GitHub using PyGithub.

Functions: gh_pull_req_for_reqs_file( github_token, repo_name, base_branch, push_type, missing_pkgs=None,
extra_pkgs=None, sys_info=None ): Creates or updates a pull request on GitHub to update a requirements file,
highlighting missing or extra packages.

"""

from github import Github


def gh_pull_req_for_reqs_file(
        github_token,
        repo_name,
        base_branch,
        push_type,
        missing_pkgs=None,
        extra_pkgs=None,
        sys_info=None
):
    """
    Creates or updates a pull request on GitHub using PyGithub.

    This function creates a new pull request or updates an existing one on the specified GitHub repository.
    The pull request title and body are generated based on the provided information.

    Args:
        github_token (str): Personal access token for authenticating with GitHub.
        repo_name (str): The name of the GitHub repository (e.g., "owner/repository").
        base_branch (str): The base branch of the pull request.
        push_type (str): The type of push operation. Should be 'create' or 'update'.
        missing_pkgs (list, optional): A list of missing packages to be included in the pull request body.
        extra_pkgs (list, optional): A list of extra packages to be included in the pull request body.
        sys_info (list of tuples, optional): System information to be included in the pull request title.

    Returns:
        None

    Raises:
        AttributeError: If an invalid push_type is provided or neither missing_pkgs nor extra_pkgs is given.
    """
    if push_type not in ["create", "update"]:
        raise AttributeError("Wrong push_type. It should be 'create or 'update'")
    sys_string = " ".join(f"{key} = {val}" for key, val in sys_info) if sys_info else None
    title = f"{push_type.capitalize()} requirements file{f' for {sys_string}' if sys_string else ''}"
    body = "" \
        if push_type == "create" \
        else \
        (
            "Missing packages:\n" if missing_pkgs else "" +
            (
                f"{pkg['name']}"
                f" @ {pkg.get('at')}" if pkg.get('at') else ""
                f" == {pkg.get('version')}" if pkg.get('version') else ""
                "\n"
            ) for pkg in missing_pkgs if missing_pkgs
            (
                "Extra packages:\n" if extra_pkgs else "" +
                (
                    f"{pkg['name']}"
                    f" @ {pkg.get('at')}" if pkg.get('at') else ""
                    f" == {pkg.get('version')}" if pkg.get('version') else ""
                    "\n"
                ) for pkg in extra_pkgs if extra_pkgs
            )
        )
    gh = Github(github_token)
    repo = gh.get_repo(repo_name)
    existing_pull = next(
        (pull for pull in repo.get_pulls(base=base_branch, head="check_requirements") if pull.title == title),
        None
    )
    if existing_pull:
        if existing_pull.body == body:
            existing_pull.edit(body=body)
            print(f"Pull request updated successfully: {existing_pull.html_url}")
        else:
            print("Pull request with the same title and body already exists. No action taken.")
    else:
        pull = repo.create_pull(title=title, body=body, base=base_branch, head="check_requirements")
        print(f"Pull request created successfully: {pull.html_url}")
