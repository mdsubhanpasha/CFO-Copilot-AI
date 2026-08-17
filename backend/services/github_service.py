from github import Github
import os

def fetch_pr_diff(repo_name: str, pr_number: int) -> str:
    """
    Fetches the patch/diff of a pull request from a given GitHub repository.
    """
    github_token = os.environ.get("GITHUB_TOKEN")

    try:
        if github_token:
            g = Github(github_token)
        else:
            g = Github() # Without token, limits apply

        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        # We can't directly get the unified diff using PyGithub easily without using the requests library.
        # Alternatively, we can construct the files and their patch.
        diff_str = ""
        for file in pr.get_files():
            diff_str += f"File: {file.filename}\n"
            diff_str += f"{file.patch}\n\n"

        return diff_str
    except Exception as e:
        print(f"Error fetching PR diff: {e}")
        return f"Error fetching PR diff: {str(e)}"
