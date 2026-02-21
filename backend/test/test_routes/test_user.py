def test_create_user(client):
    data = {
        "email": "omejesixtus@gmail.com", "password": "Nnanna"
    }
    response = client.post("/users/", json=data)

    assert response.status_code == 201
    assert response.json()["email"] == "omejesixtus@gmail.com"