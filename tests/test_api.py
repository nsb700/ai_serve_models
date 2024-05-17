from fastapi.testclient import TestClient
from webapp.main import app

client = TestClient(app)

def test_the_index():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == "Hello World"






