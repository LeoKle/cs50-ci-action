import requests

from settings import Settings


class GitHubPRCommenter:
    def __init__(self, token, username=None):
        """
        Initialize the commenter using environment and Settings.
        If there is no repo or PR context, commenting will be disabled.
        """
        self.settings = Settings()
        self.token = token
        self.disabled = False

        if not self.settings.github_repo or not self.settings.pr_number:
            print(
                "💤 No PR context detected (missing GITHUB_REPOSITORY or PR number) "
                "— commenting disabled."
            )
            self.disabled = True
            return

        self.repo_owner, self.repo_name = self.settings.github_repo.split("/")
        self.pr_number = self.settings.pr_number
        self.api_base = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    def _get_existing_comment(self):
        """
        Find an existing comment on this PR created by this GitHub App.
        """
        if self.disabled:
            return None

        comments_url = f"{self.api_base}/issues/{self.pr_number}/comments"
        response = requests.get(comments_url, headers=self.headers)
        response.raise_for_status()
        comments = response.json()

        for comment in comments:
            app_info = comment.get("performed_via_github_app")
            if app_info and app_info.get("id") == self.settings.app_id:
                return comment

        return None

    def post_comment(self, body):
        """
        Create or update a comment on the PR, unless commenting is disabled.
        """

        existing_comment = self._get_existing_comment()
        comments_url = f"{self.api_base}/issues/{self.pr_number}/comments"
        body = body.strip()

        if existing_comment:
            comment_id = existing_comment["id"]
            print(f"📝 Updating existing comment (id={comment_id})...")
            response = requests.patch(
                f"{self.api_base}/issues/comments/{comment_id}",
                headers=self.headers,
                json={"body": body},
            )
            response.raise_for_status()
        else:
            print("💬 Creating new PR comment...")
            response = requests.post(
                comments_url,
                headers=self.headers,
                json={"body": body},
            )
            response.raise_for_status()

        print("✅ Comment posted/updated successfully.")
