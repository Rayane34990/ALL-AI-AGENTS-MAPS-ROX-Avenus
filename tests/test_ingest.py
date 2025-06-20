import subprocess
import os

def test_github_ingest():
    result = subprocess.run(['python', 'ingest/github_ingest.py'], capture_output=True, text=True)
    assert 'GitHub ingestion complete' in result.stdout
    print('GitHub ingestion test passed.')
