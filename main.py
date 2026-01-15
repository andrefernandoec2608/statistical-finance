from api import ApiConnection
from app_state import AppState

def main():
    app_state = AppState()
    api_connection = ApiConnection(app_state)
    api_connection.run_app()

if __name__ == "__main__":
    main()