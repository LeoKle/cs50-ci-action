from github.auth import GithubAuthProvider
from github.cloner import GithubRepoCloner
from settings import Settings

if __name__ == "__main__":
    Settings()

    gh_token = GithubAuthProvider().get_token()

    problems_repo = GithubRepoCloner(
        token=gh_token, repository=Settings().problems_repo, branch=Settings().problems_branch
    )
    solutions_repo = GithubRepoCloner(
        token=gh_token, repository=Settings().solutions_repo, branch=Settings().solutions_branch
    )
