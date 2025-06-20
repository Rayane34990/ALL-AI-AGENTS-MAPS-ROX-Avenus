import subprocess

def test_tfhub_ingest():
    result = subprocess.run(['python', 'ingest/tfhub_ingest.py'], capture_output=True, text=True)
    assert 'TensorFlow Hub ingestion complete' in result.stdout
    print('TensorFlow Hub ingestion test passed.')
