# FILE: tests/test_calculations_integration.py
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_calculation_bread_flow():
    # ADD
    create_resp = client.post(
        "/calculations/",
        json={"operation": "add", "operand1": 2, "operand2": 3},
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    calc_id = created["id"]
    assert created["result"] == 5

    # READ
    read_resp = client.get(f"/calculations/{calc_id}")
    assert read_resp.status_code == 200
    read_data = read_resp.json()
    assert read_data["id"] == calc_id
    assert read_data["result"] == 5

    # BROWSE
    browse_resp = client.get("/calculations/")
    assert browse_resp.status_code == 200
    items = browse_resp.json()
    assert any(c["id"] == calc_id for c in items)

    # EDIT
    update_resp = client.put(
        f"/calculations/{calc_id}",
        json={"operation": "add", "operand1": 4, "operand2": 6},
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["result"] == 10

    # DELETE
    delete_resp = client.delete(f"/calculations/{calc_id}")
    assert delete_resp.status_code == 204

    # Ensure it is gone
    read_after_delete = client.get(f"/calculations/{calc_id}")
    assert read_after_delete.status_code == 404


def test_invalid_operation_returns_error():
    resp = client.post(
        "/calculations/",
        json={"operation": "power", "operand1": 2, "operand2": 3},
    )
    assert resp.status_code == 400
