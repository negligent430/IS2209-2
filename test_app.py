import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Runs /health for json
def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200

#Runs homepage
def test_homepage(client):
    response = client.get('/home')
    assert response.status_code == 302 # I have set it to 302 as the testing wont have a session - so it will always be redirected
