# # test_when_body_contains_id_and_name_then_return_200_status_code
# # test_when_body_contains_unassigned_id_and_name_then_return_assigned_id
# # test_when_body_contains_assigned_id_and_name_then_return_updated_model
# from fastapi.testclient import TestClient


# def test_when_body_contains_id_and_name_then_return_200_status_code(client: TestClient) -> None:
#     # Given
#     body = {
#         "id": "1",
#         "name": "test"
#     }

#     # When
#     response = client.post("/uml-models", json=body)

#     # Then
#     assert response.status_code == 200
#     assert response.json() == body