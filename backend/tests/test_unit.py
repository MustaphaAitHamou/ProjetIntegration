import pytest
from fastapi.testclient import TestClient
from app import app, SessionLocal, Base, engine, User

client = TestClient(app)

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    # Création du schéma en mémoire pour tests
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user_direct():
    db = SessionLocal()
    user = User(email='unit@test.com', password='pwd', is_admin=False)
    db.add(user)
    db.commit()
    assert user.id is not None
    db.close()