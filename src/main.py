from settings import Settings

if __name__ == "__main__":
    Settings()

    print("App ID:", Settings().app_id)
    print("Install ID:", Settings().install_id)
