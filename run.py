import argparse
from app import create_app
from app.utils import clean_data

app = create_app()
HOST = app.config.get('HOST')
DEBUG = app.config.get('DEBUG')


parser = argparse.ArgumentParser()
parser.add_argument('--action', type=str, default='run', help='Output dir for image')

if __name__ == "__main__":
    args = parser.parse_args()
    action = args.action
    if action == 'run':
        app.run(host=HOST, debug=DEBUG)
    elif action == 'clean':
        clean_data()
        