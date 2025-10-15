from github.auth import GithubAuthProvider
from settings import Settings

if __name__ == "__main__":
    Settings()

    GithubAuthProvider()

    print("App ID:", Settings().app_id)
    print("Install ID:", Settings().install_id)
