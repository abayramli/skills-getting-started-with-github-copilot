from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_root_redirects_to_static():
    resp = client.get('/', follow_redirects=False)
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get('location') == '/static/index.html'


def test_get_activities():
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_success_and_duplicate():
    activity = 'Chess Club'
    email = 'test_student_unique@example.com'

    # Ensure signup succeeds first time
    resp = client.post(f'/activities/{activity}/signup', params={'email': email})
    assert resp.status_code == 200
    assert f'Signed up {email}' in resp.json().get('message', '')

    # Duplicate signup returns 400
    resp2 = client.post(f'/activities/{activity}/signup', params={'email': email})
    assert resp2.status_code == 400


def test_remove_participant():
    activity = 'Programming Class'
    email = 'temp_remove_student@example.com'

    # Sign up then remove
    r1 = client.post(f'/activities/{activity}/signup', params={'email': email})
    assert r1.status_code == 200

    r2 = client.delete(f'/activities/{activity}/signup', params={'email': email})
    assert r2.status_code == 200
    assert f'Removed {email}' in r2.json().get('message', '')
