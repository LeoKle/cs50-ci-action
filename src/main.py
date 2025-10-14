import sys

from settings import Settings

if __name__ == "__main__":
    args = {
        "app_id": sys.argv[1],
        "install_id": sys.argv[2],
        "private_key": sys.argv[3],
        "problems_repo": sys.argv[4],
        "solutions_repo": sys.argv[5],
    }

    Settings(**args)

    print("App ID:", Settings().app_id)
    print("Install ID:", Settings().install_id)
