import subprocess

def test_replicate_ingest():
    result = subprocess.run(['python', 'ingest/replicate_ingest.py'], capture_output=True, text=True)
    assert 'Replicate.com ingestion complete' in result.stdout
    print('Replicate.com ingestion test passed.')
