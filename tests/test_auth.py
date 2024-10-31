from tests.conftest import async_client, client


async def test_user_can_register():
    response = client.post('/auth/register', json={
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
        })

    assert response.status_code == 201, "Failed"
