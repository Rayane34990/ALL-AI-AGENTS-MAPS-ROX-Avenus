import subprocess

def test_rapidapi_ingest():
    result = subprocess.run(['python', 'ingest/rapidapi_ingest.py'], capture_output=True, text=True)
    assert 'RapidAPI ingestion complete' in result.stdout
    print('RapidAPI ingestion test passed.')
