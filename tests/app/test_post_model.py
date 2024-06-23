# test_when_body_contains_id_and_name_then_return_200_status_code
# test_when_body_contains_unassigned_id_and_name_then_return_assigned_id
# test_when_body_contains_assigned_id_and_name_then_return_updated_model
from fastapi.testclient import TestClient


def test_when_body_contains_id_and_name_then_return_200_status_code(client: TestClient, not_existing_id_str_value):
    ID_TO_POST = not_existing_id_str_value
    NAME_TO_POST = "SOME_NAME_TO_POST"
    BODY = {"id": ID_TO_POST, "name": NAME_TO_POST}

    response = client.post("/uml-models", json=BODY)

    assert response.status_code == 200
