import os
import tempfile
import pytest
from app.models import db
from app import create_app

@pytest.fixture(scope='session')
def app():
    #app.config['TESTING'] = True
    app = create_app()
    test_db, app.config['TEST_DATABASE'] = tempfile.mkstemp()

    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app
    with app.app_context():
        db.drop_all()

    os.close(test_db)
    os.unlink(app.config['TEST_DATABASE'])



@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture    
def base_url(app):
    return 'http://' + app.config.get('HOST') + ":" + app.config.get('PORT')
    
@pytest.fixture
def post_url(base_url):
    return  base_url + "/api"

@pytest.fixture
def redirect_url(base_url):
    return   base_url+ "/api"
