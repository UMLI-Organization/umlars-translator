# # test_when_get_model_for_not_existing_id_then_return_404_status_code_and_message
# # test_when_get_model_for_existing_id_then_return_200_status_code
# # test_when_get_model_for_existing_id_then_return_model
# # test_when_new_test_run_db_is_empty
# from fastapi.testclient import TestClient


# def test_when_get_model_for_not_existing_id_then_return_404_status_code_and_detail(client: TestClient, not_existing_model_id):
#     ID_TO_GET = not_existing_model_id
    
#     response = client.get(f"/uml-models/{ID_TO_GET}")
    
#     assert response.status_code == 404
#     assert response.json() == {"detail": f"Model with ID: {ID_TO_GET} not found"}


# def test_when_get_model_for_existing_id_then_return_200_status_code(client: TestClient, single_model_in_db, existing_model_id_str_value):
#     ID_TO_GET = existing_model_id_str_value

#     response = client.get(f"/uml-models/{ID_TO_GET}")
    
#     assert response.status_code == 200


# def test_when_get_model_for_existing_id_then_return_model(client: TestClient, single_model_in_db, existing_model_id_str_value, existing_model_name):
#     ID_TO_GET = existing_model_id_str_value

#     response = client.get(f"/uml-models/{ID_TO_GET}")
    
#     assert response.json() == {"id": ID_TO_GET, "name": existing_model_name}



# def test_when_new_test_run_db_is_empty(client: TestClient, existing_model_id_str_value):
#     ID_TO_GET = existing_model_id_str_value

#     response = client.get(f"/uml-models/{ID_TO_GET}")
    
#     assert response.status_code == 404
