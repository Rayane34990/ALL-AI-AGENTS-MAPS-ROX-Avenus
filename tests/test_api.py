import requests

def test_agents_endpoint():
    resp = requests.get('http://localhost:8000/agents')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    print('API /agents endpoint test passed.')
