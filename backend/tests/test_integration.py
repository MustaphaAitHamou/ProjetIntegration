import pytest
from fastapi.testclient import TestClient
from app import app, Base, engine
from sqlalchemy.orm import sessionmaker

TestSessionLocal = sessionmaker(bind=engine)
client = TestClient(app)

@pytest.fixture(scope='module', autouse=True)
def init_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_api_create_and_get_users():
    # Création via endpoint
    response = client.post('/users', json={'email': 'int@test.com', 'password': 'pwd'})
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'int@test.com'

    # Lecture via endpoint
    response = client.get('/users')
    assert response.status_code == 200
    users = response.json()
    assert any(u['email'] == 'int@test.com' for u in users)