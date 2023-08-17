"""
GitHub Pull Request Utility

This module provides a function to create a pull request on GitHub using PyGithub.

Functions:
    gh_pull_req_for_reqs_file(
        github_token,
        repo_name,
        base_branch,
        push_type,
        missing_pkgs=None,
        extra_pkgs=None,
        sys_info=None
    ):
        Creates a pull request on GitHub to update a requirements file, highlighting missing or extra packages.

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
    Creates a pull request on GitHub using PyGithub.

    This function creates a pull request on the specified GitHub repository.
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
    if not any([missing_pkgs, extra_pkgs]):
        raise AttributeError("At least one of 'missing_pkgs' or 'extra_pkgs' should be given")
    sys_string = " ".join(f"{key} = {val}" for key, val in sys_info) if sys_info else None
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
    pull = repo.create_pull(
        title=f"{push_type.capitalize()} requirements file{f' for {sys_string}' if sys_string else ''}",
        body=body,
        base=base_branch,
        head="check_requirements"
    )
    print(f"Pull request created successfully: {pull.html_url}")
