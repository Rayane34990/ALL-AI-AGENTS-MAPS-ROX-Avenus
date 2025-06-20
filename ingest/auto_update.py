import subprocess
import time
import sys

def run_script(script):
    print(f"Running {script}...")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == "__main__":
    # List all ingestion scripts
    scripts = [
        'ingest/github_ingest.py',
        'ingest/arxiv_ingest.py',
        'ingest/pwc_ingest.py',
        'ingest/hf_ingest.py',
        # Add more as needed
    ]
    for script in scripts:
        run_script(script)
    # Deduplication/classification
    run_script('dedup/dedup.py')
    print("All ingestion and deduplication complete.")
