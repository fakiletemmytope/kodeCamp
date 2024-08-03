from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res)
    assert res.status_code == 200
    assert res.json() == {"message": "Hello Bigger Applications!"}

def test_task_create():
    res = client.post("/task", data={'title': 'value',
                                     'description': 'value'},
                                    )
    assert res.json() == {'detail': 'Token required'}

    res = client.post("/task", data={'title': 'value',
                                     'description': 'value'},
                                    headers ={"authorization":"bearer jarhrhrjo"})
    assert res.json() == {'detail': 'Expired Token'}
