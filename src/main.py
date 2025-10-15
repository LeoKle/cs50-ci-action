from github.auth import GithubAuthProvider
from github.cloner import GithubRepoCloner
from github.commenter import GitHubPRCommenter
from settings import Settings
from testing.problem import ProblemTester
from utils.markdown import build_results_markdown

if __name__ == "__main__":
    Settings()

    gh_token = GithubAuthProvider().get_token()

    problems_repo = GithubRepoCloner(
        token=gh_token, repository=Settings().problems_repo, branch=Settings().problems_branch
    )
    solutions_repo = GithubRepoCloner(
        token=gh_token, repository=Settings().solutions_repo, branch=Settings().solutions_branch
    )

    problem_tester = ProblemTester(problems_repo.get_repo_dir(), solutions_repo.get_repo_dir())

    problem_tester.test_problems()

    results = problem_tester.results
    results = sorted(results, key=lambda r: (r.problem_name or "", r.solution_name or ""))
    passed = sum(1 for r in results if r.status == "ok")
    failed = sum(1 for r in results if r.status == "fail")
    warns = sum(1 for r in results if r.status == "warning")
    total = len(results)

    print(f"\nTest Summary: {total} total")
    print(f"✅\tPassed: {passed}")
    print(f"🔴\tFailed: {failed}")
    print(f"⚠️\tWarnings: {warns}")

    markdown = build_results_markdown(results)

    commenter = GitHubPRCommenter(token=gh_token)

    commenter.post_comment(markdown)
