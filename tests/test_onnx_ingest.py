import subprocess

def test_onnx_ingest():
    result = subprocess.run(['python', 'ingest/onnx_ingest.py'], capture_output=True, text=True)
    assert 'ONNX Model Zoo ingestion complete' in result.stdout
    print('ONNX Model Zoo ingestion test passed.')
