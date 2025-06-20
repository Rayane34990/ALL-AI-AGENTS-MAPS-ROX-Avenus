import requests

def test_agent_detail():
    # Assumes at least one agent exists with id=1
    resp = requests.get('http://localhost:8000/agents/1')
    assert resp.status_code == 200
    data = resp.json()
    assert 'name' in data
    print('Agent detail API test passed.')
