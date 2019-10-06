from app import create_app

app = create_app()
HOST = app.config.get('HOST')
DEBUG = app.config.get('DEBUG')


if __name__ == "__main__":
    app.run(host=HOST, debug=DEBUG)
        