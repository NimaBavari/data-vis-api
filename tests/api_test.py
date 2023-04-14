from fastapi.testclient import TestClient

from src import app

client = TestClient(app)

def test_stats_for_nonexistent_batch() -> None:
    resp = client.get("/statistics/123e4567-e89b-12d3-a456-426614174000")
    resp_data, status_code = resp.json()
    assert status_code == 404
    assert resp_data == {"message": "Assessment batch not found"}
